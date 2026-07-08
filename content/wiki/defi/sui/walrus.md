---
title: "Walrus"
weight: 70
---

Walrus is Mysten Labs' decentralized blob-storage network, built to give [Sui](/wiki/defi/sui/) applications a place to put large data that no [blockchain](/wiki/defi/blockchain) is designed to hold. It went to mainnet on **March 27, 2025**, alongside its native **WAL** token, and forms the storage leg of Sui's emerging privacy-and-data stack.

## The Problem

On-chain state is expensive precisely because every validator stores and re-executes against it. Sui's [storage fund](/wiki/defi/sui/gas-and-storage) is engineered for *small* state — owned [objects](/wiki/defi/sui/object-model), balances, contract data — and prices it accordingly: every validator keeps a full copy forever. Putting megabytes of media, datasets, NFT artwork, website front-ends, AI model weights, or data-availability blobs through that mechanism is economically absurd.

Walrus splits the concern. The bulk bytes of a **blob** live *off-chain*, distributed across an open network of storage nodes, while the things you actually want a chain for — metadata, proof of availability, payment, and access control — are coordinated *on Sui*. The result is large-data storage at roughly cloud-like cost without surrendering decentralization or programmability.

## Erasure Coding: Red Stuff

The naive way to make off-chain data durable is full replication: store N copies so the loss of a few nodes doesn't lose the data. That costs a replication factor in the hundreds to tolerate a meaningful fraction of Byzantine or offline nodes.

Walrus instead uses **Red Stuff**, a novel two-dimensional erasure-coding scheme. A blob is encoded into many **slivers** that are spread across the storage nodes; the original blob can be reconstructed from any sufficiently large *subset* of those slivers — Walrus tolerates up to two-thirds of slivers being missing or held by faulty nodes. This buys Byzantine fault tolerance across the storage set while keeping the replication factor down to roughly **4x-5x**, comparable to a centralized cloud provider rather than to full-replication networks.

The two-dimensional structure is what makes Red Stuff distinctive. It enables efficient *recovery*: when nodes churn in or out — which they do constantly in an open, staked network — a node can reconstruct its share of a blob by pulling a small amount of data from peers, rather than re-downloading the whole object. That recovery cost is the practical bottleneck for most decentralized storage designs, and is where Walrus claims its main advantage.

## On-Chain Coordination

Every stored blob is represented by a Sui [object](/wiki/defi/sui/object-model). Storage is *purchased* up front for a chosen number of epochs, and the blob's availability is provable on-chain: a smart contract can check that a given blob is registered and still within its paid lifetime.

Because the handle to a blob is a first-class Sui object, blobs become **programmable**. A contract can reference one, gate access to it, transfer ownership of it, or make a blob's continued availability a condition of some on-chain logic — none of which is possible when your data sits in an opaque off-chain bucket.

## The WAL Token

WAL is the network's native token, with a total supply of **5 billion**. It serves two roles:

- **Payment.** Storage is paid for in WAL. Rather than being collected up front by the network, payments are streamed out to the storage nodes over the storage period, aligning node revenue with the service actually rendered.
- **Staking.** Walrus runs a delegated proof-of-stake system for its storage network: WAL holders stake or delegate to storage nodes, and stake weight governs node selection and influence, mirroring how [SUI staking](/wiki/defi/staking) secures Sui's validators.

Walrus was backed by a roughly **$140M** token sale led by Standard Crypto and a16z crypto, with participation from Franklin Templeton and others.

## Use Cases

- **NFT and media storage** — the asset itself lives on Walrus while the NFT object on Sui holds the verifiable pointer, replacing the centralized URLs that quietly undermine most "on-chain" NFTs.
- **Fully on-chain front-ends** — websites and [dApp](/wiki/defi/dapp) UIs served directly from Walrus, removing the centralized hosting dependency.
- **Data availability** — publishing DA blobs that other chains or rollups can prove are retrievable.
- **AI datasets and models** — large, verifiable, content-addressed data for training and inference.
- **Privacy stack** — Walrus is the storage leg of Sui's confidential-computing direction, pairing with **Seal** (threshold encryption) and **Nautilus** (verifiable [TEE](/wiki/defi/tee) compute) for confidential-but-auditable applications.

## Limitations

- **Blobs are public by default.** Anything you store is readable by anyone unless you encrypt it before upload (e.g. via Seal). Treat Walrus as a public bulk store, not a private one.
- **Availability is only guaranteed for the paid period.** Storage is bought for a fixed number of epochs; once that lapses, the network is under no obligation to retain the blob. Durable storage means actively keeping it funded.

## External Links

- [Walrus](https://www.walrus.xyz/) — official site
- [Walrus Documentation](https://docs.walrus.site/) — developer docs
- [Walrus Whitepaper](https://docs.walrus.site/walrus.pdf) — Red Stuff encoding and protocol design
