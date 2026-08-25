---
title: Option Spread
weight: 55
---

An **option spread** is a strategy that combines buying and selling multiple options on the same underlying asset, with different [strike prices](/wiki/economics/finance/defi/options/strike-price), expiration dates, or both. By pairing a long option with a short option, the trader caps both risk and reward -- the short leg offsets part of the long leg's cost, while the long leg limits the short leg's downside.

Naked options expose the seller to unlimited, or near-unlimited, loss. A spread bounds that loss to a number known at entry, which is what makes the position collateralizable at all — a protocol can escrow the maximum loss instead of demanding a margin buffer against an open-ended one.

## Debit spreads vs. credit spreads

Every spread falls into one of two categories based on cash flow at entry:

- **Debit spread** -- the trader pays a net premium. The purchased option costs more than the sold option. Profit comes from a favorable move in the underlying.
- **Credit spread** -- the trader receives a net premium. The sold option is worth more than the purchased option. Profit comes from time decay or the underlying staying in a favorable range.

The distinction matters for collateral: a debit spread's maximum loss is the premium paid, while a credit spread's maximum loss is the width of the strikes minus the premium received.

## Spread taxonomy

Spreads are classified by which variables differ between the legs:

| Type | Same expiration? | Same strike? | Example |
|------|-----------------|-------------|---------|
| [Vertical spread](/wiki/economics/finance/defi/options/vertical-spread) | Yes | No | Bull call spread |
| Calendar (horizontal) spread | No | Yes | Long 90-day / short 30-day call |
| Diagonal spread | No | No | Long 90-day lower-strike / short 30-day higher-strike call |

### Vertical spreads

The most common category. Two options of the same type ([calls](/wiki/economics/finance/defi/options/call-option) or [puts](/wiki/economics/finance/defi/options/put-option)) with the same expiration but different strikes. These express a directional view with bounded risk. See the dedicated [vertical spread](/wiki/economics/finance/defi/options/vertical-spread) page for payoff profiles and examples.

### Calendar spreads

Same strike, different expirations. The trader is primarily betting on [implied volatility](/wiki/economics/finance/defi/options/implied-volatility) changes or exploiting the faster time decay of the near-term option. Maximum profit occurs when the underlying is at the shared strike at the short option's expiration.

### Diagonal spreads

Different strikes *and* different expirations -- a hybrid of vertical and calendar spreads. These offer more degrees of freedom but are harder to reason about. The trader is typically combining a directional view with a volatility view.

## Multi-leg spreads

Some strategies combine two vertical spreads into a single position:

- **Iron condor** -- a bull put spread and a bear call spread. Four legs, all same expiration. Profits when the underlying stays within a range. Maximum loss is the wider of the two spreads' widths minus the total premium received.
- **Iron butterfly** -- similar to an iron condor but the short put and short call share the same strike. Higher premium collected, narrower profit zone.
- **Butterfly spread** -- three strikes, same option type. Buy the wings, sell the body (or vice versa). Profits from low [volatility](/wiki/economics/finance/defi/volatility) when the underlying expires near the middle strike.

## Spreads in DeFi

On-chain options protocols like Lyra, Dopex, and Premia support spread construction, though with important differences from traditional markets:

- **Collateral efficiency** -- some protocols recognize that a spread's max loss is bounded and reduce the collateral requirement accordingly. Others require full collateral on each leg independently, making spreads capital-inefficient.
- **Settlement** -- DeFi options typically settle in the underlying or a stablecoin, with [smart contracts](/wiki/economics/finance/defi/smart-contract) handling exercise automatically at expiration.
- **Liquidity** -- constructing a multi-leg spread requires liquidity at each strike. On-chain options markets are thinner than their TradFi counterparts, so slippage on each leg can erode the spread's expected payoff.

## Choosing a spread

The right spread depends on the market view:

| Market outlook | Spread type | Net cash flow |
|---------------|-------------|---------------|
| Moderately bullish | Bull call spread (vertical) | Debit |
| Moderately bullish | Bull put spread (vertical) | Credit |
| Moderately bearish | Bear put spread (vertical) | Debit |
| Moderately bearish | Bear call spread (vertical) | Credit |
| Neutral / range-bound | Iron condor, butterfly | Credit |
| Volatility expansion | Calendar spread (long) | Debit |

The [option Greeks](/wiki/economics/finance/defi/options/option-greeks) -- particularly delta, theta, and vega -- determine how a spread's value changes as the underlying moves, time passes, and implied volatility shifts. A spread's net greek is the long leg's minus the short leg's, so a spread decays more slowly and reacts to volatility less than the long option would on its own.
