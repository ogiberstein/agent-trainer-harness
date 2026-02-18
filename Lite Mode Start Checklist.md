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
