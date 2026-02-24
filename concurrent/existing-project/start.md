# Concurrent Mode — Existing Project Onboarding

Use this when adding autonomous parallel execution to an existing codebase, or upgrading from lite/full mode to concurrent.

## What This Harness Provides

Before auditing the project, understand what concurrent mode offers and why:

- **Phase-gated delivery**: Requirements -> Design -> Implementation -> QA -> Docs -> Growth -> Review. Each phase has explicit gate criteria enforced by an LLM judge. (`evaluation/release-gates.md`)
- **10 specialist roles**: Orchestrator, PM, Designer, Fullstack Engineer, Frontend Engineer, QA, Docs Writer, Growth Strategist, Domain SME, Setup Engineer. Each has defined inputs, outputs, and escalation rules. (`harness/agents/`)
- **Structured handoffs**: Contracts for context transfer between roles. Prevents context loss at boundaries. (`handoffs/`)
- **Quality tracking**: Scorecard, regression tracking, golden tasks. (`evaluation/`)
- **Skills library**: 17 reusable skills for requirements, security, analytics, blockchain, and more. (`skills/`)
- **Operational policies**: Context efficiency, incident runbook, concurrency rules, changelog. (`operations/`)
- **Memory layer**: Phase summaries with carried constraints, decision log. Survives session boundaries. (`memory/`, `STATUS.md`, `DECISIONS.md`)
- **Runbook playbooks**: Repeatable commands for common actions. (`COMMANDS.md`)
- **Python runtime orchestrator**: Dispatches multiple Claude Code workers in parallel via git worktrees. Enforces gates with LLM-based evaluation. (`runtime/`)
- **CLI tools**: Status, gate-check, phase-next, task management, preflight checks, and concurrent launcher. (`cli/`)
- **Run telemetry**: JSONL event logging for tracking performance, cost, and failures. (`logs/runs.jsonl`)
- **Webhook notifications**: Slack/Telegram/generic webhook for phase completions, gate results, and errors. (`runtime/config.yaml`)

You do NOT need to activate all of this. The audit below determines what adds value.

---

## Step 1 — Audit the Existing Project

Scan the repository structure, README, tests, docs, and CI. Answer these questions:

| Harness Capability | Project Has? | Quality | Action |
|---|---|---|---|
| Project description / README | yes / no / partial | good / needs work | |
| Requirements or spec doc | yes / no / partial | good / needs work | |
| Architecture documentation | yes / no / partial | good / needs work | |
| UI/design spec | yes / no / partial | good / needs work | |
| Test suite | yes / no / partial | good / needs work | |
| Issue tracking / QA process | yes / no / partial | good / needs work | |
| Decision log | yes / no / partial | good / needs work | |
| Handoff process between roles | yes / no / partial | good / needs work | |
| CI/CD or build process | yes / no / partial | good / needs work | |
| Release criteria / quality gates | yes / no / partial | good / needs work | |
| Git branching / worktree setup | yes / no / partial | good / needs work | |

Record this table in `DECISIONS.md` as DEC-001: "Harness onboarding audit."

## Step 2 — Classify the Project

Based on the audit:

- **Well-structured**: Has good docs, tests, specs, and clear processes.
  -> **Light-touch**: Add `STATUS.md`, `DECISIONS.md`, `memory/`, `runtime/`, and `cli/` for tracking and concurrent execution. Align existing docs only where it improves clarity.

- **Partial**: Has some structure but notable gaps.
  -> **Fill gaps**: Add harness files that address actual gaps. Preserve what exists. Add `runtime/` and `cli/`.

- **Bare**: Minimal docs, no tests, no process.
  -> **Full adoption**: Activate all harness files. Follow setup below, then launch.

## Step 3 — Preserve What Works

Rules:
- Never overwrite a good existing README, spec, test suite, or architecture doc.
- If the project has requirements in a different format, align them in-place.
- If the project has its own issue tracking, keep it.
- If the project has its own CI/quality process, keep it and map gate criteria to the existing process.

## Step 4 — Introduce What Helps

Based on classification, selectively activate. Priority order:

**Always needed for concurrent mode:**
- `STATUS.md` with Gate Log — the orchestrator reads and writes this
- `DECISIONS.md` — traceability
- `BRIEF.md` — workers read this to understand the project
- `runtime/` — the concurrent orchestrator and worker code
- `cli/` — preflight checks and harness CLI
- `runtime/config.yaml` — configure model, workers, webhook
- `memory/summaries/TEMPLATE.md` — phase snapshots

**Add if gaps found:**
- `specs/requirements.md` — if no existing spec
- `harness/agents/` — role definitions for workers
- `handoffs/` — if multiple roles active
- `evaluation/` — if no quality gates exist
- `operations/` — context efficiency and concurrency policy

For files you're not activating, delete them and log the reason in `DECISIONS.md`.

## Step 5 — Configure and Launch

1. Edit `runtime/config.yaml` — model, max workers, timeouts, webhook.
2. Install dependencies: `pip install -r runtime/requirements.txt`
3. Run preflight: `python3 cli/preflight_concurrent.py --project .`
4. Launch: `python3 cli/harness_cli.py --project . launch-concurrent`

Or if agent-driven: the agent reads AGENTS.md, runs preflight, and self-launches.

## Step 6 — Validate

After the first run completes or after first phase:
1. Check `STATUS.md` — does the gate log reflect actual work?
2. Check `logs/runs.jsonl` — are events being logged?
3. Check `memory/summaries/` — did phase snapshots get written?
4. Run `python3 cli/validate_harness.py --project .` for consistency check.

---

## Graduation Path

### From Lite
1. First add Full mode capabilities (gate log, handoffs, evaluation, full roles, skills).
2. Then add `runtime/` and `cli/`.
3. Configure `runtime/config.yaml` and run preflight.

### From Full
The project already has the harness structure. Just add:
1. `runtime/` — orchestrator, worker, gates, merge, config, etc.
2. `cli/` — harness_cli.py, validate_harness.py, preflight_concurrent.py
3. Configure `runtime/config.yaml` with model, workers, and webhook.
4. Run `python3 cli/preflight_concurrent.py --project .` to verify prerequisites.
5. Launch with `python3 cli/harness_cli.py --project . launch-concurrent`.

---

## Optional Memory and Search Tools

The harness's built-in memory (`memory/summaries/`, `STATUS.md`, `DECISIONS.md`) works everywhere with no extra dependencies. These tools can enhance it for multi-session projects:

- **[claude-mem](https://github.com/thedotmack/claude-mem)** (Claude Code only) — Automatically captures session observations, compresses them with AI, and injects relevant context at the start of future sessions. Install inside Claude Code: `/plugin marketplace add thedotmack/claude-mem` then `/plugin install claude-mem`.

- **[qmd](https://github.com/tobi/qmd)** (any IDE with MCP support) — Local semantic search engine for markdown. Index your project's specs, decisions, and summaries, then search with natural language. Install: `npm install -g @tobilu/qmd`, then `qmd collection add . --name myproject && qmd embed`.

See `memory/README.md` for how these complement the built-in system.

---

## Framework Shim (Optional)

If your AI IDE uses a global config file, add a pointer to the harness:

**Claude Code (~/.claude/CLAUDE.md):** Add: "If AGENTS.md exists in the project root, read it first and follow harness instructions."

**Cursor (.cursorrules):** Add: "Check for AGENTS.md in project root. If present, follow harness workflow."

**GitHub Copilot (.github/copilot-instructions.md):** Add: "If AGENTS.md exists, treat it as the primary operating instructions."
