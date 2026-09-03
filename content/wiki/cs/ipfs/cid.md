---
title: "Content Identifiers"
weight: 10
---

A **content identifier (CID)** is the name [IPFS](/wiki/cs/ipfs) gives a block.
It is not a bare hash: it is a hash wrapped in enough metadata to say which hash
function produced it, how long the digest is, how the bytes it names should be
interpreted, and which alphabet the whole thing is written in. Every one of
those is a decision that would otherwise have to be agreed out of band, and
baking them into the identifier is what lets the format change without breaking
the names already in circulation.

## Anatomy

A version-1 CID is a one-character encoding prefix followed by four binary
fields:

```text
b   afybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi
│   │
│   └── base32 of:  0x01      0x70      0x12 0x20    <32-byte digest>
│                   version   codec     multihash    digest
│                                       prefix
└── multibase prefix: which alphabet the rest is written in
```

Base32 packs five bits per character, so character boundaries do not line up
with byte boundaries: `bafybei` is a recognisable prefix rather than a parseable
one, and reading the fields out means decoding first. The three fields other than
the digest are small integers from the
[multicodec](https://github.com/multiformats/multicodec/blob/master/table.csv)
and multibase tables:

| Field | Common values |
|---|---|
| Multibase | `b` base32 (lowercase, the default), `z` base58btc, `f` base16, `k` base36 |
| Version | `0x01` |
| Multicodec | `0x70` `dag-pb`, `0x55` `raw`, `0x71` `dag-cbor`, `0x72` `libp2p-key` |
| Multihash | `0x12 0x20` sha2-256 with a 32-byte digest, `0x1e 0x20` blake3 |

The multicodec is the field that does the most work in practice. `raw` means the
block is opaque bytes with no internal structure; `dag-pb` means it is a
protobuf node with named links to other CIDs, which is how
[UnixFS](/wiki/cs/ipfs/unixfs) builds a file out of chunks. A client that
retrieves a block knows from the CID alone whether to look inside it for more
links.

## Version 0 versus version 1

A CID starting `Qm` is version 0: base58btc, sha2-256, `dag-pb`, 46 characters,
and none of that written down anywhere in the string. The prefix `Qm` is just
what a base58-encoded `0x12 0x20` happens to look like. Version 0 is a bare
multihash with three parameters assumed.

Version 1 writes the assumptions out, which costs 13 characters and buys two
things. Any hash function and any codec can appear without a new CID format. And
the default text encoding becomes lowercase base32, which matters because
[gateways](/wiki/cs/ipfs/gateways) serve content from
`https://<cid>.ipfs.dweb.link`: a DNS label is case-insensitive, so a
case-sensitive base58 string cannot be one. The 59-character base32 form fits
inside the 63-character label limit with four characters to spare.

Conversion is one-way in general and lossless in the useful direction:

```bash
# v0 -> v1: always possible, adds the explicit codec and base
ipfs cid base32 QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG

# arbitrary re-encoding
ipfs cid format -v 1 -b base16 QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG
```

Going back to version 0 only works when the CID is `dag-pb` over sha2-256, since
those are the only values version 0 can express. A `raw` block or a blake3
digest has no version-0 spelling at all.

Kubo's `ipfs add` still defaults to CIDv0 for compatibility with a decade of
stored `Qm` strings. Passing `--cid-version=1` switches to version 1 and, as a
side effect, turns on raw leaves — which changes the hash of every leaf block
and therefore the root CID as well.

## The same file, two CIDs

Two people adding byte-identical files routinely get different CIDs, and nothing
is wrong when they do. The CID is the hash of the *tree*, and the tree depends on
every import parameter: chunk size, chunker algorithm, whether leaves are `raw`
or `dag-pb`, maximum links per node, the hash function, and the CID version.
Reproducing someone's CID means reproducing their import settings, not just
their bytes.

This is why "verify the CID matches" is a check on a specific published artifact
rather than a check on file contents, and why publishing the import parameters
alongside a CID is worth doing when anyone might need to regenerate it.

## Why self-description was worth the bytes

The multiformats design assumes the cryptography will be replaced. A network
that hardcoded sha2-256 into its address format would need a flag day to adopt
blake3; one that carries the function code in every address can serve both at
once, and a client that meets a digest it cannot compute knows precisely what it
is missing rather than failing to parse. The same argument runs for the codec:
`dag-cbor` and `dag-json` were added to the ecosystem years after `dag-pb`, and
no existing name had to change.

## External links

- [CID specification](https://github.com/multiformats/cid)
- [Multiformats](https://multiformats.io/) — multibase, multicodec, multihash
- [CID inspector](https://cid.ipfs.tech/) — decodes a CID field by field
- [IPFS docs: content addressing and CIDs](https://docs.ipfs.tech/concepts/content-addressing/)
