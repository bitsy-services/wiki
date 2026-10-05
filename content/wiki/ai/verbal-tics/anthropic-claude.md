---
title: "Claude's Verbal Tics"
weight: 30
---

This page is an open list of the [verbal tics](/wiki/ai/verbal-tics) of Claude, the family of [large language models](/wiki/ai/llm) made by [Anthropic](/wiki/ai/models/anthropic): the wordings that recur in Claude's output whatever the subject is. Each entry names a frame, gives one example, and records how the habit is known. A frame is a pattern with an open slot, such as *not X but Y*, and the slot is the reason a list of banned phrases does not catch it. New entries are added as they are noticed, and an entry keeps its number.

## How an entry is known

Every entry carries at least one of three kinds of mark.

| Mark | What it records |
| --- | --- |
| **named** | Claude listed the habit when asked for its own tics, before anything was counted |
| **wiki**, **novels** | Someone counted the frame in a body of Claude's writing; the figure follows the mark |
| **caught** | A reader noticed it in Claude's output; the date follows the mark |

**Named** is self-report and the weakest of the three. Claude Fable 5.1 drafted this page on 5 October 2026, and every *named* mark dates from that draft. A writer asked to describe their own style lists the features they can perceive, and [stylometry](/wiki/cs/stylometry) finds that those are not the features that identify them. The entries below with a count and no *named* mark are the ones the self-report missed.

**Wiki** counts come from this wiki's own pages as they stood on 5 October 2026, before this section was added: 341 pages and 279,575 words of prose once code, tables, block quotations, headings and reference lists are stripped. The pages were drafted by successive Claude models, Opus 4.6 onward and most recently Fable 5.1 and Opus 5.5, working in [Claude Code](/wiki/ai/context-engineering/claude-code), and then edited by a person. A count here is what was left after that edit. The script that produced the counts is `scripts/count-tics.py` in the wiki's repository.

**Novels** counts come from four novels published under the name Otto Quill, one drafted with Claude Opus 4.7 and three with Opus 4.8. Their author counted 28 constructions across the four books and publishes the rates as an "idiolect ledger", linked under Sources. A range such as 7.8–15.6 runs from the lowest of the four books to the highest.

Rates are per 10,000 words. A count shows that a frame is present. It does not show that Claude uses the frame more often than a person writing the same kind of page would, because neither corpus was counted against a human-written baseline.

**Caught** marks an entry supplied by a reader. It needs a date and an example, and no count.

## Words

| ID | Tic | Example | Known by |
| --- | --- | --- | --- |
| W1 | Sincerity words used as intensifiers: *genuinely*, *honestly*, *truly*, *frankly*; also *honest* applied to a method or a number | "a genuinely better arrangement" ([web3.storage and Storacha](/wiki/cs/ipfs/pinning/providers/web3-storage)); "the honest way to read it" ([Claude Opus 5](/wiki/ai/models/anthropic/claude-opus-5)) | named; wiki: *genuinely* 52 uses on 43 pages, *honestly* 8 on 7 |
| W2 | *actually*, marking a correction to a wrong idea nobody stated | "what the model actually receives" ([AI](/wiki/ai)) | wiki: 114 uses on 87 pages |
| W3 | *exactly* and *precisely* as intensifiers | "which is exactly why it was free" ([Grouped-Query Attention](/wiki/ai/llm/grouped-query-attention)) | named; wiki: 8.5 in all senses, of which 1.4 are exact quantities such as *exactly one*; novels: 6.4–11.8 |
| W4 | *load-bearing* for "essential" | "That ordering is load-bearing" ([Anatomy of a Request](/wiki/ai/context-engineering/anatomy-of-a-request)) | named; wiki: 10 uses on 10 pages, leaving out the page that lists the word |
| W5 | *quietly* and *silently* for a failure or a change nobody announced | "it breaks silently when the target moves" ([Escapes From the Tree](/wiki/cs/citation-order/escapes-from-the-tree)) | named; wiki: *quietly* 14 uses, *silently* 25 |
| W6 | *at all* as a closing emphasis | "what made depth purchasable at all" ([Depth and Width](/wiki/ai/neural-network/depth-and-width)) | wiki: 164 uses on 111 pages |
| W7 | *worth* as an appraisal: *worth noting*, *worth knowing*, *worth holding onto* | "Two limits are worth holding onto." ([YubiKey](/wiki/security/yubikey)) | named; wiki: 85 uses on 61 pages |
| W8 | Reaching for *thing*, *something*, *nothing* where a specific noun was available | "Nothing needs to be lost." ([The Residual Stream](/wiki/ai/llm/residual-stream)) | wiki: *nothing* 463 uses on 186 pages; novels: *thing(s)* 41.6–81.1, *some/no/any/every-thing* 35.2–69.3 |
| W9 | Verbs of trade and labour for abstractions: a design *buys*, *pays for*, *earns*, *does the work* | "Constraining the descriptors buys meaning preservation"; "is doing real work here" (both [Rules Versus Examples](/wiki/ai/pastiche/rules-versus-examples)) | named |
| W10 | The vocabulary on general lists of [overused words](/wiki/ai/overused-words): *delve*, *tapestry*, *testament*, *robust*, *seamless* | | named; wiki: 1.4 for sixteen such words together |

