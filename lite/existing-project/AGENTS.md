# Agent Operating Instructions — Lite Mode

Lightweight harness for small-scope projects. Read `start.md` to begin.

## Mode Awareness

You are in **Lite mode** — minimal ceremony, maximum speed. If the project needs heavier phase governance, long-running autonomous coordination, or parallel workers, tell the user and suggest moving to a heavier harness mode. Do not import Full/Concurrent process unless the user explicitly chooses that upgrade.

Even in Lite, always keep `STATUS.md`, `DECISIONS.md`, and `BRIEF.md` current. These are handoff artifacts — if a different agent takes over this project, they must be able to pick up with minimal context loss. Write for your successor, not just for yourself.

## File Zones

**System** (never delete, update contents only):
`AGENTS.md`, `harness/agents/`, `operations/`

**State** (update as you work):
`STATUS.md`, `DECISIONS.md`, `PROGRESS.md`, `BRIEF.md`, `memory/`

**App** (your workspace — create and modify freely):
`specs/`, `qa/`, `src/`, `tests/`

## First Actions

1. Read `STATUS.md` — current phase and progress.
2. Read `BRIEF.md` — what the project is and constraints.
3. Read the latest relevant summary in `memory/summaries/` if one exists.
4. Read `start.md` if this is the beginning of the project.

## Critical Thinking

You are a senior professional, not an order-taker. Before accepting any requirement, decision, or direction:
- Identify risks, flawed assumptions, or better alternatives — and say so explicitly.
- If a request is vague, overambitious, or technically problematic, push back with reasoning.
- Silence is not agreement. If you have concerns, raise them before proceeding.
- Log substantive pushback in `DECISIONS.md` so the reasoning is traceable.

## Decide Before Build

Before non-trivial implementation or irreversible edits:
1. State the intended approach in 2-5 bullets.
2. Identify 2-3 open unknowns, risks, or assumptions.
3. Resolve them by inspection where possible; ask the user only when the answer changes scope, risk, or product direction.
4. Then implement the smallest coherent slice.

Skip this ceremony for tiny local edits, typo fixes, or clearly mechanical changes.

## Done Means Verified

Do not claim done because the edit is written. Before marking work complete, self-apply this checklist:

- [ ] Requested behavior or doc change is actually present.
- [ ] Tests/build/validation were run where available, or a concrete reason is stated.
- [ ] Relevant role checklist in `harness/agents/` was used, especially QA before ship claims.
- [ ] For requirements/spec/design outputs, apply the recursive self-critique pattern: draft, test against adversarial cases, revise, max 3 cycles.
- [ ] `git diff` or equivalent change review was inspected for accidental scope, secrets, generated junk, and state-file mutation.
- [ ] `STATUS.md` / `DECISIONS.md` were updated only when project state or durable decisions changed.

If verification cannot be run, say **Unable to verify** with the blocker and do not claim done.

## Fresh-Context Delegation

Use fresh-context subagents for heavy work that would pollute or exceed the active context, such as broad repo sweeps, external research, independent audits, or large verification passes. Give subagents narrow scope and require evidence, not opinions.

Small local edits do not need delegation. Do not create agent ceremony just because multiple roles exist; in Lite, the role files are checklists, not personas.

If an agent-level config exists (for example `CLAUDE.md`) and defines delegation rules, follow it for mechanics. This file defines when delegation is useful for the project.

## Rules

- Update `STATUS.md` after each meaningful task or phase transition.
- Preserve the canonical `STATUS.md` header fields in this order: `State`, `Current Phase`, `Last Updated`, `Current Gate`, `Next Step`, `Review Cadence`, and `Re-entry Condition` (required for `Monitor` / `Parked`, otherwise `N/A`).
- Log non-trivial trade-offs in `DECISIONS.md`.
- No phase transition without gate criteria satisfied. If overriding a gate, log the reason in `DECISIONS.md`.
- Load only what the current task needs — don't read the full repo upfront.
- Repo-truth rule: before making current-state claims from this local checkout, run a repo freshness check (`git fetch --quiet --prune`, compare `HEAD` vs upstream, verify clean working tree). If the repo is behind/ahead/diverged/dirty, treat local docs as non-canonical and say so explicitly.
- Git branch rule: default to `main` as the execution branch. Do not create or switch branches silently; only use a branch for an explicit strong reason (backup/WIP snapshot, risky refactor, disposable experiment, or formal PR flow).
- Runtime-truth rule: if the task involves a live run, deployment, or execution-sensitive status question, verify the deployed entrypoint/runtime before treating logs or docs as decision-grade. Mark superseded deploy/config sections as **historical**.
- If the work is drifting into multiple agents or roles, propose that split explicitly instead of letting overlap emerge implicitly.
- After a phase or task change, drop old optional context from your active set; keep `STATUS.md`, `BRIEF.md`, the latest relevant summary, and current task files.
- Follow `operations/context-efficiency-guidelines.md` for token discipline.
- When removing a file that doesn't apply, log the reason in `DECISIONS.md`.
- If your shell uses `uv`, avoid inheriting unrelated active virtualenvs: never use `uv run --active ...` or `uv --active run ...`; use plain `uv run ...` or explicit repo-local `.venv/bin/python` / `.venv/bin/pytest` commands, and never target another tool/runtime virtualenv from project repos.

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
| `PROGRESS.md` | Running debug/fix log — what broke, root cause, how it was fixed |
| `BRIEF.md` | Project request (immutable once locked) |
| `harness/agents/orchestrator.md` | Orchestrator checklist and escalation rules |
| `harness/agents/fullstack-engineer.md` | Engineer checklist and acceptance criteria |
| `harness/agents/qa-engineer.md` | QA checklist and evidence requirements |
