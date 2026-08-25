---
title: "GPT-2"
weight: 30
---

GPT-2 — Generative Pre-trained Transformer 2 — is the language model this section takes apart. OpenAI built it to test one idea — that a program trained only to guess the next piece of text, given enough ordinary writing to practise on, would pick up skills nobody set out to teach it — and it worked well enough to point the whole field in the direction it has been going ever since. It is also, by current standards, small and completely open: the weights are published, it runs on a laptop, and it is built the same way as the models people pay for today. That openness is why every page here uses it as the worked example.

## Why the worked example is a model from 2019

Every page in this section ends with a claim you can check. That is only possible with a model you can open.

A frontier model is a URL. You send text, you get text, and the interesting parts — the [rows](/wiki/ai/llm/glossary) moving rightward through the blocks, the [attention patterns](/wiki/ai/llm/glossary), the tables of weights — are on the far side of an API you don't control. You cannot pull out the row before block 0 and confirm it's bit-identical for two different sentences. You cannot zero the position table and watch [perplexity](/wiki/ai/llm/perplexity) explode. Those experiments are the point, and against a closed model none of them can be run; you'd be taking every claim on faith, which is the habit this section exists to break.

GPT-2 can be opened all the way. The weights are a free download, a forward pass on a laptop CPU takes a fraction of a second, and every intermediate the pages talk about is a tensor you can print. nanoGPT — the minimal implementation the checks keep reaching for — is roughly 300 readable lines and reproduces this exact model.

The obvious objection is that 2019 is a long time ago. But the spine hasn't changed. [Tokenize](/wiki/ai/llm/tokenization) the text, look each token up in a table, add in position, push it through a stack of blocks that alternate [attention](/wiki/ai/llm/attention) and [an MLP](/wiki/ai/llm/the-mlp), score the last row against the vocabulary, [sample](/wiki/ai/llm/sampling-strategies). That is GPT-2, and it is also every model in production right now. GPT-3 arrived a year later as essentially this architecture with more than a hundred times the parameters. What separates a modern model from GPT-2 is [scale](/wiki/ai/llm/why-scale-worked), training data, and a list of component substitutions — the substitutions are real, and the [last section here](#where-gpt-2-misleads) is that list — but the frame they slot into is the one GPT-2 laid down.

## What GPT-2 showed

Its predecessor established a two-step recipe: train on a pile of text, then [fine-tune](/wiki/ai/llm/fine-tuning) the result on the actual task you cared about. GPT-2's claim was the sharper one — that the second step was optional.

The paper is called *Language Models are Unsupervised Multitask Learners*, and the title states the claim. Text scraped from the open web already contains translations, questions with answers, articles with summaries. A model getting genuinely good at predicting that text has no way to avoid learning to translate, answer, and summarize along the way, because those skills are what the next token depends on. The tasks don't need teaching separately. They're already in the data, and prediction drags them out.

The evidence was **zero-shot** performance — the model doing a task with no training examples for it whatsoever, prompted and nothing more. GPT-2 XL, the largest of the four sizes below, zero-shot beat the state of the art on seven of the eight language-modelling benchmarks it was measured on, against models trained on those datasets specifically. (The eighth, which it lost badly, was the One Billion Word Benchmark.) It was worse than a specialist at things like summarization, but the point was that it could do them at all, having been shown no examples.

The other half of the result was the shape of the curve. The four sizes below share a training set and a recipe and differ only in how big they are, and quality climbed steadily with size with no sign of flattening. That line is what GPT-3 was a bet on, and every frontier model since has been a bet on the same line.

## The model that was too dangerous to release

OpenAI did not release GPT-2 when it announced it. In February 2019 it published the smallest of the four and held the rest back, citing the risk of automated disinformation, spam, and impersonation at scale. The remaining sizes trickled out over the following nine months, with the full model arriving that November.

It reads oddly now. GPT-2 XL writes fluent, confidently drifting nonsense; it is nowhere near the propaganda engine the announcement worried about, and anyone wanting one today has far better options for free. The withheld capability was not the dangerous part, and the staged release did not hold anything back for long.

