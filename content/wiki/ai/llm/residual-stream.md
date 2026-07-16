---
title: "The Residual Stream"
weight: 120
---

Nothing in a transformer ever replaces a token's vector. Each part of the model reads it, works something out, and adds the result on top of what's already there. What comes out the far end is the starting vector plus every contribution made along the way — a running total. That total is the residual stream, and it is the only thing travelling through the model at all.

## Why a sum, and not a pipeline

Picture the obvious design first, because almost everyone does. Each stage takes the previous stage's output, transforms it, and hands on a replacement — a relay race, one baton, passed along. That's how a plain deep network works.

The trouble isn't that such a design *can't* preserve what it doesn't use. It can: a stage that passes its input through untouched is a perfectly good stage, and a deep plain network can always, in principle, match a shallower one by having the surplus stages do exactly that. Nothing needs to be lost.

The trouble is that it has to **learn** not to lose it. Preservation is a behaviour the stage must acquire, from the same gradient descent that's busy teaching it everything else — and it turns out to be a behaviour gradient descent is surprisingly bad at finding. Historically, deep plain networks did *worse* than shallow ones, and not because the shallow solution was beyond their reach. It was sitting right there, representable, and the optimizer couldn't land on it.

Adding instead of replacing changes what the default is. Write your contribution on top of the total and leave everything else alone, and a stage that outputs nothing at all is *already* the identity — no learning required. Preservation stops being an achievement and becomes what happens when a block does nothing at all. (The `+` doing that work has its own name and page: [skip connections](/wiki/ai/llm/skip-connections), which also covers what it does for gradients on the way back.)

## The whole of a block

Given that, a [block](/wiki/ai/llm/glossary) is smaller than you'd think. It does this, and nothing else:

```text
row = row + attention(norm(row))
row = row + mlp(norm(row))
```

Read it twice, because the shape of it is the point. [Attention](/wiki/ai/llm/attention) and [the MLP](/wiki/ai/llm/the-mlp) never see the stream directly — they read a [normalized](/wiki/ai/llm/normalization) *copy* of it, and their output is added back. The stream itself is never overwritten by anyone.

So the row leaving the last block of GPT-2 small is the [embedding](/wiki/ai/llm/embeddings) plus 24 contributions: 12 from attention, 12 from the MLP, each of them [`d_model`](/wiki/ai/llm/glossary) wide. (The MLP widens a row internally on its way through, but writes back at the same width it read.) That running sum is the residual stream.

## It's a bus, not a pipeline

The consequence is worth stating on its own. Blocks do not hand each other outputs. They all read from, and write to, one shared line.

Block 9's attention can pick up something block 2 wrote and block 5 never touched — it's still sitting in the sum, untouched, because nothing along the way had the power to remove it. Nothing is relayed hop by hop. A block is a device that reads the bus and adds to it, and the model is 12 of those in a row.

## You can read it almost linearly

Because the final row is a *sum*, you can ask what any one block contributed to any one prediction and get an actual number back. [Logits](/wiki/ai/llm/unembedding-and-logits) are a linear readout of the final row, and a linear readout of a sum is the sum of the readouts of its parts. That turns a chunk of attribution into arithmetic — which is why so much interpretability work starts here.

Two caveats, both worth carrying.

**The word *direct* is load-bearing.** **Direct logit attribution** splits one logit into one number per block, and those numbers are exact — for the direct path. But a block's write also changes what every later block *computes*: block 2 reshapes block 9's attention pattern, and none of that downstream influence appears in block 2's number. A block can matter enormously and still score near zero. What the arithmetic gives you is a component's direct contribution, not its total causal effect.

**And the readout is only *nearly* linear.** The final norm rescales the row by a factor that depends on the row itself, which is not a linear operation. Direct logit attribution copes by freezing that factor at its cached value and accepting the small lie. (The **logit lens** — reading logits off a half-finished row as though it were already final — freezes nothing; it recomputes the norm each time. Its lie is a different one: intermediate rows aren't distributed like final rows, so the unembedding was never trained to read them.)

## The bandwidth never grows

Here's the pressure that shapes everything else. `d_model` is the same at the right edge as at the left: the stream does not get wider to accommodate 24 writers. All of them compete for the same 768 directions, and everything the model knows has to fit.

It doesn't fit — not the way you'd hope. Models track far more features than they have dimensions, and the trick that lets them is [superposition](/wiki/ai/llm/superposition).

## Check yourself

Two ablations — deliberately zeroing part of a running model to see what breaks — on GPT-2 small.

First, remove one contributor. Zero block 6's attention output with a forward hook on `model.transformer.h[6].attn.c_proj` returning zeros. (Hook `c_proj` rather than `.attn` itself: `.attn` hands back a tuple, not a plain tensor, and won't take the substitution.) Measure [perplexity](/wiki/ai/llm/glossary) on a few hundred tokens of WikiText — a standard Wikipedia-derived benchmark corpus, though any ordinary prose does — and it rises about 15–20%. The text stays fluent. You deleted one of the model's 24 contributions and it shrugged: the stream carried everything else straight around the hole.

Now sever the bus. Zero the *whole stream* entering block 6, and perplexity blows up by several orders of magnitude while the output collapses into repetition. That is a far bigger deletion, deliberately so — the embedding and everything the first six blocks wrote goes with it, thirteen of the twenty-four contributions rather than one.

The pairing is the point. The first ablation is what losing a contributor costs on a bus: fifteen percent. The second is the failure a *relay* design risks every time a stage declines to pass something on — block 7 receiving nothing of what came before — and it's fatal. The architecture is the whole difference between those two numbers, and it's why the second can't happen by accident: no block has the power to zero the stream, because no block can do anything but add to it.

## Depends on / leads to

Depends on [embeddings](/wiki/ai/llm/embeddings). Leads to [attention](/wiki/ai/llm/attention) and [the MLP](/wiki/ai/llm/the-mlp).
