---
title: "IOTA Rebased"
weight: 2
---

IOTA Rebased is the protocol overhaul that went live on mainnet on **5 May 2025**. It retired [the Tangle](/wiki/economics/finance/defi/iota/tangle) as IOTA's ledger and replaced it with a [Move](https://en.wikipedia.org/wiki/Move_(programming_language))-based object ledger, [delegated proof-of-stake](/wiki/economics/finance/defi/staking) consensus, and real transaction fees. The architecture is derived from the same Mysten Labs research lineage as Sui — IOTA effectively rebased its mainnet onto that stack, hence the name.

## What Changed

| | Pre-Rebased (Tangle) | Rebased (May 2025+) |
|---|---|---|
| Ledger | [DAG](/wiki/cs/dag) of transactions | Object ledger on the Move VM |
| Consensus | Tip approval + Coordinator milestones | Byzantine-fault-tolerant (BFT) dPoS over a DAG, no Coordinator (Mysticeti at launch, Starfish since May 2026) |
| Validators | Foundation Coordinator | Up to ~150 permissionless, staked |
| Fees | None | ~0.005 IOTA per tx, burned |
| Finality | Probabilistic (cumulative weight) | Deterministic, sub-second |
| L1 smart contracts | None | Native Move |

## Object Model and the Move VM

Instead of accounts-with-balances ([Ethereum](/wiki/economics/finance/defi/ethereum/)) or unspent outputs (Bitcoin, legacy IOTA), state is a set of typed **objects** owned by addresses. [Smart contracts](/wiki/economics/finance/defi/smart-contract) are Move modules; assets are Move *resources* — values the type system forbids from being copied or implicitly dropped, which structurally prevents whole classes of double-spend and accounting bugs.

Because transactions declare the objects they touch, the runtime can execute non-overlapping transactions **in parallel** rather than strictly serialising every transaction as the EVM does. This is the main throughput lever in the new design.

## Consensus: Mysticeti to Starfish

Validators are elected by stake; IOTA holders who do not run infrastructure **delegate** their stake to validators and share in rewards — the standard delegated-PoS pattern. The Foundation-run Coordinator is gone, which is the decentralisation milestone the [Coordicide](/wiki/economics/finance/defi/iota/tangle#the-coordinator) programme had promised for years.

Rebased launched on **Mysticeti**, the DAG-based BFT consensus from Mysten Labs. Mysticeti's "uncertified DAG" design achieves very low latency but, as later research showed, lacks rigorous liveness proofs — under adversarial network conditions honest validators could fail to commit even after the network stabilised (a desynchronization attack). In **May 2026**, mainnet protocol **v24** (release v1.21.1) replaced it with **[Starfish](https://blog.iota.org/why-starfish-matters/)** (IIP-2), IOTA's own consensus protocol. Starfish keeps the uncertified-DAG efficiency but adds a "push pacemaker" and *Encoded Cordial Dissemination* (Reed–Solomon erasure coding plus data-availability certificates) to guarantee liveness and keep communication linear as the validator set grows. Reported p99 latency improved from roughly 486 ms to 312 ms versus Mysticeti.

Published figures: **50,000+ transactions per second** capacity and finality on the order of **400–500 ms**. Treat these as benchmark/target numbers, as with any L1's headline throughput.

## Fees and Tokenomics

IOTA is no longer strictly feeless. Each transaction costs roughly **0.005 IOTA** on average, and that fee is **burned**, applying deflationary pressure. Fees are framed as a congestion-control mechanism, not a revenue model — they are deliberately tiny, and applications can **sponsor** fees so end users still experience a feeless flow.

Staking is inflationary to fund rewards: on the order of **767,000 IOTA minted per epoch**, an initial inflation rate near **6%** (set to decline over time), distributed to validators and their delegators. Realised yields have run roughly **10–15% APY** (annual percentage yield) depending on the staked ratio and validator commissions. Net token supply pressure is the burn rate against this issuance. A later upgrade — IIP-8, mainnet protocol **v20** — added *dynamic minimum validator commissions* to discourage stake concentration; running a mainnet validator requires a self-stake of at least **2,000,000 IOTA**.

## Relationship to IOTA EVM

Rebased did not replace [IOTA EVM](/wiki/economics/finance/defi/iota/iota-evm). The EVM chain continues to run as a Layer 2 alongside the new Move Layer 1, bridged for asset transfers. The Foundation has stated an intent to integrate EVM execution into Layer 1 in future; as of mid-2026 that remains roadmap rather than shipped, so they are still distinct environments — Move for L1-native development, EVM for Solidity portability.

## Account Abstraction

Post-launch, IOTA has been adding **account abstraction** (specified in IIP-0009): on-chain objects can act as accounts with programmable authentication and authorisation, enabling native multisig (comparable to Safe), session keys, and sponsor-pays flows without external contract wallets. The core shipped to dev, alpha, and test networks through Q1 2026, with mainnet rollout in progress. Combined with fee sponsoring, this is aimed squarely at onboarding non-crypto-native users — the prerequisite for the enterprise and trade use cases IOTA now targets.

## Roadmap

Rebased was the foundation, not the finish line. The trajectory through 2026, per the [IOTA Manifesto](https://manifesto.iota.org/) and quarterly updates:

- **Consensus and node performance** — Starfish on mainnet; a FastCommitSyncer that restores faulted nodes ~20–30× faster; an indexer rebuilt for ~80× throughput on data-heavy reads; gRPC node APIs.
- **Account abstraction to mainnet** — finishing the rollout begun on test networks.
- **EVM–L1 convergence** — still the stated long-term goal for unifying the two smart-contract surfaces.
- **Enterprise/RealFi products** — Identity, IOTA Names, Notarization, and the TWIN trade network as the demand drivers for L1 usage.

## External Links

- [IOTA Rebased: Technical View](https://blog.iota.org/iota-rebased-technical-view/) — Foundation architecture writeup
- [Why Starfish Matters](https://blog.iota.org/why-starfish-matters/) — the Mysticeti-to-Starfish consensus switch
- [IIP-2: Starfish Consensus Protocol](https://iotaledger.github.io/IIPs/iips/IIP-0002/iip-0002.html) — the specification
- [IOTA Rebased FAQ](https://docs.iota.org/about-iota/FAQ) — fees, sponsoring, staking, EVM
- [Mysticeti paper](https://arxiv.org/abs/2310.14821) — the launch consensus protocol
- [IOTA Q1 2026 Progress Update](https://blog.iota.org/q12026-progress-update/) — recent protocol and ecosystem milestones
