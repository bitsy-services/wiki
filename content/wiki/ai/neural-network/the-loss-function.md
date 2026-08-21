---
title: "The Loss Function"
weight: 70
---

The loss function is the single number that trains the entire network. Once the model has produced an answer, the loss asks one question: how far was that from the answer that was correct? A confident right answer scores well, a confident wrong answer scores terribly, and everything the model ever learns is a consequence of being pushed, over and over, to make that number smaller. Nothing else is supplied — no rules, no facts, no advice about how to improve.

It is worth being precise about how much rests on this. The architecture decides what the network *can* express; the loss decides what it *will* express. Everything a trained model does is the cheapest way it found to make one number small.

## Where the right answer comes from

Training needs, for each example, something to compare against. Classically that something is a **label** a person produced: this photograph is a cat, this transaction was fraud, this house sold for £340,000. Someone annotated it, which is slow and expensive and the reason most of machine learning's history is a history of small datasets.

The alternative is to find data that already contains its own answer. Hide part of an example and predict it from the rest — the hidden part *is* the label, and nobody had to write it down. That is **self-supervision**, and it is what changed the economics: [predicting the next word in ordinary text](/wiki/ai/llm/why-scale-worked) means every sentence ever written is already labelled, by itself, for free.

Either way the loss function's job is the same, and everything below applies to both.

## Cross-entropy: the negative log of the right answer

When the answer is a choice among a fixed set of options, the standard loss is **cross-entropy**. The network's final layer produces one score per option, [softmax](/wiki/ai/llm/softmax-and-temperature) turns those scores into probabilities that sum to 1, and the loss reads off a single one of them:

```text
loss = −(1/n) Σ log p(correct option)
```

Take the probability the model assigned to the option that turned out to be right, take its logarithm, negate it, and average over every example. That's it.

Each piece is doing something specific. The **log** is there because probabilities multiply across independent predictions and logs turn that into addition — so the loss over a batch is a sum rather than a product that would underflow to zero almost immediately. The **negation** makes lower mean better, since the log of a probability is always negative. The **average** makes batches of different sizes comparable.

The units are *nats*, natural-log units, which is the only reason `ln` shows up rather than `log₂`. Nothing conceptual turns on it, but it's why the numbers below look the way they do.

## Get the scale straight

Cross-entropy numbers are meaningless without knowing how many options there were, because that sets the do-nothing baseline: a model spreading its probability evenly over *k* options scores exactly `ln(k)`.

[GPT-2 small](/wiki/ai/llm/gpt-2) is a convenient illustration, choosing among a [vocabulary](/wiki/ai/llm/glossary) of 50,257. Uniform guessing scores `ln(50257) = 10.82`. The trained model measures 3.28 on WikiText-2. Exponentiate the loss and you get [**perplexity**](/wiki/ai/llm/perplexity) — roughly, how many options the model is effectively choosing between. Uniform is 50,257; GPT-2 small is 26.

The interesting thing about that scale is how compressed the useful part of it is. Getting from "knows nothing" to GPT-2 covers most of the distance from 10.8 down to 3.3, and every advance since has been fought over the remainder. Small absolute movements in loss are large movements in capability, which is worth remembering before dismissing a tenth of a nat.

## It rewards calibration, not just correctness

Cross-entropy does not ask whether the top-ranked option was right. It asks what probability you assigned, and the difference matters enormously.

Putting 0.99 on the right option beats putting 0.6 on it. But putting 0.99 on the *wrong* one costs at least 4.6, where an honest 0.6 on the right one costs 0.5 — confident-and-wrong is punished about nine times harder than hedging, and worse still if the leftover probability was spread thin rather than concentrated on the runner-up.

This is exactly how a weather forecaster is scored properly: not on whether it rained, but on the probability they gave to what happened. Announcing "0% chance of rain" and then getting rained on is ruinous; saying 60% and getting rain is unremarkable. Under that kind of scoring the winning strategy is to report what you actually believe, and to say so less firmly when you know less.

So a model that knows what it doesn't know scores better, and networks trained on cross-entropy tend to come out well-calibrated because the loss paid them to be. That property is fragile: [RLHF](/wiki/ai/llm/rlhf) trains it back out of language models, because human raters prefer answers that sound sure — an effect visible in the before-and-after calibration curves OpenAI published with GPT-4, where a nearly perfectly calibrated base model emerges from preference training markedly overconfident.

## When the answer is a number

Cross-entropy is for choosing among options. When the answer is a quantity — a price, a temperature, a coordinate — the usual loss is **mean squared error**: subtract the prediction from the truth, square it, average.

```text
loss = (1/n) Σ (prediction − truth)²
```

The squaring does the same job the log does in cross-entropy: it makes large errors disproportionately expensive, so the network spends its capacity on the cases it is getting badly wrong rather than shaving the ones it nearly has. It also has a known failure mode — a single wild outlier can dominate the average and drag the whole model toward it, which is why alternatives that grow linearly rather than quadratically once an error gets large are common in practice.

The general shape holds either way. A loss is a statement of what "wrong" means, written so that it is smooth enough to differentiate; [backprop](/wiki/ai/neural-network/backprop-one-weight) does the rest.

## The loss is not the goal

Worth stating plainly, because it is the source of most surprises in practice: the loss is a *proxy*. Nobody wants a small cross-entropy. They want a model that answers questions well, and cross-entropy is a differentiable stand-in chosen partly because it works and partly because the thing anyone actually cares about usually isn't differentiable at all.

Where proxy and goal diverge, the network follows the proxy — it has no access to anything else. Most of the surprising behaviour of trained models is this: a faithful optimization of exactly what was written down, which turned out not to be what was meant.

## Check yourself

Confirm on GPT-2 small that the loss really is nothing more than the formula above.

[`model(ids, labels=ids).loss`](/wiki/ai/llm/running-the-checks) must equal `F.cross_entropy(logits[:, :-1].flatten(0, 1), ids[:, 1:].flatten())` — HuggingFace shifts the labels internally, because for a next-token model the correct answer at each position is the input one step along. Compute both; they agree exactly.

Skip the shift and you get 12.9 instead of 3.3 — the most common bug in a from-scratch implementation, and note that 12.9 is *worse than guessing uniformly*, which is the tell. A model scoring above `ln(k)` isn't ignorant; it is confidently wrong, and this loss charges extra for that.

## Depends on / leads to

Depends on [the MLP](/wiki/ai/neural-network/multi-layer-perceptron) — something has to produce the answer being scored. Leads to [backprop](/wiki/ai/neural-network/backprop-one-weight), which turns this one number into a direction for every weight in the network.
