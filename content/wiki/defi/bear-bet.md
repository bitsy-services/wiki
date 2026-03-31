---
title: Bear Bet
weight: 70
---

A bear bet is a tokenized, on-chain derivative that packages a [bear put spread](/wiki/defi/bear-put-spread) into a single mintable asset. Rather than manually buying and selling [put options](/wiki/defi/put-option) at different [strike prices](/wiki/defi/strike-price), the bear bet wraps both legs into one [smart contract](/wiki/defi/smart-contract) interaction -- producing a tradeable token that represents the entire position.

Bear bets are a [risk-defined strategy](/wiki/defi/risk-defined-strategy): both the maximum gain and maximum loss are known at the time of purchase.

## Structure

A bear bet is economically equivalent to a [bear put spread](/wiki/defi/bear-put-spread) -- a [vertical spread](/wiki/defi/vertical-spread) constructed from two put options:

| Leg | Action |
|-----|--------|
| Higher-strike put | Buy (synthetic) |
| Lower-strike put | Sell (synthetic) |

The spread between the two strikes defines the maximum payout. The cost to enter (the token's market price) defines the maximum loss.

## Payoff Profile

| Metric | Value |
|--------|-------|
| **Max profit** | Strike width - cost of the bet |
| **Max loss** | Cost of the bet |
| **Breakeven** | Higher strike - cost of the bet |
| **Profitable when** | Underlying falls below the breakeven price |

The buyer profits most when the underlying asset finishes at or below the lower strike at expiration. If the underlying stays above the higher strike, the bet expires worthless and the buyer loses the purchase price.

## Minting and Collateralization

Bear bets are created by *minters* who lock collateral equal to the maximum payout (the strike width) in a smart contract. The minter receives transferable tokens representing the short side of the position. They profit by selling those tokens on the open market for more than the minting cost (collateralization fees plus gas).

Minters can exit early by buying back tokens and *burning* them to reclaim a prorated share of their locked collateral and fees.

## Mirror Strategy

The bullish counterpart is the [bull bet](/wiki/defi/bull-bet), which tokenizes a [bull call spread](/wiki/defi/bull-call-spread).

## DeFi Context

Bear bets illustrate one approach to packaging options strategies as tradeable on-chain tokens on [Ethereum](/wiki/defi/ethereum/) and other [blockchains](/wiki/defi/blockchain). Similar exposure can be constructed manually using options protocols like Lyra, Hegic, or Opyn, or approximated through [liquidity pool](/wiki/defi/liquidity-pool) positions -- see [emulating option strategies](/wiki/defi/emulating-option-strategies) for more on that approach.
