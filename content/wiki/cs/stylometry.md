---
title: "Stylometry"
weight: 35
---

Stylometry attributes a text to an author by measuring features the author was not choosing. Not vocabulary, not subject matter, not the turns of phrase a reader would quote — the rate at which a writer reaches for *upon* rather than *on*, or *while* rather than *whilst*, counted across thousands of words. Those rates are stable within a writer and different between writers, and they survive the writer's conscious attempts to change them, which is the property the whole field rests on.

## The Federalist problem

Twelve of the eighty-five Federalist Papers — numbers 49 through 58, 62 and 63 — were claimed by both Alexander Hamilton and James Madison, and a century and a half of historical argument had not settled them. Frederick Mosteller and David Wallace settled them in 1963 by counting function words.

The obvious measurements were useless, and had been tried. Mosteller and Frederick Williams measured average sentence length across the papers whose authorship was never in doubt and got 34.59 words and 34.55 words — both unusually long, and four hundredths of a word apart. Which figure belongs to which man is not worth recording, which is the point: the feature a reader would name first, and the one an imitator would reach for first, carries no information about who is writing.

So Mosteller and Wallace discarded every word that carried subject matter and kept a few dozen high-frequency function words — *by*, *to*, *from*, *upon*, *whilst* — chosen because their rate does not depend on what the essay is about. Those rates do separate the two men, and widely. A Bayesian model over them assigned all twelve disputed papers to Madison, Federalist 55 by the narrowest margin of the twelve.

The historical conclusion has held. The methodological conclusion mattered more: the words that identify a writer are the ones that carry no information about the topic. Content words track the subject and shift when the subject shifts. Function words track the writer.

## Why the signal sits where nobody is looking

A function word is grammatical scaffolding. A writer choosing between *begin to write* and *begin writing* is not making a stylistic decision in any sense they could report — the choice is made below the level at which writing feels like choosing, at the rate of several per sentence, in a distribution too fine-grained to hold in mind.

That inaccessibility is what makes the measurement work, and it has two consequences that run in opposite directions.

The useful one is robustness. A writer who sets out to change their style will change the things they can perceive: sentence length, vocabulary, imagery, punctuation habits. The function-word profile is not on that list, because it was never available to inspection in the first place.

The awkward one is that a writer cannot describe their own style accurately. Asked what makes their prose theirs, an author will name the perceptible features — the short sentences, the em-dashes, the refusal of adverbs. Those are real and they are also the features that any competent imitator can copy in an afternoon. The part that actually distinguishes the author is the part they cannot see well enough to report, which is a problem for anyone trying to build an imitation out of a description. [Pastiche produced by a language model](/wiki/ai/pastiche) runs into that wall from the other side.

## Burrows's Delta

John Burrows gave the field its standard distance measure in 2002. Delta takes the *n* most frequent words in a corpus — typically 100 to 1,000, and overwhelmingly function words at that frequency — and builds a profile for each text:

```text
for each word w in the n most frequent:
    f(w)   = relative frequency of w in this text
    z(w)   = (f(w) - mean over the corpus) / standard deviation over the corpus

Delta(A, B) = mean over w of | z_A(w) - z_B(w) |
```

The z-score is what makes it work. Word frequencies span orders of magnitude — *the* appears perhaps 60 times per thousand words, *whilst* perhaps 0.1 — so an unstandardized comparison would be decided entirely by the handful of commonest words. Standardizing each word against its own variance across the corpus gives every feature equal weight, so a small deviation in a rare function word counts as much as a small deviation in *the*.

Delta needs no training data beyond a reference corpus, no parsing, and no knowledge of the language's grammar. It has been applied unchanged to English, German, Polish, Latin and medieval Chinese. That combination of simplicity and portability is why it remains the benchmark against which newer attribution methods are reported.

## What it is used for

**Disputed authorship** is the classical application and still the visible one — contested plays, anonymous novels, pseudonymous political tracts.

**Forensic linguistics** applies the same statistics to ransom notes, threatening emails and disputed confessions, where the reference corpus is a suspect's known writing and the output is evidence. The forensic setting adds a requirement the literary one does not have: a court needs a likelihood ratio, not a nearest neighbour, so forensic methods report how much more probable the evidence is under same-author than under different-author.

**Authorship verification** is the closed-form version of the question: given two texts, one author or two? It is the framing a language model's imitation gets tested against, and [the imitation loses](/wiki/ai/pastiche/authorship-survives).

## Check yourself

Take two authors with plenty of public-domain text — Austen and Dickens will do — and compute Delta over the 150 most frequent words, holding out a novel from each. The held-out books should land nearest their own author. Then repeat with the 150 most frequent *content* words instead, having stripped the function words out. Accuracy should fall, and the errors should be topical: the seafaring novel matching the other author's seafaring novel. That failure is the positive result. It shows the attribution was never running on subject matter.

## Related

- [Pastiche](/wiki/ai/pastiche) — what happens when a language model is asked to write in a named author's style, and which of these features it reproduces.
- [Authorship survives imitation](/wiki/ai/pastiche/authorship-survives) — the verification question applied to model output.
- [Entity addressing](/wiki/cs/entity-addressing) — identity established by intrinsic properties rather than by a label, the same move in a different domain.

## Further reading

- Mosteller & Wallace, [Inference in an Authorship Problem: A Comparative Study of Discrimination Methods Applied to the Authorship of the Disputed Federalist Papers](https://doi.org/10.1080/01621459.1963.10500849), *Journal of the American Statistical Association* 58(302), 275–309 (1963)
- Burrows, ['Delta': a Measure of Stylistic Difference and a Guide to Likely Authorship](https://doi.org/10.1093/llc/17.3.267), *Literary and Linguistic Computing* 17(3), 267–287 (2002)
- Argamon, [Interpreting Burrows's Delta: Geometric and Probabilistic Foundations](https://doi.org/10.1093/llc/fqn003), *Literary and Linguistic Computing* 23(2), 131–147 (2008)
- Evert et al., [Understanding and explaining Delta measures for authorship attribution](https://doi.org/10.1093/llc/fqx023), *Digital Scholarship in the Humanities* 32(suppl_2), ii4–ii16 (2017)
- Eder, Rybicki & Kestemont, [Stylometry with R: a package for computational text analysis](https://doi.org/10.32614/RJ-2016-007), *The R Journal* 8(1), 107–121 (2016)
- Programming Historian — [Introduction to stylometry with Python](https://programminghistorian.org/en/lessons/introduction-to-stylometry-with-python)
