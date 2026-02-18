# Agent Operating Instructions

This repository uses a structured multi-agent harness for product delivery.
Treat these harness files as the primary operating instructions — do not invent ad-hoc workflows.

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
