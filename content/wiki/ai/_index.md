---
title: "AI"
weight: 15
bookCollapseSection: true
---

Techniques for getting more out of AI coding agents and large language models — using them well, not building them. The emphasis is practitioner-facing: how to make a model running in a loop produce correct work reliably and economically.

The section shares one running example: **using [Claude Code](/wiki/ai/context-engineering/claude-code) to write a page for this wiki.** It is a real agentic workload over artifacts in this repository, so each topic below can point at the same concrete task instead of inventing a fresh hypothetical.

- [Context engineering](/wiki/ai/context-engineering) — managing what the model sees: the context budget, curation, compaction, sub-agent isolation, and the pitfalls that cause wrong actions.
  - [Claude Code](/wiki/ai/context-engineering/claude-code) — those techniques applied end-to-end in a real harness; the section's worked example.
- [Prompt engineering](/wiki/ai/prompt-engineering) — wording the instructions the model receives.
- [Prompt caching & cost](/wiki/ai/prompt-caching) — the token economics behind latency and spend.
- [Agentic workflows](/wiki/ai/agentic-workflows) — planning, tool use, delegation, and verification loops.
