# Existing Project Alignment Checklist

Use this after core harness files are copied into the target repo.

**Protection policy:** Always-protected files (`AGENTS.md`, `BRIEF.md`, `STATUS.md`, `DECISIONS.md`, `harness/` dir, `profiles/` dir, `memory/` dir) must not be deleted. Individual irrelevant template files may be removed if logged in `DECISIONS.md`. See `AGENTS.md` for full policy.

## Phase A: Discovery and Mapping
- [ ] Verify `AGENTS.md` is present at repo root and readable by the agent.
- [ ] Inventory existing docs/specs and map to harness expectations.
- [ ] Identify gaps, stale artifacts, conflicting terminology, and irrelevant templates.
- [ ] Record major assumptions in `DECISIONS.md`.

## Phase B: Prune Irrelevant Templates
- [ ] Remove harness template files that do not apply (e.g., UI specs for headless, growth files for non-growth projects).
- [ ] Log each removal in `DECISIONS.md` with a one-line reason.

## Phase C: Core Alignment
- [ ] Align `specs/requirements.md` to current product behavior.
- [ ] Align `specs/architecture.md` to actual implementation.
- [ ] Align `specs/ui-spec.md` where UI exists (skip if pruned in Phase B).
- [ ] Add optional `specs/user-research.md` and/or `specs/market-research.md` when relevant.

## Phase D: Operational Alignment
- [ ] Ensure handoff files reference real project paths and workflows.
- [ ] Update `STATUS.md` to actual current phase.
- [ ] Ensure `profiles/project-profile.yaml` reflects true stack/constraints.
- [ ] Pin minimal skill set in `profiles/active-skills.yaml`.

## Phase E: Quality and Documentation Alignment
- [ ] Align `docs/README.md`, `docs/SETUP.md`, and `docs/API.md` to implementation reality (or remove if not applicable).
- [ ] Align `qa/test-plan.md`, `qa/issues.md`, `qa/audit-report.md` to current quality process (or remove if not applicable).
- [ ] Run one small end-to-end harness cycle to validate alignment.

## Done Criteria
- [ ] `AGENTS.md` is present and accessible as the agent bootstrap entry point.
- [ ] No critical mismatch between codebase reality and harness specs/docs.
- [ ] Irrelevant templates removed and logged in `DECISIONS.md`.
- [ ] At least one phase transition completed with gate PASS/FAIL output.
- [ ] Team can continue delivery using harness runbook playbooks.
