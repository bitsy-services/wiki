---
title: "Casper FFG"
weight: 80
---

Casper the Friendly Finality Gadget (FFG) is a voting protocol that runs on top of a blockchain and marks some of its blocks as final. Validators, who have each locked up a deposit, vote on *checkpoints*: blocks picked out at regular intervals. A checkpoint that collects votes from two thirds of the deposited stake, in a pattern that takes two rounds, is *finalized*, and nodes will not revert it afterwards.

Casper does not produce blocks or choose between forks. Another mechanism does that, and Casper is laid over it. Buterin and Griffith, who proposed it in 2017, describe it as "a partial consensus mechanism".

Its defining property concerns what a failure would cost. Two conflicting checkpoints cannot both be finalized unless validators holding at least one third of the stake break one of two voting rules, and breaking either rule leaves signed evidence. A validator caught that way loses its deposit, which is called *slashing*. The paper names the property *accountable safety*.

Ethereum has run Casper since its move to [proof of stake](/wiki/economics/defi/sybil-resistance/proof-of-stake) in September 2022, over a fork-choice rule called [LMD-GHOST](/wiki/economics/defi/consensus/ghost#lmd-ghost). The combination is known as Gasper.

## Checkpoints and votes

Ethereum divides time into slots of 12 seconds and groups 32 slots into an *epoch* of 6.4 minutes. The checkpoint for an epoch is the block at its first slot, or the most recent earlier block if that slot is empty. The original paper, written for a [proof-of-work](/wiki/economics/defi/sybil-resistance/proof-of-work) chain, made every hundredth block a checkpoint.

A vote names two checkpoints: a *source* that the voter already regards as justified, and a *target* in the current epoch. Votes are weighted by stake. On Ethereum a validator votes once per epoch, in a signed message called an attestation, and the same message carries its fork-choice vote: the Gasper paper says an attestation "is simultaneously a 'GHOST vote' for its block and also a 'Casper FFG vote'".

Three definitions from the paper do the rest:

- A **supermajority link** from checkpoint *a* to checkpoint *b* exists when validators holding at least two thirds of the deposits have voted with source *a* and target *b*.
- A checkpoint is **justified** if it is the first block of the chain, or if a supermajority link leads to it from a justified checkpoint.
- A checkpoint is **finalized** if it is justified and a supermajority link leads from it to its direct child checkpoint.

A checkpoint therefore becomes final in two steps. It is justified during its own epoch, and finalized in the next when the following checkpoint is justified with it as the source. Two epochs is 12.8 minutes. Ethereum's documentation gives the usual wait as "about 15 minutes".

## The two rules

A validator must not publish two different votes such that either:

1. both have the same target height, or
2. one vote's source-to-target span lies strictly inside the other's.

Ethereum's specification calls these a *double vote* and a *surround vote*.

The first rule covers conflicting checkpoints at the same height. Each would need two thirds of the stake, any two such groups share at least one third, and every validator in the overlap has voted twice for one height. The second covers conflicting checkpoints at different heights. To justify a checkpoint beyond a finalized one on a different branch, a chain of supermajority links has to get past the finalized checkpoint and its child. A link that lands on either of their heights is already excluded by the first rule, so some link has to jump over both, and a vote for that link surrounds the vote that finalized them. The paper's summary: "it is impossible for any two conflicting checkpoints to be finalized unless ≥ 1/3 of the validators violate one of the two Casper Commandments/slashing conditions".

In the paper a violation costs the validator its entire deposit. Ethereum's deployed penalty is smaller and grows with the number of validators slashed around the same time, as described under [proof of stake](/wiki/economics/defi/sybil-resistance/proof-of-stake#slashing).

## What it does not guarantee

Casper guarantees that conflicting checkpoints are not both finalized. It does not guarantee that anything gets finalized: "Casper provides safety, but liveness depends on the chosen proposal mechanism." Its second theorem, *plausible liveness*, is weaker than the name suggests. It says only that when two thirds of validators follow the protocol, a new checkpoint can always be finalized without anyone having to break a rule.

If validators holding more than one third of the stake are offline, no supermajority link can form and finalization stops. The chain underneath keeps growing, since block production does not need a two-thirds vote. Its newest blocks are simply not final.

## The inactivity leak

The paper's remedy for a long stall is an *inactivity leak*, which "slowly drains the deposit of any validator that does not vote for checkpoints, until eventually its deposit sizes decrease low enough that the validators who are voting are a supermajority." In Ethereum's specification the leak switches on once finality is more than four epochs behind.

The leak has a cost, and the paper states it: it "introduces the possibility of two conflicting checkpoints being finalized without any validator getting slashed". If the validators are split by a partition that lasts long enough, each side sees the other as offline, drains its deposits, and finalizes a checkpoint of its own. Accountable safety has that exception. The paper's advice for a node that sees both is to "favor whatever finalized checkpoint it saw first", and it adds that "the exact algorithm for recovering from these various attacks remains an open problem."

## Long-range attacks

A validator that has withdrawn its deposit can no longer be slashed, so its old key could sign an alternative history for nothing. The paper's defence has two parts: nodes never revert a block they have seen finalized, and each node is expected to come online and catch up "at some regular frequency (e.g., once per 1–2 months)". A fork that rewrites blocks older than that is ignored by every node that was present at the time. Deposits stay locked for a period after a validator leaves, and the paper notes that this "introduces a synchronicity assumption between validators and clients". [Proof of stake](/wiki/economics/defi/sybil-resistance/proof-of-stake#long-range-attacks) covers the general problem.

## May 2023

Ethereum's mainnet stopped finalizing twice, on 11 and 12 May 2023. By an Ethereum Foundation researcher's measurement, the first stall lasted about 25 minutes, with participation falling to 40.9% of stake. The second, the next day, lasted about an hour, with participation as low as 30.7%, and went on long enough to start the inactivity leak. Blocks continued to be produced throughout, and both stalls ended without intervention.

The cause was in the software. Some consensus clients, the programs that validators run, including Prysm and Teku, spent so much computation checking valid votes with old targets that they could not keep up with their own duties. The two-thirds vote is taken over all stake, so a fault shared by clients that together run more than a third of it stops finality.

## Two ledgers in one chain

Running a finality gadget over a chain that never stops is a design choice with a result behind it. Neu, Tas and Tse put it as: "no blockchain can be live under dynamic participation and safe under temporary network partitions." A chain like Bitcoin's chooses to stay live. A protocol like [Tendermint](/wiki/economics/defi/consensus/tendermint) chooses to stay safe, and halts. Gasper offers both readings of the same chain: the newest blocks, always available and revisable, and the finalized prefix, which lags during trouble and catches up afterwards. The same authors showed an attack on Gasper as it was then specified, so the combination is harder to get right than the description suggests. The [Consensus](/wiki/economics/defi/consensus#finality-or-availability) overview has the general statement.

## Status

In October 2026 Ethereum's parameters were unchanged: 12-second slots, 32 slots to an epoch, and the finality rule of the original specification. A proposal for six-second slots, Ethereum Improvement Proposal 7782 (EIP-7782), was a draft and not scheduled for any upgrade. A later proposal for shorter slots, EIP-8198, was a draft under consideration for the upgrade after next. Finalizing within a single slot remains described as research on ethereum.org.

## Sources

- Buterin & Griffith, [Casper the Friendly Finality Gadget](https://arxiv.org/abs/1710.09437) (2017; version 4, 2019)
- Buterin et al., [Combining GHOST and Casper](https://arxiv.org/abs/2003.03052) (2020)
- Ethereum consensus specifications, [`specs/phase0/beacon-chain.md`](https://github.com/ethereum/consensus-specs/blob/master/specs/phase0/beacon-chain.md), read 10 October 2026
- ethereum.org, [Single slot finality](https://ethereum.org/roadmap/single-slot-finality/), read 10 October 2026
- [EIP-7782](https://eips.ethereum.org/EIPS/eip-7782) and [EIP-8198](https://eips.ethereum.org/EIPS/eip-8198), read 10 October 2026
- Prysm, [Mainnet postmortems](https://prysm.offchainlabs.com/docs/misc/mainnet-postmortems/), entry of 12 May 2023
- Thiery, [Cascading Network Effects on Ethereum's Finality](https://ethresear.ch/t/cascading-network-effects-on-ethereums-finality/15871) (26 May 2023)
- Neu, Tas & Tse, [Ebb-and-Flow Protocols: A Resolution of the Availability-Finality Dilemma](https://arxiv.org/abs/2009.04987) (2020)
