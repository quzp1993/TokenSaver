#!/usr/bin/env bash
# TokenSaver setup — one command wires the whole pipeline:
#   input   -> rtk (installed + global hook)  — the compression engine
#   output  -> token-saver skill (terse answers)
#   context -> token-saver SessionStart ruleset + lean CLAUDE.md
# Like prokka calling prodigal/hmmer/aragorn, TokenSaver orchestrates rtk
# instead of reimplementing it.
set -e

echo "== TokenSaver setup =="

# 1. rtk — input compression engine
if command -v rtk >/dev/null 2>&1; then
  echo "rtk: found ($(rtk --version 2>/dev/null | head -1))"
else
  echo "rtk: installing..."
  if command -v winget >/dev/null 2>&1; then
    winget install rtk-ai.rtk --scope machine --silent --accept-package-agreements --accept-source-agreements
  elif command -v brew >/dev/null 2>&1; then
    brew install rtk
  else
    curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
  fi
fi
rtk init -g 2>&1 | tail -3

# 2. TokenSaver plugin — output + context levers
claude plugin marketplace add quzp1993/TokenSaver 2>&1 | tail -1
claude plugin install token-saver@token-saver 2>&1 | tail -1

echo ""
echo "Done. Restart Claude Code."
echo "Verify: rtk gain          # input savings"
echo "        claude plugin list # token-saver enabled"
