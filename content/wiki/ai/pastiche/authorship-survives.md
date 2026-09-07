---
title: "Authorship Survives Imitation"
weight: 40
---

An imitation can satisfy a reader and still be separated from the author's real writing by a statistical test that takes a second to run. The reason is structural rather than a matter of the imitation being poor: the features a reader judges style by and the features that identify an author are almost disjoint sets, and a prompt can only address the first.

## The features that identify are not the features that are noticed

[Stylometry](/wiki/cs/stylometry) established the split before computers were involved in writing: attribution runs on the rates of high-frequency function words, because those rates are stable within a writer and independent of what the writing is about. The [Federalist Papers](/wiki/cs/stylometry#the-federalist-problem) settle the comparison — Hamilton and Madison differ by four hundredths of a word in average sentence length and are separated outright by their function-word rates.

The corollary matters for anyone building an imitation from a description. **A writer cannot accurately describe their own style**, because [the identifying part of it was never available to introspection](/wiki/cs/stylometry#why-the-signal-sits-where-nobody-is-looking). Ask an author what makes their prose theirs and they will name what they can perceive — the short sentences, the semicolons, the refusal of adverbs. Those features are real, and they are also precisely the features any competent imitator copies first.

So a style brief is built from the perceptible layer by construction. There is no other layer anyone has access to. That ceiling is not a prompt-engineering problem and better prompting does not raise it.

## Does impersonation defeat verification?

This is where the literature disagrees, and the disagreement has not been resolved.

**Alperin et al. say yes, substantially.** Attacking a fine-tuned BigBird verifier — chosen because it outperformed the other transformer verifiers they tested — they report attack success up to **92%** for obfuscation on a corpus of 129 public figures' posts, 83% on a fan-fiction corpus of 1,595 authors, and up to **78%** for impersonation on the fan-fiction corpus, averaging 50–55% across target authors. Semantic content survived the attacks by the usual overlap metrics. Their attacks were engineered: paraphrase models, a fine-tuned Mistral with retrieval over the target author's writing, and a dedicated style-transfer system.

**Zeng and Nini say no.** Using GPT-4o as the adversary across four prompting conditions and three genres — emails, text messages, social posts — they tested against a battery of forensic methods in a likelihood-ratio framework: n-gram tracing, an impostors method, LambdaG, and three neural authorship models. Impersonation texts "failed to sufficiently replicate authorial individuality to bypass established AV systems" — authorship verification — and some methods rejected the impersonations *more* reliably than they rejected genuine different-author samples.

Their explanation is the same finding that appears elsewhere on these pages from a different angle: the resilience "stems, at least in part, from the higher lexical diversity and entropy inherent in LLM-generated texts." The imitation is too various and too unpredictable to be the person. That is [Hemingway rendered with a type-token ratio a third above Hemingway's](/wiki/ai/pastiche/what-transfers), and [output at half the perplexity of the writing it copies](/wiki/ai/pastiche/reversion-to-house-style), showing up as evidence for the prosecution.

### Reading the two together

The results are not in direct contradiction, and three differences account for most of the gap.

**What was defended.** Alperin et al. attack one neural verifier. Zeng and Nini attack a panel including non-neural forensic methods built to produce likelihood ratios for court. A single learned classifier has a decision surface an attacker can search; a battery of methods resting on different features does not fail in the same direction at once. The gap is wide enough that against one neural verifier even plain prompting succeeds, provided the genre is conventionalized — Wang et al.'s generated news and email [pass as the same author better than 94% of the time](/wiki/ai/pastiche/reversion-to-house-style#where-the-imitation-succeeds-is-where-the-author-was-already-generic). What resists is the forensic panel, and the genres where an individual's idiosyncrasy is most of the signal.

**What was spent.** Zeng and Nini's title names their threat model: *via LLM prompting*. Alperin et al. fine-tuned a model, attached retrieval over the target's corpus, and ran a purpose-built transfer system. The honest summary is that **prompting alone does not defeat forensic authorship verification, and a dedicated attack pipeline defeats a single neural verifier a good fraction of the time.** Those are different claims about different adversaries and both may be true.

**Which direction the attack ran.** Even within Alperin et al.'s own numbers, obfuscation beat impersonation — 92% against 78%, and 50–55% on average. Hiding your own signature is easier than acquiring someone else's, which follows from the mechanism: obfuscation only has to perturb the function-word profile in any direction, while impersonation has to land on a specific point in a high-dimensional space that neither the attacker nor the target can describe.

Both papers agree on that asymmetry, whatever else they disagree about.

## Detection is a separate question with a similar answer

Whether generated text passes as *that author* is authorship verification. Whether it passes as *a human at all* is detection. Wang et al. measured it across [the same 400-plus authors and four corpora](/wiki/ai/pastiche/reversion-to-house-style#where-the-imitation-succeeds-is-where-the-author-was-already-generic): the share of generated text classified as human ran from near zero for the GPT models up to about 54% at its best, for Gemini on the email corpus. This is a separate measurement from the verification accuracies above, asking whether the text passes as a person rather than as the target person.

Both questions come back to the same excess. A verifier finds the text too various to be the target; a detector finds it too regular to be a person. Those sound opposed and are not — the variation is in vocabulary, the regularity is in the token distribution, and generated text overshoots on the first while undershooting on the second.

## What this is good for

The defensive reading is that authorship attribution has not been destroyed by generative models, which matters for forensic linguistics, for plagiarism work, and for anyone whose anonymity depends on their writing not being traceable. Zeng and Nini's result is evidence that the standard methods still hold against the standard attack.

For a writer the reading is narrower: **the part of your style that anyone can copy is the part you could describe.** What survives the copy is what you never chose. Whether that is reassuring depends on which part you thought was yours.

## Check yourself

Take an author with enough text to build a reference profile, generate a dozen imitations, and compute [Burrows's Delta](/wiki/cs/stylometry#burrowss-delta) from each imitation to that author and to three unrelated authors. The imitations should not land nearest their target — and where they do land is the interesting part. If they cluster near each other rather than near any human author, the profile they share is the model's, which is [the reversion result](/wiki/ai/pastiche/reversion-to-house-style) arriving through the front door.

## Related

- [Stylometry](/wiki/cs/stylometry) — the measurement tradition, Burrows's Delta, and why function words carry identity.
- [What transfers and what does not](/wiki/ai/pastiche/what-transfers) — the feature-level evidence for the same ceiling.
- [Reversion to house style](/wiki/ai/pastiche/reversion-to-house-style) — the statistical excess that verifiers detect.
- [Law and ethics](/wiki/ai/pastiche/law-and-ethics) — where deception stops being a technical question.

## Further reading

- Alperin et al., [Masks and Mimicry: Strategic Obfuscation and Impersonation Attacks on Authorship Verification](https://aclanthology.org/2025.nlp4dh-1.10/), Workshop on Natural Language Processing for Digital Humanities, 2025; preprint [arXiv:2503.19099](https://arxiv.org/abs/2503.19099)
- Zeng & Nini, [Authorship Impersonation via LLM Prompting does not Evade Authorship Verification Methods](https://arxiv.org/abs/2603.29454), arXiv:2603.29454 (2026)
- Wang et al., [Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors](https://arxiv.org/abs/2509.14543), arXiv:2509.14543 (2025)
- Nini, [A Theory of Linguistic Individuality for Authorship Analysis](https://doi.org/10.1017/9781108974851), Cambridge University Press (2023)
- Mosteller & Wallace, [Inference in an Authorship Problem](https://doi.org/10.1080/01621459.1963.10500849), *Journal of the American Statistical Association* 58(302), 275–309 (1963)
