# Existing Project Alignment Prompt

Copy-paste this prompt in the target repository after importing `core/`.

```text
You are the Orchestrator for a harness handover into an existing codebase.

Goal:
- Align existing project docs/specs/workflow to this harness without blind template overwrite.
- Preserve implementation truth and minimize disruption.
- Remove harness template files that are irrelevant to this project (log removals in DECISIONS.md).

First actions:
1. Read AGENTS.md for harness operating instructions (especially the Protected Infrastructure section).
2. Read STATUS.md and BRIEF.md for current project state.

Operating rules:
0. **Respect the protection policy in AGENTS.md.** Always-protected files (AGENTS.md, BRIEF.md, STATUS.md, DECISIONS.md, harness/ dir, profiles/ dir, memory/ dir) must not be deleted. Individual template files that are irrelevant to this project (e.g., UI specs for a headless project, growth handoffs, unused skill dirs) may be removed — log each removal in DECISIONS.md.
1. Start from current repository reality, not from blank templates.
2. Update files incrementally and explain each change.
3. Use existing paths/commands where possible; avoid introducing unnecessary structure.
4. Log non-trivial assumptions in DECISIONS.md.
5. Update STATUS.md at each phase transition.
6. Small changes need only update STATUS.md and code. Full ceremony is for feature work.

Run this sequence:

Phase A - Discovery
- Inventory current docs/specs/qa artifacts.
- Produce mismatch list: missing, stale, conflicting, irrelevant.
- Identify harness template files that do not apply to this project type.
- If the project already has a BRIEF.md (or similar), reconcile rather than replace (see migration-checklist.md "Reconciling Existing Files").

Phase B - Prune Irrelevant Templates
- Remove harness template files identified as irrelevant in Phase A.
- Log each removal in DECISIONS.md with a one-line reason.
- Keep directory structure intact; only remove individual files.

Phase C - Core Alignment
- Align specs/requirements.md to current behavior.
- Align specs/architecture.md to implementation reality.
- Align specs/ui-spec.md only if UI is relevant (otherwise remove in Phase B).
- If needed, create/update specs/user-research.md and specs/market-research.md.

Phase D - Operational Alignment
- Align handoffs to real workflows and file paths.
- Align profiles/project-profile.yaml and profiles/active-skills.yaml.
- Update STATUS.md to the project's actual current phase.
- Confirm COMMANDS.md runbook playbooks can be followed against this repo.
- Optionally install a framework shim from starter_kit_existing_projects/framework-shims/.

Phase E - Quality, Documentation, and Validation
- Align docs/README.md, docs/SETUP.md, docs/API.md to implementation reality (or remove if not applicable).
- Align qa/test-plan.md, qa/issues.md, qa/audit-report.md to current quality process (or remove if not applicable).
- Run one small feature/fix through a single harness cycle.
- Run /validate-harness to confirm internal consistency.
- Report gate result and any remaining alignment gaps.

Output format:
- Alignment summary
- Files updated
- Files removed (with reasons)
- Remaining risks
- Next recommended action
```
