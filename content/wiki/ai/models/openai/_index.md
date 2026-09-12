---
title: "OpenAI"
weight: 10
bookCollapseSection: true
---

OpenAI trains the **GPT** family of large language models and serves them through an API and through ChatGPT. Its early models are the reason this wiki can teach the architecture at all: GPT-1, GPT-2 and GPT-3 shipped with papers giving layer counts, hidden dimensions, training-token counts and parameter counts, and [GPT-2 small](/wiki/ai/llm/gpt-2) is still the worked example throughout the [large language models](/wiki/ai/llm) section because its weights are public and it runs on a laptop.

That stopped at GPT-4, and OpenAI said so in writing rather than letting the silence be inferred. The GPT-4 technical report has a section headed *Scope and Limitations of this Technical Report*:

> Given both the competitive landscape and the safety implications of large-scale models like GPT-4, this report contains no further details about the architecture (including model size), hardware, training compute, dataset construction, training method, or similar.

Every flagship since has held that line. The GPT-6 Astra system card runs to 118 pages and states no parameter count, no training-compute figure and no description of the architecture.

## Reading the names

The scheme has been rebuilt twice, which is why models three years apart look like they belong to different companies.

**Through GPT-5.5**, a version number carried size variants: `gpt-5`, `gpt-5-mini`, `gpt-5-nano`, `gpt-5-pro`. Smaller suffix, smaller and cheaper model.

**At GPT-5.6 the suffixes became named tiers.** OpenAI's framing: "the number identifies a model's generation, while Sol, Terra, and Luna identify durable capability tiers that can advance on their own cadence." Sol is frontier reasoning and long-horizon agentic work, Terra is balanced everyday work, Luna is lowest cost. The point of the change is that a tier can move independently of the generation number.

**GPT-6 then shipped as a single model, `gpt-6-astra`**, with no Sol/Terra/Luna split. Astra is a model name rather than a tier. A *GPT-6 Pro* exists in ChatGPT but is a product surface powered by the same model, not a separate one.

Running alongside all of this until recently was the **`o`-series** — `o1`, `o3`, `o4-mini` — a separate line of reasoning models. **GPT-5 absorbed it.** OpenAI described GPT-5 as "a unified system with a smart and fast model that answers most questions, a deeper reasoning model for harder problems, and a real-time router" choosing between them, and said it planned "to integrate these capabilities into a single model." Since then, reasoning is a `reasoning.effort` setting on one model rather than a model of its own. The `o`-series is in wind-down with published shutdown dates.

## What is disclosed, by generation

The break is sharp enough to tabulate, and the early rows are why the wiki's architecture pages can cite real numbers:

| Generation | Disclosure |
| --- | --- |
| GPT-1 (2018) | Full architecture in the paper: 12 layers, 768-wide, 12 heads, 512-token context. No parameter count published — the familiar 117M is computed from the released weight shapes. |
| GPT-2 (2019) | Full architecture, four sizes, **weights released**. |
| GPT-3 (2020) | Full architecture, eight sizes up to 175 billion parameters, 96 layers, 12288-wide, 2048-token context, 300 billion training tokens. Weights never released. |
| GPT-3.5 | No paper, no architecture disclosure of any kind. |
| GPT-4 onward | Explicitly withheld, per the quotation above. |
| `gpt-oss` (2025) | Full architecture, **weights released** under Apache 2.0. |

A caution for anyone citing GPT-2's sizes: **the paper's numbers are wrong and OpenAI retracted them.** The paper's table says 117M / 345M / 762M / 1542M; the repository `README` says "our original parameter counts were wrong due to an error (in our previous blog posts and paper)" and gives 124M / 355M / 774M / 1558M. The corrected figures are exact and reproducible from the public configuration files. The paper's 117M was GPT-1's count carried across on the claim that the smallest model matched the original GPT — but GPT-2 small has a larger vocabulary and twice the context, so it is genuinely bigger.

**The widely repeated claim that GPT-4 is a roughly 1.8-trillion-parameter [mixture of experts](/wiki/ai/llm/mixture-of-experts) has no primary source.** It traces to a paywalled analyst post and remarks attributed to one person, and it is contradicted in spirit by the only official statement on the subject, which is a refusal to comment. The same goes for GPT-4's training compute and dataset size.

### gpt-oss, the exception

In August 2025 OpenAI released two open-weight models under Apache 2.0, with a model card describing the architecture completely — layer counts, expert counts, routing width, attention configuration and quantisation format. They are the only current view inside an OpenAI model, and they are covered on their own page: **[gpt-oss](/wiki/ai/models/openai/gpt-oss)**.

Neither is served through OpenAI's own API.

## Reasoning, and why the chain of thought is hidden

OpenAI's reasoning models are, in its own words, "trained with large-scale reinforcement learning to reason using chain of thought" — the model produces a long internal working-out before answering, and training teaches it to "refine their thinking process, try different strategies, and recognize their mistakes." That sentence has survived nearly verbatim from the o1 system card through to GPT-6 Astra.

The raw working-out is not shown. OpenAI's stated reasoning weighs three things at once: "After weighing multiple factors including user experience, competitive advantage, and the option to pursue the chain of thought monitoring, we have decided not to show the raw chains of thought to users." Users get a model-written summary instead.

The monitoring argument is the interesting half, and OpenAI states its own caveat rather than burying it. The o1 system card argues that latent thinking has previously been available only as "large blocks of illegible numbers," whereas chains of thought "are far more legible by default and could allow us to monitor our models for far more complex behavior" — then adds the condition in the same sentence: *"if they accurately reflect the model's thinking, an open research question."* Later cards escalate this into measured properties, including a named failure mode where a model reasons about how it will be graded rather than about the task.

