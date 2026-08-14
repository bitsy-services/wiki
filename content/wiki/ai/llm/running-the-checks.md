---
title: "Running the Checks"
weight: 40
---

Every page in this section ends with a *Check yourself* — a short experiment that either confirms the page's claim or breaks it. They are all the same kind of thing: a few lines of Python, run against a real but small model that fits on a laptop. What none of them spell out, because it would mean saying it thirty times, is the part that comes *before* the experiment — which language, what to install, how the model gets loaded, and what the handful of objects the checks keep naming actually are. This page is that missing preamble. Read it once and keep it open; after that, every *Check yourself* is copy-and-run.

## The three kinds of check

The experiments differ in what they need in front of you, and it's worth knowing which kind you're looking at before you start:

- **Load and look.** Most of them. Download [GPT-2 small](/wiki/ai/llm/gpt-2), run one forward pass, and read the numbers that come back — no training, a second or two on a plain CPU. [Perplexity](/wiki/ai/llm/perplexity), [the residual stream](/wiki/ai/llm/residual-stream), [attention](/wiki/ai/llm/attention), and [the unembedding](/wiki/ai/llm/unembedding-and-logits) all live here.
- **Train a tiny model.** A handful — [skip connections](/wiki/ai/llm/skip-connections), [backprop through one weight](/wiki/ai/llm/backprop-one-weight), [mixture of experts](/wiki/ai/llm/mixture-of-experts), [grouped-query attention](/wiki/ai/llm/grouped-query-attention), [fine-tuning](/wiki/ai/llm/fine-tuning) — change the architecture and watch the loss move. Those use nanoGPT and take minutes, not seconds.
- **No model at all.** A few — [GELU and SwiGLU](/wiki/ai/llm/activations), [RoPE](/wiki/ai/llm/rope), [superposition](/wiki/ai/llm/superposition), [context length](/wiki/ai/llm/context-length), [tokenization](/wiki/ai/llm/tokenization) — are pure arithmetic on random tensors, or a tokenizer with no weights behind it. They download nothing.

Everything below is Python 3. The rest of this page sets up each of the three in turn.

## Load and look: GPT-2 small in HuggingFace

Two packages cover every load-and-look check:

```bash
pip install torch transformers
```

`torch` is PyTorch, the array-and-autograd library the model's arithmetic runs on; `transformers` is HuggingFace's library of pretrained models, which is where GPT-2 comes from. With those installed, the following is the setup that every load-and-look *Check yourself* silently assumes:

```python
import torch
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

# "gpt2" is the 124M-parameter small model — downloaded once, then cached on disk.
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()   # turn off dropout, so two runs of the same input give the same answer
tok = GPT2TokenizerFast.from_pretrained("gpt2")

# Tokenize a prompt. input_ids is a tensor of shape [1, n]: one sequence, n token ids.
ids = tok("The cat sat on the", return_tensors="pt").input_ids

with torch.no_grad():                     # we aren't training, so skip gradient bookkeeping
    outputs = model(ids, labels=ids, output_hidden_states=True)
```

That one forward pass produces everything the load-and-look checks read. The three keyword arguments and the objects they fill are the vocabulary those checks are written in:

- **`labels=ids`** makes the model score itself. It returns `outputs.loss`, the average [cross-entropy](/wiki/ai/llm/the-loss-function) over the sequence. You pass the *same* tensor as both input and labels because there is no separate label — the model shifts the text by one internally and predicts each token from the ones before it. Exponentiate the loss and you have [perplexity](/wiki/ai/llm/perplexity): `torch.exp(outputs.loss)`.
- **`output_hidden_states=True`** fills `outputs.hidden_states`, a tuple of **13** tensors each shaped `[1, n, 768]` — the [embedding](/wiki/ai/llm/embeddings) output, then one snapshot after each of the 12 blocks. `hidden_states[0]` is the input before any block has run; `hidden_states[-1]` is already past the final [normalization](/wiki/ai/llm/normalization), which HuggingFace applies before handing back that last entry. (Left off, `outputs.hidden_states` is `None`.)
- **`outputs.logits`**, always present, is shaped `[1, n, 50257]`: one [score for every token in the vocabulary](/wiki/ai/llm/unembedding-and-logits), at every position.

The named pieces of the model that the checks reach into all hang off `model`:

```text
model.transformer.wte.weight     token embedding table, 50257 × 768 — also the unembedding (tied)
model.transformer.wpe.weight     position embedding table, 1024 × 768
model.transformer.h[i]           block i (i = 0…11)
model.transformer.h[i].attn.c_attn   fused Q/K/V projection, 768 × 2304
model.transformer.h[i].attn.c_proj   attention's output projection — the hook point below
model.transformer.h[i].mlp           the block's MLP
model.lm_head.weight             the unembedding — the same storage as wte.weight
```

That `wte`/`lm_head` sharing is [weight tying](/wiki/ai/llm/weight-sharing), and `c_attn` being one matrix rather than three is covered under [Q/K/V projections](/wiki/ai/llm/qkv-projections).

