---
title: "Meta"
weight: 40
bookCollapseSection: true
---

Meta published the **Llama** family, and in doing so created most of the open-weight ecosystem the rest of this section depends on — open-weight meaning the trained numbers are released as files anyone can download and run, rather than reachable only through the builder's own service. Llama 2's weights and commercial terms in 2023 made it possible for people outside a handful of labs to fine-tune, serve and study a capable model, and the papers that came with each generation are still the most detailed account any Western lab has published of how a frontier-scale model is trained.

That is written in the past tense deliberately. **Since April 2026, Meta's frontier model has been neither a Llama nor open-weight.** Muse Spark, announced by Meta Superintelligence Labs, launched as a private preview behind a paid service, with no parameter counts published for any model in the line. Llama 4, from April 2025, is still the newest open-weight generation. It shipped incomplete, and it has no research paper — the first generation without one.

## The reversal

The sequence is worth setting out plainly, because Meta has not narrated it.

**Llama 1** (February 2023) was research-only and leaked within a week. **Llama 2** (July 2023) shipped weights with commercial terms attached. **[Llama 3](/wiki/ai/models/meta/llama-3)** through **3.3** (2024) widened the sizes and added multimodal and on-device variants. **[Llama 4](/wiki/ai/models/meta/llama-4)** (April 2025) was the first built as a [mixture of experts](/wiki/ai/llm/mixture-of-experts).

Then the organisation changed. Meta invested in Scale AI and brought in its founder, Alexandr Wang, as **Chief AI Officer** in June 2025, leading a new **Meta Superintelligence Labs**. **Yann LeCun, who founded Facebook AI Research in 2013 and served as Chief AI Scientist for about twelve years, left in November 2025.** `llama.com` now redirects to `developer.meta.com/ai/`, where Llama 4 sits alongside the closed Muse lineup rather than on a property of its own.

No announcement declared a change of strategy. The change is legible only from what shipped: a closed frontier model, a discontinued brand site, and an open generation left unfinished.

## Llama 4, and what did not ship

Llama 4 arrived as three models, of which two exist. The two parameter columns are the [mixture-of-experts](/wiki/ai/llm/mixture-of-experts) convention: *total* is what must be held in memory, *active* is the share each token is actually multiplied by.

| Model | Active | Total | Experts | Status |
| --- | --- | --- | --- | --- |
| Scout | 17B | 109B | 16 | Shipped |
| Maverick | 17B | 400B | 128 routed + 1 shared | Shipped |
| Behemoth | 288B | ~2T | 16 | **Never released** |

