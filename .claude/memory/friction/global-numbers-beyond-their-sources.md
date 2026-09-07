---
name: global-numbers-beyond-their-sources
description: On research-heavy pages the recurring error is stating a figure more precisely or more broadly than the source supports; verify every number against a primary source or drop it
metadata:
  type: feedback
---

Writing the `ai/pastiche/` section (2026-09-07) took six `wiki-reviewer` rounds.
Every finding of substance across those rounds was the same shape: a claim
asserted more strongly than its source allowed. Not invention — each number came
from a real paper — but a drift toward precision and scope the evidence did not
carry.

The instances, because the pattern only shows in aggregate:

- Per-thousand-word rates for *upon* in Hamilton and Madison, and "odds of
  thousands to one" — both written from recall, neither in any reachable source.
- Federalist 55's odds given as "about 100 to 1" from a teaching tutorial. A
  reviewer countered with 240:1, also uncited. Neither was verifiable; the
  number came out.
- The Cubist-motif line attributed to *Franklin Mint*. Extracting the opinion
  showed it is not there — it traces to *Dave Grossman Designs* via *Steinberg*.
- Yang & Carpuat's table presented as descriptors beating exemplars. There is no
  exemplar-only baseline in it, and the paper attributes the gap to open-ended
  descriptor generation. The comparison was descriptors against descriptors.
- A conclusion ("constrained descriptors steer more reliably") contradicted by
  the table printed six lines above it, where the constrained variant loses
  0.347 to 0.554 on exactly that metric.
- Mikros's imitation count halved: two prompting conditions per author makes
  eighteen per author, not nine.
- An index sentence calling the evidence base "stylometric and forensic" when
  three of its sources are code generation, style transfer and persona
  simulation — the same overreach one level up, in the summary.

**Why:** a number recalled rather than read *feels* identical to one that was
read, and the feeling is what gets written. Prose fluency is orthogonal to
citation accuracy, so nothing in the drafting experience flags the difference.
`scripts/check.sh` cannot see any of it — see
[[project-green-check-says-nothing-about-content]].

**How to apply:**

- Before writing a figure, name where it came from. If the answer is "I know
  this," it is unverified: fetch it or drop it. Crossref
  (`api.crossref.org/works/<doi>`) resolves DOI metadata and does not bot-block,
  which the publishers mostly do.
- Prefer dropping an unsourceable number to softening it. "About 100 to 1" reads
  as sourced; "the narrowest margin of the twelve" is checkable and true.
- Extract PDFs rather than trusting a summary of them. Two attributions
  (Cubist, `Franklin Mint`) survived a search-result summary and died on
  `pypdf` extraction of the actual opinion.
- Check each conclusion against the table on the same page. Two findings were
  claims refuted by numbers already printed feet away.
- **A partial correction is its own defect.** Fixing the one sentence a reviewer
  named, while the lede, section opener and two recommendations still asserted
  the retracted claim, left the page self-contradictory — worse than before the
  fix. When a claim is retracted, grep the page set for every place it is
  restated, including the parent index.

Related: [[project-harness-invariants]].
