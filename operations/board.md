# Operations Board

Use this board as a simple kanban layer for orchestrator visibility.

## Rules
- Keep cards short and action-oriented.
- One owner per card.
- Move cards only when acceptance criteria are met.
- Link each card to concrete file paths.
- Include dependencies and file-scope to avoid duplicate/overlapping work.
- For implementation tasks, assign isolated branch/worktree.

## Card Format

```
- [ ] [CARD-XXX] Short title
  - Owner: [role]
  - Priority: P0 | P1 | P2
  - Phase: [phase]
  - Dependencies: [card IDs or "none"]
  - File Scope: [paths this card touches]
  - Branch/Worktree: [branch name or "n/a"]
  - Links: [related spec/handoff files]
  - Acceptance: [criteria for completion]
```

## Backlog
<!-- Add cards here when work is identified but not yet ready for assignment -->

## Unassigned (Ready Queue)
<!-- Cards here are unblocked, scoped, and ready for a worker to claim -->

## Assigned
<!-- Cards that have an owner but work has not started -->

## In Progress
<!-- Active work — one owner per card, one branch per implementation card -->

## Review
<!-- Awaiting orchestrator or human gate review -->

## Blocked
<!-- Include blocker details and escalation target for every card here -->

## Awaiting Merge
<!-- Merge steward checks required: tests pass + gate PASS + handoff complete -->

## Done
<!-- Completed and verified cards -->

## Parking Lot
<!-- Nice-to-have items not in current scope -->
