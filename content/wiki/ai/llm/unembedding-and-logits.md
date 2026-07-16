---
title: "The Unembedding and Logits"
weight: 200
---

The final row is 768 numbers. The vocabulary has 50,257 entries. The unembedding closes that gap with a single matrix multiply and nothing else.

After the final norm, the row is dotted against one vector per vocabulary entry. The score for token *t* is `dot(row, W_U[t])` — literally: how much does this row point in token *t*'s direction? Those 50,257 scores are the [logits](/wiki/ai/llm/glossary). No search, no nonlinearity, no table of stored continuations. The model's answer is one vector, and the vocabulary is a set of directions to compare it against — direction picks the winner, magnitude decides how confident the logits look.

[GPT-2](/wiki/ai/llm/gpt-2) **ties** the unembedding to the [embedding](/wiki/ai/llm/embeddings) matrix — `W_U` is `W_E` transposed, the same 38.6M numbers doing duty at both edges. The vector you look a token up in is the vector you're scored against for predicting it.

Every row produces logits, not just the bottom one. Training uses all of them ([one sequence, a thousand predictions](/wiki/ai/llm/the-loss-function)); generation throws away all but the bottom row's, which is the only one whose next token you don't already know.

## Check yourself

Run GPT-2 small with `output_hidden_states=True`. HuggingFace's last hidden state is already post-final-norm, so `hidden_states[-1] @ model.transformer.wte.weight.T` reproduces `outputs.logits` exactly — `torch.allclose` passes. One matmul, tied weights, no residue. If you expected an extra bias term, there isn't one.

## Depends on / leads to

Depends on [the residual stream](/wiki/ai/llm/residual-stream) and [embeddings](/wiki/ai/llm/embeddings). Leads to [softmax and temperature](/wiki/ai/llm/softmax-and-temperature).
