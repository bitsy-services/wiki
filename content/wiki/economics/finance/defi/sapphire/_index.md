---
title: "Sapphire"
weight: 15
bookCollapseSection: true
---

[Oasis](https://oasis.net/) **Sapphire** is the first and, for now, the only general-purpose **confidential [EVM](/wiki/economics/finance/defi/ethereum/)** — a fully Ethereum-compatible chain where [smart contract](/wiki/economics/finance/defi/smart-contract) state and transaction calldata are *encrypted by default*. Ordinary [Solidity](/wiki/economics/finance/defi/solidity/) compiles and runs unchanged, but the contract's storage, the arguments you send it, and the values it returns are sealed inside a hardware [trusted execution environment](/wiki/economics/finance/defi/tee) (TEE) and never exposed to validators, RPC providers, or block explorers. Sapphire is a *ParaTime* (a runtime) on the Oasis Network; its gas token is **ROSE**.

The pitch in one sentence: everything you already know how to build for Ethereum, but with private state — without rolling your own cryptography.

## Why You'd Want It

Every public blockchain is a broadcast medium. Contract storage, function arguments, and event logs are visible to everyone, forever. That transparency is a feature for auditability and a fatal flaw for any application that depends on *keeping a secret while computing on it*. The usual workarounds — commit-reveal schemes, off-chain order books, trusted operators, ZK circuits — each add latency, complexity, or a trust assumption. A confidential EVM removes the leak at the execution layer, so a contract can simply hold a secret in a state variable.

Concretely, encrypted on-chain state unlocks categories of application that are awkward or impossible on a transparent chain:

- **Sealed-bid auctions and private order flow** — bids stay hidden until settlement, which structurally removes the front-running and [maximal extractable value](/wiki/economics/finance/defi/maximal-extractable-value) that plague transparent [DEXes](/wiki/economics/finance/defi/dex). A searcher cannot front-run an order it cannot read.
- **Private voting and [DAO](/wiki/economics/finance/defi/dao) governance** — ballots that aren't visible mid-vote prevent vote-buying and bandwagoning.
- **Hidden-information games** — poker hands, fog-of-war, anything needing secret state that the players themselves can't peek at.
- **On-chain key management and gated access** — a contract can hold an API key, a decryption key, or a signing key and release outputs only to callers who satisfy on-chain rules, because the key never leaves the enclave.
- **Confidential DeFi and real-world assets (RWA)** — undercollateralized lending against private credit data, balances that aren't world-readable, compliance checks that don't dox the user.

The mental model: on Ethereum, "on-chain" means "public." On Sapphire, "on-chain" can mean "private but verifiable."

## How Confidentiality Works

Sapphire executes contracts inside a [TEE](/wiki/economics/finance/defi/tee) — historically Intel SGX (Software Guard Extensions) enclaves. The CPU encrypts enclave memory in hardware, so the machine operator running the node cannot read the contract's working state or storage even with full control of the host. Three things are protected:

- **State** — contract storage is encrypted at rest with keys held by the enclave. Reading the chain's database yields ciphertext.
- **Calldata** — transaction arguments are encrypted end-to-end from the client to the enclave, so the payload is private even in the mempool.
- **Outputs** — return values and the contents of confidential reads are encrypted back to the caller.

Clients trust that an enclave is genuine and running the expected code through **remote attestation** (see [TEE](/wiki/economics/finance/defi/tee#remote-attestation)). This is a fundamentally different privacy primitive from a [zero-knowledge proof](/wiki/cs/zero-knowledge-proofs): a ZKP proves a computation was done correctly while revealing nothing, whereas a TEE *performs* the computation privately inside sealed hardware. ZK gives you cryptographic soundness with no hardware trust; TEEs give you general-purpose private compute (any Solidity, no custom circuits) at the cost of trusting the chip vendor.

## The Confidential EVM in Practice

Most Solidity behaves identically to Ethereum — but confidentiality changes a few things you must design around:

- **State is private automatically.** A `private` or `internal` variable is genuinely unreadable on-chain, not merely un-exposed by the contract's application binary interface (ABI). (Note the inversion of Solidity's usual meaning, where `private` only blocks other *contracts*, not observers.)
- **View calls must be authenticated.** Because reads can return secrets, an `eth_call` that touches confidential state has to prove *who* is asking. Sapphire authenticates view calls with **[EIP](/wiki/economics/finance/defi/ethereum/eip)-712 signed queries**; the contract checks `msg.sender` and decides what to reveal. Practically, a confidential read may prompt a wallet signature.
- **Use the client wrapper.** The [`@oasisprotocol/sapphire-paratime`](https://www.npmjs.com/package/@oasisprotocol/sapphire-paratime) package wraps an EIP-1193 provider and transparently encrypts `eth_call`, `eth_estimateGas`, and `eth_signTransaction`. Framework-specific packages layer on top: `@oasisprotocol/sapphire-ethers-v6`, `@oasisprotocol/sapphire-viem-v2`, plus Hardhat and Wagmi integrations. Without the wrapper, transactions still execute but aren't end-to-end encrypted.
- **Confidential precompiles.** Sapphire adds [precompiled contracts](https://api.docs.oasis.io/sol/sapphire-contracts/contracts/Sapphire.sol/library.Sapphire.html) for secrets work: **secure on-chain randomness** (`Sapphire.randomBytes`, drawn from a per-block verifiable random function (VRF) seeded by enclave entropy rather than a manipulable block value), symmetric encryption/decryption, and key-pair generation and signing — so a contract can hold and use keys without ever exposing them.

A minimal port is often just: point your tooling at the Sapphire RPC, wrap the provider, and deploy. The confidentiality is in the runtime, not in your contract code.

## Network Facts

| Parameter | Mainnet | Testnet |
|---|---|---|
| Chain ID | `23294` (`0x5afe`) | `23295` (`0x5aff`) |
| RPC (HTTPS) | `https://sapphire.oasis.io` | `https://testnet.sapphire.oasis.io` |
| RPC (WebSocket) | `wss://sapphire.oasis.io/ws` | `wss://testnet.sapphire.oasis.io/ws` |
| Explorer | `https://explorer.oasis.io/mainnet/sapphire` | `https://explorer.oasis.io/testnet/sapphire` |
| Gas token | ROSE | TEST (faucet: `https://faucet.testnet.oasis.io/`) |

Block time is roughly 6 seconds and gas costs a fraction of a cent on typical workloads. Note that **Testnet state can be wiped**, and its confidentiality guarantees are weaker (experimental enclave configuration) — never treat Testnet as private for anything real.

## Limitations and Gotchas

Ordered roughly by how badly they can bite:

- **Confidentiality is strong, not absolute.** You are trusting Intel's hardware and attestation, and TEEs have a documented history of [side-channel attacks](/wiki/economics/finance/defi/tee#trust-model-and-limitations). Treat Sapphire as raising the cost of extraction enormously, not as information-theoretic privacy. Don't store something whose disclosure is catastrophic and irreversible without a second layer of defense.
- **Metadata still leaks.** Encryption hides argument and state *values*, but the existence of a transaction, which contract it calls, its gas usage, and storage *access patterns* are observable. A contract whose control flow branches on a secret can leak that secret through gas and access timing. Write secret-dependent paths to be constant-cost where it matters.
- **Randomness caveats.** `randomBytes` is excellent for confidentiality (an adversary can't predict it), but treat any in-contract randomness with care for high-value fairness — understand the enclave's threat model before relying on it for, say, a lottery.
- **Composability friction.** Sapphire is its own L1; it does not share liquidity or synchronous calls with Ethereum or other chains. Cross-chain interaction goes through bridges or the **Oasis Privacy Layer (OPL)**, which lets a contract on a transparent chain make confidential calls into Sapphire. That's power, but it's another moving part with its own latency and trust surface.

## Recent Developments

- **ROFL (Runtime Off-Chain Logic)** reached **mainnet in July 2025** (Oasis Core v24.2). ROFL extends Sapphire's TEE model *off-chain*: developers run verifiable, confidential compute units ("agents") inside enclaves that can talk to Sapphire contracts — well suited to trusted oracles, verifiable compute, and AI agents that must handle secrets. Oasis Core v24.3 added support for **Intel TDX**, moving beyond SGX to VM-level enclaves.
- The TDX support matters for Sapphire's longer-term trust story: Intel TDX (Trust Domain Extensions) confidential VMs are easier to provision and audit than SGX application enclaves, broadening the hardware base that confidential workloads can run on.

## External Links

- [Sapphire ParaTime — Oasis Documentation](https://docs.oasis.io/build/sapphire/) — the canonical developer docs
- [Network Information](https://docs.oasis.io/build/sapphire/network) — authoritative RPC, chain ID, and explorer details
- [sapphire-paratime on GitHub](https://github.com/oasisprotocol/sapphire-paratime) — clients, contracts, and examples
- [View-Call Authentication](https://docs.oasis.io/build/sapphire/develop/authentication/) — how signed queries work
- [Runtime Off-Chain Logic (ROFL)](https://docs.oasis.io/build/rofl/) — confidential off-chain compute
- [Get to Know Sapphire](https://oasis.net/blog/get-to-know-sapphire-the-industry-first-confidential-evm-paratime) — Oasis's own introduction

## Wiki Pages

{{< section >}}
