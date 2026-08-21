---
title: "Attention"
weight: 125
---

Attention is the part of a model that lets one word take account of another. Everything else in a transformer handles each position on its own: a word is processed without reference to its neighbours, as though it arrived alone. Attention is the exception, and it is the *only* exception — the sole mechanism by which information moves between positions. Remove it and what's left is a machine that reads every word in isolation and can never relate any of them.

It is also the piece the architecture is named for, and the one that costs the most to run. Nearly everything expensive or clever about serving a model traces back to it.

## The problem it solves

[Embeddings](/wiki/ai/llm/embeddings) hand the model one context-free vector per [token](/wiki/ai/llm/tokenization): "bank" arrives bit-identical whether the sentence is about rivers or money. That is the whole difficulty in one line. A word's meaning is mostly a function of the words around it, and at the moment the model starts work, no position knows anything about any other.

So something has to move information between positions. The question is what that something should look like — and the answer isn't obvious, because two plausible designs both fail.

**Fixed wiring doesn't work.** You could hard-code "every word looks at the three words before it." But the word that disambiguates "bank" might be one token back or two hundred, and *which* word matters depends entirely on what the sentence says. Any pattern fixed in advance is wrong for most sentences.

**Reading in order doesn't work either.** The previous generation of language models handled this with *recurrence*: read left to right, carrying a running summary of everything so far. That fails three ways. Everything must squeeze through one fixed-size summary, so early detail gets crushed out. Distant words degrade, because information survives only by being copied forward at every step. And it's inherently sequential — you can't start word 50 until you've finished word 49 — which makes training ruinously slow.

What's wanted is a scheme where any word can reach any other directly, where *which* words connect is decided by their content rather than fixed ahead of time, and where every position can be worked out at once.

## The idea: let every word ask

Attention gets all three by turning the problem into a lookup.

Each position — one token's vector, which this subsection calls a [row](/wiki/ai/llm/glossary) — emits a **query**: a description of what it's looking for. Every position also exposes a **key**: a description of what it has to offer. Compare a query against a key and the strength of the match says how relevant that position is to this one. Run that comparison against every position it's allowed to see and you get one score each, which [softmax](/wiki/ai/llm/softmax-and-temperature) squashes into weights that sum to one. That set of weights is the row's [attention pattern](/wiki/ai/llm/glossary): where this word's attention goes.

Then each position offers a **value**: what it actually contributes if something looks at it. The asking position receives a blend of the values, mixed in proportion to the pattern, and adds that blend to [its own running total](/wiki/ai/llm/residual-stream).

```text
                            depth  →

  pos 0  "The"     key ──┐   value ──┐
  pos 1  " cat"    key ──┤   value ──┤
  pos 2  " sat"    key ──┤   value ──┤
  pos 3  " on"     key ──┤   value ──┤
  pos 4  " the"    key ──┤   value ──┤   ← a row reads itself, too
                         │           │
        pos 4's query ───┘           ▼
                                  [·······] ──▶ the blend is added to
                                                pos 4's row, which
                                                carries on rightward

  1. dot pos 4's query against every key at or above it — one score each
  2. soften the scores into weights that sum to 1 (the attention pattern)
  3. blend the values in those proportions
```

It's worth being clear about what the words mean, because the query/key/value naming is borrowed from databases and only half fits. A database lookup finds the one row whose key matches exactly. Attention matches *softly* against everything at once and takes a weighted blend — much of it noise. Nothing is retrieved; it's averaged.

The crucial property is that the weights are computed at run time, from the content of the vectors. Nothing in the model says "adjectives should look at nouns." A head that does that has *learned* to, by shaping adjective-queries that happen to match noun-keys — and if the sentence changes, the pattern changes with it. That is what makes it attention rather than fixed wiring.

## What it buys

**Any distance costs the same.** Two hundred tokens back is one comparison, exactly like one token back. There is no chain to survive and nothing to decay along the way — the reason attention handles long-range dependencies that recurrence loses.

**Every position at once.** Within a single attention step, no position's query depends on another position's output *from that same step*: everything a query reads is already sitting in the stream, put there by the step before. So the whole sequence can be worked out together instead of one word at a time. That's the real contrast with recurrence, where word 50 literally cannot begin until word 49 has produced its summary. This is what made training on internet-scale corpora practical, and it is [arguably the whole reason the architecture won](/wiki/ai/llm/why-scale-worked) — though it's a *training* property, and [generation gets none of it](/wiki/ai/llm/training-vs-inference-parallelism), since the next word can't be attended to before it exists.

**The routing is learned.** Nobody specifies which words should talk. The model works it out, differently for every sentence.

## What it costs

The bill is in the design. Every position compares itself against every position, so the work grows with the *square* of the sequence: double the text and you quadruple the comparisons. This is where the famous O(n²) comes from, and it's the single fact behind most of the engineering around [context length](/wiki/ai/llm/context-length) — including [the KV cache](/wiki/ai/llm/kv-cache), which spares the model rebuilding every earlier position's keys and values from scratch each time it generates a word. (The comparisons themselves still happen; it's the re-deriving that's skipped.)

Attention also arrives with no notion of order: a query matched against a key gives the same score however the sequence is shuffled, so position has to be [added deliberately](/wiki/ai/llm/positional-encoding).

## Where the detail lives

This page is the shape of the thing. Four pages take it apart:

- [One attention head](/wiki/ai/llm/one-attention-head) — the actual arithmetic, start to finish.
- [Q/K/V as three projections](/wiki/ai/llm/qkv-projections) — where query, key, and value come from. They aren't three things a row *has*; they're three learned views of the same row.
- [The causal mask](/wiki/ai/llm/causal-mask) — why a word may look backward but never forward.
- [Multi-head attention](/wiki/ai/llm/multi-head-attention) — a dozen of these run side by side per block, each chasing a different relationship.

## Check yourself

Test the claim in the first paragraph: that attention is the only path between positions. Run [GPT-2 small](/wiki/ai/llm/gpt-2) on a sentence and keep the final row for the last token. Change a word near the *start* and re-run — the last row moves, as you'd expect, because information travelled.

Now do it with attention switched off. Zero every block's attention output with a [forward hook](/wiki/ai/llm/running-the-checks) — PyTorch's callback for replacing a module's output — on `model.transformer.h[i].attn.c_proj`, returning `torch.zeros_like(output)`. Hook `c_proj` rather than `.attn` itself: `.attn` hands back a tuple, not a plain tensor, and the block will index into your replacement instead of using it.

Swap that early word for **another single token** and the last row now comes back bit-identical. Keep the token count fixed or the test is void — a replacement that tokenizes to a different length shifts every later position, which changes their positional embeddings and moves the row for reasons that have nothing to do with attention.

With attention gone, position 5 cannot be reached by anything at position 2: every remaining part of the model — [the MLP](/wiki/ai/llm/the-mlp) and the [norms](/wiki/ai/neural-network/normalization) included — only ever reads the row it's standing on. Generate from it and you'll see what that costs. Predicting from one token and its position alone is roughly a lookup table over single tokens, so greedy decoding falls into a loop almost immediately. Not a model writing badly — a model that cannot read its own prompt.

## Depends on / leads to

Depends on [the residual stream](/wiki/ai/llm/residual-stream). Leads to [one attention head](/wiki/ai/llm/one-attention-head), where the arithmetic gets done.
