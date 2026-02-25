# Lite Mode — Existing Project Onboarding

## Quick Start

1. Read `AGENTS.md` — operating rules and file zones.
2. Read `BRIEF.md` — project scope (fill in if empty).
3. Audit the existing project (Step 1 below) — understand what exists before adding anything.
4. Add at minimum: `STATUS.md`, `DECISIONS.md`, `memory/summaries/`.

Everything below is the detailed onboarding flow. Load on-demand.

---

## What This Harness Provides

Before auditing the project, understand what lite mode offers and why:

- **Phase-gated delivery**: Requirements -> Implementation -> QA -> Review. Prevents shipping untested work. (phases defined in this file)
- **3 specialist checklists**: Orchestrator, Fullstack Engineer, QA Engineer. Each has defined inputs/outputs, acceptance criteria, and escalation rules — usable as checklists even in single-agent mode. (role definitions in `harness/agents/`)
- **Structured requirements**: Table-based template for testable FRs with acceptance criteria. Prevents vague specs. (`specs/requirements.md`)
- **Quality tracking**: Standardized issue format with severity, reproduction steps, and ship recommendations. (`qa/issues.md`)
- **Decision log**: Traceable record of non-trivial trade-offs. Prevents "why did we do this?" confusion. (`DECISIONS.md`)
- **Context efficiency**: Guidelines to keep agent runs lean and focused. (`operations/context-efficiency-guidelines.md`)
- **Memory layer**: Phase summaries that survive session boundaries. (`memory/`)

You do NOT need to activate all of this. The audit below determines what adds value.

---

## Step 1 — Audit the Existing Project

Scan the repository and answer these questions:

| Harness Capability | Project Has? | Quality | Notes |
|---|---|---|---|
| README / project description | yes / no / partial | good / needs work | |
| Requirements or spec doc | yes / no / partial | good / needs work | |
| Test suite | yes / no / partial | good / needs work | |
| Issue tracking | yes / no / partial | good / needs work | |
| Decision log | yes / no / partial | good / needs work | |
| CI/CD or build process | yes / no / partial | good / needs work | |

Record this table in `DECISIONS.md` as DEC-001: "Harness onboarding audit."

## Step 2 — Classify the Project

Based on the audit:

- **Well-structured**: Has good docs, tests, and clear processes. -> Light-touch: add only `STATUS.md` and `DECISIONS.md` for cross-session tracking. Align existing docs to harness format only if it improves clarity.
- **Partial**: Has some structure but gaps. -> Fill gaps: add harness files for missing capabilities only. Preserve and align what exists.
- **Bare**: Minimal docs, no tests, no process. -> Full adoption: activate all lite harness files.

## Step 3 — Preserve What Works

Rules:
- Never overwrite a good existing README, spec, or test suite.
- If the project has requirements in a different format, align them in-place rather than replacing.
- If the project has its own issue tracking, keep it. Use `qa/issues.md` only if nothing exists.

## Step 4 — Introduce What Helps

Based on classification, selectively activate:
- `BRIEF.md` — fill in if no project description exists, or skip if README covers it.
- `STATUS.md` — always useful for cross-session tracking.
- `DECISIONS.md` — always useful for traceability.
- `specs/requirements.md` — only if no existing spec or if existing spec lacks acceptance criteria.
- `qa/issues.md` — only if no existing issue tracking.
- `harness/agents/` — read for role guidance, but don't force role separation in solo work.
- `operations/context-efficiency-guidelines.md` — always useful, no project impact.

For files you're not activating, you may delete them from the project and log the reason in `DECISIONS.md`.

## Step 5 — Validate

Run one lightweight cycle through the harness:
1. Confirm `STATUS.md` reflects the project's actual current state.
2. Verify at least one requirement has acceptance criteria.
3. Confirm the agent can find and reference the right files.

---

## Graduation Path

### Lite -> Full
When the project outgrows lite mode (scope expansion, multiple roles, need for handoffs and formal gates):
1. Copy the `full/existing-project/` folder from the harness repo.
2. Run that folder's `start.md` — it will audit what you already have and add what's missing.
3. Key additions: gate log in STATUS.md, handoff templates, evaluation criteria, full role library, skills library.

### Lite -> Concurrent
For autonomous parallel execution:
1. First upgrade to Full (above).
2. Then copy `concurrent/existing-project/` and follow its `start.md` to add runtime/ and cli/.

---

## Framework Shim (Optional)

If your AI IDE uses a global config file, add a pointer to the harness:

**Claude Code (~/.claude/CLAUDE.md):** Add: "If AGENTS.md exists in the project root, read it first and follow harness instructions."

**Cursor (.cursorrules):** Add: "Check for AGENTS.md in project root. If present, follow harness workflow."

**GitHub Copilot (.github/copilot-instructions.md):** Add: "If AGENTS.md exists, treat it as the primary operating instructions."
