---
title: "PBFT"
weight: 50
---

Practical Byzantine Fault Tolerance (PBFT) is a protocol by which a fixed group of servers, called replicas, execute the same client requests in the same order while some of the replicas misbehave. The misbehaviour it covers is arbitrary: a faulty replica may crash, send different messages to different peers, or be run by an attacker. Faults of that kind are called *Byzantine*. With 3*f* + 1 replicas the protocol tolerates *f* faulty ones, so four replicas survive one fault and seven survive two.

Castro and Liskov published it in 1999. The replicas know one another's identities in advance, and every message is authenticated. One replica at a time, the *primary*, gives each request a sequence number. The others, the *backups*, exchange two rounds of votes on that numbering, and a replica executes a request once it holds matching votes from 2*f* + 1 replicas. When the primary stops making progress, the backups replace it.

[Tendermint](/wiki/economics/defi/consensus/tendermint) and [HotStuff](/wiki/economics/defi/consensus/hotstuff), two protocols that proof-of-stake blockchains use to make a block final at once, both start from this design. It is also the protocol to read first, because the later ones are described by what they change in it.

## Why 3f + 1

Write *n* for the number of replicas. A replica has to be able to act after hearing from all but *f* of them, because *f* may be faulty and silent. The *f* that stayed silent may also be honest and merely slow, in which case up to *f* of the replies in hand came from faulty replicas. The honest replies must still outnumber the faulty ones. In the paper's words, "there must still be enough responses that those from non-faulty replicas outnumber those from faulty ones, i.e., n-2f > f. Therefore n > 3f."

The working number that follows from it is 2*f* + 1, the size of a *quorum*. Any two quorums drawn from 3*f* + 1 replicas overlap in at least *f* + 1 replicas, and at most *f* of those are faulty. Two quorums therefore always share an honest replica, and an honest replica does not vote for two different requests at the same sequence number.

## Normal operation

| Step | Sent by | What the receiver waits for |
|---|---|---|
| Request | the client, to the primary | |
| Pre-prepare | the primary, to every backup | |
| Prepare | each backup, to every replica | the pre-prepare and 2*f* matching prepares |
| Commit | every replica, to every replica | 2*f* + 1 matching commits |
| Reply | every replica, to the client | *f* + 1 matching replies |

The primary assigns the request the next sequence number and sends a *pre-prepare* carrying that number to the backups. A backup that accepts it sends a *prepare* to all replicas. A replica calls the request *prepared* once its log holds the request, the pre-prepare, and 2*f* prepares from different backups that match it, which with the primary makes 2*f* + 1 replicas. Within one primary's term, no two different requests can become prepared under the same sequence number at honest replicas.

A replica whose request is prepared sends a *commit*. It executes the request once it holds 2*f* + 1 matching commits, its own included, and has executed every request with a lower sequence number. It then replies to the client, and the client accepts a result once *f* + 1 replicas have sent the same one. At most *f* replicas are faulty, so one of those replies is from an honest replica.

The two rounds of votes do different jobs. Prepares fix the order of requests while one primary is in charge. Commits make sure that an order some replica has already executed survives a change of primary.

## Replacing the primary

The period during which one replica is primary is a *view*, and views are numbered. The primary of view *v* is replica *v* mod *n*, so the role rotates.

A backup starts a timer when it receives a request. If the timer runs out before the request is executed, the backup stops accepting ordinary messages and sends a *view-change* message for view *v* + 1. The message carries proof of the backup's latest *stable checkpoint*, a state that 2*f* + 1 replicas have confirmed reaching, and, for every request prepared at that backup since the checkpoint, the pre-prepare and the 2*f* prepares that prove it. The primary of the new view waits for view-change messages from 2*f* other replicas and then sends a *new-view* message containing them, which re-issues every request the old view may already have executed.

Three details keep this from stalling or being abused:

- Each failed view change doubles the wait before the next one, from *T* to 2*T*, so the timeout eventually exceeds the real message delay.
- A replica that receives *f* + 1 view-change messages for a later view joins without waiting for its own timer.
- A view change needs *f* + 1 replicas to ask for it, so one faulty replica cannot force one except by being the primary and doing nothing. Because the role rotates, the primary cannot be faulty for more than *f* views in a row.

