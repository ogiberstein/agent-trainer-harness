# Memory System

Project memory that survives session boundaries. When an agent returns to a project after a break, this directory is how it reconstructs context without re-reading the entire codebase.

## What Lives Here

```
memory/
├── README.md          ← you are here
├── policies.md        ← write ownership and freshness rules
├── summaries/
│   ├── TEMPLATE.md    ← structure for phase summaries
│   └── phase-*.md     ← one per completed phase (created as you work)
└── snapshots/
    └── (raw evidence preserved across phases)
```

## How It Works

1. **After each phase**, the active agent writes a summary to `summaries/phase-{N}-{name}.md` using the template. This captures: files changed, decisions made, issues encountered, carried constraints, and inputs for the next phase.

2. **When resuming**, a returning agent reads `STATUS.md` + the latest phase summary to orient itself. This is faster and more reliable than scanning every file in the project.

3. **Snapshots** hold raw evidence (e.g., full QA reports, benchmark data) that summaries reference but don't inline. Load snapshots only when a summary flags them as relevant.

## Progressive Disclosure Pattern

Context loading should follow this order — stop as soon as you have enough:

1. `STATUS.md` + `BRIEF.md` (~2 files, ~1 min)
2. Latest `memory/summaries/phase-*.md` (~1 file, structured)
3. Specific files flagged by the summary (targeted reads)
4. Full directory scans (last resort)

See `operations/context-efficiency-guidelines.md` guideline #6 for details.

## Optional Complements

The built-in memory system is file-based and works everywhere. These tools can enhance it:

### claude-mem (Claude Code users)
[github.com/thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) — A Claude Code plugin that automatically captures session observations, compresses them with AI, and injects relevant context at the start of future sessions. Complements our phase summaries with granular session-level memory (what was tried, what failed, what approaches worked).

Install: `/plugin marketplace add thedotmack/claude-mem` then `/plugin install claude-mem` inside Claude Code.

### qmd (any IDE with MCP support)
[github.com/tobi/qmd](https://github.com/tobi/qmd) — Local semantic search engine for markdown files. Index your project's specs, decisions, memory summaries, and handoffs, then search them with natural language via MCP or CLI. Useful once a project accumulates enough context that grep isn't enough.

Install: `npm install -g @tobilu/qmd`, then `qmd collection add . --name myproject && qmd embed`.
