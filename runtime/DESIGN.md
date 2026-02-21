# Concurrent Mode — Design Document

## Overview

Concurrent mode enables fully autonomous, multi-agent project delivery. You define what to build (BRIEF.md + project profile), start the orchestrator, and walk away. The runtime spawns parallel Claude Code workers, enforces phase gates, merges code, and notifies you when done or blocked.

This is the third mode alongside Lite (solo dev, minimal overhead) and Full (human-in-the-loop, sequential phases).

| Mode | Human involvement | Concurrency | Best for |
|---|---|---|---|
| Lite | Every phase | None | Small fixes, solo dev |
| Full | Every gate approval | None | Feature work, team delivery |
| **Concurrent** | Requirements approval only | Parallel workers | MVP sprints, autonomous builds |

## Architecture

```
                    ┌──────────────────────────────────────────┐
                    │              Orchestrator                 │
                    │                                          │
                    │  1. Read STATUS.md + tracker.md           │
                    │  2. Identify ready tasks                  │
                    │  3. Spawn workers (up to max_workers)     │
                    │  4. Poll until workers finish             │
                    │  5. Run gate checks                       │
                    │  6. Merge or spawn fix tasks              │
                    │  7. Advance phase when all tasks pass     │
                    │  8. Repeat until complete or blocked      │
                    └──────────┬───────────────────────────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
         ┌────▼────┐    ┌─────▼────┐    ┌──────▼───┐
         │ Worker 1 │    │ Worker 2 │    │ Worker 3 │
         │ Backend  │    │ Frontend │    │ QA       │
         │ branch/  │    │ branch/  │    │ branch/  │
         │ worktree │    │ worktree │    │ worktree │
         └────┬─────┘    └────┬─────┘    └────┬─────┘
              │               │               │
              └───────────────┼───────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   Merge Steward    │
                    │  tests + gate →    │
                    │  merge or fix task │
                    └───────────────────┘
```

## Lifecycle

### Day 0 (human, ~30 minutes)

1. Fill in `BRIEF.md` with project scope, constraints, success criteria.
2. Customize `profiles/project-profile.yaml` (tech stack, quality bars).
3. Set `runtime/config.yaml` (model, max workers, notification webhook).
4. Run: `python runtime/run.py --project /path/to/project`

### Phase 1 — Requirements (semi-autonomous)

The orchestrator spawns a Product Manager worker to produce `specs/requirements.md`.

**Human checkpoint (default: enabled).** After the PM finishes, the orchestrator:
- Sends a notification (Telegram/Slack) with a summary of requirements.
- Creates a `runtime/.checkpoint` file.
- Pauses the loop.
- Resumes when the human deletes the checkpoint file (or runs `python runtime/run.py --resume`).

This is the one phase where human review matters most. All subsequent phases run autonomously.

### Phases 2-7 (fully autonomous)

The orchestrator advances through Design → Implementation → QA → Documentation → Growth (optional) → Final Review, following the same loop:

1. **Read state** — parse `STATUS.md` for current phase, `operations/tracker.md` for task board.
2. **Generate tasks** — if the board is empty for this phase, create task cards from the phase definition in the harness.
3. **Dispatch** — assign ready tasks to available workers (up to `max_workers`).
4. **Execute** — each worker runs as a headless Claude Code subprocess in its own git worktree.
5. **Gate check** — when a worker finishes, evaluate gate criteria using an LLM judge.
6. **Merge or retry** — on PASS, merge the branch to main. On FAIL, spawn a fix task with failure evidence.
7. **Phase complete** — when all tasks for the phase pass, update `STATUS.md` and advance.

### Completion

When all phases pass (or a phase is skipped per config), the orchestrator:
- Updates `STATUS.md` to `complete`.
- Writes a delivery summary to `DECISIONS.md`.
- Sends a final notification.
- Exits with code 0.

### Blocked / failure

If a task hits the retry ceiling (from `harness/routing-policy.md`), the orchestrator:
- Marks the task as `blocked` in `operations/tracker.md`.
- Sends a notification with failure context.
- Pauses the loop (same checkpoint mechanism as Requirements).
- The human can fix the issue manually and resume, or abort.

## Components

### orchestrator.py

Main dispatch loop. Runs until all phases complete or a blocking failure occurs.

```python
def run(project_path: str, config: Config):
    state = State(project_path)

    while state.current_phase != "complete":
        tasks = state.get_ready_tasks()

        if not tasks:
            tasks = generate_phase_tasks(state.current_phase, project_path)
            state.add_tasks(tasks)
            continue

        workers = []
        for task in tasks[:config.max_workers]:
            w = Worker(task, config, project_path)
            w.start()
            workers.append(w)
            state.mark_in_progress(task)

        for w in workers:
            w.wait()
            result = gate_check(w.task, w.output_path, config)

            if result.passed:
                merge(w.task, project_path)
                state.mark_done(w.task)
            else:
                if w.task.retries >= config.max_retries:
                    state.mark_blocked(w.task, result.evidence)
                    notify(config, f"BLOCKED: {w.task.id} — {result.summary}")
                    checkpoint_and_pause(project_path, config)
                else:
                    fix_task = create_fix_task(w.task, result.evidence)
                    state.add_tasks([fix_task])

        if state.phase_complete():
            state.advance_phase()
            if state.current_phase == "implementation" and config.checkpoint_after_requirements:
                notify(config, "Requirements complete. Review and resume.")
                checkpoint_and_pause(project_path, config)
```

