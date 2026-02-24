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

### Claude Code Agent Teams as Concurrent runtime
Claude Code's experimental [Agent Teams](https://code.claude.com/docs/en/agent-teams) feature provides native multi-agent coordination — shared task lists, inter-agent messaging, and quality hooks. When it matures, it could replace Concurrent mode's custom Python `runtime/` while keeping the harness methodology (AGENTS.md, phases, gates, roles, memory) intact. See `concurrent/*/FUTURE_IMPROVEMENTS.md` for the full migration plan.

### LangGraph upgrade path (alternative)
- Replace the Python loop orchestrator with a LangGraph StateGraph for built-in persistence, declarative retry logic, and visual execution traces in LangSmith.
- Keep file-first governance; LangGraph manages dispatch, not policy.

### Memory and search enhancements
- **Auto-summarization via claude-mem hooks**: Explore using claude-mem's session hooks to auto-generate phase summaries, reducing reliance on agents manually writing to `memory/summaries/`.
- **Native qmd bootstrap**: Add an optional step in `start.md` to index the project's harness files as a qmd collection for semantic search via MCP.
- **Progressive disclosure in AGENTS.md**: Extend "First Actions" to follow the progressive disclosure pattern more strictly.

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
