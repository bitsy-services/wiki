---
title: "Alibaba (Qwen)"
weight: 60
bookCollapseSection: true
---

Qwen is the model family built by Alibaba Cloud's Tongyi lab, and it is the most widely built-upon open-weight family in existence. When another lab needs a capable base model to fine-tune or distil onto, it usually reaches for a Qwen: four of the six models [DeepSeek](/wiki/ai/models/deepseek) distilled from [R1](/wiki/ai/models/deepseek/r1)'s reasoning traces are Qwen-based, against two on [Llama](/wiki/ai/models/meta).

What distinguishes Qwen from the other open-weight families is the **ladder**. Rather than shipping two or three sizes, Alibaba releases a generation across a wide span — from models small enough for a phone to a flagship in the trillions of parameters — trained together and released together. That breadth is the strategy: whatever hardware someone has, there is a Qwen sized for it, and they all behave similarly enough that moving between them is cheap.

## The company

Qwen is built by the Tongyi lab inside **Alibaba Cloud**, the cloud division of the Chinese e-commerce group Alibaba. That parentage explains the strategy better than anything the lab has said about it.

Alibaba announced 380 billion renminbi (RMB) — roughly US$53 billion — of AI and cloud infrastructure spending over three years in February 2025, which it said exceeded its total spending on both in the preceding decade, and raised a further US$10 billion in new shares in August 2026. Its chief executive has named artificial general intelligence (AGI) as the company's primary long-term objective and cloud computing as its clearest revenue driver in AI.

The second half of that sentence is the one that matters here. **Alibaba does not sell models; it rents computers.** Open weights seed an ecosystem that eventually rents accelerators, and they make Qwen the default thing to fine-tune — which is worth more to a cloud business than per-token revenue at the small end. The structure shows the strategy: the wide ladder is open, the flagship's weights are open but revenue-gated, and the strongest models of all stay hosted-only.

Like [DeepSeek](/wiki/ai/models/deepseek), Alibaba trains under United States export controls on accelerators sold into China, which shapes what it can build with.

## "Qwen is Apache 2.0" is no longer true of the flagship

This is the most important correction for anyone working from a 2025 understanding.

The **Qwen3.8-27B** model is genuinely Apache 2.0. The **Qwen3.8 flagship is not.** It ships under a bespoke Qwen3.8-Max Licence that requires a separate commercial agreement from any organisation above **US$50 million in aggregate revenue over any twelve months**, and imposes a prominent-attribution requirement above 100 million monthly active users (MAU) or $20 million in monthly revenue.

That is a different shape of restriction from [Meta's](/wiki/ai/models/meta), which triggers on user count frozen at a release date, and from [Mistral's](/wiki/ai/models/mistral) Modified MIT, which triggers on monthly revenue. All three are worth checking individually rather than assuming, because the family's reputation for permissive licensing was earned by earlier generations and no longer describes the top of the current one.

## The architecture changed at Qwen3.5

Through Qwen3, the models were conventional transformers: [attention](/wiki/ai/llm/attention) block, [MLP](/wiki/ai/llm/the-mlp) block, repeat. From Qwen3.5 that stopped being true.

`Qwen3.8-2.4T-A95B` interleaves two different sequence-mixing mechanisms. Its 92 layers repeat a four-block pattern — three blocks pairing **Gated DeltaNet**, a linear-attention variant whose cost grows with sequence length rather than with its square, with a [mixture-of-experts](/wiki/ai/llm/mixture-of-experts) layer, then one block pairing ordinary gated attention with a mixture-of-experts layer:

```text
3 × (Gated DeltaNet → MoE)
1 × (Gated Attention → MoE)
```

