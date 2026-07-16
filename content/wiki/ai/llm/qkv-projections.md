---
title: "Q/K/V as Three Projections"
weight: 140
---

[Attention](/wiki/ai/llm/attention) talks about a row's query, its key, and its value as though the row were carrying three things around with it. It isn't. There is only the row. Query, key, and value are three different ways of *reading* it — three learned lenses, each trained to pull a different aspect out of the same numbers. Nothing is stored. All three are worked out from the row on the spot, every time attention runs.

## Three views of one row

Each of the three is an **affine map**: multiply the row by a learned matrix, then add a learned offset. Nothing else — no nonlinearity, no lookup, nothing conditional. (ML calls these "linear layers" out of habit. The added offset strictly makes them affine rather than linear, and that pedantry earns its keep exactly once, further down.)

```text
q = norm(row) · W_Q + b_Q
k = norm(row) · W_K + b_K
v = norm(row) · W_V + b_V
```

Read the left column downward and the point is obvious: the same input, three times. `W_Q`, `W_K` and `W_V` are the learned matrices — the lenses themselves — and each `b` is a learned bias. Nothing else enters.

One detail that trips people reproducing this by hand: the input isn't the raw row off the [residual stream](/wiki/ai/llm/residual-stream). It's a [normalized](/wiki/ai/llm/normalization) copy.

## What each one is for

- **Q — the query.** What this row is looking for.
- **K — the key.** What this row advertises to anyone looking.
- **V — the value.** What this row hands over when it gets picked.

Each map also *narrows*. It takes the full [`d_model`](/wiki/ai/llm/glossary)-wide row — 768 numbers in [GPT-2 small](/wiki/ai/llm/gpt-2) — down to 64 for a single [head](/wiki/ai/llm/glossary). A head therefore works in a private, cramped subspace, with room to see only a thin slice of what the stream is carrying. That's not a limitation to apologize for; it's what makes [running twelve heads at once](/wiki/ai/llm/multi-head-attention) worth doing, since each gets its own slice.

## The split matters more than the names

Here's the part to take away. **Q·K decides where attention goes. V decides what moves.** Two separate questions, answered by two separately learned sets of weights.

That separation is the whole payoff. Because `W_V` is learned independently of `W_Q` and `W_K`, a head can attend to a row for one reason and haul something completely unrelated out of it. *Why I looked at you* and *what I took from you* are decoupled — which sounds like a technicality and is actually where a lot of the model's cleverness lives.

**Induction heads** are the standard demonstration, and they're worth following carefully, because the naive version of the story describes something the architecture can't do. A head reads its value from the row it attends to. It cannot attend to one row and take the value from the row below it — so "find the earlier A and copy what came *after* it" is not a thing a single head can express.

The real circuit takes two heads and a division of labour. An earlier **previous-token head** does something almost trivial: every row attends to the one immediately above it and writes that neighbour's identity into itself. Now the row holding B carries a note saying *my predecessor was A*.

The induction head then exploits exactly the split this page is about. The current token A forms the query. The key at each row is built from the note — *who came before me* — so the match fires on the row whose predecessor was A, which is the row holding **B**. It attends there and copies that row's value, which is B. No rule was broken: it attended to B's row and read B's row.

Look at what that row's two lenses are saying at the same instant. Its **key** advertises "A came before me." Its **value** offers "I am B." One row, two learned readings, two entirely unrelated facts — which is the whole thesis of this page, and it's what lets the model continue a pattern it has never seen before but watched happen four tokens ago. If one set of weights had to serve both roles, the circuit couldn't exist.

## Scoring is not symmetric

Row *i*'s score for row *j* is not row *j*'s score for row *i*.

The comparison runs through both lenses at once — the query lens on one side, the key lens on the other — and nothing constrains those two matrices to be arranged so the result comes out even.

Set the biases aside for a moment, and this is where that pedantry pays: the score is then a **bilinear form** with matrix `W_Q W_Kᵀ` — an expression linear in each of its two inputs taken separately, `x_i (W_Q W_Kᵀ) x_jᵀ`. Nothing requires that matrix to be symmetric, and training had no reason to make it so. Put the biases back and it isn't bilinear at all any more, merely affine in each argument. The asymmetry is untouched either way.

Worth pausing on, because the word "attention" invites a picture of a mutual relationship. It isn't mutual. An adjective can attend hard to its noun while the noun scarcely registers the adjective.

## Check yourself

GPT-2 doesn't keep the three matrices apart — it fuses them. `h[0].attn.c_attn.weight` is the first block's combined Q/K/V matrix, shaped `[768, 2304]`: one 768-wide input mapped to three 768-wide outputs stacked side by side, with a matching bias. Slice both into thirds and reproduce `q`, `k`, and `v` yourself.

Each 768-wide third is *all twelve heads* laid end to end — 12 × 64 = 768 — so what you get back is every head's query at once, not the single 64-wide one described above. Cutting them apart per head is [multi-head attention](/wiki/ai/llm/multi-head-attention)'s business.

Two traps, each worth an order of magnitude if you hit it. Feed the maps `ln_1(row)` — the block's first LayerNorm, applied to the row — rather than the raw row. And don't drop the bias.

Then test the asymmetry, which is the falsifiable claim here: compute the raw score matrix and compare it against its own transpose. They differ. Row *i*'s score for *j* really isn't *j*'s score for *i*, and that's a fact about the trained weights — `W_Q W_Kᵀ` came out asymmetric because nothing pushed it to be anything else.

Swapping the lenses is worth one pass as a check on your slicing, with a caveat that will cost you an hour otherwise. Swap the query and key projections **entirely — matrix and bias together** — and the score matrix comes out exactly transposed. Swap only the matrices and leave each bias where it sits, and it doesn't: the cross terms survive and you get neither the original nor its transpose. Note also that the corrected version is an *identity*. The dot product commutes, so it would hold for any two projections whatever, and tells you nothing about GPT-2 in particular — it tests your code, not the model.

What the transpose relationship does show is where the real one-sidedness comes from. At the level of raw scores, swapping the lenses only mirrors the matrix. Everything that makes an actual attention pattern lopsided — [the causal mask](/wiki/ai/llm/causal-mask), the row-wise [softmax](/wiki/ai/llm/softmax-and-temperature) — happens afterward, and neither survives a transpose.

## Depends on / leads to

Depends on [one attention head](/wiki/ai/llm/one-attention-head). Leads to [multi-head attention](/wiki/ai/llm/multi-head-attention).
