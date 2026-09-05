---
title: "LLM Overused Words"
weight: 25
---

*Delve*, *intricate*, *underscore*, *tapestry*, *load-bearing*, *nuanced* — a small set of words appears in text from an [aligned](/wiki/ai/llm/rlhf) [large language model](/wiki/ai/llm) far more often than in anything written before 2023. The effect is large enough to measure across the scientific literature, it comes from [preference training](/wiki/ai/llm/rlhf) rather than from the architecture or the training corpus, and it moves: once a word becomes a tell, writers scrub it and the fingerprint surfaces somewhere else.

## The size of the shift

Kousha and Thelwall tracked twelve of these terms across six bibliographic databases from 2015 to 2024. Between 2022 and 2024, *delve* rose about 1,500%, *underscore* about 1,000% and *intricate* about 700%. In PubMed Central full texts, the share of papers using *underscore* six or more times grew by over 10,000% from 2022 to 2025.

Kobak et al. came at the same question from excess vocabulary across 15.1 million abstracts and put a floor under it: at least 13.5% of 2024 abstracts had been through a model — roughly 200,000 papers — reaching 41% for computation papers from China. Liang et al., over some 950,000 papers, estimated model-modified sentences at up to 17.5% of computer-science arXiv abstracts by February 2024.

## The fingerprint migrates

Geng and Trotta found *delve* and *intricate* falling in arXiv abstracts soon after they were named as tells in early 2024, while bland markers like *significant* kept climbing. Model use did not drop; the conspicuous words did. A detector or a house style built on a fixed word list is dated from the day it ships.

## Where it comes from

Juzek and Ward tested the obvious explanations for 21 such words — training data, model architecture, decoding parameters — and none accounted for the overrepresentation. What survived was consistent with [RLHF](/wiki/ai/llm/rlhf). Their follow-up put identical PubMed-derived prompts to [Llama Base](/wiki/ai/llm/glossary) and Llama Instruct: *nuanced* appeared 8,342% more often from the instruct model, *firstly* 4,794% more. 400 raters, recruited on Prolific to match the demographics of the workforce that annotates preference data, chose the high-overuse variant 52.4% of the time against 47.6% (χ² = 9.4, p < 0.01).

Five points of preference is the whole mechanism. Comparisons are collected in bulk and then optimized against without mercy, so a bias that small comes out the far end as a verbal habit anyone can spot.

Zhang et al., who go on to propose Verbalized Sampling below, name it **typicality bias**. They model a rater's judgement as the answer's true quality plus α times how typical its wording is, and fit α̂ ≈ 0.57 (p < 10⁻¹⁴) on response pairs rated equally correct — familiarity pulling more than half as hard as being right. The words are not preferred for being better.

Model collapse is a separate risk pointing the same way: Shumailov et al. showed that training a generative model on its own recursively generated output erases the tails of the distribution, narrowing the range by an unrelated mechanism.

## Mitigations, by weight of evidence

**Verbalized Sampling** asks the model for several candidate responses with their probabilities and takes one from the tail, rather than accepting the single modal answer. It buys 1.6–2.1× the diversity of direct prompting on creative tasks and recovers 66.8% of the base model's diversity where direct prompting retains 23.8%. It needs no retraining and no access to logits, and composes with [temperature and top-p](/wiki/ai/llm/sampling-strategies) rather than replacing them.

**Banned-word lists and voice prompts** work on the words they name and only those — the coevolution result again, since the vocabulary relocates to whatever nobody thought to ban.

**A base or lightly tuned model** carries the widest range and the worst instruction-following — the trade to make when range matters more than obedience.

**A human edit pass** is the only one of these that catches the word the list did not have.

**Diversity-aware training objectives** are research-stage; nothing has shipped in a production model.

## Related

- [RLHF](/wiki/ai/llm/rlhf) — the preference-training step this vocabulary is a side effect of, and the calibration cost it charges alongside.
- [Sampling strategies](/wiki/ai/llm/sampling-strategies) — temperature, top-k and top-p, the knobs Verbalized Sampling sits on top of.
- [Prompt engineering](/wiki/ai/prompt-engineering) — where a voice prompt or a banned-word list actually gets written.

## Further reading

- Kousha & Thelwall, [How much are LLMs changing the language of academic papers after ChatGPT? A multi-database and full text analysis](https://doi.org/10.1007/s11192-026-05601-5), *Scientometrics* (2026); preprint [arXiv:2509.09596](https://arxiv.org/abs/2509.09596)
- Kobak et al., [Delving into LLM-assisted writing in biomedical publications through excess vocabulary](https://doi.org/10.1126/sciadv.adt3813), *Science Advances* 11(27), 2025
- Liang et al., [Mapping the Increasing Use of LLMs in Scientific Papers](https://arxiv.org/abs/2404.01268), arXiv:2404.01268 (2024)
- Geng & Trotta, [Human-LLM Coevolution: Evidence from Academic Writing](https://arxiv.org/abs/2502.09606), arXiv:2502.09606 (2025)
- Juzek & Ward, [Why Does ChatGPT "Delve" So Much? Exploring the Sources of Lexical Overrepresentation in Large Language Models](https://arxiv.org/abs/2412.11385), arXiv:2412.11385 (2024)
- Juzek & Ward, [Word Overuse and Alignment in Large Language Models: The Influence of Learning from Human Feedback](https://arxiv.org/abs/2508.01930), arXiv:2508.01930 (2025)
- Zhang et al., [Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity](https://arxiv.org/abs/2510.01171), arXiv:2510.01171 (2025)
- Shumailov et al., [AI models collapse when trained on recursively generated data](https://doi.org/10.1038/s41586-024-07566-y), *Nature* 631, 755–759 (2024)
- Orlowitz, [Delving into the load-bearing tapestry of AI's overused words](https://medium.com/@jakeorlowitz/delving-into-the-load-bearing-tapestry-of-ais-overused-words-a2a0024cee9a), Medium
