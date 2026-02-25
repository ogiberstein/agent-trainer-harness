"""Parse and update harness markdown state files (STATUS.md, DECISIONS.md)."""

import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

PHASE_ORDER = [
    "requirements",
    "design",
    "implementation",
    "qa",
    "documentation",
    "growth",
    "review",
    "complete",
]


@dataclass
class Task:
    id: str
    title: str
    role: str
    phase: str
    status: str = "ready"  # ready | in_progress | done | blocked
    priority: str = "P1"
    dependencies: list[str] = field(default_factory=list)
    file_scope: list[str] = field(default_factory=list)
    acceptance: str = ""
    retries: int = 0
    slug: str = ""
    evidence: str = ""

    def __post_init__(self):
        if not self.slug:
            self.slug = re.sub(r"[^a-z0-9]+", "-", self.title.lower()).strip("-")[:40]


class State:
    """Reads and writes harness state from markdown files."""

    def __init__(self, project_path: str):
        self.project_path = project_path
        self._status_path = os.path.join(project_path, "STATUS.md")
        self._decisions_path = os.path.join(project_path, "DECISIONS.md")
        self.tasks: list[Task] = []
        self._current_phase: str = "requirements"
        self._status_raw: str = ""
        self._load_status()
        self._load_tasks()

    @property
    def current_phase(self) -> str:
        return self._current_phase

    def _load_status(self):
        """Parse current phase from STATUS.md, preserving the raw content for incremental updates."""
        if not os.path.isfile(self._status_path):
            return
        self._status_raw = _read(self._status_path)
        match = re.search(r"Current Phase[:\s]*(\w+)", self._status_raw, re.IGNORECASE)
        if match:
            self._current_phase = match.group(1).lower()

    def _load_tasks(self):
        """Parse task cards from the ## Tasks section of STATUS.md.

        Reads cards in the format:
            - [ ] [CARD-XXX] Title
              - Owner: role
              - Status: ready | in_progress | done | blocked
              - Phase: phase_name
        """
        self.tasks = []
        if not os.path.isfile(self._status_path):
            return

        content = self._status_raw
        tasks_match = re.search(r"^## Tasks\s*\n(.*?)(?=^## |\Z)", content, re.MULTILINE | re.DOTALL)
        if not tasks_match:
            return

        tasks_section = tasks_match.group(1)
        card_pattern = re.compile(
            r"- \[[ x]\] \[([^\]]+)\]\s+(.+)\n"
            r"(?:\s+- Owner:\s*(.+)\n)?"
            r"(?:\s+- Priority:\s*(.+)\n)?"
            r"(?:\s+- Phase:\s*(.+)\n)?"
            r"(?:\s+- Dependencies:\s*(.+)\n)?"
            r"(?:\s+- File Scope:\s*(.+)\n)?"
            r"(?:\s+- Branch/Worktree:\s*(.+)\n)?"
            r"(?:\s+- Acceptance:\s*(.+)\n)?"
            r"(?:\s+- Status:\s*(.+)\n)?",
            re.MULTILINE,
        )

        for m in card_pattern.finditer(tasks_section):
            status_str = (m.group(10) or "ready").strip().lower()
            task = Task(
                id=m.group(1).strip(),
                title=m.group(2).strip(),
                role=(m.group(3) or "").strip(),
                priority=(m.group(4) or "P1").strip(),
                phase=(m.group(5) or self._current_phase).strip().lower(),
                acceptance=(m.group(9) or "").strip(),
                status=status_str,
            )
            deps = (m.group(6) or "").strip()
            if deps and deps.lower() != "none":
                task.dependencies = [d.strip() for d in deps.split(",")]
            scope = (m.group(7) or "").strip()
            if scope:
                task.file_scope = [s.strip() for s in scope.split(",")]
            self.tasks.append(task)

    def get_ready_tasks(self) -> list[Task]:
        return [t for t in self.tasks if t.status == "ready" and t.phase == self._current_phase]

    def add_tasks(self, tasks: list[Task]):
        self.tasks.extend(tasks)
        self._write_tasks()

    def mark_in_progress(self, task: Task):
        task.status = "in_progress"
        self._write_tasks()

    def mark_done(self, task: Task):
        task.status = "done"
        self._write_tasks()

    def mark_blocked(self, task: Task, evidence: str):
        task.status = "blocked"
        task.evidence = evidence
        self._write_tasks()

    def phase_complete(self) -> bool:
        phase_tasks = [t for t in self.tasks if t.phase == self._current_phase]
        if not phase_tasks:
            return False
        return all(t.status == "done" for t in phase_tasks)

    def advance_phase(self):
        idx = PHASE_ORDER.index(self._current_phase)
        if idx + 1 < len(PHASE_ORDER):
            self._current_phase = PHASE_ORDER[idx + 1]
            self._write_status()

    def log_decision(self, title: str, rationale: str):
        """Append a decision entry to DECISIONS.md."""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        entry = f"\n## DEC-AUTO: {title}\n- Date: {timestamp}\n- Source: Concurrent orchestrator\n- Rationale: {rationale}\n"
        _append(self._decisions_path, entry)

    def _write_status(self):
        """Update STATUS.md preserving existing content where possible.

        If the file has a 'Current Phase' line, only that line and the
        'Last Updated' line are replaced. Otherwise, the full template is written.
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

        if self._status_raw and re.search(r"Current Phase", self._status_raw, re.IGNORECASE):
            updated = re.sub(
                r"(##\s*Current Phase\s*\n).*",
                rf"\g<1>{self._current_phase}",
                self._status_raw,
                count=1,
            )
            updated = re.sub(
                r"(##\s*Last Updated\s*\n).*",
                rf"\g<1>{timestamp} by orchestrator (concurrent mode)",
                updated,
                count=1,
            )
            self._status_raw = updated
        else:
            self._status_raw = (
                f"# Project Status\n\n"
                f"## Current Phase\n{self._current_phase}\n\n"
                f"## Last Updated\n{timestamp} by orchestrator (concurrent mode)\n\n"
                f"## Completed\n\n## In Progress\n\n## Blocked\n\n## Next Up\n\n## Risks\n"
            )

        _write(self._status_path, self._status_raw)

    def _write_tasks(self):
        """Write current task state to the ## Tasks section of STATUS.md."""
        task_lines = ""
        for t in self.tasks:
            task_lines += _format_card(t)
            if t.status == "blocked" and t.evidence:
                task_lines += f"  - Evidence: {t.evidence[:200]}\n"

        tasks_section = f"## Tasks\n\n{task_lines}\n"

        if re.search(r"^## Tasks\s*\n", self._status_raw, re.MULTILINE):
            self._status_raw = re.sub(
                r"^## Tasks\s*\n.*?(?=^## |\Z)",
                tasks_section,
                self._status_raw,
                count=1,
                flags=re.MULTILINE | re.DOTALL,
            )
        else:
            self._status_raw = self._status_raw.rstrip() + "\n\n" + tasks_section

        _write(self._status_path, self._status_raw)


def _format_card(task: Task) -> str:
    """Format a single task as a STATUS.md card."""
    check = "x" if task.status == "done" else " "
    card = f"- [{check}] [{task.id}] {task.title}\n"
    card += f"  - Owner: {task.role}\n"
    card += f"  - Priority: {task.priority}\n"
    card += f"  - Phase: {task.phase}\n"
    card += f"  - Dependencies: {', '.join(task.dependencies) if task.dependencies else 'none'}\n"
    card += f"  - File Scope: {', '.join(task.file_scope) if task.file_scope else 'n/a'}\n"
    card += f"  - Branch/Worktree: agent/{task.role}/{task.id}-{task.slug}\n"
    card += f"  - Acceptance: {task.acceptance or 'see phase gate criteria'}\n"
    card += f"  - Status: {task.status}\n"
    return card



def _read(path: str) -> str:
    with open(path) as f:
        return f.read()


def _write(path: str, content: str):
    with open(path, "w") as f:
        f.write(content)


def _append(path: str, content: str):
    with open(path, "a") as f:
        f.write(content)
