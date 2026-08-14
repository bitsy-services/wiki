---
title: "Weight Sharing Across Positions"
weight: 250
---

There is no "block 6 for position 300." Every row runs through the *same* weights: one set of Q/K/V matrices, one MLP, per block, applied identically at position 1 and position 900.

This isn't a memory optimization. It's what makes the thing a language model instead of a lookup table indexed by position. Whatever "attend to the subject of this clause" costs to learn, it's learned once and works everywhere — and gradients from every position in every sequence pile into the same matrices, which is why [one sequence teaches a weight a thousand times over](/wiki/ai/llm/backprop-one-weight).

The consequence people miss: **no weight inside a block knows how long the sequence is.** Doubling the window costs compute and [KV cache](/wiki/ai/llm/kv-cache) memory, but not one extra parameter in any attention or MLP matrix.

With one exception, and it's the interesting one. [GPT-2](/wiki/ai/llm/gpt-2) learns an absolute [positional](/wiki/ai/llm/positional-encoding) vector per position — `wpe`, shaped `[1024, 768]` — the only weight in the model with a position axis. Widen the context to 4096 and `wpe` grows by 2.4M parameters while every block stays byte-for-byte the size it was. That table is also what stops GPT-2 at 1024 tokens. Not the blocks: they'd happily process row 5000. There's just no vector to tell row 5000 where it is — precisely the limitation [RoPE](/wiki/ai/llm/rope) removes.

## Check yourself

[List the parameters](/wiki/ai/llm/running-the-checks) of GPT-2 small whose shape mentions 1024: `[n for n, p in model.named_parameters() if 1024 in p.shape]`. You get `transformer.wpe.weight`, and nothing else. Every other weight in the model is blind to how long the sequence is.

## Depends on / leads to

Depends on [backprop through one weight](/wiki/ai/llm/backprop-one-weight). Leads to [the KV cache](/wiki/ai/llm/kv-cache) and [positional encoding](/wiki/ai/llm/positional-encoding).
