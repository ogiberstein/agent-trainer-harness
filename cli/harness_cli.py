#!/usr/bin/env python3
"""Standalone CLI for common harness operations.

Works in any mode (Lite/Full/Concurrent). Wraps runtime/ modules so
operators don't need to know the internal API.

Usage:
    python cli/harness_cli.py status             --project .
    python cli/harness_cli.py gate-check         --project . [--phase requirements]
    python cli/harness_cli.py phase-next         --project .
    python cli/harness_cli.py task list          --project .
    python cli/harness_cli.py task add           --project . --title "..." --role "..." --phase "..."
    python cli/harness_cli.py launch-concurrent  --project .
"""

import argparse
import json
import os
import subprocess
import sys

_CLI_DIR = os.path.dirname(os.path.abspath(__file__))
_RUNTIME_DIR = os.path.join(os.path.dirname(_CLI_DIR), "runtime")
if _RUNTIME_DIR not in sys.path:
    sys.path.insert(0, _RUNTIME_DIR)

from config import Config, load_config
from gates import gate_check, GateResult, GATE_CRITERIA
from state import State, Task, PHASE_ORDER


def cmd_status(args):
    """Print current phase and task summary from STATUS.md + tracker."""
    state = State(args.project)
    ready = [t for t in state.tasks if t.status == "ready"]
    in_progress = [t for t in state.tasks if t.status == "in_progress"]
    done = [t for t in state.tasks if t.status == "done"]
    blocked = [t for t in state.tasks if t.status == "blocked"]

    if args.json_output:
        print(json.dumps({
            "phase": state.current_phase,
            "tasks": {
                "ready": len(ready),
                "in_progress": len(in_progress),
                "done": len(done),
                "blocked": len(blocked),
            },
        }, indent=2))
    else:
        print(f"Phase: {state.current_phase}")
        print(f"Tasks: {len(ready)} ready | {len(in_progress)} in progress | {len(done)} done | {len(blocked)} blocked")
        if blocked:
            print(f"Blocked tasks:")
            for t in blocked:
                print(f"  - [{t.id}] {t.title}: {t.evidence or 'no evidence'}")


def cmd_gate_check(args):
    """Run LLM gate evaluation for a specific phase."""
    config_path = os.path.join(args.project, "runtime", "config.yaml")
    config = load_config(config_path) if os.path.isfile(config_path) else Config()

    phase = args.phase or State(args.project).current_phase
    if phase not in GATE_CRITERIA:
        print(f"Error: no gate criteria defined for phase '{phase}'")
        print(f"Available phases: {', '.join(GATE_CRITERIA.keys())}")
        sys.exit(1)

    dummy_task = Task(
        id=f"GATE-{phase.upper()}",
        title=f"Phase gate: {phase}",
        role="orchestrator",
        phase=phase,
        acceptance=GATE_CRITERIA[phase],
    )

    output_path = os.path.join(args.project, "STATUS.md")
    result = gate_check(dummy_task, output_path, config, args.project)

    if args.json_output:
        print(json.dumps({
            "phase": phase,
            "passed": result.passed,
            "summary": result.summary,
            "evidence": result.evidence,
            "missing": result.missing,
        }, indent=2))
    else:
        status = "PASSED" if result.passed else "FAILED"
        print(f"Gate [{phase}]: {status}")
        print(f"  Summary: {result.summary}")
        if result.evidence:
            print(f"  Evidence: {result.evidence}")
        if result.missing:
            print(f"  Missing: {', '.join(result.missing)}")


def cmd_phase_next(args):
    """Advance to the next phase if the current gate passes."""
    config_path = os.path.join(args.project, "runtime", "config.yaml")
    config = load_config(config_path) if os.path.isfile(config_path) else Config()
    state = State(args.project)

    current = state.current_phase
    if current == "complete":
        print("Already at 'complete' phase — nothing to advance.")
        return

    if not args.force:
        dummy_task = Task(
            id=f"GATE-{current.upper()}",
            title=f"Phase gate: {current}",
            role="orchestrator",
            phase=current,
            acceptance=GATE_CRITERIA.get(current, ""),
        )
        output_path = os.path.join(args.project, "STATUS.md")
        result = gate_check(dummy_task, output_path, config, args.project)

        if not result.passed:
            print(f"Gate [{current}] FAILED — cannot advance.")
            print(f"  Summary: {result.summary}")
            if result.missing:
                print(f"  Missing: {', '.join(result.missing)}")
            print("Use --force to override.")
            sys.exit(1)

    state.advance_phase()
    print(f"Phase advanced: {current} -> {state.current_phase}")


