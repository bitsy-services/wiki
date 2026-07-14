---
title: "Glossary"
weight: 20
---

The words this subsection uses — and it uses only these. Third column: what the same thing is called elsewhere, so you can translate when you leave.

| Term | Means | Elsewhere called |
|---|---|---|
| **row** | one token position's vector at some depth — `d_model` numbers wide | activation, hidden state, token representation |
| **`d_model`** | the row width. 768 in GPT-2 small, and fixed from embedding to unembedding | `n_embd`, hidden size, model dimension |
| **residual stream** | the row seen as a bus running rightward through every block: blocks add into it and never overwrite it | hidden state, skip path |
| **block** | one attention plus one MLP, each wrapped in a norm and a skip connection. GPT-2 small has 12 | layer, transformer layer, decoder layer |
| **MLP bulge** | the MLP widening a row to 4×`d_model` (3072) and back down. The only place a row isn't `d_model` wide | feed-forward, FFN, hidden dim |
| **head** | one attention channel: its own Q/K/V projections into a 64-wide subspace. 12 per block in GPT-2 small | attention head |
| **attention pattern** | one row's post-softmax weights over the rows it can see. Sums to 1 | attention weights, attention map |
| **KV cache** | keys and values already computed for earlier rows, kept so the next token doesn't recompute them | `past_key_values`, decoder cache |
| **logits** | the raw scores at the right edge — one per vocabulary entry (50,257), before softmax | scores, unnormalized log-probs |
| **unembedding** | the matrix that turns the final row into logits. Tied to the embedding in GPT-2 | `lm_head`, output head, `W_U` |
| **perplexity** | `exp(loss)` — roughly, how many tokens the model is choosing between | PPL |
| **feature** | a direction in the stream that means something | concept, latent |

## Words this subsection avoids

- **"Layer"** — ambiguous between a block and a sublayer inside it. Say *block*, *attention*, or *MLP*. (LayerNorm keeps its name; it's a proper noun.)
- **"Deeper," "up the stack"** — spatially wrong here; depth runs rightward. See [conventions](/wiki/ai/llm/conventions).
- **"Column"** — a row is never one, whatever shape the tensor is in memory.

## Depends on / leads to

Depends on [conventions](/wiki/ai/llm/conventions). Leads to every other page; the [backlog](/wiki/ai/llm/backlog) has the order.
