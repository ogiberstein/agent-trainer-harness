# Memory Policies

## Write Ownership
- `specs/requirements.md`: Product Manager
- `specs/ui-spec.md`, `specs/architecture.md`: Designer
- `qa/*`: QA Engineer
- `docs/*`: Documentation Writer
- `STATUS.md`, `DECISIONS.md`: Orchestrator

Ownership is advisory — any agent may write to any file if the owning role is inactive or the project is single-agent. Log deviations in `DECISIONS.md`.

## Freshness
- Artifacts older than the latest phase transition are considered stale until revalidated.
- At each phase gate, the active agent should refresh or confirm the phase summary in `memory/summaries/`.

## Phase Summaries
- After completing each phase, write a summary to `memory/summaries/phase-{N}-{name}.md` using the TEMPLATE.
- Summaries are the primary context restoration mechanism for returning agents.
- Load summaries first; load full source files only when the summary indicates they're relevant.
