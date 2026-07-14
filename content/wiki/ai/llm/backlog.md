---
title: "Backlog"
weight: 30
---

The syllabus, in dependency order. Each item becomes one page under the [contract](/wiki/ai/llm): one concept, under 300 words, one check you can run. A page is readable as soon as the ones above it are.

- [x] [Tokenization](/wiki/ai/llm/tokenization) — text becomes integers
- [x] [Embeddings](/wiki/ai/llm/embeddings) — an integer indexes a learned row
- [x] [The residual stream](/wiki/ai/llm/residual-stream) — the row as a bus
- [ ] One attention head — a row reading the rows above it
- [ ] Q/K/V as three projections
- [ ] The causal mask
- [ ] Multi-head attention
- [ ] The MLP — the bulge, and what a neuron in it does
- [ ] LayerNorm / RMSNorm
- [ ] Skip connections — why the stream is additive
- [ ] The unembedding and logits
- [ ] Softmax and temperature
- [ ] Sampling strategies — greedy, top-k, top-p
- [ ] The loss function — cross-entropy against the next token
- [ ] Backprop through one weight
- [ ] Weight sharing across positions
- [ ] The KV cache — from outside, this is [prompt caching](/wiki/ai/prompt-caching)
- [ ] Positional encoding and RoPE
- [ ] Training vs inference parallelism
- [ ] Context length and the O(n²) cost — the arithmetic under [context engineering](/wiki/ai/context-engineering)
- [ ] Mixture of experts
- [ ] Superposition — more features than dimensions
- [ ] Fine-tuning
- [ ] RLHF
- [ ] Speculative decoding — a small model guesses, a big one checks

## Depends on / leads to

Depends on [conventions](/wiki/ai/llm/conventions) and the [glossary](/wiki/ai/llm/glossary). Leads to all of the above.
