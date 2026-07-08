---
title: "Gas & Storage"
weight: 50
---

Sui prices a transaction with two meters, not one. Every transaction pays a **computation fee** for the work the validators do, and a **storage fee** for the bytes it leaves behind on-chain. The two are quoted, accrued, and reasoned about independently. This is the first thing that surprises anyone arriving from [Ethereum](/wiki/defi/ethereum/), where a single gas market bundles execution and state growth into one volatile per-unit price set by an auction. Sui unbundles them deliberately, because the cost of running a computation now and the cost of storing data forever are genuinely different economic problems.

## The Two Components

A transaction's total fee is:

```text
fee = (computation units × reference gas price) + (storage bytes × storage price)
```

**Computation** is metered in abstract computation units — roughly, the amount of work the VM does — multiplied by the **reference gas price** (below). **Storage** is metered in bytes of on-chain state the transaction creates, multiplied by a separate storage price. Because storage is charged per byte of [object](/wiki/defi/sui/object-model) data and Sui's state is a graph of discrete objects rather than a single account trie, the storage cost of a transaction is a direct function of how much object data it adds.

## Reference Gas Price

The **reference gas price (RGP)** is the floor price for computation, and it is fixed for an entire epoch. It is not discovered by a per-block fee auction. Instead, at each epoch boundary the protocol runs a *gas price survey*: every [validator](/wiki/defi/sui/consensus) submits the minimum price at which it commits to promptly process transactions, the protocol sorts those quotes, and picks the price at roughly the 2/3 percentile *weighted by stake*. That value becomes the RGP a quorum of stake has agreed to honor for the epoch.

Two incentives keep this honest. A *tallying rule* lets validators score each other on whether they actually processed transactions at the agreed price, and end-of-epoch [staking](/wiki/defi/staking) rewards are nudged by those scores — so quoting a low price and then not honoring it costs you rewards. The result is a stable, predictable price set by the people doing the work, rather than users bidding against each other in a fee market.

Users submit a *gas price* with each transaction. As long as it is at or above the RGP, the transaction is processed; setting it higher is a tip that can buy priority under congestion, but in practice this is rarely necessary. Storage price is set separately through governance and changes infrequently, tracking the off-chain dollar cost of storage.

## The Storage Fund

Here is the structural difference from most chains. Storage fees are **not** paid out to the current validators who happen to process the transaction. They are escrowed in a protocol-managed **storage fund**.

The fund exists to solve a timing mismatch: data written today must be stored by validators for years, but the validator set that stores it in 2030 is not the one that collected the fee in 2026. Rather than paying current validators for future work, the fund holds the deposit and contributes it as stake-like principal to the staking rewards pool. Its "earnings" are redirected to whichever validators are securing the network in each future epoch, compensating them for the ongoing cost of retaining that state. Whoever is storing your data is being paid to do so, indefinitely.

## Storage Rebates

The storage deposit is refundable. When an object is deleted — or shrunk — most of its original storage fee is returned to the transaction sender as a **storage rebate**. Currently the rebate is **99%** of the originally paid storage fee; the remaining **1%** is non-refundable and stays in the fund permanently.

This makes the *net* storage cost of an application reflect the *net* data it leaves on-chain. Cleaning up state you no longer need is rewarded, not punished, which is the opposite of the implicit incentive on chains where freeing storage is at best a modest one-time refund. A common pattern in [Move](/wiki/defi/sui/sui-move) code is to delete objects when they are consumed precisely to recover this deposit.

## Deflationary Effect

SUI's total supply is hard-capped at 10 billion. The non-refundable 1% of every storage fee accumulates in the storage fund and is effectively removed from circulation. As on-chain data grows over the life of the network, the fund grows with it, so a rising amount of SUI sits locked behind stored state — a structural deflationary pressure tied directly to adoption rather than to any discretionary burn.

## Paying for Gas in Practice

Gas on Sui is paid from SUI coin objects you own. A transaction can designate multiple gas coins, and a [Programmable Transaction Block](/wiki/defi/sui/programmable-transaction-blocks) can merge several SUI coins into the gas payment, so you are not blocked by having your balance split across many small coins. Because owned-object transactions take Sui's fast path and skip [consensus](/wiki/defi/sui/consensus), there is also no ordering auction to bid into. In day-to-day use a transaction costs a fraction of a US cent, and the computation/storage split keeps that cost stable across market conditions.

## External Links

- [Gas in Sui](https://docs.sui.io/concepts/tokenomics/gas-in-sui) — the two-component fee model
- [Gas Pricing](https://docs.sui.io/concepts/tokenomics/gas-pricing) — the reference gas price survey and tallying rule
- [Storage Fund](https://docs.sui.io/concepts/tokenomics/storage-fund) — escrow, rebates, and the deflationary mechanism
