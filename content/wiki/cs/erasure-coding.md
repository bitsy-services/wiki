---
title: "Erasure Coding"
weight: 50
---

Erasure coding protects stored or transmitted data by computing extra pieces from it. The data is cut into *k* pieces of equal size, and *m* more pieces of the same size are calculated from them, each a different arithmetic combination of all *k*. The *k* + *m* pieces go to separate disks, machines or network packets, and the original can be rebuilt from any *k* of them. Any *m* pieces can be lost, and the total stored is (*k* + *m*) / *k* times the size of the data.

Facebook's data warehouse encoded its least-read data with *k* = 10 and *m* = 4: fourteen pieces on fourteen machines, 1.4 times the data stored, and any four of the machines could fail. Three full copies of the same data take 3 times the space and survive the loss of two.

The name is from coding theory. An *erasure* is a piece known to be missing, and an *error* is a piece that is present and wrong with no mark on it. A code with *m* computed pieces makes up for *m* erasures and for half as many errors, and storage systems are arranged so that every fault reaches the code as an erasure.

## How any k pieces can be enough

Take two numbers to protect, *a* = 5 and *b* = 9, so that *k* = 2. Treat them as two points on a straight line, *a* at *x* = 0 and *b* at *x* = 1. The line climbs 4 with each step, and its next two points are the computed pieces:

```text
x        0    1    2    3
piece    5    9   13   17
         a    b   computed
```

Any two of the four points fix the line, and the line gives back *a* and *b*. With only 13 and 17 left, at *x* = 2 and *x* = 3, the step is 4, so the line passes through 9 at *x* = 1 and 5 at *x* = 0. With 5 and 17 left, three steps apart, the step is (17 − 5) / 3 = 4 and the value at *x* = 1 is 9. The other four pairs go the same way.

This is a **Reed–Solomon code**, named for the 1960 paper by Reed and Solomon, with *k* = 2 and *m* = 2. For a larger *k* the line becomes a polynomial of degree less than *k*. The *k* data values are its values at the first *k* points, the *m* computed pieces are its values at *m* further points, and any *k* points determine such a polynomial, as two fix a line and three a parabola.

Written as equations, the computed pieces above are 13 = 2*b* − *a* and 17 = 3*b* − 2*a*. Every piece is a weighted sum of the data, and decoding solves *k* equations for *k* unknowns. Had the fourth piece been 2*b* − *a* again, the third and fourth together would be one equation written twice, and two unknowns cannot be recovered from one equation. A code has to guarantee that every choice of *k* pieces gives *k* independent equations. Taking the pieces from one polynomial provides the guarantee. Weights chosen another way have to be proved to have it: Plank's 1997 tutorial on implementing Reed–Solomon coding printed a weight matrix that lacked the property it claimed, and the correction followed in 2003.

On whole numbers the computed pieces outgrow the data: with one-byte values, 3*b* − 2*a* ranges from −510 to 765. Wrapping the results at 256 keeps them in a byte and breaks decoding, since division is not defined for every pair of values in arithmetic modulo 256. Implementations do the same algebra in a finite field: for one-byte values, a set of 256 values with its own addition and multiplication, under which every sum and product is again one of the 256 and every division by a non-zero value has one answer. Addition in that field is the bitwise exclusive-or (XOR) of the two bytes. A computed piece is then the same size as a data piece. The field needs more elements than the code has pieces, which caps one set of pieces at about 255 for one-byte values.

With one computed piece no polynomial is needed. The piece is the sum of the data pieces with every weight 1, which in this field is their XOR, and the XOR of whichever pieces remain reproduces a lost one. RAID (redundant array of inexpensive disks) does this at level 5 and calls the computed piece *parity*, the name storage papers also give to computed pieces of other kinds. A second XOR would be a copy of the first, so surviving two losses takes a second combination with different weights.

In a storage system a piece is a whole block. Facebook's were 256 MB each, and the code ran once per byte position: byte *i* of each of the ten data blocks produced byte *i* of each of the four computed blocks.

A code whose first *k* pieces are the data itself, unmodified, as 5 and 9 are above, is called *systematic*. A read that finds every data piece does no decoding.

Whoever holds those pieces can read them. Erasure coding provides no secrecy, although splitting a file into pieces can look like a secrecy measure: the data pieces of a systematic code are the data in the clear, and a computed piece is a known combination of it. Secrecy has to be added separately, by encrypting the data before it is encoded.

