---
title: "Context Engineering"
weight: 10
bookCollapseSection: true
---

## What context engineering is

Prompt engineering asks "what do I say to the model?" Context engineering asks the broader question: "what is the complete set of tokens the model sees when it generates the next response, and how did each one get there?" For a single-shot chatbot prompt the two are nearly the same. For a coding agent — a model running in a loop, reading files, calling tools, and accumulating history over dozens of turns — they are different disciplines, and the second one dominates outcomes.

A coding agent's context window is a **finite, shared, and decaying** resource. Finite: every model has a hard token limit, and quality degrades well before that limit is reached. Shared: the system prompt, your instructions, the conversation history, tool definitions, tool outputs, and retrieved file contents all draw from the same budget. Decaying: a fact that was correct when it entered the window may be stale by the time the model relies on it. Context engineering is the practice of managing that resource deliberately rather than letting it fill by accident.

## The context budget

Everything the model attends to competes for the same window. In an agentic coding session the major consumers are, roughly in order of how fast they tend to grow:

- **Tool results** — file reads, command output, search hits, API responses. Almost always the largest and fastest-growing category, and the one most under your control.
- **Conversation history** — every prior user message, model response, and tool exchange, retained verbatim until it is summarized or evicted.
- **Instructions and memory** — the system prompt plus durable project guidance (a `CLAUDE.md`, rules files, persisted memories). Small per item, but permanent for the session.
- **Tool definitions** — the schema for every tool the agent can call, present on every turn whether used or not.
- **The active request** — the user's current message and the model's working response.

The practical consequence: a single careless `cat` of a 4,000-line generated file, or one unscoped log query, can consume more budget than the entire rest of the session and crowd out the information the model actually needs.

## Why more context is not better

The intuition that "giving the model everything relevant can't hurt" is wrong for three independent reasons:

1. **Attention dilutes.** Transformer attention is spread across all tokens (the mechanism itself is covered in [LLM internals](/wiki/ai/llm)). Doubling the irrelevant context does not leave the signal untouched — it lowers the relative weight the model can place on the tokens that matter.
2. **Position matters — the "lost in the middle" effect.** Models reliably attend best to the beginning and end of a long context and worst to the middle. A critical instruction buried in the middle of a 100-file dump is effectively weaker than the same instruction at the end.
3. **Cost and latency scale with tokens.** Every token in the window is reprocessed on every turn. Bloated context is not just lower quality; it is slower and more expensive turn after turn — which is why [prompt caching](/wiki/ai/prompt-caching) becomes essential at scale.

The goal is therefore not maximal context but the *smallest set of high-signal tokens that makes the next action correct*.

## Core techniques

### Curate, don't dump

Prefer the slice over the whole. Read the function you need, not the 2,000-line file it lives in. Use targeted search to locate code, then read narrowly around the hits. When a task requires sweeping many files to reach a single conclusion, delegate that sweep (see below) so the fan-out of file contents never enters the main window — only the conclusion does.

### Right-altitude instructions

Durable guidance — a project's `CLAUDE.md`, rules files, persisted memory — is the highest-leverage context because it is small and applies on every turn. It should sit at the right altitude: specific enough to change behavior ("use `SafeERC20`, not raw `transfer`"), general enough not to overfit to one task. Instructions that are too vague waste tokens without steering; instructions that encode one-off details pollute every future turn. This is the boundary between context engineering and [prompt engineering](/wiki/ai/prompt-engineering): the wording is prompt engineering; the decision about what earns a permanent slot in the window is context engineering.

### Compaction and summarization

When history approaches the window limit, it is summarized: older turns are compressed into a synopsis and the verbatim exchanges are dropped. This keeps the session alive but is lossy — detail that was not carried into the summary is gone. Two implications:

- **Put durable facts in memory, not chat.** A decision that must survive belongs in a memory file or a written artifact, not in a conversational aside that compaction may discard.
- **Front-load conclusions.** State outcomes explicitly ("the fix is X because Y") rather than leaving them implicit in a tool trace, so the summarizer has something concrete to keep.

### Sub-agent context isolation

A subagent runs with its own fresh context window and returns only its final message to the parent. This makes delegation the strongest single tool for context control: a search that would otherwise pour hundreds of file excerpts into the main window can run inside a subagent that reads all of them and returns one paragraph. The parent keeps the conclusion, not the dump. Use this for broad fan-out exploration; see [agentic workflows](/wiki/ai/agentic-workflows) for when delegation is and isn't worth the overhead.

