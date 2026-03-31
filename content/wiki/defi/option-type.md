---
title: Option Type
weight: 49
---

**Option type** is the most basic classification of an options contract: it is either a [call option](/wiki/defi/call-option) or a [put option](/wiki/defi/put-option). Every other property of an option -- [strike price](/wiki/defi/strike-price), expiry, the [Greeks](/wiki/defi/option-greeks) -- builds on top of this distinction.

## Call vs. Put

A **call** gives the holder the right to *buy* the underlying asset at the strike price. A **put** gives the holder the right to *sell* at the strike price. Neither obligates the holder to act -- the option can always expire unused, with the holder's loss limited to the premium paid.

| | Call | Put |
|---|---|---|
| **Right** | Buy at strike | Sell at strike |
| **Bullish / Bearish** | Bullish | Bearish |
| **Max loss (buyer)** | Premium paid | Premium paid |
| **Max profit (buyer)** | Unlimited (theoretically) | Strike minus zero (asset can't go negative) |

## Option Style

Option *type* (call vs. put) is separate from option *style*, which governs **when** the option can be exercised:

- **American** -- exercisable at any time up to and including expiry.
- **European** -- exercisable only at expiry.
- **Exotic** -- any non-standard exercise rule. Includes barrier options (activate or deactivate at a price threshold), Asian options (payoff based on an average price), and [perpetual options](/wiki/defi/perpetual-option) (no expiry at all).

Most DeFi options protocols use European-style settlement because it is simpler to implement in a [smart contract](/wiki/defi/smart-contract) -- there is no need to handle early-exercise logic.

## Options in Strategies

Calls and puts are the building blocks of every options strategy. A few examples:

- **[Vertical spread](/wiki/defi/vertical-spread)** -- buy and sell options of the same type at different strikes to cap both risk and reward.
- **Straddle** -- buy a call and a put at the same strike to profit from large moves in either direction, at the cost of paying two premiums.
- **Protective put** -- hold the underlying asset and buy a put to limit downside.

The [option spread](/wiki/defi/option-spread) page covers multi-leg structures in more detail.
