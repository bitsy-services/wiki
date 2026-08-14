---
title: "Conventions"
weight: 10
---

Every diagram and sentence here uses one layout, declared once so no page has to re-orient you.

- **Depth runs left to right.** Embedding at the left edge, block 0 next, block 11 further right, unembedding at the right edge. A vector that has been through more blocks is *further right*. Never "deeper," never "up the stack."
- **Sequence runs top to bottom.** One token position is one row: first token on top, the token you're predicting from at the bottom.
- **The feature axis is row width.** A row is `d_model` numbers wide, and the only thing that changes that is the MLP bulge — which changes it straight back.

```text
                        depth  →

  pos 0  "The"   [···········]──[···········]──▶ logits
  pos 1  " cat"  [···········]──[···········]──▶ logits
  pos 2  " sat"  [···········]──[···········]──▶ logits
    │
    ▼             embed          block 0 … 11
 sequence        └── d_model ──┘
```

## What the layout buys you

[Attention](/wiki/ai/llm/attention) moves information *between rows* — a row reads the rows above it. The MLP moves it *within a row*, never looking at another. Here that's literally vertical versus horizontal: the cleanest one-sentence account of a block you'll get.

## Most of the literature draws the transpose

Papers stack layers vertically — hence "deeper layers" — and run the sequence left to right: this picture, rotated. Neither is more correct, but mixing the two mid-explanation is where people lose the thread, so this subsection never rotates. Expect to when you read a paper.

## Check yourself

[Run](/wiki/ai/llm/running-the-checks) a 3-token prompt through [GPT-2 small](/wiki/ai/llm/gpt-2) with `output_hidden_states=True`. You get **13** tensors, not 12 — the embedding output, plus one per block — each shaped `[1, 3, 768]`: three rows, 768 wide, one snapshot per step rightward.

## Depends on / leads to

Depends on nothing. Leads to the [glossary](/wiki/ai/llm/glossary), then [GPT-2](/wiki/ai/llm/gpt-2) — the model every page here is measured against — and then [tokenization](/wiki/ai/llm/tokenization).
