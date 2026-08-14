---
title: "LayerNorm and RMSNorm"
weight: 180
---

Before [attention](/wiki/ai/llm/attention) or the MLP reads the row, the row is normalized: subtract the mean of its 768 numbers, divide by their standard deviation, then scale and shift by learned per-feature parameters. That's LayerNorm. It works *within a row*, along the feature axis — never across rows, so it can't leak anything between token positions. (The name is historical; it normalizes a row, not a [block](/wiki/ai/llm/glossary).)

[GPT-2](/wiki/ai/llm/gpt-2) is **pre-norm**: `row = row + attention(norm(row))`. Read that placement carefully. The norm applies to the copy attention reads. It does not apply to the stream. The [residual stream](/wiki/ai/llm/residual-stream) is never normalized in place — it keeps whatever magnitude it has accumulated, and it grows rightward, hard. In GPT-2 small the last row's norm runs from about 5 at the embedding to about 400 leaving block 11: a factor of a hundred. Exactly once, at the right edge, a final norm rescales it before the unembedding reads it.

Why bother: attention and the MLP see a well-conditioned input no matter how big the running sum has grown. That's what lets you chain blocks without activations exploding or gradients dying.

**RMSNorm** drops the mean subtraction and the bias — divide by the root-mean-square, scale, done. One fewer reduction, no measurable quality cost, which is why Llama and nearly everything since uses it. The centering was never earning its keep.

## Check yourself

[Print](/wiki/ai/llm/running-the-checks) the L2 norm of the *last* row of `hidden_states[i]` for i = 0…11. Mind the off-by-one: those are the embedding and blocks 0–10, not blocks 1–12. The norm climbs the whole way, ~5 → ~220. Do *not* include `hidden_states[12]` — HuggingFace has already run the final norm on it, and the number goes back down.

## Depends on / leads to

Depends on [the residual stream](/wiki/ai/llm/residual-stream). Leads to [skip connections](/wiki/ai/llm/skip-connections).
