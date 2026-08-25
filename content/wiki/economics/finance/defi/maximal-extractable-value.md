---
title: "Maximal Extractable Value (MEV)"
weight: 35
---

Maximal Extractable Value (MEV) is the profit that can be captured by reordering, inserting, or censoring transactions within a block. It exists because the order in which transactions execute affects their outcomes — and the entity assembling a block gets to choose that order.

It is charged against every [DEX](/wiki/economics/finance/defi/dex) trade, every lending-protocol liquidation, and every on-chain auction, and it surfaces downstream as reverted transactions, gas spikes, and protocol designs built specifically to deny it.

## Why transaction ordering creates value

On an [AMM](/wiki/economics/finance/defi/amm) like [Uniswap](/wiki/economics/finance/defi/uniswap), a large swap moves the price. Anyone who can insert a transaction *before* that swap — buying the token cheap — and another *after* — selling it at the new, higher price — captures risk-free profit. The original trader gets worse execution. This is a **sandwich attack**.

More broadly, any time the outcome of a transaction depends on blockchain state that can be influenced by transaction ordering, MEV exists.

## Common MEV strategies

### Arbitrage

When the price of a token differs between two DEXs, a searcher submits a transaction that buys on the cheap venue and sells on the expensive one in a single atomic transaction. This is the form of MEV with no counterparty to lose by it: the profit is the gap between two venues, and taking it is what closes the gap.

### Sandwich attacks

A searcher spots a pending swap in the mempool, front-runs it (buying the token first to push the price up), lets the victim's trade execute at the worse price, then back-runs it (selling into the higher price). The victim's slippage tolerance determines how much value can be extracted.

### Liquidations

Lending protocols like Aave and Compound allow anyone to liquidate undercollateralised positions for a bonus. Searchers race to be first to trigger these liquidations, often paying high gas to win the race.

### Just-in-time (JIT) liquidity

A searcher adds concentrated [liquidity](/wiki/economics/finance/defi/liquidity-pool) to a pool in the block just before a large swap and removes it immediately after, capturing a disproportionate share of fees without taking on price risk.

## The MEV supply chain

On [Ethereum](/wiki/economics/finance/defi/ethereum/) post-Merge, MEV extraction is split into specialised roles:

1. **Searchers** — find MEV opportunities and construct transaction bundles.
2. **Builders** — assemble full blocks from searcher bundles and regular transactions, optimising for total MEV.
3. **Relays** — act as trusted intermediaries that pass blocks from builders to validators without revealing the block contents (preventing validators from stealing MEV).
4. **Validators** — select the most profitable block from the relay and propose it to the network.

This is the **proposer-builder separation (PBS)** model, implemented off-protocol by [MEV-Boost](https://boost.flashbots.net/).

## Impact on users

- **Worse execution** — sandwich attacks widen the effective spread on DEX trades.
- **Failed transactions** — when multiple searchers target the same opportunity, the losers' transactions revert but still consume gas.
- **Gas spikes** — priority gas auctions (PGAs) between competing searchers drive up base fees for everyone.
- **Centralisation pressure** — economies of scale in block building favour a small number of sophisticated builders.

## Defences and mitigations

| Approach | How it helps |
|----------|-------------|
| **Private mempools** (Flashbots Protect, MEV Blocker) | Transactions skip the public mempool, preventing front-running by searchers who scan it. |
| **Batch auctions** (CoW Protocol) | Trades are batched and settled at a uniform clearing price, eliminating ordering-based extraction. |
| **Intent-based systems** | Users express desired outcomes; solvers compete to fill them, returning MEV to users as better prices. |
| **Encrypted mempools / threshold encryption** | Transaction contents are hidden until ordering is finalised. Still largely experimental. |
| **Tight slippage settings** | Reduces how much a sandwich can extract, at the cost of more reverted transactions. |

## External links

- [Ethereum.org MEV overview](https://ethereum.org/en/developers/docs/mev/) — official documentation
- [Flashbots documentation](https://docs.flashbots.net/) — the primary MEV research and infrastructure project
- [Flash Boys 2.0](https://arxiv.org/abs/1904.05234) — the seminal academic paper that formalised MEV (originally called "miner extractable value")
- [MEV-Boost architecture](https://boost.flashbots.net/) — how proposer-builder separation works in practice
- [libMEV dashboard](https://libmev.com/) — live MEV data and analytics