### Just-in-time retrieval

There are two ways to get information into context: pre-load it (paste it into the prompt up front) or retrieve it on demand (give the agent tools to fetch it when needed). Pre-loading is simple and cache-friendly but fills the window with material that may never be used. Just-in-time retrieval keeps the baseline small and pulls only what each step requires, at the cost of extra round-trips and the risk of over-fetching per call. Agentic coding leans heavily on the second model — the file system is the external memory, and the agent reads into context only what the current step needs.

### Ordering and recency

Place stable, reusable content (system prompt, tool definitions, long-lived instructions) at the front, where it can be cached and where the model anchors well. Place the most task-relevant material — the current request, the file under edit, the latest tool result — near the end, where attention is strongest. Putting volatile content early both breaks [prompt caching](/wiki/ai/prompt-caching) and squanders the strongest attention positions on tokens that will soon be irrelevant.

### Tool-result hygiene

Because tool output is the dominant source of growth, disciplined tool use is the highest-yield habit:

- Scope queries to the rows or lines you need, not entire tables or logs.
- Paginate or range-limit large outputs instead of dumping them whole.
- Don't re-read a file you just wrote or edited — the change already happened; re-reading only to "verify" duplicates it in the window for no new information.
- Prefer a search that returns locations over one that returns full contents when you only need to know *where* something is.

## Pitfalls, by severity

Ordered worst-first — the early items cause wrong actions; the later ones only cause waste.

1. **Context poisoning.** A hallucinated or incorrect fact enters the window (a wrong function signature, an invented config key) and, because the model attends to its own prior output, is treated as ground truth and built upon. Errors compound across turns and the agent is now confidently wrong — the most dangerous failure. Mitigation: verify facts against the source before acting on them, and never let a guess get written into context as if it were checked.
2. **Stale context.** A file is read, then modified (by the agent, the user, or another process), and a later step reasons about the old contents. An edit is applied against a version that no longer exists. Mitigation: re-read after external changes, and trust the harness's file-state tracking rather than a remembered snapshot.
3. **Context clash.** Two instructions in the window contradict each other — an old plan versus a revised one, a rule versus an ad-hoc override. The model's reasoning degrades as it tries to satisfy both. Mitigation: when direction changes, state the supersession explicitly rather than leaving both versions live.
4. **Irrelevant bloat.** Unused file dumps, redundant tool output, and stale history dilute attention and inflate cost and latency. The least severe failure — the agent can still be correct — but the most pervasive, and the one good tool hygiene prevents outright.

## Practical checklist

- Read narrowly; search to locate, then read around the hit.
- Delegate broad fan-out to a subagent so only the conclusion returns.
- Scope every tool call to the smallest output that answers the question.
- Don't re-read what you just wrote.
- Put facts that must survive into memory or an artifact, not into chat.
- Keep stable content first (for caching and anchoring), task content last (for attention).
- When a fact entered the window as a guess, verify it before building on it.
- When direction changes, retire the old instruction explicitly.

## Worked example

Every technique above is abstract until it touches a real harness. [Claude Code](/wiki/ai/context-engineering/claude-code) applies all of them to one concrete task — producing a page for this wiki — and that task is the running example the rest of the [AI section](/wiki/ai) reuses. The page you are reading now was made by the workflow that page describes, which makes it the most direct way to see the budget, curation, compaction, sub-agent isolation, and pitfalls of this page operating on something you can inspect.

## Related

- [Claude Code](/wiki/ai/context-engineering/claude-code) — the techniques on this page applied end-to-end in a real agentic harness.
- [Prompt engineering](/wiki/ai/prompt-engineering) — wording the instructions that context engineering decides to include.
- [Prompt caching & cost](/wiki/ai/prompt-caching) — why context ordering and stability translate directly into latency and spend.
- [Agentic workflows](/wiki/ai/agentic-workflows) — delegation, planning, and verification loops that depend on disciplined context.

## Further reading

- Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Anthropic, [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices)
- Liu, Zhao, Shang & Shen, [Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems](https://arxiv.org/abs/2604.14228)
- Liu et al., [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)
