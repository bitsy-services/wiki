---
title: "Sampling Strategies"
weight: 220
---

Softmax hands you a distribution over 50,257 tokens. Sampling turns it into one token — the only real choice you get at inference, and the one most likely to be blamed on the model.

**Greedy** takes the argmax. Deterministic, and it degenerates: fluent text that falls into loops, because the most likely continuation of a phrase you've just said is often to say it again.

**Pure sampling** draws from the whole distribution. It never loops, and it wanders, because the tail is enormous. After "the cat sat on the," the ~49,500 tokens below p = 0.0001 carry more probability between them (0.10) than the single best token does (0.08). Sample long enough and you *will* pick from the garbage.

**Top-k** keeps the k highest and renormalizes. Crude: `k = 50` lets in 49 tokens the model hated when it was confident, and cuts off good options when it genuinely wasn't.

**Top-p (nucleus)** keeps the smallest set whose probabilities sum to at least `p`. It adapts to the shape of the distribution — after "the capital of France is" the nucleus is one token; mid-clause it can be thousands. That adaptivity is why it's the default.

Truncation and [temperature](/wiki/ai/llm/softmax-and-temperature) compose, and both are attacking the same tail from opposite ends: temperature reweights it, truncation deletes it.

## Check yourself

Greedy-decode 100 tokens from GPT-2 small on any prompt — it falls into a repeating phrase. Same prompt with `top_p=0.9` — no loop. Then log the nucleus size at each step: at p = 0.9 it runs from 1 to about 9,400, median ~120. No fixed `k` covers that range.

## Depends on / leads to

Depends on [softmax and temperature](/wiki/ai/llm/softmax-and-temperature). Leads to [speculative decoding](/wiki/ai/llm/speculative-decoding).
