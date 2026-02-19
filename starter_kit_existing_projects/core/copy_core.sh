#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: bash copy_core.sh [OPTIONS] /path/to/target-repo

Options:
  --preset <full|backend|minimal>   Control which files are copied (default: full)
  --source /path/to/harness-repo    Explicit path to harness source repo
  -h, --help                        Show this help

Presets:
  full      All harness files (SaaS, multi-role teams)
  backend   Skips UI specs, designer/frontend/growth agents, growth skills/handoffs
  minimal   Bare essentials only (AGENTS.md, BRIEF.md, STATUS.md, DECISIONS.md,
            specs/requirements.md, core agent prompts, profiles, memory)

Examples:
  bash copy_core.sh /path/to/target
  bash copy_core.sh --preset backend /path/to/target
  bash copy_core.sh --preset minimal --source ~/harness /path/to/target
USAGE
  exit 0
}

PRESET="full"
EXPLICIT_SOURCE=""
TARGET=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --preset) PRESET="$2"; shift 2 ;;
    --source) EXPLICIT_SOURCE="$2"; shift 2 ;;
    -h|--help) usage ;;
    -*) echo "Unknown option: $1"; usage ;;
    *) TARGET="$1"; shift ;;
  esac
done

if [ -z "$TARGET" ]; then
  echo "Error: target directory is required."
  usage
fi

if [ ! -d "$TARGET" ]; then
  echo "Target directory does not exist: $TARGET"
  exit 1
fi

if [[ "$PRESET" != "full" && "$PRESET" != "backend" && "$PRESET" != "minimal" ]]; then
  echo "Unknown preset: $PRESET (expected: full, backend, minimal)"
  exit 1
fi

if [ -n "$EXPLICIT_SOURCE" ]; then
  SOURCE_ROOT="$EXPLICIT_SOURCE"
else
  ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
  SOURCE_ROOT="$ROOT"
fi

TEMP_CLONE_DIR=""
DEFAULT_GH_REPO="ogiberstein/agent-trainer-harness"
SOURCE_REPO="${HARNESS_SOURCE_REPO:-$DEFAULT_GH_REPO}"
SOURCE_REPO_URL="${HARNESS_SOURCE_REPO_URL:-}"

cleanup() {
  if [ -n "$TEMP_CLONE_DIR" ] && [ -d "$TEMP_CLONE_DIR" ]; then
    rm -rf "$TEMP_CLONE_DIR"
  fi
}
trap cleanup EXIT

has_local_source() {
  [ -f "$1/AGENTS.md" ] && [ -d "$1/harness/agents" ]
}

if ! has_local_source "$SOURCE_ROOT"; then
  echo "Local harness source not found at: $SOURCE_ROOT"
  echo "Attempting GitHub fallback..."
  TEMP_CLONE_DIR="$(mktemp -d)"

  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    if gh repo clone "$SOURCE_REPO" "$TEMP_CLONE_DIR/source" >/dev/null 2>&1; then
      SOURCE_ROOT="$TEMP_CLONE_DIR/source"
      echo "Using source from GitHub via gh: $SOURCE_REPO"
    fi
  fi

  if ! has_local_source "$SOURCE_ROOT" && [ -n "$SOURCE_REPO_URL" ]; then
    if git clone --depth 1 "$SOURCE_REPO_URL" "$TEMP_CLONE_DIR/source" >/dev/null 2>&1; then
      SOURCE_ROOT="$TEMP_CLONE_DIR/source"
      echo "Using source from HARNESS_SOURCE_REPO_URL"
    fi
  fi

  if ! has_local_source "$SOURCE_ROOT"; then
    echo "Unable to resolve harness source."
    echo "Options:"
    echo "  1) Pass --source /path/to/harness-repo"
    echo "  2) Run from within a full harness repo clone."
    echo "  3) Set HARNESS_SOURCE_REPO (default: $DEFAULT_GH_REPO) with gh auth."
    echo "  4) Set HARNESS_SOURCE_REPO_URL to a cloneable git URL."
    exit 3
  fi
fi

echo "Preset: $PRESET"
echo "Source: $SOURCE_ROOT"
echo "Target: $TARGET"
echo ""

# --- Define what each preset includes ---

FILES_ALWAYS=(
  "AGENTS.md"
  "BRIEF.md"
  "STATUS.md"
  "DECISIONS.md"
)

