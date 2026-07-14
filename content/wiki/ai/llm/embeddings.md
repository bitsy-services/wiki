---
title: "Embeddings"
weight: 110
---

The token id is an index, and the embedding matrix `W_E` is what it indexes. `W_E` is 50,257 × `d_model` — one row per vocabulary entry — and embedding token 3797 (`" cat"`) means fetching row 3797. No arithmetic. It's a lookup.

That row is the token's starting point in the model's space. Nobody assigns it; it falls out of training like any other weight, and its geometry is the model's entire prior about the token before it has seen any context. GPT-2 then *adds* a learned positional vector to it — same width, added rather than concatenated — so a token at two different positions doesn't start out identical. (Positional encoding: see the [backlog](/wiki/ai/llm/backlog).)

Which sets up the point: **at a given position, the row knows nothing about the sentence.** "bank" in a river sentence and "bank" in a money sentence enter the model as bit-identical rows. Every difference between them is added later and further right, by attention, into [the residual stream](/wiki/ai/llm/residual-stream). The embedding is the context-free prior; context is a correction applied on top of it.

`W_E` does double duty: GPT-2 ties it with the unembedding, so the matrix you look a token up in is the same matrix you dot the final row against to get [logits](/wiki/ai/llm/glossary).

## Check yourself

Put "bank" at token index 3 in two unrelated sentences and run GPT-2 small with `output_hidden_states=True`. `torch.equal` on `hidden_states[0][0, 3]` across the two returns **True** — bit-identical, because nothing has looked at the neighbors yet. At `hidden_states[12]` it returns False. Don't reach for cosine to size that gap: GPT-2's late rows sit in a narrow cone and cosine reads ~0.99 for almost any pair.

## Depends on / leads to

Depends on [tokenization](/wiki/ai/llm/tokenization). Leads to [the residual stream](/wiki/ai/llm/residual-stream), which is what that row becomes.
