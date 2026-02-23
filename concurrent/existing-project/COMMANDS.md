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
- `start.md`
- `profiles/project-profile.yaml`
- `profiles/active-skills.yaml`
- `STATUS.md`

### `/phase-next`
Purpose: Advance exactly one phase with gate enforcement.

**Executable:** `python3 cli/harness_cli.py --project . phase-next` (add `--force` to skip gate)

Runs:
1. Read current phase from `STATUS.md`.
2. Run LLM gate evaluation for current phase.
3. If gate passes, advance phase in `STATUS.md`.
4. If gate fails, report missing criteria (use `--force` to override).

Primary files:
- `cli/harness_cli.py`
- `STATUS.md`
- `DECISIONS.md`

### `/gate-check`
Purpose: Run gate review without doing implementation work.

**Executable:** `python3 cli/harness_cli.py --project . gate-check [--phase <phase>]`

Runs:
1. Evaluate LLM gate criteria for the specified or current phase.
2. Return PASS/FAIL with summary, evidence, and missing items.

Primary files:
- `cli/harness_cli.py`
- `STATUS.md`
- `operations/tracker.md`
- Phase-specific artifacts in `specs/`, `qa/`, `docs/`

## Task and Execution Operations

### `/status`
Purpose: Show current phase and task summary.

**Executable:** `python3 cli/harness_cli.py --project . status` (add `--json` for structured output)

### `/task-list`
Purpose: List all tasks from `operations/tracker.md`.

**Executable:** `python3 cli/harness_cli.py --project . task list` (add `--json` for structured output)

### `/task-add`
Purpose: Add a new task card to `operations/tracker.md`.

**Executable:** `python3 cli/harness_cli.py --project . task add --title "..." --role "..." [--phase "..."] [--priority P1]`

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

### `/preflight-concurrent`
Purpose: Verify all prerequisites for concurrent mode before launching.

**Executable:** `python3 cli/preflight_concurrent.py --project .` (add `--json` for structured output)

Checks: Python 3.10+, Claude CLI on PATH, git repo with commits, `runtime/` present, `runtime/config.yaml` valid, Python deps installed, `BRIEF.md` filled in.

### `/launch-concurrent`
Purpose: Run preflight checks and launch the concurrent orchestrator as a background process.

**Executable:** `python3 cli/harness_cli.py --project . launch-concurrent`

Runs preflight, installs deps if needed, launches `runtime/run.py` in background, prints PID and monitoring instructions. If preflight fails, prints what's missing and exits with code 1 (agent should fall back to Full mode).

### `/run-concurrent`
Purpose: Start a fully autonomous concurrent run with parallel Claude Code workers (manual steps).

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

**Executable:** `python3 cli/validate_harness.py --project .` (add `--json` for CI output)

Checks:
1. Core files exist (`AGENTS.md`, `BRIEF.md`, `STATUS.md`, `DECISIONS.md`).
2. Every role in `harness/permissions-matrix.md` has a corresponding file in `harness/agents/`.
3. Every active skill in `profiles/active-skills.yaml` exists in `skills/`.
4. Handoff templates have required sections (status, context, deliverables, acceptance criteria).
5. Backtick-quoted file paths in `AGENTS.md` and `COMMANDS.md` exist on disk.
6. `runtime/config.yaml` is valid YAML (if present).

Output: human-readable report or JSON. Exit code 0 = pass, 1 = fail.

Primary files:
- `cli/validate_harness.py`
- `AGENTS.md`
- `COMMANDS.md`
- `profiles/active-skills.yaml`
- `harness/permissions-matrix.md`
- `harness/agents/*.md`
- `handoffs/*.md`
