# Operations Board

Use this board as a simple kanban layer for orchestrator visibility.

## Rules
- Keep cards short and action-oriented.
- One owner per card.
- Move cards only when acceptance criteria are met.
- Link each card to concrete file paths.
- Include dependencies and file-scope to avoid duplicate/overlapping work.
- For implementation tasks, assign isolated branch/worktree.

## Backlog
- [ ] [CARD-001] Define project brief and constraints  
  - Owner: Product Manager  
  - Priority: P1  
  - Phase: requirements  
  - Dependencies: none  
  - File Scope: `BRIEF.md`  
  - Branch/Worktree: n/a  
  - Links: `BRIEF.md`  
  - Acceptance: brief complete and approved

## Unassigned (Ready Queue)
- [ ] [CARD-002] Draft requirements  
  - Owner: Product Manager  
  - Priority: P1  
  - Phase: requirements  
  - Dependencies: CARD-001  
  - File Scope: `specs/requirements.md`  
  - Branch/Worktree: n/a  
  - Links: `specs/requirements.md`, `handoffs/product-to-design.md`  
  - Acceptance: FRs + ACs + edge cases + out-of-scope complete

## Assigned
- [ ] [CARD-005] Implement auth endpoint
  - Owner: Fullstack Engineer
  - Priority: P1
  - Phase: implementation
  - Dependencies: design gate PASS
  - File Scope: `src/api/auth/*`, `tests/auth/*`
  - Branch/Worktree: `agent/fullstack/CARD-005-auth-endpoint`
  - Links: `specs/architecture.md`
  - Acceptance: endpoint + tests + handoff note complete

## In Progress
- [ ] [CARD-006] Implement login form flow
  - Owner: Frontend Engineer
  - Priority: P1
  - Phase: implementation
  - Dependencies: CARD-005
  - File Scope: `src/ui/login/*`, `tests/ui/login/*`
  - Branch/Worktree: `agent/frontend/CARD-006-login-flow`
  - Links: `specs/ui-spec.md`
  - Acceptance: UI states + integration + tests complete

## Review
- [ ] [CARD-003] Review design package  
  - Owner: Orchestrator  
  - Phase: design  
  - Links: `specs/ui-spec.md`, `specs/architecture.md`  
  - Acceptance: phase gate result PASS + human approval

## Blocked
- [ ] [CARD-004] API contract mismatch  
  - Owner: Fullstack Engineer  
  - Phase: implementation  
  - Links: `specs/architecture.md`, `handoffs/engineering-to-qa.md`  
  - Blocker: unresolved response schema mismatch

## Awaiting Merge
- [ ] [CARD-007] Ready for merge steward checks
  - Owner: Orchestrator
  - Phase: implementation
  - Dependencies: tests pass + gate PASS
  - Branch/Worktree: `agent/fullstack/CARD-005-auth-endpoint`
  - Links: `handoffs/engineering-to-qa.md`
  - Acceptance: merge approved or fix task created

## Done
- [x] [CARD-000] Harness setup complete  
  - Owner: Setup Engineer  
  - Links: `profiles/merged-profile.yaml`, `harness/generated-agents/`

## Parking Lot
- Nice-to-have items not in current scope.
