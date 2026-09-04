---
title: "Pinata"
weight: 10
---

Pinata is the longest-running service built for nothing but
[IPFS](/wiki/cs/ipfs) pinning, and the one most likely to be assumed when a
project says "we pin to a service". It runs its own infrastructure rather than
fronting somebody else's network, which makes the arrangement an ordinary
hosting relationship: retention while the invoice is paid, no proof mechanism,
no second tier behind it.

## Two APIs, and only one of them is portable

The native API does uploads in one call — post a file, get a
[content identifier (CID)](/wiki/cs/ipfs/cid) back — plus metadata, key scoping,
and grouping that the standard specification has no vocabulary for. Everything
written against it is written against Pinata.

The [Pinning Service API](/wiki/cs/ipfs/pinning/pinning-service-api) is served
in parallel at a separate root, authenticated with a token from the same keys
page:

```bash
ipfs pin remote service add pinata https://api.pinata.cloud/psa "$JWT"
ipfs pin remote add --service=pinata --name=site-v4 <cid>
```

Anything built on that endpoint moves to another provider by changing the URL.
The practical advice is to use the native API for whatever genuinely needs it
and keep the pinset reachable through `/psa`, because the second one is the exit
and the first one is not.

## Dedicated gateways

Pinata's most-used feature after pinning is a private
[gateway](/wiki/cs/ipfs/gateways) hostname, optionally on a custom domain, with
throughput that is not shared with the public internet. It solves the real
problem — public gateways rate-limit hard enough to break a production frontend
— and creates the standard one: every URL published through that hostname
depends on the account staying open.

A custom domain softens this, since the domain can be repointed at a different
gateway later while the paths stay valid. A `gateway.pinata.cloud` URL baked
into [NFT](/wiki/economics/finance/defi/nft) metadata cannot be repointed by
anyone.

## What to check

Pricing has moved several times, most recently around a file-oriented product
line with its own free allowance, so the numbers are worth reading from the
source rather than from anywhere else. The line that matters is bandwidth
through the dedicated gateway, not storage.

## External links

- [pinata.cloud](https://pinata.cloud/) and [pricing](https://pinata.cloud/pricing)
- [Pinata: Pinning Service API](https://docs.pinata.cloud/api-reference/pinning-service-api)
- [Pinata: dedicated gateways](https://pinata.cloud/dedicated-ipfs-gateways)
