---
title: "Arweave"
weight: 50
---

Arweave is a decentralized storage network built around a single unusual promise: pay once, store forever. Where most storage -- cloud buckets, [IPFS](/wiki/cs/ipfs) [pins](/wiki/cs/ipfs/pinning), traditional hosting -- charges recurring rent and deletes the data the moment payment stops, Arweave takes an upfront fee and commits to retaining it in perpetuity. The collection of data stored this way, served over HTTP through gateways, is marketed as the **permaweb**: a permanent, immutable layer of the web.

That promise is backed by an economic mechanism rather than a legal guarantee, and the mechanism is a bet on the price of storing a byte continuing to fall.

## The Endowment Model

The pay-once economics rest on a bet about the cost of storage. On upload, a portion of the fee covers the miners' immediate costs and the bulk is swept into a shared **storage endowment**. The endowment pays out to miners over time to compensate them for continuing to store old data.

The model assumes [Kryder's law](https://en.wikipedia.org/wiki/Mark_Kryder#Kryder's_law) holds: the cost of storing a byte falls year over year (historically ~30%+ annually, though Arweave models a deliberately conservative ~0.5%). If storage keeps getting cheaper, a fixed endowment denominated in real terms can fund storage indefinitely, because each future year of retention costs less than the last. The protocol prices uploads using a conservative cost projection so the endowment stays solvent even if the decline slows dramatically.

"Permanent" is therefore not a cryptographic guarantee like the immutability of a [blockchain](/wiki/economics/finance/defi/blockchain) record; it is a forecast that storage economics will keep behaving as they have for decades, and a sustained stall in Kryder's law shortens the endowment's runway directly.

## The Blockweave

Arweave does not use a conventional [blockchain](/wiki/economics/finance/defi/blockchain). Its data structure is the **blockweave**: each block links not only to the previous block (as in a normal chain) but also to a random earlier block, the *recall block*. To mine a new block, a miner must prove it has access to the data in that recall block.

That is **Proof of Access (PoA)**. In a normal [proof-of-work](/wiki/economics/finance/defi/blockchain) chain, miners are rewarded for spending energy; they have no incentive to retain old data. Arweave instead makes possession of historical data a precondition for mining. A miner that has discarded old blocks simply cannot answer the recall challenge and is excluded from rewards. Storage replication becomes a side effect of the consensus mechanism rather than an afterthought.

The mechanism has evolved through several iterations:

- **PoA (original)** -- prove access to a single randomly chosen recall block.
- **SPoRA** (Succinct Proof of Random Access) -- ties hashing speed to the miner's ability to read random chunks from disk, so raw compute can't substitute for actually storing data.
- **The 2.6+ mechanism** -- caps the hash rate per stored partition, which flattens the economics so that holding a complete, well-replicated copy of the dataset beats throwing GPUs at the problem. The intent is to push the network toward many full replicas rather than a few large miners.

