---
title: "Glossary"
weight: 20
---

These are the words this subsection uses, and it uses only these. The third column lists the names you'll meet elsewhere for the same thing, so you can translate when you leave.

| Term | Means | Elsewhere called |
|---|---|---|
| **row** | one token position's vector at some depth — `d_model` numbers wide | activation, hidden state, token representation |
| **`d_model`** | the row width. 768 in GPT-2 small, and fixed from embedding to unembedding | `n_embd`, hidden size, model dimension |
| **residual stream** | the row seen as a bus running rightward through every block: blocks add into it and never overwrite it | hidden state, skip path |
| **block** | one attention plus one MLP, each wrapped in a norm and a skip connection. GPT-2 small has 12 | layer, transformer layer, decoder layer |
| **MLP bulge** | the MLP widening a row to 4×`d_model` (3072 in GPT-2 small) and back down. The only place a row isn't `d_model` wide | feed-forward, FFN, hidden dim |
| **KV cache** | keys and values already computed for earlier rows, kept so the next token doesn't recompute them | `past_key_values`, decoder cache |
| **logits** | the raw scores at the right edge — one per vocabulary entry (50,257 in GPT-2), before softmax | scores, unnormalized log-probs |

## Words this subsection avoids

**"Layer."** Ambiguous between a whole block and one sublayer inside it. Say *block*, *attention*, or *MLP*.

**"Deeper," "up the stack."** Spatially wrong here — depth runs rightward. See [conventions](/wiki/ai/llm/conventions).

**"Column."** A row is never a column, no matter what shape the tensor is in memory.

## Depends on / leads to

Depends on [conventions](/wiki/ai/llm/conventions). Leads to every other page; the [backlog](/wiki/ai/llm/backlog) has the order.
