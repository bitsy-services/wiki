---
title: "Llama 3"
weight: 20
---

Llama 3 is [Meta](/wiki/ai/models/meta)'s third open-weight generation, released from April 2024 in 8B, 70B and — with Llama 3.1 in July — 405B sizes. It matters less for what it scored than for what came with it: **The Llama 3 Herd of Models**, a technical report of a detail and honesty that no lab has matched since, including Meta itself.

It is the last Llama generation with a paper. [Llama 4](/wiki/ai/models/meta/llama-4) shipped without one.

## What the report published

The report is the reason this page exists. It states, for a frontier-scale model:

- **The full architecture** — layer counts, model dimensions, head counts, [grouped-query attention](/wiki/ai/llm/grouped-query-attention) configuration, vocabulary size, [rotary position embedding](/wiki/ai/llm/rope) base frequency.
- **The training-token count**: about 15 trillion tokens, an order of magnitude past what Chinchilla-optimal scaling would have prescribed for those sizes.
- **The compute**, in GPU-hours, per model.
- **The hardware and what went wrong with it** — cluster composition, network topology, and a failure analysis covering how often training was interrupted and by what.
- **The data pipeline**: deduplication, quality filtering, the classifiers used and the mixture proportions.
- **The post-training recipe**: supervised fine-tuning, rejection sampling, and direct preference optimization, with the reasoning for choosing that over the reinforcement-learning approach [OpenAI](/wiki/ai/models/openai) used.

Very little of that is normal. Most labs publish an architecture diagram at best; several publish nothing at all. The reliability section in particular — a public account of how often a run of that size breaks — is close to unique.

## Deliberately over-trained

The most consequential single choice is the token count, and it cuts against the prevailing theory.

Google DeepMind's Chinchilla work in 2022 established that for a **fixed training budget**, model size and training tokens should scale together — roughly 20 tokens per parameter is the ratio implied by Chinchilla's own 70-billion-parameter model trained on 1.4 trillion tokens, though the paper states the equal-scaling rule rather than the ratio. Train a smaller model on more data and you waste compute; train a bigger model on less and you waste parameters.

Llama 3's 8B model was trained on about 15 trillion tokens. That is roughly **1,875 tokens per parameter**, nearly a hundred times the Chinchilla-implied ratio.

This is not a contradiction of the scaling work; it is optimising for something else. Chinchilla minimises **training** compute for a given quality. If a model is going to be downloaded and run millions of times, what matters is **inference** cost — and inference cost is set by the model's size, not by how long it trained. Spending far more training compute to get the same quality into a smaller model is a bad trade for a lab that runs the model once and a very good one for everybody who runs it afterwards.

That reasoning is what an open-weights strategy looks like when it reaches the training budget. [Why scale worked](/wiki/ai/llm/why-scale-worked) covers the underlying argument.

## The architectural choices that became standard

Llama's real influence is a set of substitutions on the original transformer that are now near-universal, established across the first three generations:

- **RMSNorm** in place of layer [normalisation](/wiki/ai/neural-network/normalization) — the same rescaling without the mean-centring step, slightly cheaper and no worse.
- **SwiGLU** in place of a plain activation in the feed-forward block, a gated variant that spends more parameters to fit better.
- **Rotary position embedding** in place of learned position vectors, which is what makes context extension possible at all.
- **Grouped-query attention**, introduced in Llama 2 for the larger models and used everywhere from Llama 3, shrinking the [KV cache](/wiki/ai/llm/kv-cache) by sharing key-value heads between query heads.

Llama 3 also replaced the tokenizer, moving to a 128,000-entry vocabulary, which cut the number of [tokens](/wiki/ai/llm/tokenization) needed for the same text and disproportionately helped non-English languages.

Read the list against [gpt-oss](/wiki/ai/models/openai/gpt-oss)'s published architecture from 2025 and the convergence is obvious: pre-normalisation with RMSNorm, SwiGLU, rotary embeddings, grouped-query attention. Different labs, different data, same skeleton.

## Status

Checked 11 September 2026. Weights are at [huggingface.co/meta-llama](https://huggingface.co/meta-llama).

Llama 3 is superseded by Llama 4, which remains Meta's newest open-weight generation. The 3.x weights remain available under the Llama Community Licence — which is not an open-source licence; the [Meta page](/wiki/ai/models/meta#the-licence-precisely) covers its terms.

The Llama 3 report remains the most detailed public account of training a frontier-scale model, and nothing published since has replaced it.

## Sources

- Grattafiori et al., [The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783), arXiv:2407.21783 (2024)
- Touvron et al., [Llama 2: Open Foundation and Fine-Tuned Chat Models](https://arxiv.org/abs/2307.09288), arXiv:2307.09288 (2023)
- Touvron et al., [LLaMA: Open and Efficient Foundation Language Models](https://arxiv.org/abs/2302.13971), arXiv:2302.13971 (2023)
- Hoffmann et al., [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556), arXiv:2203.15556 (2022) — Chinchilla
- Ainslie et al., [GQA](https://arxiv.org/abs/2305.13245), arXiv:2305.13245 (2023)
