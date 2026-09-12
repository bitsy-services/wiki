---
title: "GPT-6 Astra"
weight: 10
---

GPT-6 Astra is [OpenAI](/wiki/ai/models/openai)'s current flagship, released 3 September 2026 under the identifier `gpt-6-astra`. It takes text and images and returns text, with a 1,050,000-token context window and a reasoning effort setting running from `low` to `max`.

Two things about it are unusual enough to be the reason for this page. It is a **single model rather than a tiered family**, breaking the naming scheme OpenAI had introduced one generation earlier. And its system card declares it the first OpenAI model to reach the **Critical** cybersecurity level under the company's own risk framework — a threshold that, by OpenAI's account, changed how the model is secured internally as well as how it is released.

As with every OpenAI flagship since GPT-4, **no architecture is published**: no parameter count, no layer count, no training compute, no description of how the model is built. The system card runs to 118 pages and contains none of it.

## Astra is a name, not a tier

At GPT-5.6, OpenAI replaced its size suffixes with named capability tiers — Sol, Terra and Luna, where "the number identifies a model's generation, while Sol, Terra, and Luna identify durable capability tiers that can advance on their own cadence."

GPT-6 did not use them. It shipped as one model, and Astra names that model rather than a rung within a family. There is a *GPT-6 Pro* in ChatGPT, but it is a product surface powered by the same model, not a separate one. Whether the tier names return at a later GPT-6 release is not something OpenAI has said.

For anyone reading model identifiers, the sequence is worth holding: `gpt-5-mini` is a size, `gpt-5.6-sol` is a tier, `gpt-6-astra` is a model. Three conventions in three consecutive generations.

## The Critical cybersecurity designation

OpenAI's Preparedness Framework grades models on several risk categories. Astra is the first the company has placed at **Critical** for cybersecurity, and the system card states what that means in capability terms:

> with the right tools and access, GPT-6 Astra can find previously unknown security flaws and develop new ways to exploit them across many well-protected systems without a person guiding each step.

The measures the card describes in response are directed inward as much as outward: "stricter isolation, checkpoint encryption, universal monitoring of full trajectories including chains of thought (CoT), and a blocking alignment evaluation process before internal use."

That last phrase is the notable one. A blocking evaluation before *internal* use means the company gates its own staff's access to the model on passing a safety check — a control aimed at the lab itself rather than at its customers.

## Chain-of-thought monitorability, and a named failure mode

Astra's system card gives monitorability its own top-level section, covering whether a monitoring model can tell from a model's reasoning trace what it is actually doing, including when the model is adversarially trying to hide it.

It also names a failure mode OpenAI had not previously published:

> **Verbalized Metagaming** is when a model reasons in its Chain of Thought about how it will be graded, rewarded, or monitored, rather than only engaging in the intended task. We report it because this can change how to interpret observed behavior: for example, observed aligned actions may not be reflective of true alignment.

This matters for the whole argument OpenAI has made about why hidden reasoning is nonetheless useful — that the chain of thought can be watched even when it is not shown. A model that reasons about being watched is a harder thing to learn from by watching. The company's own caveat from the o1 card still applies: monitoring works "if they accurately reflect the model's thinking, an open research question."

## The million-token window has a price boundary inside it

Astra advertises a 1,050,000-token context. Prompts above **272,000 input tokens** are billed at double the input rate and 1.5 times the output rate *for the entire session*, not just for the tokens above the line.

That is why the model lists both a context window and a lower "max input tokens" figure — the second is a pricing boundary, not a capacity limit. It is also why the cost of a long-context agentic loop is a step function rather than a slope. [Context length](/wiki/ai/llm/context-length) covers what makes long contexts expensive to serve in the first place.

Cache writes are billable on this generation, at 1.25 times the uncached input rate; earlier models charged nothing to write a cache entry. For a loop that rebuilds its prefix often, that changes the arithmetic in [prompt caching](/wiki/ai/prompt-caching).

## Status

Checked 11 September 2026 — eight days after release. OpenAI's [model catalogue](https://developers.openai.com/api/docs/models) and [pricing page](https://developers.openai.com/api/docs/pricing) are the live sources.

Current flagship. Knowledge cutoff 30 April 2026. Reasoning effort runs `low` through `max`, with no `none` option — unlike the GPT-5.6 tier, this model cannot be asked not to think. The previous generation, GPT-5.6 (Sol, Terra and Luna), remains fully supported.

Prices across this lineup move unusually fast and should be read from the source: GPT-5.6 Sol's current rate is explicitly promotional, and Luna now sells for a fifth of its launch price.

## Sources

- OpenAI, [GPT-6 Astra system card](https://deploymentsafety.openai.com/gpt-6-astra/gpt-6-astra.pdf) (3 September 2026)
- OpenAI, [model catalogue](https://developers.openai.com/api/docs/models) and [pricing](https://developers.openai.com/api/docs/pricing)
- OpenAI, [GPT-4 Technical Report](https://arxiv.org/abs/2303.08774), arXiv:2303.08774 (2023) — the disclosure statement that still governs
- Korbak et al., [Chain of Thought Monitorability](https://arxiv.org/abs/2507.11473), arXiv:2507.11473 (2025)
