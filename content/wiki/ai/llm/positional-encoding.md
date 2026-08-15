---
title: "Positional Encoding"
weight: 270
---

A transformer, left to itself, has very little idea what order the words came in. Attention compares positions against each other by content, and nothing in that comparison records which one came first — the arithmetic that scores a word against its neighbour is the same arithmetic whichever way round they sit. Since word order carries a great deal of the meaning in most sentences, position has to be supplied deliberately, as an extra signal mixed into each word before the model starts work. Positional encoding is that signal, and the particular way it's built turns out to set a hard ceiling on how long a conversation the model can ever have.

## Why the machinery is order-blind

[Attention](/wiki/ai/llm/attention) scores a row by dotting its [query against another row's key](/wiki/ai/llm/qkv-projections) — two learned readings of the rows involved. Both were computed from the rows themselves, and a row at this stage is just an [embedding](/wiki/ai/llm/embeddings): a lookup in a table indexed by token id. Nothing in the table knows where the token appeared, because the same token gets the same vector wherever it turns up.

So the scores are a function of *which* words are present, not of their arrangement. Shuffle the sentence and, as far as the comparison is concerned, nothing has changed. Position has to be injected on purpose or it isn't there.

## GPT-2's answer: one learned vector per slot

[GPT-2](/wiki/ai/llm/gpt-2) injects it once, at the left edge, and never again.

It learns a vector per position — `wpe`, one row per slot in the window, [the only weight in the model with a position axis](/wiki/ai/llm/weight-sharing) — and *adds* it to the embedding before block 0 sees anything.

Adding is worth a moment, because concatenating is the more obvious choice and it would cost you. Concatenation would widen the row, and every matrix downstream along with it. Addition keeps the row exactly `d_model` wide, so position costs nothing in width and adds no parameters anywhere but the table itself.

But then why doesn't adding one vector to another simply corrupt the content? Because a 768-wide row has room for far more nearly-perpendicular directions than the model has distinct things to say in any one place. Position can settle into a subspace that content mostly avoids, and the projections downstream can learn to read one without picking up much of the other — the capacity argument [superposition](/wiki/ai/llm/superposition) makes in general.

Position is an unusual case of it, though, and worth flagging as one. Superposition's bargain is that collisions are affordable *because* the colliding features are sparse: almost none of them are active on any given word, so they mostly don't collide at the same moment. Position is active on every row without exception. Whatever room it occupies, it occupies permanently, and whatever interference it causes is paid on every token rather than now and then. It's a standing tax, not an occasional collision.

## That's cheap, it works, and it has two defects

**The table is finite.** There are 1024 rows in GPT-2 small. There is no vector for position 1024, so there is no position 1024. The blocks themselves would process row 5000 without complaint; the table is the only thing stopping them.

**It's absolute.** The vector for position 300 bears no built-in relation to the vector for 301. Nothing in the scheme encodes that they're adjacent — the model has to learn that from data, and it has to learn it *again* for 301 and 302, and again for every other pair. So "three tokens back," which is one fact, is a different geometric fact at every position in the window, learned separately at each.

[RoPE](/wiki/ai/llm/rope) fixes both, by making the score between two tokens depend only on the distance between them — there is no table to run out of, and "three tokens back" becomes one fact rather than a thousand. The second defect is the one that motivated it.

## One subtlety worth carrying forward

A model like GPT-2 trained with *no* positional encoding at all isn't actually position-blind. [The causal mask](/wiki/ai/llm/causal-mask) leaks order on its own — row 0 can see one row, row 5 can see six — and models trained that way do recover a usable sense of position from that alone.

Don't try to demonstrate this by zeroing GPT-2's `wpe`. It was trained *with* a position table, its weights depend on one being there, and all you will get is a broken model. The claim is about models trained without one from the start.

## Check yourself

Position enters GPT-2 in exactly one place, by addition. [Confirm it](/wiki/ai/llm/running-the-checks): `hidden_states[0][0, i]` equals `wte[token_i] + wpe[i]`, to `torch.allclose`. Then zero `wpe` and measure [perplexity](/wiki/ai/llm/perplexity) on WikiText — it explodes. That's the broken model warned about just above, and it's worth being clear about which claim it supports: it shows how heavily *this* model leans on its table, not that position is indispensable in general. One table, added once, and everything downstream built on top of it.

## Depends on / leads to

Depends on [embeddings](/wiki/ai/llm/embeddings) and [weight sharing](/wiki/ai/llm/weight-sharing). Leads to [RoPE](/wiki/ai/llm/rope).
