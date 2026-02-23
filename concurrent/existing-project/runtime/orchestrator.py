"""Main orchestrator loop for Concurrent mode.

Reads harness state, dispatches workers, enforces gates, merges branches,
and advances phases until the project is complete or a blocking failure occurs.
"""

import os
import time

from config import Config
from gates import gate_check
from merge import merge_branch, cleanup_worktree, MergeConflict
from notifier import notify
from state import State, Task, PHASE_ORDER
from telemetry import init_run, log_event, log_run_complete
from worker import Worker

# Default role assignments per phase (used when tracker board is empty)
PHASE_ROLES = {
    "requirements": [("TASK-REQ-001", "Product requirements", "product-manager")],
    "design": [
        ("TASK-DES-001", "UI/UX specification", "designer"),
        ("TASK-DES-002", "Architecture specification", "designer"),
    ],
    "implementation": [
        ("TASK-IMP-001", "Backend implementation", "fullstack-engineer"),
        ("TASK-IMP-002", "Frontend implementation", "frontend-engineer"),
    ],
    "qa": [("TASK-QA-001", "Quality audit and testing", "qa-engineer")],
    "documentation": [("TASK-DOC-001", "Project documentation", "documentation-writer")],
    "growth": [("TASK-GRO-001", "Growth strategy and execution plan", "growth-strategist")],
    "review": [("TASK-REV-001", "Final delivery review", "orchestrator")],
}


def run(project_path: str, config: Config, dry_run: bool = False):
    """Main orchestrator entry point."""
    state = State(project_path)
    run_id = init_run(project_path)
    _run_start = time.time()
    notify(config, f"Starting concurrent run {run_id}. Phase: {state.current_phase}", "info")

    while state.current_phase != "complete":
        if state.current_phase in config.skip_phases:
            notify(config, f"Skipping phase: {state.current_phase}", "info")
            state.advance_phase()
            continue

        # Check for human checkpoint
        if _checkpoint_exists(project_path):
            notify(config, "Paused at checkpoint. Run with --resume to continue.", "warning")
            _wait_for_resume(project_path)

        # Get or generate tasks for current phase
        tasks = state.get_ready_tasks()
        if not tasks:
            tasks = _generate_phase_tasks(state.current_phase, project_path)
            if not tasks:
                notify(config, f"No tasks for phase {state.current_phase}. Advancing.", "info")
                state.advance_phase()
                continue
            state.add_tasks(tasks)
            tasks = state.get_ready_tasks()

        if dry_run:
            print(f"\n[DRY RUN] Phase: {state.current_phase}")
            for t in tasks:
                print(f"  - {t.id}: {t.title} (role: {t.role})")
            state.advance_phase()
            continue

        # Dispatch workers (up to max_workers)
        batch = tasks[: config.max_workers]
        workers: list[Worker] = []

        for task in batch:
            notify(config, f"Dispatching: {task.id} ({task.title}) -> {task.role}", "info")
            log_event("task_dispatch", {}, project_path, task_id=task.id, role=task.role, phase=task.phase, model=config.model)
            w = Worker(task, config, project_path)
            try:
                w.start()
                workers.append(w)
                state.mark_in_progress(task)
            except Exception as e:
                notify(config, f"Failed to start worker for {task.id}: {e}", "error")
                log_event("task_fail", {"error": str(e)[:200]}, project_path, task_id=task.id, role=task.role, phase=task.phase)
                state.mark_blocked(task, str(e))

        # Wait for workers and evaluate gates
        for w in workers:
            task_start = time.time()
            try:
                w.wait()
            except Exception as e:
                dur = time.time() - task_start
                notify(config, f"Worker {w.task.id} failed: {e}", "error")
                log_event("task_fail", {"error": str(e)[:200]}, project_path, task_id=w.task.id, role=w.task.role, phase=w.task.phase, duration_s=dur)
                state.mark_blocked(w.task, str(e))
                continue

            dur = time.time() - task_start
            result = gate_check(w.task, w.output_path, config, project_path)

            if result.passed:
                log_event("gate_pass", {"summary": result.summary}, project_path, task_id=w.task.id, role=w.task.role, phase=w.task.phase, duration_s=dur, model=config.model)
                try:
                    merge_branch(w.task, project_path)
                    cleanup_worktree(w.task, project_path)
                    state.mark_done(w.task)
                    log_event("task_complete", {}, project_path, task_id=w.task.id, role=w.task.role, phase=w.task.phase, duration_s=dur)
                    notify(config, f"PASS + merged: {w.task.id}", "info")
                except MergeConflict as mc:
                    notify(config, f"Merge conflict on {w.task.id}: {mc.details[:200]}", "error")
                    log_event("task_fail", {"error": f"merge_conflict: {mc.details[:200]}"}, project_path, task_id=w.task.id, role=w.task.role, phase=w.task.phase, duration_s=dur)
                    _handle_failure(w.task, f"Merge conflict: {mc.details}", state, config, project_path)
            else:
                log_event("gate_fail", {"summary": result.summary, "missing": result.missing}, project_path, task_id=w.task.id, role=w.task.role, phase=w.task.phase, duration_s=dur, model=config.model)
                notify(config, f"FAIL: {w.task.id} — {result.summary}", "warning")
                _handle_failure(w.task, result.summary, state, config, project_path)

        # Check if phase is complete
        if state.phase_complete():
            log_event("phase_advance", {"from": state.current_phase}, project_path, phase=state.current_phase)
            notify(config, f"Phase complete: {state.current_phase}", "info")
            state.advance_phase()

            # Human checkpoint after requirements (configurable)
            if state.current_phase == "design" and config.checkpoint_after_requirements:
                notify(config, "Requirements phase complete. Review specs/requirements.md and resume.", "warning")
                _create_checkpoint(project_path)

    total_duration = time.time() - _run_start
    log_run_complete(project_path, total_duration)
    notify(config, "All phases complete. Project delivery finished.", "complete")
    state.log_decision(
        "Concurrent run complete",
        "All phases passed gate checks. Review deliverables and run /validate-harness.",
    )


