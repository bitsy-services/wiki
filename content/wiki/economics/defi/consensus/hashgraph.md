---
title: "Hashgraph"
weight: 130
---

Hashgraph is a consensus algorithm in which the participants never send each other votes. They exchange *events*, small signed records of who synchronized with whom, and each participant works out from its own copy of those records how every other participant would have voted. Leemon Baird published it in 2016. The Hedera network runs it.

An event is created each time one member receives a synchronization from another. It contains the hashes of two earlier events: the creator's own previous event, and the latest event of the member who just synchronized with it. It also carries any new transactions the creator wants to submit, the creator's clock time, and the creator's signature. Linked by those hashes, the events form a graph, which the paper defines as "a data structure that records who gossiped to whom, and in what order."

Two terms from the paper describe how this is used.

- **Gossip about gossip.** Members spread information by gossip, "each member repeatedly choosing another member at random, and telling them all they know". What they tell each other is the events, so the history of the gossip is itself what is being gossiped.
- **Virtual voting.** Every member ends up with the same graph, and the graph shows what each member knew at each moment. So "Alice can calculate what vote Bob would have sent her", had they been running a conventional voting protocol. In the paper's words, "Hashgraph sends no votes at all over the network".

## From graph to order

The algorithm runs a voting protocol on the graph, with events standing in for messages. The definitions build on one another.

**Seeing.** Event *x* can *see* event *y* if *y* is an ancestor of *x* and *x*'s ancestors do not include a *fork* by *y*'s creator, meaning two events by one creator of which neither follows the other in that creator's own sequence. It can *strongly see* *y* if it can see events by more than two thirds of the members, each of which can see *y*. Strongly seeing is the graph's equivalent of a quorum: it means word of *y* has passed through a supermajority on its way to *x*.

**Rounds and witnesses.** The first event is in round 1. An event moves to round *r* + 1 when it can strongly see events of round *r* from more than two thirds of the members. The first event each member creates in a round is that member's *witness* for the round.

**Fame.** The members decide, by virtual vote, which witnesses of a round are *famous*. Each witness of the next round votes yes if it can see the witness in question. If more than two thirds agree, the question is settled. If not, the vote continues in later rounds, each witness following the majority of the witnesses it can strongly see. Informally, the paper says, a witness is famous "if many members see it by the start of the next round".

**Order.** Once a round's famous witnesses are known, they fix the position of earlier events. An event's *round received* is the first round in which every famous witness has it as an ancestor. Its timestamp is the median of the times at which the creators of those witnesses first learned of it. Events are sorted by round received and then by that timestamp.

The median is the basis of the paper's fairness claim, that "it is difficult for an attacker to manipulate which of two transactions will be chosen to be first". No single member's clock decides a timestamp.

## What is guaranteed

The proofs assume *n* members, "more than 2n/3 of which are honest". The rest may be Byzantine, meaning arbitrarily faulty.

No timing is assumed. The paper describes the system as "totally asynchronous", requiring only that a message sent repeatedly eventually arrives. A [1985 result](/wiki/economics/defi/consensus#what-cannot-be-done) rules out deterministic agreement under that assumption, and the paper's claim is fitted to it: the algorithm "is nondeterministic, and achieves Byzantine agreement with probability one". The randomness comes from occasional rounds in which undecided voters flip a coin derived from their signatures.

Two conditions sit beside the headline. The abstract's speed claim is for "the absence of faults". And the algorithm as proved has a fixed, known membership in which every member counts equally. Weighting members by stake is described in a later section as a modification in which "votes are weighted proportional to the voter's stake".

## On Hedera

Hedera's documentation, read in October 2026, says the mainnet's consensus nodes "are currently permissioned; operated by the Hedera Council", a governing body of "up to 39 global enterprises". The network's address book listed 30 consensus nodes on 10 October 2026. Anyone may submit transactions. Running a node that takes part in consensus is not open.

Hedera uses the stake-weighted form of the algorithm: "each node's influence on consensus is proportional to the amount of cryptocurrency it has staked", and a transaction reaches consensus once nodes representing more than two thirds of the staked currency have processed it. The documentation gives the time to finality as "3–5 seconds", without stating the conditions.

With a closed list of node operators, what keeps an outsider from gaining influence is admission to the list, as in [proof of authority](/wiki/economics/defi/sybil-resistance/proof-of-authority). Stake sets the weights among those admitted.

The algorithm came out of Swirlds, the company named on the 2016 report. In September 2024 Hedera contributed its source code, including the consensus algorithm, to a Linux Foundation project named Hiero. Operation of the network stayed with the council.

## Relation to later designs

[DAG-based BFT](/wiki/economics/defi/consensus/dag-bft) protocols, which appeared from 2021, share the central idea that votes can be read off a graph of messages. They organize the graph into numbered rounds with one block per validator, and they designate leader blocks, which makes the commit rule simpler than the fame election here.

## Sources

- Baird, [The Swirlds Hashgraph Consensus Algorithm: Fair, Fast, Byzantine Fault Tolerance](https://www.swirlds.com/downloads/SWIRLDS-TR-2016-01.pdf), Swirlds technical report (2016; revised 2018)
- Hedera documentation, [Mainnet consensus nodes](https://docs.hedera.com/hedera/networks/mainnet/mainnet-nodes) and [Staking](https://docs.hedera.com/learn/core-concepts/staking), read 10 October 2026
- Linux Foundation Decentralized Trust, announcement of Hedera's contribution of its source code as Project Hiero (16 September 2024)
