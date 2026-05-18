---
title: "IOTA Rebased"
weight: 2
---

IOTA Rebased is the protocol overhaul that went live on mainnet on **5 May 2025**. It retired [the Tangle](/wiki/defi/iota/tangle) as IOTA's ledger and replaced it with a [Move](https://en.wikipedia.org/wiki/Move_(programming_language))-based object ledger, [delegated proof-of-stake](/wiki/defi/staking) consensus, and real transaction fees. The architecture is derived from the same Mysten Labs research lineage as Sui — IOTA effectively rebased its mainnet onto that stack, hence the name.

## What Changed

| | Pre-Rebased (Tangle) | Rebased (May 2025+) |
|---|---|---|
| Ledger | DAG of transactions | Object ledger on the Move VM |
| Consensus | Tip approval + Coordinator milestones | Mysticeti dPoS, no Coordinator |
| Validators | Foundation Coordinator | Up to ~150 permissionless, staked |
| Fees | None | ~0.005 IOTA per tx, burned |
| Finality | Probabilistic (cumulative weight) | Deterministic, sub-second |
| L1 smart contracts | None | Native Move |

## Object Model and the Move VM

Instead of accounts-with-balances ([Ethereum](/wiki/defi/ethereum/)) or unspent outputs (Bitcoin, legacy IOTA), state is a set of typed **objects** owned by addresses. [Smart contracts](/wiki/defi/smart-contract) are Move modules; assets are Move *resources* — values the type system forbids from being copied or implicitly dropped, which structurally prevents whole classes of double-spend and accounting bugs.

Because transactions declare the objects they touch, the runtime can execute non-overlapping transactions **in parallel** rather than strictly serialising every transaction as the EVM does. This is the main throughput lever in the new design.

## Mysticeti Consensus and dPoS

Rebased uses **Mysticeti**, a DAG-based BFT consensus. Validators are elected by stake; IOTA holders who do not run infrastructure **delegate** their stake to validators and share in rewards — the standard delegated-PoS pattern. The Foundation-run Coordinator is gone, which is the decentralisation milestone the [Coordicide](/wiki/defi/iota/tangle#the-coordinator) programme had promised for years.

Published figures: **50,000+ TPS** capacity and finality on the order of **400–500 ms**. Treat these as benchmark/target numbers, as with any L1's headline throughput.

## Fees and Tokenomics

IOTA is no longer strictly feeless. Each transaction costs roughly **0.005 IOTA** on average, and that fee is **burned**, applying deflationary pressure. Fees are framed as a congestion-control mechanism, not a revenue model — they are deliberately tiny, and applications can **sponsor** fees so end users still experience a feeless flow.

Staking is inflationary to fund rewards: on the order of **767,000 IOTA minted per epoch**, an initial inflation rate near **6%**, distributed to validators and their delegators. Net token supply pressure is the burn rate against this issuance.

## Relationship to IOTA EVM

Rebased did not replace [IOTA EVM](/wiki/defi/iota/iota-evm). The EVM chain continues to run as a Layer 2 alongside the new Move Layer 1, bridged for asset transfers. The Foundation has stated an intent to integrate EVM execution into Layer 1 in future, but as of the Rebased mainnet they remain distinct environments — Move for L1-native development, EVM for Solidity portability.

## External Links

- [IOTA Rebased: Technical View](https://blog.iota.org/iota-rebased-technical-view/) — Foundation architecture writeup
- [IOTA Rebased FAQ](https://docs.iota.org/about-iota/FAQ) — fees, sponsoring, staking, EVM
- [Mysticeti paper](https://arxiv.org/abs/2310.14821) — the consensus protocol
- [IOTA 2025 Review](https://blog.iota.org/iota-2025-review/) — launch retrospective
