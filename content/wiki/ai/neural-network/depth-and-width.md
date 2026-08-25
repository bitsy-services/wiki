---
title: "Depth and Width"
weight: 95
---

Two numbers get chosen before a network is trained and cannot be changed afterwards: how many layers it stacks, and how wide each one is. Everything else in this section is machinery for making the fitting work; these two decide the size and the shape of the thing being fitted. They are usually discussed as one quantity, because together they set the parameter count and the parameter count is what the bill is written against. They are not one quantity. Depth buys the ability to build on conclusions the network has already reached; width buys the room to reach several of them at once. And they are paid for in different currencies — width costs money, and depth costs time that no amount of money buys back.

## One budget, two prices

A [layer](/wiki/ai/neural-network/glossary)'s table of weights has one entry for every input-and-output pair, so a layer that takes *w* numbers and produces *w* numbers holds *w*² of them. Stack *d* of those and the network holds roughly

```text
   weights  ≈  d × w²
```

Read that as a price list. Doubling the depth doubles the weights. Doubling the width *quadruples* them. Per unit of the thing you are buying, depth is the cheap knob and width is the expensive one — which is the reverse of how the two are usually talked about, because the cheap knob is the one with the hard limits attached.

The exact constant depends on what else each layer contains. For the arrangement [GPT-2](/wiki/ai/llm/gpt-2) uses, each block works out to almost exactly 12·*w*² weights, so the whole stack is 12·*d*·*w*² — 12 × 12 × 768² = 84.9M for the small model, which is its published non-embedding count to within a rounding error.

One part of the budget breaks the rule, and it matters at small scale. The tables that convert to and from the [vocabulary](/wiki/ai/llm/glossary) are *vocabulary × width*, growing with width alone and not its square. In GPT-2 small those tables are 39M weights against the stack's 85M. Width is therefore expensive twice over — quadratically inside the stack, linearly outside it — and a model that is narrow enough spends most of its budget on the doorways rather than the building.

## What depth buys: composition

A layer can only see what the layer before it produced. That is the entire source of depth's value, and it arrives as a constraint: whatever a network does in one forward pass, it does in exactly *d* steps, and there is no loop to go around again. Depth is the number of times the network is allowed to work on its own output.

