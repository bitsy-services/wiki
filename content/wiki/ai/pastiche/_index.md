---
title: "Pastiche"
weight: 27
bookCollapseSection: true
---

Pastiche is new writing in the recognizable manner of a specific author — not a quotation of them, not a parody of them, but fresh sentences that a reader would place. Asking a [large language model](/wiki/ai/llm) for it takes one line, and the result fails in ways that are now measured rather than merely felt.

The failures are specific and they run in opposite directions. What the prompt names gets amplified past the point the real author ever took it ([generative exaggeration](/wiki/ai/pastiche/generative-exaggeration)). What the prompt does not name reverts to the model's own register ([reversion to house style](/wiki/ai/pastiche/reversion-to-house-style)). The features that survive the trip are the perceptible ones — sentence rhythm, vocabulary, punctuation habits — and the features that actually identify an author are not those ([what transfers](/wiki/ai/pastiche/what-transfers)). That last point has a hundred-year pedigree in [stylometry](/wiki/cs/stylometry) and it is the reason the whole exercise has a ceiling.

Writing about this from a model's own impression of an author's style would demonstrate the failure rather than describe it, because that impression is the caricature under examination. The measurements below come from stylometric, forensic and persona-simulation studies published between 2022 and 2026, along with two borrowed cases — code generation and style transfer — which the pages using them flag as borrowed.

## Three tasks that get confused

*Pastiche*, *style transfer* and *forgery* describe different jobs. They have different inputs, different success conditions and different literatures, and a result about one does not carry to another.

| | Input | Output | Succeeds when |
| --- | --- | --- | --- |
| **Pastiche** | a target style, named or exemplified | new text, new content | a reader or a stylometric measure places it as the target |
| **Style transfer** | a target style *and* a source text | the source text, restyled | the style moves *and* the meaning survives |
| **Forgery** | a target author and a provenance claim | text presented as genuine | a specific verifier is deceived |

**Pastiche has no meaning constraint.** Asked for a paragraph about a lighthouse in Hemingway's manner, the model may write any lighthouse paragraph it likes. Nothing is being preserved, so nothing can be lost, and the only question is whether the manner landed.

**Style transfer adds a preservation constraint that pastiche does not have**, which is why its evaluation is a joint score rather than a single one. Transfer strength and meaning preservation trade against each other: a system can max either by sacrificing the other, so the field reports style accuracy, content preservation and fluency together, often as a geometric mean. Yang and Carpuat's register-guided prompting is a style-transfer result, and its headline is a meaning-preservation number rather than a style number — so [the gains it reports](/wiki/ai/pastiche/rules-versus-examples) are largely about not destroying the source, which a pastiche prompt does not have.

**Forgery adds an adversary and a victim.** It is the only one of the three whose success condition is defined by someone else's failure, and the only one where the target's *identity* rather than the target's *manner* is the thing at stake. It is also the one where the model does worst, for a reason that turns out to be structural rather than incidental: the same statistical excess that makes the pastiche unconvincing is what the verifier detects. [Authorship survives imitation](/wiki/ai/pastiche/authorship-survives) works through the evidence, including a disagreement in the literature that is not yet settled.

The distinction matters for reading claims as much as for making them. "The model imitated Hemingway well" is a pastiche claim, and [Mikros's stylometric measurements](/wiki/ai/pastiche/what-transfers) bear on it. "The model impersonated a Reddit user" is a forgery claim, and the authorship-verification literature bears on it. A paper reporting success at one is routinely cited as evidence for the other.

## What it is used for

Literary impersonation is the memorable case and not the common one. The everyday version is getting a model's output to sound like a particular publication, a particular documentation set, or the person who has to sign it.

This wiki is a worked example of the everyday version. `.claude/rules/wiki-voice.md` is a style description, written by hand, aimed at an agent that has to produce prose matching pages it did not write — the [durable-instruction mechanism](/wiki/ai/context-engineering/claude-code#durable-instructions-claudemd-and-rules) in the section's running example. It names the perceptible layer, because that is the only layer anyone can name, and the residue it does not reach is the model's own register.

The mechanism running underneath is the one [LLM overused words](/wiki/ai/overused-words) documents from the other side. That page is about the register an aligned model reaches for by default. Pastiche is the attempt to override it, and reversion is that register winning.

## Pages

- [Generative exaggeration](/wiki/ai/pastiche/generative-exaggeration) — salient features amplified past the original, and why richer source material makes it worse rather than better.
- [What transfers and what does not](/wiki/ai/pastiche/what-transfers) — the feature-by-feature account, including a lexical-diversity result that runs backwards.
- [Reversion to house style](/wiki/ai/pastiche/reversion-to-house-style) — where the unpinned residue of a prompt actually lands.
- [Authorship survives imitation](/wiki/ai/pastiche/authorship-survives) — why the identifying features are the hard ones, and whether impersonation defeats verification.
- [Rules versus examples](/wiki/ai/pastiche/rules-versus-examples) — showing the model prose against telling it what the prose does, and what the measurements actually favour.
- [Law and ethics](/wiki/ai/pastiche/law-and-ethics) — what is settled, what is live, and where the public domain sits.

## Related

- [Stylometry](/wiki/cs/stylometry) — the measurement tradition all of this is scored against.
- [LLM overused words](/wiki/ai/overused-words) — the default register pastiche is trying to override.
- [Prompt engineering](/wiki/ai/prompt-engineering) — where a style instruction is actually written.
