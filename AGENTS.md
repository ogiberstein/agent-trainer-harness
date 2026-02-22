# Agent Operating Instructions

This repository uses a structured multi-agent harness for product delivery.
Treat these harness files as the primary operating instructions — do not invent ad-hoc workflows.

## Protected Infrastructure

### Always protected (never delete)

These files and directories are the harness backbone. Do **not** delete, remove, or replace them. Update their *contents* only.

- `AGENTS.md` (this file)
- `BRIEF.md`, `STATUS.md`, `DECISIONS.md`
- `harness/` directory (routing, permissions, adapter)
- `profiles/` directory
- `memory/` directory
- `evaluation/` directory (release gates, scorecard, regressions)
- `operations/context-efficiency-guidelines.md` (mandatory operational policy)
- `operations/runbook.md` (incident response and SLAs)

### Removable if irrelevant to this project

Agents **may** delete individual files from the lists below when they are clearly not applicable (e.g., `specs/ui-spec.md` in a headless project, `harness/agents/designer.md` when there is no design role). When removing, log the reason in `DECISIONS.md`.

- Individual template files in `specs/`, `qa/`, `docs/`
- Individual agent prompts in `harness/agents/` for unused roles
- Individual handoff templates in `handoffs/` for unused role transitions
- Individual skill directories in `skills/` that are not activated
- Operations templates for team workflows in solo projects (e.g., `operations/tracker.md`, `operations/team-concurrency-policy.md`)
- Root files that don't apply: `COMMANDS.md`, `FUTURE_IMPROVEMENTS.md`, `migration-checklist.md`, `day-0-start.md`, `lite-mode-checklist.md`, `concurrent-start-checklist.md`

**Rule of thumb:** keep the directory structure; prune the files that add noise. If in doubt, keep it.

## First Actions

1. Read `STATUS.md` — current phase and what's in progress.
2. Read `BRIEF.md` — what the project is and key constraints.
3. Load other files only when entering a phase that needs them (specs before requirements work, qa/ before QA, etc.).

Start checklists (read only if relevant):
- New project (full): `day-0-start.md`
- New project (lite): `lite-mode-checklist.md`
- New project (concurrent/autonomous): `concurrent-start-checklist.md` + `runtime/DESIGN.md`
- Existing project onboarding: `migration-checklist.md`

## Mode Selection

Choose the right mode based on scope. Do not default to the smallest mode for large tasks.

| Scope | Mode | Start file |
|-------|------|------------|
| 1-2 phases, single concern, bug fix | **Lite** | `lite-mode-checklist.md` |
| 3+ phases, sequential delivery (human present or autonomous) | **Full** | `day-0-start.md` |
| Parallelizable multi-phase work + external Python runtime available | **Concurrent** | `concurrent-start-checklist.md` |

A multi-phase MVP build (e.g., requirements → design → implementation → QA → docs) is Full mode, not Lite — even when running autonomously overnight. Full mode works unattended; the agent self-enforces gates and writes phase snapshots.

**Concurrent self-launch:** If you determine the project has parallelizable work (e.g., backend + frontend can be built simultaneously) AND you have shell access, run the preflight check: `python3 cli/preflight_concurrent.py --project .`. If it passes, launch with `python3 cli/harness_cli.py --project . launch-concurrent`. If it fails, fall back to Full mode and log the reason in `DECISIONS.md`.

## Execution Behavior

- **Proportionality:** small changes (bug fixes, config tweaks, one-liner patches) need only update `STATUS.md` and code. Full ceremony (gates, handoffs, decisions logging) is for feature work and multi-file changes.
- Update `STATUS.md` after meaningful phase/task transitions.
- Log non-trivial trade-offs and assumptions in `DECISIONS.md`.
- **Phase snapshots:** after completing each phase, write a summary to `memory/summaries/phase-{N}-{name}.md` using the template in that directory. This protects against context compaction and makes sessions resumable.
- **Gate enforcement:** phase advancement without a gate log entry in `STATUS.md` is a harness violation. Record `PASS`, `FAIL`, or `SKIPPED(reason)` with evidence. If skipping a gate, log the reason in `DECISIONS.md`.
- Follow `operations/context-efficiency-guidelines.md` to keep context scoped and concise.
- Follow `operations/team-concurrency-policy.md` when multiple agents/workers are active.
- Load only phase-relevant artifacts instead of full project history.
- Use runbook playbooks from `COMMANDS.md` when present.

## Coexistence with Agent-Level Configs

If this repository is used with an agent-level config (e.g., `CLAUDE.md`, `.cursorrules`, or similar):
- The agent config defines **how you work** (behavior, delegation, verification, tone).
- This file and the harness define **what you work on** (project phase, files, quality gates).
- Both apply. Use the agent config for process; use the harness for workflow.
- Agent-config skills (coding standards, PR review, etc.) and harness skills (`skills/` directory) are complementary, not conflicting.
- Agent-config task tracking (todos) handles granular steps; `STATUS.md` handles cross-session phase state.

## Key References

| File | Purpose |
|------|---------|
| `STATUS.md` | Current phase, progress, blockers |
| `DECISIONS.md` | Non-trivial decisions with rationale |
| `COMMANDS.md` | Runbook playbooks for repeatable actions |
| `BRIEF.md` | Original project request (immutable once locked) |
| `harness/routing-policy.md` | Scheduling, retries, escalation |
| `harness/permissions-matrix.md` | Tool/file access by role |
| `profiles/active-skills.yaml` | Enabled skills for this project |
| `evaluation/release-gates.md` | Promotion and release criteria |
| `cli/validate_harness.py` | Executable consistency checker |
| `cli/harness_cli.py` | CLI for status, gate-check, phase-next, task ops, launch-concurrent |
| `cli/preflight_concurrent.py` | Preflight check for concurrent mode prerequisites |
