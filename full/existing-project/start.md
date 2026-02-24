# Full Mode — Existing Project Onboarding

Use this when integrating the full harness into an existing codebase, or upgrading from lite mode to full structured delivery.

## What This Harness Provides

Before auditing the project, understand what full mode offers and why each piece exists:

- **Phase-gated delivery**: Requirements -> Design -> Implementation -> QA -> Docs -> Growth -> Review. Each phase has explicit gate criteria that must pass before advancing. Prevents shipping half-baked work. (gate criteria in `evaluation/release-gates.md`)
- **10 specialist roles**: Orchestrator, PM, Designer, Fullstack Engineer, Frontend Engineer, QA, Docs Writer, Growth Strategist, Domain SME, Setup Engineer. Each has defined inputs, outputs, acceptance checklists, and escalation rules. (`harness/agents/`)
- **Structured handoffs**: Contracts for context transfer between roles. Prevents "lost in translation" at role boundaries. (`handoffs/`)
- **Quality tracking**: Scorecard, regression tracking, golden tasks for benchmarking. (`evaluation/`)
- **Skills library**: 17 reusable skills for requirements clarification, security auditing, analytics instrumentation, blockchain exploration, and more. (`skills/`)
- **Operational policies**: Context efficiency guidelines, incident runbook, concurrency rules, changelog. (`operations/`)
- **Memory layer**: Phase summaries with carried constraints, decision log, project state. Survives session boundaries. (`memory/`, `STATUS.md`, `DECISIONS.md`)
- **Runbook playbooks**: Repeatable commands for common actions. (`COMMANDS.md`)
- **Validation CLI**: Mechanical consistency checker. (`python3 cli/validate_harness.py` — available in concurrent mode)

You do NOT need to activate all of this. The audit below determines what adds value for this project.

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

Record this table in `DECISIONS.md` as DEC-001: "Harness onboarding audit."

## Step 2 — Classify the Project

Based on the audit:

- **Well-structured**: Has good docs, tests, specs, and clear processes.
  -> **Light-touch**: Add `STATUS.md`, `DECISIONS.md`, and `memory/` for cross-session tracking. Align existing docs to harness format only where it improves clarity. Add gate log to STATUS.md.

- **Partial**: Has some structure but notable gaps.
  -> **Fill gaps**: Add harness files that address actual gaps. Preserve and align what exists. Focus on the weakest areas first (e.g., if no test plan, add `qa/`; if no specs, add `specs/`).

- **Bare**: Minimal docs, no tests, no process.
  -> **Full adoption**: Activate all harness files. Follow the new-project `start.md` for the full setup flow.

## Step 3 — Preserve What Works

Rules:
- Never overwrite a good existing README, spec, test suite, or architecture doc.
- If the project has requirements in a different format, align them in-place rather than replacing with the harness template.
- If the project has its own issue tracking, keep it. Use `qa/issues.md` only if nothing exists.
- If the project has its own CI/quality process, keep it and map gate criteria to the existing process.

## Step 4 — Introduce What Helps

Based on classification, selectively activate. Priority order:

**Always useful (add for any classification):**
- `STATUS.md` with Gate Log — cross-session tracking and gate enforcement
- `DECISIONS.md` — traceability
- `memory/summaries/TEMPLATE.md` — phase snapshots for context preservation
- `operations/context-efficiency-guidelines.md` — token discipline

**Add if gaps found:**
- `specs/requirements.md` — if no existing spec or spec lacks acceptance criteria
- `specs/architecture.md` — if no architecture documentation
- `qa/` templates — if no QA process
- `harness/agents/` — role definitions for multi-agent work
- `handoffs/` — if multiple roles are active and context gets lost at transitions
- `evaluation/` — if no quality gates or release criteria exist
- `skills/` — activate only skills relevant to this project's domain

**Usually not needed for existing projects:**
- `harness/generated-agents/` — only if running the full Setup Engineer workflow
- `profiles/org-profile.yaml` — only if customizing agent behavior
- `COMMANDS.md` — only if using runbook playbooks

For files you're not activating, delete them and log the reason in `DECISIONS.md`.

## Step 5 — Validate

Run one cycle through the harness to confirm value:
1. Set `STATUS.md` to reflect the project's actual current phase.
2. Verify at least one requirement has acceptance criteria.
3. Record a gate result in the STATUS.md Gate Log for the current phase.
4. Write a phase summary to `memory/summaries/` to test the snapshot flow.
5. Confirm the agent can navigate between harness files without confusion.

---

## Graduation Path

### From Lite
If you're upgrading from lite mode, the main additions are:
- Gate Log table in `STATUS.md`
- `handoffs/` directory with role-transition contracts
- Full role library in `harness/agents/` (10 roles vs. lite's 3)
- `evaluation/` directory (release gates, scorecard, regressions)
- Full `skills/` library (17 skills vs. lite's 2)
- `COMMANDS.md` for runbook playbooks
- Design and Documentation phases added to the phase sequence

### To Concurrent
When the project needs autonomous parallel execution:
1. Copy `concurrent/existing-project/` from the harness repo.
2. Follow that folder's `start.md` to add `runtime/` and `cli/`.

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
