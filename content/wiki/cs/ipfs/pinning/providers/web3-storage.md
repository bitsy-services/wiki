---
title: "web3.storage and Storacha"
weight: 80
---

This entry is a lineage rather than a live option. One service was renamed twice
and re-architected each time, dropping a little more of its
[IPFS](/wiki/cs/ipfs) surface at every step, and the names are still all over
old code and documentation.

```text
web3.storage      →   Storacha        →   Fil One
Pinning Service       own client,         S3-compatible object
API, then not         capability auth     storage for AI workloads
```

## What each generation was

**web3.storage** was Protocol Labs' free-tier upload service: post a file, get a
[content identifier (CID)](/wiki/cs/ipfs/cid), with
[Filecoin](/wiki/economics/finance/defi/filecoin) deals behind it. It
implemented the vendor-agnostic
[Pinning Service API](/wiki/cs/ipfs/pinning/pinning-service-api), and then
withdrew that interface — the first step away from portability.

**Storacha** rebuilt it as a hot-storage layer over Filecoin, with two ideas
worth recording because they show up elsewhere. Authority came from user
controlled authorization network (UCAN) tokens: capability tokens signed by a
keypair, delegatable to other keys, and verifiable without asking a server who
owns what, with a **space** identified by a decentralized identifier standing in
for a bucket. And the upload client chunked and hashed locally, so the root CID
was known before any bytes left the machine — the opposite of the
[upload-and-accept-what-comes-back](/wiki/cs/ipfs/pinning/pinning-services#two-ways-to-hand-data-over)
trap, and a genuinely better arrangement for anything whose CID has to go into a
contract.

**Fil One** is what `storacha.network` now redirects to. It is S3-compatible
object storage on Filecoin aimed at AI workloads, authenticated with an access
key and secret. Its documentation does not mention IPFS, CIDs, UCANs, or spaces.

## What this means for anything pointing at it

Content stored under the earlier generations was content-addressed, so the CIDs
remain valid names for the same bytes. Whether anything still serves them is a
separate question, and it is the question the whole of this section is about: a
CID outlives the company, and retrieval does not.

Code written against the web3.storage client, the `w3up` protocol, or a
`https://*.storacha.network` endpoint needs repointing at something that still
exists. Anything that needs IPFS retrievability needs a different provider
entirely, because the surviving product does not offer it.

`nft.storage`, the sibling service aimed at
[NFT](/wiki/economics/finance/defi/nft) metadata, went the same way on its own
schedule: Classic uploads were decommissioned on 30 June 2024 with retrieval
kept alive.

## External links

- [fil.one](https://fil.one/) — the current product
- [storacha/upload-service](https://github.com/storacha/upload-service) — the maintained implementation of the Storacha-era protocol
- [nft.storage Classic](https://classic.nft.storage/) — retrieval-only since 2024
