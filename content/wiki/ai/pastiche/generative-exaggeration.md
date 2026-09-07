---
title: "Generative Exaggeration"
weight: 10
---

Asked to write as someone, a [language model](/wiki/ai/llm) finds the features that most distinguish that someone and turns them up. Everything else about the person flattens out. Nudo et al. named this **generative exaggeration** — "a systematic amplification of salient traits beyond empirical baselines" — and measured it moving the wrong way with better information: a fuller picture of the person produces a more stereotyped portrait, not a less stereotyped one.

## Caricature, formalized

Myra Cheng, Tiziano Piccardi and Diyi Yang built the measurement in **CoMPosT**, presented in 2023. It characterizes a simulation along four dimensions — Context, Model, Persona, Topic — and scores it on two criteria that have to be met together.

**Individuation** asks whether the output is distinguishable from what the model says with no persona at all. It is measured by training a classifier on sentence embeddings to separate the persona's outputs from the default persona's outputs, and reporting its accuracy on a held-out split. Above 0.5 means the persona changed something.

**Exaggeration** asks whether what changed is a stereotype. Cheng et al. build a *contextualized semantic axis* whose two poles are the words that distinguish the persona and the words that distinguish the topic, selecting them with Fightin' Words — a log-odds method for finding the terms that genuinely separate two corpora rather than the merely frequent ones — at z > 1.96. The axis is the difference of the two pole means:

```text
V(p,t) = mean(embeddings of persona-distinguishing words)
       - mean(embeddings of topic-distinguishing words)

exaggeration = normalized mean cosine similarity of the
               simulation's outputs to V(p,t)
```

An output can be individuated without being exaggerated — that is a simulation that says something specific without saying something stereotyped. **Caricature is the conjunction:** individuation above 0.5 *and* high exaggeration. The output is recognizably the persona, and it is recognizable because it leans on the persona's cliché.

Fifteen personas were tested across age, political leaning, race and ethnicity, and gender, against thirty topic pairs drawn from WikiHow categories and ProCon.org controversial topics, plus thirty Pew Research questions reframed as open-ended interview prompts. Only GPT-4 was evaluated in depth; the authors report that older and open-weight models produced simulations too poor in quality to measure this way. A hundred outputs per simulation was fixed by power analysis — a minimum of 28 samples for individuation at effect size 0.75, and 41 for exaggeration at 0.62, with α = 0.05 and power 0.8.

## The topics where it is worst are the harmless ones

Individuation was near-total in the interview context: every persona above 0.95. In the forum context it dropped for *man* and *woman*, to roughly 0.65–0.70, and stayed above 0.85 for the rest.

Exaggeration concentrated on political and marginalized personas — nonbinary, Black, Hispanic, Middle-Eastern and conservative highest, with *man*, *woman*, *Asian* and *liberal* lowest.

Exaggeration was highest on **general, uncontroversial** subjects — health, philosophy and religion, education — and fell substantially as topics got more specific, which is a result about topics rather than about personas. A fine-grained follow-up walking from "health" down to particular mental-health questions confirmed the inverse relationship across five levels of specificity.

The mechanism is not mysterious once stated. On a specific question there is a specific answer, and the persona has somewhere to go other than itself. On "what do you think about education," there is nothing to say except be the persona, so the model performs the persona, and performing a demographic is what stereotype means.

## More information, worse portrait

Jacopo Nudo and colleagues took the same phenomenon to a scale where the ground truth is known. They built agents from 1,186 real X users drawn from 21 million interactions around the 2024 US presidential election, each user having at least 50 prior posts, and ran six models across three families — Gemini 2.0 Flash and Gemma 3, Mistral 7B and 123B, DeepSeek V2 and V3.

Two conditions: **zero-shot**, giving the model only the user's political leaning, and **few-shot**, giving it the username, the biography and thirty of that user's actual posts.

Few-shot is the condition with more truth in it, and it is the condition that produced the worse simulation.

- Ideological consistency rose steeply — DeepSeek's Republican-labelled agents went from 45% consistent to 95%. Users labelled politically neutral lost their neutrality in the same move.
- Toxicity above the 0.6 threshold matched the human baseline of roughly 5% under zero-shot, and overshot it under few-shot, with the Gemini family furthest above. Larger variants produced output more toxic than the samples they were initialized from.
- 87.47% of real tweets contained no emoji; 49% of Mistral's replies contained at least one. The rainbow emoji appeared nearly twenty times more often in DeepSeek's output than in authentic human replies.
- 96.29% of real tweets carried no hashtag. Partisan hashtags such as `#MAGA2024` and `#kamalaharris2024` ran ten to fifteen times more frequently in model output than in the users being simulated.
- Right-leaning users were caricatured harder than left-leaning ones, though both were affected.

Nudo et al.'s summary is that the models "do not emulate users, they reconstruct them," with outputs reflecting the model's internal optimization more than the observed behaviour.

The instinct on a disappointing imitation is to supply more of the author — another three chapters, a longer style brief, a bigger sample. Thirty real posts per user is a substantial sample, and it moved coherence up and realism down at the same time. The extra material sharpens the model's estimate of what is *salient* about the person, and salience is the input to the amplifier.

## What follows for a prompt

The lever that worked in Cheng et al.'s data is topic specificity, not persona detail. Exaggeration fell when the question had a real answer in it. A pastiche prompt that names a concrete subject, a concrete situation and a concrete constraint gives the model somewhere to put its effort other than performing the author.

The lever that did not work is more evidence about the target. Supplying it improves the model's model of the target and worsens the output, because the failure was never a shortage of information about who the person is.

## Check yourself

Ask a model for two paragraphs in a named author's manner: one on "what you think about family," one on a specific mechanical task — repairing a carburetor, docking a boat. Count the author's signature moves per hundred words in each. The general prompt should be denser in them. If a feature appears three times a paragraph in the abstract piece and once in the concrete one, that gap is the exaggeration term, and it moved because the topic moved, not because the author did.

## Related

- [Reversion to house style](/wiki/ai/pastiche/reversion-to-house-style) — the complementary distortion: exaggeration inflates what the prompt pins, reversion claims what it does not.
- [What transfers and what does not](/wiki/ai/pastiche/what-transfers) — which specific features get amplified, measured on literary prose.
- [Rules versus examples](/wiki/ai/pastiche/rules-versus-examples) — why adding exemplars is not the fix it appears to be.

## Further reading

- Cheng, Piccardi & Yang, [CoMPosT: Characterizing and Evaluating Caricature in LLM Simulations](https://aclanthology.org/2023.emnlp-main.669/), Conference on Empirical Methods in Natural Language Processing, 2023; preprint [arXiv:2310.11501](https://arxiv.org/abs/2310.11501)
- Nudo et al., [Generative exaggeration in LLM social agents: Consistency, bias, and toxicity](https://www.sciencedirect.com/science/article/pii/S246869642500045X), *Online Social Networks and Media* (2025); preprint [arXiv:2507.00657](https://arxiv.org/abs/2507.00657)
- Monroe, Colaresi & Quinn, [Fightin' Words: Lexical Feature Selection and Evaluation for Identifying the Content of Political Conflict](https://doi.org/10.1093/pan/mpn018), *Political Analysis* 16(4), 372–403 (2008)
- Cheng, Durmus & Jurafsky, [Marked Personas: Using Natural Language Prompts to Measure Stereotypes in Language Models](https://aclanthology.org/2023.acl-long.84/), Annual Meeting of the Association for Computational Linguistics, 2023