What it did do was set a template. Deciding what to publish and when, on capability grounds, is now routine practice across every major lab, and "we are not releasing the weights" is a sentence whose history starts here. Whether that was farsighted or an early exercise in the same instinct that now keeps frontier weights closed for commercial reasons is genuinely arguable — but it is the reason a section about how these models work has to be taught on one from 2019.

## The four sizes

| Name | Identifier | Parameters | Blocks | `d_model` | Heads |
|---|---|---|---|---|---|
| small | `gpt2` | 124M | 12 | 768 | 12 |
| medium | `gpt2-medium` | 355M | 24 | 1024 | 16 |
| large | `gpt2-large` | 774M | 36 | 1280 | 20 |
| XL | `gpt2-xl` | 1.5B | 48 | 1600 | 25 |

All four share a tokenizer, a 50,257-entry vocabulary, a 1024-token context, a training set, and a recipe. Only [depth and width](/wiki/ai/neural-network/depth-and-width) move, which is what makes them a scaling experiment rather than four unrelated models.

Divide `d_model` by the head count and every row of that table gives 64. A [head](/wiki/ai/llm/glossary) is 64 numbers wide in the smallest model and 64 in the largest. Extra width was spent on *more* heads, never wider ones — the head is treated as a fixed unit and the model buys more of them, which is the premise [multi-head attention](/wiki/ai/llm/multi-head-attention) builds on.

Unqualified "GPT-2" on these pages means **GPT-2 small**, the 124M model.

