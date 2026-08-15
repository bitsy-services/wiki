---
name: project-check-misses-write-tool-artifacts
description: scripts/check.sh passes on stray tool-call closing tags left at the end of a content file
metadata:
  type: feedback
---

When creating `content/wiki/ai/llm/bend.md` I let the literal text
`</content>` and `</invoke>` land at the end of the file — closing tags from the
Write tool call itself, written as page content. `scripts/check.sh` reported
green: the build succeeded, links resolved, fences and frontmatter were fine.
The garbage was only caught by re-reading the finished page.

**Why:** the checker validates structure (links, anchors, fences, frontmatter),
not that the prose is prose. A stray XML-ish tag is a valid paragraph as far as
Hugo and the checker are concerned, and it renders as literal text on the
published page. This is the same blind spot as
[[project-argument-pages-need-repeated-review]] — a green check says nothing
about content — but the failure mode is cruder and cheaper to catch.

**How to apply:** after writing a whole file with Write (as opposed to Edit),
read the last few lines back before running the check. Two candidate fixes worth
proposing if it recurs: a `check-content.py` rule rejecting lines matching
`^</?[a-z_]+>$` in page bodies, or a backlog item for the same. Do not rely on
`scripts/check.sh` to notice. (Written twice in one session, including into this
file — the habit is real, not hypothetical.)
