---
title: "Relative Inner-Product Invariance in Rotary Position Embeddings"
weight: 278
---

## Part

Relative inner-product invariance is an identity satisfied by [rotary position embedding (RoPE)](/wiki/ai/llm/rope), which rotates the [query and key vectors](/wiki/ai/llm/qkv-projections) an [attention head](/wiki/ai/llm/one-attention-head) computes from each token, two coordinates at a time, by an angle proportional to the token's position in the sequence. One token's query dotted with another's key is the attention score between the two, and the identity says that a query rotated for position *m*, dotted with a key rotated for position *n*, equals the unrotated query dotted with the key rotated for *n* − *m*. The score therefore depends on the query, the key and the distance between the two tokens, and not on where in the sequence the pair sits.

```text
(q rotated for m) · (k rotated for n)  =  q · (k rotated for n − m)
```

## Data

A head's query and key are each 64 numbers wide in [GPT-2 small](/wiki/ai/llm/gpt-2), computed from the token's [row](/wiki/ai/llm/glossary), its vector at that point in the model, by two learned matrices. GPT-2 itself does not use RoPE. It adds a learned vector for each position to the row before the first block, as [positional encoding](/wiki/ai/llm/positional-encoding) describes, so the sizes below are what RoPE would act on at GPT-2's head width.

| Name | Contents | Size at a 64-wide head | Written by | Read by |
| --- | --- | --- | --- | --- |
| query *q* | the head's projection of the row doing the scoring | 64 numbers per token, per head | the query projection | the rotation for the query's position *m* |
| key *k* | the head's projection of the row being scored | 64 numbers per token, per head | the key projection | the rotation for the key's position *n* |
| plane *i* | two of the 64 coordinates, rotated together as a point in a flat plane | 32 per head | the implementation's fixed pairing | the rotation |
| frequency θᵢ | the angle plane *i* turns through per position, in radians | 32 numbers, not learned | the formula θᵢ = 10000^(−2*i*/64), for *i* = 0 … 31 | the rotation |
| rotation R(*t*) | turns every plane *i* by *t*·θᵢ at once | computed from *t* each time; not a weight | the position *t* | the query and the key |
| score | the rotated query dotted with the rotated key | 1 number per (query token, key token) pair, per head | the dot product | division by √64, the [causal mask](/wiki/ai/llm/causal-mask) and [softmax](/wiki/ai/llm/softmax-and-temperature) |

Nothing in the table is learned except the two projections that produce *q* and *k*. The frequency formula is the one Vaswani et al. (2017) used for their sinusoidal position encoding, which Su et al. (2021) reused when they introduced RoPE.

Which two coordinates form a plane is a convention, and implementations differ. Meta's LLaMA reference code pairs adjacent coordinates, 2*i* and 2*i* + 1, and treats each pair as one complex number. HuggingFace's `rotate_half` pairs coordinate *i* with coordinate *i* + 32, half the head width away. The identity holds for any fixed pairing, because it holds one plane at a time. The two conventions cannot load each other's checkpoints unchanged, though: HuggingFace's script for converting Meta's LLaMA checkpoints reorders the output coordinates of the query and key projections and leaves every other weight matrix alone.

## Transforms

1. query *q* (64 numbers) → rotate each plane *i* by *m*·θᵢ → rotated query R(*m*) *q* (64 numbers)
2. key *k* (64 numbers) → rotate each plane *i* by *n*·θᵢ → rotated key R(*n*) *k* (64 numbers)
3. rotated query, rotated key → dot product → score (1 number)

Step 1 uses only *m* and step 2 only *n*. The offset between them first appears in step 3.

In one plane, rotation through an angle φ is multiplication by a 2 × 2 matrix. R(*t*) is 32 of these down the diagonal of a 64 × 64 matrix, plane *i* using the angle *t*·θᵢ:

```text
R(φ) = │ cos φ   −sin φ │
       │ sin φ    cos φ │
```

