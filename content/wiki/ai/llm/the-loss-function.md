---
title: "The Loss Function"
weight: 230
---

One number trains the entire model: the negative log-probability the model assigned to the token that actually came next, averaged over every row.

```text
loss = −(1/n) Σ log p(actual next token | rows above)
```

That's cross-entropy, and it's the *only* signal. Nobody tells the model what a verb is, that Paris is in France, or which of two continuations reads better. It's told, at each of a trillion positions, how much probability it put on the token that turned up.

Get the scale straight. A model guessing uniformly across the 50,257-token vocabulary scores `ln(50257) = 10.82`. GPT-2 small measures 3.28 on WikiText-2. Exponentiate the loss and you get **perplexity** — roughly, how many tokens it's choosing between. Uniform is 50,257. GPT-2 small is 26.

Cross-entropy rewards calibration, not just correctness. Putting 0.99 on the right token beats 0.6; putting 0.99 on the *wrong* one costs at least 4.6, where an honest 0.6 on the right one costs 0.5. Confident and wrong is punished nine times harder than hedging, and worse still if the leftover mass is spread thin. A model that knows what it doesn't know scores better, which is why base models are well-calibrated before we train that out of them.

Nearly every row contributes: a 1024-token sequence yields 1023 supervised predictions from one forward pass — every row but the last, which has no next token to check. That's [the causal mask](/wiki/ai/llm/causal-mask) paying for itself.

## Check yourself

`model(ids, labels=ids).loss` must equal `F.cross_entropy(logits[:, :-1].flatten(0, 1), ids[:, 1:].flatten())` — HuggingFace shifts the labels internally. Compute both; they agree exactly. Skip the shift and you get 12.9 instead of 3.3 — the most common bug in a from-scratch implementation.

## Depends on / leads to

Depends on [softmax and temperature](/wiki/ai/llm/softmax-and-temperature). Leads to [backprop through one weight](/wiki/ai/llm/backprop-one-weight).
