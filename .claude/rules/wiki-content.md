---
description: Rules for wiki page structure and formatting
---

# Wiki Content Rules

These add to `kit/wiki-content.md`. `scripts/check-content.py` enforces the ones
marked *(checked)*, and the kit's no-`# H1` rule too; run `scripts/check.sh`
before you consider a page done.

- Every fenced code block must declare a language, so it gets syntax highlighting. Use `text` for formulas, ASCII diagrams, and directory trees. *(checked)*
- Frontmatter needs a `title`; `weight`, if present, must be an integer. *(checked)*
- Expand every acronym on first use on **each page** that uses it — `automated
  market maker (AMM)` — or link it to the page that expands it. Per-page, not
  per-wiki: a reader landing from a search engine has not read the other pages.
  The expansion has to sit *beside* the acronym; the same words elsewhere on the
  page do not define it, and the check enforces the proximity.
  Acronyms live in `scripts/acronyms.txt`; using one that isn't listed fails the
  check, so a new acronym forces the choice (expand it, or register it as
  common knowledge with `-`). *(checked)*
- Keep deployed-address tables either complete (full copy-pasteable addresses) or omit them in favor of a link to the canonical source. Truncated addresses serve no purpose.
- Order "pitfalls" and "gotchas" sections by severity — fund-loss risks before revert-only issues.
