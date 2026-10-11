---
title: "Ouroboros"
weight: 40
---

Ouroboros is a family of proof-of-stake consensus protocols built on the longest-chain rule. Time is divided into fixed *slots*. In each slot a lottery weighted by stake decides which stakeholders, if any, may add a block, and every node follows the longest valid chain. It is [Nakamoto consensus](/wiki/economics/defi/consensus/nakamoto-consensus) with a [stake](/wiki/economics/defi/sybil-resistance/proof-of-stake) lottery where Bitcoin has a hash puzzle. Cardano runs it.

Kiayias, Russell, David and Oliynykov presented the first version as "the first blockchain protocol based on proof of stake with rigorous security guarantees". Three versions carry the design:

| Version | Who may write in a slot | Network assumed | What a joining node must be given |
|---|---|---|---|
| Ouroboros | one leader, known to all in advance | synchronous: a known bound on message delay | a recent trusted chain |
| Ouroboros Praos | none, one or several, each known only to itself | semi-synchronous: an unknown bound on delay | a recent trusted chain |
| Ouroboros Genesis | as Praos | as Praos | the first block only |

Like Bitcoin's, the guarantee is probabilistic. A block is never final in the sense that [PBFT](/wiki/economics/defi/consensus/pbft) makes one final. It becomes harder to displace as blocks are added after it.

## The lottery

The description here is of Praos, the version Cardano's parameters belong to.

Slots are grouped into *epochs*. For each epoch the protocol fixes two things: a snapshot of who holds how much stake, and a random value called the epoch *nonce*.

In every slot each stakeholder evaluates a verifiable random function (VRF) on the slot number and the nonce, using its own secret key. A VRF returns a pseudo-random number and a proof, checkable with the public key, that the number is correct. If the number falls below a threshold set by the stakeholder's share of the stake, that stakeholder is a *slot leader*. It builds a block, attaches the proof, and broadcasts it.

The threshold comes from one parameter, the *active slot coefficient* *f*: the probability that a party holding all the stake would be elected in a given slot. A stakeholder with a fraction α of the stake is elected with probability 1 − (1 − *f*)^α. The formula is chosen so that splitting stake across several keys changes nothing: the chance that at least one of the parts is elected equals the chance for the whole.

The paper lists what follows from a private, independent lottery:

- several leaders may be elected for the same slot, which produces a short fork;
- many slots have no leader at all;
- nobody but the leader knows who it is "until the other stakeholders receive a valid block from this slot leader".

The third point is the reason for the design. In the original Ouroboros the schedule of leaders was public for the whole epoch, so an attacker knew in advance which machine to knock offline. The second is deliberate too. Empty slots are "short periods of silence that facilitate synchronization", and they give the version its name: *praos* means mellow, or gentle.

Two delays keep the lottery from being steered. The stake snapshot for an epoch is taken, in the paper's protocol, at the end of the epoch before the previous one, so stake cannot be moved in reaction to the nonce. The nonce for the next epoch is a hash of the VRF outputs in the blocks of the first two thirds of the current one. The paper does not claim the nonce is unbiased. An adversary controlling some of those slots can choose among possible nonces by publishing or withholding blocks, and the security analysis accounts for it.

## Choosing a chain

A node adopts a longer valid chain when it sees one, with a limit: it never switches to a chain that forks from its current chain more than *k* blocks back. Blocks deeper than *k* are settled as far as that node is concerned.

The limit has a cost, which the Genesis paper spells out. It is a "moving checkpoint", and it works only for a node that already has the right chain. A node joining for the first time, or returning after a long absence, has no current chain to measure a fork against, and has to be handed "a recent trusted chain" by someone. Without one it is exposed to a *long-range attack*: an adversary builds an alternative chain starting far in the past and presents it as the real one.

Genesis adds one condition. When a competing chain forks more than *k* blocks back, the node compares the two chains over a fixed window of slots just after the point where they diverge and prefers the one with more blocks in that window. The honest chain, backed by the majority of stake at that time, is the denser of the two there. With this rule new or returning parties can "bootstrap their blockchain only from a trusted copy of the genesis block".

## Keys that expire

Praos signs blocks with a *forward-secure* signature scheme. The signing key is replaced on a schedule and the old one erased, so a signature can be made only for the current period. An adversary who takes over a stakeholder's machine later finds no key that can sign blocks for slots already past, which is what it would need to rewrite history from that stakeholder's old slots.

## What it assumes

Every version requires that honest parties hold a majority of the stake. The conditions around that differ:

- The original paper's proof assumes a synchronous network and that the adversary needs some time to corrupt a party it has chosen. The Praos paper notes that without synchrony the original "is susceptible to a desynchronization attack that can completely violate the common prefix property".
- Praos drops both assumptions. It tolerates an unknown maximum delay, at a price: "the effective stake of the adversary is amplified by a function of ∆", where ∆ is the maximum delay. The slower the network, the smaller the share of stake an adversary needs.
- Genesis is proved "against a fully adaptive adversary controlling less than half of the total stake", with participants coming and going.

## On Cardano

Cardano's mainnet configuration file sets:

| Parameter | Value | Meaning |
|---|---|---|
| Slot length | 1 second | |
| Epoch length | 432,000 slots | 5 days |
| Active slot coefficient *f* | 0.05 | on average one slot in twenty has a leader, if all stake is online |
| Security parameter *k* | 2,160 blocks | the depth past which a node will not switch chains |

The five-day epoch is Cardano's choice. It is 10*k* / *f* slots, where the Praos paper specifies 24*k* / *f*.

The next version, Ouroboros Leios, is meant to raise throughput. Cardano's documentation described it in October 2026 as "currently in research and development".

## Sources

- Kiayias, Russell, David & Oliynykov, [Ouroboros: A Provably Secure Proof-of-Stake Blockchain Protocol](https://eprint.iacr.org/2016/889) (2017; revision of July 2019)
- David, Gaži, Kiayias & Russell, [Ouroboros Praos: An adaptively-secure, semi-synchronous proof-of-stake blockchain](https://eprint.iacr.org/2017/573) (revision of April 2023)
- Badertscher, Gaži, Kiayias, Russell & Zikas, [Ouroboros Genesis: Composable Proof-of-Stake Blockchains with Dynamic Availability](https://eprint.iacr.org/2018/378) (2018)
- Cardano, [mainnet Shelley genesis file](https://book.play.dev.cardano.org/environments/mainnet/shelley-genesis.json), read 10 October 2026
- Cardano documentation, [Ouroboros overview](https://docs.cardano.org/about-cardano/learn/ouroboros-overview), read 10 October 2026