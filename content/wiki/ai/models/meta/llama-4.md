---
title: "Llama 4"
weight: 10
---

Llama 4 is [Meta](/wiki/ai/models/meta)'s fourth and, as of September 2026, newest open-weight generation, released 5 April 2025. It was the first Llama built as a [mixture of experts](/wiki/ai/llm/mixture-of-experts) and the first to take images through the same pathway as text. It is also the first generation with **no research paper**, and the only one that shipped incomplete.

Meta announced three models. Two exist:

| Model | Active | Total | Experts | Status |
| --- | --- | --- | --- | --- |
| Scout | 17B | 109B | 16 | Shipped |
| Maverick | 17B | 400B | 128 routed + 1 shared | Shipped |
| Behemoth | 288B | ~2T | 16 | **Never released** |

*Total* is what must be held in memory; *active* is the share each token is actually multiplied by. Both shipped models activate the same 17 billion parameters per token and differ in how much capacity sits behind that — which is the mixture-of-experts trade stated as plainly as a lineup ever states it.

## Behemoth, and why its absence matters

Behemoth was described at launch as "still training" and previewed rather than released. Seventeen months later it is still absent from Meta's model repository, and Meta has issued no cancellation.

The consequence is not just a missing model. **Scout and Maverick were both codistilled from Behemoth** — trained on the larger model's outputs while it was still training. So the generation that reached the public is the shadow of a model the public never got, and the teacher that shaped it cannot be inspected.

## The 10-million-token claim

Scout is advertised with an "industry leading 10M" context window. The same Meta blog post states that Scout's base model was "pre-trained and post-trained with a **256K** context length."

Both figures are Meta's, and the gap between them is the story. 256K is the trained length. 10M is an extrapolation beyond it — supported by synthetic retrieval evaluations rather than by training, and **39 times the longest sequence the model ever saw**. No serving stack at release came close to it, and a 10M-token [KV cache](/wiki/ai/llm/kv-cache) is not something ordinary hardware can hold regardless of what the model can represent.

### iRoPE, the mechanism behind the claim

The design that is supposed to generalise is called `iRoPE`, and it is an interleave:

- **Most layers use [rotary position embedding](/wiki/ai/llm/rope)** but attend only within chunks of 8,192 tokens. Position is encoded, reach is local.
- **Every fourth layer carries no positional embedding at all** and attends across the entire context with a full causal mask. Reach is global, position is not encoded.
- **Temperature scaling is applied at inference** to help the attention distribution stay usable at lengths far past training.

The bet is that the rotary layers handle local structure while the position-free layers carry long-range information, and that a scheme which never learned an absolute position for token 9,000,000 therefore has nothing to get wrong about it. Whether the bet pays at 10M is precisely what was never trained and never independently measured.

This is the same family of structural bet that [Gemma](/wiki/ai/models/google/gemma) makes with its local and global interleave, and that [Qwen](/wiki/ai/models/qwen) makes from Qwen3.5 with linear-attention blocks between full-attention ones: most layers get something cheaper than full attention, a minority get the real thing.

## What else changed

**Early fusion for vision.** Llama 3.2 attached images through a cross-attention adapter bolted onto a text model. Llama 4 feeds text and image tokens into the same backbone together. The vision encoder is based on MetaCLIP, trained separately against a frozen Llama.

**Scale.** Training data was "more than 30 trillion tokens" across 200 languages, roughly double Llama 3's mixture. Meta published the compute, which most labs do not: 7.38 million H100 GPU-hours across Scout and Maverick, with the associated emissions figures.

**Query-key normalisation on Scout but not Maverick** — normalising the [query and key](/wiki/ai/llm/qkv-projections) vectors before the attention scores are computed. That the two models in one generation differ here, with no paper to explain why, is characteristic of this release.

## The benchmark-variant episode

At launch, the Maverick submitted to the LMArena ranking was not the model released. Meta had entered an experimental chat-tuned variant while publishing the general one, producing a leaderboard position the downloadable model did not reproduce.

It is the cleanest illustration in this section of why leaderboard positions do not belong in a reference page: the number was real, the model it described was not the one anyone could use, and nothing in the ranking disclosed the difference.

## The licence

Llama 4 ships under the Llama Community Licence, which the Open Source Initiative has twice said is not an open-source licence. The [Meta page](/wiki/ai/models/meta#the-licence-precisely) covers it in full; the three things that bite are a 700-million-monthly-active-user threshold frozen at the release date, a requirement to display "Built with Llama" and to prefix derived model names with "Llama", and an acceptable-use policy that restricts multimodal use by entities domiciled in the European Union.

That last restriction appears only in the acceptable-use section of the model repository page — **not** in the `LICENSE` file and not in the vision model card. Checking the obvious source gives the wrong answer.

## Status

Checked 11 September 2026. Weights are at [huggingface.co/meta-llama](https://huggingface.co/meta-llama); Llama 4 documentation now lives at [developer.meta.com](https://developer.meta.com/ai/models/llama-4/) after `llama.com` began redirecting there.

Llama 4 remains the newest open-weight Llama generation. There is no Llama 5. Meta's current frontier model is Muse Spark, which is closed-weight and not a Llama.

## Sources

- Meta, [The Llama 4 herd](https://ai.meta.com/blog/llama-4-multimodal-intelligence/) (5 April 2025) — carries both the 10M and the 256K figures
- Meta, [Llama 4 licence](https://raw.githubusercontent.com/meta-llama/llama-models/main/models/llama4/LICENSE)
- Grattafiori et al., [The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783), arXiv:2407.21783 (2024) — the last generation with a paper
- Open Source Initiative, [Meta's LLaMa licence is not open source](https://opensource.org/blog/metas-llama-2-license-is-not-open-source)
