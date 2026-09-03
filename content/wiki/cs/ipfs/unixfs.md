---
title: "UnixFS and Chunking"
weight: 20
---

A hash names one block. A film does not fit in one block, and neither does a
directory of ten thousand files. **UnixFS** is the layout that turns files and
directories into a [Merkle DAG](/wiki/cs/dag) of blocks, and it is the reason
[IPFS](/wiki/cs/ipfs) can hand out a single
[content identifier (CID)](/wiki/cs/ipfs/cid) for something far larger than
anything it moves in one piece.

## The chunker

Import starts by cutting the byte stream into chunks. Kubo's default is
`size-262144` — fixed 256 KiB pieces, cut at offsets that ignore the content
entirely.

Fixed-size chunking is fast and has one bad property: insert a byte at the front
of a file and every subsequent boundary shifts, so every chunk downstream of the
edit hashes differently and nothing is shared with the previous version. Two
content-defined alternatives cut on a rolling hash of the last few dozen bytes
instead, so a boundary lands in the same place regardless of what happened
earlier in the file:

```bash
ipfs add --chunker=rabin-262144-524288-1048576 large.tar   # min-avg-max
ipfs add --chunker=buzhash                                  # faster, fixed params
```

The cost is import time — both are slower than cutting at fixed offsets, rabin
markedly so — and a CID that nobody else will reproduce unless they use the same
chunker. Fixed-size stays the default because most content is written once, and
deduplication against an earlier revision only pays when there is an earlier
revision.

## The tree

Chunks become leaves; leaves are gathered under parent nodes; parents are
gathered under their own parents until one node is left. That root is the file's
CID.

The default builder is *balanced* and puts 174 links in each node. The number is
not tuned to anything about files — it falls out of a size estimate in
go-unixfs:

```text
roughLinkSize      = 34 + 8 + 5   ≈ 47 bytes   (multihash + size field + framing)
roughLinkBlockSize = 8192                       (8 KiB of links per node)
DefaultLinksPerBlock = 8192 / 47  = 174
```

A root over 174 interior nodes over 174 leaves of 256 KiB each already covers
7.4 GiB, so almost every real file is three levels deep or fewer. `--trickle`
selects the other builder, which biases the tree so that early bytes are
reachable after fetching fewer blocks — worth it for media a player starts
consuming before the download finishes.

## Directories

A directory is a `dag-pb` node whose links carry names. Reading
`/ipfs/<cid>/docs/readme.md` means fetching the root node, finding the link
named `docs`, fetching that node, finding `readme.md`, and fetching what it
points at — one round trip per path segment, which is why deep paths on a cold
node feel slow.

Directories big enough to overflow a block are sharded into a hash array mapped
trie (HAMT) with a fanout of 256, splitting the entries across many nodes so no
single block has to hold them all. The switch happens automatically above a
256 KiB threshold, and it changes the CID of the directory — the same entries
listed under the sharded and unsharded layouts are different DAGs.

## Raw leaves

With `--raw-leaves` (implied by `--cid-version=1`), leaf blocks are stored under
the `raw` codec instead of being wrapped in a protobuf node. Two consequences
follow. The leaf's CID becomes the hash of the file bytes themselves, so a
64 KiB file has a CID you can verify with `sha256sum` and a base32 encoder. And
the protobuf framing disappears from every leaf, which for a file of many small
chunks is a measurable saving.

It also changes every leaf hash and therefore the root, which is why the flag is
not the default: a decade of published `Qm` strings were minted without it.

## Blocks are the unit of everything

The block, not the file, is what gets requested, transferred, verified, cached,
and pinned. Three behaviours follow directly:

- **Deduplication is automatic and invisible.** Two files sharing a 256 KiB run,
  cut at the same boundaries, share the block. Storage is charged once.
- **Verification is incremental.** A client fetching block 400 of a film checks
  it against the CID in its parent node, which it checked against *its* parent,
  up to a root the client was given out of band. No block is trusted on the
  strength of who sent it.
- **Partial reads are cheap.** An HTTP range request over a
  [gateway](/wiki/cs/ipfs/gateways) turns into fetches of the specific subtree
  covering that byte range rather than a download of the whole object, which is
  what makes seeking in a large file over IPFS work at all.

## External links

- [UnixFS specification](https://specs.ipfs.tech/unixfs/)
- [ipfs/boxo](https://github.com/ipfs/boxo) — the Go implementation of the importers and DAG builders
- [IPFS docs: merkle DAGs](https://docs.ipfs.tech/concepts/merkle-dag/)
- [Kubo `ipfs add` reference](https://docs.ipfs.tech/reference/kubo/cli/#ipfs-add)
