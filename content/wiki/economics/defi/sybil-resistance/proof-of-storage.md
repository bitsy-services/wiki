---
title: "Proof of Storage"
weight: 40
---

A proof of storage is a protocol by which a party holding someone else's data shows that it still holds it, without sending the data back. The holder is sent a challenge that names a few randomly chosen pieces of the file, and it returns a short answer that it could compute only from those pieces. The checker compares the answer with a small amount of information kept from when the file was first handed over.

On a blockchain the same proofs can do a second job. If the network counts each participant's proven storage and gives it a proportional chance of producing blocks, stored data becomes the scarce resource that weights consensus, and the scheme is a [Sybil-resistance mechanism](/wiki/economics/defi/sybil-resistance). Filecoin and Arweave work this way. Where the proofs only settle storage contracts and blocks are produced by other means, as on Sia, they are an audit and nothing more.

The data is what separates this from [proof of space](/wiki/economics/defi/sybil-resistance/proof-of-space). There a participant fills its disk with filler it generated itself. Here the disk holds data that somebody wants kept, which is more useful and considerably harder to prove.

## Checking a file by sampling

Two papers from 2007 defined the basic proof.

Ateniese and co-authors called theirs *provable data possession*: a scheme "that allows a client that has stored data at an untrusted server to verify that the server possesses the original data without retrieving it." The client keeps a constant amount of metadata. For each check the server is asked about a random sample of blocks, and its answer is small whatever the size of the file.

Sampling is enough because of how the odds work. If a server has deleted 1% of the blocks of a file, a random sample of 460 blocks includes a deleted one with probability greater than 99%, and 300 blocks give 95%. Those figures do not depend on the size of the file.

Juels and Kaliski defined a *proof of retrievability*, which aims at a slightly stronger statement: that the server "retains and reliably transmits file data sufficient for the user to recover F in its entirety." Their scheme adds an [error-correcting code](/wiki/cs/erasure-coding) to the file, so that the small amount of damage a sample might miss can be repaired.

Both guarantees are probabilistic, and both are a statement about the moment of the challenge.

## What changes on an open network

In those papers the client pays the server, and the client checks. On a storage blockchain the network pays providers in newly issued currency, in proportion to the storage they claim. Providers then have a reason to claim storage they are not providing. Filecoin's 2017 whitepaper names three ways:

- **Sybil attack.** A provider pretends "to store (and get paid for) more copies than the ones physically stored by creating multiple Sybil identities, but storing the data only once."
- **Outsourcing attack.** A provider commits to more data than it holds and fetches it quickly from another provider when challenged.
- **Generation attack.** A provider that can choose the data stores a short program that regenerates it on demand.

A plain possession proof passes in all three cases.

## Proof of replication

The answer is to make each provider's copy physically different. Before storing a file, the provider puts it through a slow encoding keyed to its own identity, and stores the encoded result, the *replica*. Two providers holding the same file hold different bytes, and one provider posing as two would need two encodings. Filecoin calls the encoding *sealing*, and its specification says the resulting proof "ties together: i) the data itself, ii) the miner actor that performs the sealing and iii) the time when the specific data has been sealed".

The encoding has to be slow enough that it cannot be redone inside the time allowed for answering a challenge. A provider that discarded the replica and kept the original could otherwise re-encode on demand.

Ben Fisch, who formalized the idea, defines a proof of replication as a proof that a prover "is dedicating unique resources to storing one or more retrievable replicas of a data file", and describes it as a combination: it "embeds a PoR within a PoS", a proof of retrievability inside a proof of space. He is direct about its limit. Proofs of replication "fundamentally cannot guarantee that the data is stored redundantly", because a provider could always keep its replicas in some correlated form it knows how to undo. What the scheme achieves is that cheating saves the provider nothing. The security is economic.

## Proof over time: Filecoin

A replica proven once could be deleted the next day. Filecoin's *Proof of Spacetime* repeats the check for as long as the provider claims the storage, in two forms.

**WindowPoSt** is the standing audit. "Every 24-hour period is called a 'proving period' and is broken down into a series of 30min, non-overlapping deadlines, making a total of 48 deadlines". Each unit of storage, called a sector and normally 32 or 64 GiB, is assigned to one deadline and stays there. The schedule is public, and what the provider cannot know in advance is which parts of the sector will be asked for. Missing a proof has a price: "Failing to submit WindowPoSt for a sector will result in a fault, and the storage miner supplying the sector will be slashed", meaning part of its collateral is forfeited and its counted storage reduced.

**WinningPoSt** is asked only of a provider that has just been selected to produce a block. It must answer "within a short deadline, making it impossible for the miner to seal and find the answer to the challenge on demand."

The specification states the logic of the whole arrangement in economic terms. Regular proofs make it "irrational for a miner to not keep a sealed copy of the data", since sealing again for every challenge costs more than storing.

The proofs themselves would be far too large to put on a chain. Filecoin compresses them with succinct proofs of the kind described under [Groth16](/wiki/economics/defi/development/groth16), so that the chain checks a short proof that the long one exists.

## Storage as voting weight

