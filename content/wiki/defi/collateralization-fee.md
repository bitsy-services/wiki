---
title: Collateralization Fee
weight: 82
---

A collateralization fee is the cost charged to minters when they create a [cash-backed synthetic option (CBSO)](/wiki/defi/cash-backed-synthetic-option). It is calculated as a percentage of the staked collateral, prorated over the duration of the option, and serves as the primary revenue mechanism for the CBSO protocol.

## How It Works

When a minter deposits collateral into the CBSO [smart contract](/wiki/defi/smart-contract) to mint new option tokens, the contract charges a collateralization fee on top of the collateral amount. The fee is expressed as an annual percentage rate applied to the collateral value, prorated to the option's time to expiration.

For example, with a 1% annual fee and a six-month option, the effective fee is 0.5% of the collateral.

## Prorated Refunds on Buy-Back

If a minter buys back and burns some or all of their CBSO tokens before expiration, the contract refunds a prorated portion of the collateralization fee based on two factors: the fraction of tokens burned and the time remaining.

**Example.** A minter stakes collateral with a 1% annual collateralization fee. Three months before expiration, they buy back and burn 50% of the outstanding tokens:

```
Refund = annual rate * fraction burned * time remaining
       = 1% * 50% * 3/12
       = 0.125% of the original collateral
```

This refund mechanism incentivizes minters to actively manage their positions and return unused capacity to the market.

## Why It Exists

The collateralization fee serves three purposes:

1. **Protocol revenue.** Fees flow to the [Fee Box](/wiki/defi/fee-box) after settlement, funding protocol operations, [DAO](/wiki/defi/dao) treasury, or distribution to stakeholders.
2. **Spam prevention.** Without a cost to mint, actors could flood the system with options they never intend to sell, consuming oracle and settlement resources for free.
3. **Capital-cost alignment.** The fee reflects the time value of locking collateral. A longer-duration option ties up capital for longer and costs proportionally more -- similar to how interest accrues on a margin loan in traditional finance.

## Fee Flow

Collateralization fees are held in the CBSO contract during the option's lifetime. At expiration, when the Option Settler processes settlement, accumulated fees are transferred to the [Fee Box](/wiki/defi/fee-box) for collection and distribution. See the [CBSO Design](/wiki/defi/cash-backed-synthetic-options-design) page for details on how settlement triggers fee transfer.

## Comparison with Traditional Finance

The collateralization fee is analogous to the interest or maintenance fees charged on margin accounts, or MakerDAO's "stability fee" on DAI vaults. The key difference is enforcement: in DeFi, the fee is calculated and collected entirely by the [smart contract](/wiki/defi/smart-contract), with no intermediary involved and no possibility of discretionary waiver.