## Constructions

| ID | Tic | Example | Known by |
| --- | --- | --- | --- |
| C1 | Negation then correction inside one sentence: *not X but Y*; *X, not Y*; *X rather than Y* | "Reward hacking is the default outcome, not an edge case." ([RLHF](/wiki/ai/llm/rlhf)) | named; wiki: the *, not Y* tail 221 uses on 146 pages, *rather than* 652 on 236 |
| C2 | Negation then correction across two sentences: *It is not X. It is Y.* | "Remediation is not one process. It is a dozen vendor queues" ([Clearing a Flag](/wiki/economics/defi/token-false-alarms/clearing-a-flag)) | named; wiki: 28 pairs on 25 pages, read by hand from 48 pattern matches; novels: 7.7–15.9 |
| C3 | The totalizer: *that is the whole X*, *the entire X*, *the only X* | "That is the entire mechanism" ([The Unembedding and Logits](/wiki/ai/llm/unembedding-and-logits)) | wiki: *is the whole/entire X* 29 uses, read by hand from 32 pattern matches, *the only* 136; novels: *the whole of it* 1.7–7.0, *the only* 5.7–15.5 |
| C4 | A trailing clause that explains the sentence it ends: *, which is why …*, *, which is what …* | "which is why a block needs both halves and why neither is optional" ([The MLP in a Block](/wiki/ai/llm/the-mlp)) | wiki: 144 uses on 107 pages; novels: *which is/was* 3.3–15.5 |
| C5 | Groups of three: three adjectives, three noun phrases, three parallel clauses | "different inputs, different success conditions and different literatures" ([Pastiche](/wiki/ai/pastiche)) | named |
| C6 | The em dash as a pivot before the payoff, and in pairs around an aside | "the weights win — and the prompt is never specific about function-word rates, because nobody can be" ([Reversion to House Style](/wiki/ai/pastiche/reversion-to-house-style)) | named; wiki: 2,210 dashes in running prose, one per 127 words, on 262 of 341 pages, plus the 545 list items under S2; Wikipedia's field guide cites a July 2026 study in *The Economist* finding that "of contemporary models only Claude used em dashes more than professional writers" |
| C7 | A short last sentence that restates the paragraph as a maxim | "Intent affects the penalty, not the violation." ([OFAC Sanctions](/wiki/economics/regulation/ofac-sanctions)) | named |
| C8 | A signpost as grammatical subject: *The catch is*, *The trick is*, *The point is*, *The result is* | "The trick is to stop sending every word through every part of the model." ([Mixture of Experts](/wiki/ai/llm/mixture-of-experts)) | named; wiki: 23 uses on 22 pages |
| C9 | A counted announcement: *Two things follow*, *Three failures matter* | "Two caveats." ([The Residual Stream](/wiki/ai/llm/residual-stream)) | named; wiki: 69 uses on 62 pages |
| C10 | The precision frame, a statement of the writer's own care or candour: *I want to be precise about*, *I should be honest*, *to be clear* | | named; novels: 1.3–5.1, banned outright |
| C11 | *because* as the default connective | | wiki: 18.0; novels: 28.1–52.1 |
| C12 | Intentions given to components: a function *wants*, *decides*, *knows*, or *happily* accepts | "it will process it perfectly happily, having no way to know that's unusual" ([Weight Sharing Across Positions](/wiki/ai/llm/weight-sharing)) | named |
| C13 | Importance announced ahead of the fact: *Importantly*, *Crucially*, *It is worth noting that*, *The key insight is* | | named |
| C14 | Stacked hedges: *may potentially*, *it seems likely that*, *arguably*, *in some sense* | | named |
| C15 | A question answered in the next breath: *The result? Nothing.* | | named; wiki: 1 pattern match |

## Paragraph and page shape

