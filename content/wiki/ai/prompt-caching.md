---
title: "Prompt Caching & Cost"
weight: 30
---

Prompt caching lets a model reuse the processed form of a stable context prefix instead of recomputing it on every turn, turning the [context ordering](/wiki/ai/context-engineering) decisions — stable content first, volatile content last — directly into lower latency and spend. This page will cover token economics for agentic workloads: cache hit rate, what invalidates a cache, request batching, and model selection and routing.

*This page is a stub. In the meantime:*

- Anthropic — [Prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching)
- Anthropic — [Message Batches](https://docs.claude.com/en/docs/build-with-claude/batch-processing)
- Anthropic — [Pricing](https://www.anthropic.com/pricing)
