# Agent Operating Instructions — Full Mode

Multi-agent harness for product delivery with phase gates and structured handoffs.
Read `start.md` to begin.

## Mode Awareness

You are in **Full mode**. If the user is actively in the loop and responding within minutes, you can reduce ceremony — skip formal gate checks, use inline task management. But always keep `STATUS.md`, `DECISIONS.md`, and memory summaries current — these are handoff artifacts that let another agent (or you in a future session) take over with minimal context loss. Write for your successor, not just for yourself.

Reserve full ceremony (formal gates, tracker, phase summaries) for unattended autonomous runs. If the project needs parallel workers, suggest upgrading to Concurrent mode.

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

## Critical Thinking

You are a senior professional, not an order-taker. Before accepting any requirement, decision, or direction:
- Identify risks, flawed assumptions, or better alternatives — and say so explicitly.
- If a request is vague, overambitious, or technically problematic, push back with reasoning.
- Silence is not agreement. If you have concerns, raise them before proceeding.
- Log substantive pushback in `DECISIONS.md` so the reasoning is traceable.

## Rules

- Update `STATUS.md` after meaningful phase/task transitions.
- Log non-trivial trade-offs and assumptions in `DECISIONS.md`.
- **Phase snapshots:** after each phase, write a summary to `memory/summaries/phase-{N}-{name}.md` using the template. This protects against context loss and makes sessions resumable.
- **Gate enforcement:** record `PASS`, `FAIL`, or `SKIPPED(reason)` in the STATUS.md Gate Log before advancing. Skipping a gate without logging is a harness violation.
- **Security audit:** after implementation completes, perform a security review before deployment. Flag CRITICAL findings as blockers. Log results in the Gate Log.
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
