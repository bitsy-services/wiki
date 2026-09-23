---
title: "Markets"
weight: 40
bookCollapseSection: true
---

How tokens are priced and traded without an order book or a counterparty, and what it costs to supply the capital that makes that possible. This is the heart of DeFi, and the section reads in that order: the exchange, the formula that prices it, the canonical implementation, then the economics of providing the liquidity.

A [decentralized exchange](/wiki/economics/defi/markets/dex) replaces the order book with an [automated market maker](/wiki/economics/defi/markets/amm) — a [liquidity pool](/wiki/economics/defi/markets/liquidity-pool) priced by an invariant, usually the [constant product formula](/wiki/economics/defi/markets/constant-product-formula) or its weighted cousin, the [constant mean formula](/wiki/economics/defi/markets/constant-mean-formula). [Uniswap](/wiki/economics/defi/markets/uniswap) is the canonical implementation, and its concentrated liquidity rests on [virtual reserves](/wiki/economics/defi/markets/virtual-reserves): a trick for making limited capital behave like a much deeper pool.

Providing that liquidity is not free. [Impermanent loss](/wiki/economics/defi/markets/impermanent-loss) is what the pool costs a provider when the price moves, [volatility](/wiki/economics/defi/markets/volatility) is the input that determines how much, and [maximal extractable value](/wiki/economics/defi/markets/maximal-extractable-value) is what block producers take from the ordering of a trade. [Staking](/wiki/economics/defi/markets/staking) and [yield farming](/wiki/economics/defi/markets/yield-farming) are the two standard ways of being paid to leave capital in place, and [transfer on join/exit vs. mint/burn](/wiki/economics/defi/markets/transfer-on-join-exit-vs-mint-burn) is the accounting choice underneath any of them.

A [prediction market](/wiki/economics/defi/markets/prediction-market) is the same machinery pointed at an event rather than an asset: the price of a contract is the market's probability for an outcome. [Prediction market event time](/wiki/economics/defi/markets/prediction-market-event-time) is the surprisingly awkward question of *when* the event is deemed to have happened.

[Options](/wiki/economics/defi/options) are the derivatives built on top of these markets and have a section of their own; the [oracles](/wiki/economics/defi/oracles) that bring a price on-chain from outside are the section after this one.

## Wiki Pages

{{< section >}}
