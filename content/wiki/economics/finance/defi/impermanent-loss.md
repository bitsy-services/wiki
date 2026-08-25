---
title: "Impermanent Loss"
weight: 20
---

Impermanent loss (IL) is the difference in value between holding tokens in a [liquidity pool](/wiki/economics/finance/defi/liquidity-pool) and simply holding them in a wallet. It is the cost a liquidity provider (LP) pays for the pool's automatic rebalancing, and on a volatile pair it can exceed everything the position earns in fees over the same period.

## Intuition

An [automated market maker](/wiki/economics/finance/defi/amm) (AMM) pool always sells the token that is going up and buys the token that is going down. This is the mechanism that keeps the pool's price in line with the market. The side effect is that an LP ends up with less of the appreciating token and more of the depreciating one — the opposite of what a holder would have.

If prices revert, the loss disappears — hence "impermanent." Withdrawing while they are still diverged realises it.

## How it works

Consider a constant-product pool (`x · y = k`) that holds two tokens, A and B. An LP deposits equal value of each.

When the market price of A rises relative to B, arbitrageurs buy the now-cheap A from the pool and sell B into it. The pool ends up with less A and more B. The total dollar value of the LP's share grows — but it grows *less* than it would have if the LP had just held the original tokens.

That shortfall is impermanent loss.

## The formula

Let **r** be the price ratio — the new price of token A divided by the original price. IL as a fraction of the held value is:

```text
IL = 1 − 2√r / (r + 1)
```

This only depends on **how much the ratio changed**, not on the direction. A 2× increase and a 2× decrease produce the same IL.

| Price change (r) | IL     |
|-------------------|--------|
| 1.25× (25% up)   | 0.6%   |
| 1.50× (50% up)   | 2.0%   |
| 2× (double)       | 5.7%   |
| 3×                | 13.4%  |
| 4×                | 20.0%  |
| 5×                | 25.5%  |

For small moves IL grows with the square of the log price change, which is why the first 25% of divergence costs 0.6% and the jump from 2× to 4× costs another 14 points.

## Worked example

An LP deposits 1 ETH ($1,000) and 1,000 USDC into a 50/50 pool. Total value: $2,000.

ETH doubles to $2,000.

**If held in wallet:** 1 ETH ($2,000) + 1,000 USDC = **$3,000**.

**If held in pool:** The constant-product formula rebalances the position. After rebalancing, the LP's share is worth approximately $2,828. The difference — about **$172**, or 5.7% of the held value — is the impermanent loss.

The LP has still *made money* in dollar terms ($2,828 vs. the original $2,000). They just made less than they would have by doing nothing. Trading fees earned over the same period may or may not make up the difference.

## What affects the severity

**Price divergence** is the dominant factor. The further the price ratio moves from 1, the larger the IL. Stablecoin pairs (USDC/DAI) have near-zero IL because their ratio barely moves. Volatile pairs (ETH/small-cap token) can see significant IL.

**Pool design** matters too. Constant-product pools (Uniswap V2) spread liquidity across the full price range, diluting IL across a wide band. [Concentrated liquidity](/wiki/economics/finance/defi/uniswap) (Uniswap V3) amplifies both fee income *and* IL within the chosen range — a tighter range means more of both.

**Time** is only relevant because longer exposure means more opportunity for prices to diverge. There is no time-decay component in the formula itself.

## Mitigation strategies

**Pick correlated pairs.** Pools where both tokens move together (e.g. stETH/ETH, USDC/USDT) experience minimal IL because the price ratio stays near 1.

**Earn enough fees.** IL is a cost; trading fees are revenue. A high-volume pool can generate fee income that exceeds the IL. The comparison is always: fee APR (annual percentage rate) vs. expected IL for the pair's volatility.

**Use wider ranges.** In concentrated-liquidity AMMs, a wider price range reduces IL exposure (at the cost of lower fee income per dollar of capital). Concentration multiplies fee income and IL by the same factor, so the choice sets the scale of the position rather than its risk-to-reward ratio.

**Active management.** Rebalancing positions as prices move can reduce IL, but introduces gas costs and complexity. Several protocols ([Arrakis](https://www.arrakis.finance/), [Gamma](https://www.gamma.xyz/)) automate this.

## Further reading

- [Uniswap V2 docs — Understanding Returns](https://docs.uniswap.org/concepts/protocol/integration-issues)
- [Pintail's original analysis](https://pintail.medium.com/uniswap-a-good-deal-for-liquidity-providers-104c0b6816f2) — the blog post that popularised the term
- [Bancor IL research](https://blog.bancor.network/beginners-guide-to-getting-rekt-by-impermanent-loss-7c9510cb2f22)