The throughput goal is not transactions-per-second in the [DeFi](/wiki/economics/finance/defi/) sense; it is durably replicated bytes. The recall-block structure makes the blockweave a kind of graph rather than a strict linear chain, distinct from the transaction [DAG](/wiki/cs/dag/) designs used by ledgers like [IOTA's Tangle](/wiki/economics/finance/defi/iota/tangle).

## Transactions, Bundling, and Gateways

Data on Arweave is content-addressed: every transaction has an ID derived from its contents, and that ID is the permanent address of the data. This is the same content-addressing principle behind Git objects and IPFS, and it means a stored object cannot be silently altered without changing its address.

Two layers make this usable in practice:

- **Bundling (ANS-104).** Writing one Arweave transaction per file is slow and wasteful. The ANS-104 standard packs many independent *data items* -- each individually signed and individually addressable -- into a single base-layer transaction. Bundling services (Irys, formerly Bundlr) let an application upload thousands of items cheaply, often paying in other tokens and settling to Arweave behind the scenes. This is what makes high-volume uploads ([NFT](/wiki/economics/finance/defi/nft) media, social posts) economical.
- **Gateways.** End users do not run Arweave nodes. A gateway such as `arweave.net` indexes the network, resolves transaction IDs, serves data over plain HTTPS, and exposes a GraphQL endpoint for querying transaction metadata and tags. A URL like `https://arweave.net/<tx-id>` is how the permaweb is actually consumed. Gateways are a convenience and a point of centralization -- the data lives on the network, but most reads flow through a handful of gateways.

**ArNS** (the Arweave Name System) adds human-readable names that resolve to permaweb content, the permanent-storage analogue of the [Ethereum Name Service](https://ens.domains) (ENS) for [Ethereum](/wiki/economics/finance/defi/ethereum/).

## The AR Token

[AR](https://www.arweave.org) is the network's native [cryptocurrency](/wiki/economics/finance/defi/cryptocurrency). It pays for storage and rewards miners, with the endowment denominated in AR. Supply is capped: roughly 55 million tokens existed at genesis, with up to ~11 million more released as block rewards, for a maximum of about 66 million AR. Storage demand drives token demand, and the endowment locks tokens up over long horizons, so the design couples the token's value to network usage. The market has not always priced it that way.

## AO: Compute on Top of Storage

Arweave stores data but does not, by itself, run programs. **AO** (short for "Actor Oriented") is a decentralized compute layer launched on top of Arweave that aims to be a "hyper-parallel computer." Processes communicate by passing messages -- an [actor model](/wiki/cs/entity-addressing/actor-model) design -- and write their state and message logs to Arweave for permanence and verifiability. The split is deliberate: Arweave provides the durable, ordered data layer, and AO provides computation over it, much as [smart contracts](/wiki/economics/finance/defi/smart-contract) provide computation over a blockchain's ledger.

## Arweave vs. IPFS and Filecoin

These are frequently confused because all three are "decentralized storage," but they make different promises:

| | Persistence model | Payment | Guarantees |
|---|---|---|---|
| **Arweave** | Pay once, stored permanently | Upfront, into an endowment | Economic bet on permanence |
| **[IPFS](https://ipfs.tech)** | Data persists only while *pinned* by some node | Free protocol; you pay whoever pins | None -- unpinned data is garbage-collected |
| **[Filecoin](/wiki/economics/finance/defi/filecoin)** | Storage *deals* for a fixed term | Recurring, per deal | Cryptographic proofs for the deal's duration |

IPFS is purely an addressing and transfer protocol with no built-in incentive to keep data alive; Filecoin adds a market for time-bounded storage deals that must be renewed. Arweave is the only one of the three whose core value proposition is *indefinite* retention without renewal. The trade-off is that Arweave's permanence is an economic projection, while a Filecoin deal's term is contractually and cryptographically bounded.

## Use Cases

- **Permanent web hosting** -- static sites, [dapp](/wiki/economics/finance/defi/dapp) frontends, and documentation deployed to the permaweb so they survive the company that built them.
- **NFT and on-chain media** -- storing the actual image/metadata an NFT points to, avoiding the notorious problem of NFTs whose media lived on a server that later went dark.
- **Archival** -- journalism, public records, and datasets where censorship-resistance and tamper-evidence matter.
- **Verifiable application state** -- AO processes and other systems that need an auditable, permanent log.

## Trade-offs and Criticisms

Ordered by what actually bites:

- **Permanence is a forecast, not a guarantee.** The whole system rests on Kryder's-law economics. A long stall in falling storage costs, or a collapse in the AR token's value relative to real storage costs, would stress the endowment. "Forever" is a well-engineered probabilistic claim, not a certainty.
- **Immutable means immutable -- including the things you regret.** Permanent, uncensorable storage means illegal, harmful, or simply mistaken content cannot be removed. Gateways can refuse to *serve* specific content (content moderation at the edge), but the data remains on the network. This is a feature for censorship resistance and a serious liability everywhere else.
- **Gateway centralization.** Although storage is decentralized, the practical reading experience funnels through a few gateways. An application that hardcodes `arweave.net` has reintroduced a single point of failure.
- **Write-once is unforgiving.** There is no edit and no delete. Versioning must be modeled explicitly (new transactions referencing old ones), and an accidental upload of secrets or personal data is permanent.

## External Links

- [Arweave](https://www.arweave.org) -- official site
- [The Arweave Yellow Paper](https://www.arweave.org/yellow-paper.pdf) -- protocol and endowment mechanics
- [ar.io](https://ar.io) -- gateway network and ArNS
- [AO](https://ao.arweave.dev) -- the compute layer
- [Wikipedia: Kryder's law](https://en.wikipedia.org/wiki/Mark_Kryder#Kryder's_law)
- [IPFS](https://ipfs.tech) and [Filecoin](https://filecoin.io) -- the main alternatives
