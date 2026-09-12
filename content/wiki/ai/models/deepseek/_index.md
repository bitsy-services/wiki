---
title: "DeepSeek"
weight: 50
bookCollapseSection: true
---

DeepSeek is a Chinese lab that publishes frontier-scale model weights — its current generation under the MIT licence — and describes their architecture in genuine technical papers. It is the most useful builder in this section for anyone trying to understand how a modern large language model is actually put together, because it is the only one operating at that scale that still publishes parameter counts, routing schemes, training objectives and numerical formats in enough detail to reimplement from.

Two of its results changed what the rest of the field does. **Multi-head latent attention** shrinks the [KV cache](/wiki/ai/llm/kv-cache) by roughly fifty times, which is the single biggest lever on what long-context serving costs. And **DeepSeek-R1** showed that reasoning behaviour can be trained by reinforcement learning alone, with no worked examples to imitate first.

## The company

DeepSeek was founded in 2023 by Liang Wenfeng and is based in Hangzhou. Its distinguishing feature is its funding: it is backed by **High-Flyer**, a quantitative hedge fund Liang also founded, rather than by venture capital. The fund had already built GPU clusters for trading research, so the lab began with compute rather than raising to buy it.

That matters because of the second constraint. United States export controls restrict which accelerators can be sold into China, and DeepSeek's published work is explicit about training on H800s — the cut-down part Nvidia produced for that market — rather than on the unrestricted hardware its competitors use. Most of the engineering described below exists because of that limit. The efficiency is not incidental; it is the point.

## The family

The lineage is short and the numbering is honest:

**The general line.** DeepSeek LLM (2024, dense, 7B and 67B) → V2 (May 2024, 236B total / 21B active) → V3 (December 2024, 671B total / 37B active) → V3.1 and V3.2 (2025) → **V4** (April 2026, Pro at 1.6T total / 49B active and Flash at 284B / 13B, with a million-token context) → V4.1-Flash (September 2026, 552B, natively multimodal).

**The reasoning line, and how it ended.** DeepSeek-R1-Zero and DeepSeek-R1 arrived in January 2025, both built on DeepSeek-V3-Base. R1-0528 in May 2025 was the last model shipped under the R name. **There is no R2.** The line merged back into the general one: V3.1 introduced "a hybrid reasoning architecture: a single model supports both thinking mode and non-thinking mode," and by V4 reasoning is a per-request effort setting. This is the same consolidation OpenAI made when GPT-5 absorbed the `o`-series, arrived at independently and at about the same time.

**The distilled models** are the part most often misdescribed. DeepSeek published six dense models trained on R1's reasoning traces — but not on DeepSeek base models. Four are built on Qwen and two on Llama. That is worth knowing for the licence trap below, and it is also the best single piece of evidence for how much of the open-weight ecosystem rests on [Alibaba's Qwen](/wiki/ai/models/qwen).

### The licence trap

**DeepSeek-R1 is MIT-licensed, and so are V4-Pro and V4.1-Flash.** MIT is a genuine open-source licence with no user-count threshold, no revenue trigger and no acceptable-use annex — which puts DeepSeek at the permissive end of this entire section.

But **the distilled models inherit their base models' licences, not R1's.** "R1 is MIT" is true of R1 and false of R1-Distill-Llama-70B, which carries Llama's community licence and its restrictions. Anyone choosing a distill on licensing grounds needs to check the base, not the brand.

## The architecture

DeepSeek-V3 is the reference configuration, and four ideas in it are worth understanding separately.

### Multi-head latent attention

Ordinary [attention](/wiki/ai/llm/attention) caches a key vector and a value vector for every token, every head and every layer. That cache is what makes long contexts expensive in memory, and [grouped-query attention](/wiki/ai/llm/grouped-query-attention) attacks it by having several query heads share one key-value head.

