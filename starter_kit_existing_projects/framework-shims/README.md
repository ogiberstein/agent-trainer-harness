# Framework Shims

Optional auto-discovery files for specific AI frameworks. Each shim simply points the framework's agent to `AGENTS.md` in the project root.

## Available Shims

| Framework | File | Destination in target repo |
|-----------|------|---------------------------|
| Cursor | `cursor-rules.mdc` | `.cursor/rules/harness.mdc` |
| Claude Code | `CLAUDE.md` | `CLAUDE.md` (root) |
| GitHub Copilot | `copilot-instructions.md` | `.github/copilot-instructions.md` |

## Usage

Copy the relevant shim file into the correct path in your target repo. For example:

```bash
# Cursor
mkdir -p .cursor/rules
cp starter_kit_existing_projects/framework-shims/cursor-rules.mdc .cursor/rules/harness.mdc

# Claude Code
cp starter_kit_existing_projects/framework-shims/CLAUDE.md ./CLAUDE.md

# GitHub Copilot
mkdir -p .github
cp starter_kit_existing_projects/framework-shims/copilot-instructions.md .github/copilot-instructions.md
```

## Design Principle

The canonical operating instructions live in `AGENTS.md` at the repo root. Framework shims are thin pointers that delegate to it. This keeps the harness framework-agnostic while supporting zero-config discovery in popular tools.
