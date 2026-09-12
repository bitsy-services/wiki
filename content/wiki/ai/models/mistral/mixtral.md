---
title: "Mixtral 8x7B"
weight: 20
---

Mixtral 8x7B, released by [Mistral AI](/wiki/ai/models/mistral) on 11 December 2023 under Apache 2.0, was the first sparse [mixture of experts](/wiki/ai/llm/mixture-of-experts) that large numbers of people actually ran. Sparse routing had been published years earlier; Mixtral is where it stopped being a research idea and became something a developer downloaded on a Monday.

It is on this wiki for a second reason, which is that **its name is wrong in an instructive way**. `8x7B` reads as eight 7-billion-parameter models stapled together — 56 billion. The model has 46.7 billion parameters and uses 12.9 billion per token. Working out where those numbers come from teaches most of what a mixture of experts is.

## The arithmetic

A transformer layer has two parts: an [attention](/wiki/ai/llm/attention) block and a feed-forward block, [the MLP](/wiki/ai/llm/the-mlp). Mixtral replicates **only the feed-forward block** eight times. The attention projections, the token embeddings, the output head and the normalisation parameters exist once and are shared by all eight experts.

```text
shared (attention + embeddings + norms)  ≈  1.6B
one feed-forward expert                  ≈  5.6B

total  = 1.6 + 8 × 5.6  =  46.7B
active = 1.6 + 2 × 5.6  =  12.9B
```

**Why not 56 billion.** Eight standalone copies of Mistral 7B would be 8 × 7.24B — the model is 7.24 billion parameters, not a round 7 — which is **57.9 billion**. The 11.2-billion gap down to 46.7 is seven redundant copies of that 1.6-billion shared block. Sharing it once instead of eight times is precisely what the design buys, and the name's arithmetic was never meant to be taken literally.

**Why not 14 billion active.** For each token, at each layer, a small network called the router picks 2 of the 8 experts. So two experts' worth of feed-forward is paid — but the shared attention and embeddings are paid once regardless of which experts were chosen. Hence 12.9 billion rather than 2 × 7.24.

## What the two numbers are for

This is the durable lesson, and it generalises to every model in this section that quotes a pair:

- **Total parameters set the memory.** All 46.7 billion must be resident, because the router may send the next token to any expert. There is no way to keep only the popular ones loaded.
- **Active parameters set the arithmetic.** Only 12.9 billion get multiplied per token, so the model computes — and therefore responds — roughly like a 13-billion-parameter dense model.

So Mixtral costs memory like a 47-billion-parameter model and time like a 13-billion-parameter one. What you are buying with the extra memory is **capacity**: more places to put what the model knows, without paying for them on every token.

This is also the single most common misreading of a modern spec sheet. Google says it outright about [Gemma](/wiki/ai/models/google/gemma)'s mixture-of-experts model: "all 26 billion parameters must be loaded into memory to maintain fast routing and inference speeds." The active figure never buys memory.

## Where it sits in the lineage

Mixtral's design is coarse by later standards: **8 experts, 2 active**. The direction of travel since has been to many more, much narrower experts — [DeepSeek](/wiki/ai/models/deepseek) to 256 activating 8 plus a shared expert, [Qwen](/wiki/ai/models/qwen/qwen3-8) to 512 activating 11. More, smaller experts give the router a far larger space of combinations for the same active-parameter budget, so specialisation can be finer.

Mixtral also inherits [grouped-query attention](/wiki/ai/llm/grouped-query-attention) and sliding-window attention from Mistral 7B, the model whose feed-forward block it replicates.

A larger sibling, **Mixtral 8x22B**, followed in April 2024 at 141 billion total and 39 billion active, with the same two-of-eight routing.

## Status

Checked 11 September 2026. Mixtral is historical — Mistral's current open flagship is [Mistral Large 3](/wiki/ai/models/mistral/mistral-large-3), at 675 billion total and 41 billion active.

The Mixtral weights remain available under Apache 2.0, and the model remains the clearest small-enough-to-follow example of the arithmetic every current mixture-of-experts spec sheet assumes you already understand.

## Sources

- Jiang et al., [Mixtral of Experts](https://arxiv.org/abs/2401.04088), arXiv:2401.04088 (2024)
- Mistral AI, [Mixtral of experts](https://mistral.ai/news/mixtral-of-experts/) (11 December 2023) — the 46.7B and 12.9B figures
- Jiang et al., [Mistral 7B](https://arxiv.org/abs/2310.06825), arXiv:2310.06825 (2023) — the model whose feed-forward block is replicated
- Shazeer et al., [Outrageously Large Neural Networks](https://arxiv.org/abs/1701.06538), arXiv:1701.06538 (2017) — the original sparse mixture-of-experts layer