Multi-head latent attention attacks it differently: it compresses the keys and values of *all* heads jointly into a single low-dimensional latent vector per token, and reconstructs the per-head keys and values from that latent when they are needed. The paper's framing is "the low-rank joint compression for attention keys and values to reduce Key-Value (KV) cache during inference."

The saving is the number to carry away. Per token per layer, V3 caches a 512-number latent plus a 64-number positional key — **576 numbers**, against 32,768 for the equivalent full multi-head attention. That is roughly a fiftieth. The V2 paper puts the comparison against grouped-query attention directly: the cache “is equal to GQA with only 2.25 groups, but its performance is stronger than MHA” — MHA there being ordinary multi-head attention. That is a smaller cache than grouped-query attention is normally configured to use, without grouped-query attention’s quality cost.

The subtle part is positional information. [Rotary position embedding](/wiki/ai/llm/rope) rotates keys by an angle that depends on the token's position, and that rotation does not survive being pushed through the reconstruction. So the key is split in two: a compressed part rebuilt from the latent, and a small **decoupled** part that carries the rotation and is cached separately. The final key is the two concatenated. The 64 extra numbers above are that decoupled part.

**Multi-head latent attention is no longer what DeepSeek ships.** V3.2 replaced it with a sparse-attention scheme, and V4 with a different hybrid again. It is described here because it is the version with a published paper, a clear mechanism and a measurable result — and because the idea that spread is the general one: compress the cache rather than share it.

### Fine-grained experts, and a shared one

V3's [mixture of experts](/wiki/ai/llm/mixture-of-experts) differs from the standard design in two ways. It uses many narrow experts rather than a few wide ones — 256 experts of intermediate dimension 2048, against a hidden dimension of 7168, with 8 activated per token. More, smaller experts means many more possible combinations for the same activated-parameter budget, so specialisation can be finer.

Alongside them sits **one shared expert** that every token passes through. It absorbs whatever is common to all tokens, so the 256 routed experts do not each have to relearn it.

### Load balancing without an auxiliary loss

A mixture-of-experts model has a failure mode called routing collapse, where the router learns to send nearly everything to a few experts and the rest go untrained. The standard fix adds a penalty term to the loss that pushes routing toward an even spread — which works, but means the model is partly optimising something other than predicting the next token.

V3 removes that trade-off. It keeps a per-expert bias that is adjusted during training to even out the load, and that bias affects *routing* only, not the weighting of the expert's output. The load is balanced without adding a competing gradient signal. This is V3's headline architectural contribution.

### Multi-token prediction, FP8, and the pipeline

Three more, in brief. V3 trains with a **multi-token prediction** objective — each position predicts several future tokens rather than one — which densifies the training signal and also leaves the model ready for [speculative decoding](/wiki/ai/llm/speculative-decoding). It trains in **FP8**, an 8-bit floating-point format, for most of the arithmetic, with selected operations kept at higher precision. And **DualPipe** is its pipeline-parallelism scheme, arranged so that the all-to-all traffic a mixture of experts generates between machines overlaps with computation instead of stalling it.

## The $5.576M figure, stated exactly

This is the most misreported number in the field, and the paper is careful in a way the reporting was not.

Table 1 of the V3 report gives 2,788,000 H800 GPU-hours in total — 2,664K for pre-training, 119K for context extension, 5K for post-training — and values them at **$5.576M**. The caption states the assumption: "assuming the rental price of H800 is $2 per GPU hour."

The paper then says what the figure excludes, in the same table's note: "Note that the aforementioned costs include only the official training of DeepSeek-V3, **excluding the costs associated with prior research and ablation experiments on architectures, algorithms, or data**."

So it is a notional rental valuation of the compute for one successful run. By construction it also excludes the capital cost of the cluster — the GPUs were owned, not rented — along with salaries, data acquisition, every failed run, and everything to do with R1. "DeepSeek built a frontier model for $5.6 million" is not the claim the paper makes.

