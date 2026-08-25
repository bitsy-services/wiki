---
title: "Why Scale Worked"
weight: 350
---

Language models got good because the field found a way to train on far more writing than anyone had trained on before — not because anyone found a smarter way to read a sentence. The writing was always there, and it was always free. What changed is that the transformer can turn a bigger hardware budget into more text read, and the design it replaced could not. Attention is how that was achieved. The achievement is the cheapness.

## The text was never the constraint

Next-token prediction supervises itself. [The loss function](/wiki/ai/neural-network/the-loss-function) scores each guess against the token that actually came next, and that token is not an annotation anybody wrote — it is just the text, one step along. Every sentence ever written is already labelled, by itself, for free.

That is not a new observation. Neural language models were trained this way in 2003, and recurrent ones all through the 2010s, on the same unlabelled text. If free supervision were the insight, GPT-3 would have arrived in 2012. The corpus was never the shortage; getting through it was.

## Recurrence turns a document into a queue

A recurrent model reads a sequence one position at a time, carrying a running summary forward. Position 50 cannot start until position 49 has produced its summary. A training step on a thousand-token document therefore contains a thousand strictly ordered operations, and **no quantity of hardware shortens a chain**.

The two obvious escapes don't work.

**Run more sequences side by side.** You can, and people did — but batch parallelism saturates. Past the **critical batch size**, adding more sequences to a step stops reducing the number of steps needed to converge, and you are buying compute that buys nothing. It's measured rather than derived, and it drifts upward as a run proceeds, but it is finite at every moment, which is all a ceiling has to be.

**Make the model wider.** You can do that too — 2016's recurrent language models carried summaries eight thousand units across — and it doesn't help, because width was never the problem. A wider summary makes each link in the chain do more work. It does not make the chain shorter.

## Attention replaces the queue with a matrix multiply

Both designs have to move information between positions; that's what reading a sentence in context means. They do it differently.

Recurrence moves it by **relay**. To get a fact from position 0 to position 999, it hands the fact down 999 times, and each hop waits on the one before it. [Attention](/wiki/ai/llm/attention) moves it by **lookup**. Every position emits a **query** — what it is looking for — and a **key** — what it has to offer. Position 999 scores its query against all thousand keys in a single operation, and position 0 is exactly as reachable as position 998.

What makes that operation parallel is where the keys come from. Everything a query reads inside block *k* was deposited in [the residual stream](/wiki/ai/llm/residual-stream) by block *k−1*; it is already sitting there before the block starts. No position in a block waits on any other position in the same block. And once every query and every key exists up front, scoring them is one multiplication rather than a thousand: stack the queries as the rows of one matrix, the keys as the columns of another, and a single matrix multiply drops out every query-against-key score in the sequence. So the block resolves all thousand positions at once, and the only thing left running in order is the blocks themselves — twelve in [GPT-2 small](/wiki/ai/llm/gpt-2), whatever number the architecture fixes, and the same number for a ten-token document as for a ten-thousand-token one.

**The speedup is entirely of *training***, which is the half that eats the budget. [Generation gets none of it](/wiki/ai/llm/training-vs-inference-parallelism), because the next token cannot be attended to before it exists. Recurrence's serial depth is the length of the text. The transformer's serial depth is the block count, a constant. Feed it more text and the work gets *wider*, not *longer* — and width is the one direction hardware can be thrown at.

Note what this is not. The transformer didn't win by doing less arithmetic — attention adds work recurrence never had to do, growing with the *square* of the sequence length where recurrence's grows linearly, which is why [context length](/wiki/ai/llm/context-length) is expensive. The trade is arithmetic for the shape of it: more operations, arranged so they can all happen at once. On a GPU that is a very good trade, because a GPU's problem is never having too much work to do. It is being made to wait.

And because [the causal mask](/wiki/ai/llm/causal-mask) stops any row from seeing ahead, every row can be graded honestly in that same pass. One pass over a thousand-token document yields a thousand supervised predictions, all at once, from text that labelled itself. The recurrent model produces the same thousand predictions one at a time.

```text
                        depth  →

  recurrence — the chain runs DOWN the sequence

  pos 0  "The"   [ h0 ]
                    │  h1 cannot start until h0 exists
  pos 1  " cat"  [ h1 ]
                    │
  pos 2  " sat"  [ h2 ]
                    │
  pos 3  " on"   [ h3 ]

  Four positions, four ordered steps.

  transformer — the chain runs ACROSS the blocks

  pos 0  "The"   [···]──[···]──▶ predicts " cat"
  pos 1  " cat"  [···]──[···]──▶ predicts " sat"
  pos 2  " sat"  [···]──[···]──▶ predicts " on"
  pos 3  " on"   [···]──[···]──▶ predicts " the"

  Attention still mixes the rows vertically, but it reads what the
  previous block left behind, so no row waits on a neighbour.
  Four positions, two ordered steps. Forty thousand positions,
  still two.
```

## What that bought

