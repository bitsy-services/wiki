---
title: "LayerNorm and RMSNorm"
weight: 50
---

Normalization is the housekeeping that keeps a network's numbers in a range its arithmetic can actually work in. Nothing constrains the scale of what comes out of a layer: it depends on the weights, which training is busy changing, and whatever drift one layer introduces the next one inherits and compounds. Left alone that wrecks training — each layer faces inputs of wildly varying scale depending on where it sits and how far along the run is, and the gradients that train it swing between vanishing and exploding. A norm rescales the numbers to a standard size before anything reads them. It is the least interesting mechanism in a network and one of the few that everything else quietly depends on.

## The problem: scale drifts, and sometimes only grows

In a plain stack the drift is a random walk: each layer multiplies by a matrix that might on average enlarge or shrink what passes through, and twelve of those compound. Nothing pulls it back to where it started.

In an architecture whose layers *add* to a running total rather than replacing it — which most deep architectures now are, for [reasons of their own](/wiki/ai/neural-network/skip-connections) — the drift is not even a walk. It is monotonic. Every layer adds its contribution on top of what was already there, there is no subtraction and no decay anywhere on the path, and so the numbers only ever grow.

They grow a *lot*. In [GPT-2 small](/wiki/ai/llm/gpt-2), the vector travelling through the model starts around length 5 coming out of the [embedding](/wiki/ai/llm/embeddings) and is into the hundreds by the final layers — a factor of fifty or so across twelve of them.

Now consider the last layer trying to read that. It was trained on inputs of some typical size; hand it numbers fifty times larger and anything quadratic in its input — and there is usually something, since networks routinely multiply two quantities that both scale with the input — grows *two and a half thousand*-fold instead. Whatever sits downstream of that saturates, and the gradient flowing back through it goes to nearly nothing. The model would have to learn a different effective scale at every depth, and re-learn it every time the scale drifted during training. It's a mess, and it's entirely avoidable.

## What LayerNorm does

Take the numbers, subtract their mean, and divide by their standard deviation. The result has mean 0 and variance 1 whatever went in. Then scale and shift it by two learned vectors — one multiplier and one offset per feature — so the model can undo as much of the standardization as it turns out to want.

The scoping is the part worth getting right, because there are two obvious things to average over and they give different mechanisms:

- **LayerNorm** pools statistics *within one example*, across its features. Each example is normalized by its own numbers and nothing else's.
- **BatchNorm** pools statistics *across the examples in a training batch*, one feature at a time. It came first, in 2015, and dominated image models for years.

BatchNorm's problem is that an example's output depends on which other examples it happened to be batched with — fine during training, awkward at inference, where you must fall back on running averages collected earlier, and worse still when batches are small or examples within one batch must not influence each other. In a language model that last point is fatal: pooling statistics across positions would carry information from later tokens into earlier ones and quietly defeat [the causal mask](/wiki/ai/llm/causal-mask). LayerNorm has no such coupling, which is why sequence models use it throughout.

(The name is historical and actively unhelpful. LayerNorm normalizes one example's features. It does not normalize a layer.)

## Where the norm sits

In an architecture that adds rather than replaces, there is a real choice about *where* the norm goes, and it turned out to matter more than what the norm does.

```text
  pre-norm   (the modern default)
      x = x + f(norm(x))
                └── f reads a normalized copy; the running total keeps its own scale

  post-norm  (the original 2017 transformer)
      x = norm(x + f(x))
          └── the running total itself is rescaled at every layer
```

Under pre-norm the running total is never normalized in place. It keeps whatever magnitude it has accumulated and goes on growing, and each consumer takes a well-conditioned copy for its own use. Exactly once, at the very end, a final norm rescales it before the output layer reads it.

The original transformer did it the other way round, and pre-norm displaced it for a practical reason: post-norm models are difficult to start. Rescaling the running total at every layer interrupts the clean additive path the gradient travels home on — the [skip connections](/wiki/ai/neural-network/skip-connections) page is about why that path matters — and post-norm transformers famously need a learning-rate warmup period to train at all, where pre-norm ones mostly just train. Nobody builds post-norm any more.

## RMSNorm: the half that was doing the work

**RMSNorm** drops the mean subtraction and the learned offset. Divide by the root mean square of the numbers, scale by a learned vector, done.

That removes one pass over the data and one learned parameter per feature, and costs nothing measurable in quality — which is why Llama and essentially everything since uses it. The centering was never earning its keep. Rescaling was the whole point; recentering came along for the ride because LayerNorm was borrowed from a setting where it mattered more.

The payoff of all of this is unglamorous and total: normalization is what lets you stack layers at all. Without it, depth is a numerical accident waiting to happen; with it, the twelfth layer sees inputs that look much like the first layer's, and you can keep going.

## Check yourself

Watch the scale climb, and watch the one place it gets reset.

[Print](/wiki/ai/llm/running-the-checks) the L2 norm of the last row of `hidden_states[i]` for i = 0…11 in GPT-2 small. Mind the off-by-one: those are the embedding and blocks 0–10, not blocks 1–12. The norm climbs the whole way, ~5 → ~220 — that is the monotonic growth this page opened with, measured.

Do *not* include `hidden_states[12]` — HuggingFace has already run the final norm on it, and the number goes back down. That drop is itself the check on the pre-norm claim: the only place the running total is ever rescaled in place is the very end.

## Depends on / leads to

Depends on [the MLP](/wiki/ai/neural-network/multi-layer-perceptron) and [the bend](/wiki/ai/neural-network/bend). Leads to [skip connections](/wiki/ai/neural-network/skip-connections), the other half of what makes depth trainable.
