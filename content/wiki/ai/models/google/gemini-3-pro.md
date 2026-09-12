---
title: "Gemini 3 Pro"
weight: 10
---

Gemini 3 Pro is the base model of [Google DeepMind](/wiki/ai/models/google)'s third Gemini generation, released November 2025. It earns a page not because it is the newest model Google offers — it is not — but because **every Gemini model Google shipped in 2026 descends from it**, and its model card is the only document in the family that describes the architecture at all.

Its own card states that it is not itself derived from anything: "Gemini 3 Pro is not a modification or a fine-tune of a prior model."

## The one architecture statement

Each later card in the family defers upward to its parent, and the chain terminates here. What it says:

> Gemini 3 Pro is a sparse mixture-of-experts (MoE) transformer-based model with native multimodal support for text, vision, and audio inputs. Sparse MoE models activate a subset of model parameters per input token by learning to dynamically route tokens to a subset of parameters (experts); this allows them to decouple total model capacity from computation and serving cost per token.

Two things follow from it. A third is conspicuous by its absence.

**It is a sparse [mixture of experts](/wiki/ai/llm/mixture-of-experts).** Not every parameter participates in every token; a router picks a subset. This is why a model can be very large in memory and still cheap per token.

**Its multimodality is native.** The model was trained on text, images and audio together, rather than having a vision encoder attached to a finished text model afterwards. The distinction shows up in what the model can do across modalities rather than within each one.

**No numbers are given.** No parameter count, no expert count, no routing width, no layer count, no training compute. It is a mechanism disclosure without measurements — more than [OpenAI](/wiki/ai/models/openai) or [Anthropic](/wiki/ai/models/anthropic) publish for their flagships, and far less than [DeepSeek](/wiki/ai/models/deepseek) or [Meta](/wiki/ai/models/meta) publish for theirs.

## The descendant chain

Google's model cards name their parents, which makes the family's dependency graph readable from primary documents — unusual enough to be worth stating:

```text
Gemini 3 Pro  (November 2025)
├── Gemini 3.1 Pro
└── Gemini 3 Flash
    └── each later Flash, in a chain
```

The consequence for a reader is that a point release in this family is a **descendant**, not a retrain. When Google ships a new Flash, it is building on the previous Flash, which builds ultimately on this model. Architectural claims made about Gemini 3 Pro therefore propagate forward unless a later card says otherwise — and none of them does.

## Training data, enumerated

The card lists sources explicitly, which few labs do:

> publicly available datasets that are readily downloadable; data obtained by crawlers; licensed data obtained via commercial licensing agreements; **user data** (i.e., data collected from users of Google products and services to train AI models, along with user interactions with the model) in accordance with Google's relevant terms of service, privacy policy, service-specific policies, and pursuant to user controls, where appropriate; other datasets that Google acquires or generates in the course of its business operations, or directly from its workforce; and **AI-generated synthetic data**.

Filtering covers deduplication, quality and safety filtering, and — stated outright — honouring `robots.txt`.

Post-training uses "different types of instruction tuning data, reinforcement learning data, and human-preference data," with reinforcement learning that "can leverage multi-step reasoning, problem-solving and theorem-proving data."

The card also says the disclosure was deliberately widened: it "includes more essential information about the Gemini 3 family of models than previous model cards did."

## What is not said: the hardware

The card's hardware section reads, in full, that the model "was trained using Google's Tensor Processing Units (TPUs)," with training done in JAX and ML Pathways. **It names no TPU generation.**

This is a break from the family's own history. Gemini 1.0 disclosed TPU v4 and v5e, Gemini 1.5 disclosed v4, Gemini 2.0 disclosed Trillium and Gemini 2.5 disclosed v5p. From Gemini 3 the generation stops being published, and claims that a particular recent Gemini trained on a particular recent TPU have no primary support.

## Status

Checked 11 September 2026. Google's [model documentation](https://ai.google.dev/gemini-api/docs/models) is the live source.

Gemini 3 Pro is **not the current model** — it is the base of the current generation. Gemini 3.8 Flash, from 2 September 2026, is the newest generally available model, and Gemini 3.1 Pro is in preview. The 3.x line shares one shape: 1,048,576 input tokens, 65,536 output tokens, text, image, video, audio and PDF in, text only out, with a `thinking` level set per request.

## Sources

- Google DeepMind, [Gemini 3 Pro model card](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf) (November 2025)
- Google, [Gemini API model documentation](https://ai.google.dev/gemini-api/docs/models)
- Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), arXiv:1706.03762 (2017)
- Shazeer et al., [Outrageously Large Neural Networks](https://arxiv.org/abs/1701.06538), arXiv:1701.06538 (2017)
