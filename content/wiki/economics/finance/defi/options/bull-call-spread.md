---
title: Bull Call Spread
weight: 74
---

A bull call spread is a [vertical spread](/wiki/economics/finance/defi/options/vertical-spread) that profits when the underlying asset rises. It is constructed by buying a [call option](/wiki/economics/finance/defi/options/call-option) at a lower [strike price](/wiki/economics/finance/defi/options/strike-price) and selling a call at a higher strike, both with the same expiration. The trade costs a net debit -- the premium paid for the lower-strike call exceeds the premium collected from the higher-strike call.

This is a [risk-defined strategy](/wiki/economics/finance/defi/options/risk-defined-strategy) with capped profit and capped loss, suited to traders with a moderately bullish outlook who want to reduce the cost of buying a call outright.

## Setup

| Leg | Action | Strike |
|-----|--------|--------|
| Long call | Buy | Lower (closer to current price) |
| Short call | Sell | Higher (further from current price) |

Both options share the same expiration date and underlying asset.

## Payoff Profile

| Metric | Formula |
|--------|---------|
| **Max profit** | Strike width - net debit |
| **Max loss** | Net debit paid |
| **Breakeven** | Lower strike + net debit |

Maximum profit is reached if the underlying finishes at or above the higher strike at expiration. Maximum loss occurs if the underlying finishes at or below the lower strike (both options expire worthless).

## When to Use

- **Moderately bullish outlook** -- you expect a rise but not an explosive move.
- **Cost reduction** -- cheaper than buying a naked call, at the expense of capped profit.
- **Low [implied volatility](/wiki/economics/finance/defi/options/implied-volatility)** -- debit spreads are more attractive when IV is low, since you pay less premium overall.

## Relationship to Other Spreads

The bull call spread is the debit counterpart of the [bull put spread](/wiki/economics/finance/defi/options/bull-put-spread) -- both are bullish [vertical spreads](/wiki/economics/finance/defi/options/vertical-spread), but the bull call is entered for a debit while the bull put is entered for a credit.

Its bearish mirror is the [bear call spread](/wiki/economics/finance/defi/options/bear-call-spread) (credit, bearish). The other debit vertical is the [bear put spread](/wiki/economics/finance/defi/options/bear-put-spread) (debit, bearish).

## Key Risks

1. **Time decay works against you** -- as a net debit position, theta erodes the spread's value if the underlying doesn't move.
2. **Capped profit** -- a rally above the higher strike yields no additional gain.
3. **[Greeks](/wiki/economics/finance/defi/options/option-greeks) exposure** -- the position has positive delta (bullish), negative theta (time decay hurts), and positive vega (benefits from rising [volatility](/wiki/economics/finance/defi/volatility)).

## DeFi Context

Bull call spreads can be constructed on-chain through options protocols like Lyra, Hegic, or Opyn by combining two call positions at different strikes. They can also be approximated using concentrated [liquidity pool](/wiki/economics/finance/defi/liquidity-pool) positions on [AMMs](/wiki/economics/finance/defi/amm) -- see [emulating option strategies](/wiki/economics/finance/defi/options/emulating-option-strategies) for details. The tokenized equivalent of a bullish spread is the [bull bet](/wiki/economics/finance/defi/options/bull-bet).
