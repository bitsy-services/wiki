---
title: "Anthropic"
weight: 20
bookCollapseSection: true
---

Anthropic is an American public benefit corporation that trains the **Claude** family of large language models and sells access to them through an API rather than as downloadable files. Every Claude model is closed-weight. The company publishes an unusual amount about how its models are *governed* — a written constitution the models are trained against, a scaling policy that gates releases on capability evaluations, and a commitment to preserve the weights of retired models — and almost nothing about how they are *built*. No parameter count has ever been published for any Claude model.

One thing Anthropic originated has spread past it: the [Model Context Protocol (MCP)](/wiki/ai/mcp), open-sourced in November 2024, is now implemented by competing products and is the substrate under most agent tool surfaces. [Claude Code](/wiki/ai/context-engineering/claude-code), its agentic coding tool, has not spread in the same way, but it is the harness this wiki is written in.

## The company

Anthropic describes itself as "an AI safety and research company" and is structured as a public benefit corporation, a form that obliges directors to weigh a stated public purpose alongside shareholder returns. Dario Amodei and Daniela Amodei lead it.

Beyond that, the company page is silent: it states no founding year, no founder list, no headquarters and no headcount. The widely reported account — founded in January 2021 by seven people who left OpenAI, including the Amodei siblings, with Dario having been OpenAI's Vice President of Research — is not confirmed on any Anthropic-owned page. It is almost certainly correct, and it is worth noticing that a company this well documented on governance publishes no corporate history at all.

The funding is documented, and the trajectory is the fact worth carrying away. Anthropic raised a $30 billion Series G in February 2026 at a $380 billion valuation, then a $65 billion Series H on 28 May 2026 at **$965 billion** post-money. The company says run-rate revenue crossed $14 billion at the February round and **$47 billion** by May — a bit over three months later. Both figures are Anthropic's own, stated in its funding announcements and not independently audited.

Compute comes from other people's datacentres, and the arrangements are large enough to be strategic rather than commercial. The Series H announcement names 5 gigawatts of capacity from Amazon, 5 gigawatts of tensor processing unit (TPU) capacity from Google and Broadcom, and access to GPUs from SpaceX. Amazon is both an investor and a compute partner. Google appears in these announcements only as a compute partner, not an investor, though its earlier equity investments are widely reported.

## How Claude is tiered

There are four tiers, and the ordering is the only thing the naming conveys:

| Tier | Anthropic's description |
| --- | --- |
| **Fable** (and **Mythos**) | "For demanding reasoning and long-horizon agentic work" |
| **Opus** | "For complex agentic coding and enterprise work" |
| **Sonnet** | "The best combination of speed and intelligence" |
| **Haiku** | "The fastest model with near-frontier intelligence" |

**Anthropic has never published a rationale for any of these names.** The Claude 3 launch, which introduced Haiku/Sonnet/Opus in March 2024, says only that the family "includes three state-of-the-art models in ascending order of capability." No Anthropic publication explains why those particular words. The reading that they are poetic forms of increasing length is widespread, and it is not the vendor's; the same is true of Fable and Mythos, introduced in June 2026 with no stated etymology.

**Fable and Mythos are one tier, not two.** They are the same underlying model differing only in safeguards: Fable ships with safety classifiers that can decline a request, Mythos ships without them and is invitation-only through Project Glasswing, a cybersecurity programme for vetted defenders and life scientists. A page treating Mythos as a separate capability rung would be wrong.

### Model identifiers

The scheme changed at the 4.6 generation, and the intuition most people bring to it is the wrong one.

- **From 4.6 onward, identifiers carry no date**: `claude-opus-5`, `claude-fable-5-1`. A major release omits the minor segment.
- **Before 4.6, identifiers carried a snapshot date**: `claude-haiku-4-5-20251001`, with a short alias resolving to the most recent snapshot.

A dateless identifier is **not** an evergreen pointer to the current best model. Anthropic's docs address the misconception directly: the dateless identifier "maps to a single, fixed model snapshot," and "Anthropic does not update the weights or configuration of an existing model ID." What *can* change underneath a fixed identifier is the serving infrastructure — the request router, the safety classifiers, the sampling logic — which the docs note "produce minor differences in observable behavior even when the model ID and weights have not changed." Weights are frozen; the machinery around them is not.

