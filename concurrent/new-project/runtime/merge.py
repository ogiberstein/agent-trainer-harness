"""Git worktree and branch merge management for concurrent workers."""

import os
import subprocess

from state import Task


class MergeConflict(Exception):
    def __init__(self, task: Task, details: str):
        self.task = task
        self.details = details
        super().__init__(f"Merge conflict on {task.id}: {details}")


def create_worktree(project_path: str, worktree_path: str, branch: str):
    """Create a git worktree on a new branch for isolated worker execution."""
    os.makedirs(os.path.dirname(worktree_path), exist_ok=True)
    subprocess.run(
        ["git", "worktree", "add", "-b", branch, worktree_path],
        cwd=project_path,
        check=True,
        capture_output=True,
        text=True,
    )


def merge_branch(task: Task, project_path: str):
    """Merge a worker's branch back into the main branch.

    Raises MergeConflict if the merge fails.
    """
    branch = f"agent/{task.role}/{task.id}-{task.slug}"
    result = subprocess.run(
        ["git", "merge", "--no-ff", branch, "-m", f"Merge {task.id}: {task.title}"],
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        subprocess.run(["git", "merge", "--abort"], cwd=project_path, capture_output=True)
        raise MergeConflict(task, result.stderr)


def cleanup_worktree(task: Task, project_path: str):
    """Remove worktree and delete the branch after successful merge."""
    worktree_path = os.path.join(project_path, ".worktrees", task.id)

    if os.path.isdir(worktree_path):
        subprocess.run(
            ["git", "worktree", "remove", "--force", worktree_path],
            cwd=project_path,
            capture_output=True,
        )

    branch = f"agent/{task.role}/{task.id}-{task.slug}"
    subprocess.run(
        ["git", "branch", "-d", branch],
        cwd=project_path,
        capture_output=True,
    )


def cleanup_all_worktrees(project_path: str):
    """Remove all worker worktrees. Used during abort/cleanup."""
    worktrees_dir = os.path.join(project_path, ".worktrees")
    if not os.path.isdir(worktrees_dir):
        return

    subprocess.run(
        ["git", "worktree", "prune"],
        cwd=project_path,
        capture_output=True,
    )

    for entry in os.listdir(worktrees_dir):
        path = os.path.join(worktrees_dir, entry)
        if os.path.isdir(path):
            subprocess.run(
                ["git", "worktree", "remove", "--force", path],
                cwd=project_path,
                capture_output=True,
            )
