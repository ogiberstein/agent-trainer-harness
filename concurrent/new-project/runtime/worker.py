"""Wraps a single Claude Code CLI invocation in an isolated git worktree."""

import os
import subprocess
from typing import Optional

from config import Config
from state import Task


class Worker:
    """Runs a Claude Code CLI worker for a single task on an isolated branch."""

    def __init__(self, task: Task, config: Config, project_path: str):
        self.task = task
        self.config = config
        self.project_path = project_path
        self.branch = f"agent/{task.role}/{task.id}-{task.slug}"
        self.worktree = os.path.join(project_path, ".worktrees", task.id)
        self.output_path = os.path.join(self.worktree, ".worker_output.txt")
        self._process: Optional[subprocess.Popen] = None
        self._out_file = None

    def start(self):
        """Create worktree and spawn headless Claude Code process."""
        _create_worktree(self.project_path, self.worktree, self.branch)

        role_prompt = _load_role_prompt(self.project_path, self.task.role)
        task_prompt = _build_task_prompt(self.task, self.project_path)

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        self._out_file = open(self.output_path, "w")

        self._process = subprocess.Popen(
            [
                "claude",
                "--print",
                "--model", self.config.model,
                "--systemPrompt", role_prompt,
                "--allowedTools", "Edit,Write,Bash,Read",
                "-p", task_prompt,
            ],
            cwd=self.worktree,
            stdout=self._out_file,
            stderr=subprocess.STDOUT,
        )

    def wait(self) -> int:
        """Block until the worker process exits. Returns exit code."""
        if self._process is None:
            raise RuntimeError("Worker not started")
        try:
            return self._process.wait(timeout=self.config.worker_timeout)
        finally:
            if self._out_file:
                self._out_file.close()
                self._out_file = None

    @property
    def succeeded(self) -> bool:
        return self._process is not None and self._process.returncode == 0


def _create_worktree(project_path: str, worktree_path: str, branch: str):
    """Create a git worktree for isolated concurrent work."""
    subprocess.run(
        ["git", "worktree", "add", "-b", branch, worktree_path],
        cwd=project_path,
        check=True,
        capture_output=True,
    )


def _load_role_prompt(project_path: str, role: str) -> str:
    """Load the harness role prompt file for this worker's role."""
    prompt_path = os.path.join(project_path, "harness", "agents", f"{role}.md")
    if not os.path.isfile(prompt_path):
        raise FileNotFoundError(f"Role prompt not found: {prompt_path}")
    with open(prompt_path) as f:
        return f.read()


def _build_task_prompt(task: Task, project_path: str) -> str:
    """Build the task-specific prompt passed to the Claude Code worker."""
    parts = [
        f"# Task: {task.title}",
        f"Task ID: {task.id}",
        f"Phase: {task.phase}",
        f"Priority: {task.priority}",
    ]
    if task.file_scope:
        parts.append(f"File scope: {', '.join(task.file_scope)}")
    if task.acceptance:
        parts.append(f"\n## Acceptance Criteria\n{task.acceptance}")
    if task.dependencies:
        parts.append(f"Dependencies: {', '.join(task.dependencies)}")

    brief = _load_brief(project_path)
    if brief:
        parts.append(f"\n## Project Context (from BRIEF.md)\n{brief}")

    parts.append("\n## Instructions")
    parts.append("Read AGENTS.md first for harness rules and protection policy.")
    parts.append("Read STATUS.md for current project state.")
    parts.append("Complete this task according to the acceptance criteria.")
    parts.append("Commit your changes with a clear message referencing the task ID.")
    parts.append("Do not modify files outside the specified file scope unless necessary.")

    return "\n".join(parts)


def _load_brief(project_path: str) -> str:
    """Load a truncated BRIEF.md so workers know what the project is about."""
    brief_path = os.path.join(project_path, "BRIEF.md")
    if not os.path.isfile(brief_path):
        return ""
    with open(brief_path) as f:
        content = f.read()
    if len(content) > 2000:
        return content[:2000] + "\n...(truncated)"
    return content
