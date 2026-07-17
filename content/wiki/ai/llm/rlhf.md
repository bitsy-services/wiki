---
title: "RLHF"
weight: 330
---

[Cross-entropy](/wiki/ai/llm/the-loss-function) trains a model to predict what a human *would* write. It has no way to say that one plausible continuation is better than another. RLHF is the machinery for training on that preference instead.

Three steps, classically. Supervised fine-tune on demonstrations. Then collect **comparisons** — a human sees two completions and picks one — and train a **reward model**: a copy of the language model with the unembedding swapped for a scalar head, trained so preferred completions score higher. Then optimize the policy against that reward with PPO, plus a **KL penalty** pinning it to the model it started from.

The KL term is the load-bearing part. The reward model is a proxy, and any proxy can be gamed: without a leash, the policy finds text that scores enormously and reads like nothing a human ever wrote. Reward hacking is the default outcome, not an edge case.

**DPO** removes the reward model entirely — algebra on the same preference pairs yields a loss you apply to the policy directly. Cheaper, more stable, now the common choice for open models.

What none of this does is teach new capabilities. It reweights among behaviours the pretrained model could already produce, which is why an aligned model tends to get *worse* at raw next-token prediction. You paid for helpfulness in modelling accuracy.

## Check yourself

Measure perplexity on plain WikiText for a base/instruct pair. Qwen2.5-0.5B is ungated and runs in minutes: base 17.9, Instruct 20.0. The aligned sibling is reliably worse at raw prose. Careful what you conclude, though: that gap bundles the fine-tune, the preference optimization, and a changed data mix. It's the post-training tax, not RLHF's share alone.

## Depends on / leads to

Depends on [fine-tuning](/wiki/ai/llm/fine-tuning). Leads to [speculative decoding](/wiki/ai/llm/speculative-decoding).
