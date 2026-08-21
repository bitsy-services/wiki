---
title: "LayerNorm and RMSNorm"
weight: 180
---

Normalization is the housekeeping that keeps a transformer's numbers in a range its arithmetic can actually work in. As a row travels through the model every block adds something to it and nothing ever takes anything away, so the numbers grow — and by the far end they are enormous compared with where they started. Left alone that wrecks training: each part of the model would face inputs of wildly varying scale depending on how far along it sat, and the gradients that train it would swing between vanishing and exploding. A norm rescales a copy of the row to a standard size before anything reads it. It is the least interesting mechanism in the architecture and one of the few that everything else quietly depends on.

## The problem: the stream grows without bound

[The residual stream](/wiki/ai/llm/residual-stream) is additive by construction. Every block adds its attention result and its MLP result on top of what was already there, and there is no subtraction, no decay, no rescaling step built into the path. Contributions accumulate.

They accumulate a *lot*. In [GPT-2 small](/wiki/ai/llm/gpt-2) the last row's length starts around 5 coming out of the embedding and is into the hundreds by the final blocks — a factor of fifty or so across twelve blocks.

Now consider block 11's attention trying to read that. It was trained on inputs of some typical size; hand it numbers fifty times larger and its scores don't grow fifty-fold, they grow *two and a half thousand*-fold — a score is a query dotted with a key, and both of those are read off the same oversized row, so the score scales with the **square** of its magnitude. [Softmax saturates](/wiki/ai/llm/softmax-and-temperature) long before that, and the gradient flowing back through it goes to nearly nothing. The model would have to learn a different effective scale at every depth, and re-learn it every time the scale drifted during training. It's a mess, and it's entirely avoidable.

## What LayerNorm does

Take the row's numbers, subtract their mean, and divide by their standard deviation. The result has mean 0 and variance 1 whatever went in. Then scale and shift it by two learned vectors — one multiplier and one offset per feature — so the model can undo as much of the standardization as it turns out to want.

The crucial scoping detail: it works **within a row**, along the feature axis, across the 768 numbers belonging to one token position. It never looks across rows. That's not a performance choice, it's a correctness one — a norm that pooled statistics across positions would carry information from later tokens into earlier ones and quietly defeat [the causal mask](/wiki/ai/llm/causal-mask).

(The name is historical and actively unhelpful here. LayerNorm normalizes a row, not a [block](/wiki/ai/llm/glossary).)

## Pre-norm: the copy is normalized, not the stream

Where the norm sits matters more than what it does, and this is the detail most worth reading slowly.

[GPT-2](/wiki/ai/llm/gpt-2) is **pre-norm**: the norm is applied to the copy that attention reads, *inside* the parenthesis, and never to the stream itself.

```text
  pre-norm  (GPT-2 and everything since)
      row = row + attention(norm(row))
                            └── normalized copy; the stream keeps its own scale

  post-norm (the original 2017 transformer)
      row = norm(row + attention(row))
            └── the stream itself is rescaled at every block
```

So under pre-norm the stream is never normalized in place. It keeps whatever magnitude it has accumulated and goes on growing rightward, and each consumer takes a well-conditioned copy for its own use. Exactly once, at the right edge, a final norm rescales it before [the unembedding](/wiki/ai/llm/unembedding-and-logits) reads it.

The original transformer did it the other way round, and pre-norm displaced it for a practical reason: post-norm models are difficult to start. Rescaling the stream at every block interrupts the clean additive path the gradient travels home on, and post-norm transformers famously need a learning-rate warmup period to train at all, where pre-norm ones mostly just train. Nobody builds post-norm any more.

## RMSNorm: the half that was doing the work

**RMSNorm** drops the mean subtraction and the learned offset. Divide by the root mean square of the row's numbers, scale by a learned vector, done.

That removes one pass over the row and one learned parameter per feature, and costs nothing measurable in quality — which is why Llama and essentially everything since uses it. The centering was never earning its keep. Rescaling was the whole point; recentering came along for the ride because LayerNorm was borrowed from a setting where it mattered more.

The payoff of all of this is unglamorous and total: normalization is what lets you stack blocks at all. Without it, depth is a numerical accident waiting to happen; with it, the twelfth block sees inputs that look much like the first block's, and you can keep going.

## Check yourself

[Print](/wiki/ai/llm/running-the-checks) the L2 norm of the *last* row of `hidden_states[i]` for i = 0…11. Mind the off-by-one: those are the embedding and blocks 0–10, not blocks 1–12. The norm climbs the whole way, ~5 → ~220. Do *not* include `hidden_states[12]` — HuggingFace has already run the final norm on it, and the number goes back down. That drop is itself the check on the pre-norm claim: the only place the stream is ever rescaled in place is the right edge.

## Depends on / leads to

Depends on [the residual stream](/wiki/ai/llm/residual-stream). Leads to [skip connections](/wiki/ai/llm/skip-connections).
