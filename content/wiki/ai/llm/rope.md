---
title: "RoPE"
weight: 275
---

[Attention scores a query against a key](/wiki/ai/llm/one-attention-head) with a dot product, and a dot product has no idea where either token sits in the sequence. Order has to be put in on purpose. Rotary position embedding (RoPE) puts it in as *rotation* — and does it so that the score between two tokens depends only on the distance between them.

## Position is invisible to a dot product

Attention works by dotting a query row against a key row: a large dot product means "this token is relevant to that one." But the dot product looks only at the *contents* of the two vectors. It cannot tell whether the key is the token right before the query or five hundred tokens back. Swap two rows of the sequence and every attention score comes out identical. Order isn't in the arithmetic, so it has to be injected — which is the job of [positional encoding](/wiki/ai/llm/positional-encoding).

The obvious way to do that — the one GPT-2 uses — is to learn a vector for each slot and add it to the token before the first block. It works, but it has two nagging flaws:

- **It's finite.** One learned vector per position means a fixed maximum length. There's no vector for slot 1025, so there's no slot 1025.
- **It's absolute.** The vector for position 300 bears no built-in relation to the one for 301. "Three tokens back" is a different, separately-learned fact at every position in the sequence.

What we'd really like is the opposite of both: a scheme with nothing to run out of, where the score between two tokens depends only on *how far apart they are* — the gap, not the absolute slots. RoPE is that scheme.

## The idea: turn position into rotation

Take a query vector — 64 numbers, for [one head](/wiki/ai/llm/multi-head-attention). Read those 64 numbers as 32 pairs, and read each pair as a point in a plane: an *(x, y)*. Now rotate.

For the token at position *m*, spin each pair by an angle proportional to *m*. Pair *i* turns by *m·θᵢ*, where θᵢ is a fixed frequency for that pair (why the frequencies differ comes below). A token at position 0 isn't rotated at all; a token at position 5 is spun five times as far as one at position 1. Do the identical thing to every key. Then score with the ordinary dot product — nothing else in attention changes.

That's the whole mechanism: **position becomes an angle, and a token's vector is its content spun around by its place in line.**

```text
q at position m:   rotate each 2D pair by  m · θᵢ
k at position n:   rotate each 2D pair by  n · θᵢ
score = (rotated q) · (rotated k)     ← ordinary dot product
```

## Why the score sees only the gap

Here is the property that makes it pay off. Rotate one 2D vector by angle *a* and another by angle *b*, then dot them — for a fixed pair of vectors, the result depends only on *(a − b)*, the *difference* of the two angles. (Turning both vectors by the same extra amount doesn't change the angle between them, so it can't change their dot product.)

Apply that to a query at position *m* and a key at position *n*. The query pair was spun by *m·θᵢ* and the key pair by *n·θᵢ*, so their contribution to the score depends on *(m − n)·θᵢ* — the offset *m − n*, and nothing about *m* or *n* on their own. Content still decides *what* a head looks for; position enters purely as *how far back* a match is.

A concrete check, with a single pair. Pick any 2D *q* and *k*. Rotate them for positions (3, 7) and dot them — call the result *s*. Now rotate the same two vectors for positions (103, 107): the gap is still 4, and you get *s* back, to floating-point noise. Move to (3, 107) — gap 104 — and the score is completely different. Same distance, same score; different distance, different score. Absolute position has dropped out of the arithmetic.

## Why a spectrum of frequencies

Why give each pair its own θᵢ instead of turning them all at the same rate? Because a single rate wraps around. An angle lives on a circle: rotate far enough and *m·θ* comes back to where it started, so two very different distances would land on the same angle and become indistinguishable.

RoPE fixes this the way a clock does. A clock reads a wide range of times unambiguously because its hands turn at different speeds — the second hand for fine distinctions, the hour hand for coarse ones. RoPE uses a whole spectrum of frequencies: early pairs spin fast (θ near 1), later pairs barely move (θ shrinking toward 1/10,000, from the conventional base constant of 10,000). The fast hands resolve nearby tokens; the slow hands keep distant tokens apart. Together they pin down offsets across the whole context without aliasing.

## What you get

Three things fall out, and each is a direct consequence of encoding position as rotation.

**No parameters.** The angles come from that base constant, not from training. There's nothing to learn and — the part that matters — nothing to run out of, unlike the finite lookup table of absolute positional encoding.

**It lives inside attention.** RoPE rotates q and k and nothing else — never the [values](/wiki/ai/llm/qkv-projections), never the [residual stream](/wiki/ai/llm/residual-stream). Position isn't stirred into the token once at the left edge; it's reapplied fresh inside every block, every time attention runs.

**The window stretches afterward.** Here is where the headline finally lands: a model trained at 8k tokens routinely ships with a 128k-token window. That's possible because the rotation is *continuous* in position — position 8,000.5 is a perfectly good angle even if training never used it. Nudge the frequencies (raise the base, or interpolate positions so the trained range is stretched to cover a longer one), fine-tune briefly, and the model works well past the length it saw in training. NTK-aware scaling, position interpolation, and YaRN are all variations on that one move — and it's how long-context models got long.

## Check yourself

Rotate a random q/k pair at positions (3, 7) and take the dot product. Rotate the same vectors at (103, 107) — same offset, far-off positions — and take it again: they agree to floating-point noise. Try (3, 107) and it collapses. Ten lines of torch, no download, and you've watched absolute position drop out of the score — the whole mechanism in one experiment.

## Depends on / leads to

Depends on [positional encoding](/wiki/ai/llm/positional-encoding). Leads to [context length and the O(n²) cost](/wiki/ai/llm/context-length).
