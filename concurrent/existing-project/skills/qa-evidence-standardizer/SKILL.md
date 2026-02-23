---
name: qa-evidence-standardizer
description: Standardizes QA findings with reproducible steps, severity rationale, traceability to acceptance criteria, and clear ship recommendations. Use when preparing QA issues and audit reports.
---

# QA Evidence Standardizer

## Purpose
Make QA outputs reproducible, auditable, and decision-ready.

## Use When
- Creating or reviewing `qa/test-plan.md`, `qa/issues.md`, `qa/audit-report.md`.
- Teams report issues without enough detail to reproduce.

## Required Inputs
- `specs/requirements.md`
- `qa/test-plan.md`
- `qa/issues.md`
- `qa/audit-report.md`

## Workflow
1. Ensure each acceptance criterion maps to at least one test case.
2. Verify issue entries include full reproduction steps and expected vs actual.
3. Validate severity assignment with rationale.
4. Ensure audit report includes ship recommendation and unresolved issues.

## Severity Guidance
- Critical: blocks core user path or causes unsafe behavior.
- Major: significant degradation without full path blockage.
- Minor: limited functional impact.
- Cosmetic: visual/text-only issue.

## Output Format
```markdown
## QA Evidence Review
- Coverage: [x/y acceptance criteria covered]
- Issues quality: [good/needs work]
- Missing evidence:
  - [item]
- Recommendation quality: [clear/unclear]
- Required fixes before gate:
  1. [fix]
```

## Guardrails
- Never mark a test as pass without artifact-backed verification.
- Mark untestable items as blocked with reason, never as pass.