Every figure in that Parameters column comes with a footnote, because the paper disagrees with all four: its table reports 117M, 345M, 762M, and 1542M. The counts above are the released checkpoints — what you get if you download the weights and add up the tensors, which the [check below](#check-yourself) does — and they're the ones to trust. The paper's numbers have never matched the published models, no correction was ever issued, and nothing interesting is hiding in the gap. Expect to meet both sets of figures in the wild.

## GPT-2 small, assembled

Every page in this section teaches one piece of this model. Here they are in one picture, laid out by [the section's convention](/wiki/ai/llm/conventions) — depth left to right, sequence top to bottom:

```text
                          depth  →

  pos 0    "The"   [── 768 ──]──[── 768 ──]── ⋯ ──[── 768 ──]──▶ 50,257 logits
  pos 1   " cat"   [── 768 ──]──[── 768 ──]── ⋯ ──[── 768 ──]──▶ 50,257 logits
  pos 2   " sat"   [── 768 ──]──[── 768 ──]── ⋯ ──[── 768 ──]──▶ 50,257 logits
    │                   │            │                  │
    ▼                 embed       block 0           block 11
 sequence           + position                      + final norm
 (≤ 1024)                        └── 12 heads × 64 wide ──┘
                                 └── MLP 768 → 3072 → 768 ─┘
```

And here is the same model as a parts list, each part linked to the page that teaches it:

| Part | GPT-2 small |
|---|---|
| [Vocabulary](/wiki/ai/llm/tokenization) | 50,257 entries — byte-pair encoding over raw bytes |
| [Row width](/wiki/ai/llm/residual-stream) (`d_model`) | 768, fixed from the embedding to the unembedding |
| [Embedding table](/wiki/ai/llm/embeddings) (`wte`) | 50,257 × 768 — one learned row per vocabulary entry |
| [Position table](/wiki/ai/llm/positional-encoding) (`wpe`) | 1024 × 768 — learned, absolute, added before block 0 |
| [Blocks](/wiki/ai/llm/glossary) | 12, identical in structure, ~7.1M parameters each |
| [Attention](/wiki/ai/llm/multi-head-attention) | 12 heads per block, 64 wide each, [causally masked](/wiki/ai/llm/causal-mask) |
| [MLP](/wiki/ai/llm/the-mlp) | 768 → 3072 → 768 with a [GELU](/wiki/ai/neural-network/activations) between — two-thirds of each block |
| [Normalization](/wiki/ai/neural-network/normalization) | [LayerNorm](/wiki/ai/neural-network/normalization), pre-norm placement, plus one final norm at the right edge |
| [Unembedding](/wiki/ai/llm/unembedding-and-logits) | tied to the embedding — the same table, transposed |
| Context | 1024 tokens, a limit set entirely by `wpe`'s height |

It was trained on **WebText**: about 40 GB of text from 8 million documents, gathered by following every outbound link from Reddit that had at least three karma — a cheap proxy for "a human thought this was worth sharing" — with Wikipedia deliberately excluded so it couldn't contaminate the benchmarks.

For the finished small model the paper reports a WikiText-2 perplexity of 29.41. Measure it yourself on a few hundred tokens of WikiText and you'll get a [loss](/wiki/ai/neural-network/the-loss-function) near 3.28 — a perplexity of about 26 — which is the figure the rest of these pages quote. The two aren't in conflict: the paper evaluates the full test set through its own detokenizers, and a short sample is an easier run. Same model, two measurements.

## Where GPT-2 misleads

A reference model quietly teaches its own quirks as though they were laws. Several things GPT-2 does are GPT-2's choices, not the transformer's, and every one of them has since been replaced nearly everywhere. This is the translation table:

| GPT-2 does | Nearly everything since |
|---|---|
| Learned absolute position table, hard-capped at 1024 | [RoPE](/wiki/ai/llm/rope) — position as rotation, no table, stretches past the trained length |
| LayerNorm | [RMSNorm](/wiki/ai/neural-network/normalization) — drop the centering and the bias, no measurable cost |
| GELU in a two-matrix MLP | [SwiGLU](/wiki/ai/neural-network/activations) — a three-matrix gated variant, better per parameter |
| Every head owns its keys and values | [Grouped-query attention](/wiki/ai/llm/grouped-query-attention) — heads share them, shrinking [the KV cache](/wiki/ai/llm/kv-cache) |
| A bias vector on every linear map | Dropped entirely — they weren't earning their place |
| 50,257-entry vocabulary | 128k and up — better coverage of code and languages other than English |
| Dense: every parameter runs for every token | Often [mixture of experts](/wiki/ai/llm/mixture-of-experts) — each token routed through a fraction |
| Tied embedding and unembedding | Often untied at scale, though small models still tie |

Not one of those substitutions changes the shape of the thing: rows still run rightward through a stack of blocks, attention is still the only place rows see each other, the MLP still works one row at a time, everything still adds into [the residual stream](/wiki/ai/llm/residual-stream) rather than overwriting it. They are swaps within a fixed frame. The pages here name GPT-2 explicitly whenever a claim is one of these swappable choices, rather than letting it pass as the way things are done.

## Check yourself

Add up GPT-2 small by hand. One block is two norms (768 × 2 each), attention's four 768 × 768 matrices, and the MLP's 768 × 3072 pair — with bias vectors on each map, since GPT-2 still has those — which comes to 7,087,872. Then the whole model:

```text
wte     50,257 × 768                    =   38,597,376
wpe      1,024 × 768                    =      786,432
blocks   7,087,872 × 12                 =   85,054,464
ln_f       768 × 2                      =        1,536
                                            -----------
                                            124,439,808
```

[Load](/wiki/ai/llm/running-the-checks) `gpt2` and run `sum(p.numel() for p in model.parameters())`. It returns 124,439,808 — the same number, to the digit.

Now find the missing 38.6M. There is no separate unembedding in that sum, because there is no separate unembedding: check `model.transformer.wte.weight.data_ptr() == model.lm_head.weight.data_ptr()` and it's **True**, the same storage read from both edges of the model. Untie them and the total goes to 163M. The model is 124M because that table is counted once, and the check is that `data_ptr` comparison — pointer equality, not `torch.equal`, which would only tell you the numbers currently match.

## Depends on / leads to

Depends on the [glossary](/wiki/ai/llm/glossary), and — if you have never met a fitted model before — on [the neural network section](/wiki/ai/neural-network), which says what kind of object GPT-2 is before any of the specifics. Leads to [tokenization](/wiki/ai/llm/tokenization), where the text becomes integers.
