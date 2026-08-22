---
title: Implied Volatility
weight: 53
---

**Implied volatility (IV)** is the market's forecast of how much an asset's price will fluctuate over the life of an option. It is extracted from the option's current market price -- given all the other known inputs (spot price, [strike price](/wiki/economics/finance/defi/options/strike-price), time to expiry, risk-free rate), IV is the [volatility](/wiki/economics/finance/defi/volatility) value that makes the theoretical price match the observed price.

Higher IV means options are more expensive because the market expects larger price swings. Lower IV means options are cheaper.

## IV vs. historical volatility

[Volatility](/wiki/economics/finance/defi/volatility) can be measured in two fundamentally different ways:

| | Historical (realised) volatility | Implied volatility |
|---|---|---|
| **Direction** | Backward-looking | Forward-looking |
| **Source** | Calculated from past price data | Derived from current option prices |
| **Measures** | What *did* happen | What the market *expects* to happen |

When IV is significantly higher than recent historical volatility, options are considered expensive -- the market is pricing in more movement than has actually occurred. When IV is below historical vol, options are relatively cheap.

## How IV is calculated

IV cannot be observed directly. It is the "plug" variable in an options pricing model. The most common model is Black-Scholes, where IV is the value of σ that satisfies:

```text
C = S₀·Φ(d₁) - K·e^(-rT)·Φ(d₂)
```

Since there is no closed-form solution for σ, it is found numerically -- typically via Newton's method or bisection. In practice, traders rarely compute IV by hand; pricing engines and protocols handle it automatically.

## What drives IV

- **Market sentiment** -- fear and uncertainty push traders to buy options for protection, driving IV up. Calm markets let IV drift down.
- **Events** -- protocol upgrades, token unlocks, regulatory announcements, and macro events all create expected price movement that inflates IV before the event and deflates it after (*volatility crush*).
- **Supply and demand for options** -- heavy buying of options increases their price, which mechanically raises IV. Heavy selling compresses it.
- **Time to expiry** -- longer-dated options tend to carry higher IV because more can happen over a longer horizon.

## Volatility surface

IV is not a single number -- it varies by [strike price](/wiki/economics/finance/defi/options/strike-price) and expiration. Plotting IV across strikes and expiries produces the *volatility surface*.

Two commonly observed patterns:

- **Volatility skew** -- [out-of-the-money](/wiki/economics/finance/defi/options/strike-price) (OTM) puts tend to have higher IV than at-the-money (ATM) options, reflecting demand for downside protection. In crypto markets this skew can be pronounced during drawdowns.
- **Volatility smile** -- both deep OTM puts and deep OTM calls have higher IV than ATM options, forming a U-shape. This is common in crypto where large moves in either direction are expected.

## IV and the option greeks

IV interacts directly with the [option greeks](/wiki/economics/finance/defi/options/option-greeks):

- **Vega** measures how much an option's price changes for a 1-percentage-point change in IV. ATM options have the highest vega.
- **Theta** (time decay) is connected to IV because higher IV increases the option's time value, which then decays faster as expiry approaches.

## IV in DeFi

On-chain options protocols must price options without a traditional order book, so they compute IV differently:

- **Lyra** uses a Black-Scholes-based [AMM](/wiki/economics/finance/defi/amm) that adjusts IV dynamically based on the protocol's net exposure. When the pool is net short options, IV rises; when net long, IV falls.
- **Hegic** historically used fixed IV inputs set by governance, though later versions moved toward market-driven pricing.
- **Opyn** (Squeeth) sidesteps per-strike IV entirely by offering a perpetual squared-exposure instrument whose funding rate implicitly reflects volatility.

Because crypto markets are highly volatile relative to traditional assets, IV on tokens like ETH routinely sits at 60--100%+ annualised -- far above typical equity IV levels of 15--30%.

## Practical relevance

- **Buying options when IV is high** is expensive. If IV subsequently contracts (and the underlying doesn't move enough), the position loses money even if direction is correct.
- **Selling options when IV is high** can be profitable if realised volatility ends up lower than what was priced in.
- **Volatility crush** after anticipated events (merges, halvings, Federal Open Market Committee meetings) is a well-known pattern. Traders who buy options before the event and hold through it often lose to the post-event IV collapse.
