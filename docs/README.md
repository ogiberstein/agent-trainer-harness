# Agent Trainer Harness

File-first multi-agent harness for running product delivery workflows from brief to release. Framework-agnostic — works with Claude Code, Cursor, Copilot, or any AI IDE.

## Quick Start: Pick Your Path

### New project

| Mode | Start with | What you get |
|---|---|---|
| **Lite** (solo dev, small scope, < 2 weeks) | `lite-mode-checklist.md` | 3 roles, 4 phases, minimal overhead |
| **Full** (multi-role team, SaaS, UI + backend) | `day-0-start.md` | All roles, all phases, full gate ceremony, human-in-the-loop |
| **Concurrent** (autonomous, parallel workers) | `runtime/run.py` | All roles run as parallel Claude Code workers; you define scope and walk away |

**Lite and Full** start from a clean repo. Paste the prompt from the relevant file into your AI IDE and follow the phase sequence.

**Concurrent** is fully autonomous. Setup for a new project:

```bash
# 1. Fork/clone this repo, or copy harness files into a fresh project
git clone https://github.com/ogiberstein/agent-trainer-harness.git my-project
cd my-project

# 2. Fill in BRIEF.md (project scope, users, constraints, success criteria)
# 3. Edit profiles/project-profile.yaml (tech stack, quality bars)
# 4. Edit runtime/config.yaml (model, max_workers, notification webhook)

# 5. Install Python deps
pip install -r runtime/requirements.txt

# 6. Start the orchestrator (from anywhere — path to run.py is explicit)
python runtime/run.py --project .

# 7. Review requirements when notified, then resume
python runtime/run.py --project . --resume
```

The orchestrator spawns parallel Claude Code CLI workers, each in its own git worktree. It enforces LLM-based gate checks, merges branches, and notifies you on completion or failure. See `runtime/DESIGN.md` for the full architecture.

**Prerequisites:** Python 3.10+, Claude Code CLI installed and authenticated (`claude --version`), Git.

### Existing project

Use the starter kit to drop harness files into a project that already has code, docs, and history.

```bash
bash copy_core.sh --preset <preset> /path/to/your-project
```

| Preset | Use for | What it copies |
|---|---|---|
| `full` | SaaS, multi-role teams | Everything including `runtime/` for Concurrent mode |
| `backend` | APIs, bots, headless services | Skips UI specs, designer/frontend/growth files; includes `runtime/` |
| `minimal` | Solo dev, small existing projects | Just core files + 3 agent prompts + profiles + memory (no runtime) |

After copying, run the alignment flow to reconcile your existing docs/specs with the harness:

1. Paste `starter_kit_existing_projects/alignment/EXISTING_PROJECT_ALIGNMENT_PROMPT.md` into your IDE
2. Follow `migration-checklist.md` for the full onboarding checklist

The copy script is safe-mode: it aborts on any existing conflicts and never overwrites your files. Existing `specs/`, `docs/`, and `qa/` are aligned in place, not replaced.

### Already using `CLAUDE.md` or similar agent config?

The harness coexists with agent-level configs like `~/.claude/CLAUDE.md` or `.cursorrules`:

- **Your agent config** defines *how the agent works* — behavior, delegation, verification, tone, coding standards.
- **The harness (`AGENTS.md`)** defines *what the agent works on* — project phase, which files to read, quality gates, protection rules.

Both apply simultaneously. Add a "Harness-Aware Mode" trigger to your agent config that activates when `AGENTS.md` exists at repo root. See the harness's `AGENTS.md` "Coexistence with Agent-Level Configs" section for the integration contract.

Key integration points:
- **Task tracking:** use your agent config's todos for granular within-session steps; use `STATUS.md` for cross-session phase state.
- **Skills:** agent-config skills (coding standards, PR review) and harness skills (`skills/` directory) are complementary — process vs. domain.
- **Delegation:** agent-config tool-agents (explore, librarian) run alongside harness role-personas (PM, Engineer, QA).
- **Proportionality:** small changes skip full harness ceremony — aligns with typical Trivial/Explicit request classification.

## How It Works

`AGENTS.md` is the single entry point. Every framework shim (Cursor rules, Claude Code, Copilot instructions) points to it. The agent reads `STATUS.md` and `BRIEF.md` first, then loads only phase-relevant files.

**Roles:** Product Manager, Designer, Fullstack Engineer, Frontend Engineer, QA Engineer, Documentation Writer, optional Growth Strategist and Domain SME.

**Phases:** Requirements → Design → Implementation → QA → Documentation → Growth (optional) → Final Review. Each phase has explicit gate criteria that must pass before advancing.

**Protection:** Core infrastructure files (`AGENTS.md`, `BRIEF.md`, `STATUS.md`, `DECISIONS.md`, `harness/`, `profiles/`, `memory/`, `evaluation/`) are always protected. Irrelevant template files can be pruned if logged in `DECISIONS.md`.

## Core System Areas

- `runtime/`: autonomous concurrent orchestrator (Python), worker wrappers, gate evaluator, merge steward

- `harness/`: role prompts, routing policy, permissions, adapter contract
- `profiles/`: org/project merged profiles and active skill selection
- `operations/`: tracker (board + dashboard + workflow + inbox), runbook (+ SLAs), guidelines
- `skills/`: private skill library, packs, registry, review/security policy
- `evaluation/`: release gates, scorecard, regressions, golden tasks
- `handoffs/`: structured agent-to-agent handoff templates

## Reference

- Bootstrap instructions for agents: `AGENTS.md`
- Runbook playbooks: `COMMANDS.md`
- Vision and architecture narrative: `architecture-spec.md`
- Future roadmap: `FUTURE_IMPROVEMENTS.md`
- Framework-specific shims: `starter_kit_existing_projects/framework-shims/`
- Optional Domain SME pattern: see `harness/agents/domain-sme.md`
- Concurrent mode architecture: `runtime/DESIGN.md`

## Contributing

See `docs/CONTRIBUTING.md`.

## License

This project is licensed under the MIT License – see `LICENSE` at the repository root.
