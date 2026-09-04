---
title: "Pinning Services"
weight: 10
---

A pinning service runs the [IPFS](/wiki/cs/ipfs) node a publisher would
otherwise run. It takes a [content identifier (CID)](/wiki/cs/ipfs/cid) or a
file, keeps the blocks, keeps the process up, keeps the provider records fresh,
and usually sells a gateway hostname alongside. The product is uptime and
attention, and it is priced like hosting because that is what it is.

## Two ways to hand data over

**Uploading the bytes** puts the import in the service's hands, which means the
service picks the chunker, the CID version, and whether leaves are raw — so the
CID that comes back is a function of *their* settings, not of the file alone.
Two services given the same file routinely return different CIDs, and neither is
wrong. A CID that has to be predictable, because it is going into a contract, a
signature, or a citation, has to be produced locally and then pinned rather than
discovered after the fact.

**Pinning an existing CID** makes the service fetch it over the network from
whoever currently has it, which is generally the publisher. The origin node has
to be online, reachable, and announcing for the duration of that transfer, so a
pin request that sits in `queued` forever is usually a routing failure on the
origin side rather than anything the service did. Passing origin multiaddresses
with the request skips the lookup entirely and is the difference between a
transfer that starts in seconds and one that never starts.

## What is actually being promised

Retention for as long as the invoice is paid, on the service's word. There is no
proof mechanism: a pinning service cannot demonstrate that it still holds a set
of blocks, and the status field in its API is a database row it wrote about
itself. That is the precise boundary of what content addressing buys — received
bytes can be checked against the CID that named them, and nothing checks that
anyone still has them.

The two neighbours make stronger claims.
[Filecoin](/wiki/economics/finance/defi/filecoin) providers post recurring
cryptographic proofs against a dated deal, and
[Arweave](/wiki/economics/finance/defi/arweave) makes possession of stored data
a precondition for mining. Both are checkable by a third party. A pinning
invoice is not.

Replication is the other quiet variable. "Pinned" may mean one node in one
datacentre or several across regions; services differ, and several do not say.
Anything whose loss would matter wants at least two unrelated services and a
copy under the publisher's own control, which is also what makes the
[standard API](/wiki/cs/ipfs/pinning/pinning-service-api) worth insisting on —
three copies behind one bespoke integration is one integration to rewrite.

## What it costs

Three lines, and the first is rarely the big one:

- **Storage**, per gigabyte-month. Cheap, and the number quoted in marketing.
- **Bandwidth**, per gigabyte served through the dedicated gateway. This is what
  a popular collection actually costs, and it scales with readers rather than
  with data.
- **Requests**, metered per API call or per gateway request on some plans, which
  turns a hot-linked image into a per-view charge.

A collection of ten thousand images is a rounding error to store and a real bill
to serve, so the line that moves the invoice is where read traffic lands: the
paid gateway, a public one, or the reader's own node.

## Checking a service is doing its job

Two commands, run from a machine that is not the one that uploaded:

```bash
# 1. is the service announcing the CID, or only serving it?
ipfs routing findprovs <cid>

# 2. can a gateway with no relationship to the service retrieve it?
curl -sIL "https://dweb.link/ipfs/<cid>"
```

The first needs the service's peer ID to interpret, which the service publishes
in its documentation or returns as a `delegates` entry on a pin request. Follow
the redirect in the second: `dweb.link` answers a path request with a `301` into
its subdomain form, so `curl -sI` without `-L` reports success on a CID that
cannot be fetched at all.

A CID that resolves through its own service's gateway and nowhere else is being
served from that gateway's cache rather than provided to the network. The
retention is real, the routing is not, and the content disappears the moment
anything stops using that hostname.

## Failure modes, worst first

- **The service ends the product.** Free and subsidised IPFS offerings have been
  withdrawn repeatedly, generally with a migration window of weeks; the
  [record is under providers](/wiki/cs/ipfs/pinning/providers#the-graveyard).
  Unpinned data after a shutdown is gone unless somebody else has a copy.
- **Billing lapses.** Retention ends with the subscription, typically after a
  grace period, and the deletion is not reversible by paying afterwards.
- **A quota change unpins silently.** Free tiers that convert to metered plans
  drop what exceeds the new limit, and the first symptom is a broken image in
  production.
- **Provider records expire on the service's side.** The blocks are held and
  nothing announces them, so retrieval works only through their gateway.
- **A gateway hostname was baked into published artifacts.** Covered under
  [gateways](/wiki/cs/ipfs/gateways#the-failure-that-proved-the-point): the data
  survives, the links do not.

Everything on that list is survivable by holding a second copy somewhere else,
which is why the useful question about a pinning service is not what it promises
but how cheaply one can leave.
[Providers](/wiki/cs/ipfs/pinning/providers) works through the current field on
that basis, one page each.

## External links

- [IPFS docs: work with pinning services](https://docs.ipfs.tech/how-to/work-with-pinning-services/)
- [Migrating Infura IPFS pins before the cutoff](https://discuss.ipfs.tech/t/migration-option-for-infura-ipfs-pins-before-the-august-15-cutoff/20300)
- [nft.storage Classic](https://classic.nft.storage/) — retrieval-only since 2024
