# Core File/Folder List

The copy script supports three presets: `full`, `backend`, `minimal`.

## Preset: full (default)

All harness files. Use for SaaS, multi-role teams, projects with UI + growth.

**Root files:** `AGENTS.md`, `BRIEF.md`, `STATUS.md`, `DECISIONS.md`, `COMMANDS.md`, `FUTURE_IMPROVEMENTS.md`, `migration-checklist.md`

**Directories:** `harness/`, `profiles/`, `memory/`, `evaluation/`, `operations/`, `skills/`, `handoffs/`, `specs/`, `qa/`, `docs/`

## Preset: backend

Skips UI, design, growth, and frontend. Use for APIs, bots, headless services.

**Root files:** same as full

**Directories:** `harness/`, `profiles/`, `memory/`, `evaluation/`, `operations/`, `skills/`, `handoffs/`

**Removed after copy:** `specs/ui-spec.md`, `specs/growth-plan.md`, `specs/user-research.md`, `specs/market-research.md`, `harness/agents/designer.md`, `harness/agents/frontend-engineer.md`, `harness/agents/growth-strategist.md`, `handoffs/design-to-engineering.md`, `handoffs/product-to-design.md`, `handoffs/growth-to-*.md`, `skills/growth-*`

## Preset: minimal

Bare essentials. Use for solo dev, small existing projects.

**Root files:** `AGENTS.md`, `BRIEF.md`, `STATUS.md`, `DECISIONS.md`

**Directories:** `profiles/`, `memory/`

**Additionally copied:** `specs/requirements.md`, `harness/agents/orchestrator.md`, `harness/agents/fullstack-engineer.md`, `harness/agents/qa-engineer.md`

## Excluded from all presets

New-project-only docs (`day-0-start.md`, `lite-mode-checklist.md`) are not copied for existing-project use. Use those from the full harness for greenfield projects.

## Usage

```bash
bash copy_core.sh /path/to/target                          # full preset
bash copy_core.sh --preset backend /path/to/target          # backend preset
bash copy_core.sh --preset minimal /path/to/target          # minimal preset
bash copy_core.sh --source ~/harness --preset backend /path  # explicit source
```
