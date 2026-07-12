---
description: Internal linking strategy and stub creation
---

# Wiki Linking

Internal links are machine-checked by `scripts/check-content.py`: every
`/wiki/...` target must resolve to a real page, and every `#anchor` must match a
real heading on that page. Hugo does **not** validate these — it renders a dead
link happily — so `scripts/check.sh` is the only thing standing between a
rename and a 404 in production. It has already caught one.

This means the stub rule below is enforced, not merely encouraged: link to a
page that doesn't exist and the check fails until you create it.

- Articles should be richly linked internally. Links in body text should point to other wiki pages, not external sites.
- When a link target doesn't exist yet, create a stub page with appropriate frontmatter and a body containing external links (docs, Wikipedia, blog posts) on the same topic.
- Link domain-specific terms on first mention. Only link the first occurrence per page — subsequent mentions can be plain text.
- If the concept is a narrow subtopic of a broader page, deep-link to the relevant section. Anchors are slugified headings: lowercase, punctuation dropped, each space becomes a dash (so `Tool design — the ACI` is `#tool-design--the-aci`, with two dashes).
- Renaming or moving a page breaks every inbound link. After a move, run `scripts/check.sh` and fix what it reports.