## The corporate structure

OpenAI began in 2015 as a nonprofit with a $1 billion funding pledge and Sam Altman and Elon Musk as co-chairs. In 2019 it created a capped-profit entity inside the nonprofit, in which early investors' returns were capped at 100 times their investment and anything beyond that belonged to the nonprofit. The stated reason was that scaling language models needed far more capital than donations could supply.

The conversion that followed is easy to get backwards. A December 2024 proposal would have loosened nonprofit control. After what OpenAI described as "constructive dialogue with the offices of the Attorney General of Delaware and the Attorney General of California," a **revised** plan in May 2025 restored it: "OpenAI was founded as a nonprofit and is today overseen and controlled by that nonprofit. Going forward, it will continue to be overseen and controlled by that nonprofit."

The recapitalisation completed on 28 October 2025. The nonprofit, renamed the **OpenAI Foundation**, controls the for-profit **OpenAI Group PBC**, a Delaware public benefit corporation, through a share class giving it the sole power to appoint and remove the company's directors. A memorandum of understanding with California's Attorney General makes the control concrete: the company's charter requires its board to "consider only the Mission (and may not consider the pecuniary interests of stockholders or any other interest) in respect of safety and security issues," and the Safety and Security Committee sits at the *nonprofit*, with authority "to require mitigation measures—up to and including halting the release of models or AI systems."

Two figures are widely misreported. Microsoft's investment is usually given as $10 billion; Microsoft's own announcement named no figure at all, and its annual report for the 2026 fiscal year states **$13.0 billion committed, $11.9 billion funded**. And the Foundation's stake is usually given as 26%, which was its value at close in October 2025 — Microsoft's own holding fell from 27% to 25% over the following months through dilution, so the Foundation's current share is not 26% either, and OpenAI has not restated it.

**Azure exclusivity ended on 27 April 2026.** OpenAI "can now serve all its products to customers across any cloud provider," and Microsoft's intellectual property licence became non-exclusive. This reversed a position both companies had restated as recently as that February, so the two should be read as a sequence rather than as concurrent terms.

Elon Musk's suit seeking to unwind the restructuring was decided against him on 18 May 2026 — on the statute of limitations, a procedural ground rather than a finding that the conversion was proper. It is under appeal.

## Two things about the interface that are not obvious

**The million-token context has a pricing boundary inside it.** Prompts above 272,000 input tokens are billed at twice the input rate and 1.5 times the output rate *for the whole session*. That is why a model can advertise both a million-token window and a lower "max input tokens" figure: the 272,000 line is a price change, not a capacity limit. [Context length](/wiki/ai/llm/context-length) covers why long contexts cost what they do.

**Cache writes became billable at GPT-5.6.** Earlier models charged nothing to write a cache entry; from GPT-5.6 a write costs 1.25 times the uncached input rate. For an agent loop that rebuilds its prefix often, that changes the arithmetic in [prompt caching](/wiki/ai/prompt-caching).

## Status

Checked 11 September 2026. OpenAI's [model catalogue](https://developers.openai.com/api/docs/models) and [pricing page](https://developers.openai.com/api/docs/pricing) are the live sources; the [deprecations page](https://developers.openai.com/api/docs/deprecations) carries shutdown dates.

**GPT-6 Astra**, released 3 September 2026, is the current generation — one week old at the time of writing. The **GPT-5.6** generation (Sol, Terra, Luna), released 9 July 2026, remains fully supported. Both offer a 1,050,000-token context window, take text and images and return text, and expose reasoning effort from `low` to `max`.

Prices on this lineup are unusually unstable and should be read from the source rather than from anywhere else: GPT-5.6 Sol's current rate is explicitly promotional, and Luna now sells for a fifth of its launch price.

Worth knowing about the wider catalogue: **Sora and the video interface were deprecated with no replacement**, shutting down 24 September 2026. Whisper is retired. The embedding models have not changed generation since 2024. A cybersecurity line and a life-sciences model are gated behind approval programmes rather than generally available.

## Sources

- OpenAI, [GPT-4 Technical Report](https://arxiv.org/abs/2303.08774), arXiv:2303.08774 (2023) — the disclosure statement
- Radford et al., [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) (2019) — GPT-2
- Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165), arXiv:2005.14165 (2020) — GPT-3
- Kaplan et al., [Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361), arXiv:2001.08361 (2020)
- Ouyang et al., [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155), arXiv:2203.02155 (2022) — InstructGPT
- OpenAI, [gpt-oss-120b & gpt-oss-20b Model Card](https://arxiv.org/abs/2508.10925), arXiv:2508.10925 (2025)
- OpenAI, [o1 System Card](https://cdn.openai.com/o1-system-card-20241205.pdf) (5 December 2024) — the chain-of-thought monitoring argument
- Guan et al., [Deliberative Alignment](https://arxiv.org/abs/2412.16339), arXiv:2412.16339 (2024)
- Korbak et al., [Chain of Thought Monitorability](https://arxiv.org/abs/2507.11473), arXiv:2507.11473 (2025)
- [Memorandum of understanding between OpenAI and the California Attorney General](https://oag.ca.gov/system/files/attachments/press-docs/Final%20Executed%20MOU%20Between%20OpenAI%20and%20California%20AG%20re%20Notice%20of%20Conditions%20of%20Non-Objection%20(10.27.2025)%20(Signed%20by%20OpenAI)%20(Signed%20by%20CA%20DOJ).pdf) (27 October 2025)
- Microsoft, [The next phase of the Microsoft–OpenAI partnership](https://blogs.microsoft.com/blog/2026/04/27/the-next-phase-of-the-microsoft-openai-partnership/) (27 April 2026)
