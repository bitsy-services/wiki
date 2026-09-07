---
title: "Reversion to House Style"
weight: 30
---

A prompt asking for an author's voice pins down some of the output and leaves the rest open. The open part does not drift toward some other author, and it does not drift randomly. It goes to the register the model writes in when nobody asks it to write in anyone's — the same default that [LLM overused words](/wiki/ai/overused-words) documents from the vocabulary side. Reversion is that register winning the parts of the page the instruction never reached.

## The geometry

George Mikros had GPT-4o imitate Hemingway and Shelley and reduced the [stylometric](/wiki/cs/stylometry) profiles to two dimensions, which makes the shape literal. Eighteen imitations of Hemingway and eighteen of Shelley — nine in each of the two prompting conditions — form tight, internally consistent groups, and all of them "remain separate from the originals"; and generic GPT-4o output with no style instruction "is located between the imitations."

The style instruction is a displacement from the baseline in the target's direction. It is a real displacement — the Shelley imitations do sit closer to *Frankenstein* than the Hemingway ones do — and it is short. The output's home position is the model's own register, and the prompt moves it partway.

The clearest single reading is in words per sentence. Targets 14.15 and 41.51; outputs 12.95–13.47 and 17.70–19.75. A target three times as long as the other pulled the output up by about five words. The rest of the distance stayed where the model already was, and [what transfers](/wiki/ai/pastiche/what-transfers) works through the rest of that table.

## Where the imitation succeeds is where the author was already generic

Wang et al. ran this across 400-plus authors and more than 40,000 generations per model, on four corpora, then asked an authorship-verification model whether each generated text and that author's real writing came from the same person. High accuracy means the imitation held up.

| Corpus | Judged same author |
| --- | --- |
| Reuters news articles | 94.68–97.46% |
| Enron emails | 95.65–96.64% |
| Reddit posts | 49.97–65.88% |
| Blog posts | 16.72–21.25% |

A five-fold spread across genres, on the same task with the same models. Their reading is that models "can partially emulate user style in more structured formats like news and email" and "struggle with nuanced, informal expression in domains such as blogs and forums."

The reading that connects it to everything else on these pages — and this step is inference, not a claim Wang et al. make — is that the spread measures how far each corpus sits from the model's own register rather than how hard each author is. Reuters copy is written to a house style already; a generated news article and a real one by the same correspondent are both, first, news prose. A personal blog is the genre with the least external convention shaping it, so it is the genre where an individual's idiosyncrasy makes up the largest share of the signal, and it is where imitation collapses to one in five.

That predicts the Hemingway result too. Hemingway scores well on sentence length not because his rhythm transferred but because his rhythm was already near where the model lives.

Wang et al.'s own summary of the mechanism is blunt: "without example prompts, LLMs default to a generic style."

## The statistical fingerprint the prompt cannot reach

Jemama and Kumar tested five models across three families and got style-matching accuracy up to 23.5 times higher with few-shot prompting than zero-shot, and 99.9% style alignment with completion prompting, where the model is handed the opening of a passage and continues it rather than being told what to write. By any surface measure the imitation worked.

Then they measured [perplexity](/wiki/ai/llm/perplexity). Human writing in their sample averaged **29.5**; model output tuned to match that writing averaged **15.2**. The imitation is roughly twice as predictable as the thing it imitates, while scoring near-perfectly on sounding like it.

Their conclusion is that "stylistic fidelity and statistical detectability are separable." Two texts can be indistinguishable to a style classifier and cleanly separable by how surprised a model is by their next token. Nothing in a style prompt addresses the second quantity, because nothing in a style prompt is about the distribution the tokens are drawn from.

