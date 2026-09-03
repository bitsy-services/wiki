---
title: "IPNS and DNSLink"
weight: 40
---

A [content identifier (CID)](/wiki/cs/ipfs/cid) is a hash, so publishing a new
version of anything produces a new name. Every real deployment on
[IPFS](/wiki/cs/ipfs) therefore needs a second layer: a stable name that points
at a CID and can be repointed. Three mechanisms do this, and they differ in who
is allowed to repoint, how fast the change propagates, and what has to be
trusted for the answer to be right.

## IPNS

The **InterPlanetary Name System (IPNS)** names content by a key pair. The name
is the CID of the public key under the `libp2p-key` codec, written in base36 by
default — `k51qzi5uqu5...` — and the base36 choice is a consequence of the
default key type. An Ed25519 public key is small enough that libp2p embeds it in
the identifier verbatim, under the identity multihash, rather than hashing it.
That makes the CID 40 bytes, which comes to 65 characters in base32 including
the multibase prefix — over the 63-character limit on a domain label, and
therefore unusable as a [subdomain gateway](/wiki/cs/ipfs/gateways) host. The
same 40 bytes in base36 come to 62. An RSA key is too large to embed and gets
hashed instead, producing the shorter 59-character base32 form that never had
the problem.

Publishing signs a record containing the target path, a sequence number, an
expiry, and a cache lifetime, then writes it into the distributed hash table
(DHT) under the name. Resolvers accept the record with the highest sequence
number that verifies against the public key, so only the key holder can move the
pointer and any resolver can check that the record it got is genuinely theirs.

```bash
ipfs name publish --key=site /ipfs/bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi
ipfs name resolve /ipns/k51qzi5uqu5dlvj2baxnqndepeb86cbk3ng7n3i46uzyxzyqj2xjonzllnv0v8
```

Kubo signs records with a 24-hour validity and republishes every 4 hours, which
means an unattended node that goes down for a day takes its name with it — the
record expires and resolution fails even though the content it pointed at is
still pinned and still served. The republish loop, not the pin, is what keeps an
IPNS name alive.

Resolution is also the slow path. A cold lookup is a DHT walk, routinely
seconds and sometimes tens of seconds, because the resolver must gather
competing records before it can pick the highest sequence number. `--nocache`
makes this measurable; without it, a stale local answer masks how long the real
lookup takes. Enabling IPNS over PubSub propagates updates to subscribed peers
in near real time and is worth it for anything a person waits on.

## DNSLink

DNSLink puts the pointer in an ordinary TXT record:

```text
_dnslink.example.com.  IN  TXT  "dnslink=/ipfs/bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi"
```

`/ipns/example.com` then resolves through it, and a gateway serves
`https://example.com` from the referenced CID. Updating means editing a DNS
record — seconds to propagate, no key management, no republish daemon — and the
value can itself be an `/ipns/` path, which chains the two.

What it costs is the property the rest of IPFS was built for. The answer now
depends on a registrar, a nameserver, and whoever can compel either, so the
content is verifiable and the *choice of content* is not. DNSLink is the right
answer for a site whose operators already accept that dependency for their apex
domain, and the wrong one for anything meant to survive its own domain
registration lapsing.

## `contenthash` on a name service

[EIP](/wiki/economics/finance/defi/ethereum/eip)-1577 defines a `contenthash`
record for the Ethereum Name Service (ENS), holding a binary-encoded
`/ipfs/<cid>` path. Repointing is a transaction, the record is on-chain, and
gateways that resolve ENS serve `example.eth` from whatever CID it currently
holds. Uniswap's interface reads
[token lists](/wiki/economics/finance/defi/token-registration/token-lists) this
way, which is the pattern in miniature: a stable name that a
[DAO](/wiki/economics/finance/defi/dao) or a multisig controls, pointing at
content that anyone can verify once they have the CID.

## Choosing

| | Who can repoint | Propagation | Trusted for the pointer |
|---|---|---|---|
| Raw CID | nobody | n/a | nothing |
| IPNS | the key holder | seconds to tens of seconds | the key stays private, and the node keeps republishing |
| DNSLink | whoever controls the zone | DNS cache time | registrar, nameserver, and anyone who can lean on them |
| ENS `contenthash` | the name's owner | one block, plus resolver caching | the key holding the name, and the chain |

A useful default is to publish the immutable CID everywhere it will be recorded
permanently — in a contract, in metadata, in a citation — and reserve the
mutable name for the surface humans type in.

## External links

- [IPNS specification](https://specs.ipfs.tech/ipns/ipns-record/)
- [DNSLink](https://dnslink.dev/)
- [EIP-1577: contenthash field for ENS](https://eips.ethereum.org/EIPS/eip-1577)
- [IPFS docs: IPNS](https://docs.ipfs.tech/concepts/ipns/)
