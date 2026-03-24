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
- Link domain-specific terms and concepts that a general reader may not know. On first mention, wrap the term in a markdown link to either a local wiki page (e.g. `[AMM](/wiki/defi/amm)`) or an external reference such as Wikipedia (e.g. `[intent-based architecture](https://en.wikipedia.org/wiki/Intent-based_networking)`). If the concept is a narrow subtopic of a broader page, deep-link to the relevant section (e.g. `[fee tiers](https://docs.uniswap.org/concepts/protocol/fees#fee-tiers)`). Only link the first occurrence per page — subsequent mentions can be plain text. Prefer local wiki pages when one exists or is planned; fall back to Wikipedia or official documentation.
