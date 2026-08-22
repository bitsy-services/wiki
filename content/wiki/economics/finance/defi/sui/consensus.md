---
title: "Consensus"
weight: 40
---

Most blockchains funnel every transaction through a single global agreement step: validators must agree on one total order for all transactions before any of them execute. That step is the throughput bottleneck, and it is also where ordering games — front-running, sandwiching — become possible. Sui's central insight is that *most* transactions don't actually need a global order at all. Whether a transaction needs consensus depends entirely on the [object model](/wiki/economics/finance/defi/sui/object-model): specifically, whether it touches *owned* objects or *shared* objects.

## The Two-Path Execution Model

### The fast path (consensusless)

A transaction that touches only **owned objects** — objects controlled by a single address — does **not** go through full consensus. The reasoning is structural: only the owner can mutate an owned object, so there is no competing writer to order against. If two transactions never contend for the same mutable state, there is nothing to serialize. Asking a global consensus protocol to order them would be pure overhead.

Instead, validators certify these transactions through a **Byzantine-consistent-broadcast** style path. The client sends the transaction to validators, each checks it against the object's current version and signs, and once a quorum of signatures (a *certificate*) is collected the transaction is final. There is no agreement round, no waiting for a leader, no DAG commit rule — just verify and certify. The result is very low latency; Mysticeti's own measurements put single-owner finality around 250 ms.

This fast path is unique to Sui's object model and traces back to **FastPay**, Mysten Labs' earlier single-writer payment protocol, which showed that simple asset transfers can be settled with reliable broadcast alone. Simple SUI transfers, [NFT](/wiki/economics/finance/defi/nft) sends, and any single-owner state change ride this path.

### The consensus path

A transaction that touches a **shared object** — one that anyone can mutate, like an [AMM](/wiki/economics/finance/defi/amm) pool everyone trades against — *does* need a total order. If two traders hit the same pool in the same instant, the protocol must decide who goes first, and every honest validator must reach the same decision. That is precisely what Byzantine-fault-tolerant (BFT) consensus provides. Shared-object transactions therefore go through full consensus before they execute. This is the cost of programmable shared state, and it is the path that most interesting [DeFi](/wiki/economics/finance/defi/dex) takes.

## The Consensus Engine Lineage

The protocol running the consensus path has evolved through three generations.

**Narwhal + Bullshark/Tusk.** Sui's mainnet launched on a two-component design. **Narwhal** is a mempool that structures transaction data into a [directed acyclic graph](/wiki/cs/dag/) (DAG) of blocks, guaranteeing data availability — every block references prior blocks, and the structure spreads the dissemination load across all validators. A separate ordering layer (**Bullshark**, the deterministic successor to the randomized **Tusk**) then walks that DAG and deterministically picks a total order from it. The split worked but added latency: the ordering layer had to certify the DAG before committing.

**Mysticeti.** This was replaced by Mysticeti, a single round-trip **uncertified-DAG** Byzantine-fault-tolerant (BFT) protocol. The key word is *uncertified*: validators commit blocks directly from the DAG structure without a separate certification round, which is what eliminates a full network round-trip. On Mysten's benchmarks Mysticeti cut consensus latency by roughly 80% versus Bullshark, committing in about 500 ms while sustaining very high throughput. A variant, Mysticeti-FPC, weaves the fast path into the same DAG so owned-object and shared-object transactions share one structure.

**Mysticeti v2.** Rolled out from late 2025, v2 integrates **transaction validation directly into consensus** — validators sign transaction validity as part of signing their consensus blocks, batching many transactions per signature instead of signing each one individually. It also adds a **Transaction Driver** client submission path: instead of broadcasting to every validator, the client submits to a single validator (chosen by historical latency) and retrieves one copy of the effects, pushing network usage toward optimal. The combined result is roughly **50% lower validator CPU** and, on Mysten's benchmarks, around **100,000 transactions per second at ~390 ms** latency, with regional latency improvements of 25–35%.

The validator set running all of this is selected by delegated proof-of-stake: token holders delegate SUI to validators, who are chosen by stake weight. See [staking](/wiki/economics/finance/defi/staking) for how delegation and rewards work.

## MEV Implications

The two-path split changes the [MEV](/wiki/economics/finance/defi/maximal-extractable-value) surface but does not erase it. Fast-path owned-object transactions are never ordered against anything, so they are not exposed to ordering games — there is no sequence for a searcher to exploit. Shared-object DeFi is a different story: AMM swaps, lending liquidations, and anything touching shared state still flows through consensus, where ordering exists and can in principle be gamed. Sui is **not** MEV-immune; the architecture simply narrows the attack surface to the transactions that genuinely need a global order.

## Shared Lineage with IOTA

This consensus stack is not Sui's alone. When [IOTA](/wiki/economics/finance/defi/iota/) rebased its mainnet onto the Mysten Labs research stack in 2025, it launched on Mysticeti from the same lineage. IOTA later moved to its own **Starfish** protocol — another uncertified-DAG BFT design — but the family resemblance is direct. If you understand Sui's consensus path, you already understand most of IOTA Rebased's.

## External Links

- [Mysticeti v2: Faster and Lighter Sui Transaction Processing](https://blog.sui.io/mysticeti-v2-sui-consensus/) — the current engine, Transaction Driver, and benchmarks
- [Sui Consensus (official docs)](https://docs.sui.io/concepts/sui-architecture/consensus) — architecture reference
- [Mysticeti: Reaching the Latency Limits with Uncertified DAGs](https://arxiv.org/abs/2310.14821) — the original research paper
