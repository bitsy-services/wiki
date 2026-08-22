---
title: "Sampling Strategies"
weight: 220
---

Sampling is how a model's opinion becomes a word. Everything before it produces a probability for every entry in the vocabulary; sampling is the rule that turns that spread of probabilities into the one token which actually gets emitted, appended to the text, and fed back in for the next round. It is the last step in the loop and the only part of inference that isn't the model — you can change it freely, per request, without touching a weight. It is also, when generated text comes out repetitive or unhinged, very often the thing at fault.

## The obvious rule, and why it fails

Take the most likely token every time. It's deterministic, it's reproducible, and it's called **greedy** decoding.

It also degenerates, reliably and fast, into repeating itself — and the reason is worth understanding, because it isn't a bug in the model. The most likely continuation of a phrase the model has just written is often that same phrase again: text genuinely does repeat, and the model has correctly learned so. But once the repetition begins it is now *in the context*, which makes the next repetition more likely still. Greedy decoding has no mechanism for ever leaving that groove, because leaving requires taking a token that wasn't the top one, and it never does.

What you get is fluent, grammatical, locally plausible text that locks into a loop within a paragraph.

## The opposite rule, and why that fails too

So draw randomly from the distribution instead, in proportion to the probabilities. **Pure sampling** never loops. It wanders instead.

The culprit is the sheer size of the tail. After `"the cat sat on the"`, the roughly 49,500 tokens sitting below `p = 0.0001` carry more probability *between them* — about 0.10 — than the single best token does at 0.08. Each individually is absurd; collectively they're a tenth of the distribution.

So at every single step there is a meaningful chance of drawing something the model considered nearly impossible. Sample a few hundred tokens and it stops being a chance and becomes a certainty. One such draw is usually enough to derail the passage, because it goes into the context and everything after it is conditioned on the model having apparently meant it.

## Truncation: delete the tail before drawing

Both failures come from the same place, so both are addressed the same way — cut the tail off, renormalize what's left, and sample from that.

**Top-k** keeps the `k` highest-probability tokens. It's crude, because `k` is fixed and the distribution's shape is not. `k = 50` lets in 49 also-rans when the model was certain, and amputates good options when it genuinely wasn't.

**Top-p**, or **nucleus** sampling, keeps the smallest set of tokens whose probabilities sum to at least `p`. That set grows and shrinks with the model's actual confidence: after `"the capital of France is"` the nucleus is a single token, while mid-clause it can run to thousands. The adaptivity is the entire reason it's the default nearly everywhere.

The difference is a shortlist drawn up by headcount versus one drawn up by merit. Top-k always interviews fifty candidates, whether or not fifty are any good. Top-p interviews however many it takes to cover the credible field — sometimes one, sometimes hundreds — and it's the only one of the two that can tell those situations apart.

[Temperature](/wiki/ai/llm/softmax-and-temperature) composes with either, and it's useful to see that the two are attacking the same tail from opposite ends. Temperature *reweights* the tail, making it collectively less attractive without removing anything. Truncation *deletes* it, setting those probabilities to exactly zero. Turning temperature down and turning `top_p` down both make output safer and duller; they are not the same operation and they stack.

## What this buys, and what it costs you

Sampling is the cheapest place to change a model's character. No retraining, no weights, decided per request.

The bill is determinism. A greedy model gives the same answer twice; a sampled one doesn't, which is why reproducing a bug report from a production [LLM](/wiki/ai/llm) means capturing the sampling parameters and the seed, not just the prompt. It's also the constraint [speculative decoding](/wiki/ai/llm/speculative-decoding) has to work around: a scheme that makes generation faster is only acceptable if it draws from *exactly* the distribution the sampler would have drawn from unaided, and most of the cleverness on that page is in proving it does.

## Check yourself

[Greedy-decode](/wiki/ai/llm/running-the-checks) 100 tokens from [GPT-2 small](/wiki/ai/llm/gpt-2) on any prompt — it falls into a repeating phrase. Same prompt with `top_p=0.9` — no loop. Then log the nucleus size at each step: at p = 0.9 it runs from 1 to about 9,400, median ~120. No fixed `k` covers that range.

## Depends on / leads to

Depends on [softmax and temperature](/wiki/ai/llm/softmax-and-temperature). Leads to [speculative decoding](/wiki/ai/llm/speculative-decoding), which has to reproduce whatever this page decided. That's the end of the inference track — the sidebar picks up next at [perplexity](/wiki/ai/llm/perplexity), which is [the loss](/wiki/ai/neural-network/the-loss-function) in units you can reason about.
