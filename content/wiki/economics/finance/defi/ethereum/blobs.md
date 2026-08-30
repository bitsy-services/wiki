---
title: "Blobs"
weight: 6
---

A blob is 128 KiB of data that an [Ethereum](/wiki/economics/finance/defi/ethereum/)
block commits to and then forgets. It rides alongside a transaction rather than
inside it: the [EVM](/wiki/economics/finance/defi/ethereum#the-ethereum-virtual-machine-evm)
cannot read it, no contract can store it, and consensus clients delete it after
about 18 days. EIP-4844, an [Ethereum Improvement Proposal](/wiki/economics/finance/defi/ethereum/eip)
shipped in the Dencun upgrade on 13 March 2024, added them to give
[rollups](/wiki/economics/finance/defi/ethereum#scalability-and-layer-2) somewhere
to publish transaction data other than calldata, which every node stores forever
and which costs 16 gas per non-zero byte.

## What a blob contains

A blob is exactly 4096 field elements of 32 bytes each: 131,072 bytes, 128 KiB,
fixed. There is no shorter blob and no longer one, so a rollup with 20 KiB to
publish pays for 128 KiB.

The field elements are not arbitrary 32-byte words. Each is an integer modulo
the BLS12-381 scalar field order, a prime just under 2<sup>255</sup>, so a word
with its top bits set is not a valid blob. Encoders sidestep this by filling 31
bytes per element and leaving the leading byte zero, which puts the usable
payload at 4096 × 31 = 126,976 bytes and spends 3.1% of the space on the
constraint.

Past that, the protocol assigns the bytes no meaning. Ethereum never parses a
blob, and two rollups sharing a block can compress theirs in completely
different ways.

## The block commits to the blob without carrying it

Blob transactions are type `0x03`. Beyond the fields every transaction has, the
signed body of one carries a `max_fee_per_blob_gas` limit and a list of 32-byte
**versioned hashes**, one per blob — and no blob data. The blobs themselves
travel as *sidecars*: separate consensus-layer gossip messages, propagated on
their own subnets and referenced by the beacon block.

A versioned hash is the byte `0x01` followed by the last 31 bytes of
`sha256(commitment)`. The commitment is a Kate-Zaverucha-Goldberg (KZG)
commitment: 48 bytes, a point on the BLS12-381 curve, binding the polynomial
whose evaluations at the 4096th roots of unity are the blob's field elements.
The version byte is there so a later commitment scheme can replace KZG without
changing the 32-byte shape contracts already handle.

An execution client can therefore validate a block having downloaded no blob
data whatsoever, because everything it needs is the hashes inside the
transaction. Whether the data was actually published is a separate question,
answered by the consensus layer, and the two never mix.

## What the EVM can do with one

Two pieces of machinery, and nothing else:

- **`BLOBHASH`** (opcode `0x49`, 3 gas) pushes the versioned hash of the *i*-th
  blob attached to the current transaction. A contract can learn which blobs its
  caller published; it cannot learn what is in them.
- **The point evaluation precompile** at address `0x0A` (50,000 gas) takes a
  versioned hash, an evaluation point `z`, a claimed value `y`, the 48-byte
  commitment and a 48-byte proof, and succeeds only if the committed polynomial
  really evaluates to `y` at `z`.

Between them a contract verifies claims about data it has never seen. Evaluating
at one of the 4096 roots of unity pins down a single field element, so a fraud
proof can be settled on one disputed 32-byte word instead of on 128 KiB of
republished data; evaluating at a random point outside them establishes, with
overwhelming probability, that a claimed 4096-element vector is the whole blob.
Optimistic rollups use the first to keep challenge games small,
[zero-knowledge](/wiki/cs/zero-knowledge-proofs#rollups) rollups the second to
bind a validity proof to the exact bytes that were published.

## Two fee markets

Blob space is priced in **blob gas**, which has nothing to do with execution
gas. One blob costs `GAS_PER_BLOB` = 2<sup>17</sup> = 131,072 blob gas, one unit
per byte, and the price per unit runs its own EIP-1559-style controller:

```text
base_fee_per_blob_gas = MIN_BASE_FEE_PER_BLOB_GAS * e^(excess_blob_gas / BLOB_BASE_FEE_UPDATE_FRACTION)
```

`excess_blob_gas` is a running total of how far past the per-block target the
chain has gone, carried block to block, and the response to it is exponential
rather than linear. The floor `MIN_BASE_FEE_PER_BLOB_GAS` is 1 wei, which puts a
blob at the floor at 131,072 wei — 1.3 × 10<sup>-13</sup> ETH, a fraction of a
millionth of a cent at any price ETH has traded at. Demand sat below target for
most of 2024 and blobs cleared at that floor, which is how [L2](/wiki/economics/finance/defi/micro-transactions#layer-2-rollups)
fees fell 90–95% in the months after Dencun.

The independence is real in both directions: a congested execution layer does
not raise the price of blob space, and a rollup saturating the blob market does
not raise the price of a token swap. Blob base fees are burned like execution
base fees, and there is no priority fee on blob gas at all — a proposer earns
nothing extra for carrying blobs beyond the transaction's ordinary tip. At the
floor the burn rounds to zero, so moving rollup data out of calldata and into
blobs removed most of what rollups had been contributing to ETH issuance
pressure.

## Raising the ceiling

Two of the five configurations below cost almost nothing to ship, because
EIP-7892 defines a **blob-parameter-only (BPO)** fork: one that changes the
target, the max and the update fraction and nothing else, scheduled as a
configuration entry rather than a client release. Before it, adding blob
capacity meant a full network upgrade, which is why the max sat at 6 for the
fourteen months between Dencun and Pectra.

| Upgrade | Mainnet | Target | Max | Max data per slot |
|---|---|---|---|---|
| Dencun (EIP-4844) | 13 Mar 2024 | 3 | 6 | 768 KiB |
| Pectra (EIP-7691) | 7 May 2025 | 6 | 9 | 1,152 KiB |
| Fusaka (EIP-7594) | 3 Dec 2025 | 6 | 9 | 1,152 KiB |
| BPO1 | 9 Dec 2025 | 10 | 15 | 1,920 KiB |
| BPO2 | 7 Jan 2026 | 14 | 21 | 2,688 KiB |

`BLOB_BASE_FEE_UPDATE_FRACTION` is not a free parameter. Every value the chain
has shipped equals `MAX_BLOB_GAS_PER_BLOCK / (2 ln 1.125)` — 3,338,477 at a max
of 6 blobs, 5,007,716 at 9, 8,346,193 at 15, 11,684,671 at 21 — which fixes the
price at ×1.125 for each half-block of maximum capacity accumulated as excess.

Dencun set target and max at a 1:2 ratio, so a full block raised the price 12.5%
and an empty one cut it 11.1%. Every configuration since Pectra uses 2:3
instead, and the controller is correspondingly lopsided: a full block now raises
the price 8.2% and an empty one cuts it 14.5%, which is why the blob fee
collapses back to the floor within a few dozen blocks of a demand spike ending.

## PeerDAS

Under EIP-4844 every node downloads every blob, and the binding number is not
the average bandwidth but the burst — the whole set has to arrive within the
slot for the node to attest on time. Per-node bandwidth scaling one-for-one with
total throughput is what held the max at 9.

EIP-7594, shipped in Fusaka on 3 December 2025, breaks that coupling with peer
data availability sampling. Each blob is Reed-Solomon extended to twice its
length and cut into cells; taking the cell at a given index from every blob in
the block gives one of 128 **columns**, and because the extension is twofold,
any 64 columns rebuild the other 64. A node subscribes to 8 of the 128: it
custodies 4 as a floor and samples up to a total of 8 from its peers each slot,
refusing to attest to a block whose samples it cannot fetch. Nodes attached to
validators holding 4096 ETH or more must instead be *supernodes* and custody all
128.

Eight columns of a matrix twice the size of the blob data is an eighth of that
data. Before Fusaka a node pulled all 9 blobs at max, 1,152 KiB a slot; after
BPO2 it pulls an eighth of 21, about 336 KiB. Capacity went up 2.3× and every
node's bandwidth went down. Full danksharding is the endpoint of that
substitution — every node samples, none downloads the set — at 128 blobs a slot,
16 MiB. As of August 2026
the parameters are still 14 and 21: a third BPO fork has been specified but
deferred, with blob utilisation running at 20–30% of the capacity already
available.

## The 18-day window

Consensus clients must serve blob sidecars for
`MIN_EPOCHS_FOR_BLOB_SIDECARS_REQUESTS` = 4096 epochs. At 32 slots of 12 seconds
that is 1,572,864 seconds, a little over 18 days, after which they are free to
prune and in practice do.

What survives is the commitment. Beacon blocks keep the versioned hashes
permanently, so anyone still holding a blob can prove it is the one that was
published — but the network will not hand them a copy. The guarantee is that the
data *was* available long enough for anyone who wanted it to take it, not that
it stays retrievable.

An optimistic rollup's challenge window is seven days, comfortably inside the
18; a validity proof is checked at the moment it is posted.
Everything that wants the data later — block explorers, indexers, a rollup
rebuilding its state from genesis — keeps its own archive, and asks that archive
rather than the network. This is the sharpest difference between blobs and the
calldata they replaced, which sits in the chain's transaction history forever and
was priced accordingly, and a wider one still against
[Arweave](/wiki/economics/finance/defi/arweave), which sells permanence outright.

## Working with blobs

The canonical transaction encoding carries only versioned hashes; a separate
network encoding wraps the blobs, commitments and proofs around it. That is why
`eth_getTransactionByHash` never returns blob contents — the data was never in
the object being hashed. Blob bodies come from the beacon API instead, at
`/eth/v1/beacon/blob_sidecars/{block_id}`, and only inside the retention window;
past that, an indexer such as Blobscan is the only source.

A type-`0x03` transaction must carry at least one blob and cannot be a contract
creation: `to` is not nullable, unlike in every earlier transaction type. Blobs
are also indivisible, so a 5 KiB payload costs a whole one, which is part of why
rollups batch as aggressively as they do.

Fusaka changed the sidecar wire format from whole-blob proofs to the cell proofs
PeerDAS needs, and tooling now distinguishes the two: Foundry's `cast send
--blob --path <file>` sends the EIP-7594 form, and `--eip4844` alongside it
sends the legacy one.

## External links

- [EIP-4844: Shard Blob Transactions](https://eips.ethereum.org/EIPS/eip-4844) — the original specification, constants included.
- [EIP-7691: Blob throughput increase](https://eips.ethereum.org/EIPS/eip-7691) — the Pectra bump to 6/9.
- [EIP-7594: PeerDAS](https://eips.ethereum.org/EIPS/eip-7594) — data availability sampling.
- [EIP-7892: Blob Parameter Only Hardforks](https://eips.ethereum.org/EIPS/eip-7892) — the mechanism behind BPO1 and BPO2.
- [Blobscan](https://blobscan.com/) — blob explorer and archive.
- [Generalized base fee update fraction](https://rig.ethereum.org/post/generalized-base-fee-update-fraction) — where the update-fraction formula comes from.
