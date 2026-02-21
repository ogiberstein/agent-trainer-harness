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
        self._load_status()
        self._load_tracker()

    @property
    def current_phase(self) -> str:
        return self._current_phase

    def _load_status(self):
        """Parse current phase from STATUS.md."""
        if not os.path.isfile(self._status_path):
            return
        content = _read(self._status_path)
        match = re.search(r"Current Phase[:\s]*(\w+)", content, re.IGNORECASE)
        if match:
            self._current_phase = match.group(1).lower()

    def _load_tracker(self):
        """Parse task cards from tracker.md.

        TODO: implement full markdown card parsing.
        This is a stub that returns an empty task list — the orchestrator
        will generate phase tasks when the board is empty.
        """
        self.tasks = []

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
        """Overwrite STATUS.md with current phase.

        TODO: preserve existing STATUS.md structure and update only the phase field.
        This stub writes a minimal STATUS.md.
        """
        content = f"""# Project Status

## Current Phase
{self._current_phase}

## Last Updated
{datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")} by orchestrator (concurrent mode)
"""
        _write(self._status_path, content)

    def _write_tracker(self):
        """Write current task state to tracker.md.

        TODO: implement full tracker.md card serialization.
        This stub appends task summaries to the board sections.
        """
        # Stub: will be implemented with full markdown card format
        pass


def _read(path: str) -> str:
    with open(path) as f:
        return f.read()


def _write(path: str, content: str):
    with open(path, "w") as f:
        f.write(content)


def _append(path: str, content: str):
    with open(path, "a") as f:
        f.write(content)
