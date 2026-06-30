# Sui Wiki Section — Design

**Date:** 2026-06-30
**Type:** New wiki section — index + 8 sub-pages (+ stubs as needed)

## Goal

Create a deep-dive section on the **Sui** blockchain, a high-performance Layer 1
built by Mysten Labs (ex-Meta/Diem team) around an object-centric ledger and the
Move language. The section balances **technical architecture** (what makes Sui
distinct as an L1) with a **DeFi/developer lens** (building on Sui, the
ecosystem). It mirrors the depth and footer conventions of the existing `iota/`
section, with which it shares a Mysten Labs research lineage (Move, Mysticeti) —
so the two cross-link heavily.

## Placement & Format

- **Path:** `content/wiki/defi/sui/` (sibling to `iota/`, `sapphire/`,
  `ethereum/`).
- **Section frontmatter:** `title: "Sui"`, `bookCollapseSection: true`,
  `weight: 25` (slots just after IOTA's 20, reflecting the shared lineage).
- Each page body starts at `##` (no H1 — Hugo Book renders frontmatter `title`).
  Per `wiki-content`, `wiki-audience`, `wiki-linking`, `wiki-scope` rules.
- `_index.md` footer ends with **External Links** + **Wiki Pages**
  (`{{< section >}}`), mirroring the IOTA index.

## Audience & Tone

Technically astute reader, possibly new to Sui or to Move/object-model chains.
Educational, balanced motivation + concrete facts, opinionated where useful,
honest about trade-offs and immaturity.

## Pages

### 1. `_index.md` — Sui (overview)
History (Mysten Labs, ex-Meta Diem/Novi team, mainnet May 2023); the
object-centric model in brief; Move; consensus at a glance (Mysticeti); the SUI
token + tokenomics (supply, gas, staking, storage fund); DeFi positioning; recent
developments / roadmap; "Why It Matters for DeFi"-style balanced takeaways. Links
out to every sub-page. Cross-link to [iota](/wiki/defi/iota/) (shared lineage).

### 2. `object-model.md` — The Object Model
Sui's defining feature. Objects vs the account/balance model; **owned** vs
**shared** vs **immutable** objects; object IDs, versions, and ownership; how
single-owner objects bypass consensus to enable parallel execution. The
conceptual key to the rest of the section.

### 3. `sui-move.md` — Sui Move
Move as a resource-oriented language; Sui Move vs core Move / Aptos Move (object
model, `key`/`store` abilities, no global storage); modules, structs, abilities;
contrast with Solidity (link [solidity](/wiki/defi/solidity/)). Cross-link to
IOTA (also Move-based). Note the 2024 "Move 2024" edition if current.

### 4. `programmable-transaction-blocks.md` — Programmable Transaction Blocks
PTBs: chaining many Move calls + transfers atomically in a single transaction,
passing outputs of one command as inputs to the next. A signature Sui dev
ergonomic with no clean Ethereum equivalent. Brief illustrative (pseudo)code.

### 5. `consensus.md` — Consensus
**Mysticeti** (current DAG-BFT) and the Narwhal/Bullshark lineage that preceded
it; the single-owner **fast path** (consensusless / owned-object transactions)
vs the consensus path for shared objects; throughput/latency posture; MEV notes
(link [maximal-extractable-value](/wiki/defi/maximal-extractable-value)).
Cross-link to IOTA's Mysticeti→Starfish history.

### 6. `gas-and-storage.md` — Gas & Storage
The gas model (computation + storage components); the **storage fund** and
**storage rebates** (paying once for perpetual storage, reclaiming on deletion);
reference gas price set by validators; predictable low fees. Why this differs
from Ethereum's pure pay-per-gas.

### 7. `zklogin.md` — zkLogin
Web2 OAuth (Google/Apple/etc.) → a Sui address via a zero-knowledge proof, with
no new seed phrase; the salt/ephemeral-key flow at a high level; what it solves
for onboarding and what it trusts. Link
[zero-knowledge-proofs](/wiki/cs/zero-knowledge-proofs) (verify path) or external
if absent.

### 8. `walrus.md` — Walrus
Mysten Labs' decentralized blob/storage network; erasure-coding approach;
relationship to Sui (storage coordinated on-chain, blobs off-chain); WAL token;
use cases (large media, data availability). Mainnet status verified at draft.

### 9. `defi-ecosystem.md` — DeFi on Sui
The DeFi lens. **DeepBook** (native on-chain central limit order book) as the
shared liquidity layer; AMMs/DEXs (Cetus, Turbos); lending (Suilend, Navi);
stablecoins; bridges (Wormhole, etc.). Honest on maturity/TVL. Links
[dex](/wiki/defi/dex), [dapp](/wiki/defi/dapp), [staking](/wiki/defi/staking).

## Linking Plan

- **Reuse existing pages:** `blockchain`, `ethereum/` (EVM), `solidity/`, `dapp`,
  `smart-contract`, `staking`, `dex`, `maximal-extractable-value`,
  `zero-knowledge-proofs`, `iota/` (cross-link both directions).
- **Move concept:** fold the general "what is Move" framing into `sui-move.md`
  and link IOTA's Move usage rather than create a separate stub, unless a clean
  first-mention link target is needed elsewhere — then create a minimal stub.
- **New stubs:** create only for first-mention terms with no existing target
  (decide at draft time; e.g. `zero-knowledge-proofs` location to be confirmed).

## Accuracy

Web-verify at draft time rather than from memory: mainnet date; current consensus
(Mysticeti and any successor); SUI total/circulating supply and tokenomics;
DeepBook version (v3); Walrus mainnet status and WAL token; zkLogin specifics;
Move 2024 edition status; live RPC/explorer/docs URLs.

## Out of Scope

- Bitsy-specific usage.
- Exhaustive API references or step-by-step tutorials (link upstream docs).
- Comparative "Sui vs Aptos vs Solana" essay beyond brief contrasts where they
  clarify a Sui design choice.
