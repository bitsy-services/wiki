---
title: "Weight Sharing Across Positions"
weight: 250
---

Weight sharing is the fact that the model uses the same numbers everywhere along the sequence. There is no separate copy of the machinery for a word near the start and a word much later on — the same weights per block process every position identically, whichever position it happens to be. This is easy to skim past as a memory-saving trick, and it isn't one. It is what makes the thing a language model rather than an enormous lookup table indexed by where in the sentence you are.

## What the alternative would actually look like

The point is clearest if you take the other option seriously for a moment. Suppose there really were a "block 6 for position 300" — its own attention matrices, its own MLP, distinct from block 6's machinery at position 299.

The parameter count is the least of the problems, though it is spectacular. The blocks hold about 85M of GPT-2 small's weights; multiply those by 1024 positions and you have a model of roughly 87 billion, no more capable than the 124M one it came from.

The fatal problem is that **nothing learned anywhere would transfer anywhere else.** Whatever it takes to learn "attend to the subject of this clause," the model would have to learn it separately at position 12, at position 13, at position 700 — each time from scratch, each time from only the training examples that happened to place a clause boundary at exactly that offset. Every position would get roughly a thousandth of the signal the shared version gets, to learn the identical thing a thousand times over. You would be training a thousand small, badly-informed models that happen to be stapled together.

And a sequence longer than the training window would be not merely unsupported but *meaningless*: position 1025 would have no weights.

## What sharing buys

Learn it once, use it everywhere. A pattern worth detecting is worth detecting wherever it occurs, and sharing is what encodes that assumption into the architecture rather than hoping the model discovers it.

It's the difference between a grammar and a phrasebook. A phrasebook indexed by position — "at word 40, say this" — is useless the moment anything shifts. A rule applies wherever it fits.

Sharing also multiplies the training signal. Gradients from every position in every sequence pile into the same matrices, which is why [one sequence teaches a weight a thousand times over](/wiki/ai/neural-network/backprop-one-weight). Per weight, the effective dataset is the whole corpus times the sequence length.

## No weight inside a block knows how long the sequence is

Here is the consequence people miss, and it's the one that matters downstream.

Because the same matrices apply everywhere, none of them has a position axis at all. Doubling the context window costs compute and [KV cache](/wiki/ai/llm/kv-cache) memory — both of which grow with the sequence — but it does not add a single parameter to any attention or MLP matrix. The blocks are entirely blind to sequence length. Hand block 6 a row from position 5000 and it will process it perfectly happily, having no way to know that's unusual.

## The one exception, and it's the interesting one

[GPT-2](/wiki/ai/llm/gpt-2) learns an absolute [positional](/wiki/ai/llm/positional-encoding) vector per position — `wpe`, shaped `[1024, 768]`. It is the only weight in the entire model with a position axis.

Everything about GPT-2's context limit follows from that one table. Widen the context to 4096 and `wpe` grows by 2.4M parameters while every block stays byte-for-byte the size it was. And the 1024-token limit is *not* an architectural limit — the blocks would happily process row 5000, as above. There is simply no vector to tell row 5000 where it is.

That's a useful thing to have straight, because it reframes what extending context means. It isn't a matter of making the model bigger. It's a matter of finding a way to say "you are at position 5000" that doesn't require having stored a vector for it in advance — which is exactly what [RoPE](/wiki/ai/llm/rope) does.

## Check yourself

[List the parameters](/wiki/ai/llm/running-the-checks) of GPT-2 small whose shape mentions 1024: `[n for n, p in model.named_parameters() if 1024 in p.shape]`. You get `transformer.wpe.weight`, and nothing else. Every other weight in the model is blind to how long the sequence is.

## Depends on / leads to

Depends on [backprop through one weight](/wiki/ai/neural-network/backprop-one-weight). Leads to [the KV cache](/wiki/ai/llm/kv-cache) and [positional encoding](/wiki/ai/llm/positional-encoding).
