# Future Improvements

Roadmap for the next evolution of the harness.

## Recently Shipped

- **Mode selection heuristic** — concrete decision tree in `AGENTS.md` replaces vague "smallest valid workflow" guidance.
- **Mandatory phase snapshots** — `memory/summaries/TEMPLATE.md` and enforcement rules in `AGENTS.md` + `start.md`. Protects against context compaction.
- **Structural gate enforcement** — Gate Log table in `STATUS.md`, violation rules in `AGENTS.md`, gate logging at every phase in `start.md`.
- **CLAUDE.md hard triggers** — Three conditional triggers (tracker override, snapshot mandate, gate check mandate) fire automatically when `AGENTS.md` is detected.
- **Engineer deviation logging** — Fullstack and Frontend engineer checklists now require `DECISIONS.md` entries for spec deviations.
- **Concurrent self-launch** — `cli/preflight_concurrent.py` checks prerequisites; `launch-concurrent` CLI subcommand starts the orchestrator as a background process. Agents can self-launch concurrent mode or fall back to Full mode.

## Near Term

### Battle-test Concurrent mode
- Run Concurrent mode end-to-end on a real project.
- Harden `state.py` round-trip parsing under edge cases (malformed cards, empty sections, concurrent writes).
- Validate worker <-> Claude Code CLI integration across model versions.

### Wire remaining runbook commands to scripts
Six playbooks in `COMMANDS.md` are still manual: `/dispatch-ready`, `/merge-steward`, `/resume-workflow`, `/security-gate`, `/ops-sync`, `/retrospective`. Options:
- Add to `cli/harness_cli.py` as new subcommands.
- Expose as MCP tools so agents can invoke them natively.

## Next

### Observability dashboard
- Build on `logs/runs.jsonl` telemetry (already captured by the orchestrator).
- Visualise: cost per run, gate pass/fail rates, rework loops, phase duration, worker utilisation.
- Could be a simple static HTML report generator or a lightweight web dashboard.

### Claude Code Agent Teams migration
Claude Code now ships an experimental [Agent Teams](https://code.claude.com/docs/en/agent-teams) feature — native multi-agent coordination with shared task lists, inter-agent messaging, and `TaskCompleted` hooks. This is essentially the runtime layer we built manually in `runtime/`.

**Migration path:**
- Team lead reads our `AGENTS.md` as its operating instructions and assigns teammates using `harness/agents/*.md` role prompts.
- `TaskCompleted` hooks replace `gates.py` — wire them to our gate criteria in `evaluation/release-gates.md`.
- Native shared task list could replace the task-tracking section of `STATUS.md`.
- Inter-agent messaging enables teammate collaboration (something our isolated workers can't do today).
- `STATUS.md`, `DECISIONS.md`, `memory/summaries/`, phase gates, and the full delivery methodology stay unchanged.

**What we'd drop:** `runtime/` entirely — `orchestrator.py`, `worker.py`, `merge.py`, `state.py`, `gates.py`, `notifier.py`, `config.yaml`, `run.py`. Also `cli/preflight_concurrent.py` and the `launch-concurrent` CLI subcommand.

**What we'd keep:** Everything that defines *what to build and how to check it* — AGENTS.md, STATUS.md, BRIEF.md, DECISIONS.md, phase gates, role prompts, memory, skills, evaluation criteria, handoffs.

**Blockers (as of Feb 2026):**
- Agent Teams is still experimental and disabled by default.
- No session resumption — teammates lost on restart (our checkpoint/resume is more reliable for overnight runs).
- No git worktree isolation — file conflicts are the user's problem. Our worktree model is architecturally safer.
- One team per session, no nested teams.

**Recommendation:** Monitor Agent Teams maturity. When session resumption and file isolation are solved, migrate. Until then, our custom runtime is more reliable for autonomous overnight builds.

### LangGraph upgrade path (alternative)
- Replace the Python loop orchestrator with a LangGraph StateGraph for built-in persistence, declarative retry logic, and visual execution traces in LangSmith.
- Keep file-first governance; LangGraph manages dispatch, not policy.
- This becomes the fallback path if Claude Code Agent Teams doesn't mature as expected.

### Memory and search enhancements
- **Auto-summarization via claude-mem hooks**: Explore using claude-mem's `PostToolUse` and `SessionEnd` hooks to automatically generate phase summaries from session observations, reducing reliance on agents manually writing to `memory/summaries/`.
- **Native qmd bootstrap**: Add an optional step in `start.md` that indexes the project's harness files as a qmd collection (`qmd collection add . --name project && qmd embed`), giving agents semantic search over accumulated specs, decisions, and summaries via MCP.
- **Progressive disclosure in AGENTS.md**: Extend the "First Actions" section to follow the progressive disclosure pattern more strictly — have agents read summaries before any source files.

## Later

### Remote control interface (Telegram / Slack)
- Use something like [Takopi](https://github.com/banteg/takopi) or a custom bot to send commands and receive notifications from the orchestrator on mobile.
- Keep command whitelist and file-first governance.

### Stoneforge-style platform layer
- Adopt a heavier orchestration platform (dispatch daemon, event-sourced state, web dashboard, persistent messaging) for teams running multiple concurrent projects.
- The harness stays as the policy/governance layer on top.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Added runtime complexity too early | Keep file-first governance; adopt in staged rollout |
| Parallel edits cause merge conflicts | Enforce branch/worktree isolation and file-scope ownership |
| Lower quality due to speed bias | Preserve gate checks and security/review steps |
