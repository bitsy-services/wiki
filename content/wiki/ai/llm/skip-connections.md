---
title: "Skip Connections"
weight: 190
---

A skip connection is the decision to *add* a piece of the model's output to its input rather than replace it. That sounds like a wiring detail and is closer to a load-bearing wall. It is what makes a deep stack of blocks trainable at all, it is why [the residual stream](/wiki/ai/llm/residual-stream) exists as something to talk about, and it is the reason a block can leave alone the parts of a row it has nothing to say about — instead of having to rebuild everything worth keeping from whatever its predecessor handed over.

## Why deep stacks refused to train

Skip connections predate transformers, and the problem they were invented for is worth borrowing, because it is exactly the problem a twelve-block stack would otherwise have. For a while, deeper networks were simply worse — and not in the way anyone expected.

The obvious guess is overfitting: more capacity, better memorization, worse generalization. That is not what was happening. Deeper networks did worse **on the training set** — the one thing extra capacity is supposed to guarantee you can fit. In the 2015 result that made this famous, a 56-layer image classifier was beaten by an otherwise identical 20-layer one on data both were staring directly at. The problem was optimization, not capacity: the deeper model contained a perfectly good shallow model as a special case and could not find it.

Normalization was already available and did not fix it. Those networks used **BatchNorm** — normalizing each feature across the examples in a training batch, published earlier the same year and the standard tool of the day — throughout, and still degraded. Keeping the numbers well-scaled turns out to be a genuinely separate problem from getting gradient signal down a long chain, and solving the first leaves the second untouched. That distinction is the one to carry into the rest of this page.

The diagnosis was that every layer had to actively reproduce whatever it wanted to preserve. If layer 30 receives something useful and its job is to pass it along mostly intact, it must learn a near-identity map — and learning to do nothing, exactly, is a surprisingly hard target to hit with a matrix.

## The fix, written down

```text
  row = row + attention(norm(row))
      └── the "+" is the skip connection
```

The block's output is added to what came in. The stream *is* the accumulated skip path — that identity is the whole reason the residual stream page exists.

It does two jobs, and they are worth keeping apart because people tend to know about the second and not the first.

**It makes "do nothing" the default.** A block whose attention and MLP output zeros is now exactly the identity, for free, with no weights required to achieve it. So a new block starts out harmless and learns a *correction* to the running total rather than having to earn back what its predecessors built. Learning to add nothing is easy; learning to copy perfectly is not.

**It gives the gradient a road home.** Differentiate `out = in + f(in)` and you get `1 + f′`. The gradient reaching any block is a sum over every path back to the loss, and one of those paths runs straight down the stream — derivative 1, all the way, touching no block's weights on the journey. Chain a dozen blocks *without* skips and the gradient is instead a product of a dozen Jacobians — the matrix of partial derivatives of each block's output with respect to its input — which is a quantity with no reason to stay near 1 and every opportunity to drift toward 0.

## What actually happens if you remove them

A modern pre-norm model has both mechanisms, so the failure is gentler than the textbook version leads you to expect — and it's worth knowing that, because the textbook version will send you looking for the wrong evidence.

Strip the skips out of a [normalized](/wiki/ai/llm/normalization) 12-block model and the gradients don't vanish. Nothing dramatic happens at all. It still trains, perfectly stably, to a clearly worse loss, and then stops improving. The damage shows up as a ceiling, not a crash.

That's the honest payoff. Skip connections aren't what keeps the arithmetic from blowing up — normalization handles that. They're what makes depth *pay*, by letting each block contribute an increment instead of re-justifying the whole row.

## Check yourself

In [nanoGPT](/wiki/ai/llm/running-the-checks), delete *both* skips in every block (`x = attn(ln(x))`, then `x = mlp(ln(x))`) and train on char-level Shakespeare. With skips, loss falls 5.0 → 2.4; without, 5.0 → 3.4, where it flattens. Don't bother watching gradient norms: with LayerNorm in place they don't decay toward block 0 at all. The vanishing-gradient story is about *unnormalized* networks, not this one.

## Depends on / leads to

Depends on [the residual stream](/wiki/ai/llm/residual-stream) and [normalization](/wiki/ai/llm/normalization). Leads to [backprop through one weight](/wiki/ai/llm/backprop-one-weight).
