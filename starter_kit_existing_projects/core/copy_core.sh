#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: bash starter_kit_existing_projects/core/copy_core.sh /path/to/target-repo"
  exit 1
fi

TARGET="$1"
if [ ! -d "$TARGET" ]; then
  echo "Target directory does not exist: $TARGET"
  exit 1
fi

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SOURCE_ROOT="$ROOT"
TEMP_CLONE_DIR=""

# Fallback source configuration
DEFAULT_GH_REPO="ogiberstein/agent_trainer"
SOURCE_REPO="${HARNESS_SOURCE_REPO:-$DEFAULT_GH_REPO}"
SOURCE_REPO_URL="${HARNESS_SOURCE_REPO_URL:-}"

cleanup() {
  if [ -n "$TEMP_CLONE_DIR" ] && [ -d "$TEMP_CLONE_DIR" ]; then
    rm -rf "$TEMP_CLONE_DIR"
  fi
}
trap cleanup EXIT

has_local_source() {
  [ -f "$1/AGENTS.md" ] && [ -d "$1/starter_kit_existing_projects/core" ]
}

if ! has_local_source "$SOURCE_ROOT"; then
  echo "Local harness source not found at expected path: $SOURCE_ROOT"
  echo "Attempting GitHub fallback..."

  TEMP_CLONE_DIR="$(mktemp -d)"

  # Prefer gh for private repos (uses existing GitHub CLI auth)
  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    if gh repo clone "$SOURCE_REPO" "$TEMP_CLONE_DIR/source" >/dev/null 2>&1; then
      SOURCE_ROOT="$TEMP_CLONE_DIR/source"
      echo "Using source from GitHub via gh: $SOURCE_REPO"
    fi
  fi

  # Fallback to explicit repo URL if provided
  if ! has_local_source "$SOURCE_ROOT" && [ -n "$SOURCE_REPO_URL" ]; then
    if git clone --depth 1 "$SOURCE_REPO_URL" "$TEMP_CLONE_DIR/source" >/dev/null 2>&1; then
      SOURCE_ROOT="$TEMP_CLONE_DIR/source"
      echo "Using source from HARNESS_SOURCE_REPO_URL"
    fi
  fi

  if ! has_local_source "$SOURCE_ROOT"; then
    echo "Unable to resolve harness source."
    echo "Options:"
    echo "  1) Run script from within a full harness repo clone."
    echo "  2) Authenticate GitHub CLI and set HARNESS_SOURCE_REPO (default: $DEFAULT_GH_REPO)."
    echo "  3) Set HARNESS_SOURCE_REPO_URL to a cloneable git URL."
    exit 3
  fi
fi

echo "Copying core harness files to: $TARGET"

FILES=(
  "AGENTS.md"
  "BRIEF.md"
  "STATUS.md"
  "DECISIONS.md"
  "COMMANDS.md"
  "FUTURE_IMPROVEMENTS.md"
  "day-0-start.md"
  "lite-mode-checklist.md"
  "migration-checklist.md"
)

DIRS=(
  "harness"
  "profiles"
  "memory"
  "evaluation"
  "operations"
  "skills"
  "handoffs"
  "specs"
  "qa"
  "docs"
)

CONFLICTS=()
for f in "${FILES[@]}"; do
  if [ -e "$TARGET/$f" ]; then
    CONFLICTS+=("$TARGET/$f")
  fi
done
for d in "${DIRS[@]}"; do
  if [ -e "$TARGET/$d" ]; then
    CONFLICTS+=("$TARGET/$d")
  fi
done

if [ "${#CONFLICTS[@]}" -gt 0 ]; then
  echo "Aborting: existing files/folders detected (safe mode, no overwrite)."
  for c in "${CONFLICTS[@]}"; do
    echo " - $c"
  done
  echo "Resolve/remove conflicts manually, then rerun."
  exit 2
fi

for f in "${FILES[@]}"; do
  cp "$SOURCE_ROOT/$f" "$TARGET/$f"
done

for d in "${DIRS[@]}"; do
  cp -R "$SOURCE_ROOT/$d" "$TARGET/"
done

# Copy .gitignore separately (dotfile)
if [ ! -e "$TARGET/.gitignore" ]; then
  cp "$SOURCE_ROOT/.gitignore" "$TARGET/.gitignore"
fi

echo "Core copy complete."
echo "Copied: ${#FILES[@]} root files, ${#DIRS[@]} directories, .gitignore"
echo ""
echo "Next steps:"
echo "  1. Run alignment handover: starter_kit_existing_projects/alignment/EXISTING_PROJECT_ALIGNMENT_PROMPT.md"
echo "  2. Follow the checklist: migration-checklist.md"
