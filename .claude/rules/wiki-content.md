---
description: Rules for wiki page structure and formatting
globs: content/wiki/**/*.md
---

# Wiki Content Rules

- Do not add an `# H1` heading in the page body — Hugo Book renders the frontmatter `title` as h1 already. Start body content with `##` sections.
- Introduce concepts before using them in code. If a parameter (fee tier, slippage, etc.) appears in an example, the explanation should come before or alongside the example, not in a later section.
- Keep deployed-address tables either complete (full copy-pasteable addresses) or omit them in favor of a link to the canonical source. Truncated addresses serve no purpose.
- Avoid repeating large boilerplate blocks across examples. Show the full pattern once, then show only the meaningful differences in subsequent examples.
- Order "pitfalls" and "gotchas" sections by severity — fund-loss risks before revert-only issues.
