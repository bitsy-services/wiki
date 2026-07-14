---
title: "Training vs Inference Parallelism"
weight: 280
---

The same weights, run two completely different ways.

**Training does every row at once.** One forward pass over 1024 tokens computes all 1024 rows in parallel and scores 1023 next-token predictions — [the causal mask](/wiki/ai/llm/causal-mask) is what makes that legal. The GPU is doing enormous matmuls, it's compute-bound, and that's why training is a throughput problem you solve with more FLOPs.

**Inference can't.** Token 501 depends on token 500, which you have to sample first. Generation is strictly serial: one row, one forward pass, repeat. And with a [KV cache](/wiki/ai/llm/kv-cache) the arithmetic per row is trivial — you push a single 768-wide row through 124M weights and get about one multiply out of each. Every weight is read; none is *reused*. The parallel pass reads exactly the same weights and reuses each one a thousand times over. That difference — arithmetic intensity, not FLOPs — is what makes decode memory-bandwidth-bound.

Three consequences fall out. Batching is enormously effective at inference, because many sequences amortize one read of the weights. Prefill (chewing through the prompt) is parallel and fast, like training; decode (emitting tokens) is serial and slow — different regimes, profiled separately. And [speculative decoding](/wiki/ai/llm/speculative-decoding) exists to convert some serial decode back into parallel verify.

## Check yourself

Time GPT-2 small on 1024 tokens as one forward pass, then time generating 1024 tokens one at a time with the cache on. Same model, same token count. On CPU the forward pass wins by roughly 10×. On a GPU — where the parallel pass consumes FLOPs that were sitting idle anyway — it's two orders of magnitude. The hardware decides the size of the gap; nothing makes it vanish.

## Depends on / leads to

Depends on [the causal mask](/wiki/ai/llm/causal-mask) and [the KV cache](/wiki/ai/llm/kv-cache). Leads to [speculative decoding](/wiki/ai/llm/speculative-decoding).
