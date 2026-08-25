---
title: "Context Length and the O(n²) Cost"
weight: 290
---

Context length is how much text a model can take into account at once, and it is the number that most directly limits what you can build with one. The reason it's limited, and the reason it's expensive, is that [attention](/wiki/ai/llm/attention) compares every word against every other word — so that part of the work grows not with the length of the text but with its *square*. This is the most-quoted cost fact about transformers and also the most frequently misapplied: at ordinary prompt lengths it is not, in fact, what you are paying for. The quadratic term does win eventually, and where it does is a number that can be worked out.

## What actually grows quadratically

Exactly one thing. Every row scores every row it can see, which is an n × n matrix of scores — per head, per block. That matrix, and the weighted sum that follows it, are the only parts of a transformer whose cost grows with the square of the sequence.

Everything else is linear. The Q/K/V projections, the [MLP](/wiki/ai/llm/the-mlp), and the norms all chew through one row at a time and neither know nor care how many rows there are, so doubling the context simply doubles their work. Attention's score matrix *quadruples*.

## So O(n²) is a crossover, not a flat tax

Two costs growing at different rates means one of them dominates below some length and the other above it.

Per block, the quadratic part costs roughly `4n²·d_model`. A good **kernel** — the hand-written GPU routine that does the attention arithmetic — skips the masked half and pays about half that. The linear part, projections plus MLP, costs roughly `24n·d_model²`. Set the two equal and the `n` you get is about `6·d_model`.

For [GPT-2 small](/wiki/ai/llm/gpt-2), with `d_model` = 768, that's around 4,600 tokens per block, or about 9,200 if the kernel exploits the mask. (For a whole forward pass, add the unembedding, which is linear in `n` and doesn't repeat per block: that pushes GPT-2 small's crossover out to about 6,700.) Below the crossover the MLP dominates. Above it, attention *is* the bill.

Notice what the crossover depends on: `d_model` alone — not the number of blocks, and not the total weight count. Stacking more blocks multiplies both terms equally and moves nothing. A *wider* model, `d_model` of 8192, doesn't reach the crossover until roughly 49,000 tokens.

Be careful what you take from that, though, because the obvious reading is wrong. Widening does not make long context cheaper. Go from 768 to 8192 and the quadratic work grows about 11× at fixed `n` while the linear work grows about 114× — attention's *share* of the compute falls, and its absolute cost still rises. And [the KV cache](/wiki/ai/llm/kv-cache) grows with width too, which is the constraint that actually binds. Wider models are less dominated by the quadratic term; they are not less troubled by long context. Nobody worried about any of this in 2019 with a 1024-token window; everybody does now, because contexts grew faster than models widened.

## What the famous optimizations do and don't fix

**FlashAttention doesn't repeal it.** What it removes is the *memory* cost of materializing that n × n matrix, by computing attention in tiles and never writing the full thing down. Since memory is usually the binding constraint in practice, this is an enormous win — but the arithmetic stays quadratic. It makes the quadratic term affordable, not linear.

**The [KV cache](/wiki/ai/llm/kv-cache) is usually what stops you first anyway.** It grows linearly with context, and linear growth in gigabytes beats quadratic growth in arithmetic when the arithmetic is fast and the memory is finite. Memory runs out before patience does.

That's the arithmetic sitting underneath [context engineering](/wiki/ai/context-engineering): a token isn't free, the marginal one costs more than the last, and past the crossover it costs *increasingly* more. Deciding what not to put in the context is a real engineering discipline for a real reason.

## Check yourself

Count arithmetic; don't trust a stopwatch. The claim to test is that attention is a minority of the work below the crossover, so compute the score matmul's share of a block directly: it's `n / (n + 6·d_model)`. At n = 128 that's **2.6%** of a [GPT-2 small](/wiki/ai/llm/gpt-2) block, and at n = 1024 — the largest window the model has — it's still only **18%**. Attention quadruples with every doubling and is nonetheless outvoted for the whole of GPT-2's range, which is the crossover argument in two numbers. Push `n` to 4,600 on paper and the share reaches half, by construction.

Then try to see it on a clock, and watch the measurement fail. Wall-clock won't quadruple cleanly: small `n` is dominated by fixed overhead, and past n ≈ 1024 the score matrix falls out of cache and jumps by *more* than 4×. Both effects are real and neither is the quadratic term — which is why the FLOP (floating-point operation) count is the honest instrument here and timing is not.

## Depends on / leads to

Depends on [the KV cache](/wiki/ai/llm/kv-cache) and [RoPE](/wiki/ai/llm/rope). Leads to [mixture of experts](/wiki/ai/llm/mixture-of-experts).
