---
title: "The Bend"
weight: 30
---

A bend is the smallest moving part in a [neural network](/wiki/ai/neural-network): a fixed scrap of arithmetic applied to each number on its own, wedged between the large multiplications that do the visible work. It learns nothing, holds no weights of its own, and is the same in every model that uses it. Take the bends out and a network of any size — however many layers you paid for — is exactly equal to a single multiplication, and a single multiplication cannot express a rule that says *it depends*. Everything conditional a model does traces back to a bend.

These pages say **bend** where most of the literature says *activation function* or *nonlinearity*. The word names what the operation is for — bending an otherwise straight pipeline — and keeps that separate from which function does the bending. [GELU, SwiGLU, or something else](/wiki/ai/neural-network/activations) is a much smaller question than whether a bend is there at all.

## What a bend is

Two things happen in a network [layer](/wiki/ai/neural-network/glossary), and they have opposite characters.

The multiply mixes. Every number coming out is a weighted sum of every number going in, using [weights](/wiki/ai/neural-network/glossary) that training chose. It is where the model's knowledge lives and where nearly all of its arithmetic goes.

The bend does not mix. It is a single-input, single-output function — a rule for turning one number into one number — applied to every number separately and identically. A widened vector of 3072 numbers goes through the bend as 3072 unrelated one-number decisions. Nothing is compared, nothing is combined, and no number learns anything about its neighbours.

```text
                        depth  →

   [ · · · · ]  ──[ W ]──▶  [ · · · · · · ]  ──bend──▶  [ · · · · · · ]
     input                   every number                each number
                             is a sum of all             bent alone
```

That second property is why a bend has no weights. There is nothing in it to learn: the two you will meet — ReLU's `max(0, x)`, which replaces every negative number with zero, and GELU's `x · Φ(x)`, which does something gentler along the same lines — are decided by whoever wrote the model and are identical in a freshly initialised network and a fully trained one. The bend is part of the *shape* the training fills in, not part of the filling.

## Why straight lines are not enough

The case for the bend is not that it helps. It is that without one, the surrounding parameters are refunded in full.

Multiplying by a matrix `A` and then by a matrix `B` is the same as multiplying by a single matrix `C = A·B`. That is not an approximation or a numerical near-miss; it is what matrix multiplication *is*. `C` can be computed once and both originals discarded, and no input will ever tell the difference.

Apply that to [the MLP](/wiki/ai/neural-network/multi-layer-perceptron), which is exactly two matrices with a gap between them:

```text
   with a bend       768 ──[ W_up ]──▶ 3072 ──bend──▶ 3072 ──[ W_down ]──▶ 768

   without           768 ──[ W_up ]──▶ 3072 ─────────────────[ W_down ]──▶ 768
                     768 ──────────────[ C ]──────────────────────────────▶ 768
```

