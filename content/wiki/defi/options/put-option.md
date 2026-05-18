---
title: Put Option
weight: 51
---

A **put option** is a contract that gives the holder the right -- but not the obligation -- to sell a specified quantity of an underlying asset at a predetermined [strike price](/wiki/defi/options/strike-price) before a given expiration date. Puts profit when the underlying asset's price falls below the strike, making them the primary instrument for bearish bets and downside hedging.

## Key components

- **Underlying asset** -- the token or asset the option references.
- **[Strike price](/wiki/defi/options/strike-price)** -- the price at which the holder can sell.
- **Premium** -- the upfront cost paid by the buyer. This is the buyer's maximum possible loss.
- **Expiration date** -- the deadline to exercise.

## Moneyness

| State | Condition | Intrinsic value |
|---|---|---|
| In-the-money (ITM) | Spot < Strike | Positive |
| At-the-money (ATM) | Spot ≈ Strike | Zero |
| Out-of-the-money (OTM) | Spot > Strike | Zero |

Note that moneyness for puts is the mirror of [call options](/wiki/defi/options/call-option) -- a put is ITM when the spot price is *below* the strike.

## Payoff

At expiration the payoff of a long put is:

```
payoff = max(strike - spot, 0) - premium
```

The buyer's downside is capped at the premium. The maximum profit occurs if the underlying goes to zero, yielding `strike - premium`.

## Example

A trader buys an ETH put with a $2,000 strike, expiring in 30 days, for a $120 premium.

- If ETH drops to $1,500 at expiry, the option is worth $500 and the net profit is $380.
- If ETH stays above $2,000, the option expires worthless and the loss is $120.

## Common strategies

- **Protective put** -- hold the underlying asset and buy a put to insure against a price drop. This is the options equivalent of a stop-loss, but with a guaranteed floor.
- **Bear put spread** -- buy a put at a higher strike and sell a put at a lower strike, reducing premium cost but capping the maximum profit.
- **Long put** -- a straightforward directional bet that the asset's price will decline.

## Comparison with call options

A [call option](/wiki/defi/options/call-option) gives the right to *buy*; a put gives the right to *sell*. The two are connected through put-call parity: for European-style options with the same strike and expiry, the prices of the call and put imply each other given the spot price and risk-free rate.

## On-chain options

DeFi protocols like Lyra, Hegic, and Opyn implement puts as [smart contracts](/wiki/defi/smart-contract) on [Ethereum](/wiki/defi/ethereum/) and other chains. The seller's collateral is locked in the contract, removing counterparty risk. Settlement at expiry is automatic -- if the put is ITM, the holder receives the difference between the strike and the spot price.

Puts are especially popular on-chain as portfolio insurance. Holding ETH plus an ETH put creates a position with limited downside, which is attractive in the high-[volatility](/wiki/defi/volatility) crypto environment.

## Risks

- **Total premium loss** -- if the option expires OTM, the entire premium is lost.
- **[Time decay](/wiki/defi/options/option-greeks)** -- theta erodes the option's time value as expiry approaches, working against the buyer.
- **[Volatility](/wiki/defi/volatility) contraction** -- a drop in [implied volatility](/wiki/defi/options/implied-volatility) reduces the put's price even if the spot hasn't moved upward.
- **Smart contract risk** (DeFi-specific) -- exploits in the protocol can lead to loss of funds.
