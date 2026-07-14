---
title: "Mixture of Experts"
weight: 300
---

Replace the single MLP in a block with N of them — "experts" — plus a small router. The router scores the row, picks the top one or two, and only those run. Attention is untouched; MoE is a story about [the MLP](/wiki/ai/llm/the-mlp) and nothing else.

The trade is parameters for FLOPs, and it's a good one. Eight experts give a block eight times the MLP weights, but each row still runs through only one or two of them, so compute per token barely moves. Mixtral: 46.7B parameters total, 12.9B active per token — a *top-2* number. Route to one expert and only ~7B would be active, at half the MLP FLOPs. You're buying capacity — more places to put what the model knows — without buying much latency.

Two things routinely surprise people. Routing is per **row**, not per sequence: the same sentence sends different tokens to different experts, and the choice shifts when the context changes. And "active parameters" is a compute number, not a memory number — every expert must be resident whether or not this token touches it. An MoE is cheap to run and expensive to host.

The failure mode is load collapse: the router finds three experts it likes, starves the rest, and you're paying for N while using three. Real implementations add an auxiliary load-balancing loss to force the traffic to spread.

## Check yourself

In nanoGPT, swap one block's MLP for eight copies plus a linear router, top-1. That block goes from 7.1M parameters to 40.2M — 5.67×, because the MLP was two-thirds of it — while step time barely moves. Then log the router's pick per token: adjacent tokens frequently land on different experts.

## Depends on / leads to

Depends on [the MLP](/wiki/ai/llm/the-mlp). Leads to [superposition](/wiki/ai/llm/superposition).