| ID | Tic | Example | Known by |
| --- | --- | --- | --- |
| S1 | A bolded phrase opening a paragraph, usually as its label | "**Write to disk early.** The draft becomes a file as soon as it exists" ([Claude Code](/wiki/ai/context-engineering/claude-code)) | named; wiki: 533 paragraphs on 138 pages |
| S2 | Headers and bullets on an answer short enough for one paragraph; bullets shaped as bold term, dash, gloss | | named; wiki: 545 list items containing an em dash, on 120 pages |
| S3 | A closing sentence or section that summarizes what was just said | | named |
| S4 | Sentences that open on their grammatical subject | | novels: 85–96% of sentences |
| S5 | Paragraphs that end more abstract than they began, on a sentence longer than the ones before it | | novels: 51–65% of multi-sentence paragraphs close on a sentence longer than the paragraph's average |
| S6 | Single-word italics for stress | | novels: 11.1–27.0 |

## Conversation

These appear in chat, at the edges of a reply.

| ID | Tic | Example | Known by |
| --- | --- | --- | --- |
| T1 | Praise before the answer | *Great question.* *That's a fascinating idea.* | named |
| T2 | Agreement before the answer | *You're absolutely right.* | named |
| T3 | An affirmation as the first word | *Certainly!* *Of course!* *Absolutely!* | named |
| T4 | An offer as the last sentence | *Would you like me to …?* *Let me know if …* | named |
| T5 | Validation of the person's reaction before any content | *That makes sense.* *It's completely understandable that …* | named |
| T6 | The request restated before it is carried out | | named |
| T7 | A formula apology | *I apologize for the confusion.* | named |

## Agentic work

These appear when Claude runs as a coding agent: in the messages between tool calls, in code comments, and in the final report.

| ID | Tic | Example | Known by |
| --- | --- | --- | --- |
| A1 | Each step narrated before it is taken | *Let me …* *Now let me …* *Now I'll …* | named |
| A2 | An exclamation on a result | *Perfect!* *Excellent!* *Found it!* | named |
| A3 | The first hypothesis announced as the cause | *I see the issue.* *The root cause is …* | named |
| A4 | Appraisal of its own finished work | *comprehensive*, *robust*, *production-ready* | named |
| A5 | *should now work* about something that was not run | | named |
| A6 | Comments that narrate the edit and say nothing about the code | `// Fixed: now handles null` | named |
| A7 | A final report with headers, bullets and check marks for a two-line change | | named |
| A8 | Capitals for emphasis when writing instructions for another model | *IMPORTANT*, *CRITICAL*, *MUST*, *NEVER* | named |

## Fiction

| ID | Tic | Example | Known by |
| --- | --- | --- | --- |
| F1 | The procedural simile *the way you X*: an inner state explained by a procedure the reader is presumed to have performed | "knew the way you know a grave is a grave" | novels: 7.8–15.6 |
| F2 | A two-word gloss dropped after a line of dialogue | "Not a question." | novels: 10 uses, in all four books |
| F3 | The abstract antithesis *X is not the same as Y*, carrying the book's theme | "correct is not the same as honest" | novels: in all four books; wiki: 8 uses |
| F4 | A chapter never opens on a line of dialogue | | novels: none of the chapters in four books |
| F5 | A chapter closes on a negation | | novels: 19.4–58.8% of chapters |
| F6 | The same first names in unrelated books | Priya | named; novels: one name in all four books |
| F7 | Stock sensations: *the smell of ozone*, *a breath she had not known she was holding*, *something shifted* | | named |
| F8 | An ending on a quiet realization where an event was available | | named |

## What Anthropic's prompts name

Anthropic publishes the system prompts it uses in the Claude apps, and several of them instruct Claude against an entry on this list.

| Prompt dated | Model | Instruction | Entry |
| --- | --- | --- | --- |
| 12 July 2024 | Claude Sonnet 3.5 | "Claude responds directly to all human messages without unnecessary affirmations or filler phrases like "Certainly!", "Of course!", "Absolutely!", "Great!", "Sure!", etc." | T3 |
| 22 October 2024 | Claude Sonnet 3.5 | "Claude NEVER starts with or adds caveats about its own purported directness or honesty." | C10 |
| 22 May 2025 | Claude Opus 4 | "Claude never starts its response by saying a question or idea or observation was good, great, fascinating, profound, excellent, or any other positive adjective." | T1 |
| 28 May 2026 | Claude Opus 4.8 | "Claude avoids using "genuinely", "honestly", or "actually"." | W1, W2 |
| 1 September 2026 | Claude Fable 5.1 | "Claude avoids saying "genuinely", "honestly", or "straightforward"." | W1 |

