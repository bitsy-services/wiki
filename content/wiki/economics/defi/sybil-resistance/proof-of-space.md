---
title: "Proof of Space"
weight: 30
---

A proof of space is a way for a participant to show that it has set aside a large amount of disk storage. The participant first fills the storage with data that it generates itself and that has no other use. Later, when sent a random challenge, it looks up a small part of that data and returns a short answer, which the challenger can check quickly. Answering from the stored data is cheap. Answering without it means regenerating the data, which is slow.

As a [Sybil-resistance mechanism](/wiki/economics/defi/sybil-resistance), it makes disk capacity the scarce resource. A participant's chance of producing the next block is its share of all the space committed to the network.

Dziembowski, Faust, Kolmogorov and Pietrzak introduced the idea as an alternative to [proof of work](/wiki/economics/defi/sybil-resistance/proof-of-work), "where a service requestor must dedicate a significant amount of disk space as opposed to computation." Their reasons were proof of work's energy use and the advantage it gives to specialized hardware, set against the observation "that users often have significant amounts of free disk anyway". The Chia network is built on it.

Storing useless filler is the defining feature. A scheme in which the stored data is something a customer wants kept is a [proof of storage](/wiki/economics/defi/sybil-resistance/proof-of-storage), and has different problems.

## Two phases

**Initialization.** The prover computes a large file from a seed tied to its own identity and writes it to disk. Chia calls this *plotting* and the files *plots*. Its smallest standard plot takes 101.4 GiB. Because the prover generates the data, the verifier never has to send it. The original paper points out that asking a prover to store a random file sent by the verifier would also show dedicated space, and would be useless in practice because of the bandwidth.

**Execution.** The verifier sends a challenge, the prover reads the relevant entries from disk and returns a proof, and the verifier checks it. This can be repeated as often as needed.

The guarantee has a condition that is easy to lose. Nothing forces a prover to keep the file between challenges. It could delete the file, store only the seed, and rebuild the file each time it is challenged. The paper's security definition is therefore an either/or: a cheating prover can succeed only if it "either uses N0 bits of storage in-between executions" or "invests time T for every execution". A proof of space shows space or time. The schemes are set up so that the time is long enough to miss the deadline for answering, which makes storing the rational choice.

## Why space alone is not enough for a blockchain

