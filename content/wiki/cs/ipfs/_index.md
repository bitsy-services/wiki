---
title: "IPFS"
weight: 40
bookCollapseSection: true
---

The **InterPlanetary File System (IPFS)** is a content-addressed peer-to-peer
storage network. A file is named not by where it lives but by the hash of what
it contains, so the name is verifiable and the location is negotiable.

## Content addressing

A location address (`https://example.com/logo.png`) names a server and trusts it
to serve the right bytes. A content address — in IPFS a
[content identifier (CID)](/wiki/cs/ipfs/cid) — names the bytes themselves. A
CID fetched from any peer can be verified locally, because the bytes that arrive
either hash to that CID or they do not. A peer that lies is detected by the
client that asked, without a signature, a certificate, or a reputation system.

Content addressing only reaches large or structured data because IPFS builds a
[Merkle DAG](/wiki/cs/dag) underneath it: files are chunked, each chunk hashed,
and the chunk hashes assembled into a tree whose root is the CID.
[UnixFS](/wiki/cs/ipfs/unixfs) is the layout that does it. One hash then stands
for an arbitrarily large object, and any part of it can be verified without
fetching the whole. Git's object store and
a [blockchain](/wiki/economics/finance/defi/blockchain) are the same idea with
different shapes, which is why the three keep turning up in the same
conversations.

Change one byte and the CID changes, so anything that needs a stable name for
changing content adds a mutable pointer layer on top —
[IPNS or DNSLink](/wiki/cs/ipfs/ipns-and-dnslink).

## What the protocol guarantees

IPFS guarantees that a CID identifies exactly one sequence of bytes. It
guarantees nothing about whether those bytes are anywhere.

Retrieval needs two separate things to be true at once: some peer still holds
the blocks, and the network can still find that peer. The first is
[pinning](/wiki/cs/ipfs/pinning), which marks blocks so a node's garbage
collector will not reclaim them. The second is
[content routing](/wiki/cs/ipfs/content-routing), where a provider record
expires after 48 hours and has to be republished. A node that stops paying
attention to either one leaves a CID that is still perfectly valid and no longer
resolves.

"The metadata is on IPFS" therefore promises only that the bytes hash to that
CID, not that anyone is still holding them.

## The pieces

| Layer | What it decides | Page |
|---|---|---|
| Content identifier | how a hash is written down and what it self-describes | [CID](/wiki/cs/ipfs/cid) |
| File layout | how bytes become blocks and blocks become a tree | [UnixFS](/wiki/cs/ipfs/unixfs) |
| Routing and transfer | who has a block, and how it gets to you | [Content routing](/wiki/cs/ipfs/content-routing) |
| Mutability | how a stable name points at changing content | [IPNS and DNSLink](/wiki/cs/ipfs/ipns-and-dnslink) |
| Retention | who keeps the blocks and for how long | [Pinning](/wiki/cs/ipfs/pinning) |
| HTTP access | how a browser that speaks none of this reads it anyway | [Gateways](/wiki/cs/ipfs/gateways) |

## Neighbours in the same problem space

[Arweave](/wiki/economics/finance/defi/arweave) attacks retention from the other
end: pay once, and an endowment is meant to fund storage indefinitely. That is a
stronger commitment than pinning, but it is an economic forecast rather than a
guarantee — the Arweave page is explicit that "permanent" rests on storage costs
continuing to fall. [Filecoin](/wiki/economics/finance/defi/filecoin) keeps
IPFS's addressing and adds a market where storage is a dated contract backed by
proofs. [Walrus](/wiki/economics/finance/defi/sui/walrus) erasure-codes blobs
across a staked node set and settles the bookkeeping on Sui.

All four hash the same way. What separates them is who is on the hook for
retention, for how long, and whether anyone can check.

## Where it shows up here

- [NFT](/wiki/economics/finance/defi/nft) metadata, where the `tokenURI` should
  be content-addressed so the issuer cannot swap the referenced asset after the
  sale.
- [dApp](/wiki/economics/finance/defi/dapp) frontends, hosted so they cannot be
  taken down by pressuring one host.
- [Token lists](/wiki/economics/finance/defi/token-registration/token-lists),
  published under an Ethereum Name Service (ENS) `contenthash` record so the
  name is stable and the list underneath it is not.
- [ERC-8004](/wiki/economics/finance/defi/ethereum/erc-8004) agent registration
  files.

## External links

- [ipfs.tech](https://ipfs.tech/) — project site
- [IPFS documentation](https://docs.ipfs.tech/)
- [IPFS specifications](https://specs.ipfs.tech/)
- [Wikipedia: InterPlanetary File System](https://en.wikipedia.org/wiki/InterPlanetary_File_System)

## Wiki Pages

{{< section >}}
