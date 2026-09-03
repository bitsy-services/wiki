---
title: "Pinning"
weight: 60
bookCollapseSection: true
---

**Pinning** marks blocks in a node's datastore so that garbage collection will
not reclaim them. That is the whole definition, and it is narrower than the way
the word is used: pinning is a local storage-retention flag, not a promise about
availability, not a network operation, and not something any other node can
observe.

Everything a [content identifier (CID)](/wiki/cs/ipfs/cid) fails to deliver in
practice traces back to this. [IPFS](/wiki/cs/ipfs) has no protocol-level
incentive for anyone to keep anyone else's blocks, so retention is arranged
outside the protocol — by running a node, or by paying somebody who does.

## What a node stores, and for how long

A Kubo datastore holds three kinds of block:

| Kind | How it got there | Survives garbage collection |
|---|---|---|
| Pinned | `ipfs add`, `ipfs pin add` | yes |
| In the mutable file system | `ipfs files cp` | yes, implicitly |
| Cached | fetched to satisfy a read | no |

The third row is where most surprises live. Fetching a CID through a local node
leaves the blocks in the datastore, so the content reads back instantly and
looks stored. It is cache. The next sweep removes it.

## Pin types

```bash
ipfs pin add <cid>              # recursive: this block and every descendant
ipfs pin add --recursive=false <cid>   # direct: this block only
ipfs pin ls --type=indirect     # reachable from a recursive pin
```

**Recursive** is the default and the one that means what people expect: pin a
file's root and the whole [Merkle DAG](/wiki/cs/dag) under it is retained.
**Direct** pins exactly one block and nothing it links to, which retains a
directory listing while letting its contents be collected. **Indirect** is not a
command — it is the status of a block that survives because some recursive pin
above it does. Unpinning that root converts every indirect block below it into
garbage in one step, which is how a pinset can drop by gigabytes after removing
one entry.

Pinning a CID the node does not have fetches it first, so `ipfs pin add` on a
foreign CID is a download that then refuses to expire.

## Garbage collection

Kubo does not collect automatically unless started with `--enable-gc`. With it
on, a sweep runs when the datastore crosses `StorageGCWatermark` — 90% of
`StorageMax` by default — and on a timer. Without it, the repository grows until
the disk does not, and `ipfs repo gc` is a manual step people discover late.

A sweep walks the pinset and the mutable file system root, marks everything
reachable, and deletes the rest. It is the only thing that ever removes a block,
and it never touches a pinned one.

## Pinned is not available

A pinned block is retrievable only if three things hold at once: the node is
running, it is reachable from the requesting peer, and a provider record for the
CID still exists in the routing layer. The third expires after 48 hours and has
to be republished, and [content routing](/wiki/cs/ipfs/content-routing) covers
how a node with thousands of pins quietly fails to keep up with its own
announcements.

The two halves fail independently and look identical from the outside. A
correctly pinned, correctly served CID that nobody can find is as unreachable as
one that was never pinned at all.

## Somebody has to run the node

Which leaves the question the rest of this section is about: whose node. A
[pinning service](/wiki/cs/ipfs/pinning/pinning-services) sells the answer, a
standard [HTTP API](/wiki/cs/ipfs/pinning/pinning-service-api) makes the choice
of service reversible, and
[IPFS Cluster](/wiki/cs/ipfs/pinning/ipfs-cluster) is the same job done on
machines you own.

## External links

- [IPFS docs: pinning](https://docs.ipfs.tech/concepts/persistence/)
- [Kubo `ipfs pin` reference](https://docs.ipfs.tech/reference/kubo/cli/#ipfs-pin)
- [Kubo configuration: Datastore](https://github.com/ipfs/kubo/blob/master/docs/config.md#datastore)

## Wiki Pages

{{< section >}}
