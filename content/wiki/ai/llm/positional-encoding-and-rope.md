---
title: "Positional Encoding and RoPE"
weight: 270
---

A query dotted with a key doesn't know where either row sits. Attention, by itself, is a bag of rows. Position has to be injected on purpose.

GPT-2 injects it once, at the left edge: a learned vector per position, added to the [embedding](/wiki/ai/llm/embeddings). Two defects. The table is finite — 1024 rows, the model's hard context limit. And it's *absolute*: the vector for position 300 bears no built-in relation to the one for 301, so "three tokens back" has to be relearned at every position.

**RoPE** injects position inside attention instead. It rotates q and k by an angle proportional to the row's position, in 2D coordinate pairs. Rotating two vectors by the same angle leaves their dot product alone, so what survives is the *difference* of the rotations. Content still does the work; the positional part of the score depends only on how far apart the rows are. Position becomes relative for free: no table, no hard cap (quality degrades past the trained range, but nothing forbids row 5000). Everything since Llama uses it.

A subtlety: a decoder trained with *no* positional encoding isn't position-blind. The causal mask leaks order — row 0 sees one row, row 5 sees six — and models trained that way recover position from it alone. Don't try to show this by zeroing GPT-2's `wpe`, though: it was trained with one, and you'll just get a broken model.

## Check yourself

Position enters GPT-2 in exactly one place, by addition. Confirm it: `hidden_states[0][0, i]` equals `wte[token_i] + wpe[i]`, to `torch.allclose`. Then zero `wpe` and measure perplexity on WikiText — it explodes. One table, added once, and the whole model leans on it.

## Depends on / leads to

Depends on [embeddings](/wiki/ai/llm/embeddings) and [weight sharing](/wiki/ai/llm/weight-sharing). Leads to [context length and the O(n²) cost](/wiki/ai/llm/context-length).
