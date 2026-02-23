# Routing, Retry, and Escalation Policy

## Scheduling
- Default flow is phase-based and sequential.
- Parallelism is allowed only inside implementation and bounded by `merged-profile.workflow_policy.max_parallel_tasks`.
- Orchestrator must checkpoint `STATUS.md` before and after each phase transition.
- Use ready-queue dispatch: only tasks that are unblocked, scoped, and unassigned can be claimed.
- Optional Growth Strategist has two touchpoints: (1) growth requirements input during the requirements phase, and (2) growth execution plan after QA. See `harness/agents/growth-strategist.md`.

## Ready-Task Dispatch
- A task is **Ready** only if:
  - Dependencies are complete.
  - Acceptance criteria are defined.
  - Owner role is assigned.
  - Required input files are listed.
- Queue priority order: P0 > P1 > P2, then oldest-first within same priority.
- Do not dispatch duplicate tasks for overlapping file scopes.

## Worktree and Branch Isolation
- For parallel implementation tasks, use isolated branches/worktrees per task.
- Naming convention:
  - Branch: `agent/<role>/<task-id>-<slug>`
  - Optional worktree directory: `worktrees/<task-id>-<slug>`
- One task, one isolated branch, one owner.
- Merge to main branch only after gate pass + review.

## Retry Policy
- Retry only transient failures (tool/network/timeouts).
- Max retries per task are read from merged profile.
- Quality failures are not auto-retried. The next attempt must include explicit corrective feedback.

## Timeout Policy
- Soft timeout: request partial output and write checkpoint handoff.
- Hard timeout: cancel task and escalate to orchestrator.

## Escalation Policy
- Critical blocker: escalate to human immediately.
- Major ambiguity: escalate within one orchestrator cycle.
- Minor ambiguity: proceed with explicit assumption, then log in `DECISIONS.md`.

## Gate Enforcement
- No phase transition without gate criteria satisfied.
- Emergency override requires human approval and explicit log entry.

## Merge Steward Pattern
- Treat merge/review as an explicit step, not an implicit side effect.
- Before merge:
  - Relevant tests pass.
  - Gate criteria pass.
  - Handoff notes are complete.
- On merge failure:
  - Create a fix task linked to the failed merge candidate.
  - Return task to queue with concrete failure evidence.

## Context Efficiency
- Follow `operations/context-efficiency-guidelines.md`.
- Keep context phase-scoped; load only necessary artifacts.
- Prefer summaries/handoffs over replaying full history.
- On failures, rerun only the failing slice with targeted feedback.
