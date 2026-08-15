---
title: "The Unembedding and Logits"
weight: 200
---

The unembedding is the model's last act: turning the vector it has spent the entire forward pass refining into a score for every word it might say next. Everything up to this point has been about improving one list of numbers per token position. This step compares that list against the whole vocabulary, entry by entry, and reports how well each one matches. The scores it produces are the **logits** — the model's raw opinion, not yet probabilities and not yet a choice, but a complete ranking with magnitudes attached.

## The gap that has to be closed

At the right edge of the model there is a row: `d_model` numbers, 768 of them in [GPT-2 small](/wiki/ai/llm/gpt-2). What's wanted is one number per [vocabulary](/wiki/ai/llm/glossary) entry, 50,257 of them. Something has to bridge those two shapes.

It is worth pausing on how much simpler the answer is than the alternatives you might reasonably imagine. There is no search through candidate continuations. There is no stored table of "phrases that followed this context during training." There is no second network that scores proposals. There is one matrix multiply, and then the model is done.

## One dot product per vocabulary entry

After the [final norm](/wiki/ai/llm/normalization), the row is dotted against one vector per vocabulary entry. The score for token *t* is `dot(row, W_U[t])`, which reads literally as: *how much does this row point in token t's direction?*

That's the whole mechanism, and the geometric picture is the one to keep. The vocabulary is not a list of words the model chooses among — it's 50,257 fixed directions planted in the row's space. The model's answer is a single arrow. Scoring is measuring how far that arrow leans toward each direction, and the winner is whichever it leans toward most.

Two things fall out of that immediately:

- **Direction picks the winner.** Only where the arrow points decides the ranking.
- **Magnitude decides how confident the logits look.** Double the row's length and every score doubles — the ranking unchanged, but every gap between scores twice as wide, which once [softmax](/wiki/ai/llm/softmax-and-temperature) gets hold of them is a dramatically more confident-looking model saying exactly the same thing.

That second one is precisely why [the final norm](/wiki/ai/llm/normalization) is there. The residual stream grows enormously as it crosses the blocks, and if that accumulated magnitude reached the unembedding untouched, the model's apparent confidence would be a side effect of depth rather than a statement about the text. The norm fixes the scale before the comparison happens, which means you won't observe this effect in a working model — you have to force it by hand, as the check below does.

## The same matrix at both ends

[GPT-2](/wiki/ai/llm/gpt-2) **ties** the unembedding to [the embedding](/wiki/ai/llm/embeddings) table: `W_U` is `W_E` transposed, one set of about 38.6M numbers doing duty at both edges of the model rather than two.

The consequence is a pleasing symmetry. The vector you look a token up in, on the way *in*, is the vector you are scored against for predicting it, on the way *out*. A token's row in that table is simultaneously "what this word means when you read it" and "what a context should look like for this word to be the answer" — one representation asked to serve both jobs. That saves a great deal of memory, mildly constrains what the model can express, and is standard practice. (It is a different thing from [sharing weights across positions](/wiki/ai/llm/weight-sharing), which every model does and which nobody counts as tying.)

## Every row produces logits, not just the last one

The unembedding runs at *every* position, not only the final one. A 5-token prompt produces a full 50,257-wide score vector five times over.

Training needs nearly all of them — [one sequence, a thousand predictions](/wiki/ai/llm/the-loss-function), every row but the very last, which is the arrangement the economics of the whole field rest on. Generation throws away all but the bottom row's, because it's the only one whose next token you don't already know.

So the model's answer is one vector, and the vocabulary is a set of directions to measure it against. No search, no nonlinearity, no lookup, no bias term. The most consequential step in the forward pass is also the least eventful.

## Check yourself

[Run](/wiki/ai/llm/running-the-checks) GPT-2 small with `output_hidden_states=True`. HuggingFace's last hidden state is already post-final-norm, so `hidden_states[-1] @ model.transformer.wte.weight.T` reproduces `outputs.logits` exactly — `torch.allclose` passes. One matmul, tied weights, no residue. If you expected an extra bias term, there isn't one.

Then test the magnitude claim. Multiply that last hidden state by 2 before the matmul and softmax both versions. The argmax is unchanged and the top token's probability has climbed sharply — the same opinion, stated twice as loudly.

## Depends on / leads to

Depends on [the residual stream](/wiki/ai/llm/residual-stream) and [embeddings](/wiki/ai/llm/embeddings). Leads to [softmax and temperature](/wiki/ai/llm/softmax-and-temperature).
