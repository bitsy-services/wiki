---
name: project-argument-pages-need-repeated-review
description: On wiki pages that argue an empirical thesis, first drafts overstate and one wiki-reviewer round is not enough
metadata:
  type: feedback
---

Writing `content/wiki/ai/llm/why-scale-worked.md` (2026-07-16) took **three**
`wiki-reviewer` rounds, and every round found a substantive factual error — not
style nits. The pattern is specific enough to plan around.

- **Round 1** killed the page's central historical claim. The draft said the
  transformer removed two bottlenecks, human labelling and serial training. The
  label one was false: recurrent models were already *language* models, so their
  labels were already free. Self-supervision dates to 2003.
- **Round 2** found an error *inside the round-1 fix*. The repaired thesis —
  "turns extra hardware into a bigger model" — was also false (a ~2B-param LSTM
  LM predates GPT-2). The true claim is about tokens/second, not size.
- **Round 3** found the round-2 evidence didn't support its own claim: that
  1.8B LSTM is ~1.6B of vocabulary lookup tables over a 793K-word vocab; its
  recurrent core is ~200M. The tell is that a *512-unit* model in the same table
  lists at 0.82B.

**Why:** these pages are persuasive essays, and a tidy argument creates pressure
to reach for the fact that completes the rhythm. Mechanism pages don't have this
problem — they describe something checkable that either matches the code or
doesn't. Argument pages assert about history, other architectures, and the
field, none of which `scripts/check.sh` can see. A green check means nothing
about whether the claims are true.

**How to apply:** on any page whose job is to argue rather than describe, budget
review rounds until one comes back clean — do not treat the first green check or
the first review as done. Re-review after applying fixes, scoped explicitly to
the newly written prose, since that's where the next error lives. Prefer
qualitative evidence over a headline number (cite the LSTM's 8192-unit width,
not its inflated param count): a parameter count that includes vocab tables
isn't measuring capacity. And when a correction lands, check the *summary*
paragraph too — round 2's error survived in the first paragraph, which is the
one paragraph a reader may stop at, long after the body had been fixed.

## Confirmed again, and a second error class (2026-08-22)

The `content/wiki/economics/finance/regulation/` section — a page on the Bank
Secrecy Act plus six supporting pages — took **four** `wiki-reviewer` rounds to
come back clean. Same shape: every round found substantive errors, and rounds 2
and 3 found errors *inside the previous round's fixes* (a corrected sentence
introduced a wrong count; a hedge on one page then contradicted an unhedged
claim on a page it linked to).

On statute/regulation pages the dominant error class is **scope**, not fact.
Citations, dates, form numbers, and dollar thresholds came back almost entirely
correct across seven pages. What was wrong, repeatedly, was *who a rule binds*:
the draft applied the CIP and CDD rules to money services businesses, which they
do not reach, and did so on two pages at once. The failure mode is assuming a
rule you've correctly described applies to the entity you happen to be writing
about.

**How to apply:** when a page asserts a legal or regulatory obligation, review
the *scope* clause separately from the citation — ask which defined category the
rule names, and whether the subject of the sentence is in it. And when a claim
gets hedged on one page, grep for the same claim elsewhere; a hedge that isn't
propagated leaves the wiki contradicting itself across a link.

Related: [[project-harness-invariants]] — the same theme, that a green build
says nothing about correctness.
