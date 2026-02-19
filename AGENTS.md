# Agent Operating Instructions

This repository uses a structured multi-agent harness for product delivery.
Treat these harness files as the primary operating instructions — do not invent ad-hoc workflows.

## Protected Infrastructure (Do Not Delete)

Do **not** delete, remove, or replace these harness assets. Align or update their *contents* only; do not remove the files or folders themselves.

- `AGENTS.md` (this file)
- `harness/` (role prompts, routing, permissions, adapter)
- `profiles/` (org/project profiles, active skills)
- `memory/` (policies, index, snapshots, summaries)
- `evaluation/` (gates, scorecard, regressions)
- `operations/` (runbook, board, dashboard, SLAs, guidelines)
- `skills/` (skill library, registry, packs)
- `handoffs/` (handoff templates)
- Root runbooks: `COMMANDS.md`, `BRIEF.md`, `STATUS.md`, `DECISIONS.md`, `FUTURE_IMPROVEMENTS.md`, `migration-checklist.md`

If a task says "clean up," "simplify," or "remove scaffolding," it still applies to *project* cruft only — never to the list above.

## First Actions

1. Read `docs/README.md` for system overview and entry points.
2. Read `STATUS.md` for current phase and progress.
3. Read `COMMANDS.md` for available runbook commands.
4. Follow the appropriate start checklist:
   - New project (full): `day-0-start.md`
   - New project (lite): `lite-mode-checklist.md`
   - Existing project onboarding: `migration-checklist.md`

## Execution Behavior

- Update `STATUS.md` after meaningful phase/task transitions.
- Log non-trivial trade-offs and assumptions in `DECISIONS.md`.
- Follow `operations/context-efficiency-guidelines.md` to keep context scoped and concise.
- Follow `operations/team-concurrency-policy.md` when multiple agents/workers are active.
- Do not bypass gate checks silently; report PASS/FAIL with concrete evidence and next action.
- Prefer the smallest valid workflow (lite before full when appropriate).
- Load only phase-relevant artifacts instead of full project history.
- Use command-style runbooks from `COMMANDS.md` when present.

## Key References

| File | Purpose |
|------|---------|
| `STATUS.md` | Current phase, progress, blockers |
| `DECISIONS.md` | Non-trivial decisions with rationale |
| `COMMANDS.md` | Pseudo-command runbooks for repeatable actions |
| `BRIEF.md` | Original project request (immutable once locked) |
| `harness/routing-policy.md` | Scheduling, retries, escalation |
| `harness/permissions-matrix.md` | Tool/file access by role |
| `profiles/active-skills.yaml` | Enabled skills for this project |
| `evaluation/release-gates.md` | Promotion and release criteria |