What the figure does establish is a real efficiency result, and the supporting rate is the more useful number: training on each trillion tokens took 180,000 H800 GPU-hours, "3.7 days on our cluster with 2048 H800 GPUs." The report also notes something rarely stated aloud: "Throughout the entire training process, we did not experience any irrecoverable loss spikes or perform any rollbacks."

## How R1 was trained

R1's result is that reasoning can be learned from scratch by reinforcement learning, without first being shown worked examples. The paper: "we demonstrate that reasoning capabilities can be significantly improved through large-scale reinforcement learning (RL), **even without using supervised fine-tuning (SFT) as a cold start**."

**DeepSeek-R1-Zero** is the pure version — reinforcement learning applied directly to DeepSeek-V3-Base with no supervised data at all. Three choices make it work:

**The reward is rules, not a model.** Correctness is checked mechanically: maths answers must appear in a box so they can be string-matched, and code is run against test cases by a compiler. The paper explains the choice as avoiding a known failure: "We do not apply the outcome or process neural reward model… because we find that the neural reward model may suffer from **reward hacking** in the large-scale reinforcement learning process." A model that scores answers can be gamed; a compiler cannot.

**The prompt template constrains form, not content.** It requires the reasoning to sit between `<think>` tags and says nothing about how to reason — "avoiding any content-specific biases—such as mandating reflective reasoning." Long chains of thought emerged from the training rather than being demonstrated.

**The algorithm drops the critic.** Standard [reinforcement learning from human feedback](/wiki/ai/llm/rlhf) uses proximal policy optimization, which needs a second network roughly the size of the model being trained to estimate how good a state is. Group relative policy optimization (GRPO) removes it: sample a group of answers to the same question, and use the group's mean reward as the baseline instead. The saving is an entire model's worth of memory and compute. GRPO comes from DeepSeek's earlier DeepSeekMath paper, not from the R1 paper.

## Reception and criticism

R1's release in January 2025 was followed by a sharp fall in Nvidia's share price, on the reading that frontier capability had become much cheaper to reach than the market assumed. That reading was partly right and partly a misunderstanding of the $5.576M figure above.

Three criticisms are documented and belong on the record. OpenAI alleged that DeepSeek had distilled its models — trained on outputs from OpenAI systems — which DeepSeek has not confirmed. The hosted service censors politically sensitive topics, and the behaviour differs between the hosted model and the open weights, so self-hosting does not necessarily reproduce it. And several governments have restricted the app on data-privacy grounds.

## Status

Checked 11 September 2026. DeepSeek's [API documentation](https://api-docs.deepseek.com/) is the live source; the [update log](https://api-docs.deepseek.com/updates/) is where releases are announced.

**DeepSeek-V4** is the current generation, announced 24 April 2026 as `deepseek-v4-pro` and `deepseek-v4-flash`, with **DeepSeek-V4.1-Flash** shipping on 10 September 2026 as the smallest model in the new architecture family, with native visual understanding. The legacy `deepseek-chat` and `deepseek-reasoner` endpoints that served V3 and R1 were retired on 24 July 2026. Reasoning is exposed as an effort level rather than a separate model.

## Sources

- DeepSeek-AI, [DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437), arXiv:2412.19437 (2024) — multi-head latent attention, DeepSeekMoE, auxiliary-loss-free balancing, FP8, DualPipe, and the cost table
- DeepSeek-AI, [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948), arXiv:2501.12948 (2025)
- Shao et al., [DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models](https://arxiv.org/abs/2402.03300), arXiv:2402.03300 (2024) — introduces GRPO
- DeepSeek-AI, [DeepSeek-V2](https://arxiv.org/abs/2405.04434), arXiv:2405.04434 (2024) — the first multi-head latent attention paper
- [DeepSeek-R1 repository](https://github.com/deepseek-ai/DeepSeek-R1) — licence terms and the distilled-model base list
