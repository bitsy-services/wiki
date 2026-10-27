---
name: global-checks-judge-the-visible-command
description: Permission checks judge the command they can see; an opaque script doing git moves or deletions is refused where the same work as explicit commands goes through
metadata:
  type: feedback
---

Consolidates two Gen 0 observations (`bulk-moves-explicit-git-mv`, and a
2026-10-26 refusal of `rm` inside `bash -c`) on 2026-10-26. Both are one
mechanism: Claude Code's safety checks and the auto-mode classifier decide on
the text of the command, and anything they cannot read through is treated as
the worst case.

- **Git moves in a script.** A scratchpad migration script that called
  `git mv` through `subprocess` was denied ("Modify Shared Resources"). The
  same fifty moves as eleven explicit `git mv src1 src2 ... destdir/` commands
  went through without a prompt, and the content half ran fine as an inline
  Python heredoc.
- **A removal inside `bash -c`.** A test command that reset scratch folders
  with `rm -rf $T/home/.claude ...` before a `bash -c '...'` block was refused
  by the built-in removal check, which "could not check the script for
  dangerous removals". The same test in a freshly named folder, with no `rm`,
  ran at once.

**Why:** a check that cannot see what a script does has to assume the
worst, and a deletion whose target is a shell variable could expand to `/`.
Each explicit command is reviewable and matchable by a permission rule, which
is what `.claude/rules/always.md` asks for anyway.

**How to apply:** for a restructure, run explicit `git mv` commands (several
sources, one target directory, is one command) and keep file rewrites in an
inline heredoc; rewrite links *before* writing aliases, as
`wiki-taxonomy.md` step 5 says. For test fixtures, create a new folder with a
fresh name per run in place of deleting the old one, and keep `rm` out of
`bash -c` strings and compound commands. Related:
[[global-permission-and-config-hygiene]].
