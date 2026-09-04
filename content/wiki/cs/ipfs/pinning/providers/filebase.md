---
title: "Filebase"
weight: 20
---

Filebase is object storage with an S3-compatible interface whose buckets are
backed by decentralized networks, [IPFS](/wiki/cs/ipfs) among them. The
consequence is unusual in this market: no client library is required, because
every tool that already speaks bucket semantics — the AWS command line,
backup software, Terraform, anything with an S3 driver — works against it
unmodified.

## The bucket is the pinset

Files written to an IPFS bucket are pinned automatically, and Filebase has long
described the pinning as geo-redundant across separate locations. The current
pinning documentation does not state a replication factor, which puts it in the
same position as most of this market — the
[quiet variable](/wiki/cs/ipfs/pinning/pinning-services#what-is-actually-being-promised)
is how many copies "pinned" means, and the answer is usually not written down.

```bash
aws s3 cp ./dist s3://my-bucket/ --recursive --endpoint-url https://s3.filebase.com
```

Each object's [content identifier (CID)](/wiki/cs/ipfs/cid) is exposed as
object metadata, so an upload through ordinary S3 tooling still produces a
content address that anything else on the network can fetch.

## The standard API, scoped per bucket

Filebase also serves the
[Pinning Service API](/wiki/cs/ipfs/pinning/pinning-service-api), with the
client appending `/pins` to the service root itself:

```bash
ipfs pin remote service add filebase https://api.filebase.io/v1/ipfs "$TOKEN"
```

Scoping the token to one bucket rather than to the whole account is the detail
that distinguishes it operationally: separate projects get separate pinsets,
separate credentials, and separate blast radius, without separate accounts.

## Migration is the pitch

Filebase shipped an import tool for Infura's pinset when that service wound
down, moving pinned CIDs into a bucket without a manual export and re-pin of
each one. That is the concrete form of the portability argument the rest of this
section makes in the abstract: the destination provider builds the on-ramp,
because the standard API makes it cheap to build.

## What to check

There is a free allowance and paid plans start around a flat monthly minimum,
with per-gigabyte pricing on some backends covering storage and bandwidth
together. The bucket abstraction hides which backend an object landed on, so
the network a bucket is configured for is worth confirming rather than assuming.

## External links

- [filebase.com](https://filebase.com/) and [IPFS pinning](https://filebase.com/ipfs-pinning/)
- [Filebase: IPFS Pinning Service API](https://docs.filebase.com/api-documentation/ipfs-pinning-service-api)
- [Migrating from Infura IPFS](https://filebase.com/blog/infura-ipfs-is-shutting-down-how-to-migrate/)
