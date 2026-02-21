# Harness Runbook Playbooks

These are **manual playbook descriptions**, not executable commands. Read the steps and execute them yourself (or paste to an agent). They exist for consistency and repeatability, not automation.

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
- `day-0-start.md`
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
- `lite-mode-checklist.md`
- `profiles/active-skills.lite.yaml`
- `STATUS.md`

### `/align-existing-project`
Purpose: Hand over an existing project to the harness team by aligning current docs/specs in place.

Runs:
1. Copy core harness files (`starter_kit_existing_projects/core/`).
2. Execute alignment prompt from `starter_kit_existing_projects/alignment/EXISTING_PROJECT_ALIGNMENT_PROMPT.md`.
3. Track progress via `starter_kit_existing_projects/alignment/EXISTING_PROJECT_ALIGNMENT_CHECKLIST.md`.

Primary files:
- `migration-checklist.md`
- `starter_kit_existing_projects/alignment/EXISTING_PROJECT_ALIGNMENT_PROMPT.md`
- `starter_kit_existing_projects/alignment/EXISTING_PROJECT_ALIGNMENT_CHECKLIST.md`
- `STATUS.md`
- `DECISIONS.md`

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
- `operations/tracker.md`
- Phase-specific artifacts in `specs/`, `qa/`, `docs/`

## Task and Execution Operations

### `/dispatch-ready`
Purpose: Assign only ready tasks from board queue.

Runs:
1. Read `operations/tracker.md` Ready Queue.
2. Confirm dependencies, owner, file scope, and acceptance criteria.
3. Move selected tasks to Assigned/In Progress.

Primary files:
- `operations/tracker.md`
- `harness/routing-policy.md`

### `/merge-steward`
Purpose: Process awaiting-merge tasks with test and gate evidence.

Runs:
1. Read Awaiting Merge items.
2. Verify tests and gate evidence.
3. Approve merge or create linked fix task with evidence.

Primary files:
- `operations/tracker.md`
- `operations/runbook.md`
- `evaluation/release-gates.md`

### `/resume-workflow`
Purpose: Resume from the first incomplete workflow step.

Runs:
1. Read `operations/tracker.md` Workflow State section.
2. Identify first non-completed step.
3. Continue from checkpoint only.

Primary files:
- `operations/tracker.md`

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
- `operations/tracker.md`
- `STATUS.md`
- `DECISIONS.md`

## Concurrent Mode

### `/run-concurrent`
Purpose: Start a fully autonomous concurrent run with parallel Claude Code workers.

Runs:
1. Verify `BRIEF.md` and `profiles/project-profile.yaml` are filled in.
2. Set `runtime/config.yaml` (model, max workers, notification webhook, phases to skip).
3. Execute: `python runtime/run.py --project /path/to/project`
4. Orchestrator spawns workers per phase, enforces gates, merges branches.
5. Pauses after Requirements for human review (configurable).
6. Resume with: `python runtime/run.py --project /path/to/project --resume`
7. Notifies on completion or blocking failure.

Primary files:
- `runtime/DESIGN.md`
- `runtime/config.yaml`
- `runtime/run.py`
- `BRIEF.md`
- `profiles/project-profile.yaml`
- `STATUS.md`

## Feedback and Validation

### `/retrospective`
Purpose: Run a structured post-project or post-phase retrospective.

Runs:
1. Read `evaluation/scorecard.md` and `qa/audit-report.md`.
2. Identify where rework loops occurred (from `operations/tracker.md` history and `qa/issues.md`).
3. Assess which gates caught issues vs. missed them.
4. Produce a retrospective summary:
   - What worked well
   - What caused friction or rework
   - Gate effectiveness (caught / missed / false positive)
   - Scorecard results vs. targets
   - Recommended harness or process improvements
5. Log actionable improvements in `DECISIONS.md`.
6. If improvements affect harness files, add entries to `FUTURE_IMPROVEMENTS.md`.

Primary files:
- `evaluation/scorecard.md`
- `qa/audit-report.md`
- `qa/issues.md`
- `operations/tracker.md`
- `DECISIONS.md`
- `FUTURE_IMPROVEMENTS.md`

### `/validate-harness`
Purpose: Check internal consistency of harness files.

Runs:
1. Verify every skill referenced in `profiles/active-skills.yaml` exists in `skills/`.
2. Verify every role in `harness/permissions-matrix.md` has a corresponding file in `harness/agents/`.
3. Verify handoff templates in `handoffs/` cover the workflow edges defined in `harness/routing-policy.md`.
4. Verify `AGENTS.md` references match actual file paths.
5. Verify `COMMANDS.md` primary file references exist.
6. Report:
   - PASS: all checks green
   - FAIL: list of inconsistencies with file paths and suggested fixes

Primary files:
- `AGENTS.md`
- `COMMANDS.md`
- `profiles/active-skills.yaml`
- `harness/permissions-matrix.md`
- `harness/agents/*.md`
- `handoffs/*.md`
- `harness/routing-policy.md`
