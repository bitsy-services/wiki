---
title: "The KV Cache"
weight: 260
---

Generating token 500 means running a forward pass over 499 rows to produce one new row. Do that naively for every token and you rebuild the entire prefix each time — the same keys and values, from the same unchanged rows, again and again.

[The causal mask](/wiki/ai/llm/causal-mask) says you don't have to. A row can only depend on itself and the rows above it, so once a row is computed it's final: nothing you append below can change it, and its key and value are constants. Keep them.

With the cache, each new token does one row's worth of work — project it to q/k/v, append its k and v, attend against the cache, run the MLP. Attending to *n* rows still costs O(n), but you've dropped a whole factor of *n* off every step.

The price is memory, and it's linear in context. Two tensors per block per row: for [GPT-2 small](/wiki/ai/llm/gpt-2) that's 2 × 12 × 768 = 18,432 numbers per token, 36 KB in fp16. A 100k-token context runs to 3.7 GB — which is why long context is a *memory* problem before a compute one, and why [prompt caching](/wiki/ai/prompt-caching) is something a provider can sell you: they keep your prefix's keys and values warm so you don't rebuild them.

## Check yourself

[Generate](/wiki/ai/llm/running-the-checks) greedily from GPT-2 small with `use_cache=True`, then `False`. The tokens come out identical — the cache is an optimization, not an approximation. The speedup is smaller than you'd guess and grows with context: ~2× at 200 tokens, ~4.8× at 1000. Decode is bound by reading the 124M weights, which both runs do; the cache only removes attention work.

## Depends on / leads to

Depends on [the causal mask](/wiki/ai/llm/causal-mask). Leads to [grouped-query attention](/wiki/ai/llm/grouped-query-attention) — the standard way to make this cache smaller — then [training vs inference parallelism](/wiki/ai/llm/training-vs-inference-parallelism) and [context length and the O(n²) cost](/wiki/ai/llm/context-length).
