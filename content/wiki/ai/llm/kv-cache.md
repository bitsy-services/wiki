---
title: "The KV Cache"
weight: 260
---

The KV cache is the reason generating a long response doesn't get dramatically slower with every word added. Producing each new token means running the model over everything written so far — and nearly all of that work is identical to the work already done for the previous token, over text that hasn't changed since. The cache is the observation that the repetition isn't merely wasteful but entirely avoidable: the model can keep what it worked out about each earlier word and reuse it, unchanged, for the rest of the conversation. It is the most important optimization in serving a language model, and it is paid for in memory.

## The waste, stated plainly

Generating token 500 means a forward pass over 499 existing rows in order to produce one new row.

Do that naively for every token and you rebuild the entire prefix each time — the same keys, the same values, derived from the same rows, whose contents have not moved since they were first computed. Over the course of a 500-token reply, the first row's key and value get recomputed 500 times, and every one of those computations returns the same answer.

## Why it's safe to keep them

The permission comes from [the causal mask](/wiki/ai/llm/causal-mask), and it's worth being clear that this is a *correctness* argument rather than a heuristic.

A row can only depend on itself and the rows above it. So once a row has been computed it is final — appending tokens below it cannot change it, because those tokens are not inputs to it. Its key and its value are constants for the remainder of the sequence. Keeping them isn't an approximation of recomputing them; it's the same numbers, retrieved instead of rebuilt.

It's the difference between reading a book with marginal notes and re-reading it from page one every time you turn a page. Your notes on chapter 1 are still good when you reach chapter 12, and they're still good precisely because nothing in chapter 12 can retroactively change what chapter 1 said.

## What a step costs once you have it

With the cache in place, each new token does one row's worth of work: project the new row to its query, key, and value, append that key and value to the store, attend against everything in the store, run the MLP.

Attending to *n* rows still costs O(n) — the new row does have to be compared against every earlier one, and no cache avoids that. What's gone is the rebuilding of those *n* rows, which is a whole factor of *n* off every step.

## The price is memory, and it grows with the conversation

Two tensors per block per row, held for as long as the conversation lives. For [GPT-2 small](/wiki/ai/llm/gpt-2) that's 2 × 12 × 768 = 18,432 numbers per token, or 36 KB in 16-bit precision. Across its entire 1024-token window that comes to 36 MB, which is nothing — nobody ever worried about GPT-2's cache.

Hold the per-token figure and change the model, though, and the picture inverts. A cache costs `2 × blocks × d_model` numbers per token, so it grows with both depth and width, and modern models are far larger in both while also serving contexts a hundred times longer. A frontier-scale model runs to megabytes per token rather than kilobytes, which puts a single long conversation into the tens or hundreds of gigabytes — for one user, on a card that also has to hold the weights.

Two things follow, and they shape how models are built and sold.

Long context is a **memory** problem before it is a compute problem: you run out of room to store the cache well before you run out of patience waiting for the arithmetic. That's the pressure behind [grouped-query attention](/wiki/ai/llm/grouped-query-attention), which exists almost entirely to make this number smaller.

And because the cache is exactly reusable, it is also *sellable*. [Prompt caching](/wiki/ai/prompt-caching) is a provider keeping your prefix's keys and values warm between requests so neither of you pays to rebuild them — the same invariant, billed.

## Check yourself

[Generate](/wiki/ai/llm/running-the-checks) greedily from GPT-2 small with `use_cache=True`, then `False`. The tokens come out identical — the cache is an optimization, not an approximation. The speedup is smaller than you'd guess and grows with context: ~2× at 200 tokens, ~4.8× at 1000. Emitting tokens one at a time — **decode**, as opposed to the single parallel pass over your prompt — is bound by [reading the model's weights out of memory](/wiki/ai/llm/training-vs-inference-parallelism), which both runs do equally; the cache only removes attention work.

## Depends on / leads to

Depends on [the causal mask](/wiki/ai/llm/causal-mask). Leads to [grouped-query attention](/wiki/ai/llm/grouped-query-attention) — the standard way to make this cache smaller — then [training vs inference parallelism](/wiki/ai/llm/training-vs-inference-parallelism) and [context length and the O(n²) cost](/wiki/ai/llm/context-length).
