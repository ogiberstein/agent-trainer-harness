# Core (Safe to Copy)

These files/folders are generally safe to copy into an existing project.

## Includes
- Harness orchestration layer
- Profiles and skill controls
- Operations/evaluation policies
- Handoffs and command runbooks
- Framework-agnostic bootstrap (`AGENTS.md`)

## Copy Method
Use `copy_core.sh` from repository root:

```bash
bash starter_kit_existing_projects/core/copy_core.sh "/path/to/target-repo"
```

If local source discovery fails, the script can fall back to GitHub:
- Default repo: `ogiberstein/agent_trainer` via `gh repo clone` (requires `gh auth status` success)
- Override repo slug: `HARNESS_SOURCE_REPO="owner/repo"`
- Override clone URL: `HARNESS_SOURCE_REPO_URL="https://...git"`

Then open the target repo and run:
- `starter_kit_existing_projects/alignment/EXISTING_PROJECT_ALIGNMENT_PROMPT.md`
- `migration-checklist.md`

## Notes
- This script does not touch existing `src/` or `tests/` content.
- Safe-by-default behavior: the script aborts if target core files/folders already exist, so nothing is overwritten accidentally.
- Existing `specs/`, `qa/`, and `docs/` should be aligned in place via `alignment/` (not copied over).
- To add framework-specific auto-discovery, install a shim from `starter_kit_existing_projects/framework-shims/`.
