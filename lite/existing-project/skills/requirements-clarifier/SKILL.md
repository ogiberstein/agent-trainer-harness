---
name: requirements-clarifier
description: Converts vague project briefs into testable requirements with user stories, acceptance criteria, edge cases, and explicit scope boundaries. Use when drafting or refining product requirements.
---

# Requirements Clarifier

## Purpose
Produce implementation-ready requirements from ambiguous input.

## Use When
- Starting a new project from a rough brief.
- Requirements are inconsistent, incomplete, or not testable.
- Scope boundaries are unclear.

## Required Inputs
- `BRIEF.md`
- Any user Q&A notes
- Existing `specs/requirements.md` (if present)

## Workflow
1. Extract goals, users, constraints, and success criteria.
2. Detect ambiguity and list clarifying questions.
3. Draft functional requirements with MoSCoW priorities.
4. Add at least 2 acceptance criteria per requirement.
5. Add edge cases and explicit out-of-scope items.
6. Write unresolved items to Open Questions.

## Output Contract
- Update `specs/requirements.md`.
- Include:
  - Problem statement
  - Personas
  - Functional and non-functional requirements
  - Constraints
  - Open questions

## Quality Bar
- Every FR has user story + >=2 acceptance criteria.
- Every FR has at least one edge case.
- Out-of-scope is explicit to prevent scope creep.

## Guardrails
- Do not make architecture or tool-level decisions here.
- Do not silently assume missing business rules.
