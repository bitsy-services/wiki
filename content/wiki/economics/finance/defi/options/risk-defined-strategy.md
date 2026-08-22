---
title: Risk-Defined Strategy
weight: 59
---

A risk-defined strategy is any position where the maximum possible loss is known before the trade is entered. The trader accepts a capped upside in exchange for a hard floor on downside. In traditional finance this usually means option spreads; in DeFi it extends to collateralized vault positions, bounded [liquidity-pool](/wiki/economics/finance/defi/liquidity-pool) ranges, and on-chain binary payoffs enforced by [smart contracts](/wiki/economics/finance/defi/smart-contract).

## Why It Matters

Undefined-risk positions -- selling a naked [call](/wiki/economics/finance/defi/options/call-option), providing unbounded liquidity, writing uncollateralized contracts -- can produce losses that exceed the original capital. Risk-defined strategies cap that exposure, which makes them:

- **Easier to size** -- a trader can allocate a fixed dollar amount knowing the worst-case outcome.
- **Margin-efficient** -- protocols can require only the maximum loss as collateral, rather than demanding large buffers against theoretically unlimited loss.
- **Better suited to volatile markets** -- [volatility](/wiki/economics/finance/defi/volatility) increases the chance of extreme moves; a hard loss cap prevents catastrophic drawdowns.

## Common Risk-Defined Structures

### Vertical Spreads

A [vertical spread](/wiki/economics/finance/defi/options/vertical-spread) combines a long and a short option at different [strike prices](/wiki/economics/finance/defi/options/strike-price) with the same expiry. The maximum loss is the net premium paid (for debit spreads) or the width of the strikes minus the premium received (for credit spreads).

| Spread | Outlook | Max loss |
|---|---|---|
| Bull call spread | Moderately bullish | Net debit paid |
| Bear put spread | Moderately bearish | Net debit paid |
| Bull put spread (credit) | Neutral to bullish | Strike width minus credit received |
| Bear call spread (credit) | Neutral to bearish | Strike width minus credit received |

### Iron Condor

An iron condor sells an out-of-the-money [call](/wiki/economics/finance/defi/options/call-option) spread and an out-of-the-money [put](/wiki/economics/finance/defi/options/put-option) spread simultaneously. Maximum loss is the wider of the two wing widths minus the total credit received. It profits when the underlying stays within a range -- a bet on low [volatility](/wiki/economics/finance/defi/volatility).

### Collateralized On-Chain Positions

DeFi protocols often enforce risk definition at the contract level:

- **Fully collateralized [option spreads](/wiki/economics/finance/defi/options/option-spread)** -- protocols that tokenize options can lock the maximum loss as collateral in a [smart contract](/wiki/economics/finance/defi/smart-contract) at the time the position is opened. Neither party can lose more than the locked amount.
- **Bounded LP ranges** -- a concentrated [liquidity-pool](/wiki/economics/finance/defi/liquidity-pool) position in a Uniswap v3-style AMM has a defined worst case: full conversion from one asset to the other across the range, plus [impermanent loss](/wiki/economics/finance/defi/impermanent-loss). The loss is bounded by the value of the deposited capital.
- **Vault strategies** -- structured vaults that sell covered calls or cash-secured puts enforce the strategy's parameters on-chain, guaranteeing that the position cannot exceed its defined risk.

## How DeFi Enforces Risk Boundaries

In traditional markets, risk definition depends on the broker holding sufficient margin and the clearinghouse guaranteeing settlement. In DeFi, the [smart contract](/wiki/economics/finance/defi/smart-contract) itself is the enforcement mechanism:

1. **Collateral lockup** -- the contract escrows the maximum possible payout at position creation. There is no margin call and no counterparty credit risk.
2. **Atomic settlement** -- when the position resolves, the contract distributes collateral according to the outcome in a single transaction. No manual exercise or assignment is needed.
3. **Transparency** -- anyone can inspect the contract's collateral balance and verify that every open position is fully backed.

This model eliminates the counterparty and settlement risks present in traditional options but introduces [smart-contract](/wiki/economics/finance/defi/smart-contract) risk -- a bug in the contract can circumvent the intended risk boundaries entirely.

## Trade-Offs

**Capped profit** -- the defining cost of risk definition. A [vertical spread](/wiki/economics/finance/defi/options/vertical-spread) will never capture the full move of the underlying the way a naked long option can.

**Capital efficiency** -- locking the full maximum loss as collateral is safe but capital-intensive. Protocols that allow partial collateralization (with liquidation mechanisms) can improve capital efficiency but reintroduce liquidation risk.

**Complexity** -- multi-leg strategies require more transactions to enter and exit, increasing gas costs and execution risk on-chain.

**Time decay** -- for option-based strategies, the position's value erodes as expiry approaches. If the expected move does not materialize in time, the entire debit can be lost -- which, by design, is the defined maximum loss.
