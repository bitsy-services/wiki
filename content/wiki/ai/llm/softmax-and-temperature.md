---
title: "Softmax and Temperature"
weight: 210
---

Softmax is the step that turns the model's raw scores into probabilities — numbers that are all positive and add up to one, so that something can actually be drawn from them. Temperature is a single knob wired into the middle of that conversion, and it is why the same model can be made reliably dull or unreliably interesting without retraining anything. The two belong on one page because temperature is not a separate mechanism: it is a division applied to the scores on their way in, and everything it does follows from what softmax does with the gaps between them.

## Why the scores can't be used as they are

[The logits](/wiki/ai/llm/unembedding-and-logits) arrive as dot products, which means they are unbounded, signed, and add up to nothing in particular. There is no way to sample from a list like that. It needs to be made positive and made to sum to one.

The obvious repair — shift everything up until nothing is negative, then divide by the total — technically works and is a bad idea. It makes the result depend on how far you happened to shift, and worse, it makes a gap mean wildly different things at different points on the scale. Scores of 2 and 1 would come out as 0.67 and 0.33, a two-to-one preference. Scores of 102 and 101 — the same gap of 1 — come out almost tied. Nothing about the model justifies that; the gap is the same gap.

Exponentiating first fixes both problems. It guarantees positivity for any input whatever, and — the part that matters — it converts *additive* differences in score into *multiplicative* ratios in probability. A fixed gap now always means the same likelihood ratio, wherever on the scale it sits. That is exactly the correspondence [the loss function](/wiki/ai/neural-network/the-loss-function) assumes when it grades the model in log space, so softmax isn't an arbitrary squashing choice; it's the inverse of how the model is scored.

Writing `z` for the logits and `T` for the temperature knob promised above, the operation is:

```text
p_i = exp(z_i / T) / Σ_j exp(z_j / T)
```

Ignore `T` for a moment (it's 1 by default, and the next section is entirely about it) and that reads: exponentiate every score, then divide each by the total so they sum to one.

## Only the differences matter

Add a constant to every logit and nothing changes at all — the constant factors out of the numerator and the denominator alike and cancels.

**A logit's absolute value tells you nothing.** A score of 14 is not "confident." Only the *gap* to the next logit carries information, which is why implementations routinely subtract the maximum logit before exponentiating (it prevents overflow and changes no output), and why comparing raw logit values between two different models is meaningless.

This sits alongside, not against, [the previous page's point](/wiki/ai/llm/unembedding-and-logits) that scaling the final row's magnitude makes the model look more confident. *Shifting* every logit by a constant changes nothing; *multiplying* them all by a constant stretches every gap and changes a great deal. Softmax is blind to the first and highly sensitive to the second.

## Temperature scales the gaps

Dividing every logit by `T` before exponentiating stretches or compresses those gaps, and softmax's exponential turns modest changes in gap into violent changes in probability.

`T = 1` uses the logits exactly as trained. `T < 1` stretches every gap, so the leader pulls away — as `T → 0`, softmax collapses to **argmax**, meaning it simply hands back the single highest-scoring token with probability 1. `T > 1` compresses the gaps toward uniform.

The tail is where you see it. A token 3 logits behind the leader is about **73×** less likely at `T = 0.7`, and only about **8.5×** less likely at `T = 1.4`. Same model, same logits, an entirely different willingness to say something strange.

Think of it as the contrast slider on a photograph. Turn contrast up and the brightest region swallows the frame; turn it down and everything washes toward flat grey. What the slider never does is change *which* pixel was brightest.

## What temperature does not do

It does not change the ranking. Dividing by a positive constant is a monotone transform, so the argmax at `T = 0.2` and at `T = 5` is the same token. Temperature changes how often you take the leader; it never changes who the leader is.

That doubles as a diagnostic: if something changes *which* token wins, it is not temperature. A repetition penalty, a logit bias, a grammar constraint, a banned-token list — all of those edit the logits themselves, and all of them are doing something categorically different.

`T = 0` is worth one note, because the formula divides by it. Nothing actually computes `exp(z/0)`; implementations special-case it to plain argmax, which is the limit the formula approaches anyway.

Temperature is one division, applied at the last moment and changeable per request, that moves the model between "reliable and boring" and "surprising and occasionally wrong" without touching a single weight. The other control is [deleting the tail outright](/wiki/ai/llm/sampling-strategies), which is the next page.

## Check yourself

[Take](/wiki/ai/llm/running-the-checks) one position's logits from [GPT-2 small](/wiki/ai/llm/gpt-2) and softmax at `T` = 0.5, 1.0, 2.0. The argmax is identical in all three. Entropy — the standard measure of how spread out a distribution is, largest when everything is equally likely — rises monotonically with `T`, and the top token's probability falls. Then add 100 to every logit and confirm the probabilities don't budge.

## Depends on / leads to

Depends on [the unembedding and logits](/wiki/ai/llm/unembedding-and-logits). Leads to [sampling strategies](/wiki/ai/llm/sampling-strategies).
