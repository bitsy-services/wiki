---
title: "The Graph"
weight: 30
bookCollapseSection: true
---

[The Graph](https://thegraph.com/) is a decentralised indexing protocol for querying blockchain data. Instead of running your own indexing server, you publish a **subgraph** — a schema plus mapping functions — and The Graph Network indexes the chain events for you, exposing the result through a [GraphQL](https://en.wikipedia.org/wiki/GraphQL) API.

Most DeFi front-ends rely on The Graph (or a comparable indexer) because reading historical or aggregated data directly from an [RPC node](https://en.wikipedia.org/wiki/Remote_procedure_call) is impractically slow.

## Core Concepts

| Concept | Description |
|---|---|
| **Subgraph** | A package that tells indexers *what* contract events to watch and *how* to transform them into queryable entities. Defined by a manifest (`subgraph.yaml`), a GraphQL schema, and AssemblyScript mapping handlers. |
| **Indexer** | A node operator that stakes [GRT](https://thegraph.com/docs/en/tokenomics/) tokens and indexes subgraphs in exchange for query fees and indexing rewards. |
| **Curator** | A participant who signals on subgraphs with GRT to indicate data quality, helping indexers decide what to index. |
| **Delegator** | A GRT holder who stakes to an indexer without running infrastructure, earning a share of rewards. |
| **Gateway** | The entry point for queries; routes requests to indexers and handles payment. |

## Subgraph Studio vs. Hosted Service

The legacy **Hosted Service** was deprecated in favour of the decentralised network and **Subgraph Studio**:

| | Hosted Service (deprecated) | Subgraph Studio / Network |
|---|---|---|
| **Operator** | Edge & Node (centralised) | Decentralised indexer network |
| **Cost** | Free | Query fees paid in GRT |
| **Chains** | Many EVM + non-EVM | Expanding; see [supported networks](https://thegraph.com/docs/en/developing/supported-networks/) |
| **Reliability** | Single point of failure | Redundant indexers |

New subgraphs should target **Subgraph Studio** and the decentralised network.

## Protocol Network: Arbitrum One

The Graph's protocol contracts — staking, curation, query fee billing, and indexing rewards — migrated from Ethereum mainnet to [Arbitrum One](https://en.wikipedia.org/wiki/Arbitrum) in 2024 to reduce gas costs. All new subgraphs are published on Arbitrum.

The [Graph Explorer](https://thegraph.com/explorer) reflects this with a network selector: **Arbitrum One** (active) and **Ethereum (deprecated)**. The Ethereum view is read-only for legacy subgraphs that have not yet migrated.

This is distinct from the *data source chain* a subgraph indexes — a subgraph registered on Arbitrum can still index Ethereum mainnet, Polygon, or any other [supported network](https://thegraph.com/docs/en/developing/supported-networks/).

## Tips and Gotchas

- **Indexing lag** — subgraphs trail the chain tip by a few blocks. Do not rely on them for data that must be real-time (use contract reads or event listeners instead).
- **Re-orgs** — indexers handle short re-orgs automatically, but deep re-orgs can cause temporary data inconsistencies.
- **Rate limits** — the decentralised gateway charges per query. Cache aggressively on your backend to control costs.
- **Schema migrations** — changing entity fields requires a new deployment and a full re-index. Plan your schema carefully before going to production.
- **Start block** — always set `startBlock` in `subgraph.yaml` to the contract's deployment block. Omitting it forces indexers to scan from genesis, massively slowing deployment.

## Resources

- [The Graph Documentation](https://thegraph.com/docs/)
- [Subgraph Studio](https://thegraph.com/studio/)
- [Graph Explorer](https://thegraph.com/explorer) — browse and query published subgraphs
- [GraphQL Playground](https://thegraph.com/docs/en/querying/graphql-api/) — API reference for subgraph queries

## Wiki Pages

{{< section >}}
