---
title: "Perplexity"
weight: 235
---

Perplexity is the standard single number for how good a language model is at its one core job: predicting the next token. It restates the model's average surprise as an effective number of choices — how many equally-likely options the model is, in effect, deciding between at each step. Fewer is better; a model that always knew exactly what came next would have nothing left to choose between. It's the figure papers quote to claim one model fits a body of text better than another, though the same model scores differently depending only on how that text was cut into tokens — a caveat that turns out to be most of the story of reading the number honestly.

## The number behind the number

Perplexity is [the loss](/wiki/ai/llm/the-loss-function), exponentiated:

```text
perplexity = exp(cross-entropy loss)
```

The loss is a log-probability, measured in nats — natural-log units. Exponentiating undoes the log and turns it back into a count. To see *which* count, imagine the model spread its probability evenly across `k` tokens and the true token were always somewhere in that set: the loss would be `ln(k)`, and `exp(ln(k))` is `k`. So perplexity is the size of the uniform distribution that would leave the model exactly this confused. That's the **effective branching factor** — the number of options the model is behaving as if it's choosing between, uniformly, at every position.

The same number read from the other end: perplexity is one over the geometric mean of the probabilities the model assigned to the tokens that actually turned up.

```text
perplexity = (Π p_i)^(−1/n) = 1 / geomean( p(actual token) )
```

Both statements are the same arithmetic. The first is how you compute it; the second is why it behaves the way it does.

## What 26 means

[GPT-2 small](/wiki/ai/llm/gpt-2) scores about 26 on WikiText, from a loss near 3.28. The vocabulary is 50,257 tokens, so a model guessing uniformly would score 50,257. GPT-2 has narrowed fifty thousand options down to an effective twenty-six — at each token it's about as unsure as someone rolling a fair 26-sided die, no matter that the real menu is two thousand times longer.

The die is the analogy to hold. A fair six-sided die has perplexity 6 however you label its faces, because perplexity measures uncertainty, not vocabulary. Loading the die — making some faces likelier — drops it below 6. A model that had memorized the text perfectly would face a one-sided die: perplexity 1, the floor.

```text
  perfect      GPT-2 on WikiText     uniform guess       confidently wrong
    1 ──────────────── 26 ─────────────── 50,257 ─────────────────▶  no ceiling
 (floor)          (effective            (vocabulary
                branching factor)          size)
```

Note the right end. Uniform guessing scores the vocabulary size, but that is *not* a ceiling — it's just the score of knowing nothing. A model that is confidently *wrong*, putting its mass on a token that then doesn't appear, assigns the real token less than uniform's `1/50257` and scores *worse* than 50,257. Perplexity is bounded below by 1 and unbounded above; ignorance and error live on opposite sides of the uniform line.

## Why the worst tokens set the price

Because perplexity is a geometric mean, one token can dominate it. Assign a probability near zero to a token that actually occurs and its reciprocal is enormous; the `n`-th root tames it, but a single genuine surprise still drags the whole average up more than a run of confident hits pulls it down. This is [the loss's calibration bias](/wiki/ai/llm/the-loss-function) seen through the metric: the model is scored on its worst moments, so hedging on the tokens it's unsure of buys more than sharpening the ones it already has. A model that knows what it doesn't know reports a lower perplexity than one that's occasionally, loudly wrong.

## The comparability trap: it's per-token

Perplexity is an average *per token*, and different tokenizers cut the same sentence into different numbers of tokens. A model with a larger or smarter vocabulary spends fewer, individually-easier predictions on the same text, and reports a lower perplexity that says nothing about whether it models the *language* better — only that it chopped the text into coarser pieces. Two perplexities are comparable only when they come from the same tokenizer on the same corpus. A perplexity quoted without both is a number you cannot use.

The fix when you must cross tokenizers is to normalize away the token count entirely: measure **bits per byte** or **bits per character** — the model's total surprise in bits divided by the length of the raw text, not the token stream. That lets a byte-level model and a [BPE](/wiki/ai/llm/tokenization) model be compared on equal terms, because bytes are bytes whatever the vocabulary. It's why GPT-2's own paper reports its headline WikiText figure of 29.41 with detokenizers in the loop, and why a short strided sample gives the friendlier 26 the rest of these pages quote: same model, two measurement protocols, and knowing which one you're holding is the whole skill.

## A number is only as good as its corpus

Perplexity measures fit to *a distribution*, so it moves with the text. GPT-2's 26 on WikiText becomes a different number on code, on chat logs, on its own training data. And it measures prediction, not usefulness: an [instruction-tuned](/wiki/ai/llm/rlhf) model reliably scores *worse* perplexity on raw prose than its base model — Qwen2.5-0.5B goes from 17.9 to 20.0 — while being far more useful to talk to. Past a point, lower perplexity and "better model" come apart. Treat it as a sharp instrument for one narrow question — how well does this model predict this text? — and not as a verdict on quality.

## Check yourself

Perplexity's floor and its missing ceiling are both a few lines to confirm on GPT-2 small. Tokenize a run of one repeated token — `"a a a a a a a a a a"` — and evaluate [`torch.exp(model(ids, labels=ids).loss)`](/wiki/ai/llm/running-the-checks). After the first, the model is nearly certain the next token repeats, so the per-token loss collapses and perplexity comes back barely above 1: the one-sided die.

Now the other extreme: feed `torch.randint(0, 50257, (1, 512))` — uniformly random token ids — through the same call. Perplexity lands not near 50,257 but well past it, into the tens of thousands. The model isn't merely ignorant of what random noise comes next; it's confidently expecting real English and getting garbage, and being confidently wrong scores worse than the uniform guess. Break either result and you've misunderstood what the number counts.

## Depends on / leads to

Depends on [the loss function](/wiki/ai/llm/the-loss-function). Leads to [backprop through one weight](/wiki/ai/llm/backprop-one-weight).
