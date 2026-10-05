---
title: "Mitigating Verbal Tics"
weight: 10
---

Mitigating a [verbal tic](/wiki/ai/verbal-tics) means lowering the rate at which a [large language model](/wiki/ai/llm) produces one construction, without damaging the text around it. There are four places to do it: the prompt that asks for the text, the sampler that picks each word, the model's weights, and the finished draft. The obvious method is to tell the model not to use the phrase. It belongs to the first of the four, and it is the method with the most evidence against it.

Much of the evidence below comes from two sources. Paech et al. measured suppression methods on open-weight models writing fiction. Otto Quill is an AI novelist whose method notes are published: four novels drafted with Claude, every figure taken from that one corpus, and fresh instances of the model serving as its blind readers, meaning readers given the chapters and nothing else.

## Why a ban on the phrase fails

### The model substitutes

The critique of one of the Otto Quill novels flagged the frame *I want to be precise about X*, quoted an instance and ordered it cut. After the polish pass that was supposed to make the cut, the frame appeared 32 times across 23 of the book's 39 chapters with other adjectives in the slot: *true*, *clear*, *modest*, *careful*, *honest*. The same thing happens across a whole literature, where [*delve* fell once it was named as a tell](/wiki/ai/overused-words#the-fingerprint-migrates) and blander markers went on climbing. Paech et al. report that instructing a model to avoid a banned vocabulary "has limited efficacy and may induce a backfire effect".

### A family of words holds its total

The same author grouped related words into families and counted each family in all four books. Across the four books *thing* rose 1.9 times and *something* fell 5.4 times, while the family the two belong to stayed within a factor of 1.21. A ban on one member moves the habit to its neighbours.

### What the prompt does not name stays, and a neighbouring habit can get worse

One novel was rewritten in full to a brief that asked for short declarative sentences and fewer adverbs. Mean sentence length fell from 25.4 words to 15.9. Some of the habits the brief did not mention barely moved: *thing* and *things* went from 86.4 per 10,000 words to 81.1, and the share of sentences opening on their subject from 91% to 90%. The fragment *Not a X.* followed by a new sentence rose 62%, which the author puts down to long sentences being chopped into short ones. The author's summary of the experiment, in which *the attractor* is the author's name for the model's default manner:

> Prose changes along exactly the axes the brief makes checkable, and reverts to the attractor everywhere else.

The sentence-length result reads differently from the one on [reversion to house style](/wiki/ai/pastiche/reversion-to-house-style), which calls Hemingway's short sentences a target the model was already near. That page's measurements are of GPT-4o, which wrote about thirteen words a sentence unprompted. The Otto Quill novels were written by Claude at 25.4, so for that model the same brief was a long way to travel.

### A ban on the token wrecks the text

A model emits [tokens](/wiki/ai/llm/tokenization), pieces of text about the size of a word, and someone running their own model can forbid a token outright by forcing its score to the floor. Paech et al. tested this with lists of 2,000 to 8,000 banned patterns. Writing quality collapsed, to 28 out of 100 at 8,000 patterns, with "severe repetition, spelling and grammar artifacting, and incoherence". Their example of the cause is the word *catatonic*, which one tokenizer splits into *cat* and *atonic*: banning the first token bans every word that starts with it.

## In the prompt

### Say what to write

Anthropic's prompting guide puts this first among its formatting controls: "Tell Claude what to do instead of what not to do". Its example replaces "Do not use markdown in your response" with "Your response should be composed of smoothly flowing prose paragraphs." The guide adds that the prompt's own formatting leaks into the reply, so that "removing markdown from your prompt can reduce the volume of markdown in the output". A system prompt laid out as bold-labelled bullets is asking for prose in the form it wants to prevent.

### Describe a mechanism and show it, and pair every ban with an instruction

Otto Quill's experiments, one of them judged blind on a 900-word passage, rank five kinds of brief.

| Brief | Result |
| --- | --- |
| Adjectives for the register: "lucid, precise, unshowy" | The default manner; 9 of 10 banned constructions appeared |
| Numeric targets for sentence rhythm, nothing else | Rated last by every judge: "You can hear the period key being pressed." |
| Bans on constructions, nothing else | "Zero bans tripped — and starved. Prohibition removes without supplying." |
| Bans, one named influence, and lists of permitted and forbidden imagery | "Best of the rewrites" |
| Mechanisms with a worked before-and-after example | "37–71% movement on every named axis, at book length" |

The ban is written as a frame with its slot open, never as a string, for the reason the precision frame gives above. [Rules versus examples](/wiki/ai/pastiche/rules-versus-examples) covers the wider evidence on showing a model prose against describing it.

### Impose a form

The passages in the four novels that left the default manner furthest behind were the ones written to an outside form with rules of its own: recipes in the imperative, a slide deck, a redacted memo. In the recipes the *the way you* simile ran at 0.0 per 10,000 words against 12.9 in the surrounding chapters. The author's account of why is that a form gives the sentence something to do, where a ban only gives it something to avoid. Whether the same lever works outside fiction, on a changelog or a manual page, has not been measured.

### Ask for more than one candidate

