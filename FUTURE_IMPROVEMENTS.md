# Future Improvements

This document tracks future upgrades for evolving the harness from manual orchestration to true concurrent multi-agent execution.

## Current State
- File-first orchestration is operational (`harness/`, `operations/`, `profiles/`, `skills/`).
- Team workflow runs reliably in manual/semi-manual mode via role switching and handoffs.
- Governance, quality gates, and skill controls are in place.
- **Concurrent mode scaffolded** (`runtime/`): Python orchestrator, Claude Code CLI workers, LLM-based gate evaluation, merge steward, notification layer. See `runtime/DESIGN.md` for full architecture.

## Target State (Concurrency) — IN PROGRESS
- ~~Multiple workers run in parallel on isolated tasks.~~ **Scaffolded** in `runtime/orchestrator.py` + `runtime/worker.py`.
- ~~Dispatch assigns only ready/unblocked work.~~ **Scaffolded** in `runtime/orchestrator.py`.
- ~~Merge/review is automated or semi-automated.~~ **Scaffolded** in `runtime/merge.py` + `runtime/gates.py`.
- ~~Workflow state is resumable without restarting failed runs.~~ **Scaffolded** via checkpoint files and `--resume` flag.
- **Remaining:** real-world testing, full tracker.md card parsing, STATUS.md incremental updates, observability dashboard.

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

`COMMANDS.md` currently contains manual playbook descriptions. A natural next step is wiring them to actual scripts so that `/phase-next`, `/gate-check`, `/dispatch-ready`, `/validate-harness`, etc. are executable from the terminal or an agent tool call rather than requiring a human to read and manually follow the steps.

Approach options:
- **Shell scripts:** one script per command in a `bin/` directory, reading/writing the harness markdown files directly.
- **Framework plugin:** expose commands as MCP tools or LangGraph nodes so agents can invoke them natively.
- **Hybrid:** keep markdown as the spec; auto-generate thin script wrappers that parse the "Runs:" steps.

Priority: near-term, after manual mode is stable and patterns are validated on real projects.

## Recommended Evolution Path
1. **Done:** Stay in manual mode with Lite/Full/Backend presets. ✓
2. **Done:** Scaffold Concurrent mode runtime (`runtime/`). ✓
3. **Near term:** Wire runbook playbooks to executable scripts (see above).
4. **Near term:** Test Concurrent mode on a real project; harden `state.py` card parsing and `STATUS.md` incremental writes.
5. **Next:** Add observability dashboard (cost, gate pass/fail rates, rework loops).
6. **Later:** Add optional remote control interfaces (Telegram, Slack).

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
