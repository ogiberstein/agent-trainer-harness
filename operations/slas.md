# SLA and Escalation Targets

## Escalation SLAs
- Critical blocker: immediate human escalation
- Major ambiguity: escalate within one orchestrator cycle
- Minor ambiguity: proceed with logged assumption and review later

## Operational Targets
- Orchestrator decision turnaround: <= 15 minutes (human-in-loop excluded)
- Task retry ceiling: as defined in merged profile
- Incident acknowledgement: <= 10 minutes
- Incident containment start: <= 20 minutes
- Ready-task assignment latency: <= 30 minutes for P1, <= 10 minutes for P0
- Merge steward first review latency: <= 30 minutes after task enters awaiting-merge
- Merge fix-task creation latency (on fail): <= 15 minutes after failed review

## Reporting
- Weekly quality/cost summary from scorecard and metrics.
