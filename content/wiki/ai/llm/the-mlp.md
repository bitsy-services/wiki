---
title: "The MLP in a Block"
weight: 170
---

Every [block](/wiki/ai/llm/glossary) of a transformer contains one [multi-layer perceptron](/wiki/ai/neural-network/multi-layer-perceptron) — an **MLP**. It is the half of the block that thinks about a single word at a time, without reference to any other. [Attention](/wiki/ai/llm/attention) is the other half, the part that moves information between words; the MLP is what the model does with a word once attention has gathered whatever it needed.

It is much the plainer of the two mechanisms and much the larger. Most of the model's weights sit in its MLPs, and so, as far as anyone has been able to determine, do most of its facts. The half of a transformer people find interesting is attention. The half that holds what the model knows is this one.

## What's left to do once attention has run

Attention has just delivered a blend of whatever the earlier words were offering. That sounds like the hard part is over, and it leaves one thing undone.

Everything attention produces is a **weighted average of things already present**. Given the [attention pattern](/wiki/ai/llm/glossary), its output is a straight sum of [value vectors](/wiki/ai/llm/qkv-projections) — so whatever it hands back was assembled out of material already lying around at other positions. Attention decides *what to gather* in a thoroughly conditional way, since the pattern is computed from the row through a [softmax](/wiki/ai/llm/softmax-and-temperature). What it cannot do is produce something that wasn't in the context to begin with.

And gathering isn't enough. Suppose attention has successfully established that this occurrence of `" bank"` sits in a sentence full of rivers. Something now has to act on that: suppress the finance associations, promote the ones about water and edges, and write a conclusion into the row that no earlier position ever supplied. Nothing assembled by averaging over the context can introduce that — it can only recombine what the context already held. The MLP is the part with the freedom to write something new, which is why a block needs both halves and why neither is optional.

## The bulge, in this model's numbers

Mechanically it is [the plain two-matrix MLP](/wiki/ai/neural-network/multi-layer-perceptron), sized to the row:

```text
       768  ──▶  3072  ──▶  768
              GELU
```

From [`d_model`](/wiki/ai/llm/glossary) — the row width, 768 in [GPT-2 small](/wiki/ai/llm/gpt-2) — to four times that, [GELU](/wiki/ai/neural-network/activations), and back down. That widening is the **MLP bulge**, the only place in the entire model where a row isn't `d_model` wide. Nothing mixes across rows on the way through: each row goes in alone and comes back alone, which is exactly the property attention doesn't have.

Two matrices is where the *multi* stops. The general shape allows as many layers as you like; a transformer never uses more than two, because it buys its depth by stacking blocks rather than by deepening the MLP inside one.

Each of the 3072 hidden units [detects a direction and writes a different one](/wiki/ai/neural-network/multi-layer-perceptron#the-useful-reading-detect-then-write) — and here the direction it writes goes into [the residual stream](/wiki/ai/llm/residual-stream), added on top of whatever is already there rather than replacing it. Three thousand soft if-then rules per block, editing the row in place.

## Where the parameters live

Attention in a GPT-2 block is four 768×768 matrices, about 2.4M weights. The MLP is two 768×3072 matrices, about 4.7M. Two-thirds of every block — and, on the current evidence, most of what the model knows — sits in the bulge.

That is also why [mixture of experts](/wiki/ai/llm/mixture-of-experts) targets the MLP and leaves attention untouched: if you want to add parameters without adding cost per token, you go where the parameters already are.

It is also the pressure behind [superposition](/wiki/ai/neural-network/superposition). Those 3072 detectors are built over a 768-wide row, which has room for at most 768 mutually perpendicular directions — so they overlap, and the model relies on almost none of them firing at once.

## Check yourself

Confirm the split on GPT-2 small, and then confirm the MLP really is position-independent.

[Sum the parameters](/wiki/ai/llm/running-the-checks) whose names contain `mlp` against the total excluding `wte` and `wpe`: 56.7M of 85.1M non-embedding parameters, 66.6%, against 28.3M in attention.

Now take a batch of two different prompts of the same length and run `model.transformer.h[0].mlp` directly on a tensor of rows. Feed it row *k* from one prompt in isolation, then feed it the whole batch and pull out the same row: the two match. Do the same with `model.transformer.h[0].attn` and they don't, because attention's output at position *k* depends on positions 0 through *k*. The MLP has no opinion about what a row's neighbours are doing, or whether it has any.

## Depends on / leads to

Depends on [multi-head attention](/wiki/ai/llm/multi-head-attention) — the block's other half — and on [the multi-layer perceptron](/wiki/ai/neural-network/multi-layer-perceptron), which is what this one is an instance of. Leads to [the unembedding and logits](/wiki/ai/llm/unembedding-and-logits), where the finished row becomes a prediction.
