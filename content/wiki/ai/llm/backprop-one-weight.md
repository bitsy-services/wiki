---
title: "Backprop Through One Weight"
weight: 240
---

Pick one number out of GPT-2 small's 124 million — a single entry `w` in block 6's MLP input matrix. Backprop answers exactly one question about it: *if I nudge `w` up a hair, does the loss go up or down, and how fast?* That's `∂L/∂w`. Training is that answer, applied to every weight, a few hundred thousand times.

The chain rule gets it there in one sweep. The [loss](/wiki/ai/llm/the-loss-function) is computed at the right edge; its gradient flows right to left, and at each operation the gradient arriving from the right is multiplied by that operation's local derivative. By the time it reaches `w`, the number is a **sum over every path** from `w` to the loss — through the [skip connections](/wiki/ai/llm/skip-connections), through every block to its right — each path a product of local derivatives. It's a sum, not a product. Think "product" and you've reinvented the vanishing gradient that skips exist to prevent.

It's also a sum over *rows*: `w` was used at every position ([the same weights run everywhere](/wiki/ai/llm/weight-sharing)), and its gradient adds up every one of those contributions. A single sequence gives `w` a thousand votes.

Then `w ← w − lr · ∂L/∂w`. Adam, momentum, warmup — all refinements of how much to trust that one number.

## Check yourself

Take a single weight in nanoGPT and record autograd's gradient. Now compute it by hand: `(L(w+ε) − L(w−ε)) / 2ε`, `ε = 1e-3`, same batch, model in `eval()` (dropout will destroy the difference), cross-entropy computed yourself in float64. The two agree to ~7 significant figures. That's the standard gradient check, and it's the fastest way to prove a hand-written backward pass wrong.

## Depends on / leads to

Depends on [the loss function](/wiki/ai/llm/the-loss-function) and [skip connections](/wiki/ai/llm/skip-connections). Leads to [weight sharing across positions](/wiki/ai/llm/weight-sharing).
