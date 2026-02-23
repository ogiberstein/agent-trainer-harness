---
name: handoff-quality-auditor
description: Audits handoff documents for completeness, ambiguity, and downstream executability. Use when transferring work between product, design, engineering, QA, and documentation roles.
---

# Handoff Quality Auditor

## Purpose
Prevent downstream rework by validating handoff quality before transfer.

## Use When
- Any handoff file in `handoffs/` is created or updated.
- A downstream role reports missing context or unclear requirements.

## Required Inputs
- `handoffs/*.md`
- Upstream artifact references listed in handoff deliverables

## Checklist
- Context is sufficient for the receiving role.
- Deliverables include concrete file paths.
- Open questions are explicit (or "none").
- Acceptance criteria are testable.
- Constraints are listed and actionable.
- Status is one of `draft`, `ready`, `revision-needed`.

## Workflow
1. Parse handoff sections against the template.
2. Validate each deliverable path exists and is current.
3. Flag ambiguity, missing constraints, or non-testable criteria.
4. Output `ready` or `revision-needed` with exact fixes.

## Output Format
```markdown
## Handoff Audit: [source -> target]
- Decision: ready | revision-needed
- Missing items:
  - [item]
- Ambiguities:
  - [item]
- Fixes required:
  1. [fix]
  2. [fix]
```

## Guardrails
- Never approve a handoff with missing acceptance criteria.
- Never accept vague deliverables like "code changes" without file references.
