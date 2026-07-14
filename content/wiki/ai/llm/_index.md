---
title: "LLM Internals"
weight: 80
bookCollapseSection: true
---

The rest of the [AI section](/wiki/ai) is about using a language model. This subsection is about what's happening inside one: what a token actually becomes, where that thing is kept, what each block does to it, and how a probability distribution falls out the far end. GPT-2 small is the reference implementation throughout — 12 blocks, `d_model` 768, small enough to load and poke at on a laptop.

## The contract

Every page here obeys the same rules, and they exist for the reader, not the writer:

- **One concept per page.** If two ideas need each other, they get two pages and a link.
- **Under 300 words.** Any page is three minutes. None of them teaches you everything about its subject; each teaches you the one thing it names.
- **At most one diagram**, drawn under a single [spatial convention](/wiki/ai/llm/conventions) that never varies from page to page.
- **Fixed vocabulary.** Terms are pinned in the [glossary](/wiki/ai/llm/glossary) and reused exactly. No synonyms for variety.
- **A falsifiable check.** Every page ends with a claim you can confirm or break yourself in nanoGPT or GPT-2 small. Reading about a transformer isn't the same as watching perplexity move when you delete a piece of one.

## Reading order

Start with [Conventions](/wiki/ai/llm/conventions) — it's short, and every diagram after it assumes you've read it. Keep the [Glossary](/wiki/ai/llm/glossary) open. Then the content pages, in dependency order: [tokenization](/wiki/ai/llm/tokenization), [embeddings](/wiki/ai/llm/embeddings), [the residual stream](/wiki/ai/llm/residual-stream). The [backlog](/wiki/ai/llm/backlog) is the full syllabus and the order it's being written in.

Two pages elsewhere in the wiki are this material seen from the outside: [prompt caching](/wiki/ai/prompt-caching) is the KV cache as it appears on an invoice, and [context engineering](/wiki/ai/context-engineering) is what you do for a living because attention costs O(n²).

## Wiki Pages

{{< section >}}