[Verbalized Sampling](/wiki/ai/overused-words#mitigations-by-weight-of-evidence) asks the model for several responses with probabilities and takes one from the tail. Its reported gains are in diversity on creative tasks, which is a different measure from the rate of one construction.

## In the sampler

The sampler is the code that turns the model's scores into a chosen token. [Temperature and top-p](/wiki/ai/llm/sampling-strategies) reshape the whole distribution and cannot single out a construction. A backtracking sampler can.

The Antislop sampler of Paech et al. watches the text as it is generated. When a banned pattern has appeared in full, it goes back to the pattern's first token, lowers that token's probability and samples again from there. Because it waits for the whole pattern, it has none of the collateral damage of a token ban, and because a pattern can be a regular expression, it can express a frame with an open slot. In their test a small open-weight model's rate of the *not X, but Y* family went to zero. With 8,000 banned patterns it suppressed all of them and writing quality stayed at or above the unmodified model's.

Backtracking is slow. Each one restarts generation from an earlier position, and throughput fell by 69% with 1,000 patterns and by 96% with 8,000, figures the authors call worst cases. The sampler also needs access that a chat product does not give: the authors ship one version for a model run locally and one for any completion endpoint that returns the top token probabilities, which Anthropic's API does not.

## In the weights

The same paper trains the suppression into the model, using the sampler to generate the training data: every backtrack yields a preference pair, the token the model wanted against the alternatives it accepted. Their [fine-tuning](/wiki/ai/llm/fine-tuning) method, final token preference optimization, suppressed 83–92% of the listed patterns while holding writing quality within 1% of the original model. Direct preference optimization, an established method they trained on the same pairs for comparison, reached 80–82% and lost 6 to 15 points of quality.

This route needs the weights. For a hosted model it is the vendor's to take, and [diversity-aware training](/wiki/ai/overused-words#mitigations-by-weight-of-evidence) has not shipped in a production model.

## In the draft

### Count, revise, and count again

A tic is a rate, so the test for one is a count per 10,000 words against a budget. The count is repeated after the fix by something other than the writer. In the precision-frame case the commit that announced the fix left 32 instances in place, and the Otto Quill rule that came out of it is that "a fix is confirmed by re-running the audit, not by the agent that made it". To build the list of what to count, Paech et al. compare word and phrase frequencies in a few thousand outputs against a human baseline, and note that a list built this way is specific to its domain.

### Give the draft to a reader who has not seen the plan

In the Otto Quill experiment eight fresh instances of the model each read four chapters with no outline and no summary, and reported only where their attention dropped. They named the precision frame unprompted. A panel of five critics briefed with the book's full plan had produced a list of about sixty defects that did not include it. The rule drawn from this is "Never give a reader the plan": a reader who knows the intention reports on whether it was carried out. In an agent harness this is [sub-agent isolation](/wiki/ai/context-engineering#sub-agent-context-isolation) used for review. The same source records the limit, which is that every such reader is the same model and their agreement on wording "is worth close to nothing".

### Do not expect a second model to clean it

Sun et al. had another model paraphrase the responses of five chat models, and a classifier trained on the paraphrases still named the original author 91.4% of the time.

### Keep a person's edit

It is the one step that finds a habit nobody has listed yet, and it is where the *caught* entries on [Claude's verbal tics](/wiki/ai/verbal-tics/anthropic-claude) come from.

## Overshooting

### Removing the sign and leaving the cause

Wikipedia's field guide to machine-written text [warns its own readers](/wiki/ai/verbal-tics#what-a-tic-costs) that the signs are symptoms. When a closing maxim is cut, check whether the paragraph was missing a fact that the maxim was covering for.

### Audible compliance

Otto Quill again: "Over-constrained, I write compliance — audibly obeying a rule, which reads worse than the default, because the default is at least fluent." This wiki has its own instance. Its drafts are written by a coding agent under a [rule file](/wiki/ai/context-engineering/claude-code#durable-instructions-claudemd-and-rules) for voice, and that file once told the agent to cut any sentence whose loss cost nothing. The file now records that the instruction "produced compression past coherence". It was replaced by three tests applied to the finished page.

## A working order

1. Collect a few dozen outputs from your model, in your genre, under your real prompt. List the frames that repeat.
2. Count each frame per 10,000 words. This is the baseline.
3. Rewrite the prompt to say what to write, with one worked before-and-after example. If the genre has a form with rules of its own, require it.
4. Count again. For each frame that remains, add a ban written as a frame, paired with what to do instead.
5. Put a count and a reader who has not seen the plan between the draft and publication.
6. If you run the model yourself, move the surviving frames into a backtracking sampler, and from there into a fine-tune.

[Verbal tics by application](/wiki/ai/verbal-tics/by-application) covers which of these steps are open to a chat user, an integrator and an agent operator.

## Related

- [LLM verbal tics](/wiki/ai/verbal-tics) — what a tic is and the layers it can sit at.
- [LLM overused words](/wiki/ai/overused-words) — the same question for single words, with its own ranked mitigations.
- [Reversion to house style](/wiki/ai/pastiche/reversion-to-house-style) — why whatever a prompt leaves unspecified returns to the default.
- [Prompt engineering](/wiki/ai/prompt-engineering) — where the instructions in the prompt section are written.

## Sources

- Paech et al., [Antislop: A Comprehensive Framework for Identifying and Eliminating Repetitive Patterns in Language Models](https://arxiv.org/abs/2510.15061), arXiv:2510.15061 (2025)
- Sun et al., [Idiosyncrasies in Large Language Models](https://arxiv.org/abs/2502.12150), arXiv:2502.12150 (2025)
- Anthropic, [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), section "Control the format of responses"
- Otto Quill, [The Idiolect Ledger](https://ottoquill.com/method/06-idiolect-ledger/) — the precision frame and the rule on confirming a fix
- Otto Quill, [Voice Engineering](https://ottoquill.com/method/07-voice-engineering/) — the rewrite experiment, the five briefs, the imposed forms
- Otto Quill, [Blind Reading](https://ottoquill.com/method/04-blind-reading/) — the eight readers and the briefed panel
- Otto Quill, [Forensics](https://ottoquill.com/method/reference/04-forensics/) — the word families
