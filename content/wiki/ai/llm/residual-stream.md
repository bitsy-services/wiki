---
title: "The Residual Stream"
weight: 120
---

Every block does this and nothing else:

```text
row = row + attention(norm(row))
row = row + mlp(norm(row))
```

Read it twice. A block never *replaces* the row — it computes something and **adds**. The row leaving block 11 is the [embedding](/wiki/ai/llm/embeddings) plus 24 contributions — 12 attention, 12 MLP, each `d_model` wide (the MLP's bulge is internal; it writes back 768). That running sum is the residual stream, the only thing travelling rightward. Blocks don't hand each other outputs; they read it and write into it.

**It's a bus, not a pipeline.** Block 9's attention can read something block 2 wrote and block 5 never touched — it's all still sitting in the sum. Nothing is relayed hop by hop; information survives by default.

**The output is nearly linear in the contributions.** [Logits](/wiki/ai/llm/glossary) are a linear readout of the final row, and that row is a sum, so you can ask what one block contributed to one logit and get a number. *Nearly*: the final norm rescales by a row-dependent factor, which the logit lens and direct logit attribution hold fixed.

**Bandwidth is fixed.** `d_model` doesn't grow rightward, so all 24 writes compete for the same 768 directions. Models pack far more features than dimensions — superposition, on the [backlog](/wiki/ai/llm/backlog).

## Check yourself

In GPT-2 small, zero block 6's attention output and measure perplexity on a few hundred tokens of WikiText: it rises about 15–20% and the text stays fluent — the stream carries everything else around the hole. Now zero the *whole* stream entering block 6: perplexity blows up four orders of magnitude and output degenerates into repetition. A missing contributor versus a cut bus.

## Depends on / leads to

Depends on [embeddings](/wiki/ai/llm/embeddings). Leads to one attention head and the MLP — unwritten; see the [backlog](/wiki/ai/llm/backlog).
