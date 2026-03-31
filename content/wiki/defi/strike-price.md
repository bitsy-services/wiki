---
title: Strike Price
weight: 52
---

The **strike price** (also called the exercise price) is the fixed price at which an option holder can buy or sell the underlying asset. For a [call option](/wiki/defi/call-option) the strike is the purchase price; for a [put option](/wiki/defi/put-option) the strike is the sale price. It is the single most important parameter when selecting an options contract because it determines moneyness, intrinsic value, and the risk/reward profile of the trade.

## Moneyness

The relationship between the strike price and the current spot price defines an option's *moneyness*:

| | Call | Put |
|---|---|---|
| **In-the-money (ITM)** | Spot > Strike | Spot < Strike |
| **At-the-money (ATM)** | Spot ≈ Strike | Spot ≈ Strike |
| **Out-of-the-money (OTM)** | Spot < Strike | Spot > Strike |

ITM options carry intrinsic value and cost more. OTM options have no intrinsic value -- their premium is entirely time value and [implied volatility](/wiki/defi/implied-volatility).

## Effect on premium

The strike price is a primary driver of an option's premium:

- **Deep ITM** options behave almost like the underlying itself (delta near 1 for calls, -1 for puts) and are expensive.
- **ATM** options have the highest time value and are most sensitive to [volatility](/wiki/defi/volatility) changes (highest vega -- see [option greeks](/wiki/defi/option-greeks)).
- **Deep OTM** options are cheap but unlikely to expire profitably. They are essentially bets on large price moves.

## Choosing a strike

The right strike depends on the trader's outlook and risk tolerance:

- **Directional conviction** -- strong conviction favours ITM or ATM strikes that have higher delta and move more with the underlying.
- **Cost sensitivity** -- limited budgets favour OTM strikes, which are cheaper but require a larger move to profit.
- **[Volatility](/wiki/defi/volatility) environment** -- in high-vol markets, strikes further from spot become more viable because large moves are more probable.
- **Time to expiry** -- longer-dated options give the underlying more time to reach the strike, so traders can choose strikes further away without the same probability penalty.

## Strike selection in DeFi

On-chain options protocols like Lyra, Hegic, and Opyn typically offer a predefined set of strikes rather than the continuous range available on traditional exchanges. The available strikes are often centred around the current spot price and spaced at regular intervals. Some protocols dynamically adjust available strikes as the spot price moves.

Because [smart contracts](/wiki/defi/smart-contract) on [Ethereum](/wiki/defi/ethereum/) settle automatically, the strike price also determines the exact payout at expiry -- no manual exercise is required. If a call with a $2,000 strike expires when ETH is at $2,300, the contract pays out $300 per unit automatically.

## Spreads and strike selection

Many options strategies involve multiple strikes:

- **Bull call spread** -- buy a call at a lower strike, sell a call at a higher strike. The distance between the two strikes defines the maximum profit.
- **Bear put spread** -- buy a put at a higher strike, sell a put at a lower strike.
- **Straddle** -- buy a call and a put at the *same* strike, betting on a large move in either direction.
- **Strangle** -- buy a call and a put at *different* strikes (both OTM), a cheaper alternative to the straddle that requires an even larger move to profit.

The width between strikes in a spread controls the trade-off between maximum profit and premium cost.
