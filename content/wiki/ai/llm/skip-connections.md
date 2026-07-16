---
title: "Skip Connections"
weight: 190
---

The `+` in `row = row + attention(norm(row))` is the skip connection, and it's the reason the [residual stream](/wiki/ai/llm/residual-stream) exists. The stream *is* the accumulated skip path.

It does two jobs.

**It makes "do nothing" the default.** A block whose attention and MLP output zeros is the identity, so a new block starts out harmless and learns a correction instead of having to earn back what its predecessors built. That is the argument for the [residual stream](/wiki/ai/llm/residual-stream) and it's made there; the `+` is simply the thing that does it.

**It gives the gradient a road home.** Differentiate `out = in + f(in)` and you get `1 + f′`. The gradient at any block is a sum over paths back to the loss, and one of those paths runs straight down the stream: derivative 1, touching no block's weights at all. Chain a dozen blocks *without* skips and the gradient is a product of a dozen Jacobians instead. Historically that's what killed deep networks, and it's why residual connections arrived before normalization did.

A modern pre-norm model has both, so the failure is gentler than the textbook version: strip the skips out of a normalized 12-block model and the gradients don't vanish. It still trains — to a much worse loss, where it stops.

## Check yourself

In nanoGPT, delete *both* skips in every block (`x = attn(ln(x))`, then `x = mlp(ln(x))`) and train on char-level Shakespeare. With skips, loss falls 5.0 → 2.4; without, 5.0 → 3.4, where it flattens. Don't bother watching gradient norms: with LayerNorm in place they don't decay toward block 0 at all. The vanishing-gradient story is about *unnormalized* networks, not this one.

## Depends on / leads to

Depends on [the residual stream](/wiki/ai/llm/residual-stream) and [normalization](/wiki/ai/llm/normalization). Leads to [backprop through one weight](/wiki/ai/llm/backprop-one-weight).
