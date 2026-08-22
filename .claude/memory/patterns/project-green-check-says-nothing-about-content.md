---
name: project-green-check-says-nothing-about-content
description: scripts/check.sh validates structure, not prose — and the durable fix is to move a content rule into the checker, not to remember harder
metadata:
  type: feedback
---

Consolidates two Gen 0 observations (`project-argument-pages-need-repeated-review`,
`project-check-misses-write-tool-artifacts`) plus the 2026-08-22 acronym sweep.

`scripts/check.sh` proves the site builds and that links, anchors, fences and
frontmatter are well-formed. It says nothing about whether the prose is prose,
whether the claims are true, or whether a reader can follow it. Three failures
have now landed in that gap:

- An essay's central historical claim was false, and survived two review rounds
  before a third caught it.
- Literal `</content>` tags from a Write call shipped as page text, green check
  and all.
- ~200 acronyms were used across the wiki with no expansion anywhere — `EIP`
  and `EVM` on 14 pages each, `NFT` on 10 — while every check passed.

**Why:** the checker was built around the one failure mode Hugo silently allows
(dead internal links). Everything else in `.claude/rules/` stayed advisory, and
advisory rules decay across sessions because nothing re-reads them mid-draft.

**How to apply:** when a content rule has been violated more than once, the fix
is a check, not a stronger rule. The acronym case is the worked example — an
explicit registry (`scripts/acronyms.txt`) plus a per-page check turns
"remember to expand acronyms" into a build failure, and an *unregistered*
acronym fails too, so a new one forces the decision instead of slipping through.
Prefer that shape: a small allow-list the author must edit deliberately, over a
heuristic that guesses. For what a check still can't reach — truth, tone,
readability — use `wiki-reviewer`, and keep going until a round comes back
clean. Related: [[project-harness-invariants]].
