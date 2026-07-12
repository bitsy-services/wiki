---
description: Rules for wiki page structure and formatting
---

# Wiki Content Rules

Several of these are machine-checked by `scripts/check-content.py`; run
`scripts/check.sh` before you consider a page done.

- Do not add an `# H1` heading in the page body — `layouts/single.html` renders the frontmatter `title` as the page's h1. Start body content with `##` sections. *(checked)*
- Every fenced code block must declare a language, so it gets syntax highlighting. Use `text` for formulas, ASCII diagrams, and directory trees. *(checked)*
- Frontmatter needs a `title`; `weight`, if present, must be an integer. *(checked)*
- Introduce concepts before using them in code. If a parameter (fee tier, slippage, etc.) appears in an example, the explanation should come before or alongside the example, not in a later section.
- Keep deployed-address tables either complete (full copy-pasteable addresses) or omit them in favor of a link to the canonical source. Truncated addresses serve no purpose.
- Avoid repeating large boilerplate blocks across examples. Show the full pattern once, then show only the meaningful differences in subsequent examples.
- Order "pitfalls" and "gotchas" sections by severity — fund-loss risks before revert-only issues.
- Introduce concepts before using them in code. If a parameter (fee tier, slippage, etc.) appears in an example, the explanation should come before or alongside the example, not in a later section.
- Keep deployed-address tables either complete (full copy-pasteable addresses) or omit them in favor of a link to the canonical source. Truncated addresses serve no purpose.
- Avoid repeating large boilerplate blocks across examples. Show the full pattern once, then show only the meaningful differences in subsequent examples.
- Order "pitfalls" and "gotchas" sections by severity — fund-loss risks before revert-only issues.
