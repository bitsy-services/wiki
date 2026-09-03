---
title: "IPFS Cluster"
weight: 40
---

[IPFS](/wiki/cs/ipfs) pins are per-node: a pin on one machine says nothing to
any other. **IPFS Cluster** adds the missing layer — a daemon that runs beside
each Kubo instance and gives a group of them one shared pinset, with a
replication factor per entry and automatic allocation of each pin to specific
peers.

## The shape of it

```text
  peer A                    peer B                    peer C
┌──────────────┐          ┌──────────────┐          ┌──────────────┐
│ ipfs-cluster │◄────────►│ ipfs-cluster │◄────────►│ ipfs-cluster │
│      │       │  pinset  │      │       │  pinset  │      │       │
│   kubo       │          │   kubo       │          │   kubo       │
└──────────────┘          └──────────────┘          └──────────────┘
```

The cluster peers agree on *which* [content identifiers (CIDs)](/wiki/cs/ipfs/cid)
should be pinned and by whom; the Kubo daemons underneath do the actual pinning
and serving. Cluster is not a storage layer and does not touch blocks — it is
bookkeeping over a set of nodes that each speak plain IPFS to the outside world.

```bash
ipfs-cluster-ctl pin add --replication-min 2 --replication-max 3 <cid>
ipfs-cluster-ctl status <cid>     # per-peer: PINNED, PINNING, PIN_ERROR
```

A pin with `replication-min 2` is allocated to two peers by the configured
strategy — free disk space by default — and the cluster re-allocates it
elsewhere if one of those peers stops responding. There is no sharding: each
allocated peer holds the entire [Merkle DAG](/wiki/cs/dag), so the replication
factor is literally the number of complete copies.

## Consensus: CRDT or Raft

The pinset is replicated state, and Cluster ships two ways to agree on it.

**CRDT** is the default. Updates are conflict-free replicated data type
operations broadcast over pubsub and merged in any order, so peers can join,
leave, and be offline for long stretches without a membership ceremony. Write
authority comes from a `trusted_peers` list rather than from a quorum, which
makes it the right choice for a cluster whose members come and go, and for
collaborative clusters where most participants are followers.

**Raft** is leader-based with a fixed peerset. It gives a strict ordering and
requires a majority online to accept writes — lose quorum and the pinset is
read-only until peers return. It is the older option and remains reasonable for
a small fixed set of always-on machines where the operator wants a single
authoritative log.

`ipfs-cluster-follow` runs a peer that only mirrors somebody else's pinset. That
is how public dataset collectives work: the curator pins, and volunteers replicate
without any ability to modify what they are replicating.

## It speaks the standard pinning API

Cluster exposes the
[Pinning Service API](/wiki/cs/ipfs/pinning/pinning-service-api) alongside its
own interface, so `ipfs pin remote service add` points at a cluster exactly as
it points at a commercial provider. An application written against the standard
API can move from a paid service to self-hosted infrastructure without a code
change, and back.

## When it beats paying

Self-hosting wins on egress-heavy workloads, where bandwidth pricing dominates,
and on anything where the data cannot leave your control for legal reasons. It
loses on attention: the failure mode that catches self-hosters is not disk or
uptime but announcements. A cluster holding tens of thousands of pins runs into
the reprovide ceiling described under
[content routing](/wiki/cs/ipfs/content-routing) — provider records expire after
48 hours, a full reprovide cycle takes longer than that, and content becomes
unfindable while every peer reports it as correctly pinned.

`ipfs stats reprovide` on each Kubo node reports how long the last cycle took.
Past the 22-hour target interval the node is consuming its safety margin; past
48 hours it is losing records, and the margin between those two numbers is all
the warning there is.

## External links

- [ipfscluster.io](https://ipfscluster.io/) — documentation
- [Cluster architecture](https://ipfscluster.io/documentation/guides/consensus/) — CRDT and Raft compared
- [Pinning Service API in Cluster](https://ipfscluster.io/documentation/reference/pinsvc_api/)
- [Collaborative clusters](https://collab.ipfscluster.io/) — follower peers in practice
