# Operations Tracker

Single file for task board, project dashboard, workflow state, and escalation inbox.

---

## Board

### Rules
- Keep cards short and action-oriented.
- One owner per card.
- Move cards only when acceptance criteria are met.
- Link each card to concrete file paths.
- Include dependencies and file-scope to avoid duplicate/overlapping work.
- For implementation tasks, assign isolated branch/worktree.

### Card Format

```
- [ ] [CARD-XXX] Short title
  - Owner: [role]
  - Priority: P0 | P1 | P2
  - Phase: [phase]
  - Dependencies: [card IDs or "none"]
  - File Scope: [paths this card touches]
  - Branch/Worktree: [branch name or "n/a"]
  - Acceptance: [criteria for completion]
```

### Backlog
<!-- Add cards here when work is identified but not yet ready for assignment -->

### Ready Queue
<!-- Cards here are unblocked, scoped, and ready for a worker to claim -->

### In Progress
<!-- Active work — one owner per card, one branch per implementation card -->

### Review
<!-- Awaiting orchestrator or human gate review -->

### Blocked
<!-- Include blocker details and escalation target for every card here -->

### Awaiting Merge
<!-- Merge steward checks required: tests pass + gate PASS + handoff complete -->

### Done
<!-- Completed and verified cards -->

### Parking Lot
<!-- Nice-to-have items not in current scope -->

---

## Dashboard

### Project Snapshot
- Project: <!-- name -->
- Mode: lite | full
- Current phase: <!-- requirements | design | implementation | qa | documentation | growth | review | complete -->
- Last updated: YYYY-MM-DD by <!-- role -->

### Gate Status
| Phase | Status | Owner | Last Check | Notes |
|---|---|---|---|---|
| Requirements | Pending | Product Manager |  |  |
| Design | Pending | Designer |  |  |
| Implementation | Pending | Engineering |  |  |
| QA | Pending | QA Engineer |  |  |
| Documentation | Pending | Documentation Writer |  |  |
| Growth (optional) | Pending | Growth Strategist |  |  |
| Final Review | Pending | Orchestrator |  |  |

### Top Priorities
1. <!-- priority -->
2. <!-- priority -->
3. <!-- priority -->

### Active Risks
| ID | Risk | Impact | Mitigation | Owner | Status |
|---|---|---|---|---|---|
<!-- Add risks as identified -->

### Blockers
| ID | Blocker | Blocking Phase | Owner | Escalation Needed | Status |
|---|---|---|---|---|---|
<!-- Add blockers as identified -->

### Quality and Reliability
- Open QA issues: Critical [0], Major [0], Minor [0], Cosmetic [0]
- Rework loops this run: [0]
- Latest gate failures: [none]
- Regression checks: Pass/Fail

### Cost and Efficiency
- Estimated run cost to date: <!-- $ -->
- Optional skills currently active: <!-- from profiles/active-skills.yaml -->

---

## Workflow State

Use this section to make multi-step workflows resumable.

### Active Workflow
- Workflow ID: WF-001
- Name: <!-- feature or initiative name -->
- Status: running | blocked | completed
- Current step: <!-- step-id -->
- Last checkpoint: YYYY-MM-DD HH:MM UTC
- Owner: <!-- role -->

### Steps
| Step ID | Description | Owner | Status | Evidence | Next Action |
|---|---|---|---|---|---|
| STEP-001 | <!-- description --> | <!-- role --> | pending | | |

### Resume Rules
- Resume from the first non-completed step.
- Do not repeat completed steps unless dependencies changed.
- If a step fails, append failure evidence and spawn a linked fix step.

---

## Inbox

Use this section for concise escalations and cross-role communication.

### Open
<!-- [INBOX-XXX] **Title** — From: role, To: role, Related: file, Requested action, Status: open -->

### In Triage
<!-- [INBOX-XXX] **Title** — From: role, To: role, Related: file, Requested action, Status: triage -->

### Resolved
<!-- [INBOX-XXX] **Title** — Status: resolved -->
