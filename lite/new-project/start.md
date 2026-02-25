# Lite Mode — Start Here

## Quick Start

1. Fill in `BRIEF.md` — your project scope and constraints.
2. Read `AGENTS.md` — operating rules and file zones.
3. Set `STATUS.md` Current Phase = requirements. Begin Phase 1.

---

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
2. Set `STATUS.md` Current Phase to `requirements`.
3. Skim `operations/context-efficiency-guidelines.md` for token discipline basics.

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
- [ ] `STATUS.md` set to `requirements`.
- [ ] Ready to execute Phase 1.
