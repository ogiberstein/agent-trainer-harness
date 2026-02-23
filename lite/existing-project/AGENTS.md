# Agent Operating Instructions — Lite Mode

Lightweight harness for small-scope projects. Read `start.md` to begin.

## File Zones

**System** (never delete, update contents only):
`AGENTS.md`, `harness/`, `profiles/`, `operations/`

**State** (update as you work):
`STATUS.md`, `DECISIONS.md`, `BRIEF.md`, `memory/`

**App** (your workspace — create and modify freely):
`specs/`, `qa/`, `src/`, `tests/`

## First Actions

1. Read `STATUS.md` — current phase and progress.
2. Read `BRIEF.md` — what the project is and constraints.
3. Read `start.md` if this is the beginning of the project.

## Rules

- Update `STATUS.md` after each meaningful task or phase transition.
- Log non-trivial trade-offs in `DECISIONS.md`.
- Load only what the current task needs — don't read the full repo upfront.
- Follow `operations/context-efficiency-guidelines.md` for token discipline.
- When removing a file that doesn't apply, log the reason in `DECISIONS.md`.

## Coexistence with Agent-Level Configs

If an agent-level config exists (e.g., `CLAUDE.md`, `.cursorrules`):
- Agent config = **how you work**. This file = **what you work on**. Both apply.

## Key References

| File | Purpose |
|------|---------|
| `STATUS.md` | Current phase and progress |
| `DECISIONS.md` | Non-trivial decisions with rationale |
| `BRIEF.md` | Project request (immutable once locked) |
| `harness/routing-policy.md` | Task scheduling and escalation |
| `profiles/active-skills.lite.yaml` | Enabled skills for this project |
