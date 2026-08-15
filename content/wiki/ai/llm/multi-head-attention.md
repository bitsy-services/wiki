---
title: "Multi-Head Attention"
weight: 160
---

Multi-head attention is the arrangement that lets one block chase many relationships at once. A single [head](/wiki/ai/llm/glossary) can track exactly one kind of connection between words, because it has only one [attention pattern](/wiki/ai/llm/glossary) to spend — one set of proportions over the words it can see — and any real sentence contains several kinds of connection at the same time. The answer is not to build a cleverer head but to run a batch of ordinary ones side by side over the same words, each free to specialize in something different, and add up what they all found. They never communicate with each other, which is precisely what keeps their findings from smearing together.

## Why one head isn't enough

A head produces one pattern per row, and that pattern has to serve every purpose the row has at once.

Take *"the tired dog by the river barked."* The row for `" barked"` has several unrelated pieces of business. It needs to find its subject, four tokens back. It might separately want the adjective attached to that subject. It might want to know that a prepositional phrase intervened, so it doesn't mistake `" river"` for the thing doing the barking.

One head cannot do all three, and the reason is worth stating precisely, because the obvious version of it is wrong. It is *not* that the blend is unrecoverable — summing near-perpendicular directions is exactly how [the residual stream](/wiki/ai/llm/residual-stream) carries many things at once, and [superposition](/wiki/ai/llm/superposition) is the whole account of why that works.

The real limit is that **a pattern assigns one weight per source row, and that weight applies to everything the row is offering.** The head cannot attend to `" dog"` heavily for the subject question while attending to `" river"` heavily for the intervening-phrase question — there is one set of proportions, and every purpose is served by the same one. Add that a head has only 64 dimensions to keep its answers apart in, and one head is committed to one relationship whether it likes it or not.

**Widening the head doesn't fix it.** This is the part people expect to work and it doesn't. Give a head 768 numbers to work with instead of 64 and it can draw much finer distinctions *within* the one relationship it's tracking — but it still has one pattern, still produces one average. Width buys precision in a single question; it never buys a second question.

## The output is divided, not the input

So the block runs twelve heads. What it does *not* do is make the row twelve times wider. The twelve results are 64 numbers each, and 12 × 64 = 768 — [GPT-2 small](/wiki/ai/llm/gpt-2)'s row width exactly, so the block writes back the same width it read.

Be careful about what is divided, because the arithmetic invites a misreading. Head 7 does not get 64 of the row's 768 numbers. **Every head reads the entire row**, through its own [Q/K/V projections](/wiki/ai/llm/qkv-projections), and projects it down into its own private 64-dimensional subspace — a different subspace per head, all of them views of the same complete input. What gets divided twelve ways is the *output* width, not the input.

The twelve 64-wide results are then laid end to end back into 768 numbers, passed through one shared output matrix, and added to [the residual stream](/wiki/ai/llm/residual-stream) as a single write. Twelve independent reads, one write.

```text
                              depth  →

  pos 0  "The"     ─┐
  pos 1  " tired"  ─┤     ┌────┬────┬────┬───┬─────┬─────┐
  pos 2  " dog"    ─┤     │ h0 │ h1 │ h2 │ … │ h10 │ h11 │ ──▶ one output
  pos 3  " by"     ─┼──▶  │ 64 │ 64 │ 64 │   │  64 │  64 │     matrix, then
  pos 4  " the"    ─┤     └────┴────┴────┴───┴─────┴─────┘     added to the
  pos 5  " river"  ─┤     └──────────── 768 ───────────┘       stream
  pos 6  " barked" ─┘

  every head reads every row it's allowed to, in full;
  no head reads another head
```

The arithmetic works out to roughly what one 768-wide head would have cost, so the specialization is close to free. That is the whole bargain: same budget, twelve questions instead of one.

Think of a panel of twelve specialists handed the same document, each with a different brief, whose notes are stapled together at the end — rather than one generalist reading it twelve times and trying to keep the readings straight.

## What they specialize in

The briefs are learned, not assigned, and they turn out to be surprisingly legible. Some heads do something close to *the previous token, always*. Some track the matching bracket or quotation mark. And some pair up into [induction circuits](/wiki/ai/llm/qkv-projections#the-split-matters-more-than-the-names), which continue a pattern the model watched happen a few tokens ago and has never seen before — a two-head arrangement whose mechanics are more interesting than the one-line summary suggests, and which are worth reading on their own page rather than taking on trust here.

## They are wildly uneven

Here is where the tidy picture breaks down, and it's the most interesting fact on this page.

"Twelve heads per block" suggests twelve comparable contributors, a team pulling roughly together. The ablation curve says otherwise. Delete heads one at a time and most of them cost almost nothing — a fair number make the model *better* when removed. A handful are catastrophic. And the catastrophic ones cluster in block 0, the earliest reads, which every block to their right is built on top of.

So the honest description isn't a panel of twelve specialists. It's two or three load-bearing ones, and a long tail of heads that have found something mildly useful to do or nothing at all.

## The part that didn't survive

That every head owns *all three* of its projections is a GPT-2-era choice, and the one piece of this arrangement modern models abandoned. Keys and values are the expensive things to keep around at serving time, so today's models give each head its own query but make groups of heads share a single key and value — [grouped-query attention](/wiki/ai/llm/grouped-query-attention), whose motive is the memory arithmetic on [the KV cache](/wiki/ai/llm/kv-cache) page. The division of labour survived; the private copies didn't.

## Check yourself

[Ablate heads](/wiki/ai/llm/running-the-checks) one at a time in GPT-2 small: zero head *h* of block *b*, measure [perplexity](/wiki/ai/llm/perplexity) on a few hundred tokens of WikiText, restore, repeat for all 144. Median damage is under 1%, and about twenty heads make perplexity *better* when deleted. Then look at the tail: block 0 head 10, on its own, takes perplexity from ~26 to ~145. The distribution isn't long-tailed so much as vertical.

## Depends on / leads to

Depends on [Q/K/V](/wiki/ai/llm/qkv-projections). Leads to [the MLP](/wiki/ai/llm/multi-layer-perceptron), the other half of a block.