Swapping Bitcoin's puzzle for a proof of space does not give a secure chain. Chia's design paper states the reason: "for PoSpace (after plotting) it's extremely cheap to compute a proof for a given challenge." Work is spent on each attempt. Space, once plotted, answers any number of challenges at almost no cost. The paper calls proof systems of this kind *efficient* and notes that "the analogue issue with proof of stake is sometimes called 'nothing at stake'", a problem described under [proof of stake](/wiki/economics/defi/sybil-resistance/proof-of-stake#nothing-at-stake).

It lists three attacks that follow, each with its own countermeasure:

- **Grinding.** A block producer tries many variations of a block to find one that makes its own next challenge favourable. The countermeasure is to make challenges depend only on a part of the chain the producer cannot vary.
- **Double-dipping.** A producer extends several competing chains at once, since each extra attempt is free. The countermeasure limits how independent the challenges on different branches are.
- **Bootstrapping.** An adversary "can use its resource to create a chain at basically no cost", including a [long-range attack](/wiki/economics/defi/sybil-resistance/proof-of-stake#long-range-attacks) in which it "forks the chain at a point in the past and then 'bootstraps' it into the present." The countermeasure is to prove that time has passed between blocks.

## Proof of time

For the third attack Chia interleaves its proofs of space with a verifiable delay function (VDF), which it also calls a proof of time: "a proof that a sequential function was executed a certain number of times." The function is repeated squaring of a number. Each squaring needs the result of the one before, so "the prover cannot just add more machines to make the function execute faster", and the output shows that a period of real time went by. Checking the output is fast.

The machines that run the function are called *timelords*. A timelord publishes a new challenge, called a signage point, every 9.375 seconds. Each farmer, Chia's word for a prover, checks its plots against the challenge and submits any proof that qualifies. The target is 32 blocks every ten minutes, one per 18.75 seconds.

With the delay function in place, building an alternative chain takes as long as building the real one, however much space the attacker has. The security condition is accordingly a bound on the product of an attacker's space and the speed of its delay function relative to the honest network's. The design paper proves security when the honest side's product exceeds the attacker's by a factor of 1.47, and says a double spend is possible once the factor falls below 1.34. If the attacker's delay function is exactly as fast as the fastest honest timelord's, those factors correspond to an attacker with about 40.5% and about 43% of the total space.

## Trading computation back for space

The either/or in the definition reappears as an economic problem. A plot can be stored in reduced form, with some bits left out and recomputed on demand. A proposal in Chia's own process defines it: "Removing some bits of information from a stored plot, that is later re-created using compute to respond to challenges. Typically each bit dropped doubles the compute required". With graphics processors doing the recomputation, a farmer can hold far less disk per unit of apparent space. The same proposal cites compressed plots of about 22.1 GiB against the 101.4 GiB originals, kept usable by "continuous GPU compute".

That moves the resource back toward computation and energy, which the design was meant to avoid, and it opens the way to an attacker renting processors to fake space it does not have.

Chia has responded twice. A hard fork on 13 June 2024 changed a parameter to make one form of the attack less effective. A new plot format, set out in Chia Improvement Proposal 48 (CHIP-48), is designed to resist compression and would require every farmer to plot again. As of 10 October 2026 that proposal was still under review, and the fork to activate it had no scheduled date.

## Other networks

**Signum**, launched as Burstcoin in August 2014, describes itself as the first chain to use the idea, under the name proof of capacity. In 2021 it added a stake component, calling the result Proof of Commitment. The stated reason is a familiar one: plot files "can be easily reused by copycat" chains at almost no cost, "resembling the nothing at stake problem". A miner's locked coins now scale its effective capacity up or down by as much as a factor of eight.

**Spacemesh** used a *proof of space-time*, in the sense defined by Moran and Orlov: a proof that space was held over a period, constructed as two proofs of space with a proof of elapsed sequential work between them. Its mainnet began on 14 July 2023 and asked each participant for at least 256 GiB. The network appears to have stopped. On 10 October 2026 the project's websites did not resolve and the domain that hosted its network's servers was parked for sale, the last change to the node software was dated May 2025, and a former member of the team has written that the company behind it declared bankruptcy in 2025. No official statement was found.

Moran and Orlov's definition carries the same either/or as the original. The prover shows that "she either spent a certain amount of CPU work, or reserved a certain amount of storage space for some specified period of time or spent some linear combination of the two."

## Three uses of one name

"Proof of space and time" and "proof of spacetime" refer to different things in different projects.

- In Chia, *Proof of Space and Time* is proofs of space interleaved with a delay function. Nothing in it shows that a plot was held for any period.
- In Moran and Orlov's paper, and in Spacemesh, a *proof of space-time* shows that space was held over a period.
- In Filecoin, *Proof of Spacetime* is a repeated audit that a provider still holds specific customer data. It is described under [proof of storage](/wiki/economics/defi/sybil-resistance/proof-of-storage).

Spacemesh's "proof of elapsed time" is also unrelated to the [mechanism of that name](/wiki/economics/defi/sybil-resistance/proof-of-elapsed-time) built on Intel's Software Guard Extensions (SGX). In Spacemesh it was sequential computation done by ordinary servers.

## Sources

- Dziembowski, Faust, Kolmogorov & Pietrzak, [Proofs of Space](https://eprint.iacr.org/2013/796) (2015)
- Chia Network, [The Chia Network Blockchain](https://docs.chia.net/chia-blockchain/green-paper/abstract/) (the green paper), read 10 October 2026
- Chia documentation, [Proof of Space 1.0](https://docs.chia.net/chia-blockchain/consensus/proof-of-space-1.0/), [Proof of Time](https://docs.chia.net/chia-blockchain/consensus/proof-of-time/), [Signage and infusion points](https://docs.chia.net/chia-blockchain/consensus/chains/signage-and-infusion-points/) and [Forks](https://docs.chia.net/chia-blockchain/consensus/forks/), read 10 October 2026
- Chia Network, [CHIP-48: New Proof of Space](https://github.com/Chia-Network/chips/pull/160) and [CHIP-12](https://github.com/Chia-Network/chips/blob/main/CHIPs/chip-0012.md), read 10 October 2026
- Moran & Orlov, [Simple Proofs of Space-Time and Rational Proofs of Storage](https://eprint.iacr.org/2016/035) (2016)
- Signum, [SIP-27: Proof of Commitment (PoC+) consensus](https://github.com/signum-network/SIPs/blob/master/SIP/sip-27.md), and [project history](https://docs.signum.network/ecosystem/history)
- Spacemesh, [mainnet configuration](https://github.com/spacemeshos/go-spacemesh/blob/develop/config/mainnet.go) and archived documentation; Rettig, [Spacemesh postmortem, part II](https://rettig.substack.com/p/spacemesh-postmortem-part-ii) (22 September 2025)
