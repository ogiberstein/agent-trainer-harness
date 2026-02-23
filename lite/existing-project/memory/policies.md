# Memory Policies

## Write Ownership
- `specs/requirements.md`: Orchestrator (wearing PM hat in lite mode)
- `qa/*`: QA Engineer
- `STATUS.md`, `DECISIONS.md`: Orchestrator

## Freshness
- Artifacts older than the latest phase transition are considered stale until revalidated.

## Compaction
- After completing each phase, write a summary to `memory/summaries/`.
- Load summaries by default; load full context only when deeper investigation is needed.
