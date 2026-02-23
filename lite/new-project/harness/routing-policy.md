# Routing, Retry, and Escalation Policy

## Scheduling
- Default flow is phase-based and sequential.
- Orchestrator must checkpoint `STATUS.md` before and after each phase transition.

## Retry Policy
- Retry only transient failures (tool/network/timeouts).
- Quality failures are not auto-retried. The next attempt must include explicit corrective feedback.

## Escalation Policy
- Critical blocker: escalate to human immediately.
- Major ambiguity: escalate within one orchestrator cycle.
- Minor ambiguity: proceed with explicit assumption, then log in `DECISIONS.md`.

## Gate Enforcement
- No phase transition without gate criteria satisfied.
- Emergency override requires human approval and explicit log entry.

## Context Efficiency
- Follow `operations/context-efficiency-guidelines.md`.
- Keep context phase-scoped; load only necessary artifacts.
- Prefer summaries over replaying full history.
