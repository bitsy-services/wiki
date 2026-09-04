---
title: "The Pinning Service API"
weight: 20
---

The **IPFS Pinning Service API** is one HTTP interface that every pinning
service can implement, so a node can be pointed at any of them without new
client code. [Kubo](https://github.com/ipfs/kubo) speaks it natively, which is
what turns "which service am I using" into a configuration line rather than an
integration project.

## The surface

Five operations over one resource:

```text
POST   /pins                  create a pin request
GET    /pins                  list, filtered by status, cid, name, or time
GET    /pins/{requestid}      one request
POST   /pins/{requestid}      replace the pinned CID, keeping the request
DELETE /pins/{requestid}      unpin
```

Authentication is a bearer token in the `Authorization` header. A pin request
carries the [content identifier (CID)](/wiki/cs/ipfs/cid), an optional name, an
optional `meta` map the service stores and returns untouched, and `origins`.

Status is one of `queued`, `pinning`, `pinned`, or `failed`, and the client
finds out by asking again. Polling is the whole notification model — there is no
webhook and no stream in the specification — which for a bulk import means a
loop that walks the request list until nothing is left in the first two states.

Kubo drives all of this through one subcommand:

```bash
ipfs pin remote service add pinata https://api.pinata.cloud/psa "$TOKEN"
ipfs pin remote add --service=pinata --name=site-v4 --background <cid>
ipfs pin remote ls --service=pinata --status=queued,pinning,failed
```

`ipfs pin remote ls` defaults to showing only `pinned` requests, so a failed
import looks like an empty list until the status filter is passed explicitly.

## `origins` and `delegates` do the actual work

These two fields are why a pin request succeeds or hangs, and both are easy to
skip because both are optional.

`origins` is the client telling the service where to fetch from: a list of
multiaddresses of nodes that already have the blocks. Without it the service
must find a provider through [content routing](/wiki/cs/ipfs/content-routing),
which for content that was added seconds ago and has not finished announcing
means a lookup that returns nothing.

`delegates` is the service answering in kind, in the response: multiaddresses of
its own nodes that are ready to receive. A client that connects to them directly
gets a transfer that starts immediately, and one that ignores them waits for the
two sides to discover each other.

```http
POST /pins HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "cid": "bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi",
  "name": "site-v4",
  "origins": ["/ip4/203.0.113.7/tcp/4001/p2p/12D3KooWExampleOriginPeerID"]
}
```

```json
{
  "requestid": "UiYXJlIHlvdSByZWFkaW5n",
  "status": "queued",
  "created": "2026-09-03T10:14:02.000Z",
  "pin": { "cid": "bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi", "name": "site-v4" },
  "delegates": ["/ip4/198.51.100.20/tcp/4001/p2p/12D3KooWExampleServicePeerID"]
}
```

The Kubo subcommand above has no flag for `origins`, so a client that needs the
hint has to call the API directly — which is exactly the case where a pin sits
in `queued` and the CLI gives no indication why.

## Frozen since 2022

The specification reached 1.0.0 in 2020, stopped changing in 2022, and its
repository is archived with an explicit note that work on it should not resume
there. The reasons given are worth reading as a design lesson: too many servers
and third-party integrations are locked to the 2020 shape for any change to be
non-breaking, the Go and JavaScript client libraries around it are deprecated or
archived, and the polling model does not fit later work on verifiable transfer
and delegated retrieval. Proposals for a successor go through the IPFS
Improvement Proposal (IPIP) process in `ipfs/specs` as a fresh design rather
than as a revision.

Frozen is not the same as dead. The API is implemented by the major services and
by [IPFS Cluster](/wiki/cs/ipfs/pinning/ipfs-cluster), and being unable to
change is precisely what makes it a reliable portability layer: a pinset moves
between two providers, or from a provider to your own cluster, by re-running the
same requests against a different endpoint. Whether a service implements it is
the single most useful thing to check before
[choosing one](/wiki/cs/ipfs/pinning/providers), because it decides how
expensive leaving will be.

## External links

- [Pinning Service API specification](https://ipfs.github.io/pinning-services-api-spec/)
- [ipfs/pinning-services-api-spec](https://github.com/ipfs/pinning-services-api-spec) — archived repository and the rationale for freezing it
- [IPFS docs: work with remote pinning services](https://docs.ipfs.tech/how-to/work-with-pinning-services/)
