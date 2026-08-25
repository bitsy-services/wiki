---
title: "Fee Distribution in Concentrated Liquidity"
weight: 10
---

In [Uniswap V2](../), every liquidity provider owns a fraction of a single, full-range pool. Fees accrue to the reserves themselves, so an LP's share grows automatically: burning the LP token returns slightly more of each asset than went in, and the difference is the fees. No per-LP bookkeeping is needed because there is nothing to book — the pool is one giant homogeneous pot.

[Concentrated liquidity](https://docs.uniswap.org/concepts/protocol/concentrated-liquidity) breaks that symmetry. Each position occupies its own price range, and only positions whose range contains the current price earn fees on a given swap. The naïve implementation would keep a list of active positions and, on each swap, iterate over them paying out pro-rata. Gas per swap would then scale with the number of LPs, and a single spammer could brick the pool by opening a million dust positions.

Uniswap V3 (and V4, which inherits the same accounting) sidesteps this entirely. **No code path in the protocol ever iterates over LPs.** Swaps are O(1) in LP count. Claims are O(1) per LP. The trick is a *pull-based accumulator*: the pool records one running number per swap, and each LP, whenever they feel like it, subtracts two snapshots of that number to learn what they're owed.

## The Global Accumulator

The pool maintains two state variables, `feeGrowthGlobal0` and `feeGrowthGlobal1`, one per token. These are [Q128.128 fixed-point](https://en.wikipedia.org/wiki/Q_(number_format)) numbers with a very specific meaning:

> Cumulative fees earned per unit of in-range liquidity, summed over every swap since pool inception.

The units matter. It is **not** "total fees collected." It is fees *divided by the liquidity that was active at the time they were collected*. On each swap the pool executes roughly:

```text
feeGrowthGlobal0 += feeAmount0 * 2^128 / liquidity
```

That is a single `SSTORE` per token per swap, regardless of how many LPs share the active range. The `* 2^128` is just the fixed-point shift — the denominator is the current in-range [liquidity](../../liquidity-pool) `L`, the same `L` that appears in the concentrated-liquidity price curve.

Because everyone in range contributed `L` proportionally, everyone gets paid proportionally when they later multiply by their own `Lᵢ`. The accumulator is the only piece of state the swap path touches for fee purposes.

## Per-Tick Outside Growth

A position only earns fees while the price is inside its range. So each LP needs to know not the global accumulator, but the portion of it that accrued *while the price was between my lower and upper ticks*. Call this `feeGrowthInside`.

Uniswap computes it by decomposition. Every initialized tick stores a `feeGrowthOutside` value, representing accumulator growth on the "other side" of that tick relative to the current price. The semantics are defined recursively: when the price crosses a tick, the pool flips that tick's `feeGrowthOutside` to `feeGrowthGlobal - feeGrowthOutside`. This is the only update ticks need during a swap, and it happens inside `Tick.cross` in `Tick.sol`.

With this invariant, the growth inside any range can be recovered in O(1):

```solidity
// For each token, given current tick `tickCurrent`:
if (tickCurrent < tickLower) {
    feeGrowthInside = tickLower.feeGrowthOutside - tickUpper.feeGrowthOutside;
} else if (tickCurrent >= tickUpper) {
    feeGrowthInside = tickUpper.feeGrowthOutside - tickLower.feeGrowthOutside;
} else {
    feeGrowthInside = feeGrowthGlobal
                    - tickLower.feeGrowthOutside
                    - tickUpper.feeGrowthOutside;
}
```

The intuition: `feeGrowthGlobal` is the whole number line. Subtracting the "below-lower" and "above-upper" slices leaves exactly the "inside" slice. The signed arithmetic on Q128 numbers is deliberately allowed to underflow and wrap — what matters is that *differences* between two such readings are meaningful, and those differences are what LPs actually read.

## Per-Position Snapshots and Lazy Pulls

Each position stores `feeGrowthInside0Last` and `feeGrowthInside1Last`: the value of `feeGrowthInside` the last time the position was touched. Owed fees are computed on demand in `Position.update`:

```text
tokensOwed += liquidity * (feeGrowthInside_now - feeGrowthInside_last)
feeGrowthInside_last = feeGrowthInside_now
```

LPs "claim" fees by *poking* the position — calling `modifyLiquidity` (in V4) or `burn` / `collect` (in V3) with a `liquidityDelta` of zero. The poke recomputes `feeGrowthInside`, applies the formula above, and credits the delta to `tokensOwed`, which can then be withdrawn via `collect`. Until a poke happens, the LP's fees sit *implicitly* in the accumulator. No storage slot anywhere tracks "LP Alice is owed 4.2 USDC." That fact is latent in the difference between two numbers.

## Why Pro-Rata Works Without a List

Suppose Alice has `L_A = 1000` and Bob has `L_B = 3000` in the same range `[a, b]`. While the price sits in that range, a swap pays `F = 12` units of fee0. The pool updates:

```text
feeGrowthGlobal0 += 12 / 4000 = 0.003   (ignoring the Q128 shift)
```

Neither Alice nor Bob is notified. Later, each of them pokes their position. Both compute the same `Δ feeGrowthInside0 = 0.003`. They multiply by their own liquidity:

- Alice: `1000 * 0.003 = 3`
- Bob:   `3000 * 0.003 = 9`
- Total: `12` — exactly the fee the pool collected.

The invariant `Σᵢ Lᵢ · Δf = L · Δf = F` falls out automatically because `L = Σᵢ Lᵢ` is the very denominator used when `Δf` was written. Every LP in the range reads the *same* `feeGrowthInside`, so their independently computed claims sum to the total with no coordination and no list.

## What The Design Buys

- **Constant gas per swap.** A swap's fee accounting is one read and one write per token, regardless of whether the pool has 10 LPs or 10 million.
- **Permissionless, asynchronous claims.** LPs collect whenever they want. The pool does not care if some positions are never poked — their fees remain recoverable indefinitely.
- **No griefing surface.** Nothing can force the pool to iterate a list, because there is no list.
- **[NFT](/wiki/economics/finance/defi/nft)-wrapped positions.** Because each position is a pure function of two tick snapshots and one stored `feeGrowthInsideLast`, Uniswap's [NonfungiblePositionManager](https://github.com/Uniswap/v3-periphery/blob/main/contracts/NonfungiblePositionManager.sol) can wrap positions in [ERC-721](/wiki/economics/finance/defi/ethereum/erc-721) tokens and transfer them freely. The new owner pokes and is paid correctly.

## What It Costs

- **Precision loss at low liquidity.** The `feeAmount / liquidity` division rounds down. When `liquidity` is large relative to `feeAmount`, the truncation is a few wei per swap and LPs absorb it silently. When `liquidity` is tiny, more of the fee can be lost to rounding — one reason why very shallow pools are a bad deal for LPs.
- **Per-tick storage.** Every initialized tick needs a `feeGrowthOutside` slot per token. Initializing a tick (by opening a position at a previously unused price) is therefore noticeably more expensive than subsequent uses of that tick.
- **Crossing complexity.** The tick-crossing logic in `Pool.swap` has to flip `feeGrowthOutside` for every tick the price passes through. This is O(ticks crossed), not O(LPs), and in practice bounded by the tick spacing — but it is the one place where swap gas is not strictly constant.
