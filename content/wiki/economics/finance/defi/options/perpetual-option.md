---
title: Perpetual Option
weight: 57
---

A **perpetual option** is an options contract with no expiration date. The holder retains the right to exercise indefinitely, which eliminates the need to roll positions from one expiry to the next. The tradeoff is a recurring **funding payment** that replaces the time-decay (theta) mechanism of standard options.

## How Funding Replaces Theta

In a conventional option, the passage of time erodes the option's value -- this is theta decay, one of the [option Greeks](/wiki/economics/finance/defi/options/option-greeks). The seller captures this decay as compensation for bearing risk. A perpetual option has no expiry, so there is no natural theta. Instead, the protocol charges the option holder a periodic **funding fee**, paid to the seller (or liquidity pool). This fee is analogous to the premium drip that a standard option seller earns through time decay.

Funding rates are typically recalculated at fixed intervals -- for example, every 24 hours. When demand for long exposure is high and the perpetual option trades above its fair value, funding increases to discourage longs and attract shorts. The reverse applies when shorts dominate.

## Power Perpetuals (Squeeth)

Opyn's **Squeeth** (squared ETH) is the most prominent DeFi implementation of a perpetual option. Rather than tracking a standard [call](/wiki/economics/finance/defi/options/call-option) or [put](/wiki/economics/finance/defi/options/put-option) payoff, Squeeth tracks the *square* of ETH's price -- making it a **power perpetual**. Key properties:

- The payoff is ETH² / normalization factor, giving the holder convex upside exposure without a [strike price](/wiki/economics/finance/defi/options/strike-price).
- Because the payoff is always positive (price squared is never negative), there is no liquidation risk for long holders -- only the ongoing funding cost.
- Funding is paid in-kind: the normalization factor increases over time, diluting the long position's claim. This is economically equivalent to a cash funding payment but avoids the need for periodic settlement transactions.
- Short sellers mint Squeeth by depositing ETH collateral and face liquidation risk if their collateral ratio drops too low.

Power perpetuals generalize the concept beyond simple call/put payoffs. The squared payoff approximates the exposure of a constantly-rolling at-the-money straddle, which is useful for hedging [volatility](/wiki/economics/finance/defi/volatility) rather than directional price movement.

## Perpetual Options vs. Perpetual Futures

Both instruments lack an expiry and use funding rates, but they differ in payoff shape:

- A **perpetual future** has a linear payoff -- profit and loss move one-to-one with the underlying price.
- A **perpetual option** has a nonlinear (convex) payoff -- the holder benefits from large moves and is partially protected from small adverse moves, at the cost of higher funding.

This convexity is the same property that distinguishes standard options from forwards. The perpetual wrapper removes the expiry constraint but preserves the asymmetric risk profile.

## Risks

- **Funding cost** -- holding a long perpetual option during low-[volatility](/wiki/economics/finance/defi/volatility) periods can be expensive relative to realized gains. The position bleeds value through funding much as a standard option bleeds through theta.
- **[Implied volatility](/wiki/economics/finance/defi/options/implied-volatility) mispricing** -- funding rates embed an implied volatility estimate. If the market overestimates future volatility, long holders overpay; if it underestimates, short sellers are undercompensated.
- **Smart contract risk** -- perpetual options in DeFi are governed by [smart contracts](/wiki/economics/finance/defi/smart-contract) that manage collateral, funding, and liquidation. Bugs or oracle failures can lead to loss of funds.
- **Liquidity** -- perpetual option markets are still relatively thin compared to perpetual futures. Wide spreads and low depth can make entry and exit costly.
