---
title: "Speculative Decoding"
weight: 340
---

Speculative decoding makes a large model produce text faster by having a small model guess ahead. The small one writes the next stretch of text — cheaply, and usually correctly, because most words in most sentences are not hard to predict. The large one then checks all of those guesses at once, for barely more than the cost of extending the text by a word itself. Whatever survives the check is kept, and the rest is thrown away. The remarkable part is that none of this is a quality trade: the text that comes out is drawn from exactly the distribution the large model would have produced unaided, and the only thing that changed is how long it took.

## The asymmetry it exploits

Generating is serial. Each token depends on the one before it, so there is no way to produce four tokens in less than four passes.

*Checking* four tokens is not serial at all. Hand a model a sequence and one forward pass yields a next-token distribution at every position simultaneously — which is not a special feature but simply [how training has always worked](/wiki/ai/llm/training-vs-inference-parallelism). If you already have a guess at what the next four tokens are, one pass tells you what the model itself would have said at each of those four points.

So: producing is expensive and serial, verifying is cheap and parallel. Everything else is bookkeeping.

## How a step runs

A small **draft** model generates `k` tokens (four, say), one at a time. It's serial, but the model is small, so slow is cheap.

The large **target** model then scores all `k` in a single forward pass. Now compare, position by position, what the target would have said against what the draft actually said. Accept the longest prefix that survives the test below, resample the first rejected token from a corrected distribution, and discard everything after it.

Note the floor that gives you: even if every single draft token is rejected, that verification pass still yields one good token, because the target's own opinion at the first position is sitting right there in the pass you already paid for. So the number of *target* passes never goes up. What a bad draft costs you is the draft's own work, wasted — which is why this is a speed trade and not a free lunch.

## Why the output is identical, not merely similar

This is the part that makes it an algorithm rather than a heuristic, and it's worth seeing, because "a small model helps a big one" sounds exactly like something that ought to cost quality.

Write `q` for the draft model's distribution over the vocabulary at some position, and `p` for the target's at that same position. The draft has drawn a specific token `x` from `q`. The test on it is:

- **Accept** `x` with probability `min(1, p(x)/q(x))`. If the target wanted that token at least as much as the draft did, keep it outright.
- **On rejection**, don't simply take the target's favourite. Draw instead from the *difference* between the two distributions: the one proportional to `max(0, p − q)`, renormalized.

Work a two-token vocabulary through and you can watch it balance. Say the target would pick A or B evenly — `p` = (0.5, 0.5) — while the draft is lopsided, `q` = (0.9, 0.1), and it proposes A.

A is accepted with probability `min(1, 0.5/0.9)` = 0.56. So A survives 0.9 × 0.56 = **0.45** of the time. On the other 0.44 of A-proposals the token is rejected, and the residual distribution is `max(0, p − q)` = (0, 0.4), which normalizes to B with certainty — contributing 0.9 × 0.44 = **0.4** to B. Add the times the draft proposed B outright (0.1, always accepted, since the target wanted B more than the draft did) and the totals are A: 0.45 + 0.05 = 0.5, B: 0.4 + 0.1 = 0.5.

Exactly `p`. The draft's bias toward A was rejected in precise proportion to how far it overreached, and the residual put back exactly the mass it had been neglecting. That balancing act — not the acceptance test alone — is what buys exactness. (Purists will note this is *modified* rejection sampling; the textbook version needs an envelope and retries, whereas the correction term is what makes this one work in a single shot.)

So there is no quality knob here and no tuning trade-off to get wrong. A bad draft model makes the whole thing *slower*; it cannot make the output worse.

## Why it wins

It wins for the reason [decode is bandwidth-bound](/wiki/ai/llm/training-vs-inference-parallelism): at batch size 1, generating one token and scoring four cost the target model nearly the same, because both are bounded by reading the weights out of memory rather than by arithmetic. The verification pass consumes compute that was sitting idle.

That's the honest framing of the payoff. Speculative decoding doesn't reduce the work; it relocates it into capacity that was being wasted. 2–3× is typical. The ceiling is how often the draft agrees with the target, minus what running the draft costs — which is why the draft has to be genuinely small *and* genuinely similar, and why the technique works best on exactly the predictable text it feels like it should be unnecessary for.

## Check yourself

[Call](/wiki/ai/llm/running-the-checks) `generate(..., assistant_model=gpt2)` with [GPT-2 XL](/wiki/ai/llm/gpt-2) as the target. Under greedy decoding the output is token-for-token identical to plain GPT-2 XL. Now log the acceptance rate α — don't mistake it for the speedup. It *sets* the speedup: with k = 4, α ≈ 0.7 buys about 2.8 target tokens per verification pass, α ≈ 0.9 buys 4.1. Pick a draft that disagrees and α collapses, taking the whole trick with it — but note that the *output* is still correct, exactly as the exactness argument promises. Only the clock suffers.

## Depends on / leads to

Depends on [sampling strategies](/wiki/ai/llm/sampling-strategies) and [training vs inference parallelism](/wiki/ai/llm/training-vs-inference-parallelism). Leads to [why scale worked](/wiki/ai/llm/why-scale-worked), the last page — and the argument the rest of these pages were evidence for.
