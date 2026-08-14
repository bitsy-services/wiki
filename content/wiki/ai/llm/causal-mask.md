---
title: "The Causal Mask"
weight: 150
---

A row may not read the rows below it. Before the softmax, every score pointing at a row further down the sequence is set to −∞, so its weight comes out exactly 0. That's the mechanism: a triangle of −∞ added to the score matrix.

The reason is training. One forward pass over a 1024-token sequence makes a prediction at every row — 1023 of which have a next token to score against. If row 5 could see row 6, the answer to "what follows row 5?" would be sitting in the input, the loss would go to zero, and the model would learn nothing. The mask is what makes training on every position at once honest.

It buys a second thing for free. A row can only depend on itself and the rows above it, so a row is **final** once computed — appending tokens below cannot change it. That invariant is what the [KV cache](/wiki/ai/llm/kv-cache) is built on, and what "autoregressive" actually means.

The mask sits on the scores, *before* the softmax. You could zero the weights after and renormalize — same numbers — but nobody does: masking first is cheaper and numerically safer.

## Check yourself

Run [GPT-2 small](/wiki/ai/llm/gpt-2) on `"the cat sat on the"`, keep [`hidden_states[6][0, 2]`](/wiki/ai/llm/running-the-checks), then run `"the cat sat on the mat, which was"` — same prefix, more rows below — and pull it again. `torch.allclose` passes. It is *not* bit-identical: float32 reductions change order with sequence length, and the drift grows rightward to ~1e-5 by block 11. The invariant is exact in real arithmetic, approximate in floats. A leak would show up as a large difference, not a rounding one.

## Depends on / leads to

Depends on [one attention head](/wiki/ai/llm/one-attention-head). Leads to [the KV cache](/wiki/ai/llm/kv-cache) and [training vs inference parallelism](/wiki/ai/llm/training-vs-inference-parallelism).
