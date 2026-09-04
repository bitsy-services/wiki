---
title: "Lighthouse"
weight: 40
---

Lighthouse serves content over [IPFS](/wiki/cs/ipfs) and persists it to one of
two networks behind the scenes —
[Filecoin](/wiki/economics/finance/defi/filecoin) or
[Walrus](/wiki/economics/finance/defi/sui/walrus) — with the choice made per
plan rather than per file. What distinguishes it from the rest of this section
is not the storage but the access control layered on top.

## Encryption with programmable access conditions

Kavach is Lighthouse's threshold-encryption layer. A file is encrypted before
upload, the key is split across nodes, and reassembly is conditioned on a rule
evaluated at request time: holding a particular token or
[NFT](/wiki/economics/finance/defi/nft), presenting a passkey, or satisfying an
arbitrary contract call.

Every other provider here stores public bytes. Anything confidential has to be
encrypted before it is handed over, which leaves the key-distribution problem
entirely with the publisher. Kavach makes the decryption condition itself the
programmable part, turning "store this file" into "store this file, readable by
whoever holds that token" without a server that could be asked to hand the key
over.

## Pay-once is history

Lighthouse was built around perpetual storage: one payment, no renewal, funded
by a smart-contract endowment pool that took the buffer left over after the
initial Filecoin deals and used it to pay for renewals — the
[Arweave](/wiki/economics/finance/defi/arweave) proposition executed on
somebody else's storage market.

That is not what it currently sells. The plans are monthly or annual
subscriptions with a free tier and storage quotas, and the documentation now
says data remains stored while the plan is active. The endowment model is worth
knowing about because it is still described in older write-ups and in a good
deal of third-party comparison material, and because a page or a contract
written on the strength of "pay once, stored forever" is now relying on a
subscription somebody has to keep paying.

Encryption, token gating, and
[IPNS](/wiki/cs/ipfs/ipns-and-dnslink) support sit in add-on tiers rather than
the base plans, which matters given that the encryption is the reason to be
here.

## Practicalities

The integration is Lighthouse's own SDK and HTTP API; there is no
[Pinning Service API](/wiki/cs/ipfs/pinning/pinning-service-api) endpoint, so
`ipfs pin remote` cannot address it and moving off means re-uploading rather
than replaying pin requests. Retrieval runs through Lighthouse's own dedicated
[gateways](/wiki/cs/ipfs/gateways), with media-oriented extras layered on such
as image resizing and streaming-friendly delivery.

Content stays addressable by
[content identifier (CID)](/wiki/cs/ipfs/cid) regardless of any of this, which
is what the
[second pin](/wiki/cs/ipfs/pinning/providers#an-arrangement-that-survives-the-list-above)
is for.

## External links

- [lighthouse.storage](https://www.lighthouse.storage/), [pricing](https://www.lighthouse.storage/pricing), and [documentation](https://docs.lighthouse.storage/)
- [Lighthouse on Filecoin](https://filecoin.io/blog/posts/lighthouse-makes-permanent-storage-on-filecoin-easy-and-affordable/) — the endowment model as originally described
