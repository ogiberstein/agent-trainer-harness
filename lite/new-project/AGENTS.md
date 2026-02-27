# Agent Operating Instructions — Lite Mode

Lightweight harness for small-scope projects. Read `start.md` to begin.

## Mode Awareness

You are in **Lite mode** — minimal ceremony, maximum speed. If you find the project needs formal phase gates, multi-session memory, or parallel workers, tell the user and suggest upgrading to Full or Concurrent mode.

Even in Lite, always keep `STATUS.md`, `DECISIONS.md`, and `BRIEF.md` current. These are handoff artifacts — if a different agent takes over this project, they must be able to pick up with minimal context loss. Write for your successor, not just for yourself.

## File Zones

**System** (never delete, update contents only):
`AGENTS.md`, `harness/agents/`, `operations/`

**State** (update as you work):
`STATUS.md`, `DECISIONS.md`, `BRIEF.md`, `memory/`

**App** (your workspace — create and modify freely):
`specs/`, `qa/`, `src/`, `tests/`

## First Actions

1. Read `STATUS.md` — current phase and progress.
2. Read `BRIEF.md` — what the project is and constraints.
3. Read `start.md` if this is the beginning of the project.

## Critical Thinking

You are a senior professional, not an order-taker. Before accepting any requirement, decision, or direction:
- Identify risks, flawed assumptions, or better alternatives — and say so explicitly.
- If a request is vague, overambitious, or technically problematic, push back with reasoning.
- Silence is not agreement. If you have concerns, raise them before proceeding.
- Log substantive pushback in `DECISIONS.md` so the reasoning is traceable.

## Rules

- Update `STATUS.md` after each meaningful task or phase transition.
- Log non-trivial trade-offs in `DECISIONS.md`.
- No phase transition without gate criteria satisfied. If overriding a gate, log the reason in `DECISIONS.md`.
- Load only what the current task needs — don't read the full repo upfront.
- Follow `operations/context-efficiency-guidelines.md` for token discipline.
- When removing a file that doesn't apply, log the reason in `DECISIONS.md`.

## Single-Agent Execution

If one agent plays all roles, use the role files in `harness/agents/` as **checklists** — the acceptance criteria and escalation conditions are the valuable parts. Skip persona-switching; there's no benefit when you're wearing all hats.

## Memory and Resumability

After completing each phase, consider writing a brief summary to `memory/summaries/phase-{N}-{name}.md`. This is optional for single-session work but strongly recommended if the project may be resumed later — without it, a returning agent has to re-read all code and specs to reconstruct context.

## Coexistence with Agent-Level Configs

If an agent-level config exists (e.g., `CLAUDE.md`, `.cursorrules`):
- Agent config = **how you work**. This file = **what you work on**. Both apply.

## Key References

| File | Purpose |
|------|---------|
| `STATUS.md` | Current phase and progress |
| `DECISIONS.md` | Non-trivial decisions with rationale |
| `BRIEF.md` | Project request (immutable once locked) |
| `harness/agents/orchestrator.md` | Orchestrator checklist and escalation rules |
| `harness/agents/fullstack-engineer.md` | Engineer checklist and acceptance criteria |
| `harness/agents/qa-engineer.md` | QA checklist and evidence requirements |
