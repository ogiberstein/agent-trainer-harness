# Alignment (Recommended for Existing Projects)

Use this flow to hand over an existing project to the harness team without template overwrites.

## What this is
- A guided prompt + checklist for agents to align current docs/specs with harness standards.
- Focuses on incremental updates inside existing files rather than copy-replace operations.

## How to use
1. Copy `core/` into the target repository first.
2. Run the alignment prompt from `EXISTING_PROJECT_ALIGNMENT_PROMPT.md`.
3. Track completion with `EXISTING_PROJECT_ALIGNMENT_CHECKLIST.md`.
4. Follow `migration-checklist.md` in the target repository for the full migration flow.

## Expected outputs
- Updated `specs/requirements.md`, `specs/architecture.md`, `specs/ui-spec.md` (as applicable)
- Optional `specs/user-research.md` and `specs/market-research.md`
- Updated `docs/` and `qa/` artifacts aligned to current implementation
- Alignment decisions logged in `DECISIONS.md`
