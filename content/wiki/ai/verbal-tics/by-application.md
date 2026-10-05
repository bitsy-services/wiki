---
title: "Verbal Tics by Application"
weight: 20
---

Which [mitigation](/wiki/ai/verbal-tics/mitigation) for a [verbal tic](/wiki/ai/verbal-tics) is available depends on how much of the system around the [large language model](/wiki/ai/llm) a builder controls, and which tics are worth the effort depends on the kind of text being produced. A person typing into a chat app controls their own messages. An integrator calling a hosted model controls the [system prompt](/wiki/ai/context-engineering/anatomy-of-a-request), the standing instructions sent ahead of every conversation. Someone running a model whose weights are published controls the sampler and the weights as well.

## What each setting lets you reach

The mitigation page sorts methods by where they act: on the prompt, on the finished draft, on the sampler that picks each token, or on the model's weights. The settings differ in which of those four are open.

| Setting | Prompt | Draft | Sampler | Weights |
| --- | --- | --- | --- | --- |
| Chat app, as its user | your messages and any saved instructions | by hand | closed | closed |
| Hosted model, as an integrator | the system prompt and examples | by code | whatever parameters the vendor exposes | only where the vendor sells fine-tuning |
| Coding agent, as its operator | rule files loaded every session | scripts the harness runs, and reviewer subagents | as the hosted model behind it | as the hosted model behind it |
| Open weights, self-hosted | all of it | all of it | all of it | all of it |

The two measured methods that act below the prompt need more than a hosted chat model gives: the backtracking sampler needs the top token probabilities at each step, and the fine-tune built from it needs the weights. On a hosted model that returns no token probabilities, Anthropic's among them, the work is done in the prompt and on the draft.

## The vendor's fixes stay in the vendor's app

