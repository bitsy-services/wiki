---
title: "Embeddings"
weight: 110
---

An embedding is where a token stops being an arbitrary label and becomes a position in a space the model has opinions about. Every entry in the vocabulary owns its own list of numbers, learned during training, and embedding a token means fetching its list — pulling one row out of a table. Nothing is calculated. This is the model's first move, and it is the least clever thing it does all day.

## Why a lookup, and not a calculation

The obvious alternative is to *derive* the vector from the token's id. That fails at the first step, because the id carries no information about what the token **means**.

It isn't quite meaningless. [Tokenization](/wiki/ai/llm/tokenization) builds the vocabulary by merging the most frequent pair first, so the ids come out roughly in frequency order: a low id is a common, short token, a high one is rarer and longer. But frequency rank is the whole of it. `" cat"` is 3797 because of where it landed in that queue years ago, and 3798 — the next merge the table happened to learn — is just the next-most-frequent pair, with nothing catlike about it. There is no function of "3797" that could tell you it's an animal, because nothing about catness was ever encoded into the number.

So every relationship *of meaning* between tokens has to be **stored** rather than derived. The model keeps one vector per vocabulary entry and looks the right one up. A table is the honest data structure for facts that have no pattern to exploit.

## What's in the row

The table is called `W_E`, the embedding matrix: one row per vocabulary entry — 50,257 of them in [GPT-2](/wiki/ai/llm/gpt-2) — each as wide as [`d_model`](/wiki/ai/llm/glossary), the fixed width that every row in the model carries from here to the far end. Embedding token 3797 means taking row 3797. That's the whole operation.

Nobody chooses the contents. They start as noise and get shaped by [training](/wiki/ai/llm/the-loss-function) exactly like every other weight in the model, which means the geometry is *earned*: tokens that behave alike drift into pointing alike, because the model kept being rewarded for treating them alike. What you get is the model's entire prior about a token — everything it believes about `" cat"` before it has seen a single neighbour.

One thing the lookup can't supply is position. Fetching a row by id can't know whether the token sat first in the sentence or fortieth, so GPT-2 adds a second learned vector — one per slot — on top of the row before the first block. Same width, added rather than stuck on the end, so a token in two different places doesn't start out identical. That's [positional encoding](/wiki/ai/llm/positional-encoding).

## The row knows nothing about the sentence

This is the part worth carrying forward. **At this point, the row has no idea what sentence it's in.**

"Bank" in a river sentence and "bank" in a money sentence enter the model as *bit-identical* rows. Not similar — the same numbers. The embedding is a context-free prior, and it is the same prior every time the token appears, in every sentence anyone has ever written.

Every difference between those two "bank"s is added later and further right, by [attention](/wiki/ai/llm/attention), into [the residual stream](/wiki/ai/llm/residual-stream). Which reframes what the rest of the model is for: the embedding is the starting guess, and context is a correction applied on top of it.

## One table, two jobs

`W_E` earns its keep twice. GPT-2 **ties** it to the unembedding, so the table you look a token up in on the way *in* is the same table the final row is scored against on the way *out* to produce [logits](/wiki/ai/llm/glossary). One set of numbers, both edges of the model — see [the unembedding](/wiki/ai/llm/unembedding-and-logits) for what that costs and buys.

## Check yourself

Put "bank" at the same token index in two unrelated sentences — one about rivers, one about money — and [run](/wiki/ai/llm/running-the-checks) GPT-2 small with `output_hidden_states=True`, which makes it hand back the row at every step instead of just the final answer.

Two things must be held fixed or the test is void. The index has to match across the two sentences, or you've changed the position vector as well and measured nothing. And it has to be the *same token*, not merely the same word — `" bank"` and `"Bank"` are different ids with unrelated rows, exactly as [tokenization](/wiki/ai/llm/tokenization) warned. A shared prefix guarantees both: "The bank was muddy" and "The bank was closed", with `" bank"` at index 1 in each.

`hidden_states[0]` is the state before any block has run: embedding plus position, and nothing else. Run `torch.equal` on that row across the two sentences and it returns **True**. Bit-identical, because nothing has yet looked at a neighbour.

Pull the same row out of `hidden_states[12]` — after all twelve blocks *and* the final norm, which HuggingFace applies before appending that last one — and `torch.equal` returns False. Everything separating river-bank from money-bank was built in those twelve steps, out of the neighbours.

One warning if you try to *measure* that gap rather than just detect it. Cosine similarity — the usual "how alike are two vectors" number — is no use here. GPT-2's late rows all crowd into a narrow cone of the space, so almost any pair of them reads about 0.99 whether they're related or not. The rows genuinely differ; cosine just can't see it.

## Depends on / leads to

Depends on [tokenization](/wiki/ai/llm/tokenization). Leads to [the residual stream](/wiki/ai/llm/residual-stream), which is what that row becomes.
