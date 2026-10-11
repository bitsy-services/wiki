---
title: "HotStuff"
weight: 70
---

HotStuff is a Byzantine fault tolerant (BFT) consensus protocol run by a fixed set of servers, called replicas, in which one replica at a time, the *leader*, proposes a block and gathers the other replicas' votes on it into a single compact proof called a *quorum certificate*. A Byzantine fault is an arbitrary one: a replica that crashes, lies or colludes. With *n* = 3*f* + 1 replicas the protocol tolerates *f* of them. Yin, Malkhi, Reiter, Gueta and Abraham first posted it in 2018.

A quorum certificate (QC) is a set of votes from *n* − *f* replicas for the same proposal. HotStuff combines them with a threshold signature, a scheme in which any 2*f* + 1 of the replicas' partial signatures merge into one signature of ordinary size, so a certificate costs one signature to send and one to check.

Every step has the same shape. The leader sends a message to all replicas, each replica returns a vote to the leader alone, and the leader merges *n* − *f* votes into a certificate that it attaches to its next message. Replicas do not send votes to one another. In [PBFT](/wiki/economics/defi/consensus/pbft), the 1999 protocol HotStuff is measured against, every replica sends each vote to every other replica.

The paper claims two properties from this, and claims to be the first protocol of its kind with both:

- **Linear view change.** A correct leader sends O(*n*) signatures to drive a decision, and that includes the case where it has just replaced a failed leader. PBFT's leader replacement is O(*n*³).
- **Optimistic responsiveness.** A correct leader can proceed as soon as *n* − *f* replies arrive, so the protocol runs at the speed of the actual network and has no fixed waiting period.

Both are stated for the period after the network has become timely, and for a correct leader. The price is one more round of votes per block than PBFT uses.

## The phases

A leader's term is a *view*. In the basic protocol one view decides one block, in three voting phases and a final announcement.

| Phase | The leader sends | A replica answers with |
|---|---|---|
| Prepare | a block, and the highest certificate it knows of | a prepare vote, if the block is safe to accept |
| Pre-commit | the certificate formed from the prepare votes | a pre-commit vote |
| Commit | the certificate formed from the pre-commit votes | a commit vote, after *locking* on that certificate |
| Decide | the certificate formed from the commit votes | nothing; the replica executes the block |

A new leader begins by collecting a *new-view* message from *n* − *f* replicas. Each carries the highest prepare certificate its sender has seen. The leader takes the highest of those and proposes a block that extends it.

A replica decides whether to vote for a proposal with a two-part test, which the paper names `safeNode`. It accepts if either part holds:

- the proposed block extends the block the replica is locked on (the safety rule), or
- the certificate that comes with the proposal is from a later view than the replica's lock (the liveness rule).

The second part lets a replica abandon a stale lock when it is shown a newer certificate.

## Why a third phase

With two voting phases, as in PBFT and [Tendermint](/wiki/economics/defi/consensus/tendermint), a replica locks as soon as it sees the first certificate. A new leader that has heard from *n* − *f* replicas cannot then be sure that no replica it has not heard from is locked on a block it knows nothing about. Tendermint handles this by making each proposer wait out the maximum network delay before proposing, and PBFT by having replicas ship their proofs to the new leader, which is where its cubic cost comes from.

HotStuff delays the lock by one phase. A replica locks only on the second certificate, and that certificate exists only if *n* − *f* replicas already voted on the first. Any *n* − *f* replicas a new leader hears from therefore include one that reports the first certificate, and the liveness rule lets locked replicas follow it. The paper puts it this way: "there is no explicit 'wait-for-∆' step, and the logical disjunction in SAFENODE is used to override a stale lock with the help of the three-phase paradigm".

## Chained HotStuff

Since every phase has the same shape, the phases of successive blocks can share messages. In Chained HotStuff each view proposes one new block, and replicas vote once per view. The certificate for a block travels inside the next block, where it serves as the prepare certificate for its own block, the pre-commit certificate for that block's parent, and the commit certificate for its grandparent.

