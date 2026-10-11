---
title: "DAG-Based BFT"
weight: 120
---

DAG-based BFT is a class of Byzantine fault tolerant (BFT) consensus protocols in which every validator proposes a block in every round, each block references most of the blocks of the round before, and the validators work out one agreed order for all the blocks from the shape of the resulting graph. Because references only point backwards, the graph is a [directed acyclic graph](/wiki/cs/dag) (DAG). Byzantine fault tolerant means the protocol works while up to *f* of its 3*f* + 1 validators behave arbitrarily, including lying.

No message in these protocols is a vote about order. Validators broadcast blocks and nothing else. A block's references to earlier blocks stand in for its votes on them, and since every validator reads the same graph with the same rule, every validator computes the same order. The paper that set the pattern, DAG-Rider, puts it as: "processes locally observe their DAGs and totally order all proposals with no extra communication."

The contrast is with leader-based protocols such as [PBFT](/wiki/economics/defi/consensus/pbft) and [HotStuff](/wiki/economics/defi/consensus/hotstuff), where one validator at a time proposes and the others vote on its proposal. There the leader's capacity bounds the system's throughput. Here all validators propose in parallel.

Sui, IOTA and Aleo run protocols of this class.

## The graph

Time is divided into rounds. In each round a validator creates at most one block. The block carries transactions and references to at least 2*f* + 1 blocks of the previous round, so a validator cannot start a round until it has received that many blocks from the round before. A slow or silent validator is simply not referenced, and nobody waits for it.

One misbehaviour has to be excluded for the graph to mean the same thing to everyone. A faulty validator could send one block to half the network and a different block for the same round to the other half, which is called *equivocation*. The protocols divide by how they deal with it.

- **Certified graphs.** A block is not usable until its creator has collected signed acknowledgments from 2*f* + 1 validators and broadcast the resulting certificate. At most one block per validator per round can be certified.
- **Uncertified graphs.** Blocks are sent once, with no acknowledgment round. Two conflicting blocks from one validator can both exist, and the commit rule is designed so that at most one of them can ever gather enough support.

## From graph to order

Some blocks are designated *leader* blocks by a rule all validators know. The rule may be a fixed schedule, or a shared random value revealed only after the round, so that nobody can target the leader in advance.

A leader block is committed when enough blocks in later rounds reference it, directly or through other blocks. In DAG-Rider, rounds are grouped into waves of four, and a wave's leader is committed once 2*f* + 1 blocks in the wave's last round have a path to it.

When a leader block is committed, every block reachable from it that has not been ordered yet is placed in the order ahead of it, by a fixed rule. One committed leader therefore orders a batch of blocks from all the validators.

## Three generations

The table uses two terms for what a protocol assumes about the network. *Asynchronous* means it assumes no bound on how long a message may take. *Partially synchronous* means it assumes delays are bounded from some unknown moment on.

| Protocol | Published | Network assumed | Certified | Rounds to commit |
|---|---|---|---|---|
| DAG-Rider | 2021 | asynchronous | yes | six in expectation, against an adversarial network |
| Narwhal with Tusk | 2021 | asynchronous | yes | 4.5 in expectation with random delays, 7 against an adversarial network |
| Bullshark | 2022 | asynchronous, with a faster path when the network is timely | yes | two when the network is timely, six in expectation otherwise |
| Mysticeti | 2023 | partially synchronous | no | three message delays, in steady state and under crash failures |

A round of a certified graph is several messages: the block, the acknowledgments, and the certificate. The Mysticeti paper counts Bullshark's commit at six message delays against its own three.

**DAG-Rider** showed that the two layers could be separated cleanly: a broadcast layer that builds the graph, and an ordering layer that costs no messages. It assumes nothing about message timing and picks each wave's leader with a shared random coin.

