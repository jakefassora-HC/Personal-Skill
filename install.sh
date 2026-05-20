#!/usr/bin/env bash
set -euo pipefail

MODE="both"
SOURCE_DIR=""
BUNDLED_SKILLS=(
  "skills/pilot"
  "skills/start"
  "skills/prompt-improver"
)

usage() {
  cat <<'USAGE'
Usage: ./install.sh [--both|--claude|--codex] [--source PATH]

Installs the Personal-Skill bundle for Claude Code and/or Codex.

Options:
  --both          Install for Claude Code and Codex (default)
  --claude        Install for Claude Code only
  --codex         Install for Codex only
  --source PATH   Install only one skill folder instead of the default bundle
  -h, --help      Show this help
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --both) MODE="both"; shift ;;
    --claude) MODE="claude"; shift ;;
    --codex) MODE="codex"; shift ;;
    --source)
      SOURCE_DIR="${2:-}"
      if [[ -z "$SOURCE_DIR" ]]; then
        echo "error: --source requires a path" >&2
        exit 1
      fi
      shift 2
      ;;
    -h|--help) usage; exit 0 ;;
    *) echo "error: unknown option: $1" >&2; usage; exit 1 ;;
  esac
done

CLAUDE_SKILLS="$HOME/.claude/skills"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
CODEX_SKILLS="$CODEX_HOME_DIR/skills"

skill_sources() {
  if [[ -n "$SOURCE_DIR" ]]; then
    printf '%s\n' "$SOURCE_DIR"
    return
  fi

  printf '%s\n' "${BUNDLED_SKILLS[@]}"
}

validate_sources() {
  while IFS= read -r skill_dir; do
    [[ -n "$skill_dir" ]] || continue
    if [[ ! -f "$skill_dir/SKILL.md" ]]; then
      echo "error: $skill_dir does not look like a skill folder; missing SKILL.md" >&2
      exit 1
    fi
  done < <(skill_sources)
}

install_into() {
  local target_root="$1"
  local label="$2"

  mkdir -p "$target_root"

  while IFS= read -r skill_dir; do
    [[ -n "$skill_dir" ]] || continue
    local skill_name
    local target_dir

    skill_name="$(basename "$skill_dir")"
    target_dir="$target_root/$skill_name"

    rm -rf "$target_dir"
    cp -R "$skill_dir" "$target_dir"
    echo "installed $label skill: $target_dir"
  done < <(skill_sources)
}

install_claude() {
  install_into "$CLAUDE_SKILLS" "Claude Code"
}

install_codex() {
  install_into "$CODEX_SKILLS" "Codex"
}

validate_sources

case "$MODE" in
  both)
    install_claude
    install_codex
    ;;
  claude)
    install_claude
    ;;
  codex)
    install_codex
    ;;
esac

echo "restart Claude Code or Codex to load the updated skills"
