---
title: "Fine-Tuning"
weight: 320
---

Same architecture, same weights, more training — on your data, at a small learning rate. Nothing structural changes. Every virtue and every failure of fine-tuning follows from that.

What it's good at is **behaviour**: format, tone, refusal style, the input-output shape of a task. Those are cheap to move, because the model already has the [features](/wiki/ai/llm/superposition) and you're only adjusting how it uses them.

What it's bad at is **facts**. Teaching the model something it doesn't know means shifting weights far enough to store new information, and the same gradient steps quietly degrade everything else — catastrophic forgetting. The rule of thumb that follows: if you want the model to *know* your documents, put them in the context; if you want it to *behave* a certain way, fine-tune.

**LoRA** is the standard cheap form. Freeze `W`; learn a low-rank update `ΔW = BA`, where B and A are skinny (rank 8 is common). You train well under 1% of the parameters, and at inference you either fold `BA` into `W` or keep it as a swappable adapter. It works because the update a fine-tune actually needs is close to low-rank — you're steering the model, not rebuilding it.

## Check yourself

Fine-tune [GPT-2 small](/wiki/ai/llm/gpt-2) on Shakespeare with [nanoGPT](/wiki/ai/llm/running-the-checks) and track two numbers: *training* loss on Shakespeare (falls) and loss on a held-out slice of WikiText (rises). That divergence is catastrophic forgetting, measured. Keep the run short — nanoGPT's own recipe stops at 20 iterations, because a 1 MB corpus overfits almost immediately and Shakespeare's *validation* loss turns around and climbs too.

## Depends on / leads to

Depends on [the loss function](/wiki/ai/llm/the-loss-function) and [backprop through one weight](/wiki/ai/llm/backprop-one-weight). Leads to [RLHF](/wiki/ai/llm/rlhf).
