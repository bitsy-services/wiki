---
title: Prediction Market Event Time
weight: 46
---

**Event time** is the moment a [prediction market](/wiki/economics/finance/defi/prediction-market) determines its outcome. It governs when trading stops, when resolution begins, and when winning shares become redeemable. Getting event time right is one of the hardest design problems in on-chain prediction markets because it sits at the intersection of real-world timing, [oracle](/wiki/economics/finance/defi/oracle-node) reliability, and [smart contract](/wiki/economics/finance/defi/smart-contract) mechanics.

## Resolution Lifecycle

A typical on-chain prediction market moves through several time-bound phases:

1. **Trading period** -- the market is open and participants buy and sell outcome shares. This phase ends at a predefined cutoff, which may or may not coincide with the real-world event.
2. **Observation window** -- the event occurs (or fails to occur). The market waits for the outcome to become publicly verifiable.
3. **Resolution** -- an [oracle](/wiki/economics/finance/defi/oracle-node) or designated resolver submits the outcome on-chain. The smart contract transitions the market to a settled state.
4. **Redemption** -- holders of winning shares claim their payout.

The boundaries between these phases are defined by timestamps or block numbers encoded in the market's smart contract.

## Early Resolution

Some events resolve before the scheduled end time -- an election might be called early, or a sports match might end in a forfeit. Markets that only support resolution at a fixed timestamp force participants to wait even when the outcome is already known, locking up capital unnecessarily.

Protocols handle early resolution in different ways:

- **Optimistic resolution** -- anyone can propose the outcome before the deadline. If no one disputes the proposal within a challenge window, it is accepted. Polymarket and UMA's optimistic oracle use this pattern.
- **Multi-round oracle** -- a decentralized oracle network votes on the outcome, and successive rounds of dispute resolution can overturn earlier decisions. Augur's dispute-round system is the canonical example.
- **Trusted resolver** -- a single designated address (often a multisig or [DAO](/wiki/economics/finance/defi/dao)) can resolve the market at any time. Simpler but introduces centralization risk.

## Invalid Markets and Edge Cases

Not every event resolves cleanly. Markets must define what happens when:

- **The event does not occur** -- a scheduled fight is canceled, a product launch is postponed indefinitely. Most protocols define an "Invalid" outcome that returns funds to participants proportionally.
- **The outcome is ambiguous** -- the resolution criteria were not specific enough, or multiple interpretations are defensible. Well-designed markets invest heavily in precise resolution rules up front to minimize this risk.
- **The oracle fails** -- the data source is unavailable, compromised, or reports contradictory data. Fallback mechanisms (secondary oracles, governance votes, manual override) are essential.

## Time Zone and Timestamp Pitfalls

On-chain timestamps come from block producers and are only approximately accurate. Ethereum's block timestamps, for example, must be greater than the parent block's timestamp but can drift from wall-clock time by several seconds. For markets that resolve around a precise real-world moment (the closing bell of a stock exchange, midnight UTC on election day), this imprecision matters.

Best practices include:

- Using **block number** rather than timestamp when precision is critical and the chain's block time is predictable.
- Building in a **grace period** between the event and resolution to absorb timing jitter and oracle latency.
- Specifying all times in **UTC** and defining the resolution source unambiguously in the market's metadata.