Only one layer in four pays full attention's quadratic cost. This is the same structural bet [Google's Gemma](/wiki/ai/models/google/gemma) makes with its local/global interleave and [Meta's](/wiki/ai/models/meta) Llama 4 makes with `iRoPE`: most layers get a cheap approximation of attention, a minority get the real thing, and the model recovers the difference. [Context length](/wiki/ai/llm/context-length) explains why that trade is worth making.

A [mixture-of-experts](/wiki/ai/llm/mixture-of-experts) layer replaces one feed-forward block with many, called experts, and a router sends each token through only a few of them. Qwen's is unusually fine-grained even by current standards: **512 experts with 11 active per token** — 10 chosen by the router, plus 1 *shared* expert that every token passes through regardless. The native context is 262,144 tokens, extended toward a million by YaRN, a technique for stretching [rotary position embeddings](/wiki/ai/llm/rope) beyond the length the model trained on.

Two numbers show what the generations have been spending on: the vocabulary grew from about 152,000 [tokens](/wiki/ai/llm/tokenization) to **248,320**, and claimed language coverage from 29 languages to **201**. A larger vocabulary is what makes a model efficient in languages whose text would otherwise shatter into many tokens.

## Thinking became a dial, then stopped being optional

Qwen3 introduced a **hybrid thinking mode**: one model that could reason step by step or answer directly, switched by a flag. It was an early version of the consolidation that [OpenAI](/wiki/ai/models/openai), DeepSeek and [Mistral](/wiki/ai/models/mistral) all arrived at separately.

Since then it has changed twice. The binary switch became a graded `reasoning_effort` dial, and thinking became the default rather than an opt-in. On `Qwen3.8-2.4T-A95B` it **cannot be disabled at all**; `Qwen3.8-27B` still accepts a flag to turn it off. A reader porting code from Qwen3 will find the flag no longer does what it did.

## Position

Qwen's significance is best measured by what is built on it rather than by where it sits on any ranking. The DeepSeek distillation base counts above are the cleanest primary evidence. Beyond that, figures for the volume of community derivatives circulate in mutually inconsistent forms — counts of directly-derived models, of all variants, and of name matches on a model-hosting site are three different measurements, and blending them produces a number that means nothing.

Two criticisms belong on the record. The hosted models censor politically sensitive topics, and unlike some cases the behaviour is trained into the weights rather than applied at serving time, so self-hosting does not necessarily remove it. Questions about benchmark contamination are raised against open-weight families generally, but no specific allegation against a Qwen release is documented, and a general suspicion is not a finding.

A sourcing note for anyone following up: Qwen's official blog stopped being updated in September 2025, and the current site does not render without a browser. The live record is in the model repositories and their configuration files, which is a slightly unusual place for a frontier lab's primary documentation to live.

## Status

Checked 11 September 2026. The [QwenLM repositories](https://github.com/QwenLM) and the model cards on Hugging Face are the live sources; Alibaba Cloud Model Studio carries the hosted pricing.

**Qwen3.8**, released August 2026, is the current generation — four generations past the Qwen3 that most 2025 writing describes. The chain since then runs Qwen3 (April 2025) → Qwen3.5 (February 2026) → Qwen3.6 (April 2026) → Qwen3.7 (mid-2026, hosted only) → Qwen3.8.

| Model | Size | Licence | Notes |
| --- | --- | --- | --- |
| Qwen3.8-Max | not published | closed, hosted only | 3 August 2026 |
| `Qwen3.8-2.4T-A95B` | 2.4T total / 95B active | Qwen3.8-Max Licence | open weights, 12 August 2026 |
| Qwen3.8-27B | 27B | **Apache 2.0** | 14 August 2026, natively multimodal |

Specialised lines continue alongside the main ladder: vision-language, audio, coding, mathematics and image generation each have their own Qwen variants.

## Sources

- Yang et al., [Qwen3 Technical Report](https://arxiv.org/abs/2505.09388), arXiv:2505.09388 (2025)
- Yang et al., [Qwen2.5 Technical Report](https://arxiv.org/abs/2412.15115), arXiv:2412.15115 (2024)
- Bai et al., [Qwen-VL](https://arxiv.org/abs/2308.12966), arXiv:2308.12966 (2023)
- [QwenLM on GitHub](https://github.com/QwenLM) — the changelogs that replaced the blog
- [Qwen on Hugging Face](https://huggingface.co/Qwen) — model cards, configuration files and licence texts
- [DeepSeek-R1 repository](https://github.com/deepseek-ai/DeepSeek-R1) — the distillation base list
