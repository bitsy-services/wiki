---
title: "Softmax and Temperature"
weight: 210
---

Logits are scores: unbounded, signed, meaningless alone. Softmax turns them into probabilities — exponentiate, normalize — with a temperature knob in the middle:

```text
p_i = exp(z_i / T) / Σ_j exp(z_j / T)
```

Two properties are worth knowing cold.

**Only differences matter.** Add a constant to every logit and nothing changes; the constant cancels top and bottom. A logit's absolute value tells you nothing. The *gap* to the next logit tells you everything.

**Temperature scales the gaps.** `T = 1` uses the logits as trained. `T < 1` stretches every gap, so the leader pulls away — as `T → 0`, softmax becomes argmax. `T > 1` compresses the gaps toward uniform. Because it's exponential, the tail moves violently: a token 3 logits behind the leader is about 73× less likely at `T = 0.7`, but only about 8.5× less likely at `T = 1.4`. Same model, same logits, very different willingness to say something strange.

What temperature does **not** do is change the ranking. It's a monotone transform, so the argmax at `T = 0.2` and at `T = 5` is the same token. It changes how often you take the leader, never who the leader is. Anything that changes *which* token wins — a repetition penalty, a logit bias — is doing something else entirely.

## Check yourself

[Take](/wiki/ai/llm/running-the-checks) one position's logits from [GPT-2 small](/wiki/ai/llm/gpt-2) and softmax at `T` = 0.5, 1.0, 2.0. `argmax` is identical in all three. Entropy rises monotonically with `T`, and the top token's probability falls. Then add 100 to every logit and confirm the probabilities don't budge.

## Depends on / leads to

Depends on [the unembedding and logits](/wiki/ai/llm/unembedding-and-logits). Leads to [sampling strategies](/wiki/ai/llm/sampling-strategies).
