---
title: "Smart Contract"
weight: 3
---

A smart contract is a program deployed to a blockchain that executes automatically when its functions are called. Once deployed, the code is immutable (unless the contract uses an upgradeable proxy pattern) and its execution is deterministic — given the same state and inputs, every node on the network will produce the same result.

Every [DEX](/wiki/economics/finance/defi/dex), lending protocol, [liquidity pool](/wiki/economics/finance/defi/liquidity-pool), and token in DeFi is a smart contract, or a set of contracts calling each other.

## What they replace

A traditional agreement is backed by a counterparty's willingness to perform, or by a third party that can compel performance — a court, an escrow agent, a clearinghouse. A smart contract substitutes published code: the terms are readable before anyone commits to them, they execute exactly as written, and the network's consensus mechanism is what enforces them.

Protocols built this way are:

- **Permissionless** — anyone can interact with them, no account application required.
- **Composable** — one contract can call another, enabling complex systems to be built from simple primitives.
- **Transparent** — the source code and all state transitions are publicly auditable.

## How they work

1. A developer writes the contract in a high-level language (most commonly [Solidity](/wiki/economics/finance/defi/solidity/) for [Ethereum](/wiki/economics/finance/defi/ethereum/)-compatible chains, or Rust for Solana).
2. The code is compiled to bytecode and deployed to the blockchain via a transaction.
3. The deployed contract lives at an address and holds its own storage and (optionally) a balance of the native currency.
4. Users and other contracts interact with it by sending transactions that call its functions. Each function call is a transaction that costs gas.
5. State changes are recorded on-chain and are irreversible.

## Key properties

| Property | Implication |
|----------|-------------|
| **Immutability** | Bugs cannot be patched in place. Upgradeability requires proxy patterns or migration to a new contract. |
| **Determinism** | No randomness, no network calls, no filesystem access. External data requires [oracles](/wiki/economics/finance/defi/oracle-node). |
| **Atomicity** | A transaction either fully succeeds or fully reverts. Partial execution is impossible. |
| **Gas metering** | Every operation has a cost, preventing infinite loops and ensuring the network can price computation. |

## Common patterns

- **[ERC-20](/wiki/economics/finance/defi/ethereum/erc-20) tokens** — fungible token standard.
- **Proxy / upgradeable contracts** — separate storage from logic so the logic can be swapped.
- **Access control** — restrict sensitive functions to specific addresses (owner, multisig, governance).
- **Reentrancy guards** — prevent a called contract from calling back into the caller before the first invocation completes.
- **Flash loans** — uncollateralised loans that must be repaid within a single transaction, leveraging atomicity.

For Solidity-specific implementation details and patterns, see the [Solidity section](/wiki/economics/finance/defi/solidity/).

## Risks

- **Bugs and exploits** — immutability means a vulnerability in a deployed contract can be exploited until funds are drained or the contract is paused (if it has a pause mechanism). Audits and formal verification reduce but do not eliminate this risk.
- **Governance attacks** — contracts controlled by a single admin key or a small multisig can be rug-pulled. Look for timelocks, decentralised governance, and key management practices.
- **Composability risk** — a contract that depends on another contract inherits its risks. A bug in a dependency can cascade.

## External links

- [Ethereum.org: Introduction to Smart Contracts](https://ethereum.org/en/developers/docs/smart-contracts/) — official overview
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/) — audited, reusable contract library
- [Solidity documentation](https://docs.soliditylang.org/) — the primary smart contract language for Ethereum Virtual Machine chains
