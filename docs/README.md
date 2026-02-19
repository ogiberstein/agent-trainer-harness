# Agent Trainer Harness

File-first multi-agent harness for running product delivery workflows from brief to release, with optional growth and domain skill packs.

## Start Here
- Bootstrap instructions for agents: `AGENTS.md`
- Full mode: `day-0-start.md`
- Lite mode (small projects): `lite-mode-checklist.md`
- Existing repo onboarding: `migration-checklist.md`
- Command runbooks: `COMMANDS.md`
- End-to-end example: `docs/walkthrough.md`
- Future roadmap: `FUTURE_IMPROVEMENTS.md`
- Existing-project drop-in bundle (alignment-first): `starter_kit_existing_projects/`
- Framework-specific shims: `starter_kit_existing_projects/framework-shims/`
- Vision and architecture narrative: `architecture-spec.md`

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
- Framework-agnostic bootstrap (`AGENTS.md`) with optional framework shims

## Historical Setup Notes
Initial setup artifacts have been archived for reference in:
- `docs/archive/initial-setup/`

## Contributing
See `docs/CONTRIBUTING.md`.

## License
This project is licensed under the MIT License – see `LICENSE` at the repository root.
