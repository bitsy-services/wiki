---
title: "IPFS"
weight: 40
---

The **InterPlanetary File System (IPFS)** is a content-addressed peer-to-peer
storage network. You do not ask for a file by where it lives; you ask for it by
the hash of what it contains.

## Content addressing

A location address (`https://example.com/logo.png`) names a server and trusts it
to serve the right bytes. A content address — in IPFS a **CID**, or content
identifier — names the bytes themselves. Fetch a CID from any peer and you can
verify locally that you got what you asked for, because the hash either matches
or it doesn't.

Content addressing only reaches large or structured data because IPFS builds a
[Merkle DAG](/wiki/cs/dag) underneath it: files are chunked, each chunk hashed,
and the chunk hashes assembled into a tree whose root is the CID. One hash then
stands for an arbitrarily large object, and any part of it can be verified
without fetching the whole. Git's object store and
a [blockchain](/wiki/economics/finance/defi/blockchain) are the same idea with
different shapes, which is why the three keep turning up in the same
conversations.

The flip side is that content addressing makes updates awkward. Change one byte
and you have a different CID, so anything that needs a stable name for changing
content has to add a mutable pointer layer on top.

## Pinning is the catch

IPFS does not guarantee that anything stays available. **Pinning** is the act of
marking data in a node's datastore so that garbage collection will not discard
it; availability is the consequence, not the definition. A CID is retrievable
only while some peer has the data pinned and is willing to serve it, so an
unpinned file can quietly become unreachable while the CID remains perfectly
valid.

This is the most common misunderstanding about the network, and it is why "the
metadata is on IPFS" is a weaker promise than it sounds. Practically, pinning is
outsourced to a service, which reintroduces exactly the dependency the content
addressing was supposed to remove.

[Arweave](/wiki/economics/finance/defi/arweave) attacks the same problem from
the other end: pay once, and an endowment is meant to fund storage indefinitely.
That is a stronger commitment than pinning, but it is an economic forecast
rather than a guarantee — the Arweave page is explicit that "permanent" rests
on storage costs continuing to fall. The real distinction between the two is
who is on the hook for retention and for how long, not the hashing, which both
do the same way.

## `ipfs://` versus a gateway URL

The practical trap. A reference of the form `ipfs://<CID>` names content, and
any client that speaks the protocol can resolve it from any peer. A reference of
the form `https://ipfs.io/ipfs/<CID>` names *a host that will fetch that content
for you* — convenient, because every browser can follow it without extra
software, and exactly the single-point-of-failure the content addressing was
supposed to remove. If that gateway goes away, the link dies even though the
data is fine.

This is why an [NFT](/wiki/economics/finance/defi/nft) whose `tokenURI` is a
gateway URL is only nominally content-addressed.

## Where it shows up here

- [NFT](/wiki/economics/finance/defi/nft) metadata, where the `tokenURI` should
  be content-addressed so the issuer cannot swap what you own after the sale.
- [dApp](/wiki/economics/finance/defi/dapp) frontends, hosted so they cannot be
  taken down by pressuring one host.
- [ERC-8004](/wiki/economics/finance/defi/ethereum/erc-8004) agent registration
  files.

## External links

- [ipfs.tech](https://ipfs.tech/) — project site
- [IPFS documentation](https://docs.ipfs.tech/)
- [CID specification](https://github.com/multiformats/cid)
- [Wikipedia: InterPlanetary File System](https://en.wikipedia.org/wiki/InterPlanetary_File_System)
