---
title: "QuickNode"
weight: 50
---

QuickNode sells blockchain node infrastructure, and [IPFS](/wiki/cs/ipfs)
pinning is one product in that catalogue rather than the business. The case for
using it is that the account, the billing, and the dashboard already exist for
whatever [RPC](/wiki/cs/entity-addressing/resource-vs-rpc) endpoints
the project is running on.

## Its own REST API

There are three groups of endpoints under one base — gateway management,
pinning, and account usage — authenticated with an `x-api-key` header:

```bash
curl -X POST "https://api.quicknode.com/ipfs/rest/v1/pinning" \
  -H "x-api-key: $QN_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "cid": "bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi",
        "name": "site-v4",
        "origins": ["/ip4/203.0.113.7/tcp/4001/p2p/12D3KooWExampleOriginPeerID"]
      }'
```

This is not the vendor-agnostic
[Pinning Service API](/wiki/cs/ipfs/pinning/pinning-service-api), and the way it
is not is instructive. The request body is the specification's body — `cid`,
`name`, `origins`, `meta`, with `name` required here rather than optional.
`origins` carries the multiaddresses of nodes that already have the blocks and
[does the same work here](/wiki/cs/ipfs/pinning/pinning-service-api#origins-and-delegates-do-the-actual-work)
as it does everywhere else. What differs is the envelope: a proprietary path, an
`x-api-key` header where the specification says `Authorization: Bearer`, and no
`/pins` root. So
`ipfs pin remote service add` cannot point at it, no standard client library
works, and porting to a provider that does implement the specification is mostly
a matter of moving the same JSON to a different URL.

The account-usage endpoints returning bandwidth and storage metrics are a
genuine convenience the standard specification does not cover, and they are also
part of what has to be rewritten on the way out.

## The structural risk is the shape of the business

Pinning here is a secondary product of a company whose main business is node
access. That is precisely the profile of the entries in
[the graveyard](/wiki/cs/ipfs/pinning/providers#the-graveyard) — Infura was a
node provider with an IPFS service on the side, and the IPFS service is the one
that was shut off.

This is not a prediction about QuickNode. It is a reason to treat the bespoke
integration as a cost paid twice — once to write it, once to replace it — and to
hold the
[second pin](/wiki/cs/ipfs/pinning/providers#an-arrangement-that-survives-the-list-above)
that the rest of this section argues for. The
[content identifiers (CIDs)](/wiki/cs/ipfs/cid) survive either way.

## External links

- [QuickNode IPFS](https://www.quicknode.com/ipfs) and [API documentation](https://www.quicknode.com/docs/ipfs)