**Narwhal** made the first layer a system in its own right. Its paper proposes "separating the task of reliable transaction dissemination from transaction ordering", on the argument that spreading transaction data, not agreeing on its order, was what limited earlier protocols. A block's certificate "includes 2f + 1 signatures, ie. at least f + 1 honest validators have checked and stored the block", so anything the ordering layer refers to can be fetched. In the paper's wide-area experiments with 50 validators and no faults, HotStuff ordering Narwhal's certificates reached "over 130,000 tx/sec at less than 2-sec latency compared with 1,800 tx/sec at 1-sec latency for Hotstuff" alone. Tusk is the asynchronous ordering protocol the same paper puts on top.

**Bullshark** added a fast path. While the network delivers messages promptly, leaders fixed in advance are committed after "2 round-trips", and the randomized leader remains as a fallback. The paper also gives a simpler version that works only under partial synchrony, and that version is the one that went into production.

**Mysticeti** removed the certificates. Its paper lists what certification costs: several round trips per block, commits only on every second round, and signatures from most validators on every block. Without it, Mysticeti commits in "3 message rounds", which the paper notes is the same as PBFT. In wide-area tests with 10 and 50 validators and no faults it reports a commit latency of 0.5 seconds at over 200,000 transactions per second (TPS). On Sui's mainnet, with 106 validators, the paper's figure for the switch from Bullshark is a drop in median latency from 1.9 seconds to 400 milliseconds.

## What is assumed

All of these protocols need *n* = 3*f* + 1 validators to tolerate *f* Byzantine ones.

They differ on timing. DAG-Rider and Tusk are asynchronous: they stay safe and keep making progress with no bound on message delay, and they get around the [impossibility of deterministic agreement](/wiki/economics/defi/consensus#what-cannot-be-done) in that setting by using randomness. The price is slower commits. Mysticeti and the production version of Bullshark are partially synchronous: safe always, and live once message delays are bounded.

## Who runs it

- **Sui** runs Mysticeti. Its documentation says the protocol "only requires 3 rounds of messages to commit blocks from the DAGs". The [Sui consensus](/wiki/economics/defi/chains/sui/consensus) page covers how Sui uses it.
- **IOTA** runs Starfish, "a BFT consensus protocol optimized for low latency and high throughput using an uncertified DAG structure", on its mainnet since April 2026. See [IOTA Rebased](/wiki/economics/defi/chains/iota/iota-rebased#consensus-mysticeti-to-starfish).
- **Aleo** runs AleoBFT, "built on the composition of Narwhal and a partially synchronous version of Bullshark".

## Neighbours

[Hashgraph](/wiki/economics/defi/consensus/hashgraph), from 2016, is an earlier design with the same central idea: voting is computed from a graph and never sent. It has no rounds of the kind described here, and builds its graph from the record of who synchronized with whom.

[GHOSTDAG](/wiki/economics/defi/consensus/ghostdag) also orders a graph of blocks, but it is a proof-of-work protocol with open membership. It has no fixed validator set and no quorums, and its guarantee is probabilistic.

## Sources

- Keidar, Kokoris-Kogias, Naor & Spiegelman, [All You Need is DAG](https://arxiv.org/abs/2102.08325) (2021)
- Danezis, Kokoris-Kogias, Sonnino & Spiegelman, [Narwhal and Tusk: A DAG-based Mempool and Efficient BFT Consensus](https://arxiv.org/abs/2105.11827) (2021)
- Spiegelman, Giridharan, Sonnino & Kokoris-Kogias, [Bullshark: DAG BFT Protocols Made Practical](https://arxiv.org/abs/2201.05677) (2022)
- Babel et al., [Mysticeti: Reaching the Latency Limits with Uncertified DAGs](https://arxiv.org/abs/2310.14821) (2023; version 6, 2025)
- Sui documentation, [Consensus](https://docs.sui.io/concepts/sui-architecture/consensus), read 10 October 2026
- IOTA documentation, [Consensus on IOTA](https://docs.iota.org/about-iota/iota-architecture/consensus), read 10 October 2026, and IOTA Foundation, [Starfish on Mainnet](https://blog.iota.org/starfish-mainnet-release/) (28 April 2026)
- Aleo, [AleoBFT: Explore Aleo's consensus layer](https://aleo.org/post/architecture-of-aleobft-consensus/) (13 January 2025)
