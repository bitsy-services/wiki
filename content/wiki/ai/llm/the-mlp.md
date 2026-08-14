---
title: "The MLP"
weight: 170
---

[Attention](/wiki/ai/llm/attention) moves information between rows. The MLP is what the block does *to* a row once it has what it needs — and it never looks at another row.

Mechanically it's two matrices with a nonlinearity between them: 768 → 3072, [GELU](/wiki/ai/llm/activations), 3072 → 768. That widening is the **MLP bulge**, the only place in the model where a row isn't `d_model` wide. Nothing mixes across rows on the way through; each row goes in and comes back alone.

The useful reading is detect-and-write. Take one of the 3072 hidden units. Its input weights define a direction in the row's space, and the unit lights up when the row points that way — GELU squashes everything else toward zero, so it's a detector with a soft threshold, not a proportional readout. Its output weights define a *different* direction, which it writes into the [residual stream](/wiki/ai/llm/residual-stream), scaled by how hard it fired. Detect a feature, write a feature. Three thousand of those, per block. (The literature calls this a key-value memory. Nothing to do with attention's keys and values, or with the [KV cache](/wiki/ai/llm/kv-cache).)

And that's where the parameters live. Attention in a [GPT-2](/wiki/ai/llm/gpt-2) block is four 768×768 matrices, about 2.4M weights. The MLP is two 768×3072 matrices, about 4.7M. Two-thirds of every block — and most of what the model knows — sits in the bulge, which tends to surprise people who have spent all their attention on attention.

## Check yourself

[Sum the parameters](/wiki/ai/llm/running-the-checks) in GPT-2 small whose names contain `mlp`, and compare against the total excluding `wte` and `wpe`. You'll get 56.7M of 85.1M non-embedding parameters — 66.6%, two-thirds to the decimal — against 28.3M in attention.

## Depends on / leads to

Depends on [the residual stream](/wiki/ai/llm/residual-stream). Leads to [GELU and SwiGLU](/wiki/ai/llm/activations) — the nonlinearity in the middle, and the reason the bulge isn't refunded — then [LayerNorm and RMSNorm](/wiki/ai/llm/normalization) and [mixture of experts](/wiki/ai/llm/mixture-of-experts).
