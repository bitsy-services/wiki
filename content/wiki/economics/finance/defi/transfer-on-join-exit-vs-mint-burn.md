---
title: Transfer on Join/Exit vs. Mint/Burn
weight: 68
---

When a user deposits assets into a [liquidity pool](/wiki/economics/finance/defi/liquidity-pool) or vault, the protocol needs a way to track their share. Two design patterns dominate: **transfer on join/exit**, which moves pre-existing tokens to represent membership, and **mint/burn**, which creates and destroys share tokens on the fly. The choice between them shapes a protocol's accounting model, composability, and gas profile.

## Transfer on Join/Exit

In this pattern, the pool contract accepts a deposit and records the user's share in internal storage -- a mapping from address to balance. No new tokens are created. When the user withdraws, the contract updates the ledger and transfers the underlying assets back.

### How it works

1. User calls `join()` and transfers assets to the pool contract.
2. The contract increments the user's internal share balance.
3. On `exit()`, the contract decrements the balance and sends assets back proportionally.

### Characteristics

- **Simpler token contract.** No ERC-20 mint/burn logic is needed for the share itself.
- **Lower gas on entry/exit.** A storage write to an internal mapping is cheaper than minting a new [ERC-20](/wiki/economics/finance/defi/ethereum/erc-20) token (which requires updating `totalSupply`, the recipient's balance, and emitting a `Transfer` event).
- **No composability.** Because the share is an internal ledger entry rather than a transferable token, it cannot be used as collateral, traded on a [DEX](/wiki/economics/finance/defi/dex), or plugged into other protocols. The user's position is locked inside the pool.
- **Accounting burden on the pool.** The pool contract must implement its own bookkeeping for share balances, withdrawals, and pro-rata calculations. This duplicates logic that ERC-20 already standardizes.

This pattern appears in simple single-asset [staking](/wiki/economics/finance/defi/staking) contracts and some early yield-farming designs where composability was not a priority.

## Mint/Burn

In this pattern, the pool mints new ERC-20 tokens to the depositor and burns them on withdrawal. The minted token represents a proportional claim on the pool's assets.

### How it works

1. User calls `deposit()` and transfers assets to the pool contract.
2. The contract calculates the user's share and mints that many share tokens to the user's address.
3. On `withdraw()`, the user sends share tokens back. The contract burns them and returns the corresponding underlying assets.

### Characteristics

- **Full ERC-20 composability.** Share tokens can be transferred, traded, staked elsewhere, or used as collateral in lending protocols. This is the foundation of DeFi's composability -- one protocol's output becomes another's input.
- **Standard accounting.** Ownership is tracked by the ERC-20 `balanceOf` mapping and `totalSupply`. No custom bookkeeping is needed.
- **[ERC-4626](/wiki/economics/finance/defi/ethereum/erc-4626) compatibility.** The tokenized-vault standard formalizes this pattern with a uniform interface for deposit, withdraw, and share-price calculation. Protocols that follow ERC-4626 are automatically compatible with any integration that speaks the same interface.
- **Higher gas cost.** Minting and burning involve more storage operations and event emissions than a simple internal ledger update.
- **Additional [smart contract](/wiki/economics/finance/defi/smart-contract) surface.** The mint/burn logic adds code paths that must be audited. Bugs in share-price calculation (e.g., rounding errors, donation attacks on empty vaults) have been a recurring source of exploits.

Most modern [AMMs](/wiki/economics/finance/defi/amm) -- including [Uniswap](/wiki/economics/finance/defi/uniswap) v2/v3 [LP](/wiki/economics/finance/defi/liquidity-pool) tokens and Balancer pool tokens -- use mint/burn. Yield aggregators and lending vaults almost universally follow this pattern.

## Comparison

| Dimension | Transfer on join/exit | Mint/burn |
|-----------|----------------------|-----------|
| Share representation | Internal ledger | ERC-20 token |
| Composability | None | Full |
| Gas cost (deposit) | Lower | Higher |
| Accounting | Custom per-pool | Standardized (ERC-20 / ERC-4626) |
| Transferability | Not transferable | Freely transferable |
| Audit surface | Smaller | Larger |

## When to Use Which

**Mint/burn is the default choice** for any pool or vault that needs to participate in the broader DeFi ecosystem. The gas overhead is modest relative to the composability it enables, and ERC-4626 provides a battle-tested reference implementation.

**Transfer on join/exit** makes sense in narrow cases where the position should explicitly not be transferable -- for example, a staking contract where the protocol wants to prevent liquid staking derivatives, or an internal accounting module within a larger system that already handles its own share tracking.
