# Memory Policies

## Write Ownership
- `specs/requirements.md`: Product Manager
- `specs/ui-spec.md`, `specs/architecture.md`: Designer
- `specs/growth-plan.md`: Growth Strategist
- `qa/*`: QA Engineer
- `docs/*`: Documentation Writer
- `STATUS.md`, `DECISIONS.md`: Orchestrator

## Locking

Writers create logical locks in `memory/index.json` before starting a write operation.

Lock record format:
```json
{
  "owner": "product-manager",
  "path": "specs/requirements.md",
  "started_at": "2026-02-18T10:00:00Z",
  "ttl_seconds": 1800,
  "reason": "Drafting FR-003 through FR-006"
}
```

Rules:
- Locks expire after `ttl_seconds`. Default TTL is 30 minutes.
- Orchestrator may break stale locks and must log the reason in `DECISIONS.md`.
- An agent must check for existing locks on a path before writing. If locked by another agent, wait or escalate.

## Freshness
- Artifacts older than the latest phase transition are considered stale until revalidated.
- At each phase gate, orchestrator requires a summary refresh.

## Compaction
- Every 10 handoffs (tracked via `meta.handoff_count_since_compaction`), create a phase summary in `memory/summaries/`.
- Reset the counter after compaction.
- Preserve raw evidence in `memory/snapshots/`.
- Load summaries by default; load full snapshots only when deeper investigation is needed.

## Retention
- Keep active run records for the configured retention window (`meta.retention_days`), then archive to snapshots.
- Archived records are read-only references, not active context.
