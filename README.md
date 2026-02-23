# Agent Trainer Harness

File-first multi-agent harness for AI-assisted product delivery. Framework-agnostic — works with Claude Code, Cursor, Copilot, or any AI IDE.

## Pick Your Mode

| Question | Lite | Full | Concurrent |
|----------|------|------|------------|
| **Scope** | 1-2 phases, single concern | 3+ phases, multi-role delivery | Large parallel build |
| **Autonomy** | Human-in-the-loop | Human-in-the-loop or autonomous | Fully autonomous |
| **Roles** | 3 (Orchestrator, Engineer, QA) | 10 (PM, Designer, Engineers, QA, Docs, Growth, SME) | 10 + parallel workers |
| **Gates** | Informal | Formal gate log in STATUS.md | LLM-judged gates |
| **When** | Bug fixes, scripts, small features | MVPs, SaaS products, multi-week builds | Week-long autonomous builds |

## Quick Start

### New Project

1. Pick your mode from the table above.
2. Copy the contents of that mode's `new-project/` folder into your empty repo.
3. Open `start.md` and follow the instructions.

```
# Example: start a new full-mode project
cp -R full/new-project/* /path/to/your/new/repo/
cd /path/to/your/new/repo
# Open start.md and follow instructions
```

### Existing Project

1. Pick your mode from the table above.
2. Copy the contents of that mode's `existing-project/` folder into your repo.
3. Open `start.md` — it will guide you through an audit-first onboarding:
   - Audit what exists in your project
   - Classify as well-structured / partial / bare
   - Add only what helps — never overwrite good existing docs
   - Validate with one cycle

```
# Example: add full-mode harness to existing repo
cp -R full/existing-project/* /path/to/your/existing/repo/
cd /path/to/your/existing/repo
# Open start.md and follow the audit-first flow
```

### Graduation Path

Projects naturally grow. The harness supports upgrading between modes:

```
Lite ──────> Full ──────> Concurrent
  │                          ▲
  └──────────────────────────┘
```

- **Lite -> Full**: Add gate log, handoffs, full role library, evaluation criteria, skills library.
- **Lite -> Concurrent**: First upgrade to Full, then add runtime/ and cli/.
- **Full -> Concurrent**: Add runtime/, cli/, configure config.yaml, run preflight.

Each existing-project `start.md` includes a detailed graduation guide.

## CLAUDE.md Integration

If you use Claude Code with a global `~/.claude/CLAUDE.md` config, add this trigger:

> If `AGENTS.md` exists in the project root, read it first and follow harness instructions. The harness defines **what to work on** (phases, gates, files). Your CLAUDE.md defines **how to work** (behavior, delegation, verification). Both apply.

## Folder Structure

```
agent-trainer/
├── README.md         ← you are here
├── LICENSE
├── lite/
│   ├── new-project/      25 files — copy into empty repo
│   └── existing-project/ 25 files — audit-first onboarding
├── full/
│   ├── new-project/      87 files — copy into empty repo
│   └── existing-project/ 87 files — audit-first onboarding
├── concurrent/
│   ├── new-project/     102 files — copy into empty repo
│   └── existing-project/102 files — audit-first onboarding
└── reference/
    └── architecture-spec.md  (frozen original vision)
```

## Design Principles

- **AGENTS.md as map, not manual**: Each mode's AGENTS.md is ~30-60 lines. It tells the agent what to read first and where to find everything else. Detailed rules live in the files they govern.
- **Three-zone model**: Files are labeled as System (never delete), State (update as you work), or App (your workspace). Agents know what to touch and what to protect.
- **Audit-first onboarding**: Existing projects are never blindly overwritten. The agent audits what exists, classifies the project, and adds only what improves outcomes.
- **Proportionality is the mode**: Pick lite for small work, full for features, concurrent for big builds. No need for complex per-mode proportionality rules.
- **Additive phase summaries**: Phase snapshots include "Carried Constraints" to prevent context collapse in long sessions.
- **Mechanical enforcement**: `cli/validate_harness.py` checks consistency. Gate enforcement is structural, not advisory.

## Readings and Influences

This harness was shaped by hands-on trial and error across multiple real projects, combined with ideas from:

- [Harness Engineering](https://openai.com/index/harness-engineering/) (OpenAI, Feb 2026) — AGENTS.md as navigational map, progressive context disclosure, garbage collection agents
- [Exploring Gen AI: Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) (Martin Fowler / Thoughtworks) — harnesses as future service templates, retrofitting challenges
- [AGENTS.md Standard and Best Practices](https://developers.openai.com/codex/guides/agents-md/) — file structure, discovery hierarchy, size guidelines
- [Agentic Context Engineering (ACE)](https://arxiv.org/abs/2510.04618) (Microsoft Research) — context collapse prevention, additive checkpoints
- [Agent READMEs: An Empirical Study](https://arxiv.org/html/2511.12884v1) — analysis of 2,303 context files, what works and what doesn't
- [0xHoneyJar Loa Framework](https://github.com/0xHoneyJar/loa) — three-zone model (System/State/App), lossless ledger protocol
- [Multi-Agent Orchestration Patterns](https://zylos.ai/research/2026-01-06-multi-agent-orchestration-patterns) — handoff validation, hierarchical supervision, failure isolation
- [Agentic Coding Handbook](https://tweag.github.io/agentic-coding-handbook/) (Tweag) — spec-first development, proportionality

## License

MIT — see [LICENSE](LICENSE).
