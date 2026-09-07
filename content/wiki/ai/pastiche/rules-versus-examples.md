---
title: "Rules Versus Examples"
weight: 50
---

There are two ways to tell a model what a style is. Show it prose and let it infer, or describe the prose and let it follow the description. Both are bounded, and they are bounded differently: examples carry everything about the sample including the parts you did not mean, and descriptions carry only what someone managed to notice. The measurements favour supplying both, and then constraining the description so the model cannot invent its own criteria for what the style is — with the caveat this page keeps returning to, that they were taken on code generation and on style transfer rather than on pastiche.

This page is about style specifically. [Prompt engineering](/wiki/ai/prompt-engineering) covers few-shot prompting as a general technique.

The section's running example runs both sides of the split at once. An agent [writing a page for this wiki](/wiki/ai/context-engineering/claude-code#durable-instructions-claudemd-and-rules) gets `.claude/rules/wiki-voice.md`, a hand-written description that is always in context, and then reads two or three sibling pages before drafting. That is the combined condition, which is the one the measurements below favour.

## What examples actually transmit

Exemplars work through in-context learning, and what in-context learning picks up from a demonstration is more superficial than the word "learning" suggests. Models take format regularities and local structure from demonstrations rather than the task semantics underneath.

Jeremiah Bohr measured the difference directly. Four system-prompt conditions across 160 code-generation sessions on Gemini 2.5 Pro, each run twice — an initial generation, then a revision asking for better readability, maintainability and error handling. Conditions were a control, explicit minimalist directives, two concise code samples, and both together.

| Condition | Turn 1 output | Effect size | Turn 2 growth |
| --- | --- | --- | --- |
| Control | 2560 tokens | — | +266 |
| Examples | 2036 tokens | d = −2.63 | +268 |
| Instructions | 1113 tokens | d = −7.84 | +175 |
| Both | 759 tokens | d = −10.97 | +126 |

Examples produced roughly a 20% compression; instructions produced 56%; both produced 70%.

Asked to expand the code, the exemplar condition grew by 268 tokens — statistically indistinguishable from the control's 266. Whatever the examples had established did not survive contact with a new instruction. Both conditions carrying explicit directives held: 175 tokens for instructions alone, 126 for the combination. Bohr's framing is that examples "anchor local schema through surface-form imitation, whereas directives establish constraints that generalize beyond immediate generation context," and that the exemplars' influence "appears confined to initial generation."

**This is a code-generation study, and carrying it to prose is inference rather than evidence.** The mechanism it identifies — demonstrations transmitting local surface schemas rather than persistent constraints — is general to in-context learning, and prose style is a constraint that has to survive many paragraphs. But nobody has run Bohr's design on style.

The prose evidence points the same way without being as clean. Wang et al. found few-shot prompting consistently beating zero-shot across 400-plus authors, and then found that going past five exemplars bought little further stylistic alignment. Choosing exemplars more cleverly — by content similarity to the target passage, or by matching length — gave "mixed results," and approaches optimized for content "do not always enhance stylistic imitation." More of the same signal does not become a different signal.

## What descriptions cannot reach

A style description is written by someone who noticed things. That is its whole content, and it is why [the identifying features are missing from every style brief ever written](/wiki/ai/pastiche/authorship-survives): function-word rates are not available to introspection, so no author, editor or critic has ever put them in one.

Descriptions also have the failure mode that they are followed. "Short declarative sentences" is an instruction a model can execute uniformly, whereas the author varied. Executed literally, a description of a tendency becomes a rule, which is [exaggeration](/wiki/ai/pastiche/generative-exaggeration) arriving by a different route.

## Deriving the description from the prose

A description does not have to be recalled from reading. It can be generated from the prose, which is what the two systems below do — and the comparison between them isolates something narrower than "derived beats hand-written," which nothing here measures.

**STYLL** (Patel, Andrews and Callison-Burch) established the pipeline for low-resource authorship transfer, where the target may have only a few hundred words in existence — a Reddit user rather than a published novelist. It paraphrases the input into neutral prose, extracts natural-language style descriptors from the target's exemplars, and rewrites the neutral version under those descriptors. Their in-context learning baseline was the strongest approach available, and they were explicit that "current approaches do not yet achieve mastery."

**Register-guided prompting** (Xinchen Yang and Marine Carpuat) replaces ad-hoc descriptor extraction with a linguistic framework. It asks the model to characterize the target exemplar using Biber's multidimensional register analysis — the situational and functional dimensions along which texts systematically vary — converts that analysis into style adjectives, and rewrites with those. A contrastive variant analyzes source and target together rather than the target alone.

