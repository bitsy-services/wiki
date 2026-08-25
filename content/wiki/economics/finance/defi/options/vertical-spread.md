---
title: Vertical Spread
weight: 56
---

A **vertical spread** is an [option spread](/wiki/economics/finance/defi/options/option-spread) built from two options of the same type -- both [calls](/wiki/economics/finance/defi/options/call-option) or both [puts](/wiki/economics/finance/defi/options/put-option) -- with the same expiration date but different [strike prices](/wiki/economics/finance/defi/options/strike-price). The name comes from the options chain layout, where strike prices are listed vertically.

Verticals are the simplest multi-leg options strategy. Both maximum profit and maximum loss are known at entry, making them popular with traders who want defined-risk directional exposure.

## The four verticals

There are exactly four vertical spreads, defined by option type and whether the position is net long or net short:

### Bull call spread (debit)

Buy a lower-strike call, sell a higher-strike call.

| Metric | Value |
|--------|-------|
| Max profit | (high strike − low strike) − premium paid |
| Max loss | Premium paid |
| Breakeven | Low strike + premium paid |

The trader pays a net premium (debit) and profits if the underlying rises above the breakeven. Both profit and loss are capped.

### Bear put spread (debit)

Buy a higher-strike put, sell a lower-strike put.

| Metric | Value |
|--------|-------|
| Max profit | (high strike − low strike) − premium paid |
| Max loss | Premium paid |
| Breakeven | High strike − premium paid |

Mirror image of the bull call spread, but on the downside. The trader profits if the underlying falls below the breakeven.

### Bull put spread (credit)

Sell a higher-strike put, buy a lower-strike put.

| Metric | Value |
|--------|-------|
| Max profit | Premium received |
| Max loss | (high strike − low strike) − premium received |
| Breakeven | High strike − premium received |

The trader collects a net premium (credit) and profits as long as the underlying stays above the breakeven. This is the credit-spread counterpart of the bull call spread -- both are bullish, but cash flow timing differs.

### Bear call spread (credit)

Sell a lower-strike call, buy a higher-strike call.

| Metric | Value |
|--------|-------|
| Max profit | Premium received |
| Max loss | (high strike − low strike) − premium received |
| Breakeven | Low strike + premium received |

The bearish counterpart of the bull put spread. The trader profits when the underlying stays below the breakeven.

## Payoff profiles

All four verticals share the same shape: a flat region (max loss), a sloped region (between the strikes), and another flat region (max profit). The difference is which direction is profitable.

For a bull call spread with strikes at $50 and $55, purchased for a $2 premium:

```text
Profit
  +3 |          ___________
     |         /
   0 |--------/
     |       /
  -2 |______/
     +--+--+--+--+--+--+--→ Price at expiry
       45 47 50 52 55 58
```

- Below $50: max loss ($2)
- $50--$55: profit increases linearly
- Above $55: max profit ($3)

## Debit vs. credit: choosing between them

A bull call spread and a bull put spread at the same strikes express the same directional view. The difference is practical:

- **Debit spreads** pay upfront and receive value at expiration. Max loss equals the premium. Better when [implied volatility](/wiki/economics/finance/defi/options/implied-volatility) is low (options are cheap to buy).
- **Credit spreads** collect premium upfront and hope the options expire worthless. Max loss exceeds the premium. Better when implied volatility is high (options are expensive to sell).

In efficient markets, put-call parity ensures the risk/reward of equivalent debit and credit verticals is nearly identical after accounting for interest rates and dividends.

## Strike selection

The width between strikes determines the risk/reward tradeoff:

- **Narrow spreads** (e.g. 1--2 strikes apart) -- lower cost, lower max profit, higher probability of max loss. Essentially leveraged directional bets.
- **Wide spreads** (e.g. 5--10 strikes apart) -- higher cost, higher max profit, lower probability of max profit. Approach the behavior of a single long option as width increases.

The [option Greeks](/wiki/economics/finance/defi/options/option-greeks) help calibrate strike choice. Delta approximates the probability that the short strike expires in-the-money; theta gives the daily time decay working for or against the position.

## Vertical spreads in DeFi

On-chain options protocols support vertical spread construction, but the experience differs from centralized exchanges:

- **Collateral** -- protocols that recognize spreads as a single position can collateralize at max-loss rather than per-leg. This makes verticals capital-efficient. Protocols that don't recognize spreads effectively double the capital requirement.
- **Execution** -- building a spread requires two transactions (or a multicall). On-chain, each leg hits the protocol's [AMM](/wiki/economics/finance/defi/amm) or order book, so slippage on each leg compounds.
- **Settlement** -- [smart contracts](/wiki/economics/finance/defi/smart-contract) handle exercise automatically. European-style settlement (exercised only at expiry) is standard in DeFi, simplifying the spread's payout calculation.
- **[Volatility](/wiki/economics/finance/defi/volatility) surface** -- on-chain vol oracles or the protocol's own pricing model determine the premiums. These can diverge from centralized markets, creating arbitrage opportunities and pricing inefficiencies for spread traders.
