---
title: "Mistral AI"
weight: 80
bookCollapseSection: true
---

Mistral AI is a Paris company that trains open-weight large language models, and it is the only European lab in this section. Its distinguishing fact today is one that would have surprised anyone tracking it two years ago: **its most capable model is Apache 2.0.** Mistral Large 3 — 675 billion total parameters, 41 billion active — sits in Mistral's documentation under *open weight models*, not under the premier tier.

The company was founded in April 2023 by Arthur Mensch, Guillaume Lample and Timothée Lacroix. The provenance matters: Lample and Lacroix were authors on Meta's [LLaMA paper](/wiki/ai/models/meta) and Mensch on Google DeepMind's Chinchilla scaling paper, so the founders wrote two of the papers the rest of this section rests on before leaving to compete with their former employers.

## Two models that taught the field something

**Mistral 7B** (September 2023) was the model that made "small and good" a serious position. It combined [grouped-query attention](/wiki/ai/llm/grouped-query-attention) with sliding-window attention — each layer attending only to a fixed span of recent tokens rather than the whole sequence — and demonstrated that careful design beat raw parameter count at that scale. For a great many people it was the first capable model they ran on their own hardware.

**Mixtral 8x7B** (December 2023) was the first widely-used open sparse [mixture of experts](/wiki/ai/llm/mixture-of-experts), and its name is the single most instructive piece of arithmetic in this section.

### Why `8x7B` is 46.7 billion parameters, not 56

The name reads like eight 7-billion-parameter models stapled together. It is not. Only the **feed-forward block** of each transformer layer is replicated eight times. The attention projections, the token embeddings, the output head and the normalisation parameters exist once and are shared by all eight experts:

```text
total  = shared (attention + embeddings + norms) + 8 × feed-forward  = 46.7B
active = shared (attention + embeddings + norms) + 2 × feed-forward  = 12.9B
```

Eight independent 7B models would be 56 billion parameters. The roughly 9 billion difference is exactly the shared machinery that would have been duplicated. And per token the router selects 2 of the 8 experts, so the feed-forward cost is two experts' worth — but the shared attention and embedding parameters are paid once regardless, which is why the active figure is 12.9 billion rather than a clean 14.

Both numbers are needed to reason about the model, and they answer different questions: 46.7 billion is what must sit in memory, 12.9 billion is what each token is multiplied by.

## The licence split

Mistral uses **four** sets of terms, not two, and the difference between them decides whether a model can be deployed at all:

| Terms | What it allows |
| --- | --- |
| **Apache 2.0** | Any purpose, distribution, modification. The default for open models: Mistral Large 3, Mistral Small 4, the Ministral 3 sizes, and historically Mistral 7B and the Mixtrals. |
| **Modified MIT** | Apache-equivalent, except that organisations with monthly revenue above $20 million need a commercial licence or must use Mistral's hosted service. Used for Mistral Medium 3.5. |
| **Mistral Research Licence** | Research only — "personal, scientific or academic research and for non-profit and non-commercial purposes". Commercial use needs a separate agreement. Applied historically to Mistral Large 2 and Pixtral Large. |
| **Non-Production Licence** | Testing, research and evaluation in non-production environments only. Introduced for Codestral 22B. |

Alongside these sit genuinely closed models — the embedding, moderation, document-recognition and speech lines are interface-only.

The practical consequence is that "is it a Mistral open model?" is not a question with one answer. Two models released months apart can differ on whether a business may run them at all, and the model's name does not tell you which.

## The reversal, and the criticism that is now out of date

The standard criticism of Mistral is that it built its reputation on Apache 2.0 releases and then reserved its best work for a paid interface. For 2024 and 2025 that was accurate: Mistral Large was interface-only, Mistral Large 2 shipped weights under a research-only licence, and Codestral got a bespoke non-production licence.

