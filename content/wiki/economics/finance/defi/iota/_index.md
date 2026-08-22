---
title: "IOTA"
weight: 20
bookCollapseSection: true
---

[IOTA](https://en.wikipedia.org/wiki/IOTA_(technology)) is a permissionless distributed ledger built for machine-to-machine value transfer and real-world asset tokenisation. For most of its history it was deliberately *not* a [blockchain](/wiki/economics/finance/defi/blockchain): instead of a linear chain of blocks it recorded transactions in a [directed acyclic graph](/wiki/cs/dag/) called the [Tangle](/wiki/economics/finance/defi/iota/tangle), and it charged no transaction fees — design choices aimed squarely at high-volume [micropayments](/wiki/economics/finance/defi/micro-transactions) between IoT devices.

In May 2025 the **IOTA Rebased** upgrade replaced that architecture wholesale. The Tangle ledger gave way to a [Move](https://en.wikipedia.org/wiki/Move_(programming_language))-based object ledger with [delegated proof-of-stake](/wiki/economics/finance/defi/staking) consensus, real (if tiny) gas fees, and no central Coordinator. IOTA today is closer to a Sui-style Layer 1 than to the feeless DAG it started as. This section covers both the legacy model and the current one, because both still shape how the network is described in the wild.

Since the relaunch the Foundation has steered hard toward a single thesis, formalised in the January 2026 **[IOTA Manifesto: The World Onchain](https://manifesto.iota.org/)**: rather than compete as a general-purpose smart-contract chain, IOTA aims to be the neutral settlement and data layer for the ~$35 trillion global trade sector. The flagship of that strategy is **TWIN** — the Trade Worldwide Information Network — which went live on mainnet in early 2026. Read against this, the DeFi material below is one facet of a broader "RealFi" (real-world-asset finance) positioning, not the network's headline use case.

## From the Tangle to Rebased

| Era | Ledger model | Fees | Decentralisation | Smart contracts |
|---|---|---|---|---|
| Tangle (pre-2025) | DAG of transactions; each tx approves two prior ones | None | Gated by a Foundation-run **Coordinator** | Off-ledger only (IOTA EVM as an L2) |
| [IOTA Rebased](/wiki/economics/finance/defi/iota/iota-rebased) (May 2025+) | Object ledger on the Move VM | ~0.005 IOTA per tx, burned | dPoS, permissionless staked validators, no Coordinator | Native Move on L1; [IOTA EVM](/wiki/economics/finance/defi/iota/iota-evm) still runs as L2 |

The pivot is the single most important thing to understand about IOTA. Most third-party explainers, exchange pages, and older documentation describe the Tangle as if it were still the production system. It is not — see [The Tangle](/wiki/economics/finance/defi/iota/tangle) for what it was and why it was retired.

## Two Smart-Contract Environments

Post-Rebased, IOTA exposes two programming surfaces:

- **Move on Layer 1** — resource-oriented contracts executing directly against the new object ledger, with parallel execution and a Byzantine-fault-tolerant (BFT) consensus over a [DAG](/wiki/cs/dag). (Rebased launched on Mysten Labs' [Mysticeti](https://blog.iota.org/iota-rebased-technical-view/); in May 2026 IOTA replaced it on mainnet with its own [Starfish](https://blog.iota.org/why-starfish-matters/) protocol — see [IOTA Rebased](/wiki/economics/finance/defi/iota/iota-rebased#consensus-mysticeti-to-starfish).)
- **[IOTA EVM](/wiki/economics/finance/defi/iota/iota-evm)** — a fully [EVM](/wiki/economics/finance/defi/ethereum/)-compatible chain where existing [Solidity](/wiki/economics/finance/defi/solidity/) and [ERC-20](/wiki/economics/finance/defi/ethereum/erc-20) tooling works unmodified. This remains the practical entry point for porting existing [DeFi](/wiki/economics/finance/defi/dex) protocols.

The IOTA Foundation has signalled an intent to eventually fold EVM execution into Layer 1. As of mid-2026 that integration is still on the roadmap rather than shipped — the two run side by side, bridged for asset transfers.

## Why It Matters for DeFi

IOTA's positioning is real-world assets, supply chain, and machine payments rather than pure on-chain speculation. The DeFi-relevant takeaways:

- **Solidity portability** — IOTA EVM means most Ethereum-native [dApps](/wiki/economics/finance/defi/dapp) can deploy with config changes only.
- **Low, predictable fees** — gas on L1 averages a fraction of a cent and can be *sponsored*, so applications can offer feeless UX to end users.
- **Staking yield** — IOTA holders can delegate to validators for protocol rewards; see [staking](/wiki/economics/finance/defi/staking).
- **MEV posture** — the DAG-based consensus pipeline (now Starfish) limits some classes of [maximal extractable value](/wiki/economics/finance/defi/maximal-extractable-value), though this should be treated as a design goal rather than a guarantee.

## The IOTA Token

The native token is **IOTA** (historically tickered MIOTA). Under Rebased it pays gas, is burned on every transaction, and is the staking asset for dPoS. Delegated staking has paid roughly **10–15% APY** (annual percentage yield) since launch, funded by issuance of about 767,000 IOTA per epoch (~6% annual inflation, set to decline over time). A separate incentivised network, **Shimmer (SMR)**, served as the staging ground for protocol upgrades; with Rebased live, Shimmer's role is largely historical.

## Recent Developments and Roadmap

The year after Rebased has been one of steady protocol hardening plus an aggressive enterprise pivot. Highlights through mid-2026:

- **Starfish consensus (May 2026)** — mainnet protocol v24 swapped Mysticeti for IOTA's own [Starfish](https://blog.iota.org/why-starfish-matters/), an uncertified-DAG BFT protocol with rigorous liveness proofs and better tail latency under adverse conditions. Detail on [the Rebased page](/wiki/economics/finance/defi/iota/iota-rebased#consensus-mysticeti-to-starfish).
- **Account abstraction** — programmable on-chain accounts (dynamic authentication, native multisig à la Safe) specified in IIP-0009 (an IOTA Improvement Proposal) and live on dev/test networks, with mainnet rollout in progress.
- **Identity and naming** — **IOTA Names** (human-readable addresses) launched on mainnet, and **IOTA Identity 1.9** added SD-JWT credentials aligned to the W3C Data Model 2.0.
- **TWIN goes live** — the Trade Worldwide Information Network reached mainnet in early 2026, with national pilots in Kenya and the UK (Teesside) and exploration in Rwanda. The Manifesto targets 5+ country pilots within 12 months and 30+ by 2030.
- **Validator decentralisation** — IIP-8 (protocol v20) introduced dynamic minimum validator commissions to discourage stake concentration; mainnet validators require a 2,000,000 IOTA minimum self-stake.

The throughline is **RealFi over speculative DeFi**: tokenised commodities, trade receivables, and verifiable documents on L1, with the Move/EVM smart-contract surfaces and the [Gas Station](https://docs.iota.org/) fee-sponsorship service positioned as enablers for non-crypto-native users.

## External Links

- [IOTA Documentation](https://docs.iota.org/) — current (Rebased) developer docs
- [IOTA Manifesto: The World Onchain](https://manifesto.iota.org/) — the 2026 global-trade strategy and roadmap
- [IOTA Q1 2026 Progress Update](https://blog.iota.org/q12026-progress-update/) — Starfish, account abstraction, TWIN, indexer
- [IOTA Rebased: Technical View](https://blog.iota.org/iota-rebased-technical-view/) — the architecture overhaul explained by the Foundation
- [IOTA Rebased FAQ](https://docs.iota.org/about-iota/FAQ) — fees, staking, EVM relationship
- [Wikipedia: IOTA](https://en.wikipedia.org/wiki/IOTA_(technology))
- [From IOTA Tangle 2.0 to Rebased (MDPI, 2025)](https://www.mdpi.com/1424-8220/25/11/3408) — peer-reviewed comparative analysis

## Wiki Pages

{{< section >}}