### Two more switches some checks flip

- **Attention weights.** To read the attention pattern itself, load with `attn_implementation="eager"` and pass `output_attentions=True`; then `outputs.attentions` is a tuple of `[1, 12, n, n]` matrices. The faster default (SDPA) path doesn't reliably hand those back, so the checks in [one attention head](/wiki/ai/llm/one-attention-head) and [attention](/wiki/ai/llm/attention) pin `eager` on purpose.
- **The KV cache.** `model.generate(...)` and a plain forward pass both take `use_cache=True` (the default) or `False`. The tokens are identical either way — [the cache](/wiki/ai/llm/kv-cache) is an optimization, not an approximation — which is exactly the check on that page.

### Replacing a module's output mid-pass

The [attention](/wiki/ai/llm/attention) and [residual stream](/wiki/ai/llm/residual-stream) checks delete part of the model while it runs, using a **forward hook** — PyTorch's callback that fires when a module produces its output and can return a replacement:

```python
def zero_out(module, inputs, output):
    return torch.zeros_like(output)

handle = model.transformer.h[6].attn.c_proj.register_forward_hook(zero_out)
# ... run the model; block 6's attention now contributes nothing ...
handle.remove()   # undo it
```

Hook `c_proj` rather than `.attn` itself: `.attn` returns a tuple, not a plain tensor, and the block would index into your replacement instead of using it.

### Generating text

The sampling and decoding checks call `model.generate(...)`. Greedy decoding is `do_sample=False`; nucleus sampling is `do_sample=True, top_p=0.9`; [speculative decoding](/wiki/ai/llm/speculative-decoding) passes a small `assistant_model=`. See [sampling strategies](/wiki/ai/llm/sampling-strategies) for what the arguments do.

A few checks ([RLHF](/wiki/ai/llm/rlhf), [multi-head attention](/wiki/ai/llm/multi-head-attention)) swap `"gpt2"` for another HuggingFace model id — `"gpt2-xl"`, `"Qwen/Qwen2.5-0.5B"` — but change nothing else about the setup above.

## Train a tiny model: nanoGPT

The architecture checks need to *modify* the model and retrain, which the HuggingFace weights don't let you do cleanly. They use nanoGPT — Andrej Karpathy's roughly 300-line implementation of this exact model, small enough to read end to end. Clone it and install its dependencies:

```bash
git clone https://github.com/karpathy/nanoGPT
cd nanoGPT
pip install torch numpy transformers datasets tiktoken wandb tqdm
```

The quickstart trains a character-level model on a 1 MB Shakespeare corpus in minutes on a CPU:

```bash
python data/shakespeare_char/prepare.py                    # build the dataset
python train.py config/train_shakespeare_char.py --device=cpu --compile=False
```

Two files matter for the checks. `model.py` holds the architecture — this is where "in nanoGPT, delete both skips" or "swap one block's MLP for eight copies plus a router" happen, as edits to those ~300 lines. `train.py` runs the training loop and prints the loss you're asked to watch. nanoGPT can also load GPT-2's pretrained weights, with `GPT.from_pretrained('gpt2')`, which is how the [grouped-query attention](/wiki/ai/llm/grouped-query-attention) check starts from the real model before changing it.

## No model: just torch (or tiktoken)

Some checks download nothing at all. The ones on [GELU](/wiki/ai/llm/activations), [RoPE](/wiki/ai/llm/rope), [superposition](/wiki/ai/llm/superposition), and [context length](/wiki/ai/llm/context-length) are arithmetic on random tensors — `pip install torch` and you have everything, no weights involved. Build a random matrix with `torch.randn(768, 3072)`, call `torch.nn.functional.gelu`, and you're running the experiment.

The [tokenization](/wiki/ai/llm/tokenization) check needs only the GPT-2 tokenizer, which ships without the model in a separate small package:

```bash
pip install tiktoken
```

```python
import tiktoken
enc = tiktoken.get_encoding("gpt2")
enc.encode(" cat")   # -> [3797]
```

## Check yourself

The harness has its own falsifiable check: run the load-and-look setup at the top of this page verbatim, then confirm it's wired up before you trust any experiment built on it.

```python
len(outputs.hidden_states)          # 13 — embedding plus one per block
outputs.logits.shape                # torch.Size([1, 5, 50257])
torch.exp(outputs.loss)             # GPT-2's perplexity on the sentence
```

`hidden_states` should have 13 entries; if it has none, you dropped `output_hidden_states=True`. The logits' last axis is the 50,257-token vocabulary. And `torch.exp(outputs.loss)` comes back a two-digit number for ordinary English — the same quantity the [perplexity](/wiki/ai/llm/perplexity) page opens on. If `outputs.loss` is missing entirely, you dropped `labels=ids`.

## Depends on / leads to

Depends on [GPT-2](/wiki/ai/llm/gpt-2), the model these checks all run against. Leads to every page's *Check yourself*; the reading order proper resumes at [tokenization](/wiki/ai/llm/tokenization).
