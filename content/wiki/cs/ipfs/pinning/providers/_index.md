---
title: "Providers"
weight: 30
bookCollapseSection: true
---

Pricing pages change monthly and free tiers change without warning, so the
durable questions about a pinning provider are structural: what happens to the
[content identifiers (CIDs)](/wiki/cs/ipfs/cid) when the relationship ends, and
how much code has to change to end it.

## What actually differentiates them

| Question | Why it decides things |
|---|---|
| Does it implement the [Pinning Service API](/wiki/cs/ipfs/pinning/pinning-service-api)? | If yes, migrating is re-running requests against a different endpoint. If no, the integration is bespoke and so is the exit. |
| Does it announce to the routing layer, or only serve its own gateway? | Gateway-only retention makes the hostname load-bearing, and hostnames get retired. |
| Can the blocks come back as a [content addressable archive (CAR)](/wiki/cs/ipfs/gateways#trustless-gateways)? | A bulk export is the difference between a migration and a re-upload from whatever originals survive. |
| Is there a second tier behind the pin? | [Filecoin](/wiki/economics/finance/defi/filecoin) deals or equivalent turn "we say it is there" into something a third party can check. |
| How is bandwidth priced? | For read-heavy content the egress line dominates the storage line by an order of magnitude. |

## The current field

| Provider | Interface | Backed by | Distinguishing property |
|---|---|---|---|
| [Pinata](/wiki/cs/ipfs/pinning/providers/pinata) | own API plus the standard one at `/psa` | its own infrastructure | built only for this; dedicated gateways on custom domains |
| [Filebase](/wiki/cs/ipfs/pinning/providers/filebase) | S3, plus the standard one | its own infrastructure, 3× replicated | existing S3 tooling works unmodified |
| [Lighthouse](/wiki/cs/ipfs/pinning/providers/lighthouse) | its own SDK and API | Filecoin or Walrus | encryption with programmable access conditions |
| [QuickNode](/wiki/cs/ipfs/pinning/providers/quicknode) | its own REST API | its own infrastructure | already there if the node provider is |
| [4EVERLAND](/wiki/cs/ipfs/pinning/providers/4everland) | the standard one | its own infrastructure | bulk CID import and `.car` parsing |
| [Crust](/wiki/cs/ipfs/pinning/providers/crust) | the standard one, with a wallet signature | its own chain and staked nodes | no account and no invoice |

Running the node instead is the other option, and
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
| [web3.storage and Storacha](/wiki/cs/ipfs/pinning/providers/web3-storage) | the Pinning Service API, then IPFS entirely | 2024 onward |

The first four were free or heavily subsidised, run by an organisation whose
main business was something else, and each gave a migration window measured in
weeks. The fifth is a different shape and worth reading on its own: nothing shut
down, the product was simply renamed twice and re-scoped until IPFS was no
longer part of it. None of them lost data that anybody held a second copy of.

The pattern is not that these companies are unreliable. It is that pinning at a
loss is a customer-acquisition line item, and line items get cut. A free tier is
a subsidy with an unknown expiry, and the paid tier is the number worth pricing
before anything is built on the free one.

## An arrangement that survives the list above

- **Pin to two unrelated providers**, both speaking the standard API, so
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

- [IPFS ecosystem directory](https://ecosystem.ipfs.tech/) — the fuller list, including services not covered here
- [IPFS docs: work with pinning services](https://docs.ipfs.tech/how-to/work-with-pinning-services/)
- [application-research/estuary](https://github.com/application-research/estuary) — archived, with the discontinuation notice

## Wiki Pages

{{< section >}}
