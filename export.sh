#!/usr/bin/env bash
# export.sh — copy the live skills from ~/.claude/skills back into this repo's skills/ folder.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
for s in tibetan-translate tibetan-verse tibetan-citations tibetan-dharmamitra; do
  rm -rf "$HERE/skills/$s"
  cp -R "$HOME/.claude/skills/$s" "$HERE/skills/$s"
  find "$HERE/skills/$s" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
done
echo "exported. git status:"; cd "$HERE" && git status --short 2>/dev/null || echo "(not a git repo yet: run git init)"
