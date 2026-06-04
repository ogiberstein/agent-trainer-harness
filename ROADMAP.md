# Agent Trainer Harness Roadmap

Roadmap-level direction for the public Agent Trainer Harness repo. This is the repo-level roadmap, not the per-project template `ROADMAP.md` file that downstream harnesses copy into their own projects.

## North Star
Make copied project harnesses reliable enough that a future agent can recover product direction, current state, and durable decisions without Slack archaeology or guessing.

## Now / Next / Later

### Now
- [ ] Keep the `ROADMAP.md` control-doc contract consistent across templates, validators, drift reports, and docs.
- [ ] Keep public templates sanitized and aligned with the latest release contract.

### Next
- [ ] Review active vendored harness projects and request/add correctly formatted `ROADMAP.md` files without deleting useful legacy `PROGRESS.md` history.
- [ ] Keep Lite mode as the flagship near-term path while Full/Concurrent remain available for larger projects.

### Later / Deferred
- [ ] Add broader mode-agnostic validation tooling if drift reporter checks prove insufficient for Lite/Full downstream projects.
- [ ] Revisit Concurrent runtime investment only after explicit dogfood demand.

## Milestones

| Milestone | Outcome | Acceptance Signal | Dependencies | Status |
|---|---|---|---|---|
| ROADMAP migration hardened | Templates and checks agree on the control-doc contract | Tests pass and stale references stay absent | Drift reporter/control-doc checks, stale-reference tests, copy-command fix | Done |
| Public harness release | Public repo carries the sanitized template update | Public checks pass; no private/local-path leakage | ROADMAP migration hardened | In Progress |
| Downstream project migration | Active vendored projects have ROADMAP in the right format | Drift report surfaces migration state; each project agent preserves useful legacy history | Public/private contract stable | Planned |

## Concurrent Harness Parking Lot

These are concurrent-runtime ideas retained from the old concurrent-only root roadmap. They are parked until a project explicitly chooses Concurrent mode or a dedicated dogfood run is scheduled.

- Inter-worker communication via file-based message passing in a shared `handoffs/live/` directory.
- Incremental gate checks for long tasks before a worker completes the whole task.
- Worker resume in the same worktree after timeout/crash instead of creating a fix-task from scratch.
- Cost tracking by parsing CLI token usage and aggregating per task/phase/run.
- Parallel phase support driven by task dependency graph rather than strict linear phase order.

## Roadmap Change Log
- 2026-06-04 — Generalized root roadmap after template `ROADMAP.md` adoption; moved old concurrent-specific roadmap items into parking lot.
