---
title: "Filecoin"
weight: 51
---

Filecoin is the incentive layer that [IPFS](/wiki/cs/ipfs) deliberately does not
have. It keeps the addressing — same
[content identifiers (CIDs)](/wiki/cs/ipfs/cid), same
[Merkle DAGs](/wiki/cs/dag) — and adds a market where storing data is a dated
contract that the provider must keep proving it is honouring, on chain, or lose
staked collateral.

## Deals

A client and a storage provider agree a **deal**: a piece of data, a term
measured in days, a price in FIL, and collateral the provider pledges against
delivery. The provider takes the raw bytes and **seals** them into a sector — a
slow, deliberately expensive encoding that produces a copy unique to that
provider, so storing the same file twice cannot be faked by keeping one copy and
counting it twice.

Deals are recorded on the Filecoin chain, which makes the arrangement auditable
by anyone rather than only by the parties. That is the structural difference
from a [pinning service](/wiki/cs/ipfs/pinning/pinning-services), whose status
field is a row in its own database.

## The proofs

Two mechanisms run against sealed data:

- **Proof of Replication** runs once at sealing and establishes that the
  provider holds a physically distinct copy, not a deduplicated reference to
  somebody else's.
- **Proof of Spacetime** runs continuously afterwards, sampling sectors on a
  schedule the provider cannot predict. Miss enough of them and the pledged
  collateral is slashed.

The pair converts "we are storing your data" into a claim that fails visibly and
costs money. What neither proves is that anyone can *read* the data — a proof of
possession says nothing about the provider answering a retrieval request, and
unsealing a sector to serve one takes real time unless the provider also keeps
an unsealed copy on hand.

## Proof of Data Possession

That retrieval gap is what **Proof of Data Possession (PDP)**, live on mainnet
since May 2025, addresses. Data stays in raw, unsealed form, and providers post
frequent cheap proofs over it instead of the heavyweight sealing pipeline. A
challenge samples 160 bytes regardless of how large the dataset is, and proofs
can be added to, deleted, and modified incrementally rather than being
aggregated into a sector that has to be rebuilt.

The result is a hot tier: content that is meant to be served — dApp frontends,
[NFT](/wiki/economics/finance/defi/nft) media, AI training sets — with a
cryptographic answer to "is it still there" that a smart contract can check.
Filecoin Onchain Cloud, launched on 18 November 2025, is the product layer built
on it, and it is what recent pinning services mean when they say their pins are
"backed by Filecoin".

## Filecoin is not a drop-in for pinning

Three practical differences catch people:

- **A deal is not a pin.** Getting bytes into Filecoin does not make them
  retrievable over IPFS. Services that offer both run an IPFS node in front and
  a deal behind, and the IPFS half is what answers reads.
- **Retrieval was the weak leg for years**, which is the entire motivation for
  PDP and for the retrieval markets built alongside it. A pre-PDP deal is
  archival storage with a proof, not a content delivery network.
- **Terms end.** A deal covers a fixed number of epochs and someone has to renew
  it, which is the same recurring obligation a pinning subscription creates,
  moved on chain. [Arweave](/wiki/economics/finance/defi/arweave) is the
  alternative that tries to remove the renewal entirely by funding retention
  from an endowment — a stronger promise resting on a weaker foundation, since
  it is a forecast about storage prices rather than a contract.

## FIL

FIL pays for deals, denominates provider collateral, and funds block rewards.
Providers must lock collateral proportional to the storage they commit, which
ties the network's security to the token's value in the ordinary way and means a
sharp price decline raises the real cost of pledging new capacity.

## External links

- [filecoin.io](https://filecoin.io/) — project site
- [Filecoin documentation](https://docs.filecoin.io/)
- [Introducing Proof of Data Possession](https://filecoin.io/blog/posts/introducing-proof-of-data-possession-pdp-verifiable-hot-storage-on-filecoin/)
- [Filecoin specification](https://spec.filecoin.io/)
