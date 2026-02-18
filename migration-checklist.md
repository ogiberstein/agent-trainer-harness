# Existing Project Migration Checklist

Use this checklist to add the harness into an already-active codebase without disrupting current workflows.

## Phase 0: Preflight
- [ ] Confirm current project builds and tests pass before migration.
- [ ] Create a backup branch/tag in the target repo.
- [ ] Identify current folder layout (`src/`, `tests/`, `docs/`, infra dirs).
- [ ] Identify existing CI checks and release gates.
- [ ] Decide import method:
  - Recommended: use `starter_kit_existing_projects/` (`core/` + `alignment/`)
  - Alternative: manual file-by-file copy

## Phase 1: Copy Harness (Non-Destructive)
- [ ] Recommended path: run starter kit scripts from this repository:
  - `bash starter_kit_existing_projects/core/copy_core.sh "/path/to/target-repo"`
- [ ] `copy_core.sh` is safe mode: it aborts on existing harness paths and does not overwrite.
- [ ] In target repo, run alignment handover:
  - Use `starter_kit_existing_projects/alignment/EXISTING_PROJECT_ALIGNMENT_PROMPT.md`
  - Track completion with `starter_kit_existing_projects/alignment/EXISTING_PROJECT_ALIGNMENT_CHECKLIST.md`
- [ ] Copy these directories into target repo (if not using copy_core.sh):
  - `harness/`
  - `profiles/`
  - `memory/`
  - `evaluation/`
  - `operations/`
  - `skills/`
  - `handoffs/`
- [ ] Copy these files if missing:
  - `AGENTS.md`
  - `BRIEF.md`
  - `STATUS.md`
  - `DECISIONS.md`
  - `COMMANDS.md`
  - `day-0-start.md`
  - `lite-mode-checklist.md`
- [ ] Optionally install a framework shim from `starter_kit_existing_projects/framework-shims/`.
- [ ] Do **not** copy/overwrite existing `specs/`, `qa/`, or `docs/`; align those in place via the alignment flow.
- [ ] Do **not** overwrite existing `src/` or `tests/` content.

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
- [ ] Run Setup Engineer flow from `day-0-start.md`.
- [ ] Generate/refresh `profiles/merged-profile.yaml`.
- [ ] Generate role prompts in `harness/generated-agents/`.
- [ ] Validate skills with `skills/skill-review-checklist.md` before enabling non-core skills.

## Phase 5: Controlled Rollout
- [ ] Start with core roles only (Orchestrator, PM, QA).
- [ ] Run one small feature or bugfix through full gate workflow.
- [ ] Confirm handoff quality and gate behavior.
- [ ] Add additional roles/skills incrementally after first successful cycle.
- [ ] For small projects, prefer `lite-mode-checklist.md` and `profiles/active-skills.lite.yaml`.

## Phase 6: Quality and Operations Alignment
- [ ] Validate `evaluation/release-gates.md` against current release process.
- [ ] Confirm `operations/runbook.md` aligns with incident workflow.
- [ ] Apply `operations/context-efficiency-guidelines.md` during all runs.
- [ ] Add migration notes and version entry to `operations/changelog.md`.
- [ ] Run `/validate-harness` to confirm internal consistency.

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
- [ ] `/validate-harness` passes.
