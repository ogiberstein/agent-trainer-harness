# Harness Feedback — From TEA Build (2026-02-25)

Feedback from first real-world use of the concurrent harness on a non-trivial project (two-service fintech MVP with TypeScript + Python).

## What worked well

1. **Git worktree isolation** — each worker gets its own branch. No file conflicts during execution. Clean merge-or-retry flow.
2. **Gate check pattern** — LLM judge evaluating artifacts against criteria is a solid quality gate. The retry-with-fix-task loop is well designed.
3. **Checkpoint/pause** — `runtime/.checkpoint` is a simple, reliable mechanism for human intervention.
4. **Notification hooks** — webhook-based, tested in 30 seconds. Good for overnight runs.
5. **Preflight script** — catches env issues before you waste time. Saved us from a Python 3.9 / missing deps situation.
6. **File zones (System / State / App)** — clear ownership model. Prevents workers from clobbering harness files.
7. **DECISIONS.md as audit trail** — useful for multi-session context. Workers and orchestrator both write to it.

## Issues found — must fix for production use

### 1. Implementation tasks are too coarse (Critical)

**Problem:** `PHASE_ROLES` generates exactly 2 implementation tasks: "Backend" and "Frontend." For any non-trivial project, this produces a single mega-prompt like "build the entire backend" — which is too large for a single Claude Code invocation to do well.

**Impact:** Lower code quality, missed edge cases, higher failure rate at gate checks.

**Fix:** Either:
- (a) Let the orchestrator auto-decompose implementation into 10-20 atomic tasks by reading the architecture spec, or
- (b) Support pre-seeded task boards in `operations/tracker.md` that the orchestrator respects instead of auto-generating, or
- (c) Add a "task planning" sub-phase before implementation dispatch where a planner agent reads specs and generates the task board.

Option (c) is the most robust. Option (b) is what I'm using as a workaround for TEA.

### 2. No task dependency ordering (Critical)

**Problem:** `get_ready_tasks()` returns all tasks with status "ready" for the current phase. There's no mechanism to say "Task B depends on Task A completing first." The orchestrator dispatches everything in parallel.

**Impact:** For TEA, the shared schema (JSON contract between web and engine) MUST exist before either service can import its types. Without dependency ordering, both services start building with no contract to validate against.

**Fix:** Add a `dependencies: [TASK-IMP-001]` field to Task. `get_ready_tasks()` should filter to tasks where all dependencies are marked done.

### 3. Worker prompts lack spec context (Critical)

**Problem:** `_build_task_prompt()` in `worker.py` includes a truncated BRIEF.md (2000 chars) and tells workers to "Read AGENTS.md" and "Read STATUS.md." It does NOT reference the actual specs that contain the data model, API design, tech stack, UI components, or security requirements.

**Impact:** Workers discover specs by accident (if they explore the repo) or not at all. They may build against wrong assumptions.

**Fix:** Either:
- (a) Include file paths to relevant specs in the task definition (e.g., `required_reads: [specs/architecture.md, specs/ui-spec.md]`) and inject them into the prompt, or
- (b) Always include a "## Required Reading" section listing all spec files, or
- (c) The task prompt should include the full content of key specs (not just file paths) so workers don't need to spend turns reading files.

I'm using (a) for TEA — each task explicitly lists which specs to read.

### 4. Hardcoded output paths (Medium)

**Problem:** Role prompts (fullstack-engineer.md, frontend-engineer.md) reference `src/` and `tests/` as output directories. Real projects have varied structures (`apps/web/`, `engine/`, `packages/`, etc.).

**Fix:** Make output paths configurable per-task or per-project in `project-profile.yaml`. Workers should read their task's `file_scope` instead of assuming `src/`.

### 5. No role for specialized services (Medium)

**Problem:** The role library covers generic fullstack/frontend/QA/docs. TEA's Python execution engine (asyncio, exchange adapters, trading logic) doesn't map to any existing role. The fullstack-engineer role is TypeScript-flavored.

**Fix:** Either:
- (a) Allow custom roles in `harness/agents/` (the mechanism exists but PHASE_ROLES doesn't auto-discover them), or
- (b) Support role overrides in `project-profile.yaml` (e.g., map "backend" → "engine-engineer" for this project), or
- (c) Make roles truly generic and move domain expertise into task acceptance criteria.

I'm using (a) for TEA — created a custom `engine-engineer.md` role.

### 6. Design phase redundancy (Low)

**Problem:** Phase sequence is fixed: requirements → design → implementation. If specs and designs already exist (common when a human did discovery), the design phase spawns a designer agent that re-creates work.

**Fix:** `skip_phases` already handles this. Just needs documentation nudging users to skip phases they've already completed. Currently only mentions skipping "growth" and "documentation."

### 7. Worker timeout may be too short (Low)

**Problem:** Default `worker_timeout: 3600` (1 hour). Complex implementation tasks (full exchange adapter with tests, or full Next.js app scaffold) can legitimately take longer.

**Fix:** Make timeout configurable per-task, not just globally. Some tasks are 15 minutes, some are 2+ hours.

## Suggested enhancements (future)

1. **Inter-worker communication** — Workers currently can't coordinate. If the backend worker changes an API contract, the frontend worker doesn't know. A shared `handoffs/` directory partially addresses this, but real-time coordination (e.g., via a shared Redis channel or file-based message passing) would help.

2. **Incremental gate checks** — Currently gates run after a worker finishes its entire task. For long tasks, an intermediate checkpoint ("did the worker set up the project correctly before writing all the code?") would catch issues earlier.

3. **Worker resume** — If a worker times out or crashes, the current approach creates a new fix-task from scratch. Being able to resume the worker in its worktree (with its existing progress) would be more efficient.

4. **Cost tracking** — Log token usage per worker invocation. At Opus pricing, an overnight run can get expensive. Knowing which tasks consume the most helps optimize.

5. **Parallel phase support** — Some phases can overlap. QA can start on finished tracks while implementation continues on others. The current linear phase model doesn't support this.

---

*Generated during TEA by Coinrule build session, 2026-02-25. Applied workarounds documented in DECISIONS.md.*
