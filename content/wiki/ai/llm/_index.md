---
title: "LLM Internals"
weight: 80
bookCollapseSection: true
---

The rest of the [AI section](/wiki/ai) is about using a language model. This subsection is about what happens inside one: what a token becomes, where it's kept, what each block does to it, and how a probability distribution falls out the far end. GPT-2 small is the reference throughout — 12 blocks, `d_model` 768, small enough to poke at on a laptop.

## The contract

The rules exist for the reader, not the writer:

- **One concept per page.** If two ideas need each other, they get two pages and a link.
- **Under 300 words.** Any page is three minutes. None of them teaches you everything about its subject; each teaches you the one thing it names.
- **At most one diagram**, drawn under a single [spatial convention](/wiki/ai/llm/conventions) that never varies from page to page.
- **Fixed vocabulary.** Terms are pinned in the [glossary](/wiki/ai/llm/glossary) and reused exactly. No synonyms for variety.
- **A falsifiable check.** Every page ends with a claim you can confirm or break in nanoGPT or GPT-2 small. Reading about a transformer isn't the same as watching perplexity move when you delete a piece of one.

## Reading order

Start with [Conventions](/wiki/ai/llm/conventions) — it's short, and every diagram after it assumes you've read it. Keep the [Glossary](/wiki/ai/llm/glossary) open. Then start at [tokenization](/wiki/ai/llm/tokenization) and follow each page's "leads to" links: they run in dependency order, from a string of text to a sampled token and out into training, scale, and inference tricks. The [backlog](/wiki/ai/llm/backlog) lists all 25 in that order.

Two pages elsewhere in the wiki are this material seen from the outside: [prompt caching](/wiki/ai/prompt-caching) is the KV cache as it appears on an invoice, and [context engineering](/wiki/ai/context-engineering) is what you do for a living because attention costs O(n²).

## Wiki Pages

{{< section >}}