Filecoin's block production elects leaders "from a weighted set in proportion to their power", where "power is equivalent to storage provided over time." A provider with 1% of the proven storage produces about 1% of the blocks.

Three details complicate the picture of storage as the resource.

- **Empty sectors count.** A provider may seal a sector that holds no customer data, called committed capacity, and it earns power like any other. At that point the scheme is a proof of space. Data from approved customers counted ten times as much in the launch-era rules.
- **Stake is required as well.** Hardware alone was judged too easy to repurpose to serve as the thing an attacker stands to lose. "Filecoin also uses upfront token collaterals, as in proof-of-stake protocols, proportional to the storage hardware committed."
- **Finality comes from a separate vote.** Filecoin's chain gave only probabilistic finality, with blocks treated as irreversible after 900 epochs, or 7.5 hours. Since 29 April 2025 a voting protocol specified in Filecoin Improvement Proposal 86 (FIP-0086) runs beside it and is expected to finalize blocks "within tens of seconds during regular network operation". Votes are weighted by storage power. It is a [finality gadget](/wiki/economics/defi/consensus#finality-or-availability) in the same sense as Ethereum's.

The [Filecoin](/wiki/economics/defi/chains/filecoin) page covers the storage market itself, and what these proofs do not show, which is that a customer can get the data back promptly.

## Arweave

Arweave ties mining to stored data more directly. A miner earns the right to try for a block by reading randomly selected chunks of the network's existing data, so a miner without the data cannot compete.

In the current design the data is divided into partitions of 3.6 terabytes, and a miner stores each partition in a form encoded with its own address, which is Arweave's counterpart to sealing. A Verifiable Delay Function (VDF), a computation that takes a fixed time and cannot be sped up by adding machines, releases a limited number of attempts per partition per second. The documentation calls it "a form of cryptographic 'speed limit'" which "ensures that mining is bottlenecked by storage volumes rather than pure data retrieval speed." A miner's power is then, in the words of the 2023 protocol paper, "proportional to the number of replicas of the weave accessible by a miner".

That paper names the mechanism Succinct Proofs of Replications. Arweave's documentation still uses the earlier name, Succinct Proofs of Random Access. The [Arweave](/wiki/economics/defi/chains/arweave) page follows the history of the design and the endowment that pays for it.

## Sia: the audit without the weighting

Sia stores only contracts on its chain. A host agrees to keep a client's data and to prove it, and "network consensus can be used to automatically enforce storage contracts", paying the host for a proof and penalizing it for a miss. The proofs take no part in deciding who makes blocks. Sia's blocks are produced by [proof of work](/wiki/economics/defi/sybil-resistance/proof-of-work).

The same proof technique appears in all three networks. Only where proven storage is counted toward block production does it answer the Sybil question.

## Limits

**Possession is not service.** Every proof here shows that bytes exist on a provider's disk at the moment of a challenge. None shows that the provider will hand them over when asked, or quickly.

**The guarantees are economic.** Replication cannot be proven outright, and continuous storage is enforced by making the alternative more expensive. A provider for whom cheating is cheaper than expected is outside the model.

**Sealing has a cost of its own.** Filecoin's documentation describes the first sealing step for a 32 GiB sector as the most processor-intensive part of the pipeline, needing 384 GiB of scratch space. The encoding that makes a replica unique is computation spent on nothing else.

## Sources

- Ateniese, Burns, Curtmola, Herring, Kissner, Peterson & Song, [Provable Data Possession at Untrusted Stores](https://eprint.iacr.org/2007/202) (2007)
- Juels & Kaliski, [PORs: Proofs of Retrievability for Large Files](https://eprint.iacr.org/2007/243) (2007)
- Protocol Labs, [Filecoin: A Decentralized Storage Network](https://web.archive.org/web/20240130052657/https://filecoin.io/filecoin.pdf) (19 July 2017)
- Fisch, [PoReps: Proofs of Space on Useful Data](https://eprint.iacr.org/2018/678) (2018)
- Filecoin specification, [Proof-of-Storage](https://spec.filecoin.io/algorithms/pos/), [Expected Consensus](https://spec.filecoin.io/algorithms/expected_consensus/) and [Miner Collaterals](https://spec.filecoin.io/systems/filecoin_mining/miner_collaterals/), read 10 October 2026. The specification was last revised in substance some years ago
- Filecoin documentation, [Sealing pipeline](https://docs.filecoin.io/storage-providers/architecture/sealing-pipeline), read 10 October 2026
- [FIP-0086: Fast Finality in Filecoin (F3)](https://github.com/filecoin-project/FIPs/blob/master/FIPS/fip-0086.md), and the [go-f3 README](https://github.com/filecoin-project/go-f3/blob/main/README.md) for the activation date
- Williams, Kedia, Berman & Campos-Groth, [Arweave: The Permanent Information Storage Protocol](https://www.arweave.org/files/arweave-lightpaper.pdf) (draft 17, 26 December 2023), and [Arweave documentation](https://docs.arweave.org/), read 10 October 2026
- Vorick & Champine, [Sia: Simple Decentralized Storage](https://sia.tech/sia.pdf) (2014)
