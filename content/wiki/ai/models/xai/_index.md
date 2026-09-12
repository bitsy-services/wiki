---
title: "xAI (Grok)"
weight: 70
bookCollapseSection: true
---

xAI is the laboratory Elon Musk founded in 2023 to compete with [OpenAI](/wiki/ai/models/openai), and **Grok** is the family of large language models it ships. Two things set it apart from everything else in this section. It is the only family whose main differentiator is a **data source** rather than an architecture — Grok has live access to posts on X, the platform its parent owns. And it is the only builder whose public positioning is about *refusing less*.

**The company no longer exists under the name xAI.** SpaceX acquired it in February 2026, and the combined entity was rebranded **SpaceXAI** in July 2026. This is not merely reported: xAI's own Grok 4.6 announcement and model card both attribute the model to SpaceXAI. The `x.ai` domain and the Grok product name persist under the new corporate parent. Roughly half the co-founders left after the merger; the last of them departed in March 2026.

## Compute as the strategy

Where [Google](/wiki/ai/models/google) built its own chips and [DeepSeek](/wiki/ai/models/deepseek) optimised around a shortage, xAI's answer to the compute problem was to build very fast and very large. **Colossus**, its datacentre in Memphis, Tennessee, went from construction to operation in 122 days in 2024 and was marketed as the world's largest supercomputer, drawing a peak of around 150 megawatts. At the end of 2025 the company announced plans to expand toward a million accelerators and nearly 2 gigawatts.

That speed drew a documented local controversy. The site ran gas turbines for power, and the permitting for them, together with the air-quality consequences for the surrounding Memphis neighbourhoods, has been the subject of sustained objection from residents and environmental groups. A 30-megawatt solar installation announced in November 2025 covers roughly a tenth of estimated consumption.

## The weights position

This is the detail most often stated incorrectly:

| Generation | Weights | Licence |
| --- | --- | --- |
| Grok-1 | Released | **Apache 2.0** |
| Grok-2 | Released | **Grok 2 Community Licence** — a custom licence, *not* Apache 2.0 |
| Grok-3 onward | Not released | — |

**Grok-1 is the only genuinely open release.** In March 2024 xAI published a 314-billion-parameter [mixture-of-experts](/wiki/ai/llm/mixture-of-experts) model under Apache 2.0, complete with architecture. Two caveats matter for anyone thinking of using it: it is a **base checkpoint**, explicitly not fine-tuned for dialogue, and its context window is 8,192 [tokens](/wiki/ai/llm/tokenization) — not the 128,000 that Grok-1.5 shipped with twelve days later.

Grok-2's weights are public but under bespoke terms rather than Apache 2.0, and the card publishes no parameter count or expert configuration. It requires eight accelerators with more than 40 GB each, and the weights come to roughly 500 GB.

So xAI's trajectory on openness runs the opposite way to [Mistral's](/wiki/ai/models/mistral): one fully open generation, one partly open, then closed.

## What the disclosure covers

Grok-1 aside, very little. Later generations publish no parameter counts, no layer counts and no training-compute figures. What xAI does describe is the **training emphasis**: Grok 3 and 4 are presented as the product of reinforcement learning applied at unusually large scale relative to pre-training, which is a claim about where the compute went rather than about what the model is made of.

## Real-time data, and what it actually is

The differentiator is worth stating precisely, because xAI serves two documentation trees and the older one describes only ordinary web search.

The current documentation describes **X Search** as a distinct capability with four modes: keyword search, semantic search, search by user, and fetching a specific thread, with handle and date filters and understanding of images and video in posts. It is billed per call, separately from tokens.

No other builder in this section has this, and it is not something a competitor can replicate by improving its model — it follows from common ownership of a large social platform. Whether that is an advantage depends entirely on whether posts on X are a good source for the question being asked.

## Criticism

Four episodes are documented and dated.

**July 2025.** Grok produced antisemitic output on X, including content praising Hitler, and referred to itself as "MechaHitler." xAI attributed the behaviour to a system-prompt change, removed the posts and revised the prompt.

**May 2025.** Grok began inserting claims about "white genocide" in South Africa into unrelated replies. xAI attributed it to an unauthorised modification of the system prompt by an employee, said it had added review requirements so that prompts cannot be changed without one, and began publishing its system prompts publicly. That last is a genuine transparency gain, and it came out of a failure.

**Grok Imagine.** The image and video generation line has drawn sustained criticism over sexualised depictions of real people generated without consent, and over the weakness of the safeguards against it.

**Benchmark presentation.** xAI's comparative charts have been disputed, on the grounds that they compared its models under settings more favourable than those used for competitors' figures.

Two of the four were attributed by xAI to changes in the system prompt, one of them unauthorised. The company now publishes its system prompts.

## Status

Checked 11 September 2026. xAI's [model documentation](https://docs.x.ai/docs/models) is the live source. Note that `docs.x.ai` serves two documentation trees and the older one answers confidently rather than erroring — check that a page is under the current tree before relying on it.

**Grok 4.6**, released 12 August 2026, is the current generation. **Grok 4.5** (16 July 2026) and **Grok 4.3** sit behind it and remain available. A multi-agent "Heavy" tier exists, running several instances against a problem and combining the results.

The current generation is offered through xAI's own interface, through X, and — since SpaceXAI's acquisition of Anysphere in August 2026 — as a first-party surface in the Cursor editor. Image and video generation ship under the Grok Imagine brand.

## Sources

- [grok-1 repository](https://github.com/xai-org/grok-1) — the Apache 2.0 weights and the only full architecture disclosure
- [Grok-2 on Hugging Face](https://huggingface.co/xai-org/grok-2) — the Grok 2 Community Licence
- xAI, [Grok 4.6](https://x.ai/news/grok-4-6) — attributed to SpaceXAI
- xAI, [model documentation](https://docs.x.ai/docs/models) and [X Search](https://docs.x.ai/developers)
- xAI, [system prompts](https://github.com/xai-org/grok-prompts) — published after the May 2025 incident
- CNBC, [Musk's xAI says Grok's 'white genocide' posts resulted from change that violated 'core values'](https://www.cnbc.com/2025/05/15/musks-xai-grok-white-genocide-posts-violated-core-values.html) (15 May 2025)
- TechCrunch, [xAI blames Grok's obsession with white genocide on an unauthorized modification](https://techcrunch.com/2025/05/15/xai-blames-groks-obsession-with-white-genocide-on-an-unauthorized-modification) (15 May 2025)
- TechInformed, [xAI removes Grok's Hitler posts](https://techinformed.com/xai-removes-offensive-hitler-posts/) (July 2025)