Two facts about rotations in one plane give the identity. The transpose of a rotation is the rotation the other way, R(*a*)ᵀ = R(−*a*), and rotations compose by adding their angles, R(*a*) R(*b*) = R(*a* + *b*). Together they give R(*a*)ᵀ R(*b*) = R(*b* − *a*), and because the 32 planes turn independently, the same holds for the whole 64 × 64 R(*t*). The score is then

```text
(R(m) q)ᵀ (R(n) k)  =  qᵀ R(m)ᵀ R(n) k
                    =  qᵀ R(n − m) k
```

Only *n* − *m* is left. Moving both tokens *s* positions along the sequence adds *s* to both *m* and *n*, and R(*m* + *s*)ᵀ R(*n* + *s*) is R(*n* − *m*) again.

The same fact in geometric form: the dot product of two vectors in one plane is |*q*| |*k*| cos α, where α is the angle between them. Shifting the pair turns both vectors through the same extra angle *s*·θᵢ, which changes neither α nor the lengths. A head's score is the sum of its 32 plane scores, and each is unchanged.

In one plane with θ = 1 radian per position, the query (1, 0) and the key (0.8, 0.6) score 0.212661 with the query at position 5 and the key at position 3. They score 0.212661 at positions 50 and 48, and 0.212661 at 1,005 and 1,003. With the key moved to position 4 they score 0.937124.

Reading a plane's two coordinates (*x*, *y*) as the complex number *x* + *iy* turns rotation by φ into multiplication by e^(*i*φ), and the dot product of two pairs into the real part of one number times the complex conjugate of the other. Su et al. put the conjugate on the key and write one plane's score as Re[*q* · conj(*k*) · e^(*i*(*m* − *n*)θ)], their equation 12. Putting the conjugate on the query instead gives Re[conj(*q*) · *k* · e^(*i*(*n* − *m*)θ)], which is *q*ᵀ R(*n* − *m*) *k* written one plane at a time.

Su et al. did not start from rotation. Their equation 11 states the requirement first: the inner product of the position-transformed query and key must be a function of the two tokens' vectors and *m* − *n* alone. They then derive rotation as a solution in two dimensions and apply it plane by plane. The paper calls it "a solution"; it does not show that rotation is the only one.

Adding position to the row, as GPT-2 does, gives no such identity. With a position vector *p* added to each row *x* before the projections, the score between rows *m* and *n* splits into four terms (Dai et al. 2019):

```text
(x_m + p_m)ᵀ W (x_n + p_n)  =  x_mᵀ W x_n  +  x_mᵀ W p_n  +  p_mᵀ W x_n  +  p_mᵀ W p_n
```

W is the query matrix and the key matrix multiplied into one, and the terms are content with content, content with position, position with content, and position with position. Nothing in the sum is forced to depend on *n* − *m* alone, so any relative structure has to be found by training, separately at each position.

