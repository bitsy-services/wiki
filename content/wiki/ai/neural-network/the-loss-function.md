---
title: "The Loss Function"
weight: 230
---

The loss function is the single number that trains the entire model. Once the model has produced its probabilities, the loss asks one question: how much probability did you put on the word that actually came next? A confident right answer scores well, a confident wrong answer scores terribly, and everything the model ever learns is a consequence of being pushed, over and over, to make that number smaller. Nothing else is supplied — no grammar, no facts, no opinion about which of two continuations reads better.

## Where the supervision comes from

It's natural to assume a training signal must be something a person produced: a label, a rating, an example answer. That is how most of machine learning had worked, and it's the assumption to discard first.

Here the correct answer is *the next token*, which was already sitting in the text. The model is shown a passage, asked to predict each position from the ones before it, and graded against what the author actually wrote. Nobody annotated anything. Every sentence ever written is already labelled, by itself, for free — which is why the training set could be most of the readable internet, and [why the whole field is shaped the way it is](/wiki/ai/llm/why-scale-worked).

## Cross-entropy: the negative log of the right answer

```text
loss = −(1/n) Σ log p(actual next token | rows above)
```

Take the probability the model assigned to the token that turned up, take its logarithm, negate it, and average over every position. That's **cross-entropy**, and it is the *only* signal in pre-training.

Each piece is doing something specific. The **log** is there because probabilities multiply across a sequence and logs turn that into addition — so the loss over a passage is a sum rather than a product that would underflow to zero within a paragraph. The **negation** makes lower mean better, since log of a probability is always negative. The **average** makes sequences of different lengths comparable.

The units are *nats*, natural-log units, which is the only reason `ln` shows up rather than `log₂`. Nothing conceptual turns on it, but it's why the numbers below look the way they do.

## Get the scale straight

A model guessing uniformly across the 50,257-token [vocabulary](/wiki/ai/llm/glossary) scores `ln(50257) = 10.82`. That's the do-nothing baseline.

[GPT-2 small](/wiki/ai/llm/gpt-2) measures 3.28 on WikiText-2. Exponentiate the loss and you get [**perplexity**](/wiki/ai/llm/perplexity) — roughly, how many tokens the model is choosing between. Uniform is 50,257; GPT-2 small is 26.

The interesting thing about that scale is how compressed the useful part of it is. Getting from "knows nothing" to GPT-2 covers most of the distance from 10.8 down to 3.3, and every advance since has been fought over the remainder. Small absolute movements in loss are large movements in capability, which is worth remembering before dismissing a tenth of a nat. (Comparing two models this way only means anything if they share a tokenizer and a corpus — [perplexity](/wiki/ai/llm/perplexity) is emphatic about why.)

## It rewards calibration, not just correctness

Cross-entropy does not ask whether the top-ranked token was right. It asks what probability you assigned, and the difference matters enormously.

Putting 0.99 on the right token beats putting 0.6 on it. But putting 0.99 on the *wrong* one costs at least 4.6, where an honest 0.6 on the right one costs 0.5 — confident-and-wrong is punished about nine times harder than hedging, and worse still if the leftover probability was spread thin rather than concentrated on the runner-up.

This is exactly how a weather forecaster is scored properly: not on whether it rained, but on the probability they gave to what happened. Announcing "0% chance of rain" and then getting rained on is ruinous; saying 60% and getting rain is unremarkable. Under that kind of scoring the winning strategy is to report what you actually believe, and to say so less firmly when you know less.

So a model that knows what it doesn't know scores better. Base models come out of pre-training well-calibrated for precisely this reason: cross-entropy paid them to be. [RLHF](/wiki/ai/llm/rlhf) is where that gets trained back out of them, because human raters prefer answers that sound sure — an effect visible in the before-and-after calibration curves OpenAI published with GPT-4, where a nearly perfectly calibrated base model emerges from preference training markedly overconfident.

## One pass, a thousand predictions

Nearly every row contributes. A 1024-token sequence yields 1023 supervised predictions from a single forward pass — every row but the last, which has no next token to check against.

That's [the causal mask](/wiki/ai/llm/causal-mask) paying for itself: because no row can see ahead, every row can be scored honestly at the same time, and one pass over a document produces a thousand gradient signals instead of one. Compounded over a training run, it is [the reason any of this was affordable](/wiki/ai/llm/why-scale-worked).

## Check yourself

[`model(ids, labels=ids).loss`](/wiki/ai/llm/running-the-checks) must equal `F.cross_entropy(logits[:, :-1].flatten(0, 1), ids[:, 1:].flatten())` — HuggingFace shifts the labels internally. Compute both; they agree exactly. Skip the shift and you get 12.9 instead of 3.3 — the most common bug in a from-scratch implementation, and note that 12.9 is *worse than guessing uniformly*, which is the tell.

## Depends on / leads to

Depends on [softmax and temperature](/wiki/ai/llm/softmax-and-temperature). Leads to [perplexity](/wiki/ai/llm/perplexity).
