---
title: "Prompt Caching & Cost"
weight: 30
---

When every request to a model starts with the same [tokens](/wiki/ai/llm/tokenization) — the same system prompt, the same tool definitions — the provider can run the model over that prefix once, store what the run produced, and start every later request where the prefix ends. What is stored is the prefix's [keys and values](/wiki/ai/llm/kv-cache): the per-token vectors that attention reads. Because [a token's keys and values depend only on the tokens before it](/wiki/ai/llm/causal-mask#what-it-buys-for-free-rows-are-final), the stored entries are the same numbers a fresh computation would produce — reuse is exact, not an approximation. Prompt caching is that reuse, sold: a cached input token is billed at a fraction of a fresh one, and for an agentic loop, whose every turn resends a long and mostly unchanged transcript, the cache is the difference between linear and quadratic spend over a session.

The stored computation is the **prefill**: the pass over the prompt that runs before the first output token appears. A cache hit skips the prefill for the covered prefix, so it cuts time-to-first-token as well as cost. What the prefix contains in the first place — tool definitions, then the system prompt, then the transcript — is [anatomy of a request](/wiki/ai/context-engineering/anatomy-of-a-request)'s subject.

## An exact prefix, or nothing

A cache entry is keyed on the exact bytes of the rendered prompt, and a request reuses it only for the longest stored prefix that matches byte for byte. One changed early token recomputes everything after it, for two mechanical reasons, each derived on its own page. First, every later token's keys and values [depend on the changed token](/wiki/ai/llm/kv-cache#why-its-safe-to-keep-them), so none of them can be kept. Second, position is baked into the stored vectors: under rotary position embedding (RoPE), a key is [rotated by its absolute position when it is first computed and stored already rotated](/wiki/ai/llm/rope-relative-invariance#fits-here), so even text that reappears verbatim at a different offset produces different keys — there is no salvaging a match that starts one token later.

The consequence for prompt layout: volatile content early is a standing cache miss. A current-date line at the top of a system prompt turns the first request of each day into a full re-prefill of everything below it; a per-request ID in the same place does it on every request. The practice that follows — [stable content first, volatile content last](/wiki/ai/context-engineering#ordering-and-recency) — is a context-engineering habit whose entire justification is this paragraph. For a concrete instance — why keeping `CLAUDE.md` and tool schemas stable at the front of the window makes a session cheap — see the section's running example, [Claude Code: writing a page for this wiki](/wiki/ai/context-engineering/claude-code).

A cache is also scoped to one model. The keys and values are what *that model's* weights compute; the same text run through different weights produces different numbers, so switching models mid-session forfeits the cache even when the transcript is identical.

## What the vendors sell

**Anthropic** caches at explicit breakpoints: `cache_control` markers, at most four per request, placed on content blocks. The prompt renders in the order tools, then system, then messages, so a marker on the last system block covers the tool definitions with it. An entry lives five minutes by default or one hour as a paid option, and a read refreshes the timer, so requests arriving inside the window keep an entry warm indefinitely. Writes are billed at a premium — 1.25× base input for the five-minute lifetime, 2× for the hour — and reads at roughly a tenth of base, varying by model. A prefix below a model-dependent minimum — on the order of a thousand tokens — silently doesn't cache at all ([Anthropic's documentation](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) carries the current numbers).

