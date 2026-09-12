---
title: "Gemma"
weight: 10
---

Gemma is [Google DeepMind](/wiki/ai/models/google)'s open-weight model line: the weights are published as files, and anyone can download them and run them on their own machines. It exists alongside Gemini, which is closed-weight and reachable only through Google's interfaces. The two share research but not checkpoints — Google describes Gemma as "built from the same technology that powers our Gemini models," not as a smaller Gemini.

The line matters for a reason that has nothing to do with capability rankings. An open-weight model can process data that must not leave a building, can be fine-tuned by a third party, cannot be withdrawn by its publisher, and can be inspected by anyone. Gemma is Google's answer to all four, and since April 2026 its licence stops qualifying any of them.

## The licence changed, and that is the news

**Gemma 4, released 2 April 2026, is under Apache 2.0** — and it is the first Gemma release that is. Google's own framing: Gemma 4 models are "the first in the Gemmaverse to be released under the OSI-approved Apache 2.0 license" — approved, that is, by the Open Source Initiative (OSI), which maintains the definition of what counts as open source.

Everything before it — Gemma 1, 2, 3, 3n, and most specialised variants through TranslateGemma in January 2026 — sits under the custom **Gemma Terms of Use**, which is not an approved open-source licence and carries a separate prohibited-use policy. Three variants sit outside even that, under a third set of terms each; see [Specialised variants](#specialised-variants). **Nothing was relicensed retroactively.** The Gemma Terms appendix, last modified the day before the Gemma 4 announcement, still lists every earlier model by name.

The practical consequences of the switch are visible in the distribution:

- **Gemma 4 is not gated on Hugging Face; earlier Gemma was.** Gemma 3 required a logged-in account and an explicit agreement to Google's terms before the files would download. Google's own setup documentation now prefixes the old consent flow with "Note: This is only relevant for Gemma 3 and prior versions."
- The prohibited-use policy still linked from the Gemma 4 model card was last modified in February 2024 — before Gemma 2 existed — and says nothing about whether it binds an Apache 2.0 licensee.

What is known about the result: the Apache 2.0 grant itself imposes no restriction on what the model may be used for, and Google has not said whether the still-linked prohibited-use policy is incorporated by reference. The licence text is unambiguous; its relationship to that policy is not.

## The lineup and the architecture

Gemma 4 ships as a size ladder rather than a single model, and the sizes are chosen for where the model will run rather than for a capability tier. Three conventions in the names: **`E`** marks an *effective* parameter count, meaning what has to be resident at inference rather than what the checkpoint contains; **`A`** marks the *active* count of a [mixture-of-experts](/wiki/ai/llm/mixture-of-experts) model, the share each token is actually multiplied by; and *Unified* marks the model that takes images and audio through one pathway rather than a separate encoder.

| Model | Parameters | Context | Runs on |
| --- | --- | --- | --- |
| `E2B` | 2.3B effective (5.1B with embeddings) | 128K | phones, Raspberry Pi, single-board computers |
| `E4B` | 4.5B effective (8B with embeddings) | 128K | phones and laptops |
| 12B Unified | 11.95B | 256K | a workstation accelerator |
| 26B `A4B` | 25.2B total, **3.8B active** | 256K | a datacentre accelerator, or quantised on consumer hardware |
| 31B | 30.7B | 256K | a single 80 GB accelerator at full precision |

A caution if you are counting models: `blog.google` enumerates four sizes and omits 12B Unified, while the model card, the documentation and the Hugging Face announcement all enumerate five. Google has not reconciled the two.

Architecturally, three things distinguish the line:

- **Hybrid attention.** The model "interleaves local sliding window attention with full global attention," with the final layers always global. Sliding-window [attention](/wiki/ai/llm/attention) lets most layers score each token against only a nearby span rather than the whole sequence, which is what keeps a 256K context affordable.
- **Per-layer embeddings** on the two smallest models, which let embedding data be computed outside the accelerator's memory and streamed in as each layer runs. This is why `E2B` occupies roughly 2 GB at inference despite holding over 5 billion parameters.
- **A [mixture of experts](/wiki/ai/llm/mixture-of-experts)** at 26B: 8 active experts out of 128, plus one shared expert.

### The active-parameter trap

The 26B model advertises 3.8 billion active parameters, and it is easy to read that as a memory figure. It is not. Google's documentation is unusually direct about it: "all 26 billion parameters must be loaded into memory to maintain fast routing and inference speeds."

**Active parameters buy arithmetic, not memory.** A mixture-of-experts model is cheaper per token than a dense model of the same total size because each token is multiplied by only a fraction of the weights — but every expert still has to be resident, because the next token may route to any of them. Google's own memory table bears this out: the 26B model needs about 57.7 GB at 16-bit precision and 14.4 GB quantised to 4-bit, against 26.7 GB and 6.7 GB for the dense 12B. This is the single most common misreading of a mixture-of-experts spec sheet.

## Where it runs

Google publishes quantisation-aware 4-bit checkpoints itself, and the day-one support list covers the usual local runtimes — `llama.cpp`, Ollama, LM Studio, MLX, vLLM and others.

Two details are worth knowing before committing to a small Gemma on local hardware:

- **`llama.cpp` does not implement per-layer embeddings.** Its loader reads the metadata but the forward pass never injects the per-layer signal, so `E2B` and `E4B` run without crashing and with quietly degraded output. The [issue](https://github.com/ggml-org/llama.cpp/issues/22243) is open.
- **Google's own integration pages point at community checkpoint repositories**, not at Google's, for both `llama.cpp` and MLX — probably because those pages predate Google's own quantised release, but Google does not say so.

Google serves Gemma through its own API **free of charge only** — as of September 2026 the pricing page lists a free tier and marks the paid tier "Not available." Paid hosting exists from Cloudflare, Vertex AI and others. Google positions the line for sovereign and air-gapped deployment, promising availability "across all our Sovereign Cloud offerings… including Google Distributed Cloud for air-gapped and on-premises deployments."

## Specialised variants

Gemma is also a base for narrow models, and the pattern is consistent enough to be worth naming: Google takes a Gemma generation, post-trains it for one job, and publishes the result under the Gemma family name. CodeGemma for code, PaliGemma for vision-language, ShieldGemma for content moderation, EmbeddingGemma for [embeddings](/wiki/ai/llm/embeddings), TranslateGemma for translation, VaultGemma trained under a differential-privacy guarantee, and RecurrentGemma, which replaces attention with gated linear recurrences and so has a fixed-size state rather than a growing [KV cache](/wiki/ai/llm/kv-cache).

Two carry different licences and are easy to trip over: the medical models (MedGemma, TxGemma) are under Health AI Developer Foundations terms rather than the Gemma Terms, and Gemma Scope 2 — a large release of interpretability tools for probing what Gemma's internals represent — is under Creative Commons. One announced variant, DolphinGemma, was promised as an open model in April 2025 and had still not been released seventeen months later.

## Status

Checked 11 September 2026. The [Gemma documentation](https://ai.google.dev/gemma/docs) and [model card](https://ai.google.dev/gemma/docs/core/model_card_4) are the live sources for sizes, memory requirements and licence terms.

**Gemma 4** is the current generation, released 2 April 2026 under Apache 2.0, in the five sizes above. Later additions to the same generation include multi-token prediction variants and DiffusionGemma, an experimental model that generates text by iteratively denoising blocks of tokens in parallel rather than one token at a time — also Apache 2.0, and the only specialised variant so far released under it.

## Sources

- Google, [Gemma 4](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/) (2 April 2026)
- Google Open Source, [Gemma 4: expanding the Gemmaverse with Apache 2.0](https://opensource.googleblog.com/2026/03/gemma-4-expanding-the-gemmaverse-with-apache-20.html)
- Google, [Gemma 4 model card](https://ai.google.dev/gemma/docs/core/model_card_4) — architecture and sizes
- Google, [Gemma documentation overview](https://ai.google.dev/gemma/docs/core) — the memory table and the routing note
- Google, [Gemma Terms of Use](https://ai.google.dev/gemma/terms) — the appendix listing which models it still governs
- Google, [Quantization-aware training for Gemma 4](https://blog.google/innovation-and-ai/technology/developers-tools/quantization-aware-training-gemma-4/) (5 June 2026)