The identity fixes *that* the score is a function of *q*, *k* and the offset. The frequencies fix *which* function. At a 64-wide head the fastest plane, θ₀ = 1, makes a full turn every 2π ≈ 6.28 positions, and the slowest, θ₃₁ ≈ 0.000133, makes one every 47,117. The methods that [stretch a trained model to a longer context](/wiki/ai/llm/rope#what-you-get) change these numbers and keep the identity. Position interpolation (Chen et al. 2023) multiplies every position by *L*/*L*′, the trained length over the target length, which is the same as dividing every θᵢ by *L*′/*L*. YaRN (Peng et al. 2023) rescales each plane's frequency by a different factor and also divides every score by one constant, which it calls a temperature. Both keep the score a function of *q*, *k* and *n* − *m*.

## Fits here

The rotation sits inside every head of every block of a RoPE model, between the query and key projections and the rest of the attention step. The LLaMA models, for example, dropped absolute position vectors and added rotary embeddings "at each layer of the network" (Touvron et al. 2023). Depth runs left to right and the sequence top to bottom, as everywhere in this section ([conventions](/wiki/ai/llm/conventions)):

```text
                               depth  →

  pos 3   row ──▶ k ──▶ rotate by 3·θ ──▶ R(3) k ──┐
  pos 4   row                                      │
  pos 5   row                                      │
  pos 6   row                                      │
  pos 7   row ──▶ q ──▶ rotate by 7·θ ──▶ R(7) q ──┴──▶ dot ──▶ qᵀ R(−4) k
    │
    ▼
 sequence
```

To the left, the query and key projections produce *q* and *k* from the row. To the right, the score is divided by the square root of the head width, masked and softmaxed, as in [one attention head](/wiki/ai/llm/one-attention-head#step-3-divide-by-the-square-root-of-the-head-width). The value vectors pass alongside unrotated.

Down the sequence, each row's key is rotated by that row's own position and nothing else. A key is therefore rotated once, when it is computed, and every later query scores it at the right offset without rotating it again. HuggingFace's LLaMA code rotates each key before writing it into the [KV cache](/wiki/ai/llm/kv-cache), which keeps every earlier token's keys and values between generation steps. A scheme that adds a learned term for each offset, as Shaw et al. (2018) do, cannot be folded into a cached key this way, because the term depends on the query's position as well.

Read this page after [RoPE](/wiki/ai/llm/rope), which introduces the rotation. [Context length](/wiki/ai/llm/context-length) follows.

## Does not do

**Give two pairs at the same distance the same score.** The identity holds for a fixed query and key. In a model, *q* and *k* are projections of rows that carry the surrounding context, so two tokens three positions apart in one sentence and two tokens three positions apart in another have different queries, different keys and different scores. What is shared along the sequence is the positional factor R(*n* − *m*): "three positions back" is the same rotation everywhere, so it does not have to be learned separately at each position, as it does with a [learned position table](/wiki/ai/llm/positional-encoding#thats-cheap-it-works-and-it-has-two-defects).

**Remove absolute position from the model.** Each vector is rotated by its absolute position, and only this one dot product is forced through R(*n* − *m*). Su et al.'s abstract puts it the same way: RoPE "encodes the absolute position with a rotation matrix and meanwhile incorporates the explicit relative position dependency in self-attention formulation." Absolute position reaches the model by other routes. Under the causal mask the row at position *m* can see *m* + 1 rows, and models trained with no position encoding at all [recover position from that alone](/wiki/ai/llm/positional-encoding#the-mask-leaks-order-on-its-own).

**Hold exactly in floating point.** The identity is algebra. An implementation computes each rotation angle from the absolute position, as *t* × θᵢ, and rounds it, so the rounding error grows with where the pair sits rather than with the offset. In float32 the same query and key at the same offset score 5.617583 at positions 7 and 3 and 5.653579 at positions 1,000,007 and 1,000,003 (the [Check](#check) below). In bfloat16, which keeps only 8 significant bits, a number near a million is stored to the nearest 4,096. The fastest plane's angles for positions 1,000,003 and 1,000,007 both come out as 999,424, and the angles of the other 31 planes also round to the same value for both positions, so the two rotations are identical and the offset disappears. HuggingFace's LLaMA code computes the angles in float32 with autocast, PyTorch's automatic switch to lower precision, turned off. In version 4.40 the comment there read "Force float32 since bfloat16 loses precision on long contexts".

**Make distant tokens attend less.** That is a separate claim, about the frequency list rather than the identity. Su et al. bound the size of the score by a factor that depends on *q* and *k* times a sum over the frequencies alone, and show that the sum falls as the distance grows (their Figure 2). A bound is a ceiling, not a prediction for any particular pair. Barbero et al. (2024) show that for queries and keys drawn from a standard normal distribution the expected score is zero at every distance, and that for any query and any distance there is a key whose score peaks at that distance. How the frequencies divide the work between near and far offsets is on the [RoPE page](/wiki/ai/llm/rope#why-a-spectrum-of-frequencies).

**Let a model run past its training length.** There is no table to run out of, so nothing fails at the first unseen position the way it does with GPT-2's 1,024-row position table. What the identity guarantees is narrower: a query and key at unfamiliar positions but a familiar offset are scored by the same function as in training. Past the training length the offsets are new too. A query at position 5,000, in a model trained on 2,048 tokens, also scores keys 4,000 positions back. Press et al. (2021) trained a rotary model on 512 tokens and evaluated it on longer inputs. Its [perplexity](/wiki/ai/llm/perplexity), roughly the number of tokens it is choosing between, was 20.07 at the training length. It was lowest, 19.79, with 200 tokens more, and had risen to 25.99 with 1,000 tokens more. Stretching the window further is done by changing the frequencies, as [Transforms](#transforms) describes.

**Touch the values or the residual stream.** Su et al. define the rotation for queries and keys only, and HuggingFace's `apply_rotary_pos_emb` takes a query and a key and returns the two rotated. The values are never rotated, and neither is the [residual stream](/wiki/ai/llm/residual-stream), the running per-token total that every block adds into.

**Carry over to linear attention unchanged.** Linear attention drops softmax, which makes its cost grow with the length of the sequence rather than with its square. It scores a pair by applying a fixed function, called a feature map, to the query and to the key and dotting the results, then divides each query's scores by their sum so that its weights add to 1. Su et al. apply RoPE to it by rotating after the feature maps and leaving that sum unrotated, "to avoid the risk of dividing zero", and they note that the resulting weights are "not strictly probabilistic normalized".

**Add a learned term for each offset.** RoPE is commonly called a relative position encoding, and Su et al. call it one, but the earlier schemes under that name work differently. Shaw et al. (2018) add a learned vector for each offset to the projected key and value, with offsets beyond 16 clipped to 16 in their base model, and beyond 8 to 8 in their big one. T5 (Raffel et al. 2019) adds a learned number to the score, with 32 of them covering offset ranges that grow logarithmically up to 128. Su et al. describe the difference as additive against multiplicative (their section 3.2.2): RoPE adds nothing to the score, and the offset enters only through the product of the two rotations.

## Related parts

- **Contains:** the rotation R(*t*) and the frequency list, both introduced on [RoPE](/wiki/ai/llm/rope).
- **Used by:** every head in every block of a RoPE model.
- **See also:** [positional encoding](/wiki/ai/llm/positional-encoding), [one attention head](/wiki/ai/llm/one-attention-head), [the KV cache](/wiki/ai/llm/kv-cache), [the causal mask](/wiki/ai/llm/causal-mask), [context length](/wiki/ai/llm/context-length).

### Sources

- Su et al., [RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864), arXiv:2104.09864 (2021) — the abstract for absolute and relative position, section 3.2.2 for additive against multiplicative, equation 11 for the requirement, equation 12 for the complex form, section 3.4.3 and Figure 2 for the decay bound, equation 19 for linear attention
- Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), arXiv:1706.03762 (2017)
- Dai et al., [Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context](https://arxiv.org/abs/1901.02860), arXiv:1901.02860 (2019) — section 3.3 for the four-term expansion
- Shaw, Uszkoreit & Vaswani, [Self-Attention with Relative Position Representations](https://arxiv.org/abs/1803.02155), arXiv:1803.02155 (2018)
- Raffel et al., [Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/abs/1910.10683), arXiv:1910.10683 (2019) — section 2.1
- Press, Smith & Lewis, [Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation](https://arxiv.org/abs/2108.12409), arXiv:2108.12409 (2021) — section 2.2, and the appendix table for models trained on 512 tokens
- Chen et al., [Extending Context Window of Large Language Models via Position Interpolation](https://arxiv.org/abs/2306.15595), arXiv:2306.15595 (2023)
- Peng et al., [YaRN: Efficient Context Window Extension of Large Language Models](https://arxiv.org/abs/2309.00071), arXiv:2309.00071 (2023)
- Barbero et al., [Round and Round We Go! What makes Rotary Positional Encodings useful?](https://arxiv.org/abs/2410.06205), arXiv:2410.06205 (2024) — propositions 3.1 and 3.2
- Touvron et al., [LLaMA: Open and Efficient Foundation Language Models](https://arxiv.org/abs/2302.13971), arXiv:2302.13971 (2023) — section 2.2
- HuggingFace transformers, [`modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) — `LlamaRotaryEmbedding`, `rotate_half`, `apply_rotary_pos_emb`; the float32 comment is in [version 4.40.0](https://github.com/huggingface/transformers/blob/v4.40.0/src/transformers/models/llama/modeling_llama.py)
- HuggingFace transformers, [`convert_llama_weights_to_hf.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/convert_llama_weights_to_hf.py) — `permute`, applied to the query and key weights
- Meta, [`llama/model.py`](https://github.com/meta-llama/llama/blob/main/llama/model.py) — `apply_rotary_emb`

## Check

GPT-2 has no RoPE, so this check runs on random vectors of GPT-2's head width and needs only torch, [no model](/wiki/ai/llm/running-the-checks#no-model-just-torch-or-tiktoken). It rotates one query and one key for four pairs of positions: three with the key four positions before the query, and a control with the key 104 positions back. It then repeats the four in three floating-point precisions.

```python
import torch

torch.manual_seed(0)
d = 64                                                # head width in GPT-2 small
theta = 10000 ** (-torch.arange(0, d, 2, dtype=torch.float64) / d)   # 32 frequencies

def rope(x, pos):
    a = pos * theta.to(x.dtype)                       # one angle per plane, in x's precision
    x1, x2 = x[0::2], x[1::2]                         # plane i is coordinates 2i and 2i+1
    return torch.stack([x1 * a.cos() - x2 * a.sin(),
                        x1 * a.sin() + x2 * a.cos()], dim=-1).flatten()

q, k = torch.randn(d, dtype=torch.float64), torch.randn(d, dtype=torch.float64)

for dtype in (torch.float64, torch.float32, torch.bfloat16):
    print(dtype)
    for m, n in [(7, 3), (107, 103), (1_000_007, 1_000_003), (107, 3)]:
        score = rope(q.to(dtype), m) @ rope(k.to(dtype), n)
        print(f"  query at {m:>9,}  key at {n:>9,}  score {score.item():.6f}")
```

It printed:

```text
torch.float64
  query at         7  key at         3  score 5.617582
  query at       107  key at       103  score 5.617582
  query at 1,000,007  key at 1,000,003  score 5.617582
  query at       107  key at         3  score 2.444756
torch.float32
  query at         7  key at         3  score 5.617583
  query at       107  key at       103  score 5.617575
  query at 1,000,007  key at 1,000,003  score 5.653579
  query at       107  key at         3  score 2.444749
torch.bfloat16
  query at         7  key at         3  score 5.593750
  query at       107  key at       103  score 5.843750
  query at 1,000,007  key at 1,000,003  score 7.343750
  query at       107  key at         3  score 1.656250
```

In float64 the three pairs four positions apart agree to every printed digit, from positions 7 and 3 to positions a million further on. The control pair scores 2.444756. It is what makes the check falsifiable: change the offset of any pair and its score moves. In float32 the far pair has drifted by 0.036. In bfloat16 even the near pairs are off in the second digit, and the far pair scores 7.343750. That is within rounding of the unrotated `q @ k`, 7.382404, because in every plane the far pair's two angles round to the same bfloat16 value, so the two rotations are identical and cancel completely.

## Spec

GPT-2 small has no RoPE. These are RoPE's constants at GPT-2 small's head width, with the frequency formula from Su et al. (2021).

| Constant | Value |
| --- | --- |
| Head width | 64 |
| Planes per head | 32 |
| Frequency base | 10,000 |
| Fastest plane, θ₀ | 1 radian per position; a full turn every 6.28 positions |
| Slowest plane, θ₃₁ | 0.000133 radians per position; a full turn every 47,117 positions |
| Weights added by RoPE | 0 |
