---
title: "One Attention Head"
weight: 130
---

A head is the only machinery in the model that lets one row see another. Everything else — the MLP, the norms — works on a row in isolation.

Here's the whole operation, for one head, from a single row's point of view. The row emits a **query**: what am I looking for? Every row at or above it exposes a **key**: what I've got. Dot the query against each key and you get a score per row — how much this row wants that one. Softmax those scores into an [attention pattern](/wiki/ai/llm/glossary): weights that sum to 1 across the rows it's allowed to see. Then take those rows' **value** vectors, weight them by the pattern, sum, and map the result back to `d_model`. That's what the head adds to the row's [residual stream](/wiki/ai/llm/residual-stream).

Two things worth underlining. The pattern is computed from the *contents* of the rows, not fixed in the weights — change a word above and the weights move. That's what makes it attention rather than a hard-wired mixing matrix. And the head is strictly vertical: it moves information between rows, never within one.

## Check yourself

Load GPT-2 small with `attn_implementation="eager"` — the default SDPA path returns an *empty* attentions tuple and no warning — and run it with `output_attentions=True`. `attentions[0][0, 0]` is a square matrix: every row of it sums to 1.0, and every weight a row assigns to a row *below* itself is exactly 0.0. Now change a word near the top and re-run. Rows below it move; rows above it are bit-identical. The pattern is a function of the input — but only of the input a row can see.

## Depends on / leads to

Depends on [the residual stream](/wiki/ai/llm/residual-stream). Leads to [Q/K/V as three projections](/wiki/ai/llm/qkv-projections) and [the causal mask](/wiki/ai/llm/causal-mask).
