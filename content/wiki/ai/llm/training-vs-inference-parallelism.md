---
title: "Training vs Inference Parallelism"
weight: 280
---

The same model, doing the same arithmetic with the same weights, behaves like an entirely different piece of software depending on whether it is being trained or being used. Training reads a whole document at once and is limited by how fast the hardware can multiply. Generation produces its output a word at a time, each word depending on the one before, and is limited by something else altogether — how fast the weights can be dragged out of memory. Nearly every surprising fact about what serving a model costs, and every trick anyone uses to make it cheaper, comes out of that split.

## Training does every row at once

One forward pass over a 1024-token sequence computes all 1024 rows in parallel and scores 1023 next-token predictions. [The causal mask](/wiki/ai/llm/causal-mask) is what makes that legal — no row can see ahead, so every row can be graded honestly at the same time.

The hardware sees enormous matrix multiplies. It is **compute-bound**: the arithmetic units are the bottleneck, which is the comfortable case, and it's why training is a throughput problem you solve by buying more **FLOPs** — floating-point operations, the raw count of arithmetic a machine can get through.

## Inference can't

Token 501 depends on token 500, and token 500 has to be sampled before it exists. There is no way around that — it's what generating text *means*. Generation is strictly serial: one row, one forward pass, repeat.

So far this sounds merely slower. The genuinely surprising part is what it's slow *at*.

## Why decode is slow at something other than arithmetic

The serial half of inference has a name — **decode**, the token-at-a-time emission of new text, as distinct from **prefill**, the single parallel pass that chews through the prompt you supplied. Prefill behaves like training. Decode is the interesting one.

With a [KV cache](/wiki/ai/llm/kv-cache) in place, the arithmetic per decoded token is trivial. You push a single 768-wide row through 124M weights and get roughly one multiply out of each one. Every weight in the model is read from memory; not one of them is *reused* before it's discarded.

Compare the training pass. It reads exactly the same 124M weights and puts each one to work a thousand times over, once per row in the sequence.

The quantity that differs is **arithmetic intensity** — how much arithmetic you perform per byte you move. Training's is high, so the arithmetic units stay fed. Decode's is about as low as it can be, so the units sit idle waiting on memory, and the run is **memory-bandwidth-bound**.

Note what that means when you're serving a single conversation on its own — a **batch size** of one, in the vocabulary of the next section. Decoding is not limited by how much computing your GPU can do. Most of the GPU is doing nothing at all.

It's a factory press. Training is a production run — set the machine up once, stamp out a thousand parts, and the setup cost disappears into the total. Decode is stamping a single part, tearing the machine down, setting it up again, and stamping one more. The stamping was never the slow part.

## Three consequences

**Batching is enormously effective at inference.** The **batch size** is simply how many sequences are pushed through together, and if the weights are being read from memory anyway, many sequences can ride along on the same read at almost no extra cost. That's why per-token prices fall with scale, and why a busy server is a cheap server.

**Prefill and decode are different regimes.** Chewing through the prompt is parallel and fast, exactly like training; emitting tokens is serial and slow. They should be measured, budgeted, and optimized separately, and a benchmark that reports one number for both is hiding the interesting half.

**Idle compute is available to be spent.** [Speculative decoding](/wiki/ai/llm/speculative-decoding) exists precisely because decode leaves the arithmetic units unemployed — it converts some serial decode back into parallel verify, buying speed with FLOPs that were going to waste anyway.

## Check yourself

Time [GPT-2 small](/wiki/ai/llm/gpt-2) on 1024 tokens as [one forward pass](/wiki/ai/llm/running-the-checks), then time generating 1024 tokens one at a time with the cache on. Same model, same token count. On CPU the forward pass wins by roughly 10×. On a GPU — where the parallel pass consumes FLOPs that were sitting idle anyway — it's two orders of magnitude. The hardware decides the size of the gap; nothing makes it vanish.

## Depends on / leads to

Depends on [the causal mask](/wiki/ai/llm/causal-mask) and [the KV cache](/wiki/ai/llm/kv-cache). Leads to [speculative decoding](/wiki/ai/llm/speculative-decoding).
