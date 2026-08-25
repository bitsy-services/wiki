---
title: "RLHF"
weight: 330
---

RLHF — reinforcement learning from human feedback — is how a text predictor becomes something worth talking to. Pre-training can only teach a model what a human *would* write next, and that is not the same thing as what a human would want to *read*. A helpful answer and a useless one are both perfectly plausible continuations, and nothing in the original training signal can tell them apart. RLHF is the machinery for supplying the missing judgement: people are shown pairs of answers, asked which is better, and the model is trained toward the winners.

## Why the original objective can't get you there

[Cross-entropy](/wiki/ai/neural-network/the-loss-function) rewards predicting the text that actually came next. That's all it can express.

Ask a [base model](/wiki/ai/llm/glossary) a question and it may well continue with *another question*, or with a plausible-looking Stack Overflow comment, or with the next item in what looks like a FAQ. It isn't being unhelpful. It is being accurate: those really are things that follow questions in written text. The model is doing precisely what it was paid to do, and what it was paid to do was never "be useful."

The obvious repair is to write down a better objective — but nobody can. "Helpful, harmless, and honest" is not a function you can differentiate, and there is no corpus of correctly-scored answers to regress against.

The move that makes RLHF work is to sidestep that entirely. People are unreliable at *scoring* one answer on an absolute scale, and quite reliable at *comparing* two. So never ask for a score. Ask which of these two is better, collect a great many such judgements, and let the training procedure recover a scale from the comparisons.

## Three steps, classically

1. **Supervised fine-tune** on demonstrations — a plain [fine-tune](/wiki/ai/llm/fine-tuning) on examples of the behaviour you want, to get the model into roughly the right register before anything more elaborate starts.
2. **Train a reward model.** Collect comparisons, then take a copy of the language model, replace [the unembedding](/wiki/ai/llm/unembedding-and-logits) with a head that emits a single number instead of a vocabulary-wide score, and train it so preferred completions score higher than rejected ones. What you have built is a learned stand-in for human judgement, cheap enough to consult millions of times.
3. **Optimize against that reward.** The model being trained is now called the **policy**, borrowing the vocabulary of reinforcement learning: it acts, it gets scored, it adjusts. The usual algorithm is PPO — *proximal policy optimization*, whose "proximal" refers to an internal safeguard keeping each update close to the previous version of the policy.

Separately from PPO, and this is the part that matters here, the reward is docked by a **KL penalty**: a term measuring how far the policy's output distribution has drifted from the frozen model that came out of step 1. (KL is Kullback–Leibler divergence, the standard measure of how far one distribution sits from another.) It is a leash tied to a fixed post, not to wherever the policy stood a moment ago.

## The leash is the load-bearing part

That KL penalty reads as a technical safeguard and is what keeps the step from producing nonsense.

The reward model is a proxy for human judgement, and every proxy can be gamed. Take the leash off and the policy will find text that scores enormously and reads like nothing any human has ever written — degenerate strings, obsequious padding, whatever quirk of the reward model happened to survive training. **Reward hacking is the default outcome, not an edge case.** The policy is doing its job perfectly; the job was just badly specified, and optimizing hard against an imperfect measure is exactly how you discover it was imperfect.

Pay a call centre on customer-satisfaction scores and you will get agents who beg for five stars at the end of every call. They have not misunderstood you. They have understood you exactly.

## DPO: the same result without the reward model

**DPO** (direct preference optimization) removes step 2 altogether. Some algebra on the same preference pairs yields a loss function you can apply to the policy directly, with no separately trained reward model and no reinforcement learning loop. It is cheaper, markedly more stable to train, and now the common choice for open models.

## What none of this teaches

It teaches no new capabilities. RLHF reweights among behaviours the pre-trained model could already produce — which is why the aligned model tends to get measurably *worse* at raw next-token prediction than the base model it came from.

The subtler cost is **calibration** — whether a model's confidence in an answer actually predicts how often that answer is right. A base model's is rather good, because [cross-entropy paid it to be](/wiki/ai/neural-network/the-loss-function): hedging when genuinely unsure is the score-maximizing strategy. Preference training removes that incentive, plausibly because human raters prefer answers that sound certain.

The evidence is unusually clean here. OpenAI published before-and-after plots in the GPT-4 technical report: the pre-trained model assigned probabilities to its chosen answers that lined up almost exactly with how often those answers were correct, and the same model after preference training was considerably more sure of itself than it had any business being. The report's own caption says the process "hurts the calibration quite a bit."

So the confident tone people associate with these assistants isn't a by-product of their being good at anything. It's a side effect of optimizing a proxy that could not distinguish being right from sounding right. Nobody set out to install it, and it cost accuracy of self-assessment all the same.

The trade: helpfulness paid for in modelling accuracy, confidence paid for in calibration.

## Check yourself

Measure [perplexity](/wiki/ai/llm/perplexity) on plain WikiText for a base/instruct pair. [Qwen2.5-0.5B](/wiki/ai/llm/running-the-checks) is ungated and runs in minutes: base 17.9, Instruct 20.0. The aligned sibling is reliably worse at raw prose. Careful what you conclude, though: that gap bundles the fine-tune, the preference optimization, and a changed data mix. It's the post-training tax, not RLHF's share alone.

## Depends on / leads to

Depends on [fine-tuning](/wiki/ai/llm/fine-tuning). Leads to [speculative decoding](/wiki/ai/llm/speculative-decoding).