## What Anthropic does not publish

Anthropic's Transparency Hub lists what is withheld, which makes the absence citable rather than merely conspicuous: **parameter counts, detailed architecture specifications, and training duration or computational cost** are all explicitly not disclosed.

What that leaves unknown for every Claude model: the number of layers, the hidden dimension, the attention head count, the positional-encoding scheme, the context-extension technique, the training compute in floating point operations (FLOPs), and whether any Claude model is a [mixture of experts](/wiki/ai/llm/mixture-of-experts). Any parameter count circulating for a Claude model is third-party estimation.

What *is* disclosed is the shape of the training data and the toolchain. Training uses "a proprietary mix of publicly available information from the Internet, public and private datasets, and synthetic data generated by other models," plus licensed third-party data, paid contractors, and data from users who opted in. Infrastructure is Amazon Web Services, Google Cloud and Microsoft Azure, with PyTorch, JAX and Triton. Models undergo "substantial post-training" aimed at aligning behaviour with Claude's constitution.

How some of that data was obtained has been litigated. In *Bartz v. Anthropic*, Judge Alsup held in June 2025 that training on lawfully acquired books was "quintessentially transformative" and fair use, while downloading and retaining pirated copies was not. The case settled for a minimum of $1.5 billion, with final judgment entered on 20 July 2026. [Law and ethics](/wiki/ai/pastiche/law-and-ethics) covers what the holding does and does not settle.

That the models are transformers is a safe inference — Anthropic's own interpretability papers analyse them in terms of [residual streams](/wiki/ai/llm/residual-stream), [attention heads](/wiki/ai/llm/one-attention-head) and [MLP layers](/wiki/ai/llm/the-mlp) — but it is inference from the research literature, not an architecture statement.

## What is distinctive

**Constitutional AI.** Rather than training harmlessness from human labels on harmful outputs, Anthropic trains it from AI feedback against a written document. Claude's constitution was published in January 2026 under a Creative Commons CC0 public-domain dedication, and is used at several stages of training — including by Claude itself, to generate synthetic conversations and response rankings. This is a different mechanism from [reinforcement learning from human feedback (RLHF)](/wiki/ai/llm/rlhf), though Anthropic uses both.

**The Responsible Scaling Policy.** A published, versioned document that ties deployment to capability evaluations through AI Safety Levels (ASL). The consequence is concrete rather than aspirational: the ASL-3 standard was activated on 22 May 2025 with Claude Opus 4, imposing a targeted set of deployment measures aimed at chemical, biological, radiological and nuclear misuse, and over a hundred internal security controls intended to make model weights harder to steal.

**Weight preservation.** Anthropic commits to preserving the weights of every publicly released model for at least the lifetime of the company, and to publishing post-deployment reports that include *recorded interviews with the deprecated model* about its development and its preferences regarding future deployment. The docs state the reasoning plainly, including that "model retirement introduces safety- and model welfare-related risks." No other lab in this section does this.

**Adaptive thinking.** Anthropic moved from a manual reasoning-token budget to a model-decided one, steered by an `effort` setting from `low` to `max`. On the top tier the raw chain of thought is never returned: a request can ask for a readable summary, or get thinking blocks with the content omitted. Some reasoning comes back as `redacted_thinking` — safety-redacted, opaque, encrypted, and required to be passed back unchanged.

**Refusal as a success status.** When a classifier declines a request, the API returns HTTP 200 with `stop_reason: "refusal"` rather than an error, and a `fallbacks` parameter can retry the request on another Claude model without a round trip. A refused request generates no bill if it produced no output.

**Prompt caching**, where Anthropic's version is aggressive enough to change what agent loops cost. A cache read costs a fraction of a fresh input token — an order of magnitude less, and on the top tier considerably more than that — which is why re-sending a large unchanged prefix every turn is affordable at all. [Prompt caching](/wiki/ai/prompt-caching) covers the mechanism and its economics.

