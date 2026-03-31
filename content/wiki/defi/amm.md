---
title: "Automated Market Maker"
weight: 10
---

An automated market maker (AMM) is a type of [decentralized exchange](/wiki/defi/dex) that uses a mathematical formula -- rather than an order book -- to price trades. Traders swap against a [liquidity pool](/wiki/defi/liquidity-pool) instead of matching with a counterparty.

Traditional exchanges work by matching buyers and sellers: someone posts a bid, someone posts an ask, and the exchange matches them. This requires active market makers who continuously quote prices and enough participants on both sides to maintain a liquid book. On a blockchain, where every operation costs gas and blocks are seconds apart, maintaining an on-chain order book is expensive and slow. AMMs side-step the problem entirely. A smart contract holds reserves of two tokens, and a pricing function determines the exchange rate based on the ratio of those reserves. Anyone can trade at any time, and anyone can supply liquidity.

## Pricing models

The pricing formula is what defines an AMM's behavior -- how it sets prices, how much slippage traders face, and how capital-efficient it is.

### Constant product (x * y = k)

The simplest and most widely deployed model. Two token reserves, x and y, are constrained so their product never changes. When a trader buys token Y by depositing token X, x increases and y decreases, but x * y stays at k. This means the price rises as supply shrinks -- a natural supply-demand curve. See [constant product formula](/wiki/defi/constant-product-formula) for a detailed walkthrough.

[Uniswap](/wiki/defi/uniswap) V2 and SushiSwap use this model. It is simple, robust, and works for any token pair, but it spreads liquidity across the entire price range from zero to infinity, which is capital-inefficient.

### Constant sum (x + y = k)

The reserves sum to a constant, giving zero slippage at any trade size. Sounds ideal, but it means the pool can be fully drained of one asset. In practice this is only useful in narrow cases like stablecoin pairs where the price is tightly pegged.

### Constant mean (weighted pools)

Balancer generalizes the constant product to multiple tokens with arbitrary weightings. Instead of a 50/50 two-token pool, you can have an 80/20 ETH/USDC pool or a pool with five tokens. The invariant becomes the weighted geometric mean of all reserve balances.

### Concentrated liquidity

[Uniswap](/wiki/defi/uniswap) V3 introduced concentrated liquidity, where LPs choose a price range in which their capital is active. Within that range the pool behaves like a much deeper constant-product pool. Outside it, the LP's position is inactive. This dramatically improves capital efficiency but requires LPs to actively manage their positions. Uniswap V4 extends this with hooks that allow custom logic on every swap.

### StableSwap (Curve)

Curve's StableSwap invariant blends a constant-sum and constant-product curve, producing very low slippage near the peg and increasing slippage as the price diverges. It is optimized for assets that should trade near 1:1 (stablecoins, liquid staking tokens).

## How a swap works

A constant-product AMM illustrates the basic mechanics:

1. The pool holds reserves of Token A and Token B. The invariant is `a * b = k`.
2. A trader sends `da` of Token A to the pool. The new Token A reserve becomes `a + da`.
3. The contract computes the new Token B reserve: `b' = k / (a + da)`.
4. The trader receives `b - b'` of Token B (minus a fee, typically 0.3%).
5. The fee is added to the reserves, slightly increasing k and rewarding LPs.

Because the curve is convex, larger trades push the price further -- this is **slippage**. A $100 swap in a $10M pool barely moves the price; the same swap in a $100K pool moves it substantially.

## Roles in an AMM

**Traders** swap one token for another, paying a fee on each trade.

**Liquidity providers (LPs)** deposit tokens into the pool and receive LP tokens representing their share of the reserves. They earn a pro-rata share of trading fees but bear the risk of [impermanent loss](/wiki/defi/impermanent-loss) -- the divergence in value between holding tokens in the pool versus holding them outright.

**Arbitrageurs** keep AMM prices aligned with the broader market. When the AMM price diverges from the price on other venues, arbitrageurs trade against the pool until the prices converge, pocketing the difference.

## Risks and limitations

- **[Impermanent loss](/wiki/defi/impermanent-loss)** is the dominant risk for LPs. In volatile pairs, IL can exceed fee income, making the position a net loss.
- **Slippage** on large trades is inherent to the bonding curve. Concentrated liquidity and deeper pools reduce it but don't eliminate it.
- **MEV (maximal extractable value)** -- sandwich attacks and front-running target AMM traders. A searcher sees a pending swap, trades ahead of it (pushing the price), and trades behind it (profiting from the movement). Private mempools and intent-based routing (UniswapX) are the main countermeasures.
- **Smart contract risk** -- the pool is only as safe as its code. Major AMMs like Uniswap have been extensively audited and battle-tested, but forks and new designs carry higher risk.

## Notable AMM protocols

| Protocol | Key innovation |
|---|---|
| [Uniswap](/wiki/defi/uniswap) V2 | Popularized constant-product AMM, permissionless pair creation |
| Uniswap V3/V4 | Concentrated liquidity, custom hooks |
| Curve | StableSwap invariant for like-kind assets |
| Balancer | Weighted multi-asset pools |
| SushiSwap | Uniswap V2 fork with token incentives |

## External links

- [Wikipedia -- Automated market maker](https://en.wikipedia.org/wiki/Automated_market_maker)
- [Uniswap V2 -- How it works](https://docs.uniswap.org/contracts/v2/concepts/protocol-overview/how-uniswap-works)
- [Uniswap V3 -- Concentrated liquidity](https://docs.uniswap.org/concepts/protocol/concentrated-liquidity)
- [Curve -- StableSwap whitepaper](https://curve.fi/files/stableswap-paper.pdf)
