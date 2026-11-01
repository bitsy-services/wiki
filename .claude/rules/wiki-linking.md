---
description: How internal links and anchors are checked in this wiki
---

# Wiki Linking

These add to `kit/wiki-linking.md`, which says what to link and when to create
a stub.

Internal links are machine-checked by `scripts/check-content.py`: every
`/wiki/...` target must resolve to a real page, and every `#anchor` must match a
real heading on that page. Hugo does **not** validate these — it renders a dead
link happily — so `scripts/check.sh` is the only thing standing between a
rename and a 404 in production; after a move, run it and fix what it reports.
It has already caught one.

That makes the kit's stub rule enforced, not merely encouraged: link to a page
that doesn't exist and the check fails until you create it.

Anchors are slugified headings: lowercase, punctuation dropped, each space
becomes a dash, so `Tool design — the ACI` is `#tool-design--the-aci`, with two
dashes.
