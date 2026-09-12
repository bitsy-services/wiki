---
title: "Mistral Large 3"
weight: 10
---

Mistral Large 3 is [Mistral AI](/wiki/ai/models/mistral)'s flagship, released 2 December 2025: 675 billion total parameters, 41 billion active, a 256,000-token context, and weights published under **Apache 2.0**.

That last fact is the reason for this page. Mistral's documentation lists its most capable model under *open weight models* rather than in a premier tier — and among the eight builders in this section, no other flagship is Apache 2.0. [DeepSeek](/wiki/ai/models/deepseek) publishes its current generation under MIT, which is comparably permissive; every other lab either withholds its best weights entirely or attaches conditions to them.

## Why this is a reversal

The standard account of Mistral is that it built a reputation on open releases and then reserved its best work for a paid service. For 2024 and 2025 that was accurate:

- **Mistral Large** (February 2024) was service-only.
- **Mistral Large 2** (July 2024) shipped weights under a **research-only** licence — no commercial use without a separate agreement.
- **Codestral 22B** got a bespoke **non-production** licence, permitting evaluation but not deployment.

Mistral Large 3 is the third generation of that line and it is Apache 2.0. The company's own framing, from the funding announcement titled *Making sovereign, open-weight AI the technology frontier*, is that open weights are what stop customers being "locked into a single vendor's roadmap, pricing or availability."

Anyone repeating the "open early, closed later" criticism is describing a real period that has since ended.

## The licence landscape around it

Mistral currently uses four sets of terms, and the model's name does not tell you which applies:

| Terms | Effect | Applied to |
| --- | --- | --- |
| **Apache 2.0** | Any purpose, distribution, modification | Mistral Large 3, Mistral Small 4, Ministral 3 |
| **Modified MIT** | Apache-equivalent, except above $20M monthly revenue | Mistral Medium 3.5 |
| **Research Licence** | Non-commercial research only | Mistral Large 2, Pixtral Large |
| **Non-Production Licence** | Evaluation in non-production environments | Codestral 22B |

Note the shape of the current lineup: Mistral Medium 3.5 is more expensive to use through Mistral's service than Mistral Large 3 is, and carries the *more* restrictive licence. The price ladder and the name ladder do not run in the same order, and neither tracks openness.

## Total and active

675 billion total with 41 billion active is a [mixture of experts](/wiki/ai/llm/mixture-of-experts) in the now-standard proportion — roughly one parameter in sixteen participates in any given token.

Both numbers matter and they answer different questions. **675 billion is what must be resident in memory**, because the router may send the next token to any expert. **41 billion is what each token is actually multiplied by**, which sets the arithmetic and therefore the latency. A reader budgeting hardware needs the first; a reader budgeting time or cost per token needs the second. Mistral's own lineage supplies the clearest worked example of why the distinction confuses people: [Mixtral 8x7B](/wiki/ai/models/mistral/mixtral).

## What it means to have the weights

The practical content of an Apache 2.0 flagship is worth spelling out, because "open weights" is often treated as an ideological position rather than a set of capabilities:

- It can process data that is not permitted to leave a building or a jurisdiction.
- It can be [fine-tuned](/wiki/ai/llm/fine-tuning) by a third party on proprietary data without that data reaching the vendor.
- It cannot be withdrawn, repriced or silently changed underneath a deployment.
- It can be inspected by anyone, which is the precondition for independent safety and capability research.

Those four are why Mistral's stated customers — enterprise and government in finance, manufacturing, defence, energy and public administration — are a different buyer from the one most of this section sells to, and why the sovereignty argument is a product argument rather than a political one.

## Status

Checked 11 September 2026. Mistral's [model overview](https://docs.mistral.ai/getting-started/models/models_overview/) is the live source, and the [licence explainer](https://help.mistral.ai/en/articles/347393-under-which-license-are-mistral-s-open-models-available) is the authority on which terms apply to which model.

Mistral Large 3 was released 2 December 2025, with the service identifier `mistral-large-2512`. It is multimodal, taking text and images. The current lineup around it is Mistral Medium 3.5 (128B dense, April 2026), Mistral Small 4 (119B total / 6B active, March 2026) and the Ministral 3 sizes at 14B, 8B and 3B.

The specialised lines that once ran alongside — Magistral for reasoning, Devstral for code, Pixtral for vision — were retired on or before 31 July 2026 and folded into these models, with reasoning exposed as a `reasoning_effort` setting.

## Sources

- Mistral AI, [Mistral 3](https://mistral.ai/news/mistral-3) (2 December 2025)
- Mistral AI, [model overview](https://docs.mistral.ai/getting-started/models/models_overview/)
- Mistral AI, [Under which license are Mistral's open models available?](https://help.mistral.ai/en/articles/347393-under-which-license-are-mistral-s-open-models-available)
- Mistral AI, [Making sovereign, open-weight AI the technology frontier](https://mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier/)
