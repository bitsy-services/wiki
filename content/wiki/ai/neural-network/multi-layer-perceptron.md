---
title: "Multi-Layer Perceptron"
weight: 20
---

A multi-layer perceptron is the plainest network there is, and the oldest: multiply a list of numbers by a table of learned weights, [bend the result](/wiki/ai/neural-network/bend), multiply by a second table, and keep going for as many [layers](/wiki/ai/neural-network/glossary) as you chose. Everyone shortens it to **MLP**. It has no structure beyond that — no notion that its inputs might be pixels near each other or words in an order, no memory, no wiring that treats any input differently from any other.

That plainness is why it is worth a page. Almost every architecture in use is an MLP with something bolted on to exploit whatever structure its inputs happen to have, and once you take the bolted-on part away, what remains is this — usually holding most of the weights and, as far as anyone has been able to determine, most of what the network knows.

## Every input to every output

One layer connects everything to everything. If a layer takes 768 numbers and produces 3072, then each of those 3072 outputs is a weighted sum of all 768 inputs, and the layer holds 768 × 3072 weights to say how much each input contributes to each output.

That is the sense in which the layer is *fully connected*, and it is worth noticing what it implies: the layer has no idea which input was which. Shuffle the 768 inputs, shuffle every layer's weights the same way, and the network computes exactly the same function. An MLP has no built-in opinion about the shape of its input at all — which is a weakness when the input has real structure worth exploiting, and the reason other architectures exist.

## Two matrices and a bend

The smallest interesting MLP is two layers, and the shape is usually a bulge — widen, bend, come back down:

```text
       768  ──▶  3072  ──▶  768
              GELU
```

Multiply by a matrix to go from the input width to some larger width, apply a bend — [GELU](/wiki/ai/neural-network/activations) here, though [which bend barely matters](/wiki/ai/neural-network/bend) next to whether one is there — then multiply by a second matrix to come back down.

The bend in the middle is the whole reason there are two layers rather than one. Without it, multiplying by one matrix and then another is the same as multiplying by a single matrix you could have computed in advance, and the second layer is refunded. [That arithmetic in full](/wiki/ai/neural-network/bend#why-straight-lines-are-not-enough) is a page of its own; the short version is that stacking straight lines gets you a straight line, however many you stack.

Nothing about that stops at two. The *multi* in the name allows as many layers as you like, and plenty of networks are deeper. Architectures built out of repeating blocks tend not to be, because they buy their depth by stacking blocks rather than by deepening the MLP inside one.

## The useful reading: detect, then write

Two matrices with a bend is accurate and tells you nothing. The reading that does is to look at one of the 3072 **hidden units** on its own — one number in the widened middle.

Its **input weights** define a direction in the input's space. The unit lights up when the input points that way, and the bend squashes everything else toward zero — so it behaves like a detector with a soft threshold rather than a proportional readout. Its **output weights** define a *different* direction entirely, which it writes into the layer's output, scaled by how hard it fired.

Detect a [feature](/wiki/ai/neural-network/glossary), write a feature. Three thousand of those, all running at once and summing their contributions.

That makes an MLP something like three thousand soft if-then rules: *if the input looks like X, add Y to it.* The rules are fuzzy, they overlap, and many fire a little on almost everything — but "a big pile of learned conditional edits" is much closer to what's happening than "two matrix multiplications." (The literature calls this a key-value memory, a name that collides confusingly with several unrelated uses of "key" and "value" in other architectures.)

## Why the middle is wider

The reason to widen is that the number of hidden units is the number of detectors, and a network generally wants far more detectors than its input has dimensions to spare. A 768-wide input can hold at most 768 mutually perpendicular directions; the MLP above builds 3072 detectors over it. They cannot all be perpendicular, so they interfere — which is tolerable only because on any given input almost none of them fire, and that trade is [superposition](/wiki/ai/neural-network/superposition), the subject of its own page.

The reason not to widen further is cost. Those two matrices are the network's largest objects, and their size scales directly with the multiplier — so the width of the middle is very nearly the whole parameter budget.

A 4× bulge is the convention transformers inherited, and what has actually survived from the original design through to models a thousand times larger is the *budget* rather than the multiplier: about 8·*width*² weights, whichever way you arrange them. Two matrices at 4× comes to exactly that, and so — not by coincidence — does the three-matrix, 8/3× arrangement that [SwiGLU](/wiki/ai/neural-network/activations) networks use instead.

## This is where the weights are

The practical consequence is that if you want to know where a network's parameters went, look at its MLPs first. They are dense, they are wide in the middle, and everything else in a typical architecture is smaller.

That is also why techniques for adding capacity without adding cost — [mixture of experts](/wiki/ai/llm/mixture-of-experts) being the prominent one — target the MLP and leave the rest alone. If you want more parameters per unit of compute, you go where the parameters already are.

## Check yourself

[GPT-2 small](/wiki/ai/llm/gpt-2) is a convenient thing to count, because it is a stack of twelve blocks each containing one 768→3072→768 MLP alongside its other machinery.

[Sum the parameters](/wiki/ai/llm/running-the-checks) whose names contain `mlp`, and compare against the total excluding `wte` and `wpe`. You'll get 56.7M of 85.1M non-embedding parameters — 66.6%, two-thirds to the decimal — against 28.3M in everything else. Two matrices per block, and they outweigh the architecture's distinguishing machinery two to one.

## Depends on / leads to

Depends on [the section overview](/wiki/ai/neural-network) and [the glossary](/wiki/ai/neural-network/glossary). Leads to [the bend](/wiki/ai/neural-network/bend) — the nonlinearity in the middle, and the reason the bulge isn't refunded — and then [GELU and SwiGLU](/wiki/ai/neural-network/activations). For what an MLP does inside a transformer specifically, see [the MLP in a block](/wiki/ai/llm/the-mlp).
