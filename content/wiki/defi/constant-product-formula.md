---
title: "Constant Product Formula"
weight: 16
---

The constant product formula is the pricing rule at the heart of most [AMM](/wiki/defi/amm)-based [decentralized exchanges](/wiki/defi/dex). It is elegant in its simplicity: a [liquidity pool](/wiki/defi/liquidity-pool) holds reserves of two tokens, and their product must remain constant through every trade.

```
x * y = k
```

where `x` and `y` are the reserve quantities and `k` is the invariant. [Uniswap](/wiki/defi/uniswap) V2, SushiSwap, and most early AMMs use this formula. Understanding it is the key to understanding how on-chain trading, slippage, and [impermanent loss](/wiki/defi/impermanent-loss) work.

## Intuition

Imagine a pool with 10 ETH and 25,000 USDC. The product is 250,000. If you want to buy ETH, you add USDC to the pool and remove ETH. But the formula constrains the outcome -- you can never drain all the ETH because as the supply shrinks, the price rises toward infinity along a hyperbolic curve. Conversely, adding a tiny amount of USDC when the pool is deep barely moves the price.

This creates a natural supply-demand curve: scarce assets become expensive, abundant assets become cheap. No order book, no market maker, no off-chain infrastructure -- just arithmetic.

## Swap mechanics

A trader wants to buy Token Y by sending `dx` of Token X to the pool. Before the trade, reserves are `(x, y)` with `x * y = k`. After the trade:

1. New Token X reserve: `x' = x + dx`
2. New Token Y reserve: `y' = k / x' = k / (x + dx)`
3. Tokens out: `dy = y - y' = y - k / (x + dx)`

Simplifying:

```
dy = (y * dx) / (x + dx)
```

This is the **output amount before fees**. In practice, AMMs charge a fee (typically 0.3%) on the input. Uniswap V2 applies the fee by treating the effective input as `dx * (1 - fee)`:

```
dy = (y * dx * 997) / (x * 1000 + dx * 997)
```

The fee stays in the pool, slightly increasing `k` after every trade. This is how LPs earn income.

## Price and marginal price

The **spot price** of Y in terms of X is the ratio of reserves:

```
price_Y = x / y
```

This is also the limit of `dy/dx` as the trade size approaches zero. For any finite trade, the *effective* price is worse than the spot price -- this difference is **slippage**.

## Slippage

Because the curve is convex, larger trades move the price further. The price impact of a trade scales roughly with the trade size relative to the pool reserves.

For a small trade `dx << x`, the output is approximately:

```
dy ≈ (y / x) * dx
```

which is just the spot price times the input -- minimal slippage. But a trade that represents, say, 10% of the Token X reserve will receive noticeably fewer tokens per unit than the spot price implies. In a $100K pool, a $10K trade suffers substantial slippage. In a $100M pool, the same trade barely registers.

This is why **total value locked (TVL)** matters: deeper pools mean less slippage for traders and a better trading experience.

## Worked example

Pool: 10 ETH and 25,000 USDC. `k = 250,000`. Spot price: 2,500 USDC/ETH.

A trader swaps 2,500 USDC for ETH (ignoring fees for clarity):

```
new USDC reserve = 25,000 + 2,500 = 27,500
new ETH reserve  = 250,000 / 27,500 ≈ 9.0909
ETH received     = 10 - 9.0909 ≈ 0.9091
```

The trader paid 2,500 USDC for ~0.91 ETH, an effective price of ~2,750 USDC/ETH -- about 10% worse than the spot price. That is the cost of trading a significant fraction of the pool in a single swap.

After the trade, the new spot price is `27,500 / 9.0909 ≈ 3,025 USDC/ETH`. The price has shifted, creating an arbitrage opportunity for anyone with access to a cheaper ETH source.

## Connection to impermanent loss

The constant product formula forces the pool to rebalance on every trade. When the external price of ETH rises, arbitrageurs buy cheap ETH from the pool until the pool's price matches the market. The pool ends up holding less ETH and more USDC than it started with. An LP who deposited at one price ratio and withdraws at another always ends up worse off than someone who simply held the original tokens. This is [impermanent loss](/wiki/defi/impermanent-loss), and it is a direct consequence of the constant product invariant.

## Limitations

- **Capital inefficiency.** The formula spreads liquidity across all prices from zero to infinity. Most of that liquidity sits at prices far from the current market and is never used. Concentrated liquidity (Uniswap V3) addresses this by letting LPs specify a price range.
- **Slippage on large trades.** Thin pools produce poor execution for sizable swaps. Aggregators like 1inch mitigate this by splitting trades across multiple pools.
- **Not ideal for correlated assets.** Stablecoin-to-stablecoin swaps suffer unnecessary slippage under `x * y = k`. Curve's StableSwap invariant handles this case better by flattening the curve near the 1:1 peg.

## Other invariants for comparison

| Invariant | Formula | Used by | Trade-off |
|---|---|---|---|
| Constant product | `x * y = k` | Uniswap V2, SushiSwap | Simple, universal, capital-inefficient |
| Constant sum | `x + y = k` | Rarely used standalone | Zero slippage but can be fully drained |
| StableSwap | Blend of sum and product | Curve | Low slippage near peg, worse far from peg |
| Weighted product | `x^w1 * y^w2 = k` | Balancer | Asymmetric exposure, multi-asset pools |
| Concentrated liquidity | [Virtual reserves](/wiki/defi/virtual-reserves) in a range | Uniswap V3/V4 | High capital efficiency, active management required |

## External links

- [Uniswap V2 whitepaper](https://uniswap.org/whitepaper.pdf)
- [Uniswap V2 docs -- How Uniswap works](https://docs.uniswap.org/contracts/v2/concepts/protocol-overview/how-uniswap-works)
- [Vitalik Buterin -- On Path Independence (2017)](https://vitalik.eth.limo/general/2017/06/22/marketmakers.html) -- early exploration of AMM bonding curves