def _generate_phase_tasks(phase: str, project_path: str) -> list[Task]:
    """Generate default tasks for a phase based on PHASE_ROLES."""
    role_defs = PHASE_ROLES.get(phase, [])
    tasks = []
    for task_id, title, role in role_defs:
        prompt_path = os.path.join(project_path, "harness", "agents", f"{role}.md")
        if not os.path.isfile(prompt_path):
            continue
        tasks.append(Task(id=task_id, title=title, role=role, phase=phase))
    return tasks


def _handle_failure(task: Task, evidence: str, state: State, config: Config, project_path: str):
    """Handle a task failure: retry or escalate."""
    task.retries += 1
    if task.retries > config.max_retries:
        state.mark_blocked(task, evidence)
        notify(config, f"BLOCKED (max retries): {task.id} — {evidence[:200]}", "error")
        _create_checkpoint(project_path)
    else:
        fix_task = Task(
            id=f"{task.id}-fix{task.retries}",
            title=f"Fix: {task.title}",
            role=task.role,
            phase=task.phase,
            acceptance=f"Fix the following failure:\n{evidence}",
            retries=task.retries,
        )
        state.add_tasks([fix_task])
        notify(config, f"Retry {task.retries}/{config.max_retries}: {task.id}", "info")


def _checkpoint_exists(project_path: str) -> bool:
    return os.path.exists(os.path.join(project_path, "runtime", ".checkpoint"))


def _create_checkpoint(project_path: str):
    os.makedirs(os.path.join(project_path, "runtime"), exist_ok=True)
    with open(os.path.join(project_path, "runtime", ".checkpoint"), "w") as f:
        f.write(f"Paused at {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}\n")


def _wait_for_resume(project_path: str):
    """Block until checkpoint file is removed (by --resume flag or manual deletion)."""
    checkpoint = os.path.join(project_path, "runtime", ".checkpoint")
    while os.path.exists(checkpoint):
        time.sleep(5)
