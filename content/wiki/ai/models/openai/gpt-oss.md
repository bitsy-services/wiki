---
title: "gpt-oss"
weight: 10
---

`gpt-oss` is a pair of open-weight models [OpenAI](/wiki/ai/models/openai) released in August 2025 under Apache 2.0 — `gpt-oss-120b` and `gpt-oss-20b`. They are the company's first open-weight language models since GPT-2 in 2019, and they come with a model card that describes the architecture completely: layer counts, expert counts, routing width, attention configuration, quantisation format.

That makes them unusual in a specific way. Every OpenAI flagship since GPT-4 has been covered by an explicit refusal to disclose architecture. These two are not. For anyone who wants to see what a current-generation model from a frontier lab actually looks like inside, `gpt-oss` is the only OpenAI answer — and where [GPT-2](/wiki/ai/llm/gpt-2) shows the 2019 design running on a laptop, this shows what changed in six years.

Neither model is served through OpenAI's own interface or available in ChatGPT. They exist to be downloaded.

## The two models

| | `gpt-oss-120b` | `gpt-oss-20b` |
| --- | --- | --- |
| Total parameters | 116.8B | 20.9B |
| Active per token | 5.1B | 3.6B |
| Layers | 36 | 24 |
| Experts | 128 | 32 |
| Experts used per token | 4 | 4 |
| Fits in | one 80 GB accelerator | 16 GB |

The names round the parameter counts, and the model card says so: the models "technically have 116.8B and 20.9B parameters, respectively."

The ratio between the two columns is the thing to notice. The larger model has roughly **six times** the total parameters but only about **1.4 times** the active parameters. That is the [mixture-of-experts](/wiki/ai/llm/mixture-of-experts) bargain stated as plainly as it ever gets: capacity scales with the total, cost per token scales with the active count, and the two are decoupled.

## What the architecture does

Most of it will be familiar from the rest of the [LLM section](/wiki/ai/llm), which is itself the interesting part — the design is a collection of choices that have converged across labs rather than anything proprietary.

- **A 2880-wide [residual stream](/wiki/ai/llm/residual-stream)** in both models. Depth and expert count vary; the width does not.
- **RMSNorm before each block**, in the pre-normalisation arrangement. The model card ties this directly to the worked example the wiki already uses: "Similar to GPT-2 we use Pre-LN placement" — *LN* being layer normalisation.
- **SwiGLU** in the expert feed-forward blocks, with a footnote admitting the implementation "is unconventional, including clamping and a residual connection."
- **[Grouped-query attention](/wiki/ai/llm/grouped-query-attention)** with 64 query heads of dimension 64 against **8 key-value heads** — an eight-to-one ratio, which is what keeps the [KV cache](/wiki/ai/llm/kv-cache) affordable.
- **Alternating attention patterns**, following GPT-3: layers alternate between attending to a 128-token band and attending densely across the whole context.
- **[Rotary position embeddings](/wiki/ai/llm/rope)**, with the context extended to 131,072 tokens using YaRN, a method for stretching a rotary scheme beyond its trained length.

### Attention sinks, made explicit

One detail is worth singling out because it fixes a real and slightly strange problem. Each attention head has **a learned bias in the denominator of the softmax** — an extra term that competes with the actual tokens for attention mass.

[Softmax](/wiki/ai/llm/softmax-and-temperature) forces attention weights to sum to 1, which means a head must always attend to *something*, even when nothing in the context is relevant to what it does. Models left to their own devices solve this by dumping attention onto an arbitrary token, usually the first one — the so-called attention sink. The learned bias gives the head somewhere legitimate to put that mass instead. In the model card's words, it "enables the attention mechanism to pay no attention to any tokens."

### Quantisation as a design constraint

The expert weights are trained to be quantised, then shipped in **`MXFP4`** at **4.25 bits per parameter**. Since the mixture-of-experts weights are "90+% of the total parameter count," compressing those is nearly the whole model.

This is what puts the numbers in the table within reach: the 120-billion-parameter model fits on a single 80 GB accelerator, and the smaller one runs on a machine with 16 GB. The quantisation is not an afterthought applied by the community — it is how the models were released, and the sizes were chosen against those hardware targets.

## The chain of thought is not hidden

`gpt-oss` ships the **full, unsummarised chain of thought**. This is the exact opposite of OpenAI's policy on its hosted reasoning models, where the raw working-out is never returned and users get a model-written summary instead, on stated grounds that include competitive advantage.

Both policies come from the same company in the same year. The difference is not a change of mind about whether visible reasoning is safe — it is what happens when the competitive-advantage argument does not apply, because the weights are already public. It is a useful illustration that "what a lab shows you" and "what a model does" are different questions.

## Status

Checked 11 September 2026. The [model card](https://arxiv.org/abs/2508.10925) is the architecture reference and the [repository](https://github.com/openai/gpt-oss) carries the weights.

`gpt-oss-120b` and `gpt-oss-20b` were released 5 August 2025 under Apache 2.0, alongside a separate usage policy. A safety-tuned variant line, `gpt-oss-safeguard`, followed in October 2025. **No newer open-weight release from OpenAI has appeared since**, so as of today these remain the most recent view inside an OpenAI model.

## Sources

- OpenAI, [gpt-oss-120b & gpt-oss-20b Model Card](https://arxiv.org/abs/2508.10925), arXiv:2508.10925 (2025)
- [gpt-oss repository](https://github.com/openai/gpt-oss)
- Xiao et al., [Efficient Streaming Language Models with Attention Sinks](https://arxiv.org/abs/2309.17453), arXiv:2309.17453 (2023) — the attention-sink phenomenon
- Peng et al., [YaRN: Efficient Context Window Extension of Large Language Models](https://arxiv.org/abs/2309.00071), arXiv:2309.00071 (2023)
