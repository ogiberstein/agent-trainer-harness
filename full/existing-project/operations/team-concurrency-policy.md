# Team Concurrency Policy

Use this policy when multiple humans or agents operate on the same project.

## Goals
- Prevent duplicate work and merge conflicts.
- Preserve context continuity across handoffs.
- Keep ownership and escalation paths explicit.

## Rules
1. One active owner per task card.
2. One active branch/worktree per implementation task.
3. No overlapping file scope across concurrent In Progress tasks unless explicitly approved.
4. Every blocked task must include blocker details and escalation target.
5. Merge steward checks are required before integration to main branch.

## Assignment Protocol
- Pull work only from tasks listed in `STATUS.md`.
- A task is assignable only if dependencies are complete and acceptance criteria are defined.
- Track task state in `STATUS.md`: Ready -> In Progress -> Awaiting Merge -> Done.

## Conflict Resolution
- If overlap detected, orchestrator pauses one task and re-scopes both cards.
- If duplicate work started, keep the version with better evidence and convert the other into a fix/refactor card.
- Log decisions in `DECISIONS.md`.

## Minimum Artifacts per Task
- Task entry in `STATUS.md`
- Handoff or implementation note in relevant `handoffs/` file
