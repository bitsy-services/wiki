---
title: "Constant Mean Formula"
weight: 17
---

The constant mean formula is the pricing invariant behind Balancer's weighted pools. Where the [constant product formula](/wiki/economics/finance/defi/constant-product-formula) constrains two-asset pools to a 50/50 split, the constant mean formula generalises to **any number of assets** with **arbitrary weight ratios** -- 80/20, 60/20/20, or any combination that sums to 100%.

This makes it possible to build [liquidity pools](/wiki/economics/finance/defi/liquidity-pool) that behave like self-rebalancing index funds: [LPs](/wiki/economics/finance/defi/liquidity-pool) choose the asset mix they want exposure to, and the [AMM](/wiki/economics/finance/defi/amm) maintains those proportions through trading fees rather than manual rebalancing.

## The invariant

For a pool with *n* tokens, the constant mean formula is:

```text
∏ (Rᵢ ^ Wᵢ) = k
```

where:
- `Rᵢ` is the reserve (balance) of token *i*
- `Wᵢ` is the normalised weight of token *i* (all weights sum to 1)
- `k` is a constant that stays fixed through swaps (and grows when fees accrue)

This is the **weighted geometric mean** of the reserves. The constant product formula is the special case where *n* = 2 and both weights are 0.5.

## How weights change LP exposure

In a standard 50/50 [Uniswap](/wiki/economics/finance/defi/uniswap)-style pool, an LP's position rebalances aggressively as prices move -- selling the appreciating token and buying the depreciating one. This is the mechanism behind [impermanent loss](/wiki/economics/finance/defi/impermanent-loss).

Custom weights reduce that rebalancing. In an 80/20 ETH/USDC pool, the pool holds 80% of its value in ETH and only 20% in USDC. When ETH's price rises, the pool sells *less* ETH than a 50/50 pool would, because the target allocation already favours ETH. The result is lower impermanent loss for LPs who are bullish on the high-weight asset.

The trade-off: lower-weight tokens have thinner effective liquidity, so swaps involving them experience more slippage.

| Pool weights | [IL](/wiki/economics/finance/defi/impermanent-loss) at 2× price change | Effective liquidity depth |
|---|---|---|
| 50/50 | 5.7% | Balanced |
| 80/20 | 1.6% | Deep for the 80% token, shallow for the 20% |
| 95/5 | 0.2% | Almost no rebalancing, very thin swap liquidity |

## Spot price

The spot price of token *j* in terms of token *i* in a weighted pool is:

```text
price_j = (Rᵢ / Wᵢ) / (Rⱼ / Wⱼ)
```

This follows from taking the marginal rate of substitution along the invariant surface. The weights act as multipliers on the reserve ratios.

## Multi-asset pools

The constant mean formula naturally supports pools with more than two tokens. A single Balancer pool can hold up to eight tokens, each with its own weight. Traders can swap any pair within the pool directly, without routing through an intermediate token.

A three-asset pool with weights 50/30/20 for ETH, WBTC, and USDC acts like a portfolio that is half ETH, roughly a third WBTC, and a fifth stablecoins. Arbitrageurs keep the internal prices aligned with external markets, and the pool collects fees on every rebalancing trade.

## Balancer's implementation

Balancer is the primary [DEX](/wiki/economics/finance/defi/dex) built on the constant mean formula. Its pool types include:

- **Weighted pools** -- the direct implementation of the invariant described above.
- **Managed pools** -- weighted pools where a controller can change weights over time, enabling use cases like liquidity bootstrapping (gradually shifting weight from a new token to a stablecoin during a token launch).

Balancer V2 routes all swaps through a single Vault contract that holds the tokens for every pool, reducing gas costs and enabling multi-hop swaps within a single transaction.

## Relationship to the constant product formula

The constant product formula (`x * y = k`) is a subset: set *n* = 2 and W₁ = W₂ = 0.5, and the constant mean formula reduces to `√x * √y = k'`, which is equivalent to `x * y = k`. Everything that applies to constant-product pools -- arbitrage dynamics, slippage, fee accumulation -- applies to weighted pools too, just with the added dimension of non-equal weights.

## External links

- [Balancer Weighted Math documentation](https://docs.balancer.fi/reference/math/weighted-math.html)
- [Balancer whitepaper](https://balancer.fi/whitepaper.pdf)
- [Martinelli & Mushegian -- A non-custodial portfolio manager, liquidity provider, and price sensor](https://balancer.fi/whitepaper.pdf)
