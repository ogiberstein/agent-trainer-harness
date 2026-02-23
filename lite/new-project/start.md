# Lite Mode — Start Here

Use this mode for small projects: single developer, short timeline, low risk.

## When to Use Lite
- Simple scope and straightforward architecture.
- Delivery target under 1-2 weeks.
- Minimal handoff complexity.
- Solo developer or single-agent execution.

## When to Upgrade
Switch to **Full** mode if any of these occur:
- Scope expands beyond initial assumptions.
- Multiple stakeholders and frequent requirement changes.
- Quality/compliance expectations increase.
- Rework loops become frequent.

See `full/existing-project/start.md` in the harness repo for the upgrade path.

---

## Setup

1. Fill in `BRIEF.md` with your project scope and constraints.
2. Review `profiles/project-profile.yaml` — update tech stack and quality bars.
3. Set `STATUS.md` Current Phase to `requirements`.
4. Read `operations/context-efficiency-guidelines.md`.

## Phase Sequence

### Phase 1 — Requirements (Light)
- **Active role:** Orchestrator (wearing PM hat)
- **Produce:** `specs/requirements.md` (FRs + ACs, minimal but complete)
- **Gate:** every FR has at least 2 acceptance criteria, out-of-scope is explicit
- Human approval required before moving forward.

### Phase 2 — Implementation
- **Active role:** Fullstack Engineer
- **Produce:** code in `src/` and tests in `tests/`
- **Gate:** core FRs implemented, tests present and runnable

### Phase 3 — QA (Light)
- **Active role:** QA Engineer
- **Produce:** `qa/issues.md` (any Critical/Major issues found)
- **Gate:** no Critical issues open. Major issues documented with human decision.

### Phase 4 — Final Review
- Compile delivery summary: what was built, what is deferred, risks.
- Update `STATUS.md` Current Phase to `complete` (if all gates pass).

## Execution Rules
- Never bypass gate criteria silently.
- Every phase transition must update `STATUS.md`.
- Log non-trivial decisions in `DECISIONS.md`.
- If blocked or ambiguous, escalate with a concise question and options.
- Keep context minimal — load only phase-relevant files.

## Day 0 Sanity Checklist
- [ ] `BRIEF.md` completed with concrete scope and constraints.
- [ ] `profiles/project-profile.yaml` reviewed.
- [ ] `STATUS.md` set to `requirements`.
- [ ] Ready to execute Phase 1.