A vendor can instruct against a tic for all of its chat users with one line of system prompt, and Anthropic does. Its prompt for the Claude apps dated 28 May 2026 says "Claude avoids using "genuinely", "honestly", or "actually"", and [earlier prompts](/wiki/ai/verbal-tics/anthropic-claude#what-anthropics-prompts-name) ban the opening *Certainly!* and the opening compliment by name.

Anthropic's page of published prompts says they "do not apply to the Claude API". An integrator building on the same model starts with none of those lines and has to write its own. This wiki's pages are drafted through Claude Code, a separate product with a prompt of its own, and they use *genuinely* 52 times.

## Hosted models are closing the sampler

On Anthropic's current models the integrator's row has narrowed. The sampling parameters `temperature`, `top_p` and `top_k` [are rejected](/wiki/ai/models/anthropic/claude-opus-5#three-constraints-worth-knowing-before-porting-to-it) on Claude 4.7 and later unless left at their defaults.

A second control had already gone. A prefill is a partial reply supplied by the caller for the model to continue, and it was the usual way to suppress a reply's opening line: begin the reply yourself and the model cannot begin it with *Certainly!* Anthropic's prompting guide says that starting with the Claude 4.6 models a prefill on the last assistant turn returns an error. Its replacement advice for this case is an instruction in the system prompt, "Respond directly without preamble", and stripping in code whatever still gets through.

The backtracking sampler needs more access than either of those gave. It reads the top token probabilities at each step and resumes generation from an earlier position, so it runs against a model served locally or an endpoint that exposes both. Anthropic's Messages API reference lists no field for token probabilities.

## Which tics matter in which kind of text

Lists of tics do not transfer between genres. Paech et al. built theirs from fiction and say the method "is domain-specific; the over-used patterns in creative writing will differ from professional writing". Wikipedia's field guide says the reverse about itself: it "is less useful for texts which are not informational writing", and the tells of fiction "are not listed here".

| Kind of text | Tics that dominate | Where to act first |
| --- | --- | --- |
| Conversation: assistants, support | the first and last lines of a reply | the system prompt |
| Reference pages and reports | sentence constructions; bold labels and bullets | the prompt, then a count on the draft |
| Fiction | invented names and stock sensations; similes; how chapters open and close | a list kept outside the model, across books |
| Code and agent output | step narration, comments about the edit, the closing report | the harness's rule files and scripts |

### Conversation

The tics are at the edges of the turn, and they are the ones vendors already write prompt lines against. An integrator's system prompt needs the same lines. The rate is invisible in one reply and obvious across a day's support tickets, so the count has to be taken over a sample of conversations.

### Reference pages and reports

The tics are constructions: the negation followed by its correction, the dash before the payoff, the trailing *which is why*. The first two carry the highest counts of any construction on [Claude's list](/wiki/ai/verbal-tics/anthropic-claude#constructions) in this wiki's own pages. They respond to a count on the draft, because a document is long enough to have a rate.

### Fiction

The characteristic tics are content. Paech et al. found one character name 85,513 times more often in a model's stories than in human text. A model also starts each book with no memory of the last one, so the list has to live outside it. The Otto Quill novels were each drafted in a separate repository with a style sheet of its own, and a character named Priya appears in all four. The method that followed keeps one ledger for the author, and each new book inherits every ban from the book before.

### Code and agent output

The tics are in the prose around the code: a sentence announcing each step, a comment that describes the edit and says nothing about the code, a closing report with headers for a two-line change. No measurement of these was found for this page, and the entries for them on Claude's list are self-report. The levers are the ones an agent harness offers, described in the next section.

## Length decides what can be counted

A count per 10,000 words needs enough words. The Otto Quill ledger measured how similar two halves of the same book look by their function-word frequencies, the method of [stylometry](/wiki/cs/stylometry). The score was 0.9289 on 900-word samples, 0.9732 at 2,000 words and above 0.9931 past 15,000, so at short lengths the measure mostly reports sample size. Its advice for anything shorter than a book is to count constructions.

An application that produces short outputs, a chat reply or a commit message, has to pool them before counting. Paech et al. generate 2,000 samples per model and count across the pool.

## The running example: an agent writing this wiki

This wiki's pages are drafted by [Claude Code](/wiki/ai/context-engineering/claude-code), which makes it the operator row of the first table. Between the model and a published page there is a rule file, a gate script and a reviewer.

- **A rule file for voice**, loaded into every session. It acts on the prompt. It bans by description: components given intentions, importance announced ahead of the fact, superlatives without a measurement.
- **A gate script** that fails the build. It checks links, anchors, code fences, frontmatter and acronyms. It reads no prose.
- **A reviewer subagent** that reads the finished page in a fresh context, without the plan.

What gets past all three is on [Claude's list](/wiki/ai/verbal-tics/anthropic-claude): one em dash per 127 words of running prose, the *X, not Y* tail on 146 of 341 pages, *genuinely* on 43. None of the three mechanisms counts a construction. The rule file names habits and nothing measures them, which is the arrangement the Otto Quill notes describe in one line: "An unmeasured instruction is decoration."

## Related

- [Mitigating verbal tics](/wiki/ai/verbal-tics/mitigation) — the methods themselves and the evidence for each.
- [Claude's verbal tics](/wiki/ai/verbal-tics/anthropic-claude) — the list the examples on this page are drawn from.
- [Anatomy of a request](/wiki/ai/context-engineering/anatomy-of-a-request) — what a system prompt is and who writes each part of what the model receives.
- [Sampling strategies](/wiki/ai/llm/sampling-strategies) — temperature, top-k and top-p, on the models that still accept them.
- [Claude Code](/wiki/ai/context-engineering/claude-code) — rule files, hooks and subagents in the harness this wiki is written in.

## Sources

- Anthropic, [System prompts](https://platform.claude.com/docs/en/release-notes/system-prompts), release notes
- Anthropic, [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), section "Migrating away from prefilled responses"
- Anthropic, [Messages API reference](https://platform.claude.com/docs/en/api/messages), as read on 5 October 2026, for the absence of a token-probability field
- Paech et al., [Antislop: A Comprehensive Framework for Identifying and Eliminating Repetitive Patterns in Language Models](https://arxiv.org/abs/2510.15061), arXiv:2510.15061 (2025)
- Wikipedia, [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), WikiProject AI Cleanup, as read on 5 October 2026
- Otto Quill, [The Idiolect Ledger](https://ottoquill.com/method/06-idiolect-ledger/) — the inherited bans and the sample-length figures
- Otto Quill, [Forensics](https://ottoquill.com/method/reference/04-forensics/) — the name reused across four books
- Otto Quill, [Voice Engineering](https://ottoquill.com/method/07-voice-engineering/) — the line on unmeasured instructions
