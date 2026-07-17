---
title: "Why Scale Worked"
weight: 350
---

Modern language models are not good because someone discovered a smarter way to read a sentence. They are good because someone discovered a way to train on far more writing than anyone had trained on before — and it turned out that more writing was what the problem had been short of all along. The insight everyone quotes is attention. The insight that did the work is duller: this design can turn a bigger budget into more text read, and the design it replaced could not. This page argues the second one is load-bearing and the first is mostly a means to it.

That is a claim about economics rather than intelligence, which is why it tends to get skipped. It is also the claim that best explains what happened.

## The half that was already free

Start by disposing of a tempting wrong answer: that the transformer's gift was free training data.

It wasn't, because that part was never scarce. Next-token prediction supervises itself — [the loss function](/wiki/ai/llm/the-loss-function) scores each guess against the token that actually came next, and that token is not an annotation anyone produced. It is just the text, one step along. Every sentence ever written is already labelled, by itself, for free.

And this is *old*. Neural language models were trained this way in 2003, and recurrent ones throughout the 2010s: the previous generation that [attention](/wiki/ai/llm/attention) describes were next-token predictors too, learning from raw text with nobody marking anything up. The free lunch sat on the table for fifteen years before it fed anyone. If self-supervision were the insight, GPT-3 would have arrived in 2012.

So the corpus was never the constraint. The text was free, it was already labelled, and there was more of it than anyone could use. The question is why nobody used it.

## The half that wasn't: the machine can't help

Because the old design could not turn a bigger budget into more text read.

Two wrong versions of that complaint are worth clearing away first, because both are the sort of thing that gets said and neither survives contact with someone who knows the material.

**It isn't that recurrence left the machine idle.** You can run many *sequences* side by side, and recurrent models were trained on real hardware perfectly respectably. Batching works. What recurrence precludes is parallelism *within* a single sequence — which is exactly how the transformer's authors framed their own contribution, not as a side effect but as the headline.

**Nor is it that recurrence couldn't be made wide.** It could. The big recurrent language models of 2016 carried a running summary eight thousand units across, and width costs the hardware nothing in structure: a wider summary is a bigger matrix multiply, and a bigger matrix multiply is precisely what the machine wants.

The real problem is the one thing neither of those fixes. Position 50 cannot begin until position 49 has produced its summary, so a training step contains a chain of operations as long as the text, and **no quantity of hardware shortens a chain**. For a while you can hide that: buy more machines, run a bigger batch, push more tokens through each step. But batch parallelism saturates. Past a certain point — the *critical batch size* — adding more sequences to a step stops reducing the number of steps you need to converge, and you are simply spending more compute for the same progress. It's an empirical measurement rather than a theorem, and it isn't even a constant: it drifts upward as training proceeds. But it is finite at every moment, and that is all a ceiling needs to be.

Once you're against it, the only lever left is making each step faster — and that's exactly the lever recurrence doesn't have. The transformer has a chain of its own, mind: its blocks run one after another, as the diagram below shows, and hardware doesn't shorten that either. The difference is that the transformer's chain is a fixed length, set by the architecture, and recurrence's grows with every token you add. One of those designs gets slower per step as you feed it more text. The other doesn't.

The scoreboard tracks it. The recurrent line reached about a billion training tokens and stopped: the big 2016 models trained on a billion-token benchmark, and so did the best-known recurrent language model of 2018. GPT-3, in 2020, trained on roughly three hundred billion. It would be too neat to hand the architecture credit for all of that — compute budgets grew enormously across the same window, and 2018's transformers trained on about as much text as 2018's recurrent models did. But that *is* the point rather than an objection to it. When the money arrived, only one of the two designs did absorb it.

## What the transformer actually changed

It cut the chain loose from the text. Within a single step, no position waits on any other — attention does move information between positions, that being its entire job, but every query reads material the *previous* step already deposited in [the residual stream](/wiki/ai/llm/residual-stream), never output from the step it is currently in. So the sequence contributes no depth of its own. A thousand-token document and a ten-token one pass through the same fixed stack of blocks, and each computes all its positions at once. Feed it more text and the queue doesn't lengthen; only the width of the work does — which is the kind of growth hardware absorbs.

```text
                        depth  →

  recurrence — the arrow that ruins it runs DOWN the sequence

  pos 0  "The"   [ h0 ]
                    │  carries everything so far
  pos 1  " cat"  [ h1 ]
                    │
  pos 2  " sat"  [ h2 ]
                    │
  pos 3  " on"   [ h3 ]

  h3 cannot start until h2 exists. Four positions, four steps,
  strictly ordered. More hardware does not shorten that chain.

  transformer — no arrow runs down WITHIN a step

  pos 0  "The"   [···]──[···]──▶ predicts " cat"
  pos 1  " cat"  [···]──[···]──▶ predicts " sat"
  pos 2  " sat"  [···]──[···]──▶ predicts " on"
  pos 3  " on"   [···]──[···]──▶ predicts " the"

  One pass. Every row at once, and every row scored — four
  supervised predictions for the price of one. Attention still
  mixes the rows vertically; it reads what the step before left,
  so no row waits on a neighbour inside the step.
```

One pass over a document therefore yields not one training signal but one per position, all of them, concurrently, from text that labelled itself. The free lunch was always there. This is the design that could eat it.

It's worth being blunt about what kind of advance that is. Movable type did not make anyone a better writer. It made copies cheap, and cheap copies rearranged Europe. Attention did not make a model better at relating two words than recurrence was in principle — recurrence could relate them too, just slowly and lossily. What it did was make the training cheap. The rearranging followed.