## The limit is k

*k* pieces of size 1/*k* hold as many bytes as the data does, and fewer pieces hold fewer, so no code can rebuild from fewer than *k*. A code that reaches that floor, where any *k* pieces suffice, is **maximum distance separable (MDS)**. Reed–Solomon codes are MDS. The [local reconstruction code](#local-parity) described further down is not: some sets of *k* of its pieces cannot rebuild the data.

Below *k* pieces the decoder has fewer equations than unknowns, and no approximation of the missing data comes out. A systematic code still returns whichever data pieces survived, and those are the only bytes of the original left.

Papers disagree on how to write the parameters. Coding theory writes (*n*, *k*) with *n* the total, so a (4, 2) code has four pieces. Storage papers write (data, parity), so a (12, 4) code has sixteen pieces and Facebook's (10, 4) has fourteen. This page writes 10 + 4.

## Against keeping copies

| Scheme | Reported at | Bytes stored per byte of data | Losses survived | Bytes read to rebuild one lost byte |
|---|---|---|---|---|
| Three full copies | | 3 | any 2 | 1 |
| Reed–Solomon 6 + 3 | Google | 1.5 | any 3 | 6 |
| Reed–Solomon 10 + 4 | Facebook | 1.4 | any 4 | 10 |
| Reed–Solomon 12 + 4 | | 1.33 | any 4 | 12 |
| Local reconstruction code 12 + 2 + 2 | Azure | 1.33 | any 3 | 6, for a data piece |

The Google and Azure rows come from a 2012 paper by the team behind Azure Storage, the storage service of Microsoft's cloud, called Azure from here on. The last row is the code that paper introduced: 12 data pieces, 2 parities that each cover half of them, and 2 that cover all 12.

Full copies are the *k* = 1 case of the same idea: *n* copies is a code in which any one of *n* pieces rebuilds the data. Raising *k* at a fixed overhead spreads the same redundancy over more machines. At 2 times the data, a file kept as two copies is gone when the two machines holding it fail, and a file under an 8 + 8 code is gone only when nine of its sixteen machines do. Weatherspoon and Kubiatowicz worked this through in 2002 for disks that fail independently and are repaired on a schedule: at the same storage overhead and repair interval, the erasure-coded system's mean time to failure came out "many orders of magnitude" higher.

The last column is the cost of repair, taken up [further down](#repair-reads-k-times-what-it-rebuilds). Reads are affected too. A read aimed at a piece whose machine is down has no second copy to go to, and Azure rebuilds the piece on demand from enough of the others.

Neither Facebook nor Azure encoded data as it arrived. Facebook kept its most frequently read data as three copies, to make its batch jobs easier to schedule, and encoded data that had gone three months without being read. Azure writes three copies of data that is still being appended to, encodes a chunk in the background once it is full and sealed against further writes, and then deletes the copies.

Whole copies are still what several peer-to-peer storage networks keep. In an [IPFS Cluster](/wiki/cs/ipfs/pinning/ipfs-cluster), a group of storage nodes that share one list of content to keep, the replication factor counts peers that each hold the entire object. The paper describing [Walrus](/wiki/economics/defi/chains/sui/walrus), a decentralized storage network for large files, classes [Filecoin](/wiki/economics/defi/chains/filecoin) and [Arweave](/wiki/economics/defi/chains/arweave) as replication systems. It gives the reason too. In a network that nodes join and leave freely, a node with a complete copy can serve it, or pass it to a replacement node, without depending on any other node.

## A wrong piece costs more than a missing one

The decoder has to be told which pieces it holds. Given that, *m* parity pieces fill any *m* gaps. When some pieces are present and wrong and the decoder is left to find them, a Reed–Solomon code corrects at most *m* / 2.

Storage systems keep the code out of that mode. Each piece is stored with a checksum or a hash, a piece that fails its check is discarded, and the corruption has become an erasure. Content addressing gives the same result by construction: a piece named by its hash, the way a [content identifier (CID)](/wiki/cs/ipfs/cid) names a block, is verified by whoever fetches it.

A hash catches a storage node that returns the wrong bytes. A writer who encodes the pieces inconsistently, so that different sets of *k* decode to different data, passes every per-piece check. Where the writer is untrusted, readers check the encoding as well. A Walrus reader decodes the file, encodes it again, and recomputes a commitment, a short value bound to the content, for every piece. If those differ from the commitments recorded when the file was written, the read returns no data.

## Repair reads k times what it rebuilds

When a machine dies under replication, its data is copied from another replica: one byte read for each byte restored. A Reed–Solomon code has no replica to copy from. Rebuilding one lost piece means fetching *k* surviving pieces, as many bytes as the whole original, to compute a piece 1/*k* that size.

A 2013 study measured the effect in Facebook's warehouse. A *stripe* is one set of *k* + *m* pieces encoded together, and of the stripes with a block missing, 98.08% were missing only one. Each such repair downloaded ten blocks from ten other racks. In one of the warehouse's two clusters, the daily medians over 24 days were 95,500 blocks rebuilt and more than 180 terabytes moved between racks for the rebuilding. The study's authors give that traffic as the main obstacle to erasure-coding more of the warehouse.

Other codes lower the repair cost.

### Local parity

Azure's **local reconstruction code (LRC)** splits 12 data pieces into two groups of 6, gives each group a *local* parity of its own, and adds 2 *global* parities computed over all 12. A lost data piece is rebuilt from the other 5 in its group and the group's parity: 6 pieces read, where a 12 + 4 Reed–Solomon code at the same 1.33 times overhead reads 12.

The any-*k* property goes. Sixteen pieces with four parities survive any 3 losses and only some patterns of 4. Losing three data pieces from one group together with that group's local parity leaves the two global parities as two equations for three unknowns.

### Regenerating codes

Dimakis and co-authors showed that the *k*-fold cost is not forced on a code that keeps the any-*k* property. If each surviving node sends a computed combination of what it holds in place of the piece itself, the replacement node needs less than the whole. In their four-piece, *k* = 2 example, building a replacement piece takes a download three-quarters the size of the data, where plain decoding downloads all of it. Nodes that store somewhat more than 1/*k* of the data can be repaired with less traffic still. The paper derives the curve along which storage and repair traffic trade, and names the codes on that curve *regenerating codes*.

### A second dimension

Walrus arranges a file as a grid of small equal units and encodes it twice, once along the columns and once along the rows, so that each node holds one row piece and one column piece. Its paper calls the scheme Red Stuff. A node that lost its pieces rebuilds them from single units fetched from the other nodes, and repair traffic falls from the size of the file to the size of what was lost.

Walrus assumes that up to a third of its nodes may be faulty and that the network may delay messages for any length of time. A one-dimensional code under those assumptions has to be decodable from a third of its pieces, and so stores 3 times the file. Red Stuff stores 4.5 times.

## Data availability sampling

[Blockchains](/wiki/economics/defi/blockchain) use the same codes for a different job. A node should accept a block only if the block's transaction data was published, since whoever produced the block can hide an invalid transaction by withholding a few bytes. Downloading every block in full settles the question. Data availability sampling is the way around the download: the node fetches a few randomly chosen pieces and infers that the rest were published. On raw data the inference fails, because a random sample will almost never land on a few withheld bytes.

Extending the data to twice its length with a Reed–Solomon code changes the odds. Any half of the pieces rebuilds the rest, so making even one byte unrecoverable means withholding more than half of them. Each random sample then lands on a withheld piece with probability above one half. If the data were unrecoverable, the chance that thirty samples in a row all succeed would be under one in a billion.

The 2018 paper that proposed sampling, by Al-Bassam, Sonnino and Buterin, presents this version first and then sets it aside. A producer can also compute the extension wrongly, and with a one-dimensional code the proof of that is the whole block. Their proposal encodes the data in two dimensions so that the proof is a single row or column, and the threshold drops: withholding a little over a quarter of the pieces is then enough to lose data. In both versions there have to be enough samplers that the pieces they hold between them can rebuild the block. The paper adds that a short proof of correct encoding, attached by the producer, would remove the reason for the second dimension.

Ethereum's sampling protocol, [PeerDAS](/wiki/economics/defi/chains/ethereum/blobs#peerdas) (peer data availability sampling), is one-dimensional. It applies to blobs, the fixed-size chunks of data that ride alongside Ethereum transactions. Each blob is extended to twice its length and cut into 128 pieces, any 64 of which rebuild the rest, and every piece carries a proof that it matches a commitment to its blob.

A PeerDAS node downloads the pieces at 8 or more of the 128 positions, some of them fixed by the node's own identifier, so the thirty-sample arithmetic above does not describe a single node. The protocol's security argument is about the network. It bounds the chance that a producer who withholds data convinces a given fraction of the nodes that the data is available, and that chance falls as the network grows.

[IOTA Rebased](/wiki/economics/defi/chains/iota/iota-rebased#consensus-mysticeti-to-starfish), another blockchain, uses a Reed–Solomon code with acknowledgements in place of sampling. Its Starfish protocol splits a block's transaction data into fragments, one for each validator (a machine that votes on blocks). The data is certified available once enough validators have acknowledged it that the honest ones among them must hold enough fragments to rebuild it.

## Other names

| Name | What it refers to |
|---|---|
| Forward error correction (FEC) | The same codes on a transmission link: computed packets sent along with the data, so the receiver can make up losses without a resend |
| Information dispersal algorithm (IDA) | Rabin's 1989 name for splitting a file into *n* pieces of which any *k* rebuild it |
| Maximum distance separable (MDS) code | Any code in which every *k* of the *n* pieces suffice |
| Parity, *k*-of-*n* | The terms used for storage products; RAID 5 is the one-parity case |

## Check

Run the example and confirm that all six pairs of pieces decode:

```python
from fractions import Fraction
from itertools import combinations

a, b = 5, 9
# (weight on a, weight on b, stored value)
pieces = [(1, 0, a), (0, 1, b), (-1, 2, 2 * b - a), (-2, 3, 3 * b - 2 * a)]

for (p1, q1, v1), (p2, q2, v2) in combinations(pieces, 2):
    det = p1 * q2 - p2 * q1
    print(Fraction(v1 * q2 - v2 * q1, det), Fraction(p1 * v2 - p2 * v1, det))
```

It prints `5 9` six times. Change the last piece to `(-1, 2, 2 * b - a)` and the final pair raises `ZeroDivisionError`. The two computed pieces are now the same equation, and the determinant the solver divides by is zero.

## Sources

- Reed & Solomon, [Polynomial Codes Over Certain Finite Fields](https://doi.org/10.1137/0108018), *Journal of the Society for Industrial and Applied Mathematics* 8(2), 300–304 (1960)
- Rabin, [Efficient Dispersal of Information for Security, Load Balancing, and Fault Tolerance](https://doi.org/10.1145/62044.62050), *Journal of the ACM* 36(2), 335–348 (1989)
- Plank, A Tutorial on Reed–Solomon Coding for Fault-Tolerance in RAID-like Systems, *Software: Practice and Experience* 27(9), 995–1012 (1997), and Plank & Ding, [Note: Correction to the 1997 Tutorial on Reed–Solomon Coding](https://doi.org/10.1002/spe.631), *Software: Practice and Experience* 35(2), 189–194 (2005), first issued as a technical report in April 2003
- Weatherspoon & Kubiatowicz, [Erasure Coding vs. Replication: A Quantitative Comparison](https://doi.org/10.1007/3-540-45748-8_31), International Workshop on Peer-to-Peer Systems (2002)
- Dimakis, Godfrey, Wu, Wainwright & Ramchandran, [Network Coding for Distributed Storage Systems](https://doi.org/10.1109/TIT.2010.2054295), *IEEE Transactions on Information Theory* 56(9), 4539–4551 (2010); [arXiv:0803.0632](https://arxiv.org/abs/0803.0632)
- Huang et al., [Erasure Coding in Windows Azure Storage](https://www.usenix.org/conference/atc12/technical-sessions/presentation/huang), USENIX Annual Technical Conference (2012)
- Rashmi et al., [A Solution to the Network Challenges of Data Recovery in Erasure-coded Distributed Storage Systems: A Study on the Facebook Warehouse Cluster](https://www.usenix.org/conference/hotstorage13/workshop-program/presentation/rashmi), USENIX HotStorage (2013)
- Al-Bassam, Sonnino & Buterin, [Fraud and Data Availability Proofs: Maximising Light Client Security and Scaling Blockchains with Dishonest Majorities](https://arxiv.org/abs/1809.09044) (2018)
- Danezis et al., [Walrus: An Efficient Decentralized Storage Network](https://arxiv.org/abs/2505.05370) (2025)
- [EIP-7594: PeerDAS](https://eips.ethereum.org/EIPS/eip-7594), the Ethereum Improvement Proposal (EIP) that specifies the one-dimensional extension and the per-piece proofs
- IOTA Foundation, [Why Starfish Matters](https://blog.iota.org/why-starfish-matters/)
