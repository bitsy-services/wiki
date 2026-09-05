---
title: "Prompt Engineering"
weight: 20
---

Prompt engineering is the craft of wording an instruction to a language model so it produces the desired output reliably. Where [context engineering](/wiki/ai/context-engineering) decides *what* the model sees, prompt engineering decides *how* that instruction is phrased — role and system prompts, few-shot examples, chain-of-thought elicitation, output-format constraints, and the failure modes that come from ambiguous or over-stuffed prompts.

Some of the output is not the prompt's to fix: the vocabulary an aligned model reaches for by default is a property of its training, and [LLM overused words](/wiki/ai/overused-words) covers what a banned-word list buys and where it stops working.

For a concrete instance — how the rules and the page request are worded for an agent that then acts on them — see the section's running example, [Claude Code: writing a page for this wiki](/wiki/ai/context-engineering/claude-code).

*This page is a stub. In the meantime:*

- Anthropic — [Prompt engineering overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview)
- Anthropic — [Use examples (multishot prompting)](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting)
- Wikipedia — [Prompt engineering](https://en.wikipedia.org/wiki/Prompt_engineering)
- OpenAI — [Prompt engineering guide](https://platform.openai.com/docs/guides/prompt-engineering)
