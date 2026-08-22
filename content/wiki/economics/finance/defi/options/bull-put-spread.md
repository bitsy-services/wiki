---
title: Bull Put Spread
weight: 75
---

A bull put spread is a [vertical spread](/wiki/economics/finance/defi/options/vertical-spread) that profits when the underlying asset stays flat or rises. It is constructed by selling a [put option](/wiki/economics/finance/defi/options/put-option) at a higher [strike price](/wiki/economics/finance/defi/options/strike-price) and buying a put at a lower strike, both with the same expiration. The trade produces a net credit -- the premium collected from the sold put exceeds the premium paid for the bought put.

This is a [risk-defined strategy](/wiki/economics/finance/defi/options/risk-defined-strategy) with capped profit and capped loss, making it popular for generating income in neutral-to-bullish conditions.

## Setup

| Leg | Action | Strike |
|-----|--------|--------|
| Short put | Sell | Higher (closer to current price) |
| Long put | Buy | Lower (further from current price) |

Both options share the same expiration date and underlying asset.

## Payoff Profile

| Metric | Formula |
|--------|---------|
| **Max profit** | Net credit received |
| **Max loss** | Strike width - net credit |
| **Breakeven** | Higher strike - net credit |

The position reaches maximum profit if the underlying finishes at or above the higher strike at expiration (both options expire worthless, and the trader keeps the full credit). Maximum loss occurs if the underlying finishes at or below the lower strike.

## When to Use

- **Neutral to mildly bullish outlook** -- you expect the underlying to stay above a certain level.
- **Income generation** -- you want to collect premium with defined risk.
- **High [implied volatility](/wiki/economics/finance/defi/options/implied-volatility)** -- selling spreads is more attractive when IV is elevated, since the credit received is larger.

## Relationship to Other Spreads

The bull put spread is the credit counterpart of the [bull call spread](/wiki/economics/finance/defi/options/bull-call-spread) -- both are bullish [vertical spreads](/wiki/economics/finance/defi/options/vertical-spread), but the bull put is entered for a credit while the bull call is entered for a debit.

Its bearish mirror is the [bear put spread](/wiki/economics/finance/defi/options/bear-put-spread) (debit, bearish). The other credit vertical is the [bear call spread](/wiki/economics/finance/defi/options/bear-call-spread) (credit, bearish).

## Key Risks

1. **Capped profit** -- even a large rally in the underlying yields only the initial credit.
2. **Assignment risk** -- the short put can be exercised early, particularly if it goes deep in-the-money.
3. **[Greeks](/wiki/economics/finance/defi/options/option-greeks) exposure** -- the position has positive delta (bullish), positive theta (benefits from time decay), and negative vega (benefits from falling [volatility](/wiki/economics/finance/defi/volatility)).

## DeFi Context

Bull put spreads can be constructed on-chain through options protocols like Lyra, Hegic, or Opyn by combining two put positions at different strikes. They can also be approximated using concentrated [liquidity pool](/wiki/economics/finance/defi/liquidity-pool) positions on [AMMs](/wiki/economics/finance/defi/amm) -- see [emulating option strategies](/wiki/economics/finance/defi/options/emulating-option-strategies) for details. The tokenized equivalent of a bullish spread is the [bull bet](/wiki/economics/finance/defi/options/bull-bet).
