---
name: project-gate-needs-hugo-and-theme
description: The WSL clone had no hugo binary and an uninitialized theme submodule, so scripts/check.sh and the Stop hook failed regardless of content; check both before relying on the gate
metadata:
  type: feedback
---

On 2026-10-26, the first content session in the new WSL clone (after the
`git on wsl` commits), `scripts/check.sh` failed with `hugo: command not found`,
and `git submodule status` showed `-cec082b8 themes/hugo-book`: the theme had
never been checked out. The content half of the gate (`check-content.py`) ran
fine; the build half could not run at all, so the Stop hook would block every
turn whatever the pages said.

The gate was run instead on a scratch copy: `rsync` of the working tree minus
`.git`, `public` and `themes`; Hugo 0.159.0 extended downloaded from the GitHub
release and checked against `hugo_0.159.0_checksums.txt` (0.159.0 is what
`.github/workflows/check.yml` pins); the theme cloned at the submodule commit;
then `PATH=<hugo dir>:$PATH CLAUDE_PROJECT_DIR=<copy> scripts/check.sh`.
`CLAUDE_PROJECT_DIR` has to be overridden, or check.sh `cd`s back into the
real repo.

**Why:** the hook's failure message looks like a content failure, and nothing
in the session says the environment is incomplete until the build line is
read.

**How to apply:** at the start of a content session run `command -v hugo` and
`git submodule status`. If either is missing, tell the user in one line that
the gate cannot build here (the fix is installing Hugo extended at the CI
version and `git submodule update --init`), and verify on a scratch copy as
above in the meantime. Related: [[project-hugo-quiet-hides-errors]],
[[project-forward-links-block-the-turn]].