The best recurrent language models of 2016 trained on a one-billion-word benchmark, and so did the best-known recurrent model of 2018. GPT-3, in 2020, trained on roughly three hundred billion tokens. Compute budgets grew enormously over the same window, so the architecture doesn't get sole credit — but that is the point rather than an objection to it. When the money arrived, only one of the two designs could absorb it.

Nothing guaranteed the results would be worth having. Cheap training is not good training, and the runs could have flattened out at a mediocre loss. Instead loss kept falling as compute, data, and parameters grew — smoothly, and predictably enough to forecast the loss of a model you have not trained from a curve fitted to smaller ones. These are the **scaling laws**: an empirical observation with no agreed explanation, and certainly none available in advance to justify the spending. Falling loss then cashed out as capability nobody targeted. Grammar, arithmetic, translation, something that behaves like reasoning — none were designed in. They appear to be what predicting text well enough *requires*.

The **Chinchilla** correction in 2022 raised the bill. Scaling laws say loss falls as you spend more; they don't say how to split a fixed budget between a bigger model and more text. The 2020 answer favoured parameters heavily, and the field duly raced to hundreds of billions of weights trained on comparatively little writing. Chinchilla redid the measurement and found that advice badly wrong: parameters and tokens should grow roughly *in step*, on the order of twenty tokens per parameter. A 70B model trained on 1.4 trillion tokens beat a 280B model trained on 300 billion, at matched compute. Practically every large model of the preceding era had been starved of text.

Models today are trained well past even that point — Llama 3's 8B model was fed 15 trillion tokens — because a model that is expensive to train once and cheap to serve forever is worth over-training. Every step in that direction wants more text still.

## Attention isn't the only way to get it

If the parallel-training property is what mattered, and not attention specifically, you would expect something else to deliver it eventually. Something has.

State-space models — Mamba and its relatives — keep a running summary much as recurrence did, but make the state update linear on purpose, which is what lets a whole sequence be resolved at once instead of walked. Same summary, no queue, and no quadratic cost either. They train on the same self-labelling text and land competitive with transformers at the sizes anyone has tried, which honestly stated means up to around eight billion parameters. Nothing at frontier scale is a pure state-space model, so the top end is untested — but if attention were the seat of the magic, parity even at that size shouldn't happen.

Where they *are* worse is telling: verbatim recall, reaching back and retrieving *this exact string* from far up the context. A fixed-size summary loses detail; attention doesn't, because reaching back two hundred positions is the same single comparison as reaching back one. That is what attention genuinely buys, and it's why models shipping state-space components almost always keep some attention blocks alongside them. It is not what made scale work.

## Where the engine runs out

If what drives all this is cheap parallel training over text that labels itself, it runs exactly as long as the text does. The internet is finite, the good parts more finite still, and the frontier is close enough to the bottom of that well that "add more data" has stopped being a plan. That single fact explains most of what the labs are visibly doing: synthetic data, hard curation over raw volume, and a centre of gravity shifting from pre-training toward [fine-tuning](/wiki/ai/llm/fine-tuning), [RLHF](/wiki/ai/llm/rlhf), and reinforcement learning against checkable outcomes — all of which manufacture training signal rather than find it lying around.

"Attention was the breakthrough" predicts nothing. "Cheap supervision at a scale hardware can chew" predicted the data wall, and predicted it early.

## Check yourself

The argument rests on one claim you can test in a couple of lines: **one forward pass produces a supervised prediction at every position at once, from text that labelled itself.**

Take a 1024-token chunk of anything and run GPT-2 small as [`out = model(ids, labels=ids)`](/wiki/ai/llm/running-the-checks). Look at what you passed: the same tensor, twice. There is no label argument distinct from the input, because there is no label — the model shifts the text by one internally and scores against it. `out.loss` comes back a single scalar averaged over 1023 predictions, and you supplied no annotation to get any of them.

Now the parallel half. From that one pass, `model(ids).logits[0, k]` is the prediction made at position `k`. Recompute it the expensive way, with a pass that has never seen a token past `k`: `model(ids[:, :k+1]).logits[0, -1]`. The two match for every `k` you try, because [the causal mask](/wiki/ai/llm/causal-mask) meant position `k` could not have peeked forward anyway.

Compare with `atol=1e-4`, not bitwise. The two passes hand the kernel different sequence lengths, so it blocks the matrix multiplies differently and sums them in a different order, and float addition doesn't associate — true on a CPU as much as a GPU. Twelve blocks of that drifts the logits by around `1e-4`, and `torch.allclose` at its defaults will report a difference and be wrong about what it means. Tell noise from a real failure by magnitude and structure: arithmetic noise is tiny, scattered, and won't reproduce exactly on a re-run, whereas leakage through the mask would be large and would *track the actual next tokens*.

Then picture the same test on the recurrent design: the same 1023 predictions, each waiting on the last, and no amount of hardware that shortens the queue. That gap is the entire reason you have heard of any of this.

## Depends on / leads to

Depends on [attention](/wiki/ai/llm/attention), [the loss function](/wiki/ai/neural-network/the-loss-function), and [training vs inference parallelism](/wiki/ai/llm/training-vs-inference-parallelism). Nothing follows; this is the last page, and the one the rest of the subsection was evidence for.
