---
title: "Grouped-Query Attention"
weight: 265
---

When a model is served to real users, the thing that fills the graphics card is not always the model. It's the pile of remembered arithmetic kept for every token of every conversation in flight — and [multi-head attention](/wiki/ai/llm/multi-head-attention) makes that pile as large as it can possibly be, by giving every head its own private copy. Grouped-query attention is the observation that they don't all need one. Put the heads in groups, let a group share, and most of the memory goes away while the model carries on asking just as many questions as before. It costs a little quality, and it is why essentially every model served at scale today is built this way.

## The cache is the bill

[The KV cache](/wiki/ai/llm/kv-cache) is the trade that makes generation affordable: keep each row's key and value once computed, because [the causal mask](/wiki/ai/llm/causal-mask) guarantees nothing arriving later can change them. The cost is memory, and it grows with every token.

For [GPT-2 small](/wiki/ai/llm/gpt-2) that cost is a rounding error. Two tensors per block per row, 12 blocks, 768 numbers wide: 18,432 numbers per token, 36 KB in fp16. A full 1024-token context holds 36 MB of cache. Nobody has ever worried about it.

Now scale up. Llama 2 70B has 80 blocks and 64 heads per block, each head 128 numbers wide, so a single token costs `2 × 80 × 64 × 128` = 1.3M numbers — **2.5 MB per token**, against GPT-2's 36 KB. One 4,096-token conversation carries **about 10 GB** of cache. The weights are already about 140 GB in fp16 and spread across several cards; every concurrent conversation now demands another ten on top.

That is the whole problem, and it's an economic one. Serving models is a batch business — you make money by running many conversations at once on hardware you've already paid for — and the cache is what caps how many fit. Halve it and you double the customers per card.

## The only term you can touch

The size of the cache multiplies out as `2 × blocks × heads × head width`, per token. Look at what's actually available in that product.

**Blocks** and **head width** are the model's capacity; cutting them makes it worse at its job in the obvious way. The factor of **2** is keys and values, and you need both. That leaves **heads** — and heads are the one term where the model might be doing redundant work, because every head builds its own key and value for the same row.

## Queries are the questions; keys and values are the index

Here is the split that makes the whole thing work. In multi-head attention, each head has three projections of its own: a query, a key, and a value. The query is the question that head is asking. The key and value are the index it searches and the content it retrieves.

Only the key and the value get cached. The query is computed fresh for the current row and thrown away.

So the two are not symmetric at all, and it's worth asking whether they need to be treated as though they were. **Grouped-query attention keeps every head's query private and shares the keys and values within a group.** Sixty-four heads, eight groups: eight heads share each key/value pair, the cache shrinks eightfold, and the model still asks sixty-four distinct questions.

Three arrangements side by side — multi-head attention as GPT-2 does it, grouped-query in the middle, and at the far end **multi-query attention** (MQA), where all sixty-four heads share a single key and value between them:

```text
  MHA — GPT-2            GQA — Llama 2 70B         MQA
  ───────────            ─────────────────         ───
  q0 ── k0,v0            q0 ─┐                     q0 ─┐
  q1 ── k1,v1            q1 ─┤                     q1 ─┤
  q2 ── k2,v2            q2 ─┤                     q2 ─┤
  q3 ── k3,v3            q3 ─┼── k0,v0             q3 ─┼── k0,v0
   ┆       ┆             q4 ─┤                      ┆  ┤
  q11 ─ k11,v11          q5 ─┤                     q63─┘
                         q6 ─┤
                         q7 ─┘
                          ┆
                         q63 ── k7,v7
  12 heads, 12 K/V       64 heads, 8 K/V           64 heads, 1 K/V
```

The analogy that fits: sixty-four researchers, each with a different question, all working through the same library. Multi-head attention gives every researcher a private card catalogue, separately built, of the same books — sixty-four catalogues to maintain. Grouped-query attention builds eight and lets groups of eight researchers share. Nobody's question changes. They just stop each keeping a personal index of the same shelves.

## A dial, not a design

The number of groups is a knob, and both ends of it already have names:

