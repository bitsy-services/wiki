---
title: Fee Box
weight: 83
---

The Fee Box is a [smart contract](/wiki/defi/smart-contract) in the [CBSO](/wiki/defi/cash-backed-synthetic-option) system that acts as the central collection point for [collateralization fees](/wiki/defi/collateralization-fee). After all options for a given expiry are settled, the Option Settler transfers accumulated fees to the Fee Box, where they are held until distributed to protocol stakeholders.

## Role in the CBSO System

During the lifetime of a CBSO, [collateralization fees](/wiki/defi/collateralization-fee) are held within the individual option contracts. The fees do not move until settlement is complete. Once the Option Settler has processed all options for an expiry, it calls `collectFees()` on the Fee Box, transferring the total accumulated fees in a single operation.

This post-settlement transfer ensures that fee accounting never interferes with the collateral that backs live options.

## Interface

| Function | Description |
|----------|-------------|
| `collectFees(amount)` | Called by the Option Settler to deposit accumulated fees after settlement |
| `distributeFees(recipient, amount)` | Sends fees to a designated address -- treasury, [DAO](/wiki/defi/dao), staking rewards, etc. |
| `getBalance()` | Returns the current fee balance held in the contract |
| `authorizeDistributor(address)` | Grants an address permission to call `distributeFees` |
| `revokeDistributor(address)` | Removes distribution permission from an address |

## Access Control

Only authorized distributors can call `distributeFees`. The `authorizeDistributor` and `revokeDistributor` functions manage this allowlist. This means that even if the Fee Box accumulates a large balance, no unauthorized party can withdraw funds.

In practice, the authorized distributor is typically a governance contract (a [DAO](/wiki/defi/dao)) or a predefined payout schedule encoded in another smart contract.

## Distribution Patterns

The Fee Box is deliberately simple -- it collects and holds fees, then distributes them on instruction. The *policy* for how fees are distributed lives outside the Fee Box itself, which keeps the contract focused and auditable. Common distribution patterns include:

- **Treasury funding.** Fees route to a protocol treasury contract for operational expenses or development.
- **Staking rewards.** Fees distribute to token holders who have [staked](/wiki/defi/staking) governance tokens, aligning protocol revenue with governance participation.
- **Automated payouts.** A [decentralized keeper](/wiki/defi/decentralized-keeper) triggers periodic distribution calls on a schedule, removing the need for manual intervention.

## Design Rationale

Separating fee collection into its own contract -- rather than distributing fees inline during settlement -- provides two benefits:

1. **Gas efficiency.** Settlement is already a gas-intensive operation (iterating through options, calculating payouts, transferring collateral). Deferring fee distribution avoids compounding that cost.
2. **Flexibility.** The fee distribution policy can change over time (via governance) without modifying the settlement contracts. The Fee Box's interface remains stable while the downstream recipients evolve.

For the full settlement flow and how the Fee Box fits into the contract architecture, see [CBSO Design](/wiki/defi/cash-backed-synthetic-options-design).
