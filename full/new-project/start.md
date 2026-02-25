# Full Mode — Start Here

## Quick Start

1. Fill in `BRIEF.md` — your project scope and constraints.
2. Read `AGENTS.md` — operating rules and file zones.
3. Read `STATUS.md` — current phase.
4. Customize `profiles/project-profile.yaml` — tech stack and quality bars.
5. Set `STATUS.md` Current Phase = requirements. Begin Phase 1.

Everything below is reference. Load on-demand as phases progress.

---

## Full Setup (first-time projects)

1. Read `COMMANDS.md` and `operations/context-efficiency-guidelines.md`.
2. Perform Setup Engineer workflow (`harness/agents/setup-engineer.md`):
   - Produce `profiles/merged-profile.yaml`
   - Generate role prompts in `harness/generated-agents/` for needed roles
   - Validate `harness/adapter-config.yaml`
3. Log setup decisions in `DECISIONS.md`.
4. Review skills: check `skills/skill-review-checklist.md` before enabling non-core skills. Pin in `profiles/active-skills.yaml`.

---

## Phase Sequence

### Phase 1 — Requirements
- **Active role:** Product Manager
- If growth is relevant: run Growth Strategist input pass for SEO/GEO/analytics requirements
- **Produce:** `specs/requirements.md`, `handoffs/product-to-design.md`
- **Gate:** every FR has user story + at least 2 ACs; edge cases and out-of-scope explicit; Risks/Assumptions section filled; open questions listed
- Record gate result in STATUS.md Gate Log. Human approval before advancing.

### Phase 2 — Design
- **Active role:** Designer
- **Produce:** `specs/ui-spec.md`, `specs/architecture.md`, `handoffs/design-to-engineering.md`
- **Gate:** component states defined; responsive/a11y specified; architecture includes data model + API
- Record gate result. Human approval before advancing.

### Phase 3 — Implementation
- **Active roles:** Fullstack Engineer, then Frontend Engineer
- **Produce:** code in `src/`, tests in `tests/`, `handoffs/engineering-to-qa.md`
- **Gate:** core FRs implemented; integration path clear; tests present and runnable
- Record gate result.

### Phase 4 — QA
- **Active role:** QA Engineer
- **Produce:** `qa/test-plan.md`, `qa/issues.md`, `qa/audit-report.md`, `handoffs/qa-to-engineering.md`
- **Gate:** no Critical/Major issues open (unless human-approved exception); ship recommendation present
- Record gate result.

### Phase 5 — Documentation
- **Active role:** Documentation Writer
- **Produce:** `docs/README.md`, `docs/SETUP.md`, `docs/API.md`, `docs/CONTRIBUTING.md`
- **Gate:** no placeholders; setup steps explicit; known issues reflected from QA
- Record gate result.

### Phase 6 — Growth (Optional)
- **Active role:** Growth Strategist
- **Produce:** `specs/growth-plan.md`, growth handoffs
- **Gate:** SEO/GEO strategy measurable; experiment backlog with hypothesis + metric
- Record gate result.

### Phase 7 — Final Review
- Compile delivery summary: what was built, deferred, risks, recommended next iteration.
- Update `STATUS.md` Current Phase = complete.

---

## Execution Rules

- Never skip a phase. Never bypass gate criteria silently.
- Every phase transition must update `STATUS.md`.
- Every non-trivial decision must be logged in `DECISIONS.md`.
- After each phase, write a summary to `memory/summaries/phase-{N}-{name}.md`.
- Record gate result in STATUS.md Gate Log (PASS/FAIL/SKIPPED with evidence) before advancing.
- If blocked or ambiguous, escalate with a concise question and options.
- Follow `operations/context-efficiency-guidelines.md`.