- **Groups = heads.** Every head has its own key and value. This *is* multi-head attention — not merely similar to it, but arithmetically the same thing.
- **Groups = 1.** Every head shares one key and value — multi-query attention, the right-hand column above, and the older of the two ideas by four years. The cache is as small as it goes, but quality drops and training gets unstable.
- **Anything between.** That's GQA. Llama 2 70B and the Llama 3 models use eight.

Why eight, specifically? Honestly, because eight tested well. The GQA paper measured speed against quality across group counts and picked eight as, in its words, "a favorable middle ground." There's no deeper principle, and it's worth resisting the temptation to invent one.

The hardware does get a say, but not the one you'd expect: it doesn't justify eight groups so much as it kills the alternative. Llama 2's largest models are served on a node of eight accelerators using **tensor parallelism** — the heads of each block split across the devices so each holds a slice of the work. At eight groups, every device owns exactly one key/value head and needs nothing from its neighbours. Multi-query attention cannot beat that: with a single key/value head and eight devices there is nothing to split, so the head is duplicated onto every device and the cache ends up the same size grouped-query attention's would have been — while being worse at the job. At eight-way parallelism MQA's entire advantage evaporates, which is a large part of why the middle of the dial, and not the end of it, is what shipped.

## You don't have to start over

The reason GQA spread as fast as it did is that nobody had to throw away a trained model to adopt it.

An existing multi-head checkpoint can be **uptrained** into a grouped one: average the key projections of the heads within each group into a single projection, do the same for the values, then continue training for a small fraction — around 5% — of the compute the original run took. The result lands close to the multi-head model it came from, at the grouped model's memory. A frontier model represents months of compute; converting one over a long weekend is a different proposition from retraining it, and that practicality is most of why the technique won.

## What it costs

Quality, a little. Eight groups sits close to full multi-head attention and comfortably above the one-group extreme — the middle of the dial is where the curve is kind, which is the empirical finding the whole technique rests on. It also trims a few parameters, since there are fewer key and value matrices, but that's incidental. Nobody adopted GQA to save parameters. They adopted it to fit more conversations on the card.

## Check yourself

**Prove it's a true generalization.** Grouped-query attention with one group per head should be multi-head attention exactly, so make it prove that. In [nanoGPT](/wiki/ai/llm/running-the-checks), project the keys and values to `n_kv_head` heads instead of `n_head`, then `repeat_interleave` them back up to `n_head` before the score matmul. Set `n_kv_head = n_head = 12`, load GPT-2 small's weights, and run: the logits come out **bit-identical** to the stock model, because repeating twelve heads into twelve groups of one is the identity function. If they don't match, your implementation isn't GQA — it's a different model wearing the name.

**Then try to make it cheaper, and find out you can't just flip it.** Set `n_kv_head = 2` and the model won't even load. nanoGPT fuses the three projections into one matrix, `c_attn` of `[768, 2304]`, and with two key/value heads that becomes `768 + 2 × 2 × 64` = `[768, 1024]` — so `from_pretrained`'s shape assertion fires long before any token comes out. Notice what that means about the first experiment: `n_kv_head = n_head` is the *only* setting where the fused shape survives untouched, which is exactly why it was free.

To get anywhere you have to do the conversion by hand — mean-pool each group's six key heads into one, the same for the values, and assemble the `[768, 1024]` weight yourself. That's uptraining's first step, performed on a model that then gets none of uptraining's retraining. Do it and the model runs, the cache drops sixfold, and the [loss](/wiki/ai/llm/the-loss-function) is clearly worse. Nothing is broken: those weights were trained as twelve independent key/value heads, and averaging six of them into one destroys information that no amount of shape-juggling restores. The gap you just measured is what that 5% of retraining compute is buying. Which is the real lesson — grouped-query attention is a decision made at *training* time that pays off at inference, not a switch you can throw on a finished model.

## Depends on / leads to

Depends on [the KV cache](/wiki/ai/llm/kv-cache) and [multi-head attention](/wiki/ai/llm/multi-head-attention). Leads to [context length and the O(n²) cost](/wiki/ai/llm/context-length).