## The part that wasn't guaranteed

Cheap does not imply worthwhile. The transformer made enormous training runs affordable; nothing promised the results would be any good. They could have plateaued at a modest loss and left the field with a very efficient way to build something mediocre.

They didn't, and this is the genuinely surprising fact of the era. Loss keeps falling as you add compute, data, and parameters — smoothly, and predictably enough that you can forecast the loss of a model you have not trained yet from a curve fitted to smaller ones. These are the *scaling laws*, and they are an empirical observation rather than a theorem. There are serious attempts to explain why they hold, but no consensus account, and certainly none that was available in advance to justify the spending.

The second surprise stacks on the first: falling loss cashed out as capability nobody targeted. The objective only ever asked for the next token. Grammar, arithmetic, translation, the ability to close a bracket thirty lines later, something that behaves like reasoning — none were designed in. They appear to be what predicting text well enough *requires*, so they were learned on the way. The [section landing page](/wiki/ai/llm) puts it as competence being a side effect of the guessing game. Scale is what made the side effects worth having.

## So why isn't attention the insight?

Because the essential property has since been delivered without it.

State-space models — Mamba and its relatives — keep a running summary much as recurrence did, but make the state update linear on purpose, which is what lets a whole sequence be resolved in parallel rather than walked one position at a time. Same running summary; no queue.

That buys them the property this page says is load-bearing, without attention and without its quadratic [context](/wiki/ai/llm/context-length) cost — time grows linearly with sequence length instead. They train on the same self-labelling text and land competitive with transformers at the sizes anyone has tried, which, honestly stated, means up to around seven or eight billion parameters. Nothing at frontier scale is a pure state-space model, so the top end is untested. But if attention were the seat of the magic, parity at that size shouldn't happen either.

The honest counter-evidence: it isn't a clean swap. A fixed-size running summary is lossy in a specific, well-documented way — these models are measurably worse at verbatim recall and copying, at reaching back and retrieving *this exact string* from far up the context. Attention has no such trouble, because reaching two hundred positions back is the same single comparison as reaching back one. That's a real capability, and it's why models that do ship with state-space components almost always keep some attention blocks alongside them rather than going without.

So attention buys something genuine: precise retrieval across the context. What it does not buy is the answer to "why do these work at all." The evidence points at the duller property — *trains in parallel, on text that labels itself, at a scale hardware can actually be thrown at* — and attention was simply the first mechanism that delivered it.

## What the frame is good for

Take the economic reading seriously and it tells you where the next wall is, which the architectural reading never does.

If the engine is cheap parallel training over text that labels itself, it runs exactly as long as the text does. The internet is large but finite, the good parts more finite still, and the frontier is now close enough to the bottom of that well that "just add data" has stopped being a plan. That single fact explains most of what the labs are visibly doing: synthetic data, aggressive curation over raw volume, and a centre of gravity that has shifted from pre-training toward [fine-tuning](/wiki/ai/llm/fine-tuning), [RLHF](/wiki/ai/llm/rlhf), and reinforcement learning against checkable outcomes — all of which manufacture training signal rather than find it lying around. When the free lunch runs out, you start cooking.

That's the payoff of getting the insight right. "Attention was the breakthrough" predicts nothing. "Cheap supervision at a scale hardware can chew" predicts the data wall, and predicted it early.

## Check yourself

The argument rests on one claim you can test in a couple of lines: **one forward pass produces a supervised prediction at every position at once, from text that labelled itself.**

Take a 1024-token chunk of anything and run [GPT-2 small](/wiki/ai/llm/gpt-2) as `out = model(ids, labels=ids)`. Look at what you passed: the same tensor, twice. There is no label argument distinct from the input, because there is no label — the model shifts the text by one internally and scores against it. `out.loss` comes back a single scalar averaged over 1023 predictions, and you supplied no annotation to get any of them.

Now test the parallel half. From that one pass, `model(ids).logits[0, k]` is the prediction made at position `k`. Recompute it the expensive way, with a pass that has never seen a token past `k`: `model(ids[:, :k+1]).logits[0, -1]`. The two match for every `k` you care to try — [the causal mask](/wiki/ai/llm/causal-mask) guarantees it, since position `k` could not have peeked forward anyway.

Compare with `atol=1e-4`, and don't expect bitwise equality. The two passes hand the kernel different sequence lengths, so it blocks the matrix multiplies differently and sums them in a different order, and float addition doesn't associate — true on a CPU as much as a GPU. Twelve blocks of that drifts the logits by around `1e-4`. `torch.allclose` at its defaults will report a difference and be wrong about what it means.

Tell noise from a real failure by **magnitude and structure, not trend**. Arithmetic noise is tiny, scattered, and won't reproduce exactly if you re-run it; leakage through the mask would be large, and the difference would *track the actual next tokens*, since those are what the full pass would have been improperly reading. Don't reach for "the gap grows as I truncate more" — it does that either way, because the passes differ more in shape the further apart their lengths are.

Then picture the same test on the recurrent design: 1023 predictions, each waiting on the last, no way to overlap them, and no amount of hardware that shortens the queue. Same predictions, 1023× the serial steps. That gap is the entire reason you have heard of any of this.

## Depends on / leads to

Depends on [attention](/wiki/ai/llm/attention), [the loss function](/wiki/ai/llm/the-loss-function), and [training vs inference parallelism](/wiki/ai/llm/training-vs-inference-parallelism). Nothing follows; this is the last page, and the one the rest of the subsection was evidence for.
