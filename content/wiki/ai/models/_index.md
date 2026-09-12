---
title: "Model Builders"
weight: 90
bookCollapseSection: true
---

A model builder is an organisation that trains large language models and owns the resulting weights: the numbers a trained model consists of, which nobody writes by hand and which training alone sets. Training one at the leading edge means assembling three separately scarce things — a datacentre holding tens of thousands of accelerator chips, a corpus of text measured in tens of trillions of [tokens](/wiki/ai/llm/tokenization), and a team that has done it before. The capital requirement is what keeps the list short. This section covers eight organisations — five in the United States, two in China, one in France — and the model families they ship.

The first thing to know about any of them is whether you can download the weights. A **closed-weight** model exists only behind its builder's interface: requests go to the builder's hardware, and the weights never leave it. An **open-weight** model is published as a file anyone can run on their own machines. The split is not a proxy for quality — open-weight models from DeepSeek and Alibaba have traded places with the closed frontier repeatedly — but it decides almost everything else about how a model can be used: whether it can process data that must not leave a building, whether a third party can fine-tune it, whether the builder can withdraw it, and whether anyone outside the lab can inspect what it actually does. "Open weights" is also not "open source": most open-weight licences in this section restrict something, and Meta's restricts by revenue.

What these pages are careful about is the difference between what a lab **publishes** and what is **known**. Meta, DeepSeek, Alibaba and Mistral release parameter counts, training-token counts and architectural detail alongside their weights. Anthropic, OpenAI and Google publish essentially none of it for their flagship models, and the confident figures circulating for those models come from leaks and repetition rather than disclosure. Where a page here states a model's size, a lab stated it; where a lab has not, the page says so instead of guessing.

## What these pages are, and are not

The rest of the [AI section](/wiki/ai) explains the machinery. [Large language models](/wiki/ai/llm) takes a transformer apart — [attention](/wiki/ai/llm/attention), [the MLP](/wiki/ai/llm/the-mlp), [the KV cache](/wiki/ai/llm/kv-cache), [mixture of experts](/wiki/ai/llm/mixture-of-experts) — and [neural networks](/wiki/ai/neural-network) supplies the parts underneath it. These pages do not re-teach any of that. They say who built what, which lab introduced which mechanism, and how to read the names.

They are also deliberately thin on numbers that move. Prices change without an announcement and leaderboard positions change monthly, so each page quarantines everything perishable into a single dated `Status` section and links the vendor's own page as the live source. A reader who finds that section stale has lost one paragraph rather than a page's worth of credibility.

## Reading the names

The single most common reason to arrive at a page like this is that a name made no sense. The schemes are genuinely inconsistent, they are rarely explained by the vendor, and no lab explains a competitor's:

- A **family** is a lineage sharing a name and a training approach — Claude, GPT, Gemini, Llama, Qwen, Grok.
- A **tier** is a size or capability rung within one generation, usually priced differently. Anthropic names its tiers with words (Haiku, Sonnet, Opus); OpenAI and Google use suffixes (`mini`, `nano`, Flash, Pro).
- A **generation** is a version number, and the numbering is not comparable between labs. Gemini 3 and Claude 5 and Llama 4 say nothing about each other.
- A **variant** is the same generation retrained or configured for one job — reasoning, code, vision, on-device.

Parameter counts follow their own convention. For a [mixture-of-experts](/wiki/ai/llm/mixture-of-experts) model, the **total** count is what must be held in memory and the **active** count is what each token is multiplied by, so a model advertised at 26 billion parameters with 4 billion active costs memory like the former and arithmetic like the latter. Both numbers matter and they answer different questions.

## Wiki Pages

{{< section >}}
