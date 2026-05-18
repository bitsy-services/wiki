---
title: Call Option
weight: 50
---

A **call option** is a contract that gives the holder the right -- but not the obligation -- to buy a specified quantity of an underlying asset at a predetermined [strike price](/wiki/defi/options/strike-price) before a given expiration date. If the asset's market price exceeds the strike at expiry, the holder profits; if not, the option expires worthless and the holder loses only the premium paid.

## Key components

- **Underlying asset** -- the token or asset the option references (e.g. ETH, BTC).
- **[Strike price](/wiki/defi/options/strike-price)** -- the price at which the holder can buy.
- **Premium** -- the upfront cost the buyer pays for the contract. This is the buyer's maximum possible loss.
- **Expiration date** -- the deadline to exercise. After this the contract is void.

## Moneyness

A call option's relationship to the current spot price determines its *moneyness*:

| State | Condition | Intrinsic value |
|---|---|---|
| In-the-money (ITM) | Spot > Strike | Positive |
| At-the-money (ATM) | Spot ≈ Strike | Zero |
| Out-of-the-money (OTM) | Spot < Strike | Zero |

Moneyness affects the premium: ITM options cost more because they already carry intrinsic value.

## Payoff

At expiration the payoff of a long call is:

```
payoff = max(spot - strike, 0) - premium
```

The buyer's downside is capped at the premium. The upside is theoretically unlimited.

## Example

A trader buys an ETH call with a $2,000 strike, expiring in 30 days, for a $100 premium.

- If ETH is at $2,500 at expiry, the option is worth $500 and the net profit is $400.
- If ETH stays below $2,000, the option expires worthless and the loss is $100.

## Common strategies

- **Covered call** -- hold the underlying asset and sell a call against it, collecting premium in exchange for capping upside.
- **Bull call spread** -- buy a call at a lower strike and sell a call at a higher strike, reducing premium outlay but capping maximum profit.
- **Protective call** -- buy a call to hedge a short position against an adverse price rise.

## Comparison with put options

A call gives the right to *buy*; a [put option](/wiki/defi/options/put-option) gives the right to *sell*. Calls profit from rising prices, puts from falling prices. The two are linked through put-call parity -- given the same strike and expiration, mispricing between the two creates an arbitrage opportunity.

## On-chain options

In DeFi, call options are implemented as [smart contracts](/wiki/defi/smart-contract) on networks like [Ethereum](/wiki/defi/ethereum/). Protocols such as Lyra, Hegic, and Opyn let users buy and sell calls without a traditional broker. The contract handles collateral, settlement, and exercise automatically.

Key differences from traditional options markets:

- **Collateral is on-chain** -- sellers lock collateral in the contract, removing counterparty risk.
- **Settlement is automatic** -- ITM options are typically settled at expiry without manual exercise.
- **[Implied volatility](/wiki/defi/options/implied-volatility)** is often computed by the protocol's pricing engine rather than derived from an order book.

## Risks

- **Total premium loss** -- if the option expires OTM, the entire premium is lost.
- **[Time decay](/wiki/defi/options/option-greeks)** -- as expiration approaches, the option's time value erodes (measured by *theta*). This works against the buyer.
- **[Volatility](/wiki/defi/volatility) contraction** -- a drop in [implied volatility](/wiki/defi/options/implied-volatility) reduces the option's price even if the underlying hasn't moved.
- **Smart contract risk** (DeFi-specific) -- bugs or exploits in the options protocol can lead to loss of premium or collateral.
