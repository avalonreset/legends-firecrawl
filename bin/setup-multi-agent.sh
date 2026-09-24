#!/usr/bin/env bash
set -euo pipefail
repo="$(cd "$(dirname "$0")/.." && pwd)"
skill="$repo/skills/legends-firecrawl"
for root in "$HOME/.grok/skills" "$HOME/.codex/skills" "$HOME/.claude/skills" "$HOME/.gemini/skills"; do
  mkdir -p "$root"
  ln -sfn "$skill" "$root/legends-firecrawl"
done
echo "PASS house skill linked; vendor integrations and MCP were not installed."

