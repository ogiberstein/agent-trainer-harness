# Memory Policies

## Write Ownership
- `specs/requirements.md`: Product Manager
- `specs/ui-spec.md`, `specs/architecture.md`: Designer
- `qa/*`: QA Engineer
- `docs/*`: Documentation Writer
- `STATUS.md`, `DECISIONS.md`: Orchestrator

## Locking
- Writers create logical locks in `memory/index.json`.
- Locks should include owner, path, started_at, ttl_seconds.
- Orchestrator may break stale locks and must log reason.

## Freshness
- Artifacts older than the latest phase transition are considered stale until revalidated.
- At each phase gate, orchestrator requires a summary refresh.

## Compaction
- Every 10 handoffs, create a phase summary in `memory/summaries/`.
- Preserve raw evidence in `memory/snapshots/`.

## Retention
- Keep active run records for configured retention window, then archive.
