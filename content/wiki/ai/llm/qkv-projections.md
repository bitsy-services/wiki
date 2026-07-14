---
title: "Q/K/V as Three Projections"
weight: 140
---

The query, key, and value aren't three things a row *has*. They're three learned linear maps of the *same* row: `q = norm(row)·W_Q + b_Q`, and likewise for k and v. One row, normalized, read three ways. Nothing else enters.

Each has a job:

- **Q** — what this row is looking for.
- **K** — what this row advertises to anyone looking.
- **V** — what this row hands over when it gets picked.

Each map takes the 768-wide row down to 64 per [head](/wiki/ai/llm/glossary) — a private subspace, narrow enough to see only a slice of the stream.

The split matters more than the names. **Q·K decides where attention goes; V decides what moves.** The matrices are learned independently, so a head can attend to a row for one reason and copy something unrelated out of it. Induction heads do exactly that: match on "this token appeared before" (a Q/K job), then copy "whatever followed it last time" (a V job).

Scoring is not symmetric, either. Row *i*'s score for row *j* runs through the bilinear form `W_Q W_Kᵀ`, which has no reason to be symmetric — swap the two rows and you get a different number.

## Check yourself

GPT-2 fuses the three maps: `h[0].attn.c_attn.weight` is `[768, 2304]`, with a matching bias. Slice both into thirds and reproduce `q`, `k`, `v` yourself — but feed them `ln_1(row)`, not the row, and don't drop the bias; do either and you're off by an order of magnitude. Then recompute the scores with `W_Q` and `W_K` swapped: the score matrix comes out *exactly* transposed. The causal mask and the row-wise softmax, not the projections, are what turn it into a different pattern.

## Depends on / leads to

Depends on [one attention head](/wiki/ai/llm/one-attention-head). Leads to [multi-head attention](/wiki/ai/llm/multi-head-attention).
