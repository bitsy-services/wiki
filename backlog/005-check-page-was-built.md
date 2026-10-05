# 005 — Make the gate notice a page Hugo did not build

- **Priority:** P1 (the gate passes while a linked page is missing from the site)
- **Status:** open

## Problem

`scripts/check-content.py` resolves every `/wiki/...` link against the source
tree under `content/`. It never looks at `public/`. A page that exists as a
source file and is dropped by Hugo therefore satisfies every inbound link, the
gate is green, and the URL 404s in production.

This happened on 2026-10-05. `content/wiki/ai/verbal-tics/claude.md` sat beside
a directory-scoped `content/wiki/ai/verbal-tics/CLAUDE.md`. Hugo folds filename
case, so the two collided, and with `ignoreFiles = ['CLAUDE\.md$']` in
`hugo.toml` neither was rendered. `public/wiki/ai/verbal-tics/` contained
`mitigation/` and `by-application/` and no `claude/`, five pages linked to
`/wiki/ai/verbal-tics/claude`, and `scripts/check.sh` printed `OK`. It was found
by listing `public/` by hand. The page was renamed `anthropic-claude.md`; the
blind spot is still there.

## Proposed fix

1. In `scripts/check-content.py`, after a link target resolves to a source
   file, also require the built page: `public/<url>/index.html`. Report a
   missing one as `link: target exists in content/ but was not built`.
   `scripts/check.sh` already runs `hugo --destination public` first, so the
   output is fresh when the checker runs.
2. Add a direct check for the cause seen so far: two entries in one content
   directory whose names are equal ignoring case.
3. Decide what the checker does when `public/` is absent (running
   `check-content.py` alone). Failing with "build first" is safer than skipping.

## Files

- `scripts/check-content.py`
- `CLAUDE.md` (the "Never name a page `claude.md`" bullet can then say the gate
  enforces it)

## Verification

- `scripts/check.sh` is green on the current tree.
- Temporarily copying any page to `claude.md` in a directory that holds a
  `CLAUDE.md`, and linking to it, makes `scripts/check.sh` fail. Remove the copy
  afterwards.
- A draft page (`draft: true`) that is linked to also fails, which is correct:
  the production build does not render drafts.
