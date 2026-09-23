---
title: "Smart Contract"
weight: 20
bookCollapseSection: true
---

A smart contract is a program deployed to a blockchain that executes automatically when its functions are called. Once deployed, the code is immutable (unless the contract uses an upgradeable proxy pattern) and its execution is deterministic — given the same state and inputs, every node on the network will produce the same result.

Every [DEX](/wiki/economics/defi/markets/dex), lending protocol, [liquidity pool](/wiki/economics/defi/markets/liquidity-pool), and token in DeFi is a smart contract, or a set of contracts calling each other.

## What they replace

A traditional agreement is backed by a counterparty's willingness to perform, or by a third party that can compel performance — a court, an escrow agent, a clearinghouse. A smart contract substitutes published code: the terms are readable before anyone commits to them, they execute exactly as written, and the network's consensus mechanism is what enforces them.

Protocols built this way are:

- **Permissionless** — anyone can interact with them, no account application required.
- **Composable** — one contract can call another, enabling complex systems to be built from simple primitives.
- **Transparent** — the source code and all state transitions are publicly auditable.

## How they work

1. A developer writes the contract in a high-level language (most commonly [Solidity](/wiki/economics/defi/development/solidity/) for [Ethereum](/wiki/economics/defi/chains/ethereum/)-compatible chains, or Rust for Solana).
2. The code is compiled to bytecode and deployed to the blockchain via a transaction.
3. The deployed contract lives at an address and holds its own storage and (optionally) a balance of the native currency.
4. Users and other contracts interact with it by sending transactions that call its functions. Each function call is a transaction that costs gas.
5. State changes are recorded on-chain and are irreversible.

## Key properties

| Property | Implication |
|----------|-------------|
| **Immutability** | Bugs cannot be patched in place. Upgradeability requires proxy patterns or migration to a new contract. |
| **Determinism** | No randomness, no network calls, no filesystem access. External data requires [oracles](/wiki/economics/defi/oracles/oracle-node). |
| **Atomicity** | A transaction either fully succeeds or fully reverts. Partial execution is impossible. |
| **Gas metering** | Every operation has a cost, preventing infinite loops and ensuring the network can price computation. |

## Common patterns

- **[ERC-20](/wiki/economics/defi/chains/ethereum/erc-20) tokens** — fungible token standard.
- **Proxy / upgradeable contracts** — separate storage from logic so the logic can be swapped.
- **Access control** — restrict sensitive functions to specific addresses (owner, multisig, governance).
- **Reentrancy guards** — prevent a called contract from calling back into the caller before the first invocation completes.
- **Flash loans** — uncollateralised loans that must be repaid within a single transaction, leveraging atomicity.

For Solidity-specific implementation details and patterns, see the [Solidity section](/wiki/economics/defi/development/solidity/).

## Risks

- **Bugs and exploits** — immutability means a vulnerability in a deployed contract can be exploited until funds are drained or the contract is paused (if it has a pause mechanism). Audits and formal verification reduce but do not eliminate this risk.
- **Governance attacks** — contracts controlled by a single admin key or a small multisig can be rug-pulled. Look for timelocks, decentralised governance, and key management practices. [Hidden admin controls](/wiki/economics/fraud/hidden-admin-controls) covers which privileged functions to look for, and why an upgradeable proxy makes an audit of the implementation close to meaningless.
- **Composability risk** — a contract that depends on another contract inherits its risks. A bug in a dependency can cascade.

## In this section

A [finalized smart contract](/wiki/economics/defi/smart-contract/finalized-smart-contract) is one nobody — including its author — can change, which is the property everything below depends on. On top of the contract sit the [decentralized application](/wiki/economics/defi/smart-contract/dapp) that wraps it in an interface, the [decentralized autonomous organization](/wiki/economics/defi/smart-contract/dao) that governs one by vote, and the loose banner of [Web3](/wiki/economics/defi/smart-contract/web3) covering the lot. A [trusted execution environment](/wiki/economics/defi/smart-contract/tee) is a hardware enclave that runs code whose state nobody outside it, including the machine's operator, can read — the confidentiality a public chain, which broadcasts every byte of state, cannot offer — and is what a confidential chain such as [Sapphire](/wiki/economics/defi/chains/sapphire) is built on. [Smart contracts in real estate](/wiki/economics/defi/smart-contract/smart-contracts-in-real-estate) looks at the most-cited non-financial application and where it runs aground.

## External links

- [Ethereum.org: Introduction to Smart Contracts](https://ethereum.org/en/developers/docs/smart-contracts/) — official overview
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/) — audited, reusable contract library
- [Solidity documentation](https://docs.soliditylang.org/) — the primary smart contract language for Ethereum Virtual Machine chains

## Wiki Pages

{{< section >}}
