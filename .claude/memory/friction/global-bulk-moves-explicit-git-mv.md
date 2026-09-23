---
name: bulk-moves-explicit-git-mv
description: The auto-mode classifier denies a scratchpad script that shells out to git; explicit `git mv` commands with multiple sources go through and match the one-command rule
metadata:
  type: feedback
---

A migration script written to the scratchpad that called `git mv` through
`subprocess` was denied by the auto-mode classifier ("Modify Shared Resources").
The same fifty moves as eleven explicit `git mv src1 src2 ... destdir/`
commands went through without a prompt, and the content half of the script
ran fine as an inline Python heredoc.

**Why:** the classifier judges the visible command. An opaque script from
outside the repo doing git operations reads as a shared-resource change; each
explicit command is reviewable and matchable by a permission rule, which is
what `.claude/rules/always.md` asks for anyway.

**How to apply:** for a restructure, do the moves as explicit `git mv` commands
(multiple sources, one target directory — that is one command, not a compound)
and keep the file rewrites in an inline heredoc. Rewrite links *before* writing
aliases, or the rewrite clobbers the aliases; `wiki-taxonomy.md` step 5 now
says so.
