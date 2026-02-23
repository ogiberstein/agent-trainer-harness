---
name: user-research-discovery
description: Conducts structured user discovery by combining stakeholder interviews with online desk research, then synthesizes insights into requirements-ready outputs. Use when refining project requirements and reducing assumption risk before design/implementation.
---

# User Research Discovery

## Purpose
Improve requirement quality by grounding decisions in real user needs and external evidence.

## Use When
- Project goals are still ambiguous.
- Product manager needs stronger evidence before finalizing scope.
- You want interview + desk research synthesis before writing requirements.

## Inputs Required
- `BRIEF.md`
- Initial hypotheses and constraints
- Interview answers from stakeholder/user sessions
- Relevant online sources for desk research

## Steps
1. Define discovery questions (users, pains, alternatives, triggers, constraints).
2. Interview stakeholder/user and capture direct quotes or explicit claims.
3. Run desk research on market behavior, competitor patterns, and user signals.
4. Separate facts, assumptions, and unknowns.
5. Synthesize insights into actionable requirement implications.
6. Propose follow-up questions where confidence is low.

## Output Contract
- `specs/user-research.md` (interview + desk research synthesis)
- Update `specs/requirements.md` with evidence-backed refinements
- Log major scope/priority decisions in `DECISIONS.md`

## Report Template
```markdown
# User Research Synthesis: [Project]

## Research Scope

## Interview Findings
- Insight:
- Evidence:

## Desk Research Findings
- Source:
- Finding:

## Facts vs Assumptions
- Facts:
- Assumptions:
- Unknowns:

## Requirement Implications
- FR/NFR updates:
- Priority shifts:

## Open Questions
```

## Safety and Security
- Cite source links for external claims.
- Mark uncertain findings clearly; do not overstate confidence.
- Escalate legal/compliance uncertainty for human review.
