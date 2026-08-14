---
title: "Multi-Head Attention"
weight: 160
---

One head is a narrow channel: a 64-wide query chasing one kind of relationship. [GPT-2 small](/wiki/ai/llm/gpt-2) runs **12 of them per block, in parallel, over the same row**, and they never talk to each other.

The row doesn't get wider. `d_model` is split, not multiplied: 12 heads × 64 = 768. Each head reads the full row through its own [Q/K/V projections](/wiki/ai/llm/qkv-projections), produces its own 64-wide result, and the twelve results are concatenated back to 768, passed through one output matrix, and added to the stream as a single write. Twelve independent reads, one write.

That every head owns *all three* of its projections is a GPT-2-era choice, and the one part of this arrangement that didn't survive. Keys and values are the expensive things to keep around, so modern models hand each head its own query but make groups of heads share a key and value — [grouped-query attention](/wiki/ai/llm/grouped-query-attention), which the [KV cache](/wiki/ai/llm/kv-cache) page's memory arithmetic explains the motive for.

The point is division of labour. A head has exactly one attention pattern per row, so it can chase one relationship — "the noun this adjective modifies," "the previous occurrence of this token." Twelve heads means twelve at once.

They specialize sharply, and *wildly* unevenly. "Attention is 12 heads per block" suggests twelve comparable contributors. The ablation curve says otherwise: most heads are nearly free to delete, a few are catastrophic, and the catastrophic ones cluster in block 0 — the earliest reads, which everything to their right is built on.

## Check yourself

[Ablate heads](/wiki/ai/llm/running-the-checks) one at a time in GPT-2 small: zero head *h* of block *b*, measure [perplexity](/wiki/ai/llm/perplexity) on a few hundred tokens of WikiText, restore, repeat for all 144. Median damage is under 1%, and about twenty heads make perplexity *better* when deleted. Then look at the tail: block 0 head 10, on its own, takes perplexity from ~26 to ~145. The distribution isn't long-tailed so much as vertical.

## Depends on / leads to

Depends on [Q/K/V](/wiki/ai/llm/qkv-projections). Leads to [the MLP](/wiki/ai/llm/the-mlp), the other half of a block.
