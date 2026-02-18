# Harness Commands (Pseudo-Slash)

Use these command aliases as repeatable runbooks in manual orchestration mode.

## Core Lifecycle

### `/research-opportunity`
Purpose: Run optional market/domain opportunity research before scope lock.

Runs:
1. Activate `market-opportunity-research` skill.
2. Produce `specs/market-research.md`.
3. Select top opportunity and log rationale in `DECISIONS.md`.
4. Carry chosen scope into `specs/requirements.md`.

Primary files:
- `BRIEF.md`
- `specs/market-research.md`
- `specs/requirements.md`
- `DECISIONS.md`

### `/research-users`
Purpose: Run optional user discovery (interview + online desk research) before requirements lock.

Runs:
1. Activate `user-research-discovery` skill.
2. Capture interview findings + desk research in `specs/user-research.md`.
3. Update `specs/requirements.md` with evidence-backed refinements.
4. Log major scope/priority shifts in `DECISIONS.md`.

Primary files:
- `BRIEF.md`
- `specs/user-research.md`
- `specs/requirements.md`
- `DECISIONS.md`

### `/harness-start`
Purpose: Start a new project run with full setup.

Runs:
1. Validate `BRIEF.md` and profiles.
2. Run Setup Engineer flow.
3. Generate `profiles/merged-profile.yaml` and `harness/generated-agents/*`.
4. Initialize `STATUS.md` to requirements.

Primary files:
- `Day 0 Start with this Prompt.md`
- `profiles/project-profile.yaml`
- `profiles/active-skills.yaml`
- `STATUS.md`

### `/harness-start-lite`
Purpose: Start a small project with minimal overhead.

Runs:
1. Apply lite skill preset.
2. Skip optional roles.
3. Use shortened phase flow (requirements -> implementation -> QA -> review).

Primary files:
- `Lite Mode Start Checklist.md`
- `profiles/active-skills.lite.yaml`
- `STATUS.md`

### `/phase-next`
Purpose: Advance exactly one phase with gate enforcement.

Runs:
1. Read current phase from `STATUS.md`.
2. Execute only the next role prompt.
3. Check gate criteria.
4. Update `STATUS.md` and `DECISIONS.md`.

Primary files:
- `STATUS.md`
- `DECISIONS.md`
- `harness/generated-agents/*.md`

### `/gate-check`
Purpose: Run gate review without doing implementation work.

Runs:
1. Validate required artifacts for current phase.
2. Return PASS/FAIL with missing items.
3. Record outcome and next action.

Primary files:
- `STATUS.md`
- `operations/dashboard.md`
- Phase-specific artifacts in `specs/`, `qa/`, `docs/`

## Task and Execution Operations

### `/dispatch-ready`
Purpose: Assign only ready tasks from board queue.

Runs:
1. Read `operations/board.md` Ready Queue.
2. Confirm dependencies, owner, file scope, and acceptance criteria.
3. Move selected tasks to Assigned/In Progress.

Primary files:
- `operations/board.md`
- `harness/routing-policy.md`

### `/merge-steward`
Purpose: Process awaiting-merge tasks with test and gate evidence.

Runs:
1. Read Awaiting Merge items.
2. Verify tests and gate evidence.
3. Approve merge or create linked fix task with evidence.

Primary files:
- `operations/board.md`
- `operations/runbook.md`
- `evaluation/release-gates.md`

### `/resume-workflow`
Purpose: Resume from the first incomplete workflow step.

Runs:
1. Read `operations/workflow-state.md`.
2. Identify first non-completed step.
3. Continue from checkpoint only.

Primary files:
- `operations/workflow-state.md`
- `operations/inbox.md`

## Review and Hardening

### `/security-gate`
Purpose: Execute security gate before release for high-risk changes.

Runs:
1. Run security audit skill/process.
2. Validate no unresolved critical/high findings.
3. Record decision in release gates.

Primary files:
- `evaluation/release-gates.md`
- `skills/security-audit-adversarial-testing/SKILL.md`
- `DECISIONS.md`

### `/ops-sync`
Purpose: Keep board, dashboard, and status consistent.

Runs:
1. Update board states.
2. Refresh dashboard metrics.
3. Ensure status and decisions align with latest phase.

Primary files:
- `operations/board.md`
- `operations/dashboard.md`
- `STATUS.md`
- `DECISIONS.md`
