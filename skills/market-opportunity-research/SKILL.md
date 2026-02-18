---
name: market-opportunity-research
description: Produces structured market opportunity research reports for new projects, including TAM/SAM/SOM framing, competitor landscape, user segments, edge hypotheses, and opportunity scoring. Use when kicking off product strategy, especially for trading, prediction-market, or domain-specific opportunities.
---

# Market Opportunity Research

## Purpose
Create a decision-ready research brief before implementation begins.

## Use When
- Starting a new product and validating opportunity scope.
- Evaluating niches (for example, prediction-market bots such as Polymarket workflows).
- Prioritizing where to focus initial build effort.

## Inputs Required
- Project objective from `BRIEF.md`
- Target domain and user segment assumptions
- Any known constraints (regulatory, technical, geography, timeline)
- Existing references or competitor list (optional)

## Steps
1. Restate objective and assumptions.
2. Define market framing (problem, segment, why-now signal).
3. Map competitor landscape and current alternatives.
4. Identify user pain points, willingness-to-pay/value proxy, and adoption blockers.
5. Generate 5-10 opportunity hypotheses with evidence confidence.
6. Score opportunities by impact, feasibility, and time-to-value.
7. Recommend top 1-3 opportunities and next validation actions.

## Output Contract
- Primary report: `specs/market-research.md`
- Optional summary for decisions: `DECISIONS.md` entry with selected opportunity and rationale

## Report Template
```markdown
# Market Opportunity Report: [Project]

## Objective

## Assumptions and Constraints

## Market and Segment Snapshot

## Competitor and Alternatives Map

## Opportunity Hypotheses
| ID | Opportunity | Evidence | Confidence | Feasibility | Impact | Score |
|---|---|---|---|---|---|---|

## Recommended Opportunities
1. ...
2. ...
3. ...

## Risks and Unknowns

## Next Validation Actions (7-14 days)
```

## Safety and Security
- Distinguish facts from assumptions.
- Do not present uncertain estimates as certainties.
- For regulated domains, flag legal/compliance uncertainty for human review.