Against baselines including a one-line instruction prompt and STYLL, on Llama-3.2-3B-Instruct. Transfer accuracy asks whether the style moved, meaning preservation whether the source text survived; both run 0 to 1, higher better.

| Task | Metric | Register-guided | Contrastive | STYLL |
| --- | --- | --- | --- | --- |
| Reddit authorship imitation | meaning preservation | 0.545 | 0.536 | 0.221 |
| Informal → formal | transfer accuracy | 0.347 | 0.886 | 0.554 |
| Informal → formal | meaning preservation | 0.580 | 0.554 | 0.280 |
| Medical simplification | simplification score | 0.374 | 0.390 | 0.382 |

The headline is meaning preservation, roughly 2.5× STYLL's on the authorship task. Both systems derive descriptors, so this is not a rules-against-examples result: it is a result about *which* descriptors. Yang and Carpuat attribute the gap to STYLL's open-ended generation, which "tends to produce more affective, tone-oriented style descriptors, which may signal shifts in tone or intent and thus are more likely to alter the original meaning." Constraining the description to register dimensions keeps it from drifting into instructions about intent.

The win is narrower than the headline. On *steering* — transfer accuracy — the target-only register variant loses to STYLL, 0.347 against 0.554, and roughly ties it on simplification. Constraining the descriptors buys meaning preservation, not style strength.

The variant that wins on both is the contrastive one, at 0.886 transfer accuracy against STYLL's 0.554. Contrasting source with target tells the model what to *change*, which a description of the target alone does not contain. That is a style-transfer-shaped advantage: a pastiche prompt has no source text, so it inherits neither the meaning-preservation gain nor the contrastive one. [The task distinction](/wiki/ai/pastiche) is doing real work here — this table's best numbers are about a task pastiche is not.

## What to do

**Keep both, and expect the description to be the part that lasts.** Bohr's combined condition beat either alone by a wide margin, and his second turn says why the two are not interchangeable: the stated rule was still operating after a revision request and the exemplars were not. Supply both; assume the exemplars set the opening and the rules hold the line.

**Constrain the description.** An unconstrained model asked to characterize a style reaches for tone and affect — instructions about intent wearing the clothes of instructions about form, which is [exaggeration](/wiki/ai/pastiche/generative-exaggeration) arriving through the description rather than through the prompt. Both systems above derive their descriptors from the target's prose, and the one working inside a fixed linguistic framework preserved meaning far better than the one generating them freely. That number belongs to style transfer; the mechanism behind it does not.

**Aim the description at the gap.** Descriptors that restate where the model already is spend nothing. The instructions that pay are the ones that name where the author differs from the default: the repetition, the refused transition, the sentence that does not resolve. [Reversion to house style](/wiki/ai/pastiche/reversion-to-house-style) covers where that gap tends to sit.

## Check yourself

Take a page of an author's prose and run three prompts: the page as an exemplar; a style description you wrote from reading it; and a description the model derived from the page, used without the page. Generate 500 words from each, then continue each conversation with an unrelated revision request. Measure sentence length and type-token ratio at both turns. The exemplar condition should drift furthest between turn one and turn two.

## Related

- [Prompt engineering](/wiki/ai/prompt-engineering) — few-shot prompting and instruction wording in general.
- [Claude Code: writing a page for this wiki](/wiki/ai/context-engineering/claude-code) — the section's running example, and a live instance of the rules-side choice.
- [Authorship survives imitation](/wiki/ai/pastiche/authorship-survives) — why no description reaches the identifying layer.
- [Generative exaggeration](/wiki/ai/pastiche/generative-exaggeration) — what happens when a description of a tendency is executed as a rule.
- [Reversion to house style](/wiki/ai/pastiche/reversion-to-house-style) — where to point the instruction budget.

## Further reading

- Yang & Carpuat, [Steering Large Language Models with Register Analysis for Arbitrary Style Transfer](https://arxiv.org/abs/2505.00679), arXiv:2505.00679 (2025)
- Patel, Andrews & Callison-Burch, [Low-Resource Authorship Style Transfer: Can Non-Famous Authors Be Imitated?](https://arxiv.org/abs/2212.08986), arXiv:2212.08986 (2022)
- Bohr, [Show and Tell: Prompt Strategies for Style Control in Multi-Turn LLM Code Generation](https://arxiv.org/abs/2511.13972), arXiv:2511.13972 (2025)
- Wang et al., [Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors](https://arxiv.org/abs/2509.14543), arXiv:2509.14543 (2025)
- Min et al., [Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?](https://aclanthology.org/2022.emnlp-main.759/), Conference on Empirical Methods in Natural Language Processing, 2022
- Biber, [Variation across Speech and Writing](https://doi.org/10.1017/CBO9780511621024), Cambridge University Press (1988)