## Two things the spec sheet does not tell you

**The tokenizer changed at Opus 4.7**, and produces roughly 30% more tokens for the same text. Per-token prices are therefore not comparable across that boundary: the docs put a million tokens at about 555,000 words on the current tokenizer against roughly 750,000 on the previous one. A model that looks like it costs the same per token costs about a third more per page.

**Two knowledge cutoffs are published per model**, and they differ. The "reliable knowledge cutoff" is the date through which knowledge is most extensive; the "training data cutoff" covers a broader and later range of data. For Claude Haiku 4.5 those are February 2025 and July 2025 respectively.

## The Fable 5 suspension

On 12 June 2026 the United States government applied export controls to Claude Fable 5 and Mythos 5, three days after their release. Amazon researchers had found a way to bypass Fable 5's safeguards such that the model could identify software vulnerabilities and, in one case, produce code demonstrating how one could be exploited. The controls required restricting access by nationality; Anthropic had no way to verify nationality in real time, and so **suspended access for every user**. The controls were lifted on 30 June and the model returned globally on 1 July.

Anthropic trained a classifier against the reported bypass, reporting a block rate above 99% for that specific method, and says the episode led it to work with Amazon, Microsoft and Google on a shared framework for assessing jailbreak severity. It is the clearest case so far of a frontier model being withdrawn from general availability by government action rather than commercial choice.

## Status

Checked 11 September 2026. Anthropic's [model overview](https://platform.claude.com/docs/en/about-claude/models/overview) and [pricing page](https://platform.claude.com/docs/en/about-claude/pricing) are the live sources for context limits, prices and retirement dates.

| Model | Identifier | Released | Context | Tier |
| --- | --- | --- | --- | --- |
| Claude Fable 5.1 | `claude-fable-5-1` | 1 Sep 2026 | 1M | Fable |
| Claude Mythos 5.1 | `claude-mythos-5-1` | 1 Sep 2026 | 1M | Fable, invite only |
| Claude Opus 5 | `claude-opus-5` | 24 Jul 2026 | 1M | Opus |
| Claude Sonnet 5 | `claude-sonnet-5` | 30 Jun 2026 | 1M | Sonnet |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | 15 Oct 2025 | 200K | Haiku |

Earlier releases from Claude Opus 4.5 forward remain available and are marked legacy. Two properties hold across the whole current lineup and are easy to assume wrongly:

- **Every model is text and images in, text out.** There is no audio input, no audio output and no image generation anywhere in the family.
- **`temperature`, `top_p` and `top_k` are rejected** on Claude 4.7 and later, returning an error if set to a non-default value. [Sampling strategies](/wiki/ai/llm/sampling-strategies) explains what those parameters do on models that still accept them.

Models are served through Anthropic's own API, Amazon Bedrock, Google Cloud Vertex AI and Microsoft Foundry. Retirement carries at least 60 days' notice on Anthropic-operated platforms; the resellers set their own dates.

## Sources

- Anthropic, [Company](https://www.anthropic.com/company) and [Transparency Hub](https://www.anthropic.com/transparency)
- Anthropic, [Series H funding announcement](https://www.anthropic.com/news/series-h) (28 May 2026)
- Anthropic, [Introducing the next generation of Claude](https://www.anthropic.com/news/claude-3-family) (4 March 2024) — the ascending-order statement
- Anthropic, [Claude's new constitution](https://www.anthropic.com/news/claude-new-constitution) (22 January 2026)
- Bai et al., [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073), arXiv:2212.08073 (2022)
- Anthropic, [Responsible Scaling Policy](https://www.anthropic.com/responsible-scaling-policy) and [Activating AI Safety Level 3 protections](https://www.anthropic.com/news/activating-asl3-protections) (22 May 2025)
- Anthropic, [Commitments on model deprecation and preservation](https://www.anthropic.com/research/deprecation-commitments) (4 November 2025)
- Anthropic, [Redeploying Claude Fable 5](https://www.anthropic.com/news/redeploying-fable-5) (June 2026)
- Anthropic, [Model IDs and versions](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions) and [model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)
- Anthropic, [Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) (25 November 2024)
