---
title: Option Greeks
weight: 54
---

The **option greeks** are a set of sensitivity measures that describe how an option's price responds to changes in underlying variables -- spot price, time, [volatility](/wiki/economics/finance/defi/volatility), and interest rates. They are the primary tools for understanding and managing risk in options positions.

## Summary

| Greek | Symbol | Measures sensitivity to | Typical range (calls) | Typical range (puts) |
|---|---|---|---|---|
| Delta | Δ | Underlying price | 0 to +1 | -1 to 0 |
| Gamma | Γ | Rate of change of delta | Always positive | Always positive |
| Theta | Θ | Time (passage of days) | Usually negative | Usually negative |
| Vega | ν | [Implied volatility](/wiki/economics/finance/defi/options/implied-volatility) | Always positive | Always positive |
| Rho | ρ | Interest rates | Positive (calls) | Negative (puts) |

## Delta (Δ)

Delta measures how much an option's price changes for a $1 move in the underlying.

- A [call option](/wiki/economics/finance/defi/options/call-option) with delta 0.60 gains $0.60 when the underlying rises $1.
- A [put option](/wiki/economics/finance/defi/options/put-option) with delta -0.40 gains $0.40 when the underlying falls $1.

Delta also approximates the probability that the option expires in-the-money. A 0.30-delta call has roughly a 30% chance of finishing ITM.

ATM options have delta near ±0.50. As an option moves deeper ITM, delta approaches ±1; as it moves further OTM, delta approaches 0.

## Gamma (Γ)

Gamma is the rate of change of delta per $1 move in the underlying. It tells you how *quickly* delta shifts as the spot price moves.

- Gamma is highest for ATM options and near-term expirations.
- Deep ITM and deep OTM options have low gamma because their deltas are already near their extremes.

High gamma means the position's directional exposure changes rapidly, which can be either an opportunity (long gamma benefits from large moves) or a risk (short gamma suffers from large moves).

## Theta (Θ)

Theta measures the daily erosion of an option's value due to the passage of time -- commonly called *time decay*.

- A theta of -0.05 means the option loses $0.05 per day, all else equal.
- Theta accelerates as expiry approaches, especially for ATM options.
- Option *buyers* are hurt by theta; option *sellers* benefit from it.

Theta is the cost of holding optionality. The closer to expiry, the faster it decays, which is why short-dated options are popular with sellers and dangerous for buyers who need the underlying to move quickly.

## Vega (ν)

Vega measures the change in an option's price for a one-percentage-point change in [implied volatility](/wiki/economics/finance/defi/options/implied-volatility).

- A vega of 0.15 means the option gains $0.15 if IV rises by 1%.
- Vega is highest for ATM options and longer-dated expirations.
- Both calls and puts have positive vega -- rising IV benefits all option holders.

In crypto markets, where [volatility](/wiki/economics/finance/defi/volatility) can shift dramatically, vega exposure often dominates other greeks. A position can be delta-neutral but still suffer large losses from an IV contraction.

## Rho (ρ)

Rho measures sensitivity to changes in the risk-free interest rate.

- Call rho is positive -- higher rates increase call values.
- Put rho is negative -- higher rates decrease put values.

Rho matters most for long-dated options. For the short-dated contracts typical in DeFi (often 7--30 days), rho is usually negligible.

## Interaction between greeks

The greeks do not operate in isolation:

- **Delta + Gamma**: gamma tells you how unstable your delta hedge is. High gamma means frequent rebalancing.
- **Vega + Theta**: high-IV options have more time value, so they also have higher theta. Selling expensive (high-IV) options earns more theta but carries more vega risk if IV rises further.
- **Delta + Vega**: a change in IV shifts the probability distribution of outcomes, which changes delta. This second-order effect (*vanna*) matters for large portfolios.

## Practical example

An ETH [call option](/wiki/economics/finance/defi/options/call-option) with a $2,000 [strike](/wiki/economics/finance/defi/options/strike-price), 14 days to expiry, spot at $1,950:

| Greek | Value | Interpretation |
|---|---|---|
| Delta | 0.45 | Gains $0.45 per $1 rise in ETH |
| Gamma | 0.03 | Delta increases by 0.03 per $1 rise |
| Theta | -3.20 | Loses $3.20 per day from time decay |
| Vega | 5.50 | Gains $5.50 per 1% rise in IV |
| Rho | 0.12 | Gains $0.12 per 1% rise in rates |

## Greeks in DeFi

On-chain options protocols like Lyra, Hegic, and Opyn expose greeks either directly in their UIs or through their pricing engines. Lyra's AMM, for example, dynamically adjusts pricing based on the pool's aggregate greek exposure -- when the pool accumulates too much short gamma, it widens spreads to discourage further selling.

Understanding greeks is especially relevant for DeFi liquidity providers. Depositing into an options [liquidity pool](/wiki/economics/finance/defi/liquidity-pool) means implicitly taking the other side of user trades, which creates greek exposures that the pool manages through hedging or pricing adjustments.