Those bottom two are the same function. An MLP with no bend carries about 4.7M weights and computes something a single 768 × 768 matrix — 590K weights — reproduces exactly. The bulge — the widening that [holds most of a network's weights](/wiki/ai/neural-network/multi-layer-perceptron#why-the-middle-is-wider) — buys precisely nothing.

The collapse doesn't stop at one stage, either. Chain twelve bend-free MLPs directly together — a plain stack, with nothing at all between them — and each adjacent pair folds, then each pair of pairs, until twelve stages are one matrix. Depth becomes free and worthless at the same time. (A real transformer has other machinery in those gaps, which changes the picture; that complication is taken up below.)

(Matrices in most networks each carry a bias vector, which makes every step *affine* rather than strictly linear. It changes nothing: chain affine maps and you get a matrix plus a constant vector, which folds exactly as completely.)

## Folding the paper

Take a sheet of paper, fold it a few times, and make one straight cut through the folded stack. Unfold it. The cut was straight — scissors have no other option — but the shape in the paper has many corners, and with enough folds it can be made remarkably intricate.

A matrix can only cut straight. The bend is the fold. Each bend creases the space the input lives in, and the next matrix draws its straight cut through the creased version; unfolded, that cut is a boundary with corners in it. Stack a dozen layers and the paper has been folded a dozen times before the last cut, so a model's behaviour can turn sharply on distinctions no single weighted sum could draw.

This has a formal version. A network with even one bend and enough units can approximate any continuous function to any accuracy you like — the universal approximation theorem, proved in the late 1980s. It is reassuring and almost useless in practice: it says nothing about how many units, and the answer is often absurd. What made the result matter is the empirical discovery that stacking *more folds* is drastically more efficient than making one stage wider; [a transformer](/wiki/ai/llm) accordingly buys its depth by repeating blocks rather than by inflating the bulge inside one.

## Where "it depends" comes from

Without a bend, every output number is a fixed weighted sum of the inputs. The recipe never changes. Double an input and its contribution doubles, every time, regardless of context — there is no arrangement of weights that makes a unit pay attention to one feature only when some other feature is present, because that is not a thing a weighted sum can do.

The bend breaks that, and it is the only thing in the [MLP](/wiki/ai/neural-network/multi-layer-perceptron) that does. Because GELU crushes negatives toward zero and passes large positives nearly untouched, a hidden unit is effectively *off* for most inputs and *on* for a few. Its output weights then contribute to the layer's output only when it fired. Detect, then write — and the "then" is the bend. Strip it out and every unit writes its contribution to every input in proportion, all the time, which is a lookup table with the lookup removed.

This is what the MLP page means by three thousand soft if-then rules, and what makes a hidden unit a *detector* rather than a readout. It is also why [superposition](/wiki/ai/neural-network/superposition) is survivable: interference between overlapping detectors is tolerable only because the bend keeps almost all of them near zero on any given input.

## Nonlinearities that aren't bends

A bend is nonlinear, but not everything nonlinear is a bend, and the distinction matters because only a bend leaves each number's fate independent of its neighbours'. Take [the transformer](/wiki/ai/llm) as the worked example: "where is this model's nonlinearity" has four answers there, and the activation function is only the first of them. Only that one is a bend in the sense defined above:

| Where | The nonlinearity | Elementwise? | Count in [GPT-2 small](/wiki/ai/llm/gpt-2) |
|---|---|---|---|
| [MLP](/wiki/ai/neural-network/multi-layer-perceptron) | [GELU](/wiki/ai/neural-network/activations) on the widened row | yes — a bend | 12 — one per block |
| [Attention](/wiki/ai/llm/one-attention-head) | [softmax](/wiki/ai/llm/one-attention-head#step-4-mask-then-softmax) over the scores | no — divides by a sum across the row | 12 — one per block |
| [Norms](/wiki/ai/neural-network/normalization) | dividing by a spread computed from the row | no — the divisor comes from all of it | 25 — two per block, plus a final one |
| [Attention scores](/wiki/ai/llm/qkv-projections) | a query multiplied by a key | no — two numbers in, one out | 12 — one per block |

A bend is nonlinear *and* elementwise. The other three are nonlinear precisely because they are not — a softmax weight depends on every score in the row, a norm's divisor on every number in it. They stop the collapse too. They just aren't bends, and these pages reserve the word.

The last row has no activation function in it anywhere. The Q, K and V projections are each strictly affine, and yet the score is a query dotted with a key — two quantities both computed from the input, multiplied together. A product of two things that each vary with the input is not linear in that input, so attention would be nonlinear with its softmax deleted.

The inventory carries one honest correction to the collapse argument above. Because those other three exist, a real transformer stripped of its GELUs would *not* fold down to a single matrix: attention would survive, and the norms sitting between every MLP and the next would stop even the MLPs folding into each other. But each MLP still collapses internally, from 4.7M parameters to 590K, and the MLPs are two-thirds of every block's parameters.

## What makes a bend usable

Any nonlinear function stops the collapse, so the choice is not constrained by the argument above. It is constrained by everything else:

- **It must be cheap.** The bend runs on every number in the bulge — in GPT-2 small, 3072 per row per block, so 36,864 separate invocations for every single token that passes through. Anything expensive is disqualified before it is considered.
- **It must leave backprop a usable slope.** [Backprop](/wiki/ai/neural-network/backprop-one-weight) moves a weight by asking which way to nudge it, and a stretch where the function is exactly flat answers "nudging changes nothing." A bend with a genuinely flat region can therefore strand a unit in it. Whether that is a real problem or a theoretical one is the first question the next page takes up.
- **It must not squash.** A bend that crushes everything into a narrow range shrinks the gradient at every stage, and twelve such shrinkages in a row leave almost nothing to train on. This is why the S-shaped functions of the 1990s lost to functions that pass large positive values through roughly unchanged.
- **It should broadly preserve order.** A bend that scrambled the ranking of its inputs would break the detector reading above, where a unit fires *harder* the better the match.

Those four constraints are what the history of activation functions is a search over, and [GELU and SwiGLU](/wiki/ai/neural-network/activations) is where that search currently stands.

## Check yourself

**Watch the fold happen.** The collapse argument is six lines of `torch` and needs no model downloaded at all — multiply two random matrices of the MLP's shape, precompute their product, and confirm the two give identical answers. [The activations page runs it](/wiki/ai/neural-network/activations#check-yourself), including the reason you must do it in `float64` to see it cleanly.

**Count the bends, and confirm they are free.** The claim that a bend holds no weights is one line to check:

```python
from transformers import GPT2LMHeadModel

model = GPT2LMHeadModel.from_pretrained("gpt2")
acts  = [m for n, m in model.named_modules() if n.endswith("mlp.act")]

len(acts)                                              # 12 — one per block
sum(p.numel() for a in acts for p in a.parameters())   # 0 — not one weight
```

Twelve modules, zero parameters between them, and removing them from the parameter count changes nothing because they were never in it. The most load-bearing part of the MLP is the part that costs nothing to store.

**Now take them out.** [Score a sentence](/wiki/ai/llm/running-the-checks) with `labels=ids` to get a baseline — a few points of loss on ordinary English — then replace every bend with a function that does nothing at all and score the same sentence again:

```python
import torch.nn as nn

for block in model.transformer.h:
    block.mlp.act = nn.Identity()
```

Nothing else changed. Every weight is the trained one, all 124M of them still present and still being multiplied in exactly the same order. The claim to break: the loss climbs past the **just-under-11** that [an untrained GPT-2 with random weights](/wiki/ai/neural-network) scores. Not merely "worse" — *worse than never having been trained*, because the ablated model is not ignorant but confidently miscalibrated, and the [loss](/wiki/ai/neural-network/the-loss-function) punishes confident wrongness harder than it punishes having no opinion. Generate from it and you get noise.

What was deleted to achieve that is a function with no parameters, which in the 12 MLPs of a trained GPT-2 was doing nothing more than turning negative numbers down.

## Depends on / leads to

Depends on [the MLP](/wiki/ai/neural-network/multi-layer-perceptron), the two matrices it sits between. Leads to [GELU and SwiGLU](/wiki/ai/neural-network/activations) — which bend, and why the field changed its mind.