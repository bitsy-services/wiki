---
title: Bear Put Spread
weight: 73
---

A bear put spread is a [vertical spread](/wiki/defi/options/vertical-spread) that profits when the underlying asset declines. It is constructed by buying a [put option](/wiki/defi/options/put-option) at a higher [strike price](/wiki/defi/options/strike-price) and selling a put at a lower strike, both with the same expiration. The trade costs a net debit -- the premium paid for the higher-strike put exceeds the premium collected from the lower-strike put.

This is a [risk-defined strategy](/wiki/defi/options/risk-defined-strategy) with capped profit and capped loss, suited to traders with a moderately bearish outlook who want to reduce the cost of buying a put outright.

## Setup

| Leg | Action | Strike |
|-----|--------|--------|
| Long put | Buy | Higher (closer to current price) |
| Short put | Sell | Lower (further from current price) |

Both options share the same expiration date and underlying asset.

## Payoff Profile

| Metric | Formula |
|--------|---------|
| **Max profit** | Strike width - net debit |
| **Max loss** | Net debit paid |
| **Breakeven** | Higher strike - net debit |

Maximum profit is reached if the underlying finishes at or below the lower strike at expiration. Maximum loss occurs if the underlying finishes at or above the higher strike (both options expire worthless).

## When to Use

- **Moderately bearish outlook** -- you expect a decline but not a collapse.
- **Cost reduction** -- cheaper than buying a naked put, at the expense of capped profit.
- **Low [implied volatility](/wiki/defi/options/implied-volatility)** -- debit spreads are more attractive when IV is low, since you pay less premium overall.

## Relationship to Other Spreads

The bear put spread is the debit counterpart of the [bear call spread](/wiki/defi/options/bear-call-spread) -- both are bearish [vertical spreads](/wiki/defi/options/vertical-spread), but the bear put is entered for a debit while the bear call is entered for a credit.

Its bullish mirror is the [bull put spread](/wiki/defi/options/bull-put-spread) (credit, bullish). The other debit vertical is the [bull call spread](/wiki/defi/options/bull-call-spread) (debit, bullish).

## Key Risks

1. **Time decay works against you** -- as a net debit position, theta erodes the spread's value if the underlying doesn't move.
2. **Capped profit** -- a dramatic drop below the lower strike yields no additional gain.
3. **[Greeks](/wiki/defi/options/option-greeks) exposure** -- the position has negative delta (bearish), negative theta (time decay hurts), and positive vega (benefits from rising [volatility](/wiki/defi/volatility)).

## DeFi Context

Bear put spreads can be constructed on-chain through options protocols like Lyra, Hegic, or Opyn by combining two put positions at different strikes. They can also be approximated using concentrated [liquidity pool](/wiki/defi/liquidity-pool) positions on [AMMs](/wiki/defi/amm) -- see [emulating option strategies](/wiki/defi/options/emulating-option-strategies) for details. The tokenized equivalent of a bearish spread is the [bear bet](/wiki/defi/options/bear-bet).
