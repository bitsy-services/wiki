---
title: "What Transfers and What Does Not"
weight: 20
---

A style is not one thing, and the parts of it come across a pastiche prompt at very different rates. The measurable summary is that the perceptible layer — how long the sentences run, how long the words are, what the punctuation does — moves in the right direction, and the layer underneath it does not move at all. George Mikros put numbers on both halves by having GPT-4o imitate Ernest Hemingway and Mary Shelley and then running the output through four independent [stylometric](/wiki/cs/stylometry) feature sets.

## The setup

Mikros generated 45 texts in five groups of nine: generic GPT-4o output with no style instruction, and imitations of each author under two conditions — a plain request naming the author, and in-context learning with a 15,000-word excerpt supplied. The reference texts were *The Old Man and the Sea* (26,663 tokens) and *Frankenstein* (75,143 tokens).

Four feature sets were computed independently, so that no single measurement decides the result: 74 textual-complexity and readability features including word and sentence lengths and several lexical-diversity indices; a 900-element profile of character bigrams, character trigrams and word unigrams; sentence embeddings; and a 115-feature psycholinguistic inventory.

A random-forest classifier separated genuine from generated text at 79.84% accuracy on the complexity features, 83.29% on the n-gram profile, 83.64% on embeddings and 84.03% on the psycholinguistic features. Four different views of the text, four ways of telling the difference, spanning 79.8 to 84.0.

## Sentence length: the right direction, the wrong distance

Hemingway and Shelley sit at opposite ends of English sentence rhythm, and the imitations did order them correctly.

| | Words per sentence | Characters per word |
| --- | --- | --- |
| Hemingway, original | 14.15 | 3.84 |
| GPT-4o as Hemingway | 12.95–13.47 | 4.29–4.49 |
| Shelley, original | 41.51 | 4.42 |
| GPT-4o as Shelley | 17.70–19.75 | 4.53–4.71 |

Asked for Hemingway, the model wrote shorter sentences than asked for Shelley. That is the correct direction and it is what "surface structure imitates well" means when people say it.

The distances tell a different story. Shelley's actual mean is 41.51 words per sentence; the imitation reached 19.75 at its longest, less than half. Hemingway's 14.15 came out at 12.95, which is close — and the closeness is worth being suspicious of, because both imitations landed inside the same narrow band of 12.95 to 19.75 words regardless of whether the target was 14 or 42. The word-length column does the same thing: targets spanning 3.84 to 4.42 characters, outputs spanning 4.29 to 4.71.

Mikros reports the Hemingway sentence length as a success and the Shelley sentence length as a failure. The reading the numbers also permit — and this one is inference rather than a claim the paper makes — is that neither is a result about Hemingway or Shelley. The outputs occupy a band the model would occupy anyway, and Hemingway scores well because Hemingway happens to live near it. Shelley does not, and no amount of asking moved the model out to meet her. That is [reversion to house style](/wiki/ai/pastiche/reversion-to-house-style) measured in words per sentence.

Note also that GPT-4o-as-Hemingway *overshot* Hemingway's word length by 12–17% — 4.29–4.49 characters against 3.84. Hemingway's plainness is the single most famous thing about his prose, and the imitation used longer words than he did.

## Lexical diversity runs backwards

Standardized type-token ratio (TTR) counts distinct words against total words over fixed-length windows. Hemingway's own prose scores **34.62**; GPT-4o imitating Hemingway scores **47.79 ± 0.95**, the highest value in the entire study, above generic model output and above both real authors. No story about the imitation being merely weak predicts a number above the target.

The imitation is not less various than Hemingway. It is a third more various, and consistently so, with a standard deviation under one point across nine independent generations.

That inversion locates the failure precisely. Hemingway's low type-token ratio is not an absence of vocabulary; it is repetition used deliberately, the same plain noun returning across a paragraph because returning to it is the effect. Asked to write like Hemingway, the model reached for a synonym at exactly the points where Hemingway reached for the same word again. It could not not-vary, because varying is what it does.

Mikros's own summary is that GPT-4o "captures some surface-level stylistic elements of the authors" but "struggles to fully replicate the depth and uniqueness of their stylometric signatures," and that while models "excel at mimicking surface-level attributes, such as vocabulary and sentence structure, replicating deeper stylistic elements... remains a significant challenge."

## What in-context learning buys

In-context learning helped modestly. Supplying 15,000 words of the real author produced "some improvement in stylistic alignment" but did "not bridge the gap to the original authors." That is worth separating from [the persona-simulation result](/wiki/ai/pastiche/generative-exaggeration), where richer source material made the output actively worse. On literary imitation, more of the author is a small positive; on simulating a specific person, it is a negative. The two findings are about different tasks and neither generalizes to the other.

## The pattern underneath

Ranking the features by how well they came across:

1. **Relative ordering of gross structure** — transfers. Shorter for Hemingway, longer for Shelley.
2. **Absolute values of gross structure** — compressed toward the model's own range, badly for any author far from it.
3. **Lexical diversity** — inverted, not merely missed.
4. **The function-word profile that actually identifies an author** — not addressed by the prompt at all, which is [why authorship verification still works](/wiki/ai/pastiche/authorship-survives).

The ordering is not arbitrary. It tracks how available each feature is to description. Sentence length is nameable, so a prompt can ask for it and the model can aim at it. Deliberate repetition is nameable but cuts against the model's default hard enough that naming it is not sufficient. The stylometric signature is not nameable by anyone, including the author.

## Check yourself

Take any writer with a distinctive rhythm and enough public-domain text to measure. Compute their mean sentence length, mean word length and standardized type-token ratio. Then generate a dozen imitations and compute the same three. Expect the ordering to be right and the magnitudes to be pulled toward the middle, and expect type-token ratio to come out high whatever the author's is. If your author is a *high*-diversity writer, the inversion should shrink or vanish, because the model is no longer being asked to do the thing it cannot do.

## Related

- [Reversion to house style](/wiki/ai/pastiche/reversion-to-house-style) — what the compressed band is compressing toward.
- [Generative exaggeration](/wiki/ai/pastiche/generative-exaggeration) — the opposite distortion, on features the prompt does name.
- [Stylometry](/wiki/cs/stylometry) — where these feature sets come from and what they were built to do.
- [LLM overused words](/wiki/ai/overused-words) — the vocabulary side of the same default register.

## Further reading

- Mikros, [Beyond the surface: stylometric analysis of GPT-4o's capacity for literary style imitation](https://academic.oup.com/dsh/article/40/2/587/8118784), *Digital Scholarship in the Humanities* 40(2), 587–605 (2025)
- Jemama & Kumar, [How Well Do LLMs Imitate Human Writing Style?](https://arxiv.org/abs/2509.24930), arXiv:2509.24930 (2025)
- Wang et al., [Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors](https://arxiv.org/abs/2509.14543), arXiv:2509.14543 (2025)
- Patel, Andrews & Callison-Burch, [Low-Resource Authorship Style Transfer: Can Non-Famous Authors Be Imitated?](https://arxiv.org/abs/2212.08986), arXiv:2212.08986 (2022)
