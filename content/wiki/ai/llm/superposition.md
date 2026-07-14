---
title: "Superposition"
weight: 310
---

A feature is a direction. "This text is French," "this token is a proper noun," "we're inside a quotation" — each is, to a good approximation, a direction in the [residual stream](/wiki/ai/llm/residual-stream), and how far a row points that way is how present the feature is.

Which raises an arithmetic problem. `d_model` is 768. Models plainly track far more than 768 things. Where do the rest live?

Packed in as **almost**-orthogonal directions. You can only fit 768 mutually perpendicular vectors in 768 dimensions — but you can fit exponentially many that are *nearly* perpendicular: a couple of degrees off for a typical pair, a dozen for the worst of them. Features stored that way interfere slightly, and the model tolerates it because features are **sparse**: hardly any are active on a given row, so the collisions mostly don't happen at once. Superposition: more features than dimensions, paid for in noise.

It explains the thing that most frustrates people poking at models. A single neuron, or a single dimension of the stream, is **polysemantic**: not "the Golden Gate neuron" but a coordinate that a hundred unrelated features happen to share. Which is why interpretability moved to sparse autoencoders — train an overcomplete basis (32k directions, say) and pull the superposed features back apart.

Fixed width is the cause. The stream doesn't widen rightward, so everything the model knows competes for the same 768 directions.

## Check yourself

Sample 10,000 random unit vectors in 768 dimensions and take the largest pairwise cosine. It lands around 0.2 — ten thousand "features," none meaningfully aligned with another. Repeat in 8 dimensions and near-orthogonality collapses immediately. That gap is the capacity superposition is exploiting.

## Depends on / leads to

Depends on [the residual stream](/wiki/ai/llm/residual-stream) and [the MLP](/wiki/ai/llm/the-mlp). Leads to [fine-tuning](/wiki/ai/llm/fine-tuning).
