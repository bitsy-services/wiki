---
title: "Anatomy of a Request"
weight: 5
---

A request to a chat model is a single sequence of [tokens](/wiki/ai/llm/tokenization), assembled by concatenation and processed front to back. What the user typed is the last and usually the smallest part. In front of it, in a fixed order, sit blocks written by other parties: role markers from the model's **chat template**, the format the model was trained to expect a conversation in; a **system prompt**, instructions from the vendor or the application; **tool definitions**, machine-generated descriptions of what the model may call; and the conversation's earlier messages. The model receives nothing else. There is no configuration channel beside the text, no state carried over from the previous request, and no initialization step before the first token: anything a vendor wants the model to treat as context is spliced into that one sequence, somewhere in front of the user's words.

Those vendor-written blocks are what "pre-prompt" informally names, and this page takes them apart in order: who writes each block, what it contains, which ones the user can see or change, and what the assembly costs. Whether the front of the sequence must be recomputed on every request — it need not be, and the reuse is exact — is [prompt caching](/wiki/ai/prompt-caching)'s subject.

## The parts, in order

On Anthropic's API the rendered order is fixed and [documented with its caching rules](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), because prompt caching depends on it: tool definitions first, then the system prompt, then the messages, oldest first, the newest last.

| Block | Written by | Changes |
| --- | --- | --- |
| Chat-template markers | the model builder, fixed at training time | never |
| Tool definitions | the application, generated from code | when the tool set changes |
| System prompt | the vendor or application | rarely — versioned like software |
| Earlier messages | both sides, accumulated | grows every turn |
| The newest message | the user | every request |

Reading down the table, each block changes more often than the one before it. That ordering is load-bearing: the front of the sequence is identical from request to request, which is what lets a provider reuse its computation, and [ordering stable content first](/wiki/ai/context-engineering#ordering-and-recency) is what keeps it identical.

## The chat template

A chat model's fine-tuning data is conversations serialized in one fixed textual format, with reserved tokens marking where each message starts, which role wrote it, and where the model's own reply should begin. That format is the model's chat template. ChatML, an early one, wraps every message in `<|im_start|>role` and `<|im_end|>` markers; Llama 2's wraps user turns in `[INST]` and `[/INST]`; each model family defines its own, and the Hugging Face `transformers` library ships every model's template beside its weights so that client code can render a message list without hand-building the markers ([chat templating documentation](https://huggingface.co/docs/transformers/chat_templating)).

Two things follow from the template being text. A role is a token, not a channel: nothing in the architecture treats an instruction marked `system` differently from the same words marked `user` — whatever extra weight system instructions carry was put there by fine-tuning on conversations where they carried it. And a [base model](/wiki/ai/llm#where-the-weights-come-from) — one that has only been trained to continue text, not fine-tuned on conversations — has no template at all, which is why prompting one means writing a document for it to continue rather than a message for it to answer.

## The system prompt

The system prompt is the block of instructions rendered ahead of the conversation. Who writes it depends on where the request comes from, and "the pre-prompt" usually means the second case:

- **A raw API call has no system prompt unless the developer supplies one.** The `system` parameter is optional and defaults to empty; Anthropic states that the prompts used in its consumer products do not apply to the API. What the API does add on its own: the chat template's markers always, and, when tool use is enabled, a vendor-written instruction block — a few hundred tokens teaching the tool-call format.
- **A consumer app carries a large vendor prompt.** claude.ai's runs to thousands of words and is published in [Anthropic's release notes](https://platform.claude.com/docs/en/release-notes/system-prompts); [xAI publishes Grok's](/wiki/ai/models/xai/grok-4-6). The current date rides in it, which is how a chat app answers "what day is it" from weights that finished training months ago.
- **A harness assembles one from layers.** [Claude Code](/wiki/ai/context-engineering/claude-code) combines its own system prompt, the generated tool definitions, and the user's durable instructions — with the `CLAUDE.md` cascade delivered as user-role context rather than folded into the system block.

## Tool definitions

Every tool the model may call is described inside the sequence: a name, a prose description, and a JSON Schema for its parameters, serialized as text ahead of the conversation. The descriptions are [present on every turn](/wiki/ai/context-engineering#the-context-budget) whether the turn uses them or not, and tools added by a [Model Context Protocol (MCP)](/wiki/ai/mcp) server are spliced in the same way, so a large tool surface is a per-turn tax on the whole session. There is no function-call machinery behind the prompt: the model emits a tool call as tokens in the format the template defines, the harness parses it, runs the tool, and appends the result to the sequence as another message.

## Assembled again on every request

The application programming interface (API) keeps no session state. Every request carries the whole conversation, and a "conversation" exists only because the client resends it each turn, one message longer. Processing the sequence grows with its length, so turn after turn the same opening tokens are paid for again; prompt caching stores the computation for the unchanged front and resumes after it. The other consequence of statelessness is that the client may rewrite history before resending it: [compaction](/wiki/ai/context-engineering#compaction-and-summarization) replaces old turns with a summary, at the price of invalidating the stored computation from the first changed token on.

## Baking the prompt into the weights

A block that is resent with every request forever can instead be trained in. **Context distillation** ([Askell et al. 2021](https://arxiv.org/abs/2112.00861)) fine-tunes the model to produce, without the prompt, the token probabilities it produces with the prompt — the training penalty is the Kullback-Leibler (KL) divergence, the standard measure of how far one probability distribution sits from another, between the two — and the paper used it to internalize an instruction prompt for a helpful, honest and harmless assistant. **Prefix tuning** ([Li & Liang 2021](https://arxiv.org/abs/2101.00190)) skips the text entirely: it trains, for a virtual prefix of ten to a few hundred positions, the per-layer [key and value vectors](/wiki/ai/llm/qkv-projections) a real prefix would have produced. The result acts on the model like a prompt but corresponds to no words.

The division of labour follows from what each side can change. Behaviour meant to hold for every user — the assistant persona, what gets refused — moves into the weights through [fine-tuning](/wiki/ai/llm/fine-tuning) and [reinforcement learning from human feedback (RLHF)](/wiki/ai/llm/rlhf). Anything that must change faster than a training run — the date, the product's features, the tool list — stays in the prompt, which can be edited and shipped the same afternoon.

## Related

- [Prompt caching & cost](/wiki/ai/prompt-caching) — how the unchanged front of the sequence is computed once and billed at a discount.
- [Context engineering](/wiki/ai/context-engineering) — managing what goes into the parts of the sequence the application controls.
- [Prompt engineering](/wiki/ai/prompt-engineering) — wording the instructions once they have a slot.
- [The KV cache](/wiki/ai/llm/kv-cache) — the per-token computation that request assembly feeds.

## Sources

- Askell et al., [A General Language Assistant as a Laboratory for Alignment](https://arxiv.org/abs/2112.00861), arXiv:2112.00861 (2021)
- Li & Liang, [Prefix-Tuning: Optimizing Continuous Prompts for Generation](https://arxiv.org/abs/2101.00190), arXiv:2101.00190 (2021)
- Anthropic, [System prompt release notes](https://platform.claude.com/docs/en/release-notes/system-prompts)
- Hugging Face, [Chat templates](https://huggingface.co/docs/transformers/chat_templating)
