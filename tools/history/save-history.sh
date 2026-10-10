#!/usr/bin/env bash
# Copy this project's local Claude Code transcripts into ai-history/raw/ (git-ignored).
# Sessions run in the cloud (claude.ai/code) or on other machines are not here: export those from the session itself.
set -euo pipefail
root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
key="$(printf '%s' "$root" | sed 's/[^A-Za-z0-9]/-/g')"
src="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/$key"
dst="$root/ai-history/raw"
mkdir -p "$dst"
if compgen -G "$src/*.jsonl" > /dev/null; then
  cp -p "$src"/*.jsonl "$dst"/
  for d in "$src"/*/; do [ -d "$d" ] && cp -rp "$d" "$dst"/; done
  echo "Copied $(ls "$dst"/*.jsonl | wc -l | tr -d ' ') transcript file(s), with their subagent and tool-result folders, to ai-history/raw/"
else
  echo "No transcripts found at $src"
fi
