---
name: orchestrator-phase-gate-enforcer
description: Enforces phase order, gate criteria, and required status updates for multi-agent delivery workflows. Use when orchestrating requirements, design, implementation, QA, documentation, and release transitions.
---

# Orchestrator Phase Gate Enforcer

## Purpose
Ensure no phase transition happens without explicit gate checks, evidence, and required file updates.

## Use When
- Running a project through the harness lifecycle.
- A team is skipping steps or moving forward with unclear quality.
- You need consistent PASS/FAIL gate outcomes.

## Required Inputs
- `STATUS.md`
- `DECISIONS.md`
- `harness/routing-policy.md`
- Relevant phase artifacts in `specs/`, `src/`, `tests/`, `qa/`, `docs/`

## Workflow
1. Identify current phase from `STATUS.md`.
2. Read gate criteria for the next phase.
3. Check evidence files against criteria.
4. Emit gate result as `PASS` or `FAIL` with concrete reasons.
5. Update `STATUS.md` and log non-trivial decisions in `DECISIONS.md`.
6. If blocked, escalate with options and recommended next action.

## Output Format
```markdown
## Gate Review: [Phase A -> Phase B]
- Result: PASS | FAIL
- Evidence checked:
  - [file path]
  - [file path]
- Criteria:
  - [criterion]: pass/fail + note
- Risks:
  - [risk]
- Human approval needed: YES | NO
- Next file to edit: [path]
```

## Guardrails
- Never skip requirements or QA gates.
- Never mark pass without artifact evidence.
- Never advance phase without updating `STATUS.md`.
