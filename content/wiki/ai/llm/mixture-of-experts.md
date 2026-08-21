---
title: "Mixture of Experts"
weight: 300
---

Mixture of experts is a way to make a model know more without making it cost more to run. The trick is to stop sending every word through every part of the model. A block keeps several alternative copies of its bulkiest component, along with a small piece of machinery that decides, word by word, which handful of them to use — so the model's total size can grow many times over while the work done on any individual word barely moves. It is how most frontier models are now built, and what it really does is convert a compute problem into a memory problem.

## The bind it gets you out of

Most of what a model knows lives in [the MLP](/wiki/ai/llm/the-mlp) — two-thirds of every block's weights, and the best available guess at where the facts are.

So if you want a model that knows more, you want more MLP. And here the two things everyone wants collide head-on: producing even a single token means running that token through the model's weights, so more weights means more arithmetic per token, always, no matter how short the prompt. Capacity and speed are the same dial turned in opposite directions.

Unless the token doesn't have to visit all of it.

## What replaces the MLP

Replace the single MLP in a block with N of them — the **experts** — plus a small **router**. The router scores the row, picks the top one or two experts, and only those run. Everything else in the block is untouched: attention in particular is left exactly as it was, and MoE is a story about the MLP and nothing else.

Think of a hospital with twelve doctors on the payroll. However deep that bench is, any given patient sees one of them, so an appointment costs what an appointment costs — the hospital's capacity and your visit's cost have been decoupled. Staffing the building, on the other hand, costs all twelve salaries whether or not today's patients happen to need all twelve, which is the half of this analogy that turns out to matter most.

Don't push it as far as the word *specialist*, though. The routing is much stranger than a triage desk, as the next section explains.

## The trade: parameters for FLOPs

Eight experts give a block eight times the MLP weights, but each row still runs through only one or two, so compute per token barely moves.

Mixtral is the standard worked example: 46.7B parameters in total, 12.9B **active** per token — that second figure being a top-2 number. Route to a single expert instead and only about 7B would be active, at half the MLP arithmetic. What you're buying is capacity, meaning more places to put what the model knows, without buying much latency.

## Two things that routinely surprise people

**Routing is per row, not per sequence.** The same sentence sends different tokens to different experts, and the choice shifts when the context around a token changes. There is no "this is a physics question, use the physics expert" — the granularity is far finer and far less interpretable than the name suggests. Experts do not, on inspection, correspond to subjects.

**"Active parameters" is a compute number, not a memory number.** Every expert must sit resident in memory whether or not this particular token touches it, because the next token might. So an MoE is cheap to *run* and expensive to *host* — and that is the whole trade restated. You have not made the model smaller. You have made it faster while keeping it exactly as large, and moved the binding constraint from arithmetic to how much memory your hardware has.

## The failure mode: load collapse

Routing is learned, and learned routing has a rich-get-richer problem built into it. An expert that receives more traffic gets more gradient updates, becomes better at what it's handed, and so attracts more traffic still. Left alone, the router finds three experts it likes, starves the rest, and you are paying to host N experts while using three of them.

Real implementations add an auxiliary **load-balancing loss** — an extra term in training that penalizes uneven traffic — to force the distribution to spread. It's not a refinement; without it the technique doesn't work.

## Check yourself

In [nanoGPT](/wiki/ai/llm/running-the-checks), swap one block's MLP for eight copies plus a linear router, top-1. That block goes from 7.1M parameters to 40.2M — 5.67×, because the MLP was two-thirds of it — while step time barely moves. Then log the router's pick per token: adjacent tokens frequently land on different experts, which is the per-row claim above, and is not what you'd see if experts were subject specialists.

## Depends on / leads to

Depends on [the MLP](/wiki/ai/llm/the-mlp). Leads to [fine-tuning](/wiki/ai/llm/fine-tuning).
