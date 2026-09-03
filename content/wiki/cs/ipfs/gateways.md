---
title: "Gateways"
weight: 50
---

A gateway is an HTTP server that speaks [IPFS](/wiki/cs/ipfs) so the client does
not have to. It accepts a URL containing a
[content identifier (CID)](/wiki/cs/ipfs/cid), fetches the blocks over the
peer-to-peer network, reassembles them, and returns an ordinary HTTP response.
Every browser follows such a link with no extension, no daemon, and no awareness
that any of this happened.

## Three URL shapes

```text
https://ipfs.io/ipfs/<cid>/logo.png                path gateway
https://<cid>.ipfs.dweb.link/logo.png              subdomain gateway
https://example.com/logo.png                       DNSLink gateway
```

The path form is the one people paste, and it puts every CID on the network
under a single browser origin. Anything served from `ipfs.io/ipfs/` shares
cookies, local storage, and permissions with everything else served from
`ipfs.io/ipfs/`, so one hostile page can read another page's state. The
subdomain form exists to fix exactly that: each CID gets its own origin, and the
browser's same-origin policy does the isolation it was designed to do. `ipfs.io`
and `dweb.link` redirect path requests into the subdomain form for this reason.
Only a version-1 CID in lowercase base32 can appear in that hostname, because a
domain label is case-insensitive and capped at 63 characters, so a `Qm` link
still works and is converted on the way through.

DNSLink gateways resolve `_dnslink` TXT records and serve a whole site from a
CID, covered under [IPNS and DNSLink](/wiki/cs/ipfs/ipns-and-dnslink).

## Trustless gateways

A plain gateway response is a stream of bytes with the verification already
done — by the gateway, on the gateway's word. The client sees a `200` and has no
way to tell a correct response from a fabricated one, so the gateway is trusted
in the same way any web server is trusted, and the content addressing has bought
nothing at the last hop.

The trustless gateway specification closes that by having the gateway return
verifiable data instead of rendered output:

```bash
curl -H 'Accept: application/vnd.ipld.raw' https://ipfs.io/ipfs/<cid>     # one block
curl -H 'Accept: application/vnd.ipld.car' https://ipfs.io/ipfs/<cid>     # the DAG, as a CAR
```

A content addressable archive (CAR) is the [Merkle DAG](/wiki/cs/dag) serialised
into one file: blocks plus the roots that index them. The client hashes each
block and checks it against its parent, so a gateway that alters or omits
anything is caught by the client rather than believed. `?dag-scope=` narrows the
response to the subtree actually wanted. This is what browser-side IPFS
implementations use, and it turns the gateway into a transport rather than an
authority.

## `ipfs://` versus a gateway URL

A reference of the form `ipfs://<cid>` names content, and any client that speaks
the protocol resolves it from any peer. A reference of the form
`https://ipfs.io/ipfs/<cid>` names *a host that will fetch that content* —
convenient, because every browser follows it without extra software, and exactly
the single point of failure the content addressing was supposed to remove. If
that gateway goes away, the link dies although the data is fine.

This is why an [NFT](/wiki/economics/finance/defi/nft) whose `tokenURI` is a
gateway URL is only nominally content-addressed, and why the fix costs nothing:
store the `ipfs://` form, and let the client pick a gateway at read time.

## The failure that proved the point

Cloudflare ran a free public gateway for years, and a great deal of software
hardcoded `cloudflare-ipfs.com`. On 14 May 2024 those hostnames began
redirecting to `ipfs.io` and `dweb.link`; on 14 August 2024 they stopped
resolving to IPFS at all. Wallets and interfaces carrying the hostname in a
default gateway list — MetaMask and the Uniswap interface among them — shipped
broken image loading until each project noticed and cut a release. Not one CID
changed. Every one of those assets was still retrievable from the network the
whole time, from any of a dozen other gateways.

The lesson generalises past Cloudflare: a gateway hostname baked into a
long-lived artifact is a dependency on a company's product roadmap. Public
gateways also rate-limit aggressively, which is what pinning services are
selling when they offer a "dedicated gateway" — a hostname whose throughput and
uptime are somebody's contractual problem, and a hostname you will one day have
to migrate off in exactly the same way.

## Takedowns

Gateway operators consult denylists and refuse to serve specific CIDs, whether
for copyright claims, abuse reports, or legal orders. The block is at the
serving layer only: the content stays addressable, stays retrievable by any peer
speaking the protocol directly, and reappears through any gateway that does not
share the list. Publishing to IPFS is therefore not a defence against removal
from a given gateway, and pinning to IPFS is not a way to make anything
unavailable to law enforcement — it changes who can be asked and what asking
achieves, not whether the bytes exist.

## External links

- [Trustless gateway specification](https://specs.ipfs.tech/http-gateways/trustless-gateway/)
- [Subdomain gateway specification](https://specs.ipfs.tech/http-gateways/subdomain-gateway/)
- [Public IPFS utilities](https://docs.ipfs.tech/concepts/public-utilities/)
- [Cloudflare Web3 migration guide](https://developers.cloudflare.com/web3/reference/migration-guide/) — the gateway shutdown notice
- [A practical explainer for IPFS gateways](https://blog.ipfs.tech/2022-06-30-practical-explainer-ipfs-gateways-2/)
