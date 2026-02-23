# Concurrent Mode — Start Here

Fully autonomous, parallel product delivery. Multiple Claude Code workers execute simultaneously, coordinated by a Python orchestrator. You define the scope, walk away, and come back to a polished MVP.

## Prerequisites

- Python 3.10+
- Claude Code CLI (`claude` command available)
- Git (initialized repo)

## Setup

1. Fill in `BRIEF.md` with your project scope and constraints.
2. Customize `profiles/project-profile.yaml` — tech stack, quality bars, workflow policy.
3. Edit `runtime/config.yaml` — model, max workers, timeouts, notification webhook.
4. Install runtime dependencies: `pip install -r runtime/requirements.txt`
5. Read `AGENTS.md` — operating instructions and file zones.
6. Set `STATUS.md` Current Phase to `requirements`.

## Agent-Driven Launch (Single Command)

If you are an AI agent with shell access:
1. Run preflight: `python3 cli/preflight_concurrent.py --project .`
2. If all checks pass: `python3 cli/harness_cli.py --project . launch-concurrent`
3. If any check fails: fall back to solo-autonomous Full mode and log the reason in `DECISIONS.md`.

## Manual Launch

1. Optional dry run: `python3 runtime/run.py --project . --dry-run`
2. Start orchestrator: `python3 runtime/run.py --project .`
3. The orchestrator will:
   - Run requirements phase (may pause for human review)
   - Dispatch parallel workers for implementation
   - Enforce gates between phases
   - Merge results and advance to QA, docs, etc.
4. Walk away. Monitor via:
   - `python3 cli/harness_cli.py --project . status`
   - `tail -f logs/orchestrator.log`
   - `cat STATUS.md`

## Phase Sequence

Same as Full mode (Requirements -> Design -> Implementation -> QA -> Docs -> Growth -> Review), but implementation phases run in parallel across isolated git worktrees.

See `runtime/DESIGN.md` for the full architecture.

## Monitoring

- **CLI status:** `python3 cli/harness_cli.py --project . status`
- **Task board:** `python3 cli/harness_cli.py --project . task list`
- **Gate check:** `python3 cli/harness_cli.py --project . gate-check`
- **Run telemetry:** `cat logs/runs.jsonl`
- **Worker output:** Check individual worktree logs

## Stopping / Pausing

- **Graceful pause:** `touch runtime/.checkpoint` — workers finish current tasks, then stop.
- **Resume:** `python3 runtime/run.py --project . --resume`
- **Hard stop:** Kill the orchestrator process.

## Webhook Notifications

Configure `runtime/config.yaml` with a webhook URL to receive notifications on:
- Phase completions
- Gate results
- Errors and escalations

## Day 0 Sanity Checklist

- [ ] `BRIEF.md` completed with concrete scope and constraints.
- [ ] `profiles/project-profile.yaml` customized.
- [ ] `runtime/config.yaml` edited (model, workers, webhook).
- [ ] `runtime/requirements.txt` dependencies installed.
- [ ] `STATUS.md` set to `requirements`.
- [ ] Git repo initialized with initial commit.
- [ ] `python3 cli/preflight_concurrent.py --project .` passes all checks.
