# Roadmap — Concurrent Harness

Future enhancements for the concurrent orchestration harness. These are harness-level concerns, not specific to any individual project.

## Inter-worker communication

Workers currently can't coordinate during execution. If the backend worker changes an API contract mid-task, the frontend worker doesn't know. The `handoffs/` directory provides post-task coordination, but real-time awareness (e.g., a shared message file or lightweight event bus) would catch contract drift earlier.

**Approach:** File-based message passing in a shared `handoffs/live/` directory that workers poll. Lower complexity than Redis, works within the git worktree model.

## Incremental gate checks

Gates currently run only after a worker finishes its entire task. For long tasks, an intermediate checkpoint (e.g., "did the worker set up the project scaffold correctly before writing all the application code?") would catch structural issues earlier and reduce wasted work.

**Approach:** Optional mid-task gate definitions on the Task card. The orchestrator polls worker output and triggers a lightweight gate check at defined intervals or when specific markers appear in the output log.

## Worker resume

If a worker times out or crashes, the current approach creates a new fix-task from scratch. The worktree already contains the worker's partial progress — resuming the Claude Code session in that worktree (with context about what was already done) would be significantly more efficient than starting over.

**Approach:** On timeout/crash, instead of creating a fix-task, re-invoke Claude Code in the same worktree with a prompt that includes a summary of prior progress (extracted from the output log) and the remaining acceptance criteria.

## Cost tracking

Log token usage per worker invocation. At Opus pricing, an overnight run can get expensive. Knowing which tasks and phases consume the most tokens helps optimize prompt sizes, model selection, and task granularity.

**Approach:** Parse the Claude CLI output for token usage metadata and log it alongside existing telemetry events. Aggregate per-task, per-phase, and per-run totals. Surface in a post-run cost summary.

## Parallel phase support

Some phases can overlap — QA can start on finished tracks while implementation continues on other tracks. The current linear phase model (`requirements -> design -> implementation -> qa -> ...`) prevents this.

**Approach:** Allow phase-level dependencies instead of strict ordering. A task's phase becomes advisory metadata; the dependency graph (already supported on tasks) drives execution order. Requires rethinking `advance_phase()` and `phase_complete()` to work with partial phase overlap.

---

*Collected from TEA by Coinrule build feedback (2026-02-25) and ongoing harness development.*
