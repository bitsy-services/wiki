#!/usr/bin/env bash
#
# The definition of done for this repo. Exits non-zero if the site does not
# build or the content violates .claude/rules/. Wired to a Stop hook in
# .claude/settings.json, so an agent cannot finish a turn with this failing.
#
# Run it yourself with: scripts/check.sh
set -uo pipefail

cd "${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}" || exit 1

status=0

if ! build_out=$(hugo --quiet --destination public 2>&1); then
  echo "hugo build FAILED:"
  echo "$build_out"
  status=1
elif [ -n "$build_out" ]; then
  # Hugo exits 0 on warnings; surface them but don't fail the gate.
  echo "hugo build warnings:"
  echo "$build_out"
fi

if ! check_out=$(python3 scripts/check-content.py 2>&1); then
  echo "content check FAILED:"
  echo "$check_out"
  status=1
fi

if [ "$status" -eq 0 ]; then
  echo "OK — site builds and content passes all checks."
fi

exit "$status"
