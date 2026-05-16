---
title: "Single-Tick Liquidity"
weight: 6
---

A single-tick liquidity position is a [Uniswap](../) V3/V4 position whose range is exactly one [tick](ticks) wide — the narrowest range the protocol allows. Inside that one tick the position stops behaving like a curve and starts behaving like a *fixed-price block of depth*: trades fill at an almost constant rate until the position is exhausted, then price jumps to the next tick. It is the building block behind on-chain limit orders ("range orders") and behind the price corridor a [par token](../../par-token) lives in.

## A curve flattened to a point

A full-range [constant-product](../../constant-product-formula) pool prices every trade along `x * y = k`. [Concentrated liquidity](../../virtual-reserves) lets a provider restrict that curve to a chosen price range. Shrink the range far enough — to a single tick — and the slice of the curve the pool actually traverses is so short it is effectively a straight line.

A tick is one [basis point](https://en.wikipedia.org/wiki/Basis_point) wide:

```
price(i) = 1.0001^i
```

So a position seeded at tick `i` covers exactly `[1.0001^i, 1.0001^(i+1))` — a price band 0.01% tall. Across a window that narrow, marginal price barely moves. The position behaves like a *constant-sum* segment (`x + y = k`): swap in, get out at a near-fixed rate, with depth equal to the tokens seeded — until one side runs out.

## Exhaustion, not slippage

The defining property is what happens at the edges, not in the middle:

- While the position has inventory on the side you are buying, you trade at ~the tick price regardless of size. Depth is finite but flat.
- When that side is fully consumed, price reaches the top of the tick and stops. It cannot continue up through that position because the position is empty above it. The next trade only proceeds if there is liquidity in an adjacent tick.

This inverts the usual AMM intuition. A normal pool gives you continuous price impact and infinite (but ever-worsening) depth. A single-tick position gives you near-zero price impact and a hard quantity ceiling.

## Single-sided seeding

A single-tick position can be seeded entirely in one token by starting price at the edge of the tick. At the lower edge the position is 100% token0; a buyer brings token1 and walks price across the one tick, converting the position to token1 as they go. This is how a fixed supply can be deployed as a market with no paired capital — the seeded token *is* the entire offer.

## Where it shows up

- **Range orders.** Uniswap documents the single-tick position explicitly as an on-chain limit order: seed it out-of-range, let price cross it, withdraw the other side. The fill is the same fixed-price behavior described here.
- **Tight stable pairs.** LPs cluster in a few ticks around 1:1 because correlated assets never need the rest of the curve.
- **Par tokens.** A [par token](../../par-token) seats its entire supply in one tick at `tick = 0`, never withdraws it, and never adds liquidity below it — turning the "fixed price until exhausted" property into a permanent peg.

## Caveats

- **The tick must be initialized and aligned.** Positions must sit on multiples of the pool's `tickSpacing`. A 1-bp corridor requires `tickSpacing = 1`, which only the 0.01% fee tier (or a V4 pool configured that way) provides.
- **Outside the tick, the position is inert.** It earns no fees and provides no depth once price leaves the range — by design here, a liability for a yield-seeking LP.
- **"Fixed price" is fixed *within* the tick.** The band still has a 1-bp width; it is a corridor, not a single number. Treat the bound as `[1.0001^i, 1.0001^(i+1))`, not an exact rate.

## External links

- [Uniswap — Range orders](https://docs.uniswap.org/concepts/protocol/range-orders) — the single-tick position as a limit order
- [Uniswap V3 whitepaper](https://uniswap.org/whitepaper-v3.pdf) — Section 6, tick indexing
- [`TickMath.sol`](https://github.com/Uniswap/v3-core/blob/main/contracts/libraries/TickMath.sol) — tick ↔ sqrtPrice conversion
