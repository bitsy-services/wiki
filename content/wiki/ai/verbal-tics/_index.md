---
title: "LLM Verbal Tics"
weight: 26
bookCollapseSection: true
---

A verbal tic, in the output of a [large language model](/wiki/ai/llm), is a wording that recurs at a rate the content does not explain: a word, a sentence pattern, a paragraph shape or a way of opening a reply that the model produces whatever it was asked to write. *It's not X, it's Y* is one. So is a paragraph that ends by restating itself, a reply that begins *Certainly!*, and a character named Elara. Each is unremarkable once, and what makes it a tic is how often it comes back.

This section covers the tics above the level of the single word, what lowers their rate, and one model's list. The single words have a page of their own at [LLM overused words](/wiki/ai/overused-words), and the attempt to replace a model's manner wholesale with a named author's is [pastiche](/wiki/ai/pastiche).

## Where a tic can sit

| Layer | What repeats | Examples |
| --- | --- | --- |
| Word | a single word or fixed phrase | *delve*, *tapestry*, *a testament to* |
| Construction | a sentence pattern with open slots | *It's not X, it's Y*; three items in a row; a dash before the payoff |
| Shape | the form of a paragraph or a page | a bold label on every paragraph, bullets for everything, a closing summary |
| Turn | the first and last lines of a reply | *Certainly!*, *You're absolutely right!*, *Would you like me to …?* |
| Content | invented material | the same character names, the same sensory details |

### Constructions

Reinhart et al. gave six models a 500-word chunk from each of several thousand human-written texts and asked for 500 more "in the same style, tone, and diction", then compared the result with the human's next 500 words. GPT-4o used present participial clauses, the *-ing* phrase hung on the end of a sentence, at 5.3 times the human rate. Their example has two: "Bryan, leaning on his agility, dances around the ring, evading Show's heavy blows." It used nominalizations, nouns made from verbs or adjectives such as *development*, at 2.1 times the human rate. The models had been shown the target style and asked to match it.

Paech et al. counted the sentence form *It's not X, it's Y* at 6.3 times its rate in human writing in some models. Wikipedia's editors keep a field guide to the signs of machine-written text. It lists the same form under "negative parallelisms" and has further entries for the "rule of three" and for overuse of the em dash. As of September 2026 the em dash entry carries a note that the sign "seems to be less common in current LLM output", records that some vendors have tried to suppress it, and adds that a July 2026 study in *The Economist* "found that of contemporary models only Claude used em dashes more than professional writers, and ChatGPT used them less."

### Shape and turn

Sun et al. trained a classifier on nothing but the Markdown elements of each response, with the text replaced by placeholders. It still named the right chat model out of five 73.1% of the time. In their sample ChatGPT put key points in bold under headers where Claude used plain lists. First words differ by model too: ChatGPT opened with "certainly" and "below is", Claude with a reference back to the prompt.

### Content

In 2,000 pieces of creative writing from one open-weight model, Paech et al. found the name "Elara" 85,513 times more often than in human text. Across 67 models, the word "flickered" was on the over-represented list of 98.5% of them.

## Each model has its own

Sun et al. collected responses from five chat models, ChatGPT, Claude, Grok, Gemini and DeepSeek, and trained a classifier to say which model wrote a given response. It was right 97.1% of the time, against 20% for a guess. With the words of each response shuffled into random order it was still right 88.9% of the time, so most of the signal is in which words a model uses and how often.

The same paper had a different model rewrite the responses. A classifier trained on the paraphrases identified the original author 91.4% of the time, and on translations into Chinese 91.8%. Only summarizing to one paragraph made a large dent, to 58.1%.

For anyone trying to remove tics, the first result means a list of them has to be made for the model in use. Paech et al. found the same from the other direction: the lists cluster within a model family and differ between families. [Claude's verbal tics](/wiki/ai/verbal-tics/anthropic-claude) is such a list for one family. The second result means that passing a draft through another model does not clean it.

## Where they come from

The habits arrive with the training that turns a text predictor into an assistant. Meta publishes Llama 3 both as a base model, which only continues text, and as an instruction-tuned model, which has been further trained to answer requests. Reinhart et al. found that the base models used grammatical features "at rates similar to human texts" and the instruction-tuned ones did not; their reading is that "instruction tuning appears to make the model output less human, not more." Instruction tuning bundles several steps, and for the vocabulary the evidence points at one of them: [LLM overused words](/wiki/ai/overused-words#where-it-comes-from) sets out why the word shift is consistent with preference training, in which raters reward wording they find familiar and the optimizer turns a preference of a few points into a habit. Whether the grammatical shift has the same origin has not been tested separately.

## What a tic costs

Readers use tics to decide that a text was machine-written. Wikipedia's guide exists for that purpose: its editors use the signs to find model output that was added without disclosure.

A tic can also mark a place where something specific is missing. The guide describes the underlying habit as regression to the mean, in which the "inventor of the first train-coupling device" becomes "a revolutionary titan of industry". It warns its own readers against treating the signs as the thing to fix:

> Please do not merely treat these signs as the problems to be fixed; that could just make detection harder.

Its stated reason is that the signs point to deeper problems in the text, and those remain after the signs are edited out.

## In this section

- [Mitigating verbal tics](/wiki/ai/verbal-tics/mitigation) — the four places a tic can be intercepted, what each has been measured to do, and why a ban on the phrase fails.
- [Verbal tics by application](/wiki/ai/verbal-tics/by-application) — which of those methods a chat user, an API integrator, a coding agent's operator and a novelist can reach, and which tics each should care about.
- [Claude's verbal tics](/wiki/ai/verbal-tics/anthropic-claude) — an open list for one model family, with each entry marked by how it is known.

## Related

- [LLM overused words](/wiki/ai/overused-words) — the word layer, with the measurements across the scientific literature.
- [Reversion to house style](/wiki/ai/pastiche/reversion-to-house-style) — why the default manner returns wherever a style instruction is silent.
- [RLHF](/wiki/ai/llm/rlhf) — the training step that installs the preference.
- [Stylometry](/wiki/cs/stylometry) — the older discipline of identifying a writer from word frequencies.

## Sources

- Reinhart et al., [Do LLMs write like humans? Variation in grammatical and rhetorical styles](https://arxiv.org/abs/2410.16107), arXiv:2410.16107 (2024, revised 2025)
- Sun et al., [Idiosyncrasies in Large Language Models](https://arxiv.org/abs/2502.12150), arXiv:2502.12150 (2025)
- Paech et al., [Antislop: A Comprehensive Framework for Identifying and Eliminating Repetitive Patterns in Language Models](https://arxiv.org/abs/2510.15061), arXiv:2510.15061 (2025)
- Wikipedia, [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), WikiProject AI Cleanup, as read on 5 October 2026; the July 2026 study it reports is *The Economist*, [How to spot AI writing](https://www.economist.com/culture/2026/07/30/how-to-spot-ai-writing), 30 July 2026, which this page has not read directly