[The MLP](/wiki/ai/neural-network/multi-layer-perceptron#the-useful-reading-detect-then-write) gives the concrete version. One layer's units detect [features](/wiki/ai/neural-network/glossary) of the input and write features back out. The next layer's units detect features of *those* — combinations, contradictions, refinements of what the first layer concluded. Adding width gives you more detectors looking at the same thing. Only depth gives you detectors that can be about what the earlier detectors found.

[The paper-folding picture](/wiki/ai/neural-network/bend#folding-the-paper) says the same thing geometrically: each [bend](/wiki/ai/neural-network/bend) is a fold, and folds compose. A bigger sheet does not.

This has a formal edge to it. Width can substitute for depth *in principle* — one bent layer with enough units approximates anything, which is the universal approximation result — but the known separation theorems put the exchange rate at exponential: there are functions a three-layer network represents with a modest number of units that a two-layer network cannot represent with fewer than exponentially many. An exchange rate of that shape is a theoretical possibility and a practical impossibility, and it is why nobody builds the wide shallow version even though the theorem says they could.

## What width buys: room

Width is how many numbers are in play at one stage — the working set the network gets to carry from each step to the next. Nothing in a layer queues: every unit computes at once and they all contribute to the same output. So width is the network's capacity to have many things be true simultaneously.

[Superposition](/wiki/ai/neural-network/superposition) is why width buys more than its face value — a 768-wide stage tracks far more than 768 features by overlapping them in directions that are merely *almost* perpendicular. But that trick is bought entirely with dimension, and it fails ungracefully. Ten thousand random directions in 768 dimensions are all nearly perpendicular; in 8 dimensions they are on top of each other and there is nowhere to hide a feature. Narrowing a network does not cost capacity in proportion to the narrowing. It costs it faster than that.

## Where the two meet the hardware

Here the symmetry breaks, and it is the break that decides real designs.

**Width is parallel. Depth is serial.** Layer *k*+1 cannot start until layer *k* has finished, and [no quantity of hardware shortens a chain](/wiki/ai/llm/why-scale-worked#recurrence-turns-a-document-into-a-queue) — the same argument that killed recurrent models applies inside a single network's stack. Everything inside one layer, by contrast, happens at once.

```text
                depth  →

   3 × 1536    ███  ███  ███                     3 steps, strictly in order
               ███  ███  ███
               ███  ███  ███

  12 ×  768    ██ ██ ██ ██ ██ ██ ⋯              12 steps, strictly in order
               ██ ██ ██ ██ ██ ██ ⋯

  27 ×  512    █ █ █ █ █ █ █ █ █ ⋯              27 steps, strictly in order
```

Those three hold the same number of weights. Counting the cells says otherwise — the drawing makes the deep one look biggest — because width is squared in the budget and a picture only gets to show it once.

Four consequences follow from the serial/parallel split:

**Wall-clock time.** Doubling the width of a network running on hardware that wasn't saturated can cost almost nothing, because the extra arithmetic fits in units that were idle. Doubling the depth always costs another round trip, on any hardware, forever.

**Efficiency per weight.** Big matrix multiplies have high [arithmetic intensity](/wiki/ai/llm/training-vs-inference-parallelism#why-decode-is-slow-at-something-other-than-arithmetic) — a lot of arithmetic per byte dragged out of memory — so they run near the machine's peak. A thin deep stack does the same total arithmetic as many small multiplies instead of a few large ones, each with its own fixed overhead and each waiting on the one before. Identical arithmetic, worse wall-clock.

**Splitting across machines.** Width shards cleanly: give each device a slice of every layer, have them exchange results once per layer, and every device is busy the whole time. Depth shards badly: give each device a run of consecutive layers and device 2 sits idle while device 1 works — the *pipeline bubble*. It can be mostly filled by pushing several batches through at staggered offsets, but never quite paid off, and the leftover is proportional to how many ways you split.

**Latency at inference.** Depth sits in the critical path of every single output. Width is work that a well-fed machine absorbs. This is why models shaped for cheap serving skew wider and shallower than the shape that would have trained best, and it is a real and deliberate loss of quality traded for response time. (In a transformer, [the KV cache](/wiki/ai/llm/kv-cache) grows with depth and width alike, so that particular cost gives neither knob an advantage.)

Training memory is the one place they tie. The [activations](/wiki/ai/neural-network/glossary) kept around for [the backward sweep](/wiki/ai/neural-network/backprop-one-weight) scale with depth × width — linear in both, no preference either way.

## Depth used to be limited by something else entirely

For most of the field's history, depth was capped not by cost or by usefulness but by *trainability*. Past a couple of dozen layers, deeper networks came out worse — [worse on the training set](/wiki/ai/neural-network/skip-connections#why-deep-stacks-refused-to-train), which is the one thing extra capacity is supposed to guarantee against. The 56-layer model losing to the 20-layer model was an optimization failure, not a capacity failure.

[Skip connections](/wiki/ai/neural-network/skip-connections) and [normalization](/wiki/ai/neural-network/normalization) moved that ceiling from around twenty layers to several hundred, and moved it far enough that it stopped being the binding constraint. The older account is still widely taught, and it no longer describes anything: in a modern normalized stack with skips, a hundred layers trains perfectly stably. Depth is now limited by latency and by diminishing returns — not by whether the thing converges.

## Why the split barely matters, until it does

The measurements that produced the [scaling laws](/wiki/ai/llm/why-scale-worked#what-that-bought) also settled this question. Hold the parameter count fixed and vary the split between depth and width, and the loss moves by a couple of percent across a wide range of shapes — while changing the parameter count by the same factor moves it a great deal more. Shape is a second-order term. The budget is the first-order one.

The practical reading is: don't agonize. Pick a conventional shape and spend your attention on how many parameters and how much data you can afford, which is where the loss actually lives.

The band is wide, though, not infinite, and both edges are real.

**Too shallow and too wide** and you are paying the exponential exchange rate for composition you cannot do any other way, while the vocabulary tables — linear in width — start eating the budget.

**Too deep and too thin** and three things go wrong at once: hardware efficiency falls, superposition's room runs out faster than the narrowing suggests, and the marginal layer starts contributing very little. The last of those has direct evidence behind it. On large trained models, a contiguous run of the *later* layers can be deleted with startlingly little damage — far less than deleting the same fraction of weights from anywhere else, and far less than deleting layers near the input. Nothing comparable is true of width; there is no slice of a layer you can drop for free. A deep network's effective depth is shorter than its nominal depth, and the last layers you paid for are the ones doing the least.

## What the field actually picks

The convention is stated as an **aspect ratio**: width divided by depth. Both the [GPT-2 family](/wiki/ai/llm/gpt-2) and its successors are public, so the trend is readable directly.

| Model | Depth | Width | Aspect ratio |
|---|---|---|---|
| GPT-2 small | 12 | 768 | 64 |
| GPT-2 medium | 24 | 1024 | 43 |
| GPT-2 large | 36 | 1280 | 36 |
| GPT-2 XL | 48 | 1600 | 33 |
| GPT-3 | 96 | 12288 | 128 |
| Llama 3 8B | 32 | 4096 | 128 |
| Llama 3 70B | 80 | 8192 | 102 |
| Llama 3 405B | 126 | 16384 | 130 |

Within the GPT-2 family the ratio *falls*: across four models, depth grew 4× and width only 2×, so scaling up meant getting relatively deeper. Everything after it moved the other way and then stopped moving, settling around 100. That reversal is the hardware argument winning. Depth's serial cost is paid on every forward pass forever, and once models got large enough to be split across many machines, the pipeline bubble made it worse still.

So, in order of how much they matter:

- **Spend the budget first, shape it second.** At fixed compute, moving parameters to data is worth more than any depth/width choice — the [Chinchilla](/wiki/ai/llm/why-scale-worked#what-that-bought) correction, and it dwarfs this page's subject.
- **Pick width in sizes the hardware likes**, then take depth from the aspect ratio. Around 100 for anything large; smaller models are conventionally deeper for their width, which is what the GPT-2 column shows.
- **Skew wider and shallower if latency dominates**, deeper if the task genuinely needs chained steps inside one pass.
- **If what you want is more parameters without more arithmetic**, neither knob does that, and [mixture of experts](/wiki/ai/llm/mixture-of-experts) is the mechanism that does — which is why it targets the widened middle of the MLP, where the parameters already are.

One honest caveat on all of it: the shape-independence measurements were made on transformer language models over a particular range of sizes. It is the best evidence anyone has, and it is not a law of nature.

## Check yourself

The claim to test is the price list: weights go as depth × width², so shapes with wildly different serial depths can hold identical parameter counts — and the deep one is *slower* despite doing the same arithmetic.

Three shapes make it exact. 12 × 768² = 3 × 1536² = 27 × 512² = 7,077,888, so all three stacks hold the same weights, and each width divides evenly into 64-wide [heads](/wiki/ai/llm/glossary). Count them with [the standard setup](/wiki/ai/llm/running-the-checks), excluding the two vocabulary tables, which are the one part that doesn't follow the rule:

```python
from transformers import GPT2LMHeadModel, GPT2Config

def stack_params(n_layer, n_embd, n_head):
    m = GPT2LMHeadModel(GPT2Config(n_layer=n_layer, n_embd=n_embd, n_head=n_head))
    return sum(p.numel() for n, p in m.named_parameters()
               if not n.startswith("transformer.w"))   # drop wte and wpe

stack_params(3, 1536, 24)    # 84,997,632
stack_params(12, 768, 12)    # 85,056,000  — GPT-2 small's actual shape
stack_params(27, 512,  8)    # 85,115,392
```

Serial depths of 3, 12, and 27; parameter counts agreeing to within 0.14%. The leftover is bias vectors and norms, which scale with width rather than width squared.

Now time them, and time the stack alone — not the whole model:

```python
import torch, time
ids = torch.randint(0, 50257, (1, 1024))
with torch.no_grad():
    m.transformer(ids)     # not m(ids)
```

The full model would decide the race on something else: the output table is width × 50,257, so the 1536-wide model does 77M multiply-accumulates there against the 512-wide model's 26M, and you would be measuring the vocabulary rather than the shape.

**The prediction: the 3-layer model is fastest and the 27-layer one slowest, monotonically, despite identical weight-matrix arithmetic.** Two effects push the same way — larger multiplies run closer to the machine's peak, and this architecture's sequence-mixing step costs in proportion to depth × width, which is 4,608, 9,216, and 13,824 for the three. If the 27-layer model comes out fastest, the hardware section above is wrong.

For the other half — that the loss barely cares — the same identity works at a trainable size: 2 × 768² = 8 × 384² = 32 × 192², so those three shapes hold 14.2M weights each. Train them on character-level Shakespeare [in nanoGPT](/wiki/ai/llm/running-the-checks), where the vocabulary is 65 characters and the tables are too small to confound anything. Expect the middle shape to win, the aspect-ratio-384 and aspect-ratio-6 ends to trail it, and the whole spread to be small next to what you get by simply halving any one of them. If the 32-layer model matches the 8-layer one, the band's lower edge is further out than this page claims.

## Depends on / leads to

Depends on [the MLP](/wiki/ai/neural-network/multi-layer-perceptron), where the width² sits; [skip connections](/wiki/ai/neural-network/skip-connections) and [normalization](/wiki/ai/neural-network/normalization), which are what made depth purchasable at all; and [superposition](/wiki/ai/neural-network/superposition), which is what width is spent on. Nothing follows in this section; for these parts assembled into a working architecture, start the [LLM section](/wiki/ai/llm) at [conventions](/wiki/ai/llm/conventions).
