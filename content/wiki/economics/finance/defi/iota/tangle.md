---
title: "The Tangle"
weight: 1
---

The Tangle was IOTA's original ledger: a [directed acyclic graph](/wiki/cs/dag/) (DAG) of transactions rather than a chain of blocks. It defined the network from launch until the [IOTA Rebased](/wiki/economics/finance/defi/iota/iota-rebased) upgrade in May 2025 retired it. Understanding it still matters, because most third-party material describes IOTA as if the Tangle were the live system.

## What the Tangle Is

In a [blockchain](/wiki/economics/finance/defi/blockchain), miners or validators batch transactions into blocks and link the blocks in a line. The Tangle had no blocks and no dedicated block producers. Each new transaction directly **approved two previous transactions** by referencing them, forming a growing mesh:

- A transaction with no approvals yet is a **tip**.
- Issuing a transaction required selecting two tips, verifying they did not conflict, and doing a small [proof-of-work](https://en.wikipedia.org/wiki/Proof_of_work) to deter spam.
- Confirmation strength was measured by **cumulative weight** — how many later transactions indirectly approved a given one.

Because issuing a transaction also did the work of validating two others, throughput was meant to *increase* with usage rather than contend for scarce block space.

## Feeless by Design

With no miners competing for block rewards, there was no fee market. The sender's proof-of-work substituted for a fee. This was the entire point: IOTA targeted the machine economy, where billions of [micropayments](/wiki/economics/finance/defi/micro-transactions) between devices would be uneconomical if each carried a gas cost. Feelessness, not smart-contract expressiveness, was the original value proposition.

## The Coordinator

The Tangle had a well-known caveat. While the network was small, an attacker with modest hashing power could outpace honest tip approval and rewrite history (a "parasite chain" attack). IOTA's mitigation was the **Coordinator**: a node operated by the IOTA Foundation that periodically issued signed **milestones**. A transaction was considered confirmed only once referenced by a milestone.

This made the Coordinator a single point of trust and control — it could, in principle, censor or halt the network — and it drew sustained criticism that IOTA was not genuinely decentralised. Removing it was a years-long research programme branded **Coordicide** (and later **IOTA 2.0**).

## Why It Was Replaced

Coordicide never reached a production mainnet under the Tangle model. Meanwhile the ecosystem's demands shifted toward expressive [smart contracts](/wiki/economics/finance/defi/smart-contract), deterministic finality, and competitive throughput — areas where the DAG, having no account or unspent-transaction-output (UTXO) model, was awkward to extend. Rather than ship Coordicide, the Foundation pivoted: [IOTA Rebased](/wiki/economics/finance/defi/iota/iota-rebased) replaced the Tangle ledger entirely with a Move-based object ledger and delegated-proof-of-stake consensus.

A subtle point often muddled in coverage: Rebased did not abandon DAGs. Its Byzantine-fault-tolerant (BFT) consensus is itself DAG-structured — Mysticeti at launch, and **Starfish** since the May 2026 mainnet upgrade. What was retired is the *Tangle as the ledger and validation model* — the feeless, Coordinator-gated, tip-approval design — not the use of a DAG anywhere in the stack.

## External Links

- [Wikipedia: IOTA](https://en.wikipedia.org/wiki/IOTA_(technology))
- [The Tangle whitepaper (Popov, 2018)](https://assets.ctfassets.net/r1dr6vzfxhev/2t4uxvsIqk0EUau6g2sw0g/45eae33637ca92f85dd9f4a3a218e1ec/iota1_4_3.pdf)
- [From IOTA Tangle 2.0 to Rebased (MDPI, 2025)](https://www.mdpi.com/1424-8220/25/11/3408) — decentralisation and suitability analysis