### worker.py

Wraps a single Claude Code CLI invocation. Each worker runs in an isolated git worktree on its own branch.

```python
class Worker:
    def __init__(self, task: Task, config: Config, project_path: str):
        self.task = task
        self.branch = f"agent/{task.role}/{task.id}-{task.slug}"
        self.worktree = f"{project_path}/.worktrees/{task.id}"
        self.process = None

    def start(self):
        create_worktree(self.worktree, self.branch, project_path)
        role_prompt = read_file(f"harness/agents/{self.task.role}.md")
        task_prompt = build_task_prompt(self.task)

        self.process = subprocess.Popen(
            ["claude", "--print",
             "--model", self.config.model,
             "--systemPrompt", role_prompt,
             "--allowedTools", "Edit,Write,Bash,Read",
             "-p", task_prompt],
            cwd=self.worktree,
            stdout=open(f"{self.worktree}/.worker_output.txt", "w"),
            stderr=subprocess.STDOUT,
        )

    def wait(self):
        self.process.wait()
        self.output_path = f"{self.worktree}/.worker_output.txt"
```

### gates.py

Evaluates phase gate criteria by sending the criteria prose + produced artifacts to an LLM judge.

```python
def gate_check(task: Task, output_path: str, config: Config) -> GateResult:
    criteria = load_gate_criteria(task.phase)
    artifacts = collect_artifacts(task)
    worker_output = read_file(output_path)

    prompt = f"""You are a quality gate reviewer.

Phase: {task.phase}
Gate criteria:
{criteria}

Artifacts produced:
{artifacts}

Worker output (summary):
{worker_output[:4000]}

Evaluate whether the gate criteria are met.
Return JSON: {{"passed": true/false, "summary": "...", "evidence": "...", "missing": [...]}}
"""

    response = call_llm(prompt, model=config.gate_model or config.model)
    return parse_gate_result(response)
```

### merge.py

Manages git worktrees and branch merging.

```python
def create_worktree(worktree_path, branch, project_path):
    subprocess.run(["git", "worktree", "add", "-b", branch, worktree_path], cwd=project_path)

def merge(task, project_path):
    branch = f"agent/{task.role}/{task.id}-{task.slug}"
    result = subprocess.run(
        ["git", "merge", "--no-ff", branch, "-m", f"Merge {task.id}: {task.title}"],
        cwd=project_path, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise MergeConflict(task, result.stderr)
    cleanup_worktree(task, project_path)

def cleanup_worktree(task, project_path):
    worktree = f"{project_path}/.worktrees/{task.id}"
    subprocess.run(["git", "worktree", "remove", worktree], cwd=project_path)
```

### state.py

Parses and updates harness markdown files programmatically.

```python
class State:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.status = parse_status_md(f"{project_path}/STATUS.md")
        self.tracker = parse_tracker_md(f"{project_path}/operations/tracker.md")

    @property
    def current_phase(self):
        return self.status["current_phase"]

    def get_ready_tasks(self) -> list[Task]:
        return [t for t in self.tracker.tasks if t.status == "ready" and t.phase == self.current_phase]

    def advance_phase(self):
        next_phase = PHASE_ORDER[PHASE_ORDER.index(self.current_phase) + 1]
        self.status["current_phase"] = next_phase
        write_status_md(self.project_path, self.status)

    def mark_in_progress(self, task): ...
    def mark_done(self, task): ...
    def mark_blocked(self, task, evidence): ...
    def add_tasks(self, tasks): ...
    def phase_complete(self) -> bool: ...
```

### notifier.py

Sends notifications via webhook when the orchestrator needs human attention or when the run completes.

```python
def notify(config: Config, message: str):
    if config.notification_webhook:
        requests.post(config.notification_webhook, json={
            "text": f"[Harness Concurrent] {message}",
            "project": config.project_name,
            "timestamp": datetime.utcnow().isoformat(),
        })
    # Always log locally
    print(f"[NOTIFY] {message}")
```

### config.yaml