def cmd_task_list(args):
    """Print tasks from tracker.md."""
    state = State(args.project)

    if not state.tasks:
        print("No tasks found in operations/tracker.md")
        return

    if args.json_output:
        print(json.dumps([
            {
                "id": t.id,
                "title": t.title,
                "role": t.role,
                "phase": t.phase,
                "status": t.status,
                "priority": t.priority,
            }
            for t in state.tasks
        ], indent=2))
    else:
        for t in state.tasks:
            status_icon = {"ready": "○", "in_progress": "▶", "done": "✓", "blocked": "✗"}.get(t.status, "?")
            print(f"  {status_icon} [{t.id}] {t.title} ({t.role}, {t.phase}, {t.priority})")


def cmd_task_add(args):
    """Add a new task card to tracker.md."""
    state = State(args.project)

    existing_ids = {t.id for t in state.tasks}
    task_num = len(state.tasks) + 1
    task_id = args.id or f"CARD-{task_num:03d}"
    while task_id in existing_ids:
        task_num += 1
        task_id = f"CARD-{task_num:03d}"

    task = Task(
        id=task_id,
        title=args.title,
        role=args.role,
        phase=args.phase or state.current_phase,
        priority=args.priority or "P1",
        acceptance=args.acceptance or "",
    )

    state.add_tasks([task])
    print(f"Added task [{task.id}] '{task.title}' to {task.phase} phase, assigned to {task.role}")


def cmd_launch_concurrent(args):
    """Run preflight checks and launch the concurrent orchestrator as a background process."""
    _PREFLIGHT = os.path.join(_CLI_DIR, "preflight_concurrent.py")

    print("Running preflight checks...")
    result = subprocess.run(
        [sys.executable, _PREFLIGHT, "--project", args.project],
        capture_output=False,
    )
    if result.returncode != 0:
        print("\nPreflight failed. Fix the issues above before launching.")
        print("Fallback: use solo-autonomous Full mode (day-0-start.md).")
        sys.exit(1)

    req_file = os.path.join(args.project, "runtime", "requirements.txt")
    if os.path.isfile(req_file):
        print("\nInstalling runtime dependencies...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "-r", req_file],
            check=False,
        )

    run_py = os.path.join(args.project, "runtime", "run.py")
    log_path = os.path.join(args.project, "logs", "orchestrator.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    print(f"\nLaunching orchestrator (log: {log_path})...")
    with open(log_path, "w") as log_file:
        proc = subprocess.Popen(
            [sys.executable, run_py, "--project", args.project],
            stdout=log_file,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )

    print(f"Orchestrator started (PID: {proc.pid})")
    print(f"\nMonitor:")
    print(f"  tail -f {log_path}")
    print(f"  python3 cli/harness_cli.py --project {args.project} status")
    print(f"  cat {os.path.join(args.project, 'STATUS.md')}")
    print(f"\nPause:  touch {os.path.join(args.project, 'runtime', '.checkpoint')}")
    print(f"Resume: python3 {run_py} --project {args.project} --resume")
    print(f"Stop:   kill {proc.pid}")


def main():
    parser = argparse.ArgumentParser(description="Harness CLI — operate harness from any mode")
    parser.add_argument("--project", default=".", help="Path to harness-enabled project")
    parser.add_argument("--json", action="store_true", dest="json_output", help="JSON output")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Show current phase and task summary")

    gate_parser = subparsers.add_parser("gate-check", help="Run LLM gate evaluation")
    gate_parser.add_argument("--phase", help="Phase to check (default: current)")

    next_parser = subparsers.add_parser("phase-next", help="Advance to next phase")
    next_parser.add_argument("--force", action="store_true", help="Skip gate check")

    task_parser = subparsers.add_parser("task", help="Task operations")
    task_sub = task_parser.add_subparsers(dest="task_command", required=True)

    task_sub.add_parser("list", help="List all tasks")

    add_parser = task_sub.add_parser("add", help="Add a new task")
    add_parser.add_argument("--title", required=True, help="Task title")
    add_parser.add_argument("--role", required=True, help="Assigned role")
    add_parser.add_argument("--phase", help="Phase (default: current)")
    add_parser.add_argument("--priority", default="P1", help="Priority (default: P1)")
    add_parser.add_argument("--acceptance", default="", help="Acceptance criteria")
    add_parser.add_argument("--id", help="Custom task ID (auto-generated if omitted)")

    subparsers.add_parser("launch-concurrent", help="Preflight + launch concurrent orchestrator")

    args = parser.parse_args()

    args.project = os.path.abspath(args.project)
    if not os.path.isdir(args.project):
        print(f"Error: directory not found: {args.project}")
        sys.exit(2)

    if args.command == "status":
        cmd_status(args)
    elif args.command == "gate-check":
        cmd_gate_check(args)
    elif args.command == "phase-next":
        cmd_phase_next(args)
    elif args.command == "launch-concurrent":
        cmd_launch_concurrent(args)
    elif args.command == "task":
        if args.task_command == "list":
            cmd_task_list(args)
        elif args.task_command == "add":
            cmd_task_add(args)


if __name__ == "__main__":
    main()
