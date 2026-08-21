---
title: "Fine-Tuning"
weight: 320
---

Fine-tuning is what you do to a finished model to make it behave differently. There is no new architecture and no fresh start: you take the trained weights and simply carry on training them, on a much smaller and far more particular body of text, nudging gently rather than shoving. That modesty is the whole character of the technique. Nearly everything fine-tuning is good at, and everything it is bad at, follows from the fact that it can only move a model a short distance from wherever it already was.

## What "carry on training, gently" actually means

Same architecture, same weights, more training — on your data, at a small learning rate. Nothing structural changes: nothing is bolted on, no vocabulary is extended, no part of the model is replaced. [The loss](/wiki/ai/neural-network/the-loss-function) is the same cross-entropy it always was, and [backprop](/wiki/ai/neural-network/backprop-one-weight) does the same thing it always did.

The small learning rate is the operative choice. It is what keeps the model near where it started, and it is simultaneously the reason fine-tuning is cheap, the reason it's reliable, and the reason it cannot do the thing people most often want from it.

## What it's good at: behaviour

Format, tone, refusal style, the input-output shape of a task, the house style of your documentation, reliably emitting JSON.

These are all cheap to move, because the model already possesses the [features](/wiki/ai/neural-network/superposition) involved and you are only adjusting how it deploys them. Nothing new has to be stored. You're changing which of the model's existing habits get reached for, and a small nudge is enough to change a habit.

## What it's bad at: facts

Teaching the model something it genuinely doesn't know means shifting weights far enough to store new information — and the same gradient steps that store it quietly degrade everything else the model had learned. That's **catastrophic forgetting**, and it is not a tuning problem you can configure your way out of. It's the direct consequence of writing new information into weights that were already holding other information.

It's the difference between training a new hire in your house style and teaching them a subject they never studied. A week of the first works well. A week of the second produces somebody who has half-learned the subject and forgotten some of what they came in knowing.

The rule of thumb follows immediately, and it's the most useful sentence on this page: **if you want the model to *know* your documents, put them in the context; if you want it to *behave* a certain way, fine-tune.**

## LoRA: fine-tuning without touching the model

The standard cheap form is **LoRA**, low-rank adaptation. Freeze the original weight matrix `W` entirely and learn a separate update `ΔW = BA`, where `B` is tall and narrow and `A` is short and wide. Both pass through a shared inner dimension `r` — the **rank** — and that narrow waist is where the saving comes from.

Take one of GPT-2's 768×768 matrices. Updating it directly means learning 589,824 numbers. At `r = 8`, `B` is 768×8 and `A` is 8×768, so the whole update is described by 768×8 + 8×768 = 12,288 of them — about 2% of the entries, while still expressing a change that covers the full 768×768 shape.

Apply that to only some of the matrices, which is normal (commonly just the query and value projections), and measure against the whole model including its embedding tables, and you end up training a fraction of one percent of the weights. At inference you either fold `BA` back into `W`, costing nothing at run time, or keep it separate as a swappable **adapter**.

It works because the update a fine-tune actually needs really is close to low-rank. You are steering the model, not rebuilding it, and steering doesn't require many independent knobs.

And that swappability is the practical payoff. One base model held in memory, many small adapters layered on top and exchanged per request — dozens of specialized behaviours for barely more than the cost of hosting one model. It only works at all because fine-tuning moves the model such a short distance in the first place.

## Check yourself

Fine-tune [GPT-2 small](/wiki/ai/llm/gpt-2) on Shakespeare with [nanoGPT](/wiki/ai/llm/running-the-checks) and track two numbers: *training* loss on Shakespeare (falls) and loss on a held-out slice of WikiText (rises). That divergence is catastrophic forgetting, measured. Keep the run short — nanoGPT's own recipe stops at 20 iterations, because a 1 MB corpus overfits almost immediately and Shakespeare's *validation* loss turns around and climbs too.

## Depends on / leads to

Depends on [the loss function](/wiki/ai/neural-network/the-loss-function) and [backprop through one weight](/wiki/ai/neural-network/backprop-one-weight). Leads to [RLHF](/wiki/ai/llm/rlhf).
