---
title: "Choosing a Service"
weight: 30
---

Pricing pages change monthly and free tiers change without warning, so the
durable questions about a pinning service are structural: what happens to your
[content identifiers (CIDs)](/wiki/cs/ipfs/cid) when the relationship ends, and
how much of your code has to change to end it.

## What actually differentiates them

| Question | Why it decides things |
|---|---|
| Does it implement the [Pinning Service API](/wiki/cs/ipfs/pinning/pinning-service-api)? | If yes, migrating is re-running requests against a different endpoint. If no, the integration is bespoke and so is the exit. |
| Does it announce to the routing layer, or only serve its own gateway? | Gateway-only retention makes the hostname load-bearing, and hostnames get retired. |
| Can you get the blocks back as a content addressable archive (CAR)? | A bulk export is the difference between a migration and a re-upload from whatever originals you still have. |
| Is there a second tier behind the pin? | [Filecoin](/wiki/economics/finance/defi/filecoin) deals or equivalent turn "we say it is there" into something a third party can check. |
| How is bandwidth priced? | For read-heavy content the egress line dominates the storage line by an order of magnitude. |

## The landscape

- **Pinata** is the longest-running service built only for this, implements the
  Pinning Service API, and sells dedicated gateway hostnames. It is the default
  answer for a project that wants pinning and nothing else.
- **Filebase** presents an S3-compatible interface over IPFS, which means
  existing tooling — the AWS command line, anything that speaks bucket
  semantics — works unmodified, and geo-replicates across regions. It also
  shipped an import tool for Infura's pinset when that service wound down.
- **Storacha**, formerly web3.storage, is a hot-storage layer settling to
  Filecoin, and it dropped the Pinning Service API interface on the way. It is
  the strongest option for durability with a proof behind it and the weakest for
  drop-in portability.
- **Lighthouse** sells perpetual storage paid once, backed by Filecoin deals it
  renews, which is the closest thing in this market to the
  [Arweave](/wiki/economics/finance/defi/arweave) model.
- **Quicknode** and **4EVERLAND** bundle pinning into a broader platform, which
  is convenient when the account already exists and is one more thing to
  untangle when it does not.
- **Crust Network** pins against on-chain staking rather than a subscription,
  and is worth a look for anything that needs the payment itself to be
  permissionless.

Running the node yourself is the other option, and
[IPFS Cluster](/wiki/cs/ipfs/pinning/ipfs-cluster) is what that looks like past
one machine.

## The graveyard

Four shutdowns since 2023, all with the same shape:

| Service | What ended | When |
|---|---|---|
| Estuary | discontinued; `estuary.tech` and its API taken down | July 2023, site April 2024 |
| `nft.storage` Classic | uploads and pinning; retrieval kept | 30 June 2024 |
| Cloudflare public gateway | `cloudflare-ipfs.com` stopped resolving to IPFS | 14 August 2024 |
| Infura IPFS | uploads 3 August, API and gateway 15 August | August 2026 |

Every one was free or heavily subsidised, run by an organisation whose main
business was something else, and every one gave a migration window measured in
weeks. None of them lost data that anybody held a second copy of.

The pattern is not that these companies are unreliable. It is that pinning at a
loss is a customer-acquisition line item, and line items get cut. Treat a free
tier as a subsidy with an unknown expiry, and price the paid tier before
building on the free one.

## An arrangement that survives the list above

- **Pin to two unrelated services**, both speaking the standard API, so
  switching is a configuration change and losing one is not an incident.
- **Keep the originals**, and keep the import parameters that produced the CIDs
  alongside them. Reproducing a CID needs the chunker and version settings, not
  just the file — see [UnixFS](/wiki/cs/ipfs/unixfs).
- **Publish `ipfs://` references**, not gateway URLs, wherever the reference
  outlives the deployment: contract storage, metadata, anything signed.
- **Check retrieval from outside**, on a schedule, with the two commands under
  [checking a service is doing its job](/wiki/cs/ipfs/pinning/pinning-services#checking-a-service-is-doing-its-job).

None of that is expensive, and all of it is much cheaper before the notice email
than after.

## External links

- [Pinata](https://pinata.cloud/), [Filebase](https://filebase.com/), [Storacha](https://storacha.network/), [Lighthouse](https://www.lighthouse.storage/) — current services
- [IPFS docs: pinning services list](https://docs.ipfs.tech/how-to/work-with-pinning-services/)
- [application-research/estuary](https://github.com/application-research/estuary) — archived, with the discontinuation notice
