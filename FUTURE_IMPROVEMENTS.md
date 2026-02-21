# Future Improvements

This document tracks future upgrades for evolving the harness from manual orchestration to true concurrent multi-agent execution.

## Current State
- File-first orchestration is operational (`harness/`, `operations/`, `profiles/`, `skills/`).
- Team workflow runs reliably in manual/semi-manual mode via role switching and handoffs.
- Governance, quality gates, and skill controls are in place.
- **Concurrent mode scaffolded** (`runtime/`): Python orchestrator, Claude Code CLI workers, LLM-based gate evaluation, merge steward, notification layer. See `runtime/DESIGN.md` for full architecture.
- **CLI tooling** (`cli/`): `validate_harness.py` for consistency checks, `harness_cli.py` for status/gate-check/phase-next/task operations.
- **Role prompt contracts**: All 8 agent prompts have Required Inputs, Acceptance Checklist, and Escalation Conditions.
- **Run telemetry**: JSONL event logging in `logs/runs.jsonl` wired into the concurrent orchestrator.

## Target State (Concurrency) — IN PROGRESS
- ~~Multiple workers run in parallel on isolated tasks.~~ **Scaffolded** in `runtime/orchestrator.py` + `runtime/worker.py`.
- ~~Dispatch assigns only ready/unblocked work.~~ **Scaffolded** in `runtime/orchestrator.py`.
- ~~Merge/review is automated or semi-automated.~~ **Scaffolded** in `runtime/merge.py` + `runtime/gates.py`.
- ~~Workflow state is resumable without restarting failed runs.~~ **Scaffolded** via checkpoint files and `--resume` flag.
- **Remaining:** real-world testing, observability dashboard.

## What Concurrency Enables
- Faster cycle times for independent tasks (backend/frontend/docs in parallel).
- Reduced idle time between phases.
- Better handling of long-running research/build/test tracks.
- Stronger operational visibility (queue health, throughput, rework loops).

## Tooling and Setup Options

### Option A: Keep Manual + Add Better Ops Layer (Lowest Complexity)
- Use current harness with stricter board/queue discipline.
- Add more automation scripts around `COMMANDS.md`.
- Best for: solo/early-stage projects.

### Option B: LangGraph-Style Runtime (Local/Self-Hosted)
- Implement graph nodes per role and phase gate.
- Use file-based state as canonical source of truth.
- Add optional observability stack later.
- Best for: controlled, custom orchestration without full platform adoption.

### Option C: Stoneforge-Like Orchestration Platform
- Adopt runtime features: dispatch daemon, worktree isolation, merge steward, dashboard.
- Keep this harness as policy/governance layer on top.
- Best for: heavier parallelism, multi-worker workflows, persistent operations.

### Option D: Telegram Remote Control Layer (Takopi-Style)
- Add remote command + notification interface for orchestrator actions.
- Keep command whitelist and file-first governance.
- Best for: mobile/remote interaction and asynchronous supervision.

## Executable Runbook Commands

**Implemented:** Core playbooks are now executable via `cli/harness_cli.py` and `cli/validate_harness.py`:
- `/validate-harness` → `python3 cli/validate_harness.py --project .`
- `/status` → `python3 cli/harness_cli.py --project . status`
- `/gate-check` → `python3 cli/harness_cli.py --project . gate-check`
- `/phase-next` → `python3 cli/harness_cli.py --project . phase-next`
- `/task-list` → `python3 cli/harness_cli.py --project . task list`
- `/task-add` → `python3 cli/harness_cli.py --project . task add --title "..." --role "..." --phase "..."`

**Remaining (not yet wired):** `/dispatch-ready`, `/merge-steward`, `/resume-workflow`, `/security-gate`, `/ops-sync`, `/retrospective`.

Future approach options for remaining commands:
- **Framework plugin:** expose commands as MCP tools or LangGraph nodes so agents can invoke them natively.
- **Hybrid:** keep markdown as the spec; auto-generate thin script wrappers that parse the "Runs:" steps.

## Recommended Evolution Path
1. **Done:** Stay in manual mode with Lite/Full/Backend presets. ✓
2. **Done:** Scaffold Concurrent mode runtime (`runtime/`). ✓
3. **Done:** Wire core playbooks to executable CLI scripts (`cli/validate_harness.py`, `cli/harness_cli.py`). ✓
4. **Done:** Add role prompt I/O contracts (Required Inputs, Acceptance Checklist, Escalation Conditions) to all agent prompts. ✓
5. **Done:** Add JSONL run telemetry (`runtime/telemetry.py`) wired into orchestrator. ✓
6. **Near term:** Test Concurrent mode on a real project; harden `state.py` round-trip parsing under edge cases.
7. **Next:** Add observability dashboard (cost, gate pass/fail rates, rework loops) — can now build on `logs/runs.jsonl` telemetry.
8. **Later:** Add optional remote control interfaces (Telegram, Slack).

## Readiness Criteria Before Moving to Concurrency
- Stable gate pass/fail behavior in manual mode.
- Handoffs are consistently high quality.
- Minimal duplicate/overlapping work in board workflow.
- Team can recover cleanly from failed or blocked tasks.

## Risks and Mitigations
- **Risk:** Added runtime complexity too early.  
  **Mitigation:** Keep file-first governance; adopt in staged rollout.
- **Risk:** Parallel edits cause conflicts.  
  **Mitigation:** Enforce branch/worktree isolation and file-scope ownership.
- **Risk:** Lower quality due to speed bias.  
  **Mitigation:** Preserve gate checks and security/review steps.