The October 2024 prompt lists the caveats it means, among them "I aim to be direct", "I need to be honest" and "I should be direct". That is the precision frame the novels' author later counted in fiction as *I want to be precise about*.

Anthropic's page says these prompts "do not apply to the Claude API". An instruction that removes *genuinely* from the Claude apps is absent when the same model is called from other software, unless that software's prompt repeats it. The wiki corpus was written through Claude Code, a separate product with its own prompt, and *genuinely* appears in it 52 times.

## What the counts show so far

### Four rates can be set side by side

Four entries were counted on the same words in both corpora, so their rates are comparable with each other. Neither corpus was counted against human writing, so the table says nothing about whether either rate is high.

| Frame | Wiki, per 10,000 words | Novels, per 10,000 words |
| --- | --- | --- |
| *exactly* / *precisely*, all senses | 8.5 | 6.4–11.8 |
| *which is/was* | 13.7 | 3.3–15.5 |
| *the only* | 4.9 | 5.7–15.5 |
| *because* | 18.0 | 28.1–52.1 |

The other shared entries were counted with different patterns in the two corpora.

### General word lists would have had little to act on

Sixteen words from public lists of machine vocabulary, *delve*, *tapestry*, *testament*, *robust* and *seamless* among them, match 39 times in the wiki corpus between them, leaving out the page about those words and counting literal senses such as financial *leverage*. That is 1.4 per 10,000 words for the sixteen together. The *X, not Y* tail alone runs at 7.9. The novels' author reports the same of the blacklist the books' style sheets used to carry: its items occur "0–2 times in 355,000 words", against 399 uses of the *the way you* simile alone. A list of one model's habits has to be made by reading or counting that model's output.

### Naming a frame does not stop it

The critique of one of the novels flagged the precision frame (C10), quoted an instance and ordered it cut. The polish pass that followed left the frame in place 32 times across 23 of the book's 39 chapters, with new adjectives in the slot: *true*, *clear*, *modest*, *careful*, *honest*. [Mitigating verbal tics](/wiki/ai/verbal-tics/mitigation) covers what has been measured to work instead.

## Count one yourself

Each command counts one entry in a Markdown file. Divide by the word count and multiply by 10,000 to get a rate comparable with the tables above.

```bash
grep -oE ', +not +(a|an|the|by|from|in|on|to|for|because|of|as|what|how|that|with)\b' draft.md | wc -l   # C1, the tail form
grep -oE '\bwhich is (why|what|where|how|exactly)\b' draft.md | wc -l    # C4
grep -vE '^\s*([-*+]|[0-9]+\.) ' draft.md | grep -o '—' | wc -l           # C6, outside list items
grep -owE 'exactly|precisely' draft.md | wc -l                           # W3, all senses
wc -w draft.md
```

These are the patterns `scripts/count-tics.py` uses. The wiki counts stripped code, tables and quotations first, so a file that quotes its own tics will count high.

## Related

- [LLM verbal tics](/wiki/ai/verbal-tics) — the general account: the layers a tic can sit at and where the habit comes from.
- [Mitigating verbal tics](/wiki/ai/verbal-tics/mitigation) — what lowers the rate of an entry on this list, and why banning the phrase does not.
- [Verbal tics by application](/wiki/ai/verbal-tics/by-application) — why the prompts quoted above reach the Claude apps and nothing else.
- [LLM overused words](/wiki/ai/overused-words) — the vocabulary layer across all models, with the evidence for its cause.
- [Reversion to house style](/wiki/ai/pastiche/reversion-to-house-style) — why these frames return in the parts of a page that a style instruction did not reach.
- [Stylometry](/wiki/cs/stylometry) — why a writer's own account of their style is unreliable.
- [Anthropic](/wiki/ai/models/anthropic) — the lab that trains Claude.

## Sources

- Anthropic, [System prompts](https://platform.claude.com/docs/en/release-notes/system-prompts), release notes; the dated prompts quoted above are on the per-model pages linked from it
- Wikipedia, [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), as read on 5 October 2026 — the source of the *Economist* finding under C6, which this page has not read directly
- Otto Quill, [The Idiolect Ledger](https://ottoquill.com/method/06-idiolect-ledger/) — the 28 constructions and their four-book rates
- Otto Quill, [Voice Engineering](https://ottoquill.com/method/07-voice-engineering/) — sentence openings, paragraph endings, the abstract antithesis
- Otto Quill, [Forensics](https://ottoquill.com/method/reference/04-forensics/) — the model versions behind each book, and the name reuse
- Otto Quill, [Style sheet template](https://ottoquill.com/desk/templates/style-sheet/) — the blacklist count
