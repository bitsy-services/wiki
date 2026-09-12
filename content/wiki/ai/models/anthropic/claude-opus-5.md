---
title: "Claude Opus 5"
weight: 10
---

Claude Opus 5 is the Opus-tier model of [Anthropic](/wiki/ai/models/anthropic)'s fifth Claude generation, released 24 July 2026 with the identifier `claude-opus-5`. Anthropic positions it for "complex agentic coding and enterprise work" and recommends it as the default starting point for most workloads — below the Fable tier in capability, above Sonnet in both capability and price.

**Nothing is published about how it is built.** No parameter count, no layer count, no hidden dimension, no attention scheme, no training compute, no indication of whether it is a [mixture of experts](/wiki/ai/llm/mixture-of-experts). Anthropic's transparency documentation lists those categories explicitly as not disclosed. What can be said about this model is what it does, what it costs to use, and what constraints it ships under — which is what this page covers.

## What "Opus tier" means

The Claude family is four tiers deep and the ordering is the only thing the names convey. Opus sits second from the top: **Fable**, then **Opus**, then **Sonnet**, then **Haiku**. Within a generation, moving up a tier buys capability and costs latency and money.

Opus 5's specific position is that it is the tier Anthropic points at for agentic work — long-running loops that call tools, read files and act over many turns, rather than single question-and-answer exchanges. That is a claim about what the model was trained and tuned toward, not a statement about its architecture, and the honest way to read it is as the vendor's own recommendation.

## Thinking is adaptive, and always somewhat on

Opus 5 uses Anthropic's **adaptive thinking**: rather than being given a fixed budget of reasoning tokens, the model decides how long to think, steered by an `effort` setting that runs `low`, `medium`, `high`, `xhigh`, `max`. The default is `high`.

This replaced the earlier mechanism, in which a caller set `budget_tokens` to a specific number. That older mode — now called **extended thinking** — is not accepted on Opus 5 at all. Code written against Claude 3.7 or Claude 4 that sets a thinking budget will fail here rather than degrade.

The reasoning itself is returned as a summary or omitted entirely, never raw. Some of it comes back as `redacted_thinking`: safety-redacted, encrypted, opaque to the caller, and required to be passed back unmodified on the next turn if the conversation continues.

## Three constraints worth knowing before porting to it

**Sampling parameters are rejected.** `temperature`, `top_p` and `top_k` return an error if set to anything but their defaults, on Claude 4.7 and later. [Sampling strategies](/wiki/ai/llm/sampling-strategies) explains what those knobs do on models that still accept them; here, they are gone.

**The tokenizer is not the old one.** Claude 4.7 introduced a tokenizer that produces roughly 30% more [tokens](/wiki/ai/llm/tokenization) for the same text. A million tokens is about 555,000 words on it, against roughly 750,000 on the previous one. Per-token prices are therefore not comparable across that boundary, and neither are context-window figures: the same document fills more of the window than it used to.

**Two knowledge cutoffs are published, and they differ.** Anthropic distinguishes a *reliable knowledge cutoff* — the date through which knowledge is most extensive — from a broader *training data cutoff*. For Opus 5 both are around May 2026, but on other models in the family they diverge by months, so the distinction is worth carrying.

## Text and images in, text out

Like every model in the current Claude lineup, Opus 5 accepts text and images and returns text. **There is no audio input, no audio output and no image generation** anywhere in the family. This is narrower than the Gemini or GPT lineups and is easy to assume wrongly.

## Safety constraints as shipped

Opus 5 runs under the same **AI Safety Level 3 (ASL-3)** protections first activated with Claude Opus 4 in May 2025: a targeted set of deployment measures aimed at chemical, biological, radiological and nuclear misuse, implemented through classifiers and monitoring, plus internal security controls intended to make the weights harder to steal.

When a classifier declines a request, the interface returns HTTP 200 with `stop_reason: "refusal"` rather than an error — a refusal is a successful response that happens to contain no answer. A `fallbacks` parameter can retry the same request on a different Claude model without a round trip, and a request refused before producing any output is not billed.

## Status

Checked 11 September 2026. Anthropic's [model overview](https://platform.claude.com/docs/en/about-claude/models/overview) is the live source for limits, prices and retirement dates.

Current Opus-tier model, released 24 July 2026. Context window 1M tokens, maximum output 128K synchronously and 300K through the batch interface. Anthropic commits to at least 60 days' notice before retirement and, for this model, to no retirement before 24 July 2027. Available through Anthropic's own interface, Amazon Bedrock, Google Cloud Vertex AI and Microsoft Foundry.

A **fast mode** is offered on this model and Opus 4.8 only, trading price for roughly 2.5 times the output token rate.

## Sources

- Anthropic, [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- Anthropic, [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) — the lifecycle and notice commitments
- Anthropic, [Extended thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) — adaptive thinking, redacted and preserved thinking blocks
- Anthropic, [Activating AI Safety Level 3 protections](https://www.anthropic.com/news/activating-asl3-protections) (22 May 2025)
- Anthropic, [Transparency Hub](https://www.anthropic.com/transparency) — the list of what is not disclosed
