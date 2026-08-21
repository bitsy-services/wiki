---
title: "Backprop Through One Weight"
weight: 240
---

Backprop is how the model finds out which way to adjust each of its weights. Training needs, for every single number in the model, an answer to one question: would nudging this number up make the predictions better or worse, and by how much? Working that out separately for each weight would be hopelessly expensive, because there are far too many of them. Backprop gets every answer in a single sweep backwards through the model, reusing at each step the work it has already done. This page follows one weight through that sweep, because the story for one is the story for all of them.

## The question being asked

Pick one number out of [GPT-2 small](/wiki/ai/llm/gpt-2)'s 124 million — a single entry `w` in block 6's MLP input matrix. Backprop answers exactly one thing about it: *if I nudge `w` up a hair, does the loss go up or down, and how fast?*

That's `∂L/∂w`, the partial derivative of [the loss](/wiki/ai/llm/the-loss-function) with respect to that one weight. A positive value means increasing `w` makes the model worse, so decrease it. That's all a gradient is: a direction and a strength, per weight.

## Why not just try it and see?

There is an obvious way to get that number without any calculus. Nudge `w` up by a hair and run the model; nudge it down by the same hair and run again; subtract the two losses and divide by the size of the nudge. That's the derivative, near enough, and it needs no theory whatsoever.

Do the arithmetic on what it costs. Two forward passes per weight, 124 million weights, so roughly 250 million forward passes — to compute *one* training step. GPT-2 was trained for hundreds of thousands of steps. Multiply those together and the answer isn't "slow," it's a number with no physical meaning.

Backprop produces every one of those 124 million gradients for about the cost of two more forward passes. Not two per weight — two, total. That factor of tens of millions is not an optimization; it is the entire reason training a [neural network](/wiki/ai/llm/neural-networks) is a thing anyone can do, and it's why the same idea has survived unchanged since the 1980s while everything around it was replaced.

## The sweep, and where the savings come from

The loss is computed at the right edge. Its gradient flows right to left, and at each operation the gradient arriving from the right is multiplied by that operation's own local derivative — the chain rule, applied mechanically, one operation at a time.

The reuse is the whole trick, and it's easy to miss. When the sweep reaches block 7, it computes the gradient with respect to block 7's *output* exactly once. Every weight inside block 7 then reads that same number, and so does everything to its left. Nothing is recomputed. The finite-difference approach above throws all of that away and starts from scratch for every weight, which is precisely why it costs a hundred million times more.

Think of a company tracing a bad quarter back through its org chart. Each manager is told how much their department's result mattered and divides that responsibility among their own reports, in proportion to each one's influence. Every manager does this exactly once, regardless of how many people sit below them, and the blame reaches the bottom of the chart in a single pass down. Asking each individual employee separately what would have changed had they worked differently means re-running the whole quarter, once per employee.

Make it a matrix organization, where people report to more than one manager and each sends down a share independently, and the analogy gets the next part right too: an employee's total blame is the *sum* of what every manager above them passed down.

## It is a sum over paths, not a product

By the time the gradient reaches `w`, the number is a **sum over every path** from `w` to the loss — through the [skip connections](/wiki/ai/llm/skip-connections), through every block to its right — where each individual path contributes a product of local derivatives.

The distinction matters more than it looks. A product of a dozen small numbers is reliably a very small number. A sum that includes one path of derivative 1 — running straight down the residual stream, touching no block's weights at all — has no such tendency, though nothing makes it *impossible* for the remaining terms to cancel it out.

That structure is what [skip connections](/wiki/ai/llm/skip-connections) buy, and it's worth carrying that page's caveat along with it: in a model that also has [normalization](/wiki/ai/llm/normalization), taking the skips away does not in fact make gradients vanish. The sum-rather-than-product shape is real and it is genuinely why the gradient has a clean road home. The dramatic collapse it usually gets credited with preventing is a story about unnormalized networks, not this one.

## And a sum over rows

`w` was also used at every position in the sequence — [the same weights run everywhere](/wiki/ai/llm/weight-sharing) — and its gradient adds up every one of those uses. A single 1024-token sequence gives `w` a thousand votes on which way it should move.

Then the update itself, which is the anticlimax of the page: `w ← w − lr · ∂L/∂w`, where `lr` is the **learning rate**, a small number setting how far to move per step. Step downhill, a little. Adam, momentum, weight decay, learning-rate warmup — every optimizer anyone has built is a refinement of *how much to trust that one number*, not a replacement for it.

## Check yourself

Take a single weight in [nanoGPT](/wiki/ai/llm/running-the-checks) and record the gradient that **autograd** — PyTorch's built-in machinery for running exactly the backward sweep described above — reports for it. Now compute the same number the expensive way: `(L(w+ε) − L(w−ε)) / 2ε`, `ε = 1e-3`, same batch, model in `eval()` (dropout will destroy the difference), cross-entropy computed yourself in float64. The two agree to ~7 significant figures.

That's the standard gradient check, and it's the fastest way to prove a hand-written backward pass wrong. Note what you just did: you spent two forward passes to verify one weight out of millions, which is the cost argument above, demonstrated rather than asserted.

## Depends on / leads to

Depends on [the loss function](/wiki/ai/llm/the-loss-function) and [skip connections](/wiki/ai/llm/skip-connections). Leads to [weight sharing across positions](/wiki/ai/llm/weight-sharing).