```yaml
# Runtime configuration for Concurrent mode
model: "claude-sonnet-4-20250514"          # Model for workers
gate_model: null                       # Model for gate checks (defaults to model)
max_workers: 3                         # Max parallel Claude Code workers
max_retries: 2                         # Per-task retry ceiling before escalation
checkpoint_after_requirements: true    # Pause for human review after Phase 1

# Notification (set one)
notification_webhook: ""               # Slack/Telegram incoming webhook URL

# Timeouts (seconds)
worker_timeout: 3600                   # 1 hour per worker invocation
gate_timeout: 120                      # 2 minutes for gate evaluation

# Phases to skip (e.g., ["growth", "documentation"] for backend-only projects)
skip_phases: []

# Project
project_name: ""                       # Display name for notifications
```

### run.py

CLI entry point.

```python
#!/usr/bin/env python3
"""Harness Concurrent Mode — autonomous multi-agent project delivery."""

import argparse
from orchestrator import run
from config import load_config

def main():
    parser = argparse.ArgumentParser(description="Run harness in Concurrent mode")
    parser.add_argument("--project", required=True, help="Path to project directory")
    parser.add_argument("--config", default="runtime/config.yaml", help="Config file path")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")
    args = parser.parse_args()

    config = load_config(args.config)
    config.project_name = config.project_name or args.project.split("/")[-1]

    if args.resume:
        checkpoint = f"{args.project}/runtime/.checkpoint"
        if os.path.exists(checkpoint):
            os.remove(checkpoint)
            print("Checkpoint cleared. Resuming...")

    run(args.project, config)

if __name__ == "__main__":
    main()
```

## How to Run

### Prerequisites

- Python 3.10+
- Claude Code CLI installed and authenticated (`claude --version`)
- Git (project must be a git repo with at least one commit)
- `pip install -r runtime/requirements.txt`

### Where the code lives

The runtime Python files (`run.py`, `orchestrator.py`, etc.) live inside the project's `runtime/` directory. The orchestrator reads harness files (`AGENTS.md`, `STATUS.md`, `BRIEF.md`, `harness/agents/`, etc.) from the same project.

- **New project:** clone/fork this repo and it's all in one place.
- **Existing project:** `copy_core.sh --preset full` or `--preset backend` copies `runtime/` into your project alongside the other harness files.
- **Minimal preset** does not include `runtime/` — use `full` or `backend` for Concurrent mode.

### Quick start — new project

```bash
# 1. Clone the harness repo as your project starting point
git clone https://github.com/ogiberstein/agent-trainer-harness.git my-project
cd my-project

# 2. Fill in BRIEF.md (what to build, for whom, constraints, success criteria)
# 3. Edit profiles/project-profile.yaml (tech stack, quality bars)
# 4. Edit runtime/config.yaml (model, max_workers, notification webhook)

# 5. Install Python deps
pip install -r runtime/requirements.txt

# 6. Start the orchestrator
python runtime/run.py --project .

# 7. Wait for Requirements notification, review specs/requirements.md
# 8. Resume
python runtime/run.py --project . --resume

# 9. Come back when you get the "complete" notification
```

### Quick start — existing project

```bash
# 1. Copy harness + runtime into your existing project
bash copy_core.sh --preset full --source /path/to/harness-repo /path/to/my-project
cd /path/to/my-project

# 2. Fill in BRIEF.md, edit runtime/config.yaml
# 3. Install Python deps
pip install -r runtime/requirements.txt

# 4. Start
python runtime/run.py --project .
```

### Dry run

Preview what the orchestrator will dispatch without actually running workers:

```bash
python runtime/run.py --project . --dry-run
```

### Monitoring

- Watch `STATUS.md` for current phase.
- Watch `operations/tracker.md` for task progress (updated live by the orchestrator).
- Watch `DECISIONS.md` for orchestrator decisions.
- Worker output is in `.worktrees/<task-id>/.worker_output.txt`.

### Stopping

- To pause gracefully: `touch /path/to/project/runtime/.checkpoint`
- To abort: kill the orchestrator process (workers will finish their current task).
- To resume after a pause: `python runtime/run.py --project . --resume`

## Upgrade Path: LangGraph

The orchestrator can be upgraded to a LangGraph StateGraph for:
- Built-in state persistence (survives crashes without checkpoint files)
- Declarative retry logic
- Visual graph of execution in LangSmith
- Easier conditional routing (e.g., skip phases dynamically)

This is documented here for future reference. The simple Python loop is recommended for initial use — it's easier to debug and has no extra dependencies.

## Relationship to Existing Harness

| Harness file | Concurrent runtime uses it for |
|---|---|
| `STATUS.md` | Current phase — orchestrator reads and writes |
| `operations/tracker.md` | Task board — orchestrator manages cards |
| `harness/agents/*.md` | System prompts passed to each worker |
| `harness/routing-policy.md` | Retry ceilings, dispatch rules, branch naming |
| `evaluation/release-gates.md` | Release criteria for final gate |
| `DECISIONS.md` | Orchestrator logs non-trivial decisions |
| `BRIEF.md` | Project scope — passed to PM worker in Phase 1 |
| `profiles/project-profile.yaml` | Constraints and quality bars |
| `operations/context-efficiency-guidelines.md` | Worker context budgets |
