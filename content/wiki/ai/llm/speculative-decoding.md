---
title: "Speculative Decoding"
weight: 340
---

Decoding is serial: each token depends on the last. *Verifying* isn't. That asymmetry is the whole trick.

A small **draft** model generates k tokens (four, say) one at a time — but it's small, so slow is cheap. The big **target** model then scores all k in a *single* forward pass, which it can do because [that's how training already works](/wiki/ai/llm/training-vs-inference-parallelism): one pass over a sequence yields a next-token distribution at every row at once. Compare the target's distribution at each row against the draft's, accept the longest prefix that survives a rejection-sampling test, resample the first rejected token from a corrected distribution, discard the rest.

The property that makes it more than a heuristic: the accepted tokens are distributed **exactly** as if the target model had produced them alone. Not an approximation, not a quality trade: same distribution, fewer serial steps.

Why it wins is the [bandwidth argument](/wiki/ai/llm/training-vs-inference-parallelism): at batch size 1, generating one token and scoring four cost nearly the same, because both are bounded by reading the weights, not by arithmetic. You spend idle compute to buy back serial steps. 2–3× is typical; the ceiling is how often the draft agrees, minus what the draft costs to run.

## Check yourself

[Call](/wiki/ai/llm/running-the-checks) `generate(..., assistant_model=gpt2)` with [GPT-2 XL](/wiki/ai/llm/gpt-2) as the target. Under greedy decoding the output is token-for-token identical to plain GPT-2 XL. Now log the acceptance rate α — don't mistake it for the speedup. It *sets* the speedup: with k = 4, α ≈ 0.7 buys about 2.8 target tokens per verification pass, α ≈ 0.9 buys 4.1. Pick a draft that disagrees and α collapses, taking the whole trick with it.

## Depends on / leads to

Depends on [sampling strategies](/wiki/ai/llm/sampling-strategies) and [training vs inference parallelism](/wiki/ai/llm/training-vs-inference-parallelism). Leads to [why scale worked](/wiki/ai/llm/why-scale-worked), the last page — and the argument the rest of these pages were evidence for.
