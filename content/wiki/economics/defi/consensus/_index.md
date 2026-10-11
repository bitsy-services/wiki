---
title: "Consensus"
weight: 14
bookCollapseSection: true
---

Consensus, for a blockchain, is the procedure by which a set of computers that do not trust one another come to hold the same ordered list of transactions. Each computer applies the transactions, in that order, to its own copy of the ledger, so the same list gives every one of them the same ledger.

A protocol is judged on two properties. *Safety* means that two honest computers never hold conflicting lists. *Liveness* means that the list keeps growing: a valid transaction is eventually added. Every protocol in this section is a decision about the conditions under which it delivers both, and about which one it gives up when those conditions fail.

Consensus is a separate question from who is allowed to take part. That question belongs to [Sybil resistance](/wiki/economics/defi/sybil-resistance): proof of work, proof of stake and the other schemes that decide whose voice counts and for how much. The protocols here take those weights as given. The ledger being agreed on is described under [Blockchain](/wiki/economics/defi/blockchain), and consensus engineering specific to one chain stays with that chain, as on the [Sui consensus](/wiki/economics/defi/chains/sui/consensus) page.

## Faults

A computer taking part in a protocol can fail in two ways. A *crash* fault is a machine that stops. A *Byzantine* fault is a machine that does anything at all: it may send different messages to different peers, lie about what it has seen, or act in concert with other faulty machines. The term comes from a 1982 paper by Lamport, Shostak and Pease that framed the problem as generals who must agree on a plan while some of them are traitors.

Blockchains assume Byzantine faults, since their participants are strangers with money at stake.

## What cannot be done

Three results from before blockchains set the limits that every design here works within.

**One third.** Lamport, Shostak and Pease showed that when messages carry no signatures, "no solution with fewer than 3m + 1 generals can cope with m traitors". Signatures remove that limit only if the network is reliable and timely. Dwork, Lynch and Stockmeyer showed in 1988 that when the network may be slow for an unknown time, tolerating *t* Byzantine faults takes 3*t* + 1 participants with or without signatures: "authentication does not improve resiliency."

**No guarantee without timing.** Fischer, Lynch and Paterson proved in 1985 that in a fully asynchronous system, one with no bound at all on message delay, "every protocol for this problem has the possibility of nontermination, even with only one faulty process". The result is for deterministic protocols, and the one fault is a crash. The authors point at the ways out themselves: the result calls for "more refined models" of timing, and "termination might be required only with probability 1."

**Partial synchrony.** The model most protocols adopt is from the 1988 paper. Messages are delivered within a known bound, but only from some moment that nobody knows in advance, the global stabilization time (GST). A protocol designed for this model never produces conflicting results however long the network misbehaves, and makes progress once it settles. The HotStuff paper states the contract: "ensure safety always, and ... guarantee progress within a bounded duration after GST."

The fewest participants *N* that can tolerate *t* faults, from the 1988 paper's table:

| Fault | Network always timely | Network timely after an unknown time | No timing guarantee |
|---|---|---|---|
| Crash | any number of faults tolerated | 2*t* + 1 | impossible |
| Byzantine, messages signed | any number of faults tolerated | 3*t* + 1 | impossible |
| Byzantine, messages unsigned | 3*t* + 1 | 3*t* + 1 | impossible |

The last column is for deterministic protocols. Protocols that use randomness, such as [Hashgraph](/wiki/economics/defi/consensus/hashgraph) and some [DAG-based protocols](/wiki/economics/defi/consensus/dag-bft), work in that setting and terminate with probability one.

## Finality or availability

The protocols divide on what they do when they cannot tell whether other participants have left or are just slow to answer.

**Chain-based protocols keep going.** Whoever is present extends the chain, and the heaviest chain wins. The network can lose most of its participants and continue. In exchange, no block is ever final: a block is only less and less likely to be displaced. These protocols tolerate an adversary with less than half of the resource, whether that is computing power or stake.

**Voting protocols stop.** A block is final the moment a quorum, usually more than two thirds, has signed it, and no later event can undo it. In exchange, if a third of the participants are unreachable the protocol produces nothing until they return. These protocols tolerate an adversary with less than a third.

The division is forced. Lewis-Pye and Roughgarden proved that "no protocol is both adaptive and has finality", where adaptive means able to keep running when the amount of participating resource is unknown. Neu, Tas and Tse restate it: "no blockchain can be live under dynamic participation and safe under temporary network partitions."

A third group runs both at once. A *finality gadget* is a voting protocol laid over a chain that never stops, so that the chain's recent blocks are available and provisional while its older blocks are final.

## In this section

The pages run from the chain-based protocols, through the voting protocols, to the designs that combine or depart from both.

