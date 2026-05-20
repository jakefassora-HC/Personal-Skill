#!/usr/bin/env bash
set -euo pipefail

MODE="both"
SOURCE_DIR="skills/pilot"

usage() {
  cat <<'USAGE'
Usage: ./install.sh [--both|--claude|--codex] [--source PATH]

Installs the pilot skill for Claude Code and/or Codex.

Options:
  --both          Install for Claude Code and Codex (default)
  --claude        Install for Claude Code only
  --codex         Install for Codex only
  --source PATH   Skill folder to install (default: skills/pilot)
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

if [[ ! -f "$SOURCE_DIR/SKILL.md" ]]; then
  echo "error: $SOURCE_DIR does not look like a skill folder; missing SKILL.md" >&2
  exit 1
fi

CLAUDE_SKILLS="$HOME/.claude/skills"
CLAUDE_TARGET="$CLAUDE_SKILLS/pilot"
CODEX_SKILLS="$HOME/.agents/skills"
CODEX_TARGET="$CODEX_SKILLS/pilot"

install_claude() {
  mkdir -p "$CLAUDE_SKILLS"
  rm -rf "$CLAUDE_TARGET"
  cp -R "$SOURCE_DIR" "$CLAUDE_TARGET"
  echo "installed Claude Code skill: $CLAUDE_TARGET"
}

install_codex() {
  mkdir -p "$CODEX_SKILLS"

  if [[ -d "$CLAUDE_TARGET" ]]; then
    rm -rf "$CODEX_TARGET"
    ln -sfn "$CLAUDE_TARGET" "$CODEX_TARGET" 2>/dev/null || cp -R "$CLAUDE_TARGET" "$CODEX_TARGET"
  else
    rm -rf "$CODEX_TARGET"
    cp -R "$SOURCE_DIR" "$CODEX_TARGET"
  fi

  echo "installed Codex skill: $CODEX_TARGET"
}

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

echo "restart Claude Code or Codex to load the updated pilot skill"
