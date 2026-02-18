# Agent Trainer Harness

File-first multi-agent harness for running product delivery workflows from brief to release, with optional growth and domain skill packs.

## Start Here
- Full mode: `Day 0 Start with this Prompt.md`
- Lite mode (small projects): `Lite Mode Start Checklist.md`
- Existing repo onboarding: `Existing Project Migration Checklist.md`
- Command runbooks: `COMMANDS.md`

## Optional Domain SME Pattern
- Keep core team lean by default.
- Add a Domain SME role only when domain complexity/risk is high (finance, healthcare, regulated workflows).
- Prefer enabling domain skills first; promote to a full Domain SME agent only if repeated domain ambiguity causes rework.
- Recommended kickoff for domain-heavy projects: run `market-opportunity-research` and write `specs/market-research.md` before finalizing scope.
- For user-need clarity, run `user-research-discovery` and write `specs/user-research.md` before locking requirements.

## Core System Areas
- `harness/`: role prompts, routing policy, permissions, adapter contract
- `profiles/`: org/project merged profiles and active skill selection
- `operations/`: board, dashboard, runbook, SLAs, workflow-state, inbox
- `skills/`: private skill library, packs, registry, review/security policy
- `evaluation/`: release gates, scorecard, regressions, golden tasks
- `handoffs/`: structured agent-to-agent handoff templates

## Starter Scaffold Status
The initial scaffold is complete and includes:
- Core templates (`BRIEF.md`, `STATUS.md`, `DECISIONS.md`)
- Specs templates (`specs/requirements.md`, `specs/ui-spec.md`, `specs/architecture.md`, optional `specs/growth-plan.md`)
- Base role prompts and generated-agent destination
- Memory policies and retention structure
- QA, docs, operations, and governance templates

## Historical Setup Notes
Initial setup artifacts have been archived for reference in:
- `docs/archive/initial-setup/`

## Contributing
See `docs/CONTRIBUTING.md`.
