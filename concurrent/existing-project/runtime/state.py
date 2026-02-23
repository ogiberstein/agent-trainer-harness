"""Parse and update harness markdown state files (STATUS.md, tracker.md, DECISIONS.md)."""

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
        self._tracker_path = os.path.join(project_path, "operations", "tracker.md")
        self._decisions_path = os.path.join(project_path, "DECISIONS.md")
        self.tasks: list[Task] = []
        self._current_phase: str = "requirements"
        self._status_raw: str = ""
        self._load_status()
        self._load_tracker()

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

    def _load_tracker(self):
        """Parse task cards from tracker.md Board sections.

        Reads cards in the format:
            - [ ] [CARD-XXX] Title
              - Owner: role
              - Status: ready | in_progress | done | blocked
              - Phase: phase_name
        """
        self.tasks = []
        if not os.path.isfile(self._tracker_path):
            return

        content = _read(self._tracker_path)
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

        section_map = _parse_board_sections(content)

        for section_status, section_text in section_map.items():
            for m in card_pattern.finditer(section_text):
                task = Task(
                    id=m.group(1).strip(),
                    title=m.group(2).strip(),
                    role=(m.group(3) or "").strip(),
                    priority=(m.group(4) or "P1").strip(),
                    phase=(m.group(5) or self._current_phase).strip().lower(),
                    acceptance=(m.group(9) or "").strip(),
                    status=section_status,
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
        self._write_tracker()

    def mark_in_progress(self, task: Task):
        task.status = "in_progress"
        self._write_tracker()

    def mark_done(self, task: Task):
        task.status = "done"
        self._write_tracker()

    def mark_blocked(self, task: Task, evidence: str):
        task.status = "blocked"
        task.evidence = evidence
        self._write_tracker()

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

    def _write_tracker(self):
        """Write current task state to tracker.md using the Board card format."""
        sections = {
            "ready": [],
            "in_progress": [],
            "done": [],
            "blocked": [],
        }
        for t in self.tasks:
            sections.setdefault(t.status, []).append(t)

        board = "# Operations Tracker\n\n"
        board += "Single file for task board, project dashboard, workflow state, and escalation inbox.\n"
        board += "Managed by the concurrent orchestrator — do not edit manually while a run is active.\n\n"
        board += "---\n\n## Board\n\n"

        board += "### Ready Queue\n"
        for t in sections["ready"]:
            board += _format_card(t)
        board += "\n"

        board += "### In Progress\n"
        for t in sections["in_progress"]:
            board += _format_card(t)
        board += "\n"

        board += "### Blocked\n"
        for t in sections["blocked"]:
            board += _format_card(t)
            if t.evidence:
                board += f"  - Evidence: {t.evidence[:200]}\n"
        board += "\n"

        board += "### Done\n"
        for t in sections["done"]:
            board += _format_card(t)
        board += "\n"

        os.makedirs(os.path.dirname(self._tracker_path), exist_ok=True)
        _write(self._tracker_path, board)


def _format_card(task: Task) -> str:
    """Format a single task as a tracker.md card."""
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


def _parse_board_sections(content: str) -> dict[str, str]:
    """Map board section headers to their status and text content."""
    mapping = {
        "Ready Queue": "ready",
        "Backlog": "ready",
        "In Progress": "in_progress",
        "Review": "in_progress",
        "Blocked": "blocked",
        "Done": "done",
        "Awaiting Merge": "in_progress",
    }
    result = {}
    section_pattern = re.compile(r"^###\s+(.+)$", re.MULTILINE)
    matches = list(section_pattern.finditer(content))

    for i, m in enumerate(matches):
        header = m.group(1).strip()
        status = mapping.get(header)
        if status is None:
            continue
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        result[status] = result.get(status, "") + content[start:end]

    return result


def _read(path: str) -> str:
    with open(path) as f:
        return f.read()


def _write(path: str, content: str):
    with open(path, "w") as f:
        f.write(content)


def _append(path: str, content: str):
    with open(path, "a") as f:
        f.write(content)
