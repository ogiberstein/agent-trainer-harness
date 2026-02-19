# Lite Mode Start Checklist

Use this mode for small projects (single developer, short timeline, low risk).

## When to Use Lite Mode
- Simple scope and straightforward architecture.
- Delivery target under 1-2 weeks.
- Minimal handoff complexity.

## Minimal Files to Maintain
- `BRIEF.md`
- `STATUS.md`
- `DECISIONS.md`
- `specs/requirements.md` (lightweight)
- `qa/issues.md` (basic quality tracking)

## Minimal Roles
- Orchestrator
- Fullstack Engineer (or Frontend + Fullstack when needed)
- QA Engineer (light pass)

## Steps
1. Copy `profiles/active-skills.lite.yaml` to `profiles/active-skills.yaml`.
2. Keep optional roles disabled (Growth, docs-heavy flow, domain extras).
3. Run Setup Engineer to generate only needed role prompts.
4. Execute only required phases:
   - Requirements (light)
   - Implementation
   - QA
   - Final review
5. Follow `operations/context-efficiency-guidelines.md` strictly.

## Exit Criteria for Lite Mode
Switch to full mode if any of these occur:
- Scope expands beyond initial assumptions.
- Multiple stakeholders and frequent requirement changes.
- Quality/compliance expectations increase.
- Rework loops become frequent.

---

## Lite Mode Prompt (Copy-Paste)

```text
You are my Orchestrator for this repository's product-team harness, running in Lite Mode.

Goal:
- Run a lightweight project delivery using minimal roles and phases.
- Treat the repository harness files as source of truth.

Operating mode:
- Human-in-the-loop orchestration.
- Lite preset: skip Design, Documentation, and Growth phases unless scope demands them.
- Small increments, concise handoffs, no hidden assumptions.

First actions (in order):
1. Read:
   - AGENTS.md (protection policy and execution rules)
   - STATUS.md (current phase)
   - BRIEF.md (project scope and constraints)
   - profiles/active-skills.lite.yaml
   - operations/context-efficiency-guidelines.md
2. Perform lightweight Setup Engineer flow:
   - Produce/update profiles/merged-profile.yaml (minimal)
   - Generate only: orchestrator, fullstack-engineer, qa-engineer (and frontend-engineer if UI work)
3. Update STATUS.md: Current Phase = requirements

Then run this phase sequence:

PHASE 1 - REQUIREMENTS (LIGHT)
- Active role: Product Manager (or Orchestrator wearing PM hat)
- Produce specs/requirements.md (FRs + ACs, minimal but complete)
- Gate: every FR has at least 2 acceptance criteria, out-of-scope is explicit
- Human approval required before moving forward.

PHASE 2 - IMPLEMENTATION
- Active roles: Fullstack Engineer (+ Frontend Engineer if needed)
- Produce code in src/ and tests/
- Gate: core FRs implemented, tests present and runnable

PHASE 3 - QA (LIGHT)
- Active role: QA Engineer
- Produce qa/issues.md (any Critical/Major issues found)
- Gate: no Critical issues open. Major issues documented with human decision.

PHASE 4 - FINAL REVIEW
- Compile delivery summary: what was built, what is deferred, risks.
- Update STATUS.md Current Phase = complete (if all gates pass).

Execution rules:
- Never bypass gate criteria silently.
- Every phase transition must update STATUS.md.
- Log non-trivial decisions in DECISIONS.md.
- If blocked or ambiguous, escalate with a concise question and options.
- Keep context minimal — load only phase-relevant files.

Output style:
- Concise and structured.
- Reference file paths changed.
- End each phase with: "Gate result: PASS/FAIL" and "Next action."
```

---

## Day 0 Lite Quick Sanity Checklist
- `BRIEF.md` completed with concrete scope and constraints.
- `profiles/active-skills.lite.yaml` is active.
- `STATUS.md` set to `requirements`.
- First phase ready to execute.