Zeng and Nini find the same excess from the direction of forensics: impersonation attempts fail against authorship-verification methods precisely because the generated text is too various and too unpredictable to be the person, which [authorship survives imitation](/wiki/ai/pastiche/authorship-survives#does-impersonation-defeat-verification) takes up. The overshoot is not a bug in one prompt. It is a property of the generator that survives instructions to the contrary, which is why it shows up as [Hemingway with a larger vocabulary than Hemingway](/wiki/ai/pastiche/what-transfers).

## Why the default is so hard to leave

The register has a documented cause. Preference training rewards typicality: Zhang et al. model a rater's judgement as an answer's true quality plus α times how typical its wording is, and fit α̂ ≈ 0.57 on response pairs rated equally correct. Familiar phrasing pulls more than half as hard as being right, and [RLHF](/wiki/ai/llm/rlhf) optimizes against that signal without mercy.

The result is a strong prior over wording that a style instruction competes with rather than replaces. A prompt is a few hundred tokens of context; the register is what the weights were tuned to prefer. Where the two disagree and the prompt is not specific, the weights win — and the prompt is never specific about function-word rates, because nobody can be.

## What this changes about prompting

**Pin the features that actually differ from the default, not the ones that characterize the author.** A style brief that says "short declarative sentences, concrete nouns, no adverbs" for Hemingway is describing a target the model is already near, and spending its instruction budget on distance it did not have to travel. The useful instructions are the ones aimed where the gap is: repeat the noun rather than pronominalize it, do not vary the verb, let the paragraph end without a summarizing clause.

**Expect the residue to be house style, and check for it there.** The failure will not look like a bad imitation of the author. It will look like a competent imitation with the model's own habits filling the gaps — the vocabulary from [overused words](/wiki/ai/overused-words), the tidy tripartite structures, the closing sentence that appraises what just happened.

**Measure the gap rather than the match.** A style classifier says the imitation is good; perplexity and [type-token ratio](/wiki/ai/pastiche/what-transfers#lexical-diversity-runs-backwards) say it is generated. Reporting only the first is how a 99.9% style-alignment number and a 2× perplexity gap end up in the same paper.

## Check yourself

Generate three passages: one with no style instruction, one in an author whose measurable profile sits near the model's default, and one in an author far from it. Compute mean sentence length and standardized [type-token ratio](/wiki/ai/pastiche/what-transfers#lexical-diversity-runs-backwards) for all three. The unstyled baseline should land between the two imitations rather than outside them, and the far author's imitation should sit closer to the baseline than to its target. If the baseline lands outside the pair, the model's register is not where this page says it is, and the compression story is wrong for that model.

## Related

- [LLM overused words](/wiki/ai/overused-words) — the same default register, measured through vocabulary, with the evidence for its origin in preference training.
- [What transfers and what does not](/wiki/ai/pastiche/what-transfers) — the feature-level measurements the geometry here is built from.
- [Generative exaggeration](/wiki/ai/pastiche/generative-exaggeration) — the complementary failure, on the features the prompt does pin.
- [Authorship survives imitation](/wiki/ai/pastiche/authorship-survives) — the same statistical excess, seen by a verifier.
- [Perplexity](/wiki/ai/llm/perplexity) — what the 29.5 against 15.2 is measuring.

## Further reading

- Wang et al., [Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors](https://arxiv.org/abs/2509.14543), arXiv:2509.14543 (2025)
- Mikros, [Beyond the surface: stylometric analysis of GPT-4o's capacity for literary style imitation](https://academic.oup.com/dsh/article/40/2/587/8118784), *Digital Scholarship in the Humanities* 40(2), 587–605 (2025)
- Jemama & Kumar, [How Well Do LLMs Imitate Human Writing Style?](https://arxiv.org/abs/2509.24930), arXiv:2509.24930 (2025)
- Zeng & Nini, [Authorship Impersonation via LLM Prompting does not Evade Authorship Verification Methods](https://arxiv.org/abs/2603.29454), arXiv:2603.29454 (2026)
- Zhang et al., [Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity](https://arxiv.org/abs/2510.01171), arXiv:2510.01171 (2025)
