---
title: "Content Routing and Bitswap"
weight: 30
---

Fetching a [content identifier (CID)](/wiki/cs/ipfs/cid) is two problems that
[IPFS](/wiki/cs/ipfs) solves with two separate subsystems. *Routing* answers
"which peers claim to have this block". *Transfer* gets the bytes from one of
them. Neither is guaranteed to succeed, and they fail for unrelated reasons —
which is why a CID that stops resolving is rarely a storage problem.

## Provider records and the Amino DHT

The public IPFS distributed hash table (DHT), named **Amino** in 2023 to
separate the specific network from the Kademlia protocol it runs, maps a
multihash — the raw digest inside the CID, without the version and codec
wrapper — to a list of peers advertising it. A node holding a block *provides*
it by writing a record to the peers whose IDs sit closest to that multihash in
the keyspace. Keying on the digest rather than the whole CID means two CIDs over
the same bytes, differing only in codec or base, share one set of provider
records.

Provider records carry a 48-hour validity. Nothing renews them but the provider,
so a node has to walk its entire pinset and re-announce, which Kubo does every
22 hours by default. The record says only that a peer claimed to have the block
at announcement time; no one checks, and a peer that has since deleted it, gone
offline, or lied leaves a record that stays valid for up to two days.

## The reprovide bottleneck

Announcing one CID means a DHT walk to find the closest peers and then writes to
each — around 15 seconds of wall clock, one CID at a time, in the sequential
implementation. Two deadlines bound what that allows. The 22-hour interval is
the target, and a cycle that overruns it causes the next scheduled cycle to be
skipped, so cycles start running back to back: roughly 5,280 CIDs is where the
slack disappears. The 48-hour record validity is the deadline that matters, and
a pinset large enough to make one full cycle take longer than that — about
11,520 CIDs at 15 seconds each — begins losing provider records faster than it
replaces them. The content then quietly stops being findable while every byte of
it is still on disk and still pinned.

The failure is silent from the operator's side. The node reports the pins as
present, `ipfs pin ls` agrees, local retrieval works, and only a stranger trying
to fetch the CID discovers there is no route to it. Anyone
[self-hosting](/wiki/cs/ipfs/pinning/ipfs-cluster) more than a few thousand
objects hits this, and it is the strongest single argument for paying somebody
whose job is to keep announcements current.

Two responses exist. `Reprovider.Strategy` can be narrowed to `roots`, which
announces only the root CID of each pinned [DAG](/wiki/cs/dag) rather than every
block — retrieval then depends on the fetching peer walking the tree from a root
it already found. And *Provide Sweep*, work landed in 2025, restructures the
process to walk the keyspace in regions and batch announcements per region
rather than paying a full lookup per CID.

## Bitswap

Once a provider is known, **Bitswap** moves the blocks. A node maintains a
want-list, sends `want-have` messages to peers it is already connected to, and
follows up with `want-block` to whichever answers first. Because the broadcast to
existing connections is free of any DHT lookup, a block that some nearby peer
happens to hold often arrives before routing has finished running at all.

Bitswap has no payment layer and no enforced accounting. Early designs included
a tit-for-tat ledger to punish leeching; what shipped serves whoever asks. That
choice is why IPFS has no native incentive to store anything for anyone, and why
[pinning](/wiki/cs/ipfs/pinning) is a commercial arrangement rather than a
protocol feature — the gap that [Filecoin](/wiki/economics/finance/defi/filecoin)
was built to fill.

## Delegated routing

A browser tab cannot join a DHT: it has no persistent identity, no inbound
connectivity, and no reason to spend the user's battery on Kademlia. Delegated
routing gives it one HTTP call instead:

```text
GET /routing/v1/providers/bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi
```

The endpoint returns the multiaddresses of providers, and the client connects
directly. Responses are cacheable — five minutes fresh, with a 48-hour
stale-while-revalidate window matched to the provider-record lifetime — so a
popular CID is answered from cache rather than a fresh walk.

Large publishers can also skip per-CID DHT announcements entirely by advertising
to an InterPlanetary Network Indexer (IPNI) such as `cid.contact`, which ingests
signed advertisement chains covering millions of multihashes at once and answers
the same routing queries. The DHT and the indexers cover different scales of
publisher, and a client that queries both finds content that either alone would
miss.

## Two ways for a CID to die

| Symptom | Cause | Fix |
|---|---|---|
| No provider records returned | nobody announced, or the announcement expired | reprovide, narrow the strategy, or delegate |
| Providers listed, transfer stalls | the peer is offline, behind an unreachable address, or no longer holds the block | pin somewhere reachable |

Both present to the user as an infinite spinner, and telling them apart takes
one command:

```bash
ipfs routing findprovs <cid>    # empty output means it is a routing failure
```

## External links

- [Kademlia DHT specification](https://specs.ipfs.tech/routing/kademlia-dht/)
- [Bitswap specification](https://specs.ipfs.tech/bitswap-protocol/)
- [Delegated Routing V1 HTTP API](https://specs.ipfs.tech/routing/http-routing-v1/)
- [Provide Sweep](https://ipshipyard.com/blog/2025-dht-provide-sweep/) — the reprovide bottleneck and its fix
- [Amino, the public IPFS DHT](https://blog.ipfs.tech/2023-09-amino-refactoring/)
