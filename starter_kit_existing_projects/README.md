# Starter Kit for Existing Projects

Use this folder as a safe import kit when adding the harness to an existing repository.

## Structure
- `core/` -> safe-to-copy operational harness files and folders.
- `alignment/` -> recommended handover flow (prompt + checklist) to align existing docs/specs in place.
- `framework-shims/` -> optional auto-discovery files for Cursor, Claude Code, GitHub Copilot, etc.

## Recommended Flow
1. Read `core/README.md` and pick a preset (`full`, `backend`, or `minimal`).
2. Run `copy_core.sh --preset <preset> /path/to/target`.
3. Read `alignment/README.md` and run the alignment handover flow (includes pruning irrelevant templates).
4. Run `migration-checklist.md` in the target repository.
5. Optionally install a framework shim from `framework-shims/`.

## Why split this way
- Core files can usually be dropped in without touching existing app code.
- Alignment-first avoids risky overwrite behavior in mature docs/specs.
- Framework shims are optional thin pointers to the canonical `AGENTS.md`.
