---
title: "Sui"
weight: 25
bookCollapseSection: true
---

[Sui](https://sui.io/) is a high-throughput, low-latency [Layer 1](/wiki/economics/finance/defi/blockchain) [blockchain](/wiki/economics/finance/defi/blockchain) built by **Mysten Labs**, a team of engineers and researchers who previously built the Diem (Libra) and Novi projects at Meta. It launched its mainnet in **May 2023**. Sui's defining bet is that the account-and-balance model used by [Ethereum](/wiki/economics/finance/defi/ethereum/) and most other chains is the wrong primitive for scaling: instead, Sui represents all on-chain state as discrete, typed [objects](/wiki/economics/finance/defi/sui/object-model), which lets independent transactions execute *in parallel* rather than single-file.

That object model is paired with the [Move](/wiki/economics/finance/defi/sui/sui-move) language — a resource-oriented language, also created at Meta, in which on-chain assets are first-class values the type system refuses to copy or silently drop. Sui shares this Move/object lineage with [IOTA](/wiki/economics/finance/defi/iota/), which rebased its own mainnet onto the same Mysten Labs research stack in 2025. If you know one, much of the other will feel familiar.

## Why Sui Is Different

Three design choices distinguish Sui from EVM chains, and most of the rest of this section elaborates on them:

- **The [object model](/wiki/economics/finance/defi/sui/object-model).** State is a graph of owned, shared, and immutable objects rather than a flat map of account balances. Ownership is explicit and tracked by the protocol.
- **Parallel execution.** Transactions that touch disjoint sets of objects never contend, so the network scales with available hardware instead of being bottlenecked by a global lock. Transactions touching only *owned* objects skip [consensus](/wiki/economics/finance/defi/sui/consensus) entirely via a "fast path."
- **[Move](/wiki/economics/finance/defi/sui/sui-move) as the contract language.** Assets are typed resources with linear semantics, eliminating whole classes of bugs (reentrancy, accidental loss) that plague [Solidity](/wiki/economics/finance/defi/solidity/).

On top of these, Sui adds developer- and user-facing primitives that have no clean Ethereum equivalent: [Programmable Transaction Blocks](/wiki/economics/finance/defi/sui/programmable-transaction-blocks) (compose many actions atomically in one transaction) and [zkLogin](/wiki/economics/finance/defi/sui/zklogin) (derive a wallet from a Web2 OAuth login, no seed phrase).

## Consensus at a Glance

Sui uses **Mysticeti**, a DAG-based Byzantine-fault-tolerant [consensus](/wiki/economics/finance/defi/sui/consensus) protocol, with proof-of-stake validator selection. The **Mysticeti v2** upgrade (rolled out from late 2025) folds transaction validation into consensus and, on Mysten's benchmarks, sustains ~100,000 transactions per second at roughly 390 ms finality. Crucially, single-owner transactions bypass consensus altogether and finalize even faster. See [Consensus](/wiki/economics/finance/defi/sui/consensus) for the Narwhal/Bullshark history and the fast-path vs. consensus-path split.

## The SUI Token

The native token is **SUI**, with a hard-capped maximum supply of **10 billion**. Roughly 40% was circulating in early 2026; the remainder vests on a multi-year schedule into the late 2020s. SUI has four roles:

- **Gas** — pays for [computation and storage](/wiki/economics/finance/defi/sui/gas-and-storage).
- **Staking** — delegated to validators to secure the proof-of-stake network and earn rewards drawn from gas fees plus stake subsidies; see [staking](/wiki/economics/finance/defi/staking).
- **Storage fund** — fees for on-chain storage are escrowed in a protocol-managed [storage fund](/wiki/economics/finance/defi/sui/gas-and-storage), which pays future validators for retaining that data and is refunded (rebated) when data is deleted. As usage grows, SUI accumulates in the fund and is effectively removed from circulation.
- **Governance** — on-chain voting on protocol parameters.

## Why It Matters for DeFi

- **Parallelism for trading.** [DeepBook](/wiki/economics/finance/defi/sui/defi-ecosystem), Sui's native on-chain central limit order book, exploits parallel execution to deliver a low-latency [DEX](/wiki/economics/finance/defi/dex) primitive that other protocols build on as shared liquidity.
- **Low, predictable fees.** Gas is fractions of a cent, and the computation/storage split keeps pricing stable; see [Gas & Storage](/wiki/economics/finance/defi/sui/gas-and-storage).
- **Onboarding.** [zkLogin](/wiki/economics/finance/defi/sui/zklogin) lets [dApps](/wiki/economics/finance/defi/dapp) onboard users with a Google or Apple login instead of a seed phrase, lowering the biggest UX barrier in DeFi.
- **MEV posture.** Owned-object transactions that skip consensus are not subject to ordering games, narrowing some [MEV](/wiki/economics/finance/defi/maximal-extractable-value) surface — though shared-object DeFi (AMMs, lending) still orders through consensus and is not immune.

See [DeFi on Sui](/wiki/economics/finance/defi/sui/defi-ecosystem) for the ecosystem map.

## Recent Developments

- **Mysticeti v2 (late 2025)** — validation merged into consensus and a new Transaction Driver client path; large latency and validator-CPU reductions. Detail on [Consensus](/wiki/economics/finance/defi/sui/consensus).
- **Programmable privacy stack** — Mysten released **Seal** (decentralized secrets management / threshold encryption; whitepaper January 2026) and **Nautilus** (verifiable off-chain compute in [TEEs](/wiki/economics/finance/defi/tee)). Combined with [Walrus](/wiki/economics/finance/defi/sui/walrus) storage, these target confidential-but-auditable applications and signal a 2026 "privacy pivot."
- **Walrus mainnet (March 2025)** — Mysten's [decentralized blob-storage network](/wiki/economics/finance/defi/sui/walrus) went live with the WAL token.
- **DeepBook v3 + DEEP token** — the native order book added flash loans, governance, and its own fee token; see [DeFi on Sui](/wiki/economics/finance/defi/sui/defi-ecosystem).
- **Security note.** Sui DeFi TVL peaked around **$2.6 B in October 2025** before falling to roughly **$561 M by February 2026**, driven partly by the May 2025 [Cetus](/wiki/economics/finance/defi/sui/defi-ecosystem) exploit and broader market weakness — a reminder that ecosystem maturity lags the protocol's engineering.

## External Links

- [Sui Documentation](https://docs.sui.io/) — official developer docs
- [Sui Tokenomics Overview](https://docs.sui.io/concepts/tokenomics) — gas, staking, storage fund
- [Mysticeti v2: Faster and Lighter Sui Transaction Processing](https://blog.sui.io/mysticeti-v2-sui-consensus/) — the current consensus engine
- [The Move Book](https://move-book.com/) — Sui Move language reference
- [Sui GitHub](https://github.com/MystenLabs/sui) — protocol source
- [Wikipedia: Sui (blockchain)](https://en.wikipedia.org/wiki/Sui_(blockchain))

## Wiki Pages

{{< section >}}
