---
title: "IOTA"
weight: 20
bookCollapseSection: true
---

[IOTA](https://en.wikipedia.org/wiki/IOTA_(technology)) is a permissionless distributed ledger built for machine-to-machine value transfer and real-world asset tokenisation. For most of its history it was deliberately *not* a [blockchain](/wiki/defi/blockchain): instead of a linear chain of blocks it recorded transactions in a [directed acyclic graph](/wiki/cs/dag/) called the [Tangle](/wiki/defi/iota/tangle), and it charged no transaction fees — design choices aimed squarely at high-volume [micropayments](/wiki/defi/micro-transactions) between IoT devices.

In May 2025 the **IOTA Rebased** upgrade replaced that architecture wholesale. The Tangle ledger gave way to a [Move](https://en.wikipedia.org/wiki/Move_(programming_language))-based object ledger with [delegated proof-of-stake](/wiki/defi/staking) consensus, real (if tiny) gas fees, and no central Coordinator. IOTA today is closer to a Sui-style Layer 1 than to the feeless DAG it started as. This section covers both the legacy model and the current one, because both still shape how the network is described in the wild.

## From the Tangle to Rebased

| Era | Ledger model | Fees | Decentralisation | Smart contracts |
|---|---|---|---|---|
| Tangle (pre-2025) | DAG of transactions; each tx approves two prior ones | None | Gated by a Foundation-run **Coordinator** | Off-ledger only (IOTA EVM as an L2) |
| [IOTA Rebased](/wiki/defi/iota/iota-rebased) (May 2025+) | Object ledger on the Move VM | ~0.005 IOTA per tx, burned | dPoS, ~150 permissionless validators, no Coordinator | Native Move on L1; [IOTA EVM](/wiki/defi/iota/iota-evm) still runs as L2 |

The pivot is the single most important thing to understand about IOTA. Most third-party explainers, exchange pages, and older documentation describe the Tangle as if it were still the production system. It is not — see [The Tangle](/wiki/defi/iota/tangle) for what it was and why it was retired.

## Two Smart-Contract Environments

Post-Rebased, IOTA exposes two programming surfaces:

- **Move on Layer 1** — resource-oriented contracts executing directly against the new object ledger, with parallel execution and Sui-derived [Mysticeti](https://blog.iota.org/iota-rebased-technical-view/) consensus.
- **[IOTA EVM](/wiki/defi/iota/iota-evm)** — a fully [EVM](/wiki/defi/ethereum/)-compatible chain where existing [Solidity](/wiki/defi/solidity/) and [ERC-20](/wiki/defi/ethereum/erc-20) tooling works unmodified. This remains the practical entry point for porting existing [DeFi](/wiki/defi/dex) protocols.

The IOTA Foundation has signalled an intent to eventually fold EVM execution into Layer 1, but as of the Rebased mainnet the two run side by side, bridged for asset transfers.

## Why It Matters for DeFi

IOTA's positioning is real-world assets, supply chain, and machine payments rather than pure on-chain speculation. The DeFi-relevant takeaways:

- **Solidity portability** — IOTA EVM means most Ethereum-native [dApps](/wiki/defi/dapp) can deploy with config changes only.
- **Low, predictable fees** — gas on L1 averages a fraction of a cent and can be *sponsored*, so applications can offer feeless UX to end users.
- **Staking yield** — IOTA holders can delegate to validators for protocol rewards; see [staking](/wiki/defi/staking).
- **MEV posture** — the Mysticeti pipeline limits some classes of [maximal extractable value](/wiki/defi/maximal-extractable-value), though this should be treated as a design goal rather than a guarantee.

## The IOTA Token

The native token is **IOTA** (historically tickered MIOTA). Under Rebased it pays gas, is burned on every transaction, and is the staking asset for dPoS. A separate incentivised network, **Shimmer (SMR)**, served as the staging ground for protocol upgrades; with Rebased live, Shimmer's role is largely historical.

## External Links

- [IOTA Documentation](https://docs.iota.org/) — current (Rebased) developer docs
- [IOTA Rebased: Technical View](https://blog.iota.org/iota-rebased-technical-view/) — the architecture overhaul explained by the Foundation
- [IOTA Rebased FAQ](https://docs.iota.org/about-iota/FAQ) — fees, staking, EVM relationship
- [Wikipedia: IOTA](https://en.wikipedia.org/wiki/IOTA_(technology))
- [From IOTA Tangle 2.0 to Rebased (MDPI, 2025)](https://www.mdpi.com/1424-8220/25/11/3408) — peer-reviewed comparative analysis

## Wiki Pages

{{< section >}}