The commit rule is stated on the chain. A block carrying the certificate for its direct parent forms a *one-chain*. If the parent in turn carries the certificate for its own direct parent, that is a *two-chain*, and one more link makes a *three-chain*. The block at the base of a three-chain is committed. A block proposed in view 1 is committed by the end of view 4 if views 2, 3 and 4 each succeed.

The links have to be direct. When a leader fails to get its block certified, the next block's certificate points past the gap to an older ancestor, and that block does not count as a link.

## Pacemaker

The paper splits the protocol in two. Everything above is the safety half, and it holds whatever the timing. The other half, which the paper calls the *pacemaker*, decides when a view ends and who leads the next one. It has to bring the correct replicas and one correct leader into the same view for long enough to finish. The basic version doubles the view timeout after each failure. Safety does not depend on the pacemaker, so a deployment can change it without re-proving agreement.

## Cost, and its conditions

The paper's comparison counts *authenticators*: the signatures, or equivalent proofs, that replicas receive on the way to one decision, once the network is timely.

| Protocol | Correct leader | Leader failure | *f* leader failures | Responsive |
|---|---|---|---|---|
| PBFT | O(*n*²) | O(*n*³) | O(*fn*³) | yes |
| Tendermint, [Casper](/wiki/economics/defi/consensus/casper-ffg) | O(*n*²) | O(*n*²) | O(*fn*²) | no |
| HotStuff | O(*n*) | O(*n*) | O(*fn*) | yes |

Three conditions go with the HotStuff row. It holds after the global stabilization time (GST), the unknown moment from which the network delivers messages within a fixed bound. It is a cost per correct leader, so a run of failed leaders multiplies it, to O(*n*²) in the worst case. And it depends on threshold signatures. A footnote to the table gives Tendermint and Casper O(*n*) as well if they are assumed to use threshold signatures, "though this optimization is not mentioned in their original works". What separates HotStuff in the table is linear cost together with responsiveness.

The measurement in the abstract is that a deployment "with over 100 replicas achieves throughput and latency comparable to that of BFT-SMaRt", an established PBFT-style implementation.

## Descendants and relatives

- **Jolteon** (2021) commits on a two-chain. The authors report "reducing the steady state block-commit latency by 30%" and accept "a quadratic view-change" in exchange. In their experiments the gain was 200 to 300 milliseconds.
- **Aptos** names its protocol AptosBFT, and its documentation says it "is based on Jolteon".
- **Flow**'s node software says it "uses a derivative of HotStuff called Jolteon".
- **Monad**, whose public mainnet launched on 24 November 2025, runs MonadBFT. Its documentation describes it by comparison with "pipelined HotStuff consensus mechanisms prior to MonadBFT".
- **HotStuff-2** (2023) shows that two phases can keep optimistic responsiveness after all, with O(*n*²) communication in the worst case: "two phases are enough for BFT after all".

HotStuff was also the basis of DiemBFT, the protocol of the Diem payment network. The Diem Association sold its assets on 31 January 2022 and announced that it would wind down.

## Sources

- Yin, Malkhi, Reiter, Gueta & Abraham, [HotStuff: BFT Consensus in the Lens of Blockchain](https://arxiv.org/abs/1803.05069) (version 6, 2019)
- Gelashvili, Kokoris-Kogias, Sonnino, Spiegelman & Xiang, [Jolteon and Ditto: Network-Adaptive Efficient Consensus with Asynchronous Fallback](https://arxiv.org/abs/2106.10362) (2021)
- Malkhi & Nayak, [HotStuff-2: Optimal Two-Phase Responsive BFT](https://eprint.iacr.org/2023/397) (2023)
- Aptos documentation, [Glossary](https://aptos.dev/network/glossary), last updated 14 September 2026
- Flow, [consensus/hotstuff README](https://github.com/onflow/flow-go/blob/master/consensus/hotstuff/README.md), read 10 October 2026
- Monad documentation, [MonadBFT](https://docs.monad.xyz/monad-arch/consensus/monad-bft), read 10 October 2026
- Diem Association, statement on the sale of its assets to Silvergate, 31 January 2022
