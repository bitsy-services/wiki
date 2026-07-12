---
name: project-harness-invariants
description: Non-obvious facts about this repo's Hugo setup and agent config that are easy to get wrong
metadata:
  type: project
---

Two traps in this repo that cost real time to discover (2026-07-12), both of
which look fine and are silently wrong.

**1. Hugo does not validate internal links.** Every link in this wiki is a plain
absolute path (`/wiki/defi/amm`), not a Hugo `ref`/`relref` shortcode. Hugo
renders a link to a nonexistent page without warning, and the build stays green.
Six links to `/wiki/defi/chainlink-automation` had been 404ing in production
since the page moved under `chainlink/`. `scripts/check-content.py` is the only
thing that catches this — a green `hugo` build means nothing about link
integrity. Run `scripts/check.sh`, not `hugo`.

Its anchor slugifier is calibrated against Hugo's real output and verified
identical across all 142 pages. The subtle part: Hugo does **not** collapse
whitespace runs, so a heading with an em dash (`Tool design — the ACI`) becomes
`#tool-design--the-aci` with *two* dashes. If you "fix" that to one dash you
will break a working link.

**2. The `.claude/rules/` scoping field is `paths:`, not `globs:`.** Five rule
files used `globs:`, which Claude Code does not recognize — so rules the author
believed were scoped to `content/wiki/**` were in fact loading into *every*
session's always-on context. An unrecognized frontmatter key fails open and
silently: the rule still loads, it just never scopes. If you intend a rule to be
conditional, write `paths:` as a YAML list and confirm it is absent from the
always-on block at the next session start.

The theme is also worth knowing: `hugo-book`'s `single.html` and `list.html` are
stubs, so it renders **no page-level `<h1>` at all** — 140 of 141 pages had none.
`layouts/single.html` and `layouts/list.html` in this repo override the `main`
block to render the frontmatter title as the h1. That is why the "no `# H1` in
the body" rule exists; before those overrides the rule's stated rationale was
simply false.

Related: [[global-permission-and-config-hygiene]].