## What it assumes about the network

Safety here means that no two honest replicas execute different requests at the same sequence number. It holds however the network behaves: "The algorithm does not rely on synchrony to provide safety."

Liveness, meaning that clients eventually receive replies, is guaranteed only when at most ⌊(*n* − 1) / 3⌋ replicas are faulty and, in the paper's words, message delays do not "grow faster than the timeout period indefinitely". Since the timeout doubles after each failed view change, that rules out only delays that keep outgrowing it. The paper calls this "a rather weak synchrony assumption". Some timing assumption is unavoidable, because a 1985 result by Fischer, Lynch and Paterson shows that no deterministic protocol is guaranteed to reach agreement in a network with no timing guarantees at all once a single process may crash. The [Consensus](/wiki/economics/defi/consensus#what-cannot-be-done) overview sets out that result and the model later papers use for it.

The paper describes its setting as asynchronous. The HotStuff paper, twenty years on, calls PBFT "the first practical BFT replication solution in the partial synchrony model". The two descriptions refer to the same pair of properties: safe always, live once the network settles.

## Cost

Every replica sends its prepare and its commit to every other replica. The 1999 paper gives no formula for the total. The HotStuff paper's comparison counts *authenticators*, the signatures a replica has to receive and check, and puts PBFT at O(*n*²) per decision while the primary is working and O(*n*³) for a view change. The same paper credits a 2002 revision by Castro and Liskov with bringing the view change down to O(*n*²).

The abstract's performance claim is that a replicated file service built on PBFT was "only 3% slower than a standard unreplicated NFS", the Network File System (NFS). The body of the paper gives the conditions. The figure is the total time on one benchmark with four replicas and no view changes, measured against a different file server, the one shipped with Digital Unix. Against the authors' own server with replication switched off, the replicated version took 26% longer.

## Where it runs now

Hyperledger Besu, an Ethereum client, offers two voting protocols for private networks. One is IBFT 2.0, a revision of the Istanbul BFT protocol (IBFT), whose authors describe its handling of a failed proposer as "based on the view change protocol of PBFT". The other is QBFT, which Besu now recommends in its place. Besu's documentation says they "have immediate finality; there are no forks and all valid blocks get included in the main chain". It states the thresholds in its own terms. A block needs signatures from "greater than or equal to 2/3" of validators, a network needs four validators to tolerate a Byzantine one, and if more than a third of validators stop, block production stops. Besu classes both as [proof of authority](/wiki/economics/defi/sybil-resistance/proof-of-authority), since the validators are an approved list.

Public blockchains run its descendants. Tendermint weights votes by stake and removes the separate view-change procedure. HotStuff has the leader gather votes into one certificate, so that replacing a leader costs O(*n*) authenticators.

## Sources

- Castro & Liskov, [Practical Byzantine Fault Tolerance](https://www.usenix.org/legacy/publications/library/proceedings/osdi99/full_papers/castro/castro_html/castro.html), Third Symposium on Operating Systems Design and Implementation (1999)
- Yin, Malkhi, Reiter, Gueta & Abraham, [HotStuff: BFT Consensus in the Lens of Blockchain](https://arxiv.org/abs/1803.05069) (2019), for the authenticator counts in its Table 1
- Fischer, Lynch & Paterson, [Impossibility of Distributed Consensus with One Faulty Process](https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf), *Journal of the ACM* 32(2) (1985)
- Hyperledger Besu documentation, [Proof of authority consensus](https://docs.besu-eth.org/private-networks/concepts/poa) and [QBFT](https://docs.besu-eth.org/private-networks/how-to/configure/consensus/qbft), read 10 October 2026
- Saltini & Hyland-Wood, [IBFT 2.0: A Safe and Live Variation of the IBFT Blockchain Consensus Protocol for Eventually Synchronous Networks](https://arxiv.org/abs/1909.10194) (2019)