[Nakamoto consensus](/wiki/economics/defi/consensus/nakamoto-consensus) is Bitcoin's rule and the starting point: follow the chain with the most accumulated work. [GHOST](/wiki/economics/defi/consensus/ghost) changes how competing chains are weighed so that blocks can come faster, and its descendant is the fork-choice rule of proof-of-stake Ethereum. [GHOSTDAG](/wiki/economics/defi/consensus/ghostdag) drops the single chain and orders a graph of blocks. [Ouroboros](/wiki/economics/defi/consensus/ouroboros) keeps the longest-chain rule and replaces proof of work with a stake lottery.

[PBFT](/wiki/economics/defi/consensus/pbft) is the classical voting protocol, and the one the others are described against. [Tendermint](/wiki/economics/defi/consensus/tendermint) adapts it to validators weighted by stake and removes its separate leader-replacement procedure. [HotStuff](/wiki/economics/defi/consensus/hotstuff) makes replacing a leader as cheap as an ordinary step.

[Casper FFG](/wiki/economics/defi/consensus/casper-ffg) is Ethereum's finality gadget, and [BABE and GRANDPA](/wiki/economics/defi/consensus/grandpa) are Polkadot's block production and finality gadget. Both pair a chain that keeps growing with a vote that makes part of it final.

Two protocols avoid having every participant vote. [Algorand](/wiki/economics/defi/consensus/algorand) draws a small committee by private lottery for each step. [Avalanche](/wiki/economics/defi/consensus/avalanche) has each node poll small random samples until the network tips one way.

[DAG-based BFT](/wiki/economics/defi/consensus/dag-bft) lets every validator propose at once and reads the order off the graph of blocks. [Hashgraph](/wiki/economics/defi/consensus/hashgraph) is an earlier design on the same idea, where the graph records who gossiped with whom.

[Federated Byzantine agreement](/wiki/economics/defi/consensus/federated-byzantine-agreement) has no global validator set at all. Each node picks whom it relies on. [Proof of history and Tower BFT](/wiki/economics/defi/consensus/proof-of-history) is Solana's pairing of a hash-chain clock with a voting rule built on it.

| Protocol | When a block is final | Run by |
|---|---|---|
| Nakamoto consensus | never; reversal becomes improbable | Bitcoin, Litecoin, Monero |
| GHOST | never; reversal becomes improbable | a descendant is Ethereum's fork choice |
| GHOSTDAG | never; reversal becomes improbable | Kaspa |
| Ouroboros | never; reversal becomes improbable | Cardano |
| PBFT | when a quorum has committed it | private networks, as Istanbul BFT (IBFT 2.0) |
| Tendermint | when more than two thirds of voting power has precommitted it | Cosmos Hub |
| HotStuff | when a chain of three certificates sits on it | Aptos and Flow, as Jolteon |
| Casper FFG | two epochs later, in the usual case | Ethereum |
| BABE and GRANDPA | when more than two thirds of voters agree on a chain containing it | Polkadot |
| Algorand | when a certifying committee has voted for it | Algorand |
| Avalanche | after enough consecutive successful polls, with a chosen error bound | Avalanche |
| DAG-based BFT | when a leader block that reaches it is committed | Sui, IOTA, Aleo |
| Hashgraph | when the witnesses that fix its position are decided | Hedera |
| Federated Byzantine agreement | when a quorum, as each node defines it, has confirmed it | Stellar, XRP Ledger |
| Proof of history and Tower BFT | after two thirds of stake has voted and 31 further blocks are confirmed | Solana |

## Sources

- Lamport, Shostak & Pease, [The Byzantine Generals Problem](https://lamport.azurewebsites.net/pubs/byz.pdf), *ACM Transactions on Programming Languages and Systems* 4(3) (1982)
- Fischer, Lynch & Paterson, [Impossibility of Distributed Consensus with One Faulty Process](https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf), *Journal of the ACM* 32(2) (1985)
- Dwork, Lynch & Stockmeyer, [Consensus in the Presence of Partial Synchrony](https://groups.csail.mit.edu/tds/papers/Lynch/jacm88.pdf), *Journal of the ACM* 35(2) (1988)
- Yin, Malkhi, Reiter, Gueta & Abraham, [HotStuff: BFT Consensus in the Lens of Blockchain](https://arxiv.org/abs/1803.05069) (2019)
- Lewis-Pye & Roughgarden, [Resource Pools and the CAP Theorem](https://arxiv.org/abs/2006.10698) (2020)
- Neu, Tas & Tse, [Ebb-and-Flow Protocols: A Resolution of the Availability-Finality Dilemma](https://arxiv.org/abs/2009.04987) (2020)

## Wiki Pages

{{< section >}}
