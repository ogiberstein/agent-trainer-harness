# Existing Project Migration Checklist

Use this checklist to add the harness into an already-active codebase without disrupting current workflows.

## Phase 0: Preflight
- [ ] Confirm current project builds and tests pass before migration.
- [ ] Create a backup branch/tag in the target repo.
- [ ] Identify current folder layout (`src/`, `tests/`, `docs/`, infra dirs).
- [ ] Identify existing CI checks and release gates.

## Phase 1: Copy Harness (Non-Destructive)
- [ ] Copy these directories into target repo:
  - `harness/`
  - `profiles/`
  - `memory/`
  - `evaluation/`
  - `operations/`
  - `skills/`
  - `handoffs/`
- [ ] Copy these files if missing:
  - `BRIEF.md`
  - `STATUS.md`
  - `DECISIONS.md`
  - `Day 0 Start with this Prompt.md`
- [ ] Do **not** overwrite existing `src/`, `tests/`, or mature `docs/` content.

## Phase 2: Reconcile Project Reality
- [ ] Update `profiles/project-profile.yaml` with real stack, constraints, and quality bars.
- [ ] Update `profiles/active-skills.yaml` to minimal required skills.
- [ ] Update `harness/permissions-matrix.md` if repo boundaries differ.
- [ ] Update `harness/adapter-config.yaml` for your chosen harness/runtime.
- [ ] Add any project-specific paths/commands to `docs/SETUP.md`.

## Phase 3: Baseline Existing System
- [ ] Backfill `specs/requirements.md` from current product behavior.
- [ ] Backfill `specs/architecture.md` from actual implementation.
- [ ] Backfill `specs/ui-spec.md` where relevant.
- [ ] Set `STATUS.md` current phase to where reality is today (often implementation, QA, or documentation).
- [ ] Log migration assumptions in `DECISIONS.md`.

## Phase 4: Day 0 Setup in Existing Repo
- [ ] Run Setup Engineer flow from `Day 0 Start with this Prompt.md`.
- [ ] Generate/refresh `profiles/merged-profile.yaml`.
- [ ] Generate role prompts in `harness/generated-agents/`.
- [ ] Validate skills with `skills/skill-review-checklist.md` before enabling non-core skills.

## Phase 5: Controlled Rollout
- [ ] Start with core roles only (Orchestrator, PM, QA).
- [ ] Run one small feature or bugfix through full gate workflow.
- [ ] Confirm handoff quality and gate behavior.
- [ ] Add additional roles/skills incrementally after first successful cycle.
- [ ] For small projects, prefer `Lite Mode Start Checklist.md` and `profiles/active-skills.lite.yaml`.

## Phase 6: Quality and Operations Alignment
- [ ] Validate `evaluation/release-gates.md` against current release process.
- [ ] Confirm `operations/runbook.md` aligns with incident workflow.
- [ ] Apply `operations/context-efficiency-guidelines.md` during all runs.
- [ ] Add migration notes and version entry to `operations/changelog.md`.

## Common Pitfalls to Avoid
- Copying full architecture text into every prompt instead of referencing files.
- Activating too many optional skills/agents on the first run.
- Re-running whole phases instead of targeted retries after gate failures.
- Overwriting mature project docs/specs instead of merging carefully.

## Definition of Done
- [ ] Harness is present and configured without breaking existing project workflows.
- [ ] At least one real task completed through phase gates.
- [ ] Team can run Day 0 + ongoing phases repeatably.
- [ ] Minimal active skill set is documented and pinned.
