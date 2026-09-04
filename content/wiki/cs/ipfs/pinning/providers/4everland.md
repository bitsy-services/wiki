---
title: "4EVERLAND"
weight: 60
---

4EVERLAND is a Web3 infrastructure platform — storage, static hosting, and node
access — whose storage arm includes 4EVER Pin, an [IPFS](/wiki/cs/ipfs) pinning
service that implements the vendor-agnostic
[Pinning Service API](/wiki/cs/ipfs/pinning/pinning-service-api).

## Standard API, bulk-oriented tooling

The endpoint takes a bearer token generated on the 4EVER Pin page, and Kubo
talks to it with no adapter:

```bash
ipfs pin remote service add 4everland https://api.4everland.dev "$TOKEN"
ipfs pin remote add --service=4everland --name=archive-2026 <cid>
```

The tooling around it leans toward bulk work that the specification does not
describe: importing many
[content identifiers (CIDs)](/wiki/cs/ipfs/cid) at once, uploading whole
folders, and parsing
[content addressable archive (CAR)](/wiki/cs/ipfs/gateways#trustless-gateways)
files rather than requiring individual objects. Bringing an existing pinset in
from somewhere else is the operation that is usually painful and is specifically
catered for here.

## Where it fits

The [arrangement that survives a shutdown](/wiki/cs/ipfs/pinning/providers#an-arrangement-that-survives-the-list-above)
calls for two unrelated providers both speaking the standard API, and 4EVER Pin
qualifies with an ingest path for whole pinsets rather than individual objects —
the same role [Filebase](/wiki/cs/ipfs/pinning/providers/filebase) fills from
the other direction.

Two things count against it. The pinning service is one component of a platform
whose other products — bucket storage fronting
[Arweave](/wiki/economics/finance/defi/arweave) and
[Filecoin](/wiki/economics/finance/defi/filecoin), static hosting, gateway
endpoints — carry their own bespoke interfaces, so only 4EVER Pin itself is
portable and it is easy to end up depending on the rest. And like every entry
here that is not the company's whole business, the pinning service is a product
line rather than the reason the company exists.

## External links

- [4everland.org](https://www.4everland.org/) and [4EVER Pin documentation](https://docs.4everland.org/storage/4ever-pin)
- [4EVERLAND Pinning Services API](https://docs.4everland.org/storage/4ever-pin/pinning-services-api)
