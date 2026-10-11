---
title: "Federated Byzantine Agreement"
weight: 140
---

Federated Byzantine agreement (FBA) is a model of consensus in which there is no global list of validators. Byzantine agreement is agreement among nodes some of which may behave arbitrarily, including dishonestly. Each node chooses for itself which other nodes it relies on, and the sets of nodes able to reach agreement emerge from the combination of everyone's choices. David Mazières introduced the model in the paper that defines the Stellar Consensus Protocol (SCP). The XRP Ledger works on a related principle, with a trusted list per server.

In protocols such as [PBFT](/wiki/economics/defi/consensus/pbft) and [Tendermint](/wiki/economics/defi/consensus/tendermint), every node knows the full set of validators, and a quorum is any two thirds of that set. Here a node knows only its own choices. Nothing is staked and no work is done, and anyone can run a validator. What gives a validator influence is that other nodes choose to rely on it.

The model moves the security assumption from a number to a configuration. A classical protocol is safe if fewer than a third of a known set are faulty. A federated one is safe if the nodes' individual choices overlap enough, which no single party controls and the protocol cannot enforce.

## Slices and quorums

A node's choices take the form of *quorum slices*. A slice is a set of nodes whose joint assertion is enough to convince that one node: "When a node hears a sufficient set of nodes assert a statement, it assumes no functioning node will ever contradict that statement." A node may have several slices, any one of which suffices.

A *quorum* is then a set of nodes that contains at least one slice for each of its own members. It is a group in which every member is convinced by the others in the group. The paper's summary: "A quorum is a set of nodes sufficient to reach agreement. A quorum slice is the subset of a quorum convincing one particular node of agreement."

Nobody declares quorums. They are a consequence of the slices.

## Safety depends on overlap

Two quorums that share no node can agree on two different things, each without hearing from the other. The paper's requirement is *quorum intersection*: "any two of its quorums share a node". It adds: "A protocol can guarantee agreement only if the quorum slices ... satisfy a validity property we call quorum intersection."

Intersection has to survive failures too. If the only nodes two quorums share are faulty, those nodes can tell each side a different story. The condition that matters is that the quorums still intersect after the faulty nodes are removed.

So safety is conditional on configuration. The paper claims that the protocol's "safety is optimal for an asynchronous protocol, in that it guarantees agreement under any node-failure scenario that admits such a guarantee". If the slices nodes have chosen do not overlap enough, no protocol could keep those nodes in agreement, and this one does not either.

## The protocol

SCP builds agreement out of *federated voting*, in which a statement passes through stages at each node. A node *votes* for a statement, *accepts* it once enough of the nodes it relies on have voted for or accepted it, and *confirms* it once a quorum has accepted it. A confirmed statement will not be contradicted by any node the protocol can protect.

Two sub-protocols use this to decide the contents of each ledger. The *nomination* protocol produces candidate values and converges on one. The *ballot* protocol then commits it, moving through phases the paper names prepare, confirm and externalize. Stellar's current documentation describes the ballot protocol as two steps, prepare and commit.

The paper lists four properties it claims together for the first time: decentralized control, low latency, flexible trust, and asymptotic security. The first and third are what the federated model is for. "Anyone is able to participate and no central authority dictates whose approval is required for consensus", and "users have the freedom to trust any combination of parties they see fit."

## On Stellar

A Stellar validator's operator lists the organizations and validators it relies on, each with a quality rating, and the software derives the slices and their thresholds from the list. A threshold is how many members of a set must agree: a node with three others in its set and a threshold of two is convinced by any two of them.

In practice the choices concentrate. Stellar's documentation defines *Tier 1 organizations* as those that "bear the safety and liveness of the Stellar network on their shoulders", a status they hold "because most other organizations on the network require agreement from them". Nobody appoints them: "every existing Tier 1 organization independently decides whether to add you to their quorum set."

On 15 May 2019 the network stopped for 67 minutes. The Stellar Development Foundation's account is that several validators had been unreliable for weeks, and when one more was taken down for maintenance, too few remained for quorums to form. No conflicting ledgers were produced. The foundation described the outcome as intended: "For a system like Stellar, a temporary halt is preferable to the permanent confusion of a fork."

## On the XRP Ledger

Each XRP Ledger server has a Unique Node List (UNL): "a server's list of validators that it trusts not to collude". A server counts only the votes of validators on its list, and validates a new ledger when 80% of them agree.

In principle every operator picks its own list. In practice the default configuration uses two published lists, "one published by the XRP Ledger Foundation, and one published by Ripple", which the documentation says are "very similar to one another or even identical". As of June 2024 the default lists held 35 validators, so the network "would stop making forward progress if 8 or more of them were offline". An extension called the Negative UNL lets the remaining validators agree to set aside ones that are offline, down to a floor of 60% of the total.

How much two servers' lists must overlap for them never to disagree was analysed by Chase and MacBrough in 2018. Their sufficient condition, "assuming 80% quorums and 20% faults", comes to "roughly > 90% UNL overlaps". They also show that agreement can stall "even with 99% UNL overlaps and no Byzantine faults". The freedom to choose a different list is narrow in practice.

## Limits

**Safety rests on choices the protocol cannot check.** A node that picks slices carelessly, or a network whose slices drift apart, loses the guarantee without any node misbehaving.

**Influence concentrates in the nodes everyone lists.** Both networks above have a small group whose availability the whole network depends on.

**The response to failure is to stop.** Neither network forks when too few validators are reachable. Both halt until enough return.

## Sources

- Mazières, [The Stellar Consensus Protocol: A Federated Model for Internet-level Consensus](https://www.stellar.org/papers/stellar-consensus-protocol.pdf) (draft of 25 February 2016)
- Stellar documentation, [Stellar Consensus Protocol](https://developers.stellar.org/docs/learn/fundamentals/stellar-consensus-protocol) and [Tier 1 organizations](https://developers.stellar.org/docs/validators/tier-1-orgs), read 10 October 2026
- Stellar Development Foundation, [May 15th network halt](https://stellar.org/blog/developers/may-15th-network-halt) (16 May 2019)
- XRP Ledger documentation, [Unique Node List](https://xrpl.org/docs/concepts/consensus-protocol/unl) and [Negative UNL](https://xrpl.org/docs/concepts/consensus-protocol/negative-unl), read 10 October 2026
- Chase & MacBrough, [Analysis of the XRP Ledger Consensus Protocol](https://arxiv.org/abs/1802.07242) (2018)
