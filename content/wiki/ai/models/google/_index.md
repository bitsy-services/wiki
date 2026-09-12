---
title: "Google DeepMind"
weight: 30
bookCollapseSection: true
---

Google DeepMind trains two families of large language models: **Gemini**, the closed-weight frontier line served through Google's interfaces and Google Cloud, and **[Gemma](/wiki/ai/models/google/gemma)**, an open-weight line published as files anyone can run. This page covers the organisation and Gemini; Gemma has its own page because the licensing, the sizes and the reasons to reach for it are all different.

Google is the only builder in this section that trains on silicon it designed. Every Gemini model runs on **tensor processing units (TPUs)**, Google's own accelerator chips, rather than on the Nvidia parts the rest of the industry competes for. That vertical integration is the company's structural advantage and it is why TPU generations appear in the training disclosures below.

It is also the lab whose research the rest of this section is built on. The [transformer](/wiki/ai/llm) was published by Google researchers in 2017; so were the [mixture-of-experts](/wiki/ai/llm/mixture-of-experts) layer that makes today's frontier models affordable, the Chinchilla scaling work that reset how training budgets are allocated, and word2vec, seq2seq and BERT before them.

## The organisation

Google ran two AI labs for a decade. **Google Brain** sat inside Google and produced the transformer, TensorFlow and the TPU work. **DeepMind**, acquired in 2014 and run semi-independently from London, pursued reinforcement learning and game-playing: a deep Q-network (DQN) reaching human-level Atari play in 2015, AlphaGo beating Lee Sedol 4–1 in March 2016, then AlphaGo Zero, AlphaZero and MuZero. The two merged into **Google DeepMind** in 2023 under Demis Hassabis.

That pre-language-model history is not decoration. It is why the lab's output still splits between products and science: AlphaFold 2 predicted protein structure to near-experimental accuracy and seeded a database of over 200 million structures; AlphaProof and AlphaGeometry took a silver medal at the 2024 International Mathematical Olympiad. The 2025 result is the one that connects back to this section — a version of Gemini with an extended reasoning mode scored 35 of 42 for a gold medal **operating end-to-end in natural language**, with no formal-proof translation step of the kind the 2024 system needed.

## What Google discloses

More than OpenAI or Anthropic, and sharply less than it used to. The Gemini 1.0 and 1.5 releases came with real technical reports carrying architecture and infrastructure sections. The 3.x releases come with model cards that are safety documents with a short architecture paragraph attached.

That paragraph is still the most any closed frontier lab says about its flagship's shape:

> Gemini 3 Pro is a sparse mixture-of-experts (MoE) transformer-based model with native multimodal support for text, vision, and audio inputs. Sparse MoE models activate a subset of model parameters per input token by learning to dynamically route tokens to a subset of parameters (experts); this allows them to decouple total model capacity from computation and serving cost per token.

It is a **mechanism disclosure with no numbers** — no parameter count, no expert count, no routing width, no layer count. What it does establish is that Gemini is a sparse mixture of experts and that its multimodality is native, meaning the model was trained on text, images and audio together rather than having a vision encoder bolted to a text model afterwards.

### One base model, eight descendants

The more unusual disclosure is structural. Each Gemini model card names its parent, and the chain converges:

```text
Gemini 3 Pro  (November 2025)
├── Gemini 3.1 Pro
└── Gemini 3 Flash
    └── Gemini 3.5 Flash
        └── Gemini 3.6 Flash
            └── Gemini 3.7 Flash
                └── Gemini 3.8 Flash
```

Every 2026 Gemini model declares itself a descendant of one November 2025 base model, and the Gemini 3 Pro card states that it, in turn, "is not a modification or a fine-tune of a prior model." Being able to draw the dependency graph of a frontier lineup from the vendor's own documents is rare enough to be worth noting.

### Training data, enumerated

Google's model card lists its training sources explicitly, which few labs do:

> publicly available datasets that are readily downloadable; data obtained by crawlers; licensed data obtained via commercial licensing agreements; **user data** (i.e., data collected from users of Google products and services to train AI models, along with user interactions with the model) in accordance with Google's relevant terms of service, privacy policy, service-specific policies, and pursuant to user controls, where appropriate; other datasets that Google acquires or generates in the course of its business operations, or directly from its workforce; and **AI-generated synthetic data**.

