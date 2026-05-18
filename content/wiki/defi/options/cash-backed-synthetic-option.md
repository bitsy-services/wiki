---
title: Cash-Backed Synthetic Option
weight: 80
---

A cash-backed synthetic option (CBSO) is a fully collateralized, on-chain derivative that replicates the payoff of a traditional [option spread](/wiki/defi/options/vertical-spread) without requiring an actual underlying asset to change hands. The "cash-backed" part means every position is backed one-to-one by a settlement currency locked in a [smart contract](/wiki/defi/smart-contract) -- there are no margin calls and no liquidation risk. The "synthetic" part means the contract derives its value from an external price feed rather than from custody of the underlying asset.

[Bull bets](/wiki/defi/options/bull-bet) and [bear bets](/wiki/defi/options/bear-bet) are specific implementations of CBSOs, packaging [bull call spreads](/wiki/defi/options/bull-call-spread) and [bear put spreads](/wiki/defi/options/bear-put-spread) respectively into single mintable tokens.

## Why Full Collateralization Matters

Traditional options sellers face potentially unlimited liability (for naked calls) or rely on margin systems that can force liquidation during volatile markets. CBSOs eliminate both problems:

- **No margin calls.** The maximum payout is locked in the contract at mint time. The seller's worst case is losing the entire stake -- which is already deposited.
- **No counterparty credit risk.** Settlement is guaranteed by the collateral held in the smart contract, not by a clearinghouse or broker.
- **Risk-defined by construction.** Every CBSO is a [risk-defined strategy](/wiki/defi/options/risk-defined-strategy) with capped profit and capped loss, structurally identical to a [vertical spread](/wiki/defi/options/vertical-spread).

The tradeoff is capital efficiency: because the full maximum payout must be locked upfront, CBSOs require more collateral than a margin-based system would for the same notional exposure.

## Minting and the Option Lifecycle

### Minting

A *minter* creates CBSOs by depositing settlement currency (such as USDC or ETH) into the CBSO [smart contract](/wiki/defi/smart-contract). The deposited amount equals the maximum payout of the option -- the width between the two [strike prices](/wiki/defi/options/strike-price). In return, the minter receives [ERC-20](/wiki/defi/ethereum/erc-20)-compliant tokens representing the option position.

The minter also pays a [collateralization fee](/wiki/defi/collateralization-fee) proportional to the collateral amount and the time to expiration.

### Trading

Because CBSOs are standard ERC-20 tokens, they can be traded on any [DEX](/wiki/defi/dex) or transferred between wallets. No special infrastructure is needed beyond the token contract itself.

### Buy-Back and Burn

A minter can exit their position early by purchasing CBSO tokens on the open market and *burning* them. Burning returns a prorated share of the locked collateral and a prorated refund of the [collateralization fee](/wiki/defi/collateralization-fee) based on the time remaining until expiration.

### Settlement

At expiration, the smart contract settles each CBSO based on the final asset price reported by a decentralized [oracle](/wiki/defi/oracle-node). The payout is calculated from the relationship between the [strike price](/wiki/defi/options/strike-price) and the settlement price, capped at the locked collateral. Any remaining collateral is returned to the minter.

### Automatic Refund

If a CBSO is never sold before expiration, the minter receives a refund of their staked collateral minus fees. This is a safety valve for low-liquidity scenarios -- in traditional options markets, an unsold position simply expires worthless with no recourse.

## Volatile Settlement Currencies

Traditional options settle in a stable currency like USD. CBSOs can also settle in a volatile [cryptocurrency](/wiki/defi/cryptocurrency) like ETH, which introduces an additional dimension of risk and opportunity. A CBSO settled in ETH exposes both parties not only to the underlying asset's price movement but also to changes in the value of ETH itself.

This *dual volatility* property is not available in traditional options markets and enables hedging strategies that account for settlement-currency risk -- a concern unique to DeFi environments where the base currency is often a volatile asset.

## Relationship to Bull Bets and Bear Bets

[Bull bets](/wiki/defi/options/bull-bet) and [bear bets](/wiki/defi/options/bear-bet) are the primary user-facing CBSO products:

| Product | Underlying strategy | Profits when |
|---------|-------------------|--------------|
| Bull bet | [Bull call spread](/wiki/defi/options/bull-call-spread) | Asset price rises above the breakeven |
| Bear bet | [Bear put spread](/wiki/defi/options/bear-put-spread) | Asset price falls below the breakeven |

By combining bull bets and bear bets at different strikes, traders can construct more complex positions -- iron condors, butterfly spreads, and other multi-leg strategies -- entirely on-chain. See [emulating option strategies](/wiki/defi/options/emulating-option-strategies) for details.

## Technical Design

The smart contract architecture behind CBSOs -- including the Option Factory, Option Settler, Asset Price Oracle, and [Fee Box](/wiki/defi/fee-box) -- is covered in [CBSO Design](/wiki/defi/options/cash-backed-synthetic-options-design).
