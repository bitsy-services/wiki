---
title: "GELU and SwiGLU"
weight: 175
---

Almost everything a transformer does to a row is, arithmetically, a straight line: multiply by a matrix, add a vector, multiply by another matrix. Straight lines have an inconvenient property — chain as many as you like and the result is just another straight line. A model built only from them would be no more capable with a hundred blocks than with one, however many parameters you poured in. The activation function is the small bend in the middle of the MLP that breaks the straightness, and it is the reason depth buys anything at all. GPT-2 bends with GELU; nearly everything since bends with SwiGLU.

## Why a bend is necessary

[The MLP](/wiki/ai/llm/multi-layer-perceptron) is two matrices with something in between: widen the row from 768 to 3072, do the something, narrow it back. Take the something away and watch what happens.

Multiplying by matrix `A` and then by matrix `B` is the same as multiplying by a single matrix `C = A·B`. That isn't an approximation or a trick; it's what matrix multiplication *is*, and you can precompute `C` once and throw both originals away. So an MLP with no bend — 768 → 3072 → 768, about 4.7M parameters — is exactly equal to one 768 × 768 matrix holding 590K. The [bulge](/wiki/ai/llm/glossary) is refunded in full. Worse, the collapse doesn't stop at one block: chain twelve bend-free MLPs and they fold into a single matrix too.

