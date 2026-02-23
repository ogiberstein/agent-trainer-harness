# Full Mode — Start Here

Use this to launch a new project with the full multi-agent harness. Works in manual mode (human-as-orchestrator) or autonomous mode (agent self-enforces gates).

## How to Use

1. Fill in `BRIEF.md` with your project scope and constraints.
2. Follow the setup steps below, then execute the phase sequence.
3. For existing projects, use `full/existing-project/start.md` instead.
4. For small projects, use `lite/new-project/start.md` instead.

---

## Setup

1. Read these files:
   - `AGENTS.md` — operating instructions and file zones
   - `STATUS.md` — current phase
   - `BRIEF.md` — project scope and constraints
   - `profiles/project-profile.yaml` — customize tech stack and quality bars
   - `COMMANDS.md` — available runbook playbooks
   - `operations/context-efficiency-guidelines.md`
2. Perform Setup Engineer workflow (`harness/agents/setup-engineer.md`):
   - Produce `profiles/merged-profile.yaml`
   - Generate role prompts in `harness/generated-agents/` for needed roles
   - Validate `harness/adapter-config.yaml`
3. Update `STATUS.md`: Current Phase = requirements.
4. Log setup decisions in `DECISIONS.md`.
5. Review skills: check `skills/skill-review-checklist.md` before enabling non-core skills. Pin selections in `profiles/active-skills.yaml`.
6. Optional: activate `market-opportunity-research` skill -> produce `specs/market-research.md`.
7. Optional: activate `user-research-discovery` skill -> produce `specs/user-research.md`.

---

## Phase Sequence

### Phase 1 — Requirements
- **Active role:** Product Manager
- If growth is relevant: run Growth Strategist input pass for SEO/GEO/analytics requirements
- **Produce:** `specs/requirements.md`, `handoffs/product-to-design.md`
- **Gate:** every FR has user story + at least 2 ACs; edge cases and out-of-scope explicit; open questions listed
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

## Day 0 Sanity Checklist

- [ ] `BRIEF.md` completed with concrete scope and constraints.
- [ ] `profiles/project-profile.yaml` customized.
- [ ] `profiles/merged-profile.yaml` generated.
- [ ] `harness/generated-agents/` populated for needed roles.
- [ ] `STATUS.md` set to `requirements`.
- [ ] `DECISIONS.md` has setup decisions logged.
- [ ] Skills reviewed via `skills/skill-review-checklist.md`.
