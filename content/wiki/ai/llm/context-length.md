---
title: "Context Length and the O(n²) Cost"
weight: 290
---

Every row scores every row it can see: an n × n matrix of scores, per head, per block — the only thing in a transformer that grows quadratically with the sequence.

Everything else is linear: projections, MLP, and norms chew one row at a time, so doubling the context doubles their work. [Attention](/wiki/ai/llm/attention)'s score matrix and its weighted sum *quadruple*.

So the famous O(n²) is a **crossover**, not a flat tax. Per block the quadratic part costs about `4n²·d_model` (the full n × n; a good kernel skips the masked half and pays half that), the linear part — projections plus MLP — about `24n·d_model²`. Equal at `n ≈ 6·d_model`: ~4,600 tokens for [GPT-2 small](/wiki/ai/llm/gpt-2), ~9,200 causal-only. Below that the MLP dominates; above it, attention *is* the bill. Nobody worried about this in 2019 with a 1024-token window; everybody does now.

FlashAttention doesn't repeal this: it removes the *memory* cost of materializing the n × n matrix — the binding constraint in practice — but the FLOPs stay quadratic.

And the [KV cache](/wiki/ai/llm/kv-cache) grows linearly, which usually stops you first: memory runs out before patience does. This is the arithmetic under [context engineering](/wiki/ai/context-engineering): a token isn't free, and the marginal one costs more than the last.

## Check yourself

Count FLOPs; don't trust a stopwatch. The score matmul's FLOPs quadruple per doubling of n, while a full GPT-2 small forward pass at n = 128 → 1024 grows only ~1.1–1.5× per doubling — you're below the crossover. Time that matmul and the wall-clock won't quadruple cleanly: small n is overhead-bound, and past n ≈ 1024 the score matrix falls out of cache and jumps by *more* than 4×.

## Depends on / leads to

Depends on [the KV cache](/wiki/ai/llm/kv-cache) and [RoPE](/wiki/ai/llm/rope). Leads to [mixture of experts](/wiki/ai/llm/mixture-of-experts).
