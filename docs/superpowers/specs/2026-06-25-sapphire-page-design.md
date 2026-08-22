# Sapphire Wiki Page — Design

**Date:** 2026-06-25
**Type:** New wiki content page (+ one stub)

## Goal

Create a Bitsy-independent, practical landing page for **Oasis Sapphire**, the
confidential EVM chain. The page should carry enough conceptual motivation to
explain *why* a reader might need a TEE chain, alongside concrete developer
facts. It is the first of several per-chain pages; future chains each get their
own section directly under `defi/` (matching `iota/`, `ethereum/`).

## Placement & Format

- **Path:** `content/wiki/economics/finance/defi/sapphire/_index.md`
- **Frontmatter:** `title: "Sapphire"`, `bookCollapseSection: true`, `weight`
  chosen to slot sensibly among existing chain sections (IOTA is 20; pick an
  unused value).
- Single, balanced `_index.md` — no sub-pages yet; spin them out organically
  (as IOTA did) once a subtopic earns it.
- Body starts at `##` (no H1 — Hugo Book renders `title`). Per `wiki-content`,
  `wiki-audience`, `wiki-linking` rules.

## Audience & Tone

Technically astute reader, new to confidential computing on-chain. Balanced:
motivation + concrete dev facts. Educational, opinionated where useful, honest
about limitations.

## Section Outline

1. **Intro paragraph** — Sapphire is Oasis's confidential EVM ParaTime; the only
   EVM-compatible chain where contract state and calldata are encrypted by
   default, enforced by hardware TEEs. Native token ROSE; relationship to the
   Oasis Network.
2. **Why You'd Want It** — the motivating core. Public chains leak *all* state,
   which breaks whole categories of apps: sealed-bid auctions, private
   voting/DAOs, hidden-information games, confidential DeFi, on-chain key
   management, secrets/credentials. Frame against the transparency + MEV problem
   (link [maximal-extractable-value](/wiki/economics/finance/defi/maximal-extractable-value)).
3. **How Confidentiality Works (TEEs)** — Intel SGX enclaves, encrypted runtime
   state, end-to-end encrypted calldata, remote attestation. Contrast with
   [zero-knowledge-proofs](/wiki/cs/zero-knowledge-proofs) ("ZK proves without
   revealing; TEEs compute privately inside sealed hardware"). Links to new
   [tee](/wiki/economics/finance/defi/tee) stub.
4. **The Confidential EVM in Practice** — what differs from vanilla Solidity:
   encrypted state is automatic; **view calls must be signed** (EIP-712) so the
   chain can authorize reads; the `@oasisprotocol/sapphire-paratime` wrapper
   (auto-encrypts `eth_call`/`eth_estimateGas`/`eth_signTransaction`) plus
   framework packages (`sapphire-ethers-v6`, `sapphire-viem-v2`, Hardhat,
   Wagmi); on-chain precompiles (secure randomness, key generation,
   sign/encrypt/decrypt). Keep code minimal and idiomatic per `solidity-examples`
   rules if any Solidity appears.
5. **Network Facts** — complete, copy-pasteable: Mainnet chain ID 23294
   (`0x5afe`) / Testnet 23295 (`0x5aff`), gas token ROSE, ~6s blocks, sub-cent
   gas, RPC + explorer + faucet links. No truncated values (per `wiki-content`).
6. **Limitations & Gotchas** — ordered by severity: confidentiality is *not*
   absolute (TEE side-channel history, trust in Intel attestation); gas /
   access-pattern leakage; secure randomness is for confidentiality, with caveats;
   composability friction with transparent chains.
7. **Recent Developments** — ROFL (Runtime Off-Chain Logic): TEE off-chain
   compute for oracles / AI agents, **mainnet July 2025** (Oasis Core v24.2;
   v24.3 adds Intel **TDX**). OPL (Oasis Privacy Layer) for cross-chain
   confidential calls.
8. **External Links** + **Wiki Pages** (`{{< section >}}`) — mirror IOTA footer.

## Linking Plan

- **Reuse existing pages:** `maximal-extractable-value`, `zero-knowledge-proofs`,
  `ethereum/` (EVM), `solidity/`, `blockchain`, `dapp`, `smart-contract`.
- **New stub:** `content/wiki/economics/finance/defi/tee.md` — Trusted Execution Environment
  concept (SGX/TDX, enclaves, remote attestation), with external links
  (Wikipedia, Intel SGX docs). Per `wiki-linking`, link targets must exist.

## Accuracy

Facts web-verified 2026-06-25: chain IDs, ROSE/gas, wrapper package names and
behavior, EIP-712 view-call auth, ROFL mainnet timing and TDX support, OPL.
Re-verify RPC/explorer/faucet URLs at draft time.

## Out of Scope

- Sub-pages (confidential-EVM deep dive, dev how-to) — deferred until earned.
- Bitsy-specific usage.
- A confidential-chains thematic grouping section (explicitly declined).
