---
title: "The Causal Mask"
weight: 150
---

The causal mask is the rule that a word may look backward but never forward. Attention, left to its own devices, lets every position read every other position — including the ones that come after it. The mask is what forbids the second half of that: a fixed, unlearned rule applied inside every head of every block, erasing any attempt to look ahead before it can have an effect. It is the smallest thing in the architecture and one of the most consequential, because almost everything about how these models are trained and served rests on it holding.

## Why looking ahead would be fatal

The reason is training, though the mask is usually explained as though it were about generation. The mask bites whenever a single pass covers more than one new row — which is training, and also the **prefill** step that processes a prompt all at once. When the model is emitting tokens one at a time, each pass adds a single row, the future genuinely doesn't exist yet, and there is nothing to peek at.

Training is where it earns its keep. A single forward pass over a sequence makes a prediction at *every* row at once — feed in 1024 tokens and you get 1023 scored guesses out, one for each position that has a next token to be checked against. That is the arrangement that makes training on internet-scale text affordable in the first place, and it is [most of the reason the architecture won](/wiki/ai/llm/why-scale-worked).

But it only works if each of those predictions is honest. If row 5 could see row 6, then the answer to "what follows row 5?" would be sitting right there in the input. [The loss](/wiki/ai/neural-network/the-loss-function) would collapse to nearly zero, the gradients would carry no useful signal, and the model would learn to copy rather than to predict — a machine that scores beautifully in training and is worthless the moment it has to produce a token that isn't already on the page.

It's an exam with the answer key stapled to the question paper. Everyone gets full marks and nobody learns anything. The mask is what unstaples it, and it is what lets you get a thousand honest questions out of one sheet.

## The mechanism: a triangle of −∞

The scores are computed for every pair of positions — the machinery doesn't know yet which ones it's allowed to use. Then, before the softmax, every score pointing at a row further down the sequence has −∞ added to it.

```text
                 key: pos 0   pos 1   pos 2   pos 3

  query pos 0         s₀₀     −∞      −∞      −∞
  query pos 1         s₁₀     s₁₁     −∞      −∞
  query pos 2         s₂₀     s₂₁     s₂₂     −∞
  query pos 3         s₃₀     s₃₁     s₃₂     s₃₃
```

Softmax exponentiates, and `exp(−∞)` is 0, so those positions come out at exactly zero weight — not small, zero — and the remaining weights renormalize to sum to one on their own, with no extra step. A row on the diagonal always sees itself.

Implementations split on how literally to take the −∞. nanoGPT uses a true `float('-inf')`, as does PyTorch's fused causal path. HuggingFace's eager GPT-2 uses the smallest finite value the dtype can hold — `torch.finfo(dtype).min`, which is -3.4e38 in float32 — and older codebases often hard-code an arbitrary `-1e9`. The arithmetic comes out the same, since `exp` of anything that negative is zero either way. The reason to prefer a finite floor is an edge case: a row where *everything* is masked gives 0/0 under true −∞, and NaN propagates from there through the rest of the model.

You could get the same numbers by letting softmax run unmasked, zeroing the forbidden weights afterwards, and renormalizing by hand. Nobody does, and the reason isn't the one you'd guess. It isn't overflow — every real softmax subtracts the row's maximum before exponentiating, so nothing overflows regardless. It's that if a masked score happens to *be* the row maximum, every legitimate score gets shifted far below it, their exponentials underflow toward zero, and you renormalize what little precision survived. Masking first sidesteps that, and saves a second normalization pass into the bargain.

## What it buys for free: rows are final

Erasing the forward direction has a consequence nobody had to design for, and it is arguably worth more than the training property.

A row can only ever depend on itself and the rows above it. So once a row has been computed, it is **final** — appending more tokens below cannot change it, ever. Not approximately, not usually: the later tokens are not inputs to it at all.

That invariant is the ground every serving optimization stands on. [The KV cache](/wiki/ai/llm/kv-cache) keeps each row's keys and values precisely because they can never need recomputing. [Prompt caching](/wiki/ai/prompt-caching) resells the same fact at the API layer: a conversation beginning with the same 8,000 tokens as the last one would repeat exactly the work already done for that prefix, so the vendor keeps the result rather than redoing it, and charges you less for the hit. Both are the mask, monetized.

It is also what the word **autoregressive** actually means. Not "generates one token at a time" — that's a consequence — but "each position is a function only of the positions before it."

## Check yourself

Run [GPT-2 small](/wiki/ai/llm/gpt-2) on `"the cat sat on the"`, keep [`hidden_states[6][0, 2]`](/wiki/ai/llm/running-the-checks), then run `"the cat sat on the mat, which was"` — same prefix, more rows below — and pull it again. `torch.allclose` passes. It is *not* bit-identical: float32 reductions change order with sequence length, and the drift grows rightward to ~1e-5 by block 11. The invariant is exact in real arithmetic, approximate in floats. A leak would show up as a large difference, not a rounding one.

## Depends on / leads to

Depends on [one attention head](/wiki/ai/llm/one-attention-head). Leads to [the KV cache](/wiki/ai/llm/kv-cache) and [training vs inference parallelism](/wiki/ai/llm/training-vs-inference-parallelism).