(GPT-2's matrices each carry a bias vector too, which makes every step *affine* rather than strictly linear. It changes nothing: chain affine maps and you get a matrix plus a constant vector, which folds exactly as completely.)

That is the gap the activation fills. It sits between `A` and `B` and makes the fold impossible, so the second matrix has something genuinely new to work on and the parameters start earning their place.

One honest caveat: the MLP isn't the model's only nonlinearity — [the softmax inside attention](/wiki/ai/llm/one-attention-head) is one too, so a real transformer stripped of its activations wouldn't collapse *all* the way to a single matrix. But the MLP is two-thirds of every block's parameters, and without a bend, that two-thirds collapses.

## ReLU and the dead unit

The simplest possible bend is ReLU — rectified linear unit, `max(0, x)`. Positive numbers pass untouched, negative numbers become zero. It is one comparison, it is fast, and it works.

Its flaw is the corner. For any negative input the output is zero and, the part that bites, the *slope* is zero too. [Backprop](/wiki/ai/llm/backprop-one-weight) moves a weight by asking which way to nudge it, and a slope of exactly zero answers "nudging changes nothing." So a unit that lands negative for every example in the batch receives no gradient, never moves, and stays negative forever. It is dead: it contributes nothing, it cannot recover, and you are still paying for its parameters. Enough dead units and a chunk of the model is decoration.

## GELU: a dimmer, not a switch

[GPT-2](/wiki/ai/llm/gpt-2) uses **GELU**, the Gaussian error linear unit:

```text
GELU(x) = x · Φ(x)
```

`Φ(x)` is the standard normal cumulative distribution function — the probability that a single draw from a standard bell curve comes out below `x`. It runs smoothly from 0 for very negative `x` to 1 for very positive `x`.

So read GELU as a soft gate: **scale each number by how large it is relative to a bell curve.** A big positive input has `Φ` near 1 and passes nearly untouched. A big negative input has `Φ` near 0 and is suppressed nearly to nothing. In between, inputs are damped in proportion to how unremarkable they are.

That's the difference in one line. ReLU is a switch — on or off, with a corner where it flips. GELU is a dimmer: same overall behaviour, no corner anywhere, and never a slope of exactly zero, so no unit can die the way a ReLU unit does.

Two things about the curve are worth seeing rather than taking on trust:

```text
    x       ReLU(x)    GELU(x)
  -3.00      0.000     -0.004
  -1.00      0.000     -0.159
  -0.75      0.000     -0.170   ← the minimum
  -0.25      0.000     -0.100
   0.00      0.000      0.000
   0.50      0.500      0.346
   1.00      1.000      0.841
   3.00      3.000      2.996
```

First, negatives survive. GELU(−1) is −0.159, not 0 — small, but not nothing, and crucially not flat. Second, **GELU is not monotonic**, which surprises most people. Between −3 and −0.75 the curve goes *down*, bottoming at about −0.170, then turns and climbs back toward zero. A slightly-negative input produces a more negative output than a very-negative one. Nothing depends on this; it's just what `x · Φ(x)` does when `x` is negative and `Φ(x)` hasn't reached zero yet.

A GPT-2 wrinkle: computing `Φ` exactly needs the error function, `erf`, which was slow in 2019, so GPT-2 ships a `tanh`-based approximation instead. The two agree to about a thousandth. If you go looking, HuggingFace calls the approximation `gelu_new` — the name is the only confusing thing about it.

## SwiGLU: let the row pick the gate

GELU's gate has a limitation that's easy to miss: how much of `x` passes depends only on `x`. Each number decides its own fate, using a fixed rule baked in before training. Nothing else in the row gets a vote, and nothing about the gate is learned.

The gated linear unit (GLU) family asks the obvious next question — what if the gate were *computed* from the row, with weights the model trains? **SwiGLU** is that idea in its winning form. Project the row twice instead of once, into two separate 3072-wide vectors: call one the content and the other the gate. Bend the gate, multiply the two together element by element, project back down.

```text
GELU MLP     row ──[ W_up ]──▶ 3072 ──GELU──▶ 3072 ──[ W_down ]──▶ row

SwiGLU MLP   row ──[ W_up ]────────────▶ 3072 ─┐
                                               ⊗──▶ 3072 ──[ W_down ]──▶ row
             row ──[ W_gate ]──Swish──▶ 3072 ─┘
```

The bend on the gate branch is **Swish**, `x · σ(x)`, where `σ` is the sigmoid — the S-shaped curve that squashes any number into the range 0 to 1. (PyTorch ships Swish under its other name, `SiLU`, which is what you'll actually import.) Swish is GELU's near-twin in shape and cheaper to compute; the two are close enough that the choice between them is not where the win comes from. The win comes from the multiply. Because `W_gate` reads the *whole row*, the gate is data-dependent and learned: a unit can now be suppressed for reasons that have nothing to do with its own value, which GELU could never express.

**The cost is a third matrix.** GELU's MLP needs two; SwiGLU's needs three. At the same 3072 width that's 1.5× the parameters, which would be cheating in a comparison. So SwiGLU models shrink the bulge to pay for the extra matrix — the convention is a width of `8/3 · d_model` rather than `4 · d_model`, and the arithmetic is exact: three matrices at 8/3 is 8·`d_model`², and two at 4 is also 8·`d_model`². Llama's oddly-specific hidden width is that fraction, rounded to a convenient multiple. Same budget, rearranged.

**The payoff is measured, not explained.** For that identical budget, gated variants win a small but stubbornly consistent amount of loss, which is why they took over. Why they win, nobody really knows. Noam Shazeer's *GLU Variants Improve Transformer* (2020), the paper that introduced SwiGLU, closes with the most honest sentence in the literature: *"We offer no explanation as to why these architectures seem to work; we attribute their success, as all else, to divine benevolence."* It's a joke, and it's also the actual state of the art. This is an empirical result that stuck because it kept winning, and the bend that beat GELU did it without ever explaining itself.

## Check yourself

**Watch the collapse.** [Make two random matrices](/wiki/ai/llm/running-the-checks), `A` of 768 × 3072 and `B` of 3072 × 768 — the shape of GPT-2's MLP, 4.7M numbers between them. Build them in `float64`; the reason is worth a paragraph and it's below. Precompute `C = A @ B`, a single 768 × 768 matrix holding 590K. Now `torch.allclose(x @ A @ B, x @ C)` passes for every `x` you throw at it. Eight times the parameters, the same function, provable in six lines with no download. Then put a GELU between them and go looking for a `C` that reproduces it — there isn't one, and that failure is the activation earning its keep.

Now the `float64`. Run that same test in `float32`, the dtype you'd reach for by default, and `allclose` returns **False** — which looks like the page lying to you and isn't. The relative error is about 6e-7 across the board: ordinary roundoff from summing 3072 products, exactly the [float32 drift the causal mask page runs into](/wiki/ai/llm/causal-mask). It fails because `allclose`'s default tolerance is *relative*, so the handful of outputs that land near zero are asked to match to within about 1e-8 while carrying 1e-3 of accumulated float error. The maths is exact; `float32` just can't show it to you. Either use `float64` or loosen the tolerance to `rtol=1e-4, atol=1e-2` — and note which one of those two is the honest fix.

**Find the minimum.** `torch.nn.functional.gelu(torch.tensor(-0.7518))` returns about −0.1700, and that is the lowest value GELU takes anywhere on the number line. Sweep `x` from −5 to 0 in small steps and confirm nothing dips below it. A bend that goes down before it goes up.

## Depends on / leads to

Depends on [the MLP](/wiki/ai/llm/multi-layer-perceptron). Leads to [LayerNorm and RMSNorm](/wiki/ai/llm/normalization).
