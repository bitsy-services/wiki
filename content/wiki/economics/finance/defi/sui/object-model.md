---
title: "The Object Model"
weight: 10
---

Sui's single most distinctive idea is that there are no accounts holding balances in the [Ethereum](/wiki/economics/finance/defi/ethereum/) sense. Everything on-chain — coins, [NFTs](/wiki/economics/finance/defi/nft), [AMM](/wiki/economics/finance/defi/amm) pools, published [smart contract](/wiki/economics/finance/defi/smart-contract) code, configuration — is a discrete, typed **object**. State is a graph of these objects rather than a global key-value store keyed by address. Understanding this model is the key to understanding why Sui can execute transactions in parallel and why its developers think about ownership the way they do.

## Objects vs. the Account Model

On Ethereum, a contract owns a slice of a single global storage trie. Your [ERC-20](/wiki/economics/finance/defi/ethereum/erc-20) balance is an entry in a mapping that lives inside the token contract's storage; "your" tokens are just a number the contract attributes to your address. Reading or writing that mapping touches shared contract state, so the protocol cannot know in advance whether two transactions will collide — it must execute them one after another to be safe.

Sui inverts this. A `Coin<SUI>` is itself an object that you hold directly. An NFT is an object. The data structures a DeFi protocol uses are objects. Each object is a self-contained, typed value defined in [Move](/wiki/economics/finance/defi/sui/sui-move), the resource-oriented language Sui inherits from the Diem project (and which it shares with [IOTA](/wiki/economics/finance/defi/iota/)).

Every object carries two pieces of identity-and-history metadata:

- A globally unique **object ID** — a 32-byte identifier (the `UID` field every Sui object must contain), assigned at creation and never reused.
- A **version** number, incremented every time the object is mutated. The combination of ID and version uniquely identifies one specific state of one specific object, giving every object an unambiguous, totally ordered history.

```move
public struct Sword has key {
    id: UID,        // the 32-byte object ID
    strength: u64,
}
```

## Three Kinds of Ownership

Ownership in Sui is explicit, tracked by the protocol, and falls into three categories. Which one you choose has direct consequences for latency and contention.

**Owned objects** are controlled by a single address — usually a wallet, but an object can also be owned by *another object* (parent/child relationships, "wrapping," and dynamic fields, discussed below). Only the owner can use an owned object as a transaction input. Because no one else can touch it, there is nothing to contend over and nothing to order globally. Transactions that read and write *only* owned objects can therefore skip [consensus](/wiki/economics/finance/defi/sui/consensus) entirely and finalize via Sui's "fast path" with very low latency. A simple payment or NFT transfer takes this route.

**Shared objects** are explicitly made shareable and can be accessed by any transaction. The canonical example is an AMM liquidity pool: everyone trades against the same pool object. Because multiple transactions may try to mutate a shared object in the same window, the protocol must agree on a global order for them — so any transaction touching a shared object goes through full consensus. This costs more latency than the fast path and exposes the object to contention when activity is high.

**Immutable objects** are frozen: once made immutable, an object can never be mutated or transferred again. Anyone can read it, and because it can't change, reads need no ordering at all. Published Move packages (deployed contract code) and on-chain configuration are typically immutable.

## Why This Enables Parallelism

The payoff is Sui's central scalability claim. A Sui transaction declares its inputs up front, so the protocol knows *before execution* exactly which objects each transaction will read and write. Two transactions whose object sets don't overlap cannot interfere with each other, so validators can run them at the same time on different cores. Throughput scales with available hardware instead of being capped by a single global execution lock. Owned-object transactions, with no shared state at all, are the extreme case: they need no agreement on ordering and finalize almost immediately.

This is also why owned vs. shared is a genuine design decision rather than a detail. Address-owned objects belong to a wallet; object-owned objects (children attached to a parent, or values stored under [dynamic fields](/wiki/economics/finance/defi/sui/programmable-transaction-blocks)) let you build large, mutable collections without making the whole thing a single shared bottleneck. Reaching for a shared object is sometimes unavoidable — shared liquidity, global counters, order books — but it opts you into consensus latency and into contention if many users hit the same object at once. A well-designed Sui protocol pushes as much state as possible onto the owned/fast path and reserves shared objects for the points where global agreement is genuinely required.

## External Links

- [Sui Concepts: Object Model](https://docs.sui.io/concepts/object-model)
- [Sui Developer Guide: Object Model](https://docs.sui.io/guides/developer/objects/object-model)