FILES_FULL=(
  "${FILES_ALWAYS[@]}"
  "COMMANDS.md"
  "FUTURE_IMPROVEMENTS.md"
  "migration-checklist.md"
)

FILES_BACKEND=("${FILES_FULL[@]}")

FILES_MINIMAL=("${FILES_ALWAYS[@]}")

DIRS_FULL=(
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

DIRS_BACKEND=(
  "harness"
  "profiles"
  "memory"
  "evaluation"
  "operations"
  "skills"
  "handoffs"
)

DIRS_MINIMAL=(
  "profiles"
  "memory"
)

case "$PRESET" in
  full)    FILES=("${FILES_FULL[@]}");    DIRS=("${DIRS_FULL[@]}") ;;
  backend) FILES=("${FILES_BACKEND[@]}"); DIRS=("${DIRS_BACKEND[@]}") ;;
  minimal) FILES=("${FILES_MINIMAL[@]}"); DIRS=("${DIRS_MINIMAL[@]}") ;;
esac

# --- Minimal preset: extra individual files to copy (and conflict-check) ---

EXTRA_FILES_MINIMAL=(
  "specs/requirements.md"
  "harness/agents/orchestrator.md"
  "harness/agents/fullstack-engineer.md"
  "harness/agents/qa-engineer.md"
  "harness/routing-policy.md"
  "harness/permissions-matrix.md"
)

# --- Conflict check ---

CONFLICTS=()
for f in "${FILES[@]}"; do
  [ -e "$TARGET/$f" ] && CONFLICTS+=("$TARGET/$f")
done
for d in "${DIRS[@]}"; do
  [ -e "$TARGET/$d" ] && CONFLICTS+=("$TARGET/$d")
done
if [ "$PRESET" = "minimal" ]; then
  for ef in "${EXTRA_FILES_MINIMAL[@]}"; do
    [ -e "$TARGET/$ef" ] && CONFLICTS+=("$TARGET/$ef")
  done
fi

if [ "${#CONFLICTS[@]}" -gt 0 ]; then
  echo "Aborting: existing files/folders detected (safe mode, no overwrite)."
  for c in "${CONFLICTS[@]}"; do
    echo " - $c"
  done
  echo "Resolve/remove conflicts manually, then rerun."
  exit 2
fi

# --- Copy ---

for f in "${FILES[@]}"; do
  cp "$SOURCE_ROOT/$f" "$TARGET/$f"
done

for d in "${DIRS[@]}"; do
  cp -R "$SOURCE_ROOT/$d" "$TARGET/"
done

# --- Preset-specific post-copy ---

if [ "$PRESET" = "backend" ]; then
  rm -f "$TARGET/harness/agents/designer.md" 2>/dev/null || true
  rm -f "$TARGET/harness/agents/frontend-engineer.md" 2>/dev/null || true
  rm -f "$TARGET/harness/agents/growth-strategist.md" 2>/dev/null || true
  rm -f "$TARGET/handoffs/design-to-engineering.md" 2>/dev/null || true
  rm -f "$TARGET/handoffs/product-to-design.md" 2>/dev/null || true
  rm -f "$TARGET/handoffs/growth-to-engineering.md" 2>/dev/null || true
  rm -f "$TARGET/handoffs/growth-to-documentation.md" 2>/dev/null || true
  rm -rf "$TARGET/skills/growth-"* 2>/dev/null || true
fi

if [ "$PRESET" = "minimal" ]; then
  for ef in "${EXTRA_FILES_MINIMAL[@]}"; do
    mkdir -p "$TARGET/$(dirname "$ef")"
    cp "$SOURCE_ROOT/$ef" "$TARGET/$ef"
  done
fi

if [ ! -e "$TARGET/.gitignore" ]; then
  cp "$SOURCE_ROOT/.gitignore" "$TARGET/.gitignore"
fi

echo ""
echo "Core copy complete (preset: $PRESET)."
echo "Copied: ${#FILES[@]} root files, ${#DIRS[@]} directories, .gitignore"
echo ""
echo "Next steps:"
echo "  1. Run alignment handover: starter_kit_existing_projects/alignment/EXISTING_PROJECT_ALIGNMENT_PROMPT.md"
echo "  2. Follow the checklist: migration-checklist.md"
