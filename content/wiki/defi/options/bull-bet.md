---
title: Bull Bet
weight: 71
---

A bull bet is a tokenized, on-chain derivative that packages a [bull call spread](/wiki/defi/options/bull-call-spread) into a single mintable asset. Instead of separately buying and selling [call options](/wiki/defi/options/call-option) at different [strike prices](/wiki/defi/options/strike-price), the bull bet wraps both legs into one [smart contract](/wiki/defi/smart-contract) interaction -- producing a tradeable token that represents the entire position.

Bull bets are a [risk-defined strategy](/wiki/defi/options/risk-defined-strategy): both the maximum gain and maximum loss are known at the time of purchase.

## Structure

A bull bet is economically equivalent to a [bull call spread](/wiki/defi/options/bull-call-spread) -- a [vertical spread](/wiki/defi/options/vertical-spread) constructed from two call options:

| Leg | Action |
|-----|--------|
| Lower-strike call | Buy (synthetic) |
| Higher-strike call | Sell (synthetic) |

The spread between the two strikes defines the maximum payout. The cost to enter (the token's market price) defines the maximum loss.

## Payoff Profile

| Metric | Value |
|--------|-------|
| **Max profit** | Strike width - cost of the bet |
| **Max loss** | Cost of the bet |
| **Breakeven** | Lower strike + cost of the bet |
| **Profitable when** | Underlying rises above the breakeven price |

The buyer profits most when the underlying asset finishes at or above the higher strike at expiration. If the underlying stays below the lower strike, the bet expires worthless and the buyer loses the purchase price.

## Minting and Collateralization

Bull bets are created by *minters* who lock collateral equal to the maximum payout (the strike width) in a smart contract. The minter receives transferable tokens representing the short side of the position. They profit by selling those tokens on the open market for more than the minting cost (collateralization fees plus gas).

Minters can exit early by buying back tokens and *burning* them to reclaim a prorated share of their locked collateral and fees.

## Mirror Strategy

The bearish counterpart is the [bear bet](/wiki/defi/options/bear-bet), which tokenizes a [bear put spread](/wiki/defi/options/bear-put-spread).

## DeFi Context

Bull bets illustrate one approach to packaging options strategies as tradeable on-chain tokens on [Ethereum](/wiki/defi/ethereum/) and other [blockchains](/wiki/defi/blockchain). Similar exposure can be constructed manually using options protocols like Lyra, Hegic, or Opyn, or approximated through [liquidity pool](/wiki/defi/liquidity-pool) positions -- see [emulating option strategies](/wiki/defi/options/emulating-option-strategies) for more on that approach.
