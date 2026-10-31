---
name: project-gate-needs-hugo-and-theme
description: The WSL clone had no hugo binary, an uninitialized theme submodule and no jq, so scripts/check.sh fails regardless of content and the Stop hook fails open; check all three before relying on the gate
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

**Still true on 2026-10-30** (GitHub team-access pages), with a third gap:
`jq` is not installed either, and `.claude/hooks/verify.sh` uses it both to
read `stop_hook_active` and to print the `block` decision. With `jq` missing
the hook runs check.sh, fails to print anything, and exits 0, so it never
blocks: in this clone the gate runs only when it is run by hand. A reusable
version of the scratch-copy run was kept as a script (rsync both trees, then
check.sh with `PATH` and `CLAUDE_PROJECT_DIR` overridden); it took a minute to
rebuild.

**How to apply:** at the start of a content session run
`command -v hugo jq` and `git submodule status`. If any is missing, tell the
user in one line that the gate cannot build here, or that the Stop hook cannot
block (the fix is installing Hugo extended at the CI version and `jq`, and
`git submodule update --init`), and verify on a scratch copy as above in the
meantime, running it yourself before every turn end. Related: [[project-hugo-quiet-hides-errors]],
[[project-forward-links-block-the-turn]].
