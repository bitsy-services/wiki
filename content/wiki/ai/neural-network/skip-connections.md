---
title: "Skip Connections"
weight: 60
---

A skip connection is the decision to *add* a layer's output to its input rather than replace it. It is what makes a deep stack trainable at all, and the reason a layer can leave alone the parts of its input it has nothing to say about — instead of having to rebuild everything worth keeping from whatever its predecessor handed over.

## Why deep stacks refused to train

Skip connections were invented for image classifiers, and the problem they solved is one every deep stack has. For a while, deeper networks were simply worse.

The obvious guess is overfitting: more capacity, better memorization, worse generalization. That is not what was happening. Deeper networks did worse **on the training set** — the one thing extra capacity is supposed to guarantee you can fit. In the 2015 result that made this famous, a 56-layer image classifier was beaten by an otherwise identical 20-layer one on data both were staring directly at. The problem was optimization, not capacity: the deeper model contained a perfectly good shallow model as a special case and could not find it.

Normalization was already available and did not fix it. Those networks used [BatchNorm](/wiki/ai/neural-network/normalization#what-layernorm-does) throughout — published earlier the same year and the standard tool of the day — and still degraded. Keeping the numbers well-scaled turns out to be a separate problem from getting gradient signal down a long chain, and solving the first leaves the second untouched.

The diagnosis was that every layer had to actively reproduce whatever it wanted to preserve. If layer 30 receives something useful and its job is to pass it along mostly intact, it must learn a near-identity map — and learning to do nothing, exactly, is a surprisingly hard target to hit with a matrix.

## The fix, written down

```text
  x = x + f(norm(x))
      └── the "+" is the skip connection
```

`f` is whatever the layer computes — one matrix and a bend, or something far more elaborate. Whatever it is, its output is *added* to what came in rather than handed on in place of it.

Do that at every layer and what travels through the network is a running total of every contribution made so far. In a transformer that total has its own name and its own page: [the residual stream](/wiki/ai/llm/residual-stream).

It does two jobs. The second is the one usually named; the first is the one that answers the 56-layer result above.

**It makes "do nothing" the default.** A layer whose output is all zeros is now exactly the identity, for free, with no weights required to achieve it. So a new layer starts out harmless and learns a *correction* to the running total rather than having to earn back what its predecessors built. Learning to add nothing is easy; learning to copy perfectly is not.

**It gives the gradient a road home.** Differentiate `out = in + f(in)` and you get `1 + f′`. The gradient reaching any layer is [a sum over every path back to the loss](/wiki/ai/neural-network/backprop-one-weight#it-is-a-sum-over-paths-not-a-product), and one of those paths runs straight down the running total — derivative 1, all the way, touching no layer's weights on the journey. Chain a dozen layers *without* skips and the gradient is instead a product of a dozen Jacobians — the matrix of partial derivatives of each layer's output with respect to its input — which is a quantity with no reason to stay near 1 and every opportunity to drift toward 0.

## What actually happens if you remove them

A modern pre-norm model has both mechanisms, so removing one produces a gentler failure than the textbook account predicts.

Strip the skips out of a [normalized](/wiki/ai/neural-network/normalization) 12-block model and the gradients don't vanish. Nothing dramatic happens at all. It still trains, perfectly stably, to a clearly worse loss, and then stops improving. The damage shows up as a ceiling, not a crash.

Skip connections aren't what keeps the arithmetic from blowing up — normalization handles that. They're what makes depth *pay*, by letting each layer contribute an increment instead of re-justifying everything worth keeping.

## Check yourself

In [nanoGPT](/wiki/ai/llm/running-the-checks), delete *both* skips in every block (`x = attn(ln(x))`, then `x = mlp(ln(x))`) and train on char-level Shakespeare. With skips, loss falls 5.0 → 2.4; without, 5.0 → 3.4, where it flattens. Don't bother watching gradient norms: with LayerNorm in place they don't decay toward block 0 at all. The vanishing-gradient story is about *unnormalized* networks, not this one.

## Depends on / leads to

Depends on [normalization](/wiki/ai/neural-network/normalization), the other half of what makes depth trainable. Leads to [the loss function](/wiki/ai/neural-network/the-loss-function), where training starts.
