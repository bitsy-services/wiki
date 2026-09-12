---
title: "DeepSeek-V4"
weight: 10
---

DeepSeek-V4 is [DeepSeek](/wiki/ai/models/deepseek)'s current generation, announced 24 April 2026. It ships as two models — `deepseek-v4-pro` at 1.6 trillion total parameters with 49 billion active, and a Flash line an order of magnitude smaller — both with a million-token context, both under the MIT licence.

The generation matters for two reasons beyond its size. It is where DeepSeek **finished merging its reasoning line back into its general line**, so that thinking is a per-request setting rather than a separate model. And it is where the architecture that made the lab's name, multi-head latent attention, stopped being what it ships.

## There is no R2

DeepSeek-R1 in January 2025 was the model that demonstrated reasoning could be trained by reinforcement learning alone. R1-0528, from May 2025, was the last model released under the R name.

The line did not end; it was absorbed. V3.1 in August 2025 introduced "a hybrid reasoning architecture: a single model supports both thinking mode and non-thinking mode," and by V4 the choice is an **effort level** — `low`, `high`, `max` — set on each request. `DeepSeek-V4-Pro-Max` is named in DeepSeek's own material as the maximum-effort mode of V4-Pro, not as a separate model.

This is the same consolidation [OpenAI](/wiki/ai/models/openai) made when GPT-5 absorbed the `o`-series, [Mistral](/wiki/ai/models/mistral) made when Magistral was retired into Mistral Small 4, and [Alibaba](/wiki/ai/models/qwen) made with Qwen3's hybrid thinking mode. Four labs of very different sizes and origins reached the same conclusion inside about a year: a reasoning model is better as a dial than as a product.

## What replaced multi-head latent attention

[Multi-head latent attention](/wiki/ai/models/deepseek#multi-head-latent-attention) — compressing the keys and values of all heads into one low-dimensional latent per token, and reconstructing them when needed — is the technique DeepSeek is best known for, and it is two generations old.

V3.2 layered a **sparse-selection** scheme over it: rather than changing how the cache is stored, an indexer chooses which earlier tokens each query attends to at all, so the quadratic term shrinks. V4 changed the attention design again, to a hybrid.

DeepSeek's own claim for what this buys, at the length where it matters: at a million tokens of context, V4-Pro "requires only 27% of single-token inference FLOPs and 10% of [KV cache](/wiki/ai/llm/kv-cache) compared with DeepSeek-V3.2" — a FLOP being one floating point operation, the unit compute budgets are counted in. A tenth of the cache is the figure to hold — [context length](/wiki/ai/llm/context-length) explains why that is the binding constraint on long-context serving rather than the arithmetic.

The general lesson is worth separating from the specific mechanism. The idea that spread from DeepSeek's work is **compress the cache rather than share it**; the particular compression it used in V3 has already been superseded twice by its own authors.

## Why the engineering looks the way it does

DeepSeek trains under United States export controls on accelerators sold into China, on H800s — the reduced-interconnect variant Nvidia built for that market. Several of the techniques the lab is admired for exist specifically to work around the constrained bandwidth between machines rather than as general elegance: the DualPipe pipeline scheme that overlaps the all-to-all traffic a [mixture of experts](/wiki/ai/llm/mixture-of-experts) generates with computation, the custom communication kernels, and the node-limited routing that caps how many machines a single token's experts can span.

Read that way, the efficiency is not a style preference. It is what the constraint produced, and it transferred to everyone.

## The company behind it

DeepSeek was founded in July 2023 by Liang Wenfeng, is based in Hangzhou, and is funded out of **High-Flyer**, a quantitative hedge fund Liang co-founded in 2015, rather than by venture capital. Its headcount is around 160.

Those two facts together explain a good deal. A lab financed from a hedge fund's balance sheet has no investors pressing it to monetise and no need to price access against a return, which is why an organisation of that size publishes weights, prices, papers and its own training-cost table while much larger competitors publish none of them.

## Status

Checked 11 September 2026. DeepSeek's [API documentation](https://api-docs.deepseek.com/) is the live source and its [update log](https://api-docs.deepseek.com/updates/) carries releases.

`deepseek-v4-pro` reached general availability 13 August 2026. **DeepSeek-V4.1-Flash** shipped 10 September 2026 — one day before this page was checked — as `deepseek-flash`, described as "the smallest model in our new architecture family, with native multimodal visual understanding"; the earlier Flash identifiers now route to it. The legacy `deepseek-chat` and `deepseek-reasoner` endpoints that served V3 and R1 were retired on 24 July 2026.

Pricing carries a peak and off-peak split, so every rate is two numbers.

## Sources

- DeepSeek, [V4 announcement](https://api-docs.deepseek.com/news/news260424/) (24 April 2026)
- DeepSeek, [API update log](https://api-docs.deepseek.com/updates/)
- DeepSeek-AI, [DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437), arXiv:2412.19437 (2024) — the reference configuration this generation moved on from
- DeepSeek-AI, [DeepSeek-V2](https://arxiv.org/abs/2405.04434), arXiv:2405.04434 (2024) — the first multi-head latent attention paper
