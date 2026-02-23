# Agent Operating Instructions — Full Mode

Multi-agent harness for product delivery with phase gates and structured handoffs.
Read `start.md` to begin.

## File Zones

**System** (never delete, update contents only):
`AGENTS.md`, `harness/`, `profiles/`, `evaluation/`, `operations/`

**State** (update as you work):
`STATUS.md`, `DECISIONS.md`, `BRIEF.md`, `memory/`, `handoffs/`

**App** (your workspace — create and modify freely):
`specs/`, `qa/`, `docs/`, `src/`, `tests/`

## First Actions

1. Read `STATUS.md` — current phase, gate log, and progress.
2. Read `BRIEF.md` — what the project is and constraints.
3. Read `start.md` if this is the beginning of the project.
4. Load other files only when entering a phase that needs them.

## Rules

- Update `STATUS.md` after meaningful phase/task transitions.
- Log non-trivial trade-offs and assumptions in `DECISIONS.md`.
- **Phase snapshots:** after each phase, write a summary to `memory/summaries/phase-{N}-{name}.md` using the template. This protects against context loss and makes sessions resumable.
- **Gate enforcement:** record `PASS`, `FAIL`, or `SKIPPED(reason)` in the STATUS.md Gate Log before advancing. Skipping a gate without logging is a harness violation.
- Follow handoff contracts in `handoffs/` when transitioning between roles.
- Follow `operations/context-efficiency-guidelines.md` for token discipline.
- When removing a harness file that doesn't apply, log the reason in `DECISIONS.md`.
- Use runbook playbooks from `COMMANDS.md` for repeatable actions.

## Coexistence with Agent-Level Configs

If an agent-level config exists (e.g., `CLAUDE.md`, `.cursorrules`):
- Agent config = **how you work**. This file = **what you work on**. Both apply.
- Agent-config task tracking handles granular steps; `STATUS.md` handles cross-session phase state.

## Key References

| File | Purpose |
|------|---------|
| `STATUS.md` | Current phase, progress, gate log |
| `DECISIONS.md` | Non-trivial decisions with rationale |
| `BRIEF.md` | Project request (immutable once locked) |
| `COMMANDS.md` | Runbook playbooks for repeatable actions |
| `harness/routing-policy.md` | Scheduling, retries, escalation |
| `harness/permissions-matrix.md` | Tool/file access by role |
| `profiles/active-skills.yaml` | Enabled skills for this project |
| `evaluation/release-gates.md` | Phase promotion criteria |
