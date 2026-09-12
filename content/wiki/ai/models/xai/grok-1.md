---
title: "Grok-1"
weight: 20
---

Grok-1 is the first model [xAI](/wiki/ai/models/xai) shipped, and the only one whose architecture it has ever published. Released 17 March 2024 under **Apache 2.0** — code and weights both — it is a 314-billion-parameter [mixture of experts](/wiki/ai/llm/mixture-of-experts), and at the time the largest open-weight model anyone had put out.

It is on this wiki as a worked example rather than as a recommendation. Nothing xAI has released since discloses a parameter count, a layer count or a routing scheme, so Grok-1 is the last look inside the family. And because it is a full frontier-scale mixture of experts with every number published, it is a useful counterpart to [GPT-2](/wiki/ai/llm/gpt-2), which is small and dense and runs on a laptop.

## The configuration

| Property | Value |
| --- | --- |
| Total parameters | 314B |
| Experts | 8, with **2 active per token** |
| Layers | 64 |
| Embedding dimension | 6,144 |
| Attention | 48 query heads, 8 key-value heads |
| Positional encoding | rotary |
| Context window | **8,192 tokens** |
| Tokenizer | SentencePiece, 131,072 entries |
| Licence | Apache 2.0, code and weights |

Three of those repay a second look.

**Eight experts, two active** is a coarse-grained mixture by later standards. [DeepSeek](/wiki/ai/models/deepseek) would go to 256 experts activating 8, and [Qwen](/wiki/ai/models/qwen/qwen3-8) to 512 activating 11. More, narrower experts give the router a far larger space of combinations to choose from for the same active-parameter budget, and the field moved that way over the following two years. Grok-1 is a clean snapshot of the earlier arrangement.

**48 query heads against 8 key-value heads** is [grouped-query attention](/wiki/ai/llm/grouped-query-attention) at a six-to-one ratio — six query heads share each key-value head, so the [KV cache](/wiki/ai/llm/kv-cache) is a sixth the size it would otherwise be. This was the standard answer to cache size in 2024, before the compression approaches that replaced it.

**A 131,072-entry vocabulary** is large for the period, and about half of what the current Qwen generation uses. A bigger vocabulary means fewer [tokens](/wiki/ai/llm/tokenization) per unit of text, especially in languages that are poorly served by a small one.

## Two things that catch people out

**The context window is 8,192 tokens.** Not 128,000. Grok-1.5, which shipped twelve days after the weights release, had a 128,000-token window — and the two get conflated constantly. The released weights are the earlier, shorter-context model.

**It is a base model, not an assistant.** The repository is explicit that the checkpoint is not fine-tuned for dialogue. It continues text; it does not follow instructions, hold a conversation or refuse anything. Using it as a chat model means doing the [fine-tuning](/wiki/ai/llm/fine-tuning) yourself. Pre-training finished in October 2023, and no training-data composition, training date or knowledge cutoff is published.

Practically, it also needs a great deal of hardware: 314 billion parameters must all be resident even though only about a quarter of them are used per token, which is the [mixture-of-experts](/wiki/ai/llm/mixture-of-experts) memory trap in its starkest form.

## What the release was, and what followed

The release is JAX code plus an example inference script, with weights distributed by torrent and through Hugging Face. It was a genuine open-weights release with no revenue gate, no user threshold and no acceptable-use annex — the most permissive terms any model of that size had carried.

It did not set a pattern. Grok-2's weights were later published under a bespoke **Grok 2 Community Licence** rather than Apache 2.0, and no generation from Grok-3 onward has been released at all. xAI's trajectory on openness runs opposite to [Mistral's](/wiki/ai/models/mistral): one fully open generation, one partly open, then closed.

## Status

Checked 11 September 2026. The [repository](https://github.com/xai-org/grok-1) is the source.

Grok-1 is historical. The current generation is Grok 4.6, which is closed and discloses nothing about its architecture. The Grok-1 weights remain available under Apache 2.0 and remain the last architecture disclosure xAI has made.

## Sources

- [grok-1 repository](https://github.com/xai-org/grok-1) — the configuration table above, the licence, and the base-model caveat
- [Grok-2 on Hugging Face](https://huggingface.co/xai-org/grok-2) — the custom licence that followed
- Shazeer et al., [Outrageously Large Neural Networks](https://arxiv.org/abs/1701.06538), arXiv:1701.06538 (2017) — the mixture-of-experts layer
- Ainslie et al., [GQA: Training Generalized Multi-Query Transformer Models](https://arxiv.org/abs/2305.13245), arXiv:2305.13245 (2023)
