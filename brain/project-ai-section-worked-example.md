---
name: project-ai-section-worked-example
description: The AI section shares one running example; reuse it instead of inventing new hypotheticals
metadata:
  type: project
---

The `content/wiki/ai/` section deliberately shares a single running example: **using Claude Code to write a page for this wiki**, documented in full at `content/wiki/ai/context-engineering/claude-code.md`. `context-engineering` is a section (`_index.md` with `bookCollapseSection: true`); Claude Code is its child page. The `_index.md`, `agentic-workflows.md`, and the `prompt-engineering`/`prompt-caching` stubs all point at this one example.

**Why:** the user asked for the wiki-page-creation use case to be the practical example reused across other AI-section topics, so each page grounds abstract technique in the same inspectable, in-repo task rather than a fresh invented scenario.

**How to apply:** when writing or expanding any `content/wiki/ai/` page (including filling in the prompt-engineering / prompt-caching stubs), instantiate concepts against this same Claude-Code-writes-a-wiki-page task and link to [[]] `/wiki/ai/context-engineering/claude-code`. Do not introduce a competing worked example. Preserve the `/wiki/ai/context-engineering` URL and its `#sub-agent-context-isolation` etc. anchors — other pages deep-link to them.
