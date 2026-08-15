---
title: "Multi-Layer Perceptron"
weight: 170
---

A multi-layer perceptron is the plainest arrangement in the [neural network](/wiki/ai/llm/neural-networks) repertoire, and the oldest: multiply a list of numbers by a table of learned weights, [bend the result](/wiki/ai/llm/bend), multiply by a second table. Every [block](/wiki/ai/llm/glossary) of a [transformer](/wiki/ai/llm) contains one — an **MLP**, as everyone shortens it. It is the half of the block that thinks about a single word at a time, without reference to any other. [Attention](/wiki/ai/llm/attention) is the other half, the part that moves information between words; the MLP is what the model does with a word once attention has gathered whatever it needed.

It is much the plainer of the two mechanisms and much the larger. Most of the model's weights sit in its MLPs, and so, as far as anyone has been able to determine, do most of its facts. The half of a transformer people find interesting is attention. The half that holds what the model knows is this one.

## What's left to do once attention has run

Attention has just delivered a blend of whatever the earlier words were offering. That sounds like the hard part is over, and it leaves one thing undone.

Everything attention produces is a **weighted average of things already present**. Given the [attention pattern](/wiki/ai/llm/glossary), its output is a straight sum of [value vectors](/wiki/ai/llm/qkv-projections) — so whatever it hands back was assembled out of material already lying around at other positions. Attention decides *what to gather* in a thoroughly conditional way, since the pattern is computed from the row through a [softmax](/wiki/ai/llm/softmax-and-temperature). What it cannot do is produce something that wasn't in the context to begin with.

And gathering isn't enough. Suppose attention has successfully established that this occurrence of `" bank"` sits in a sentence full of rivers. Something now has to act on that: suppress the finance associations, promote the ones about water and edges, and write a conclusion into the row that no earlier position ever supplied. Nothing assembled by averaging over the context can introduce that — it can only recombine what the context already held. The MLP is the part with the freedom to write something new, which is why a block needs both halves and why neither is optional.

## Two matrices and a bend

Mechanically there is almost nothing to it. The row is widened, bent, and squeezed back:

```text
       768  ──▶  3072  ──▶  768
              GELU
```

Multiply by a matrix to go from [`d_model`](/wiki/ai/llm/glossary) — the row width, 768 in [GPT-2 small](/wiki/ai/llm/gpt-2) — to four times that, apply [GELU](/wiki/ai/llm/activations) — the nonlinearity, the *bend*, and the reason the two matrices don't collapse into one — then multiply by a second matrix to come back down. That widening is the **MLP bulge**, the only place in the entire model where a row isn't `d_model` wide. Nothing mixes across rows on the way through: each row goes in alone and comes back alone.

Two matrices is where the *multi* in *multi-layer perceptron* stops. [The general shape](/wiki/ai/llm/neural-networks) allows as many stages as you like, and a transformer never uses more than two, because it buys its depth by stacking blocks rather than by deepening the MLP inside one.

## The useful reading: detect, then write

Two matrices with a bend is accurate and tells you nothing. The reading that does is to look at one of the 3072 **hidden units** on its own — one number in the widened middle, and what the rest of the world is pointing at when it says a *neuron*.

Its **input weights** define a direction in the row's space. The unit lights up when the row points that way, and GELU squashes everything else toward zero — so it behaves like a detector with a soft threshold rather than a proportional readout. Its **output weights** define a *different* direction entirely, which it writes into [the residual stream](/wiki/ai/llm/residual-stream), scaled by how hard it fired.

Detect a feature, write a feature. Three thousand of those, per block, all running at once and summing their contributions.

That makes an MLP something like three thousand soft if-then rules: *if this row looks like X, add Y to it.* The rules are fuzzy, they overlap, and many fire a little on almost everything — but "a big pile of learned conditional edits to the row" is much closer to what's happening than "a neural network layer." (The literature calls this a key-value memory. It has nothing to do with attention's keys and values, or with [the KV cache](/wiki/ai/llm/kv-cache).)

## Why it's four times wider in the middle

The bulge isn't arbitrary, and what has survived from the original transformer through to models a thousand times larger is the *budget* it implies: about 8·`d_model`² weights in the MLP, whichever way you arrange them. Two matrices at 4× width comes to exactly that, and so — not by coincidence — does the three-matrix, `8/3 · d_model`-wide arrangement that [SwiGLU](/wiki/ai/llm/activations) models use instead. The multiplier moved; the budget didn't.

The reason to widen at all is that the number of hidden units is the number of detectors, and a block wants far more detectors than the row has dimensions to spare. A 768-wide row can hold at most 768 mutually perpendicular directions; the MLP builds 3072 detectors over it. They cannot all be perpendicular, so they interfere — which is tolerable only because on any given token almost none of them fire, and that trade is [superposition](/wiki/ai/llm/superposition), the subject of its own page.

The reason not to widen further is cost: the two matrices are the model's largest, and their size scales directly with the multiplier.

## Where the parameters live

And that is where the weights are. Attention in a GPT-2 block is four 768×768 matrices, about 2.4M weights. The MLP is two 768×3072 matrices, about 4.7M. Two-thirds of every block — and, on the current evidence, most of what the model knows — sits in the bulge.

This tends to surprise people who have spent all their attention on attention. It also explains why [mixture of experts](/wiki/ai/llm/mixture-of-experts) targets the MLP and leaves attention untouched: if you want to add parameters without adding cost per token, you go where the parameters already are.

## Check yourself

[Sum the parameters](/wiki/ai/llm/running-the-checks) in GPT-2 small whose names contain `mlp`, and compare against the total excluding `wte` and `wpe`. You'll get 56.7M of 85.1M non-embedding parameters — 66.6%, two-thirds to the decimal — against 28.3M in attention.

## Depends on / leads to

Depends on [neural networks](/wiki/ai/llm/neural-networks) and [the residual stream](/wiki/ai/llm/residual-stream). Leads to [the bend](/wiki/ai/llm/bend) — the nonlinearity in the middle, and the reason the bulge isn't refunded — then [GELU and SwiGLU](/wiki/ai/llm/activations), [LayerNorm and RMSNorm](/wiki/ai/llm/normalization) and [mixture of experts](/wiki/ai/llm/mixture-of-experts).
