---
title: "Qwen3.8"
weight: 10
---

Qwen3.8 is [Alibaba](/wiki/ai/models/qwen)'s current generation, released across August 2026. It is worth a page for two reasons that cut against the family's reputation: its flagship's weights are **no longer Apache 2.0**, and its architecture is **no longer a conventional transformer**.

Most writing about Qwen describes Qwen3, from April 2025. Four generations have shipped since — Qwen3.5 in February 2026, Qwen3.6 in April, Qwen3.7 in mid-year as a hosted-only release, and Qwen3.8 in August — and both of the changes above happened inside that gap.

## The lineup, and the licence split inside it

| Model | Size | Licence |
| --- | --- | --- |
| Qwen3.8-Max | not published | closed, hosted only |
| `Qwen3.8-2.4T-A95B` | 2.4T total / 95B active | Qwen3.8-Max Licence |
| Qwen3.8-27B | 27B | **Apache 2.0** |

The open flagship shipped nine days after the closed one, which is the strategy in miniature: the model whose weights you can have is not the best model Alibaba has, and the model whose weights you can have comes with conditions.

Those conditions are a **revenue gate**. An organisation above US$50 million in aggregate revenue over any twelve months needs a separate commercial agreement, and a prominent-attribution requirement applies above 100 million monthly active users (MAU) or $20 million in monthly revenue. Qwen3.8-27B carries none of this and is genuinely Apache 2.0.

Three labs in this section gate their open weights, and no two gate on the same thing: [Meta](/wiki/ai/models/meta) on monthly active users frozen at a release date, [Mistral](/wiki/ai/models/mistral) on monthly revenue, Alibaba on aggregate revenue over a rolling year. A reader who learns one and assumes the others will be wrong.

## The architecture stopped being a plain transformer

Through Qwen3, a layer was an [attention](/wiki/ai/llm/attention) block followed by an [MLP](/wiki/ai/llm/the-mlp) block, repeated. From Qwen3.5 that is no longer true.

`Qwen3.8-2.4T-A95B` has 92 layers repeating a four-block pattern:

```text
3 × (Gated DeltaNet → MoE)
1 × (Gated Attention → MoE)
```

**Gated DeltaNet** is a linear-attention variant. Where ordinary attention compares every token against every earlier token — work that grows with the square of the sequence length — a linear-attention layer maintains a fixed-size running state instead, so its cost grows in proportion to length rather than to length squared. What it gives up is the ability to reach back and look at any specific earlier token precisely, which is exactly what full attention is good at.

Hence the interleave: **only one layer in four pays the quadratic cost.** The three cheap layers carry the sequence forward; the fourth can look anywhere.

This is the same structural bet made independently by [Gemma](/wiki/ai/models/google/gemma) with local and global attention interleaved, and by [Llama 4](/wiki/ai/models/meta/llama-4) with its `iRoPE` chunked and unchunked layers. Three labs, three different cheap mechanisms, one shared conclusion: full attention in every layer is more than a model needs.

### The mixture of experts is very fine-grained

Every block pairs its sequence mixer with a [mixture-of-experts](/wiki/ai/llm/mixture-of-experts) layer — many feed-forward blocks called experts, with a router sending each token through only a few. Qwen3.8's has **512 experts and activates 11 per token**: 10 chosen by the router plus one *shared* expert that every token passes through regardless, holding whatever is common to all of them.

512 experts activating 11 is finer-grained than almost anything else published. More, smaller experts means a much larger space of possible expert combinations for the same active-parameter budget, so specialisation can be narrower.

The native context is 262,144 [tokens](/wiki/ai/llm/tokenization), extended toward a million by YaRN — a method for stretching [rotary position embeddings](/wiki/ai/llm/rope) past the length a model trained on.

## Thinking is no longer optional

Qwen3 introduced a **hybrid thinking mode**: one model that could reason step by step or answer directly, chosen by a flag. It was among the earliest versions of a consolidation that [OpenAI](/wiki/ai/models/openai), [DeepSeek](/wiki/ai/models/deepseek/deepseek-v4) and Mistral all reached separately.

Since then it has changed twice. The flag became a graded `reasoning_effort` dial, and thinking became the default rather than something to opt into. On `Qwen3.8-2.4T-A95B` it **cannot be disabled at all**; `Qwen3.8-27B` still accepts a flag to turn it off.

Code written against Qwen3 that sets `enable_thinking: False` will therefore behave differently depending on which current model it points at, which is an unusually sharp break for a family that has otherwise been easy to move around inside.

## Two numbers that show what the generations bought

The **vocabulary** grew from about 152,000 entries to **248,320**, and claimed language coverage from 29 languages to **201**. These are related. A larger vocabulary means text in languages that would otherwise shatter into many short tokens can be represented in fewer, which makes the model both cheaper and better in those languages — the cost being a larger embedding table and a wider output layer.

## Status

Checked 11 September 2026. The [QwenLM repositories](https://github.com/QwenLM) and the Hugging Face model cards are the live sources; Alibaba Cloud Model Studio carries hosted pricing.

Qwen3.8-Max was released 3 August 2026, `Qwen3.8-2.4T-A95B` on 12 August and Qwen3.8-27B on 14 August. The 27B model has a vision tower and is natively multimodal rather than text-only. Specialised lines — vision-language, audio, coding, mathematics, image generation — continue alongside the main ladder.

A sourcing note: Qwen's official blog stopped being updated in September 2025, and the current site does not render without a browser. The live record is in the repositories and their configuration files.

## Sources

- [Qwen on Hugging Face](https://huggingface.co/Qwen) — model cards, configuration files and licence texts
- [QwenLM on GitHub](https://github.com/QwenLM) — the changelogs that replaced the blog
- Yang et al., [Qwen3 Technical Report](https://arxiv.org/abs/2505.09388), arXiv:2505.09388 (2025) — the last generation with a full report
- Yang et al., [Gated Delta Networks](https://arxiv.org/abs/2412.06464), arXiv:2412.06464 (2024) — the linear-attention mechanism
- Peng et al., [YaRN](https://arxiv.org/abs/2309.00071), arXiv:2309.00071 (2023)
