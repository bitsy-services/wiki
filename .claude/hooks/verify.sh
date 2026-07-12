#!/usr/bin/env bash
#
# Stop hook: closes the verification loop.
#
# Rules in .claude/rules/ are advisory — the model may or may not follow them.
# This makes the checkable subset deterministic: the turn cannot end while the
# site is broken. Without it, "looks done" is the only completion signal and the
# human becomes the verification loop.
set -uo pipefail

input=$(cat)

# Claude is already continuing because of this hook — let it stop, or we spin.
if [ "$(printf '%s' "$input" | jq -r '.stop_hook_active // false')" = "true" ]; then
  exit 0
fi

root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"

if out=$("$root/scripts/check.sh" 2>&1); then
  exit 0
fi

jq -nc --arg out "$out" '{
  decision: "block",
  reason: ("scripts/check.sh is failing, so this work is not done. Fix every problem below and re-run it — do not stop while it is red.\n\n" + $out)
}'
exit 0
