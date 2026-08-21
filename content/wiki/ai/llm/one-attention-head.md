---
title: "One Attention Head"
weight: 130
---

A head is one complete instance of the attention machinery — the smallest piece of a transformer that can move information from one word to another. [Attention](/wiki/ai/llm/attention) describes what that is for; this page is what it actually computes. A block runs several heads side by side and they never interact, so following a single one all the way through shows the entire operation. It takes a handful of steps, and not one of them is more than multiplication, addition, and a division.

Throughout, take the point of view of one row — one token position — asking its question. Every other row is doing the same thing at the same time, independently.

## Step 1: the row becomes a query, a key, and a value

The row arrives off [the residual stream](/wiki/ai/llm/residual-stream), gets [normalized](/wiki/ai/neural-network/normalization), and is then read three separate ways.

- The **query** is what this row is looking for.
- The **key** is what this row advertises to anything looking at it.
- The **value** is what this row hands over if it gets picked.

Each of the three is produced by multiplying the row by its own learned matrix. Nothing is stored between runs and nothing is retrieved from anywhere — all three are worked out from the row on the spot, every time. They are three views of the same numbers, which is a big enough idea to get [its own page](/wiki/ai/llm/qkv-projections).

Each view also *narrows*. A row is `d_model` wide — 768 numbers in [GPT-2 small](/wiki/ai/llm/gpt-2) — and a head's query, key, and value are 64. That width is the head's whole world, and it is why one head can only ever track one kind of relationship.

## Step 2: score the query against every key

Dot this row's query against the key of every row, and you get one number per row: how strongly this row wants that one. A large dot product means the query and the key point in similar directions in that cramped 64-dimensional space, which is what "relevant" means here and all it means.

Note what is being compared. This row's *query* against the other row's *key* — two different lenses, so the relationship is one-sided. Row 4 wanting row 1 says nothing about whether row 1 wants row 4.

## Step 3: divide by the square root of the head width

Nothing so far stops those scores from being enormous, and their size is a problem.

A query and a key are each 64 numbers, and their dot product is a sum of 64 products. If the entries were independent, centred on zero, and of typical size 1, that sum would have variance 64 and so land around 8 in magnitude — and the *gaps* between competing scores would be roughly that wide too. (The centring is what makes the total grow like √64 rather than like 64: the terms cancel as often as they reinforce.) Widen the head and the gaps widen with it, for no reason except the arithmetic.

Imagine ranking job candidates by summing their scores across independent criteria. Rate them on 4 criteria and the totals cluster; rate them on 64 and the totals spread much further apart — not because the candidates got more different, but because you added up more numbers. If your rule is then "whoever leads by 8 points takes the job outright," the number of criteria has quietly rewritten your decision rule. Dividing by the square root of the count restores the rule you meant.

That matters because of what happens next. [Softmax is exponential in the gaps](/wiki/ai/llm/softmax-and-temperature): a gap of 8 makes one row about three thousand times likelier than another. A head whose scores are spread that far apart has stopped blending and started picking a single row — and worse, softmax's gradient nearly vanishes once its output is that lopsided, so a head which lands there early in training has a hard time learning its way back out.

One division fixes it. Every score is divided by the square root of the head width — √64 = 8 in GPT-2 — which is exactly the factor that pulls the spread back to where it would be for a single product, keeping softmax soft and its gradient alive. This is the "scaled" in *scaled dot-product attention*, and it is the one part of the operation the [database analogy](/wiki/ai/llm/attention) gives you no reason to expect.

## Step 4: mask, then softmax

The scores now cover every row in the sequence, including the ones *after* this one. Those get erased — set to −∞ before the softmax, so they come out at exactly zero weight. That's [the causal mask](/wiki/ai/llm/causal-mask), and it exists so that a model being trained to predict the next word cannot simply read it.

Softmax then turns what survives into weights that are positive and sum to one, across the rows this row is allowed to see. That set of weights is the row's [attention pattern](/wiki/ai/llm/glossary): where its attention actually went.

## Step 5: blend the values, and add the result back

Take each visible row's value, scale it by that row's weight, and sum. The result is a 64-wide blend — mostly the values of whatever the pattern favoured, with a little of everything else mixed in.

That blend is still stuck in the head's narrow subspace, so a final learned matrix maps it back up to full row width. The result is *added* into the row's running total on the residual stream, alongside whatever the other heads in this block contributed. Nothing is overwritten.

```text
                              depth  →

  pos 0  "The"   row ──▶ k₀, v₀ ──┐
  pos 1  " cat"  row ──▶ k₁, v₁ ──┤
  pos 2  " sat"  row ──▶ k₂, v₂ ──┤   pos 4 may read rows 0–4,
  pos 3  " on"   row ──▶ k₃, v₃ ──┤   and nothing below itself
  pos 4  " the"  row ──▶ k₄, v₄ ──┤
                  │               │
                  └──▶ q₄ ────────┤
                                  ▼
                    q₄ · kⱼ  →  ÷ 8  →  mask  →  softmax  →  weights
                                                               │
                              Σⱼ weightⱼ · vⱼ  ◀────────────────┘
                                     │
                                     ▼
                          widen back to d_model,
                          add into pos 4's row
```

## What one head is worth

The head is strictly vertical. It moves information between rows and never within one — that is the MLP's job, and the two never overlap.

And a head is narrow on purpose. Sixty-four numbers is enough to chase one relationship: *the noun this adjective belongs to*, *the open bracket this close bracket matches*, *the token that followed the last time this one appeared*. It is nowhere near enough to chase all of them at once. That limitation is not a flaw to be engineered away; it's the reason a block runs [twelve heads side by side](/wiki/ai/llm/multi-head-attention), each free to specialize in something different.

## Check yourself

Load [GPT-2 small](/wiki/ai/llm/gpt-2) with `attn_implementation="eager"` — the default SDPA path returns an *empty* attentions tuple and no warning — and run it with [`output_attentions=True`](/wiki/ai/llm/running-the-checks). `attentions[0][0, 0]` is a square matrix: every row of it sums to 1.0, and every weight a row assigns to a row *below* itself is exactly 0.0. Now change a word near the top and re-run. Rows below it move; rows above it are bit-identical. The pattern is a function of the input — but only of the input a row can see.

Then rebuild one pattern yourself and confirm the divisor in step 3 is load-bearing. Two traps sink most attempts, and both are simply steps 1 and 2 taken literally: the projections read a *normalized* row, not the raw one, and `c_attn` is a module to be called rather than a matrix to be sliced — calling it is also what applies the bias you'd otherwise drop.

```python
h0 = model.transformer.h[0]
qkv = h0.attn.c_attn(h0.ln_1(outputs.hidden_states[0]))   # [1, n, 2304]
q, k, _ = qkv.split(768, dim=-1)
q0, k0 = q[..., :64], k[..., :64]                          # head 0's slice
scores = q0 @ k0.transpose(-1, -2)
```

Mask and softmax `scores` as-is and it doesn't match `attentions[0][0, 0]` — it's visibly too sharp, with most rows dumping nearly all their weight on one position. Divide by 8 first and it matches to `torch.allclose`. The factor isn't cosmetic tidying; leaving it out gives you a different model.

## Depends on / leads to

Depends on [attention](/wiki/ai/llm/attention). Leads to [Q/K/V as three projections](/wiki/ai/llm/qkv-projections) and [the causal mask](/wiki/ai/llm/causal-mask).
