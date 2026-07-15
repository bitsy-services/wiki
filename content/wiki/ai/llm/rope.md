---
title: "RoPE"
weight: 275
---

Rotary position embedding — the reason a model trained at 8k tokens ships with a 128k window.

Read a query's 64 numbers as 32 points in a plane. Rotate pair *i* by `m·θᵢ`: `m` is the row's position, `θᵢ` a fixed frequency shrinking as *i* grows, so early pairs spin fast and late ones barely move. Do the same to every key, then score as usual.

Rotation preserves the dot product. Rotate a query at row *m* and a key at row *n*, each by its own angle, and what survives in `q·k` depends on `m − n` — the offset, not the positions. Content still decides what a head hunts for; position enters only as "how far back."

Three consequences.

**No parameters.** The angles come from a base constant (usually 10,000), not from training. Nothing to learn, nothing to run out of — unlike the finite table of [absolute positional encoding](/wiki/ai/llm/positional-encoding).

**It lives inside attention.** RoPE touches q and k, never v, never the [residual stream](/wiki/ai/llm/residual-stream) — position is reapplied in every block, not mixed into the row once at the left edge.

**The window stretches afterwards.** The frequencies are continuous in position, so you can raise the base constant, fine-tune briefly, and the model works beyond its trained range. NTK scaling, position interpolation, and YaRN are variations on that move; it's how long-context models got long.

## Check yourself

Rotate a random q/k pair at positions (3, 7); take the dot product. Rotate the same vectors at (103, 107) — same offset, far-off positions — and take it again. They agree to floating-point noise. Try (3, 107) and it collapses. Ten lines of torch, no download: the whole mechanism.

## Depends on / leads to

Depends on [positional encoding](/wiki/ai/llm/positional-encoding). Leads to [context length and the O(n²) cost](/wiki/ai/llm/context-length).
