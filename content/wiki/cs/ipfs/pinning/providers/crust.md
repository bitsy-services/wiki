---
title: "Crust"
weight: 70
---

Crust is a decentralized storage network with a chain of its own, and its
pinning product is the only one in this section with no account and no invoice.
Storage is ordered on chain and served by staked nodes, so the thing that
normally ends a pinning relationship — a company deciding to stop — has no
obvious counterpart.

## A wallet signature in place of a token

Crust's W3Auth pinning service implements the standard
[Pinning Service API](/wiki/cs/ipfs/pinning/pinning-service-api) surface and
then replaces the one part that assumes a vendor. The specification says the
`Authorization` header carries a bearer token; Crust carries a signature
instead:

```text
Authorization: Bearer base64(ChainType-PubKey:SignedMsg)
```

`SignedMsg` is the public key signed by its own private key, so the header
proves control of an address rather than possession of something a company
issued. Substrate chains, Ethereum, Solana, Polygon, Near, Avalanche, and Aptos
are all accepted, which means an application that already has a connected wallet
has everything it needs to authenticate.

Because the surrounding shape is unchanged, Kubo still talks to it as an
ordinary remote service — the token is constructed rather than copied from a
dashboard:

```bash
ipfs pin remote service add crust https://pin.crustcode.com/psa "$SIGNED_TOKEN"
```
 A matching W3Auth [gateway](/wiki/cs/ipfs/gateways) accepts
the same header for write operations over HTTP.

## What the guarantee actually is

Nodes stake the network's native token and are rewarded for holding the files
covered by on-chain storage orders, with the order recording what should be
stored and for how long. Retention therefore depends on the network's economics
continuing to make storing that order worthwhile, rather than on a contract with
a named counterparty.

"No invoice" is not "no cost": placing a storage order means holding and
spending the network's native token, so a billing relationship is replaced by an
exposure to a token price rather than removed.

The assurance is a different risk rather than an absent one, and weaker than the
[Filecoin](/wiki/economics/finance/defi/filecoin) equivalent in the sense that
matters: Filecoin providers post recurring proofs against a deal and lose staked
collateral for failing them, which gives an outside observer something to check.
Crust's rests on the network's own accounting. For a
[content identifier (CID)](/wiki/cs/ipfs/cid) whose loss would matter, this is a
[second pin](/wiki/cs/ipfs/pinning/providers#an-arrangement-that-survives-the-list-above)
rather than the only one.

## Self-hosting the endpoint

The pinning service is open source and deployable, which makes it one of the few
ways to run a Pinning Service API endpoint that authenticates arbitrary wallets
without building the auth layer. Pointed at a local
[IPFS Cluster](/wiki/cs/ipfs/pinning/ipfs-cluster), it turns a private cluster
into something an application's users can pin to with a signature.

## External links

- [crust.network](https://crust.network/) and [wiki](https://wiki.crust.network/)
- [IPFS W3Auth pinning service](https://wiki.crust.network/docs/en/buildIPFSW3AuthPin)
- [crustio/ipfs-w3auth-pinning-service](https://github.com/crustio/ipfs-w3auth-pinning-service)
