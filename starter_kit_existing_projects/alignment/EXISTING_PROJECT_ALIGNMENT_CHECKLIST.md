# Existing Project Alignment Checklist

Use this after core harness files are copied into the target repo.

## Phase A: Discovery and Mapping
- [ ] Verify `AGENTS.md` is present at repo root and readable by the agent.
- [ ] Inventory existing docs/specs and map to harness expectations.
- [ ] Identify gaps, stale artifacts, and conflicting terminology.
- [ ] Record major assumptions in `DECISIONS.md`.

## Phase B: Requirements and Architecture Alignment
- [ ] Align `specs/requirements.md` to current product behavior.
- [ ] Align `specs/architecture.md` to actual implementation.
- [ ] Align `specs/ui-spec.md` where UI exists.
- [ ] Add optional `specs/user-research.md` and/or `specs/market-research.md` when relevant.

## Phase C: Operational Alignment
- [ ] Ensure handoff files reference real project paths and workflows.
- [ ] Update `STATUS.md` to actual current phase.
- [ ] Ensure `profiles/project-profile.yaml` reflects true stack/constraints.
- [ ] Pin minimal skill set in `profiles/active-skills.yaml`.

## Phase D: Quality and Documentation Alignment
- [ ] Align `docs/README.md`, `docs/SETUP.md`, and `docs/API.md` to implementation reality.
- [ ] Align `qa/test-plan.md`, `qa/issues.md`, `qa/audit-report.md` to current quality process.
- [ ] Run one small end-to-end harness cycle to validate alignment.

## Done Criteria
- [ ] `AGENTS.md` is present and accessible as the agent bootstrap entry point.
- [ ] No critical mismatch between codebase reality and harness specs/docs.
- [ ] At least one phase transition completed with gate PASS/FAIL output.
- [ ] Team can continue delivery using harness commands and policies.
