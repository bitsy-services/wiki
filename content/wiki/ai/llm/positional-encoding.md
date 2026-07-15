---
title: "Positional Encoding"
weight: 270
---

A query dotted with a key doesn't know where either row sits. Attention, by itself, is a bag of rows. Position has to be injected on purpose.

GPT-2 injects it once, at the left edge. It learns a vector per position — `wpe`, one row per slot — and *adds* it to the [embedding](/wiki/ai/llm/embeddings) before block 0 sees anything. Same width, added rather than concatenated, so position costs the row no capacity; it just perturbs it. Every block and every head downstream reads position out of a signal mixed into the row's content at the start.

That's cheap, it works, and it has two defects.

**The table is finite.** 1024 rows in GPT-2 small. There's no vector for position 1024, so there's no position 1024. The [blocks would happily process row 5000](/wiki/ai/llm/weight-sharing); the table is what stops them.

**It's absolute.** The vector for position 300 bears no built-in relation to the one for 301, so "three tokens back" is a different geometric fact at every position and the model learns it separately at each. [RoPE](/wiki/ai/llm/rope) is the fix.

One subtlety worth carrying forward: a decoder trained with *no* positional encoding isn't position-blind. The causal mask leaks order — row 0 sees one row, row 5 sees six — and models trained that way recover position from that alone. Don't try to show this by zeroing GPT-2's `wpe`, though: it was trained with one, and you'll just get a broken model.

## Check yourself

Position enters GPT-2 in exactly one place, by addition. Confirm it: `hidden_states[0][0, i]` equals `wte[token_i] + wpe[i]`, to `torch.allclose`. Then zero `wpe` and measure perplexity on WikiText — it explodes. One table, added once, and the whole model leans on it.

## Depends on / leads to

Depends on [embeddings](/wiki/ai/llm/embeddings) and [weight sharing](/wiki/ai/llm/weight-sharing). Leads to [RoPE](/wiki/ai/llm/rope).
