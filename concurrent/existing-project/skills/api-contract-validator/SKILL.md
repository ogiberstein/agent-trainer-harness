---
name: api-contract-validator
description: Validates consistency between API specifications, backend implementation, and frontend usage. Use when reviewing architecture/API changes or before QA and release gates.
---

# API Contract Validator

## Purpose
Catch API drift early by checking spec-to-code-to-client consistency.

## Use When
- API endpoints are added or changed.
- Frontend and backend integration is in progress.
- Preparing for QA gate.

## Required Inputs
- `specs/architecture.md` (API section)
- Backend code in `src/`
- Frontend integration code in `src/`
- Relevant tests in `tests/`

## Validation Steps
1. Build endpoint inventory from spec.
2. Compare method/path/auth/request/response against backend implementation.
3. Compare frontend calls and payload expectations against backend behavior.
4. Verify validation and error status handling.
5. Report mismatches with severity and recommended fix owner.

## Severity Rules
- Critical: contract mismatch blocks core flow.
- Major: incorrect error or auth behavior with business impact.
- Minor: non-breaking documentation or naming mismatch.

## Output Format
```markdown
## API Contract Validation
- Summary: [pass/fail]
- Mismatches:
  - [severity] [endpoint] [problem] [owner]
- Coverage gaps:
  - [missing tests/spec detail]
- Recommended actions:
  1. [action]
```

## Guardrails
- Treat undocumented endpoint behavior as mismatch.
- Do not assume client behavior from naming alone; verify call sites.