**OpenAI** caches automatically: no markers, any prompt of 1,024 tokens or more is eligible, and cached tokens are billed at a reduced per-model rate — up to 90% off. The mechanics have shifted between model generations: earlier models matched in 128-token increments and evicted entries after five to ten idle minutes, an hour after last use at most, while current ones keep a prefix reusable for thirty minutes after its last use and charge a write premium as Anthropic does ([OpenAI's guide](https://developers.openai.com/api/docs/guides/prompt-caching) carries the current rules).

**Self-hosted serving stacks** do the same without a bill. vLLM's automatic prefix caching reuses stored blocks across requests, and SGLang's RadixAttention ([Zheng et al. 2023](https://arxiv.org/abs/2312.07104)) keeps every live prefix in a radix tree — a tree whose branches are shared string prefixes — so a new request reuses the longest prefix *any* earlier request left behind, not just a designated one.

## The arithmetic of a hit

The five-minute entry pays for itself at the second request: a write plus one read costs 1.25× + 0.1× = 1.35× of base, against 2× for prefilling the prefix twice. The one-hour entry costs more to write than it saves on one read — 2× + 0.1× against 2× — and pays from the third request on; it exists for traffic whose gaps outlive the five-minute timer, not for steady loops.

The quadratic claim in the lede is the same arithmetic run over a session. An agent's turn *n* resends a transcript roughly *n* messages long, so an uncached session prefills 1 + 2 + … + *n* turns' worth of tokens — growth with the square of the session length. With a cache each token's prefill is paid about once, plus the read fee: linear. On a long session the ratio between those two curves, not the per-token discount, is what decides whether the loop is affordable.

## What caching does not save

Three costs survive a hit, all derived on [the KV cache page](/wiki/ai/llm/kv-cache):

- **Memory.** A restored entry [occupies the same accelerator memory](/wiki/ai/llm/kv-cache#the-price-is-memory-and-it-grows-with-the-conversation) as a recomputed one, for as long as the request runs.
- **Attention.** Every generated token [still attends to every cached row](/wiki/ai/llm/kv-cache#what-a-step-costs-once-you-have-it) — O(n) per output token, and no cache avoids it.
- **The window.** Cached tokens count against the [context length](/wiki/ai/llm/context-length) and [dilute attention](/wiki/ai/context-engineering#why-more-context-is-not-better) exactly as fresh ones do.

A 20,000-token system prompt served from cache is billed at a tenth and still costs full attention arithmetic on every token of every reply. Caching changes what a prefix costs to *load*, never what it costs to *carry*.

## A cache can be observed from outside

A hit returns faster than a miss, and that timing difference leaks. [Gu et al. (2025)](https://arxiv.org/abs/2502.07776) audited seventeen commercial APIs by timing probe prompts: eight providers were caching, and at seven of them — OpenAI among them, at audit time — entries were shared globally, so a probe returning fast revealed that *some other user* had recently sent the same prefix. Sharing a cache across customers is sharing a side channel. The major vendors now document scoping instead: Anthropic states that caches are never shared across organizations, and further isolates them per workspace on its own platform; OpenAI states the same at the organization boundary — trading some hit rate for not answering timing questions about other people's prompts.

## Beyond caching: batches and routing

Two other levers move the same bill. **Batching** trades latency for price: Anthropic's [Message Batches](https://platform.claude.com/docs/en/build-with-claude/batch-processing) and OpenAI's equivalent take a queue of requests with no interactive deadline at half price — OpenAI completes each batch within twenty-four hours, Anthropic finishes most within an hour and expires anything still unprocessed at the day mark without billing it. The discount buys the provider the right to schedule the work into idle capacity. **Routing** picks a cheaper model per request. It interacts badly with caching — caches are model-scoped, so a session that bounces between models re-prefills at every switch — and the honest metric is cost per completed task, not per request: a cheaper request that needs more turns to finish the job isn't cheaper. Which builders publish which prices is on the [model builder](/wiki/ai/models) pages.

## Related

- [Anatomy of a request](/wiki/ai/context-engineering/anatomy-of-a-request) — what the cached prefix actually contains, and who wrote it.
- [The KV cache](/wiki/ai/llm/kv-cache) — the stored object itself, and why keeping it is exact.
- [Context engineering](/wiki/ai/context-engineering) — the ordering discipline that keeps the prefix stable.
- [Agentic engineering](/wiki/ai/agentic-engineering) — where caching sits among an agent system's cost levers.

## Sources

- Anthropic — [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), [Message Batches](https://platform.claude.com/docs/en/build-with-claude/batch-processing), [Pricing](https://www.anthropic.com/pricing)
- OpenAI — [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
- Zheng et al., [SGLang: Efficient Execution of Structured Language Model Programs](https://arxiv.org/abs/2312.07104), arXiv:2312.07104 (2023)
- Gu et al., [Auditing Prompt Caching in Language Model APIs](https://arxiv.org/abs/2502.07776), arXiv:2502.07776 (2025)
