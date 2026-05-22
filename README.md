# Agent Trainer Harness

File-first multi-agent harness for AI-assisted product delivery. Framework-agnostic — works with Claude Code, Cursor, Copilot, or any AI IDE. Public distribution of the reusable Agent Trainer Harness templates. Private dogfood/internal forks may carry additional operator-specific guardrails; this public repo should remain generic and reusable.

## Pick Your Mode

| Question | Lite | Full | Concurrent |
|----------|------|------|------------|
| **Scope** | 1-2 phases, single concern | 3+ phases, multi-role delivery | Large parallel build |
| **Autonomy** | Human-in-the-loop | Human-in-the-loop or autonomous | Fully autonomous |
| **Roles** | 3 (Orchestrator, Engineer, QA) | 10 (PM, Designer, Engineers, QA, Docs, Growth, SME) | 10 + parallel workers |
| **Gates** | Informal | Formal gate log in STATUS.md | LLM-judged gates |
| **When** | Bug fixes, scripts, small features | MVPs, SaaS products, multi-week builds | Week-long autonomous builds |

## Quick Start

All harness modes now use the same canonical `STATUS.md` header: `State`, `Current Phase`, `Last Updated`, `Current Gate`, `Next Step`, `Review Cadence`, and `Re-entry Condition` (required for `Monitor` / `Parked`, otherwise `N/A`). Agents are expected to preserve that header on every update.

Each copied harness carries a machine-readable `.harness-version` file. This is the version/drift anchor for read-only reporting; it is not an auto-upgrade mechanism. Run `scripts/harness_drift_report.py` (read-only) to compare vendored project copies against the canonical templates — it reports version delta, managed-file divergence, and project-specific section flags without modifying anything.

Concurrent mode is currently **parked / opt-in**. Keep its validators passing, but do not invest in Concurrent propagation or refactors unless a project explicitly chooses that mode or a dedicated dogfood run is scheduled.

## Latest hardening updates

This public distribution includes the current Lite-first harness hardening:

- **Decide before build**: Lite `AGENTS.md` requires agents to state approach and open unknowns before non-trivial implementation.
- **Done means verified**: Lite mode now has an explicit self-check before claiming completion, including test/build/validation evidence or an `Unable to verify` note.
- **Fresh-context delegation**: heavy research, broad sweeps, and independent audits should run in fresh-context subagents; small local edits stay local.
- **Checklist roles**: Lite role files are plain Orchestrator / Engineer / QA checklists, not persona prompts.
- **Version and drift reporting**: `.harness-version` files and `scripts/harness_drift_report.py` provide read-only reporting for version delta, managed-file drift, and project-specific section flags. The reporter never mutates project files.
- **Public-safe wording**: private operator-specific guidance has been generalized for public reuse.

### New Project

1. Pick your mode from the table above.
2. Copy the contents of that mode's `new-project/` folder into your empty repo.
3. Open `start.md` and follow the instructions.
4. If your environment uses `uv`, avoid inheriting unrelated active virtualenvs: do not use `uv run --active ...` / `uv --active run ...`; use plain `uv run ...` or explicit repo-local `.venv/bin/...` commands.

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
│   ├── new-project/      16 files — copy into empty repo
│   └── existing-project/ 16 files — audit-first onboarding
├── full/
│   ├── new-project/      85 files — copy into empty repo
│   └── existing-project/ 85 files — audit-first onboarding
├── concurrent/
│   ├── new-project/     100 files — copy into empty repo
│   └── existing-project/100 files — audit-first onboarding
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
- **Runtime truth over stale artifacts**: For deployment/live-run work, verify the actual runtime before calling status decision-grade; mark superseded deploy/config sections as **historical**. If multi-agent work is needed, propose the split explicitly rather than drifting into overlap.

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
- [claude-mem](https://github.com/thedotmack/claude-mem) — automatic session memory with progressive disclosure, semantic compression
- [qmd](https://github.com/tobi/qmd) — local hybrid search (BM25 + vector + re-ranking) over markdown knowledge bases

## License

MIT — see [LICENSE](LICENSE).
