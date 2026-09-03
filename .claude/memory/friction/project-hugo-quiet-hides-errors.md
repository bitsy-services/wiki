---
name: project-hugo-quiet-hides-errors
description: hugo --quiet suppresses ERROR lines, so probing Hugo behaviour with it produces false "works fine" results
metadata:
  type: feedback
---

`hugo --quiet` hides `ERROR` output as well as the build summary. A probe loop that
runs `hugo --quiet` and greps stdout for an error string reports every case as
passing, including cases where the build actually failed with exit 1.

This produced a wrong claim while researching the Hugo section: a sweep over the
embedded shortcodes said `gist` and `twitter` were available, when both were
removed in Hugo v0.156 and fail the build. The `wiki-reviewer` subagent caught it.

**Why:** `scripts/check.sh` uses `--quiet` and inspects the exit status, which is
correct for a gate. Copying that invocation into an exploratory probe is not —
a probe reads the output, and `--quiet` empties it.

**How to apply:** when probing Hugo behaviour in a scratch site, run plain `hugo`
and read stderr, or test `$?` directly. Never grep the output of a `--quiet` run.
Related: [[project-green-check-says-nothing-about-content]].
