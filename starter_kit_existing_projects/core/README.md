# Core (Safe to Copy)

These files/folders are generally safe to copy into an existing project.

## Includes
- Harness orchestration layer
- Profiles and skill controls
- Operations/evaluation policies
- Handoffs and runbook playbooks
- Framework-agnostic bootstrap (`AGENTS.md`)

## Presets

The copy script supports three presets to control what gets copied:

| Preset | Use for | What it skips |
|--------|---------|---------------|
| `full` (default) | SaaS, multi-role teams | Nothing |
| `backend` | APIs, bots, headless services | UI specs, designer/frontend/growth agents, growth skills/handoffs |
| `minimal` | Solo dev, small projects | Most harness — copies only core files, profiles, memory, and 3 agent prompts |

See `FILE_LIST.md` for the detailed breakdown per preset.

## Copy Method

```bash
bash copy_core.sh /path/to/target                              # full preset
bash copy_core.sh --preset backend /path/to/target              # backend preset
bash copy_core.sh --preset minimal /path/to/target              # minimal preset
bash copy_core.sh --source ~/harness --preset backend /path     # explicit source
```

If local source discovery fails, the script can fall back to GitHub:
- Default repo: `ogiberstein/agent-trainer-harness` via `gh repo clone`
- Override repo slug: `HARNESS_SOURCE_REPO="owner/repo"`
- Override clone URL: `HARNESS_SOURCE_REPO_URL="https://...git"`

Then open the target repo and run:
- `starter_kit_existing_projects/alignment/EXISTING_PROJECT_ALIGNMENT_PROMPT.md`
- `migration-checklist.md`

## Notes
- This script does not touch existing `src/` or `tests/` content.
- Safe-by-default behavior: the script aborts if target core files/folders already exist, so nothing is overwritten accidentally.
- Existing `specs/`, `qa/`, and `docs/` should be aligned in place via `alignment/` (not copied over) — except in `full` preset where blank templates are included.
- To add framework-specific auto-discovery, install a shim from `starter_kit_existing_projects/framework-shims/`.
