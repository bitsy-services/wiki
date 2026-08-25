---
title: "NFT"
weight: 9
---

A **non-fungible token (NFT)** is a token whose units are not interchangeable.
It is a claim about bookkeeping rather than about art: the contract records
which specific token belongs to whom, and says nothing about what it depicts.

## Fungible vs non-fungible

Fungibility is the property that any unit of a thing substitutes for any other.
One dollar is one dollar; one [ERC-20](/wiki/economics/finance/defi/ethereum/erc-20)
token is one ERC-20 token. A fungible token contract therefore needs to track
only a number per address:

```text
balances[alice] = 500
balances[bob]   = 120
```

A non-fungible contract tracks identity instead — which specific token belongs
to whom:

```text
owners[1] = alice
owners[2] = alice
owners[3] = bob
```

Alice holds two tokens, but "token 1" and "token 2" are distinct and a transfer
must name one. This is the same
[entity-addressing](/wiki/cs/entity-addressing) distinction that separates a
quantity from an identified object, applied to on-chain state.

The standard for this on Ethereum is
[ERC-721](/wiki/economics/finance/defi/ethereum/erc-721), which replaces
ERC-20's `transfer(to, amount)` with `transferFrom(from, to, tokenId)` and adds
`safeTransferFrom(from, to, tokenId)` — the variant that checks whether the
recipient can hold the token, covered under [pitfalls](#pitfalls) below.
[ERC-1155](/wiki/economics/finance/defi/ethereum/erc-1155) splits the
difference: one contract holds many token IDs, each with its own supply, so it
can represent both kinds at once.

## What the token actually contains

Almost nothing. An ERC-721 token is an ID, an owner, and a `tokenURI` — a
pointer to metadata held somewhere else. The image, the name, the traits: none
of it is on-chain in the typical case.

That pointer is where most of the risk lives. If `tokenURI` returns an HTTPS URL
on a server someone stops paying for, the token survives and its contents do
not. Pointing at [IPFS](/wiki/cs/ipfs) or
[Arweave](/wiki/economics/finance/defi/arweave) makes the reference
content-addressed, so the metadata cannot be silently swapped — though with IPFS
it still has to be pinned by somebody to remain retrievable. Arweave's
pay-once-store-forever model puts an endowment behind retention instead, which
is a stronger *commitment* than pinning but still an economic bet rather than a
guarantee — see the
[trade-offs](/wiki/economics/finance/defi/arweave#trade-offs-and-criticisms) on
that page.

A minority of collections store the image on-chain outright, usually as SVG
generated in the contract. Expensive, and immune to all of the above.

## Where they show up in DeFi

NFTs are used well beyond collectibles, and in most of these cases the
"non-fungible" part is doing real work:

- **Concentrated liquidity positions.** A
  [Uniswap](/wiki/economics/finance/defi/uniswap) v3 position is an NFT because
  each position covers its own
  [price range](/wiki/economics/finance/defi/virtual-reserves), bounded by two
  [ticks](/wiki/economics/finance/defi/uniswap/ticks), and accrues its own fees. Two positions in the same pool are genuinely
  not interchangeable, so an ERC-20
  [LP token](/wiki/economics/finance/defi/liquidity-pool) cannot represent them.
- **Locked liquidity receipts.** A
  [lock](/wiki/economics/finance/defi/locked-liquidity) is a specific amount
  with a specific unlock time.
- **Identity and naming.** Ethereum Name Service (ENS) names are NFTs; so are the registrations under
  [ERC-8004](/wiki/economics/finance/defi/ethereum/erc-8004).
- **Asset titles — sometimes.** Whole-title ownership is the natural NFT case,
  but it is not what the tokenization market mostly does:
  [smart contracts in real estate](/wiki/economics/finance/defi/smart-contracts-in-real-estate)
  models a property as *fungible* fractional shares, because divisibility and a
  liquid secondary market matter more there than a single indivisible deed.

## Pitfalls

Ordered worst-first.

- **Approval scope.** `setApprovalForAll` grants an operator every token in the
  collection, present and future, until revoked. It is the ERC-721 analogue of
  an unlimited ERC-20 allowance, and it is what most phishing signatures are
  after: one signature, the whole collection. Most NFT theft runs through this
  call rather than through a stolen key.
- **`transferFrom` to a contract that cannot handle it.** ERC-721 has no plain
  `transfer`. Bare `transferFrom` to a contract with no ERC-721 receiver hook
  strands the token: the contract is now the owner, and unless it happens to
  expose a rescue function there is no way to move it again. This is not a burn
  — a burn means sending to `address(0)`, which `transferFrom` rejects — but
  the practical result is usually the same.
  `safeTransferFrom` checks for the hook and reverts instead.
- **Metadata that isn't content-addressed.** As above: a mutable `tokenURI`
  lets the issuer change what a token depicts after it has been sold.
- **Royalties are not enforced on-chain.** ERC-2981 exposes a royalty *query*.
  Whether a marketplace honours it is a marketplace policy, not a protocol rule
  — the same voluntary-adoption property that governs every
  [ERC](/wiki/economics/finance/defi/ethereum/eip).

## External links

- [ERC-2981 royalty standard](https://eips.ethereum.org/EIPS/eip-2981)
- [OpenZeppelin ERC-721 implementation](https://docs.openzeppelin.com/contracts/5.x/erc721)