Filtering includes deduplication, quality and safety filtering, and — stated outright — honouring `robots.txt`.

### The knowledge cutoff is ragged, and Google says so

Most vendors publish a single cutoff date. Google's recent Flash cards publish something more honest:

> The knowledge cutoff date for Gemini 3.8 Flash is March 2026 – users can expect updated information for some domains while in others they may experience the model's knowledge is limited to January 2025 (in line with the Gemini 3 Model Family).

A refreshed model does not refresh evenly. That is almost certainly true of every model in this section; Google is the one that writes it down.

## Long context: three different numbers

The 10-million-token figure attached to Gemini in popular accounts is real, and it is not a product limit. Separating the three numbers is the whole story:

- **10M is a research result.** The Gemini 1.5 report found "continued improvement in next-token prediction and near-perfect retrieval (>99%) up to at least 10M tokens." It was never a shipped limit.
- **1M is the shipped limit.** Every current Gemini 3.x model accepts 1,048,576 input tokens and emits at most 65,536. Gemini 1.5 Pro did once ship a 2M window; 1.5 is retired and the current documentation mentions neither 2M nor 10M.
- **The recall claim has quietly weakened.** Google's current wording is that the models "achieve high performance across various needle-in-a-haystack retrieval evals… up to 99% accuracy in many cases," but that performance "can vary to a wide degree" when searching for *multiple* pieces of information at once.

The gap between finding one planted fact in a long document and finding several is the honest version of the long-context story, and it is a better guide to what a million-token window buys than the headline number. [Context length](/wiki/ai/llm/context-length) covers what that window costs to use.

## Which chips trained which model

Google published the TPU generation behind each Gemini family until it stopped:

| Model | Trained on |
| --- | --- |
| Gemini 1.0 | TPU v4 and v5e; Ultra on v4 across multiple datacentres |
| Gemini 1.5 | TPU v4, multiple 4096-chip pods |
| Gemini 2.0 | Trillium (TPU v6e) |
| Gemini 2.5 | TPU v5p, multiple 8960-chip pods |
| Gemini 3 Pro | **Not disclosed** — the card says only "Google's Tensor Processing Units" |

Note that the ordering is not monotonic: Gemini 2.5 trained on v5p *after* Gemini 2.0 trained on Trillium. Nothing about a model's quality follows from the generation number of the chips underneath it, and claims that a particular recent Gemini trained on a particular recent TPU are not supported by anything Google has published.

## Status

Checked 11 September 2026. Google's [model documentation](https://ai.google.dev/gemini-api/docs/models) and [pricing page](https://ai.google.dev/pricing) are the live sources.

**Gemini 3.8 Flash**, released 2 September 2026, is the most recent generally available model. **Gemini 3.1 Pro** remains in preview. The whole 3.x line shares one shape: 1,048,576 input tokens, 65,536 output tokens, **text, image, video, audio and PDF in, text only out**, and a `thinking` level set per request from `minimal` or `low` up to `high`.

Google also ships non-language models under the same brand — Imagen for images, Veo for video, Lyria for music, and a separate weather line — which are outside this section's scope.

## Sources

- Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), arXiv:1706.03762 (2017)
- Shazeer et al., [Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](https://arxiv.org/abs/1701.06538), arXiv:1701.06538 (2017)
- Hoffmann et al., [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556), arXiv:2203.15556 (2022) — Chinchilla
- Google DeepMind, [Gemini 1.5 technical report](https://storage.googleapis.com/deepmind-media/gemini/gemini_v1_5_report.pdf) — the 10M retrieval result
- Google DeepMind, [Gemini 3 Pro model card](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf) (November 2025) — architecture and training data
- Jouppi et al., [In-Datacenter Performance Analysis of a Tensor Processing Unit](https://arxiv.org/abs/1704.04760), arXiv:1704.04760 (2017)
- Jouppi et al., [TPU v4: An Optically Reconfigurable Supercomputer for Machine Learning](https://arxiv.org/abs/2304.01433), arXiv:2304.01433 (2023)
- Jumper et al., [Highly accurate protein structure prediction with AlphaFold](https://doi.org/10.1038/s41586-021-03819-2), Nature 596 (2021)
- Google DeepMind, [Gemini Deep Think achieves gold-medal standard at the IMO](https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/) (21 July 2025)