Behemoth was described at launch as "still training" and previewed rather than released. It is still absent from Meta's model repository, and Meta has issued no cancellation. This matters beyond the missing model: Scout and Maverick were both **codistilled from Behemoth** — trained on the larger model's outputs while it was still training, the technique [DeepSeek-R1](/wiki/ai/models/deepseek/r1#the-distilled-models) uses to put reasoning into small models. The generation that shipped is the shadow of a model the public never got.

### The 10-million-token context

Scout is advertised with an "industry leading 10M" context window, which would be an order of magnitude beyond anything else in this section. The same Meta blog post also states that Scout's base model was "pre-trained and post-trained with a **256K** context length."

Both numbers are Meta's. 256K is the trained length; 10M is an extrapolation beyond it, supported by synthetic retrieval evaluations rather than by training, and **39 times the longest sequence the model ever saw**. No serving stack at release came close to it. The mechanism behind the claim is `iRoPE`, an interleave of chunked and unchunked attention layers that [the Llama 4 page](/wiki/ai/models/meta/llama-4#irope-the-mechanism-behind-the-claim) sets out.

Quoting either number alone misleads. The honest version is that 10M is an architectural claim and 256K is the trained length, and Meta printed both on the same page. [Context length](/wiki/ai/llm/context-length) covers why the distinction bites — a 10M-token [KV cache](/wiki/ai/llm/kv-cache) is not something ordinary hardware can hold regardless of what the model can represent.

### What the architecture actually changed

Llama's contribution across generations was less about novelty than about showing, in public and in detail, which combination works. Llama 1 made three substitutions on the original [transformer](/wiki/ai/llm) that are now near-universal: **RMSNorm** instead of layer normalisation, **SwiGLU** instead of a plain activation in [the MLP](/wiki/ai/llm/the-mlp), and **rotary position embedding** instead of learned position vectors. Llama 2 brought [grouped-query attention](/wiki/ai/llm/grouped-query-attention) to the larger sizes; Llama 3 used it everywhere and replaced the tokenizer.

Llama 4 added the mixture of experts, and changed how vision enters the model: where Llama 3.2 attached images through a cross-attention adapter, Llama 4 uses **early fusion**, feeding text and image tokens into the same backbone together. Training data was "more than 30 trillion tokens" across 200 languages, and Meta published the compute: 7.38 million H100 GPU-hours across Scout and Maverick, with the associated emissions.

## The licence, precisely

The Llama Community Licence is **not** an open-source licence. The Open Source Initiative has said so twice, naming which parts of the Open Source Definition it fails. Three restrictions matter:

**The 700-million-user clause.** If a licensee's products had more than 700 million monthly active users in the calendar month before the version's release date, they must request a separate licence from Meta. Two details are routinely got wrong: the figure is 700 million, not 700 thousand; and **the test is frozen at the release date**. A company under the threshold on 5 April 2025 does not fall into the clause by growing past it later. The same construction appears in the Llama 2 and Llama 3.2 licences, measured at their own release dates.

**Naming and attribution.** Redistribution requires prominently displaying "Built with Llama", and any model trained on Llama outputs must have "Llama" at the start of its name. This is why so many community models are called Llama-something.

**An acceptable-use policy**, which includes a restriction on multimodal use by entities domiciled in the European Union. That restriction is worth knowing about because of where it lives: it is **absent from the `LICENSE` file and from the vision model card**, appearing only in the acceptable-use section of the model repository page. Checking the obvious source leads to the wrong conclusion.

## Criticism

**The benchmark-variant episode.** At Llama 4's launch, the Maverick model submitted to the LMArena ranking was not the one released. Meta had entered an experimental chat-tuned variant while publishing the general release, which produced a leaderboard position the downloadable model did not reproduce. It is the clearest case in this section of why leaderboard positions do not belong in a reference page.

**The context gap** above, where the advertised figure is 39 times the trained one.

**No paper.** Every prior generation came with a detailed technical report; Llama 4 did not. For a family whose main contribution was disclosure, that is a substantive loss.

**Training data.** *Kadrey v. Meta* tested whether training on copyrighted books is fair use. Meta prevailed, but on the specific record before the court rather than on a general holding that training is always fair use.

## Status

Checked 11 September 2026. Meta's [developer site](https://developer.meta.com/ai/) is the live source; open weights are at [huggingface.co/meta-llama](https://huggingface.co/meta-llama).

**Llama 4** — Scout and Maverick — remains the newest open-weight generation, released 5 April 2025. There is no Llama 5; claims otherwise are not supported by Meta's own repositories.

**Muse Spark** is the current frontier model, announced 8 April 2026, closed-weight, sold through a paid interface with a million-token context. Meta publishes no parameter count for any Muse model — the sharpest possible break with what Llama stood for.

## Sources

- Touvron et al., [LLaMA: Open and Efficient Foundation Language Models](https://arxiv.org/abs/2302.13971), arXiv:2302.13971 (2023)
- Touvron et al., [Llama 2: Open Foundation and Fine-Tuned Chat Models](https://arxiv.org/abs/2307.09288), arXiv:2307.09288 (2023)
- Grattafiori et al., [The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783), arXiv:2407.21783 (2024)
- Meta, [The Llama 4 herd](https://ai.meta.com/blog/llama-4-multimodal-intelligence/) (5 April 2025) — carries both the 10M and 256K figures
- Meta, [Llama 4 licence](https://raw.githubusercontent.com/meta-llama/llama-models/main/models/llama4/LICENSE) — the 700-million-user clause
- Open Source Initiative, [Meta's LLaMa licence is not open source](https://opensource.org/blog/metas-llama-2-license-is-not-open-source)
- Meta, [Introducing Muse Spark](https://ai.meta.com/blog/introducing-muse-spark-msl/) (8 April 2026)
