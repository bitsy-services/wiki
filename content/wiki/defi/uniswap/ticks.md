---
title: "Ticks"
weight: 5
---

A [Uniswap](../) V3 or V4 pool does not track a continuous price. It tracks an integer called the *current tick*, and the price is a function of that integer. Every position's range boundary, every initialized price point, and every sqrt-price stored on chain is ultimately a tick.

Ticks exist because [concentrated liquidity](../../virtual-reserves) needs to discretize the price axis. Liquidity providers must choose a range, and the pool must be able to add or remove their liquidity efficiently as the price crosses range boundaries. Doing that with arbitrary-precision real numbers is intractable; doing it on a lattice of integer tick indices is fast and deterministic.

## The Price Formula

Ticks are spaced geometrically, one [basis point](https://en.wikipedia.org/wiki/Basis_point) apart:

```
price(i) = 1.0001^i
```

where `i` is the (signed) tick index. Each step of 1 changes the price by exactly 0.01%, so ticks approximate a log-price axis with 1 bip resolution. The base `1.0001` is chosen precisely to make the spacing one basis point — the smallest unit traders already think in.

The price here is `token1 / token0`: how many units of token1 one unit of token0 is worth. Swapping the token ordering of a pool flips all tick signs.

### Intuition Table

| Tick | Price (token1 / token0) | Notes |
|---|---|---|
| −887272 | ≈ 2.9 × 10⁻³⁹ | minimum (`MIN_TICK`) |
| −46054 | ≈ 0.01 | 100× cheaper |
| −23027 | ≈ 0.1 | 10× cheaper |
| −6932 | ≈ 0.5 | half |
| −100 | 0.99005 | ≈ 1% below |
| −10 | 0.99900 | 10 bips below |
| −1 | 0.99990 | 1 bip below |
| 0 | 1.00000 | reference |
| 1 | 1.00010 | 1 bip above |
| 10 | 1.00100 | 10 bips above |
| 100 | 1.01005 | ≈ 1% above |
| 1000 | 1.10517 | ≈ 10.5% above |
| 6932 | ≈ 2 | double |
| 23027 | ≈ 10 | 10× |
| 46054 | ≈ 100 | 100× |
| 69081 | ≈ 1000 | 1000× |
| 887272 | ≈ 3.4 × 10³⁸ | maximum (`MAX_TICK`) |

Two anchors worth internalizing: **a tick is a basis point**, and **doubling the price takes ≈ 6932 ticks**. Almost every tick-level calculation you run into falls out of those two facts.

## sqrtPriceX96

The pool never stores `price` directly. It stores `sqrt(price)` as a [Q64.96 fixed-point](https://en.wikipedia.org/wiki/Q_(number_format)) number called `sqrtPriceX96`:

```
sqrtPriceX96 = floor(sqrt(price) * 2^96)
```

Sqrt-price is used because the concentrated-liquidity invariant `(x + x_off) * (y + y_off) = L²` factors cleanly into sqrt terms (see [virtual reserves](../../virtual-reserves)). Swap math reduces to additions and multiplications of `sqrtPrice` and `L` with no square roots at runtime.

Conversion between the two representations lives in Uniswap's [`TickMath` library](https://github.com/Uniswap/v3-core/blob/main/contracts/libraries/TickMath.sol):

```solidity
// tick → sqrtPriceX96
uint160 sqrtPriceX96 = TickMath.getSqrtRatioAtTick(tick);

// sqrtPriceX96 → tick (floor)
int24 tick = TickMath.getTickAtSqrtRatio(sqrtPriceX96);
```

`getSqrtRatioAtTick` is a fully unrolled bit-by-bit multiplication that avoids transcendental functions on chain. `getTickAtSqrtRatio` is its approximate inverse; it returns the largest tick whose price is ≤ the given `sqrtPriceX96`, which is the tick index the pool itself would report.

## Tick Spacing

Not every tick is usable as a position boundary. Each pool has a *tick spacing* `s`, and positions must be aligned to multiples of `s`. The canonical V3 fee tiers ship with fixed spacings:

| Fee tier | Tick spacing | Smallest range increment |
|---|---|---|
| 0.01% (1 bip) | 1 | 0.01% |
| 0.05% | 10 | 0.10% |
| 0.30% | 60 | ≈ 0.60% |
| 1.00% | 200 | ≈ 2.02% |

Wider spacing is a gas-vs-granularity trade-off. Every initialized tick costs a `SSTORE` and — crucially — the pool has to stop and update bookkeeping every time a swap crosses one. Pairs whose price moves smoothly (ETH/stablecoin) can afford dense ticks because most swaps don't cross many of them. Volatile or exotic pairs benefit from sparser ticks to keep swap gas bounded.

In V4 the pool creator chooses `tickSpacing` at initialization; it is no longer bolted to the fee tier. Hooks can effectively behave like custom fee tiers, so the protocol exposes the underlying parameter.

## Initialized vs. Uninitialized Ticks

A tick that no position uses as a boundary has no storage slot. The first position to use a tick *initializes* it — paying for a `feeGrowthOutside` slot per token and setting a bit in the pool's tick bitmap so future swaps know to look at it.

- Opening a position on a previously unused tick is more expensive than reusing a popular one.
- Swaps skip over uninitialized ticks for free; the tick bitmap lets the swap loop jump straight to the next initialized boundary.
- When the last position referencing a tick is closed, the pool clears that tick's storage and clears the bitmap bit, reclaiming gas.

This is why [fee distribution](fee-distribution) piggybacks on ticks: the per-tick `feeGrowthOutside` slot is already there for range tracking, so adding one accumulator per token is essentially free.

## Tick Bounds

The min and max ticks, ±887272, are not arbitrary. They are the largest tick indices for which `sqrt(1.0001^i)` still fits in a `uint160`. In price terms that is roughly the range `[2⁻¹²⁸, 2¹²⁸]` — enough headroom for any realistic token pair, even wildly mispriced launch tokens or tokens denominated in different decimals.

A position cannot extend past those bounds, and no swap can push `sqrtPriceX96` outside them. If a pair's market price would imply a tick beyond ±887272, the pool is mis-parameterized — usually the fix is to deploy it with reversed token ordering, or with one side scaled to a sensible unit via a wrapper.

## External Links

- [Uniswap V3 whitepaper](https://uniswap.org/whitepaper-v3.pdf) — Section 6 covers tick indexing and sqrt-price representation
- [Uniswap docs — Ticks](https://docs.uniswap.org/sdk/v3/guides/usage)
- [`TickMath.sol`](https://github.com/Uniswap/v3-core/blob/main/contracts/libraries/TickMath.sol) — canonical tick ↔ sqrtPriceX96 conversions
- [`TickBitmap.sol`](https://github.com/Uniswap/v3-core/blob/main/contracts/libraries/TickBitmap.sol) — how the pool finds the next initialized tick in O(1)
