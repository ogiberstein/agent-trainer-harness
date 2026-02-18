# Operations Runbook

## Incident Types
- Routing failure
- Memory/context drift
- Quality gate bypass
- Tool outage
- Cost runaway
- Merge queue stall
- Orphaned worktree/branch

## Prevention Baseline
- Apply `operations/context-efficiency-guidelines.md` in normal operation to reduce drift, rework, and unnecessary context load.
- Apply `operations/team-concurrency-policy.md` when parallel tasks are active.
- Use command runbooks in `COMMANDS.md` for consistent operator behavior.

## Response Workflow
1. **Triage** - classify incident type and severity.
2. **Contain** - pause dispatch, preserve snapshots, disable risky tools.
3. **Diagnose** - replay handoffs + memory records.
4. **Recover** - roll back to last known-good version.
5. **Postmortem** - document root cause and add regression test.

## Merge Steward Recovery
- If merge queue stalls:
  - Validate gate evidence and test status for each awaiting-merge task.
  - Reassign merge owner if primary owner is unavailable.
  - Spawn fix task for any failed merge candidate with concrete evidence.
- If worktree/branch is orphaned:
  - Re-link orphaned branch to task card in `operations/board.md`.
  - Mark status as `Blocked` until ownership is reassigned.
  - Clean up stale worktrees only after branch state is preserved.

## Rollback Procedure
- Revert to previous `agents-vX.Y.Z`, `profile-vX.Y.Z`, `adapter-vX.Y.Z`.
- Re-run smoke golden task.
- Re-open dispatch only after orchestrator + human approval.
