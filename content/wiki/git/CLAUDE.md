# Git Section — Agent Instructions

These instructions apply when developing pages in `content/wiki/git/`. They are picked up automatically when you work on files in this directory.

## Commit whole, not partial

When committing work in this repository, prefer workflows that **commit all changes not excluded by `.gitignore`**, rather than hand-picking individual files or hunks.

- Default to `git add -A` (or `git add .` from the repo root) so every tracked and newly-created, non-ignored file is staged together.
- **Avoid partial commits** — staging only some of the files touched in a unit of work. Partial commits leave the tree in a state that may not build or render, break `git bisect`, and produce commits whose message does not match their contents.
- Before committing, run `git status` and confirm that everything shown as modified/untracked is genuinely meant to be in this commit. If something should *not* be committed, the correct fix is to add it to `.gitignore` (or remove it), not to selectively leave it unstaged.
- If a change truly belongs in a separate commit, make it a separate, self-contained change first — don't split one logical edit across a "committed half" and an "uncommitted half".

The goal: every commit is a complete, coherent snapshot. There should be no surprise uncommitted edits left behind in the working tree after you commit.
