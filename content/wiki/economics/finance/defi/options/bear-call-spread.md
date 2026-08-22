---
title: Bear Call Spread
weight: 72
---

A bear call spread is a [vertical spread](/wiki/economics/finance/defi/options/vertical-spread) that profits when the underlying asset stays flat or declines. It is constructed by selling a [call option](/wiki/economics/finance/defi/options/call-option) at a lower [strike price](/wiki/economics/finance/defi/options/strike-price) and buying a call at a higher strike, both with the same expiration. The trade produces a net credit -- the premium collected from the sold call exceeds the premium paid for the bought call.

This is a [risk-defined strategy](/wiki/economics/finance/defi/options/risk-defined-strategy) with capped profit and capped loss, making it popular for generating income in neutral-to-bearish conditions.

## Setup

| Leg | Action | Strike |
|-----|--------|--------|
| Short call | Sell | Lower (closer to current price) |
| Long call | Buy | Higher (further from current price) |

Both options share the same expiration date and underlying asset.

## Payoff Profile

| Metric | Formula |
|--------|---------|
| **Max profit** | Net credit received |
| **Max loss** | Strike width - net credit |
| **Breakeven** | Lower strike + net credit |

The position reaches maximum profit if the underlying finishes at or below the lower strike at expiration (both options expire worthless, and the trader keeps the full credit). Maximum loss occurs if the underlying finishes at or above the higher strike.

## When to Use

- **Neutral to mildly bearish outlook** -- you expect the underlying to stay below a certain level.
- **Income generation** -- you want to collect premium with defined risk.
- **High [implied volatility](/wiki/economics/finance/defi/options/implied-volatility)** -- selling spreads is more attractive when IV is elevated, since the credit received is larger.

## Relationship to Other Spreads

The bear call spread is the credit counterpart of the [bear put spread](/wiki/economics/finance/defi/options/bear-put-spread) -- both are bearish [vertical spreads](/wiki/economics/finance/defi/options/vertical-spread), but the bear call is entered for a credit while the bear put is entered for a debit.

Its bullish mirror is the [bull call spread](/wiki/economics/finance/defi/options/bull-call-spread) (debit, bullish). The other credit vertical is the [bull put spread](/wiki/economics/finance/defi/options/bull-put-spread) (credit, bullish).

## Key Risks

1. **Capped profit** -- even a large drop in the underlying yields only the initial credit.
2. **Assignment risk** -- the short call can be exercised early, particularly if it goes deep in-the-money or if a dividend is approaching.
3. **[Greeks](/wiki/economics/finance/defi/options/option-greeks) exposure** -- the position has negative delta (bearish), positive theta (benefits from time decay), and negative vega (benefits from falling [volatility](/wiki/economics/finance/defi/volatility)).

## DeFi Context

Bear call spreads can be constructed on-chain through options protocols like Lyra, Hegic, or Opyn by combining two call positions at different strikes. They can also be approximated using concentrated [liquidity pool](/wiki/economics/finance/defi/liquidity-pool) positions on [AMMs](/wiki/economics/finance/defi/amm) -- see [emulating option strategies](/wiki/economics/finance/defi/options/emulating-option-strategies) for details. The tokenized equivalent of a bearish spread is the [bear bet](/wiki/economics/finance/defi/options/bear-bet).