**What has happened since is a reversal.** Mistral Large 3, released December 2025, is Apache 2.0. Mistral Medium 3.5, the most expensive model in the lineup, publishes its weights under Modified MIT. The company's funding announcement is titled "Making sovereign, open-weight AI the technology frontier," and argues that open weights are what prevent customers being "locked into a single vendor's roadmap, pricing or availability."

A page reporting only the old criticism would be wrong about the present; one reporting only the current openness would be wrong about how the company got here. Both halves are the story.

## The sovereignty argument

Mistral's positioning is not mainly about capability rankings, and treating it as a smaller American lab misses what it sells. Its stated target customers are enterprise and government in finance, manufacturing, defence, energy and public administration — buyers for whom *where the model runs and who controls it* is a procurement requirement rather than a preference.

The funding follows that positioning rather than the usual venture pattern: a Series C led by the Dutch semiconductor-equipment maker ASML in September 2025, then a Series D of about €3 billion led by Samsung Electronics, with the Grand Duchy of Luxembourg among the investors. Strategic industrial and sovereign money, not growth capital.

This is where open weights stop being an ideological position and become a product feature. A European bank or defence ministry that cannot send data to a United States interface, and cannot accept that a vendor might withdraw or reprice a model mid-contract, has a short list of options. Mistral is on it; most of this section is not. The same logic explains why Google markets [Gemma](/wiki/ai/models/google/gemma) for air-gapped deployment.

## Consolidation

Mistral once ran parallel specialised lines — Magistral for reasoning, Devstral for code, Pixtral for vision. **Those are retired**, all on or before 31 July 2026, replaced by Mistral Medium 3.5 and Mistral Small 4. Mistral Small 4 "consolidates three specialized models into one" with a `reasoning_effort` setting, which is the same consolidation [OpenAI](/wiki/ai/models/openai) made when GPT-5 absorbed the `o`-series and [DeepSeek](/wiki/ai/models/deepseek) made when the R line merged back into V. Three labs of very different sizes reached the same conclusion within about a year: a reasoning model is better as a setting than as a separate product.

## Status

Checked 11 September 2026. Mistral's [model overview](https://docs.mistral.ai/getting-started/models/models_overview/) is the live source, and its [licence explainer](https://help.mistral.ai/en/articles/347393-under-which-license-are-mistral-s-open-models-available) is the authority on which terms apply to which model.

| Model | Size | Context | Licence |
| --- | --- | --- | --- |
| Mistral Large 3 | 675B total / 41B active | 256K | Apache 2.0 |
| Mistral Medium 3.5 | 128B dense | 256K | Modified MIT |
| Mistral Small 4 | 119B total / 6B active | 256K | Apache 2.0 |
| Ministral 3 | 14B, 8B, 3B dense | 256K | Apache 2.0 |

Mistral Large 3 was released 2 December 2025, Mistral Small 4 on 16 March 2026 and Mistral Medium 3.5 on 28 April 2026. Closed models cover embeddings, moderation, document recognition and speech.

## Sources

- Jiang et al., [Mistral 7B](https://arxiv.org/abs/2310.06825), arXiv:2310.06825 (2023)
- Jiang et al., [Mixtral of Experts](https://arxiv.org/abs/2401.04088), arXiv:2401.04088 (2024)
- Mistral AI, [Mixtral of experts](https://mistral.ai/news/mixtral-of-experts/) (11 December 2023) — the 46.7B / 12.9B figures
- Mistral AI, [Mistral 3](https://mistral.ai/news/mistral-3) (2 December 2025)
- Mistral AI, [Mistral Small 4](https://mistral.ai/news/mistral-small-4/) (16 March 2026)
- Mistral AI, [Under which license are Mistral's open models available?](https://help.mistral.ai/en/articles/347393-under-which-license-are-mistral-s-open-models-available)
- Mistral AI, [Making sovereign, open-weight AI the technology frontier](https://mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier/)
- Mistral AI, [About](https://mistral.ai/about/) — founding and positioning
