---
name: growth-experimentation-roadmap
description: Prioritizes growth experiments with hypothesis quality, impact-confidence-effort scoring, guardrails, and stop/go criteria. Use when creating measurable experiment backlogs for product and marketing growth.
---

# Growth Experimentation Roadmap

## Purpose
Create a high-signal experiment backlog with clear hypotheses and decision criteria.

## Use When
- Establishing growth experimentation process.
- Prioritizing limited execution capacity.

## Inputs Required
- `specs/growth-plan.md`
- Baseline performance metrics (if available)
- Team capacity and implementation constraints

## Steps
1. Define experiment objective linked to a business metric.
2. Write hypothesis in if/then/because format.
3. Score opportunities via impact/confidence/effort.
4. Add guardrails and stop conditions.
5. Sequence experiments into sprint-ready roadmap.

## Output Contract
- Prioritized experiment table in `specs/growth-plan.md`
- Execution requirements in `handoffs/growth-to-engineering.md`

## Safety and Security
- Do not run experiments that compromise user trust or compliance.
- Include rollback criteria for risky tests.
