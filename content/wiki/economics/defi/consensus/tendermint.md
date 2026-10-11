---
title: "Tendermint"
weight: 60
---

Tendermint is a consensus algorithm for blockchains in which a set of validators, each holding some amount of voting power, agrees on one block for each position in the chain, and a block is final as soon as it is agreed. It tolerates Byzantine faults, meaning validators that crash, lie or collude, provided the faulty validators hold less than one third of the total voting power. On a proof-of-stake chain a validator's voting power is its [stake](/wiki/economics/defi/sybil-resistance/proof-of-stake).

A position in the chain is a *height*. For each height the validators run one or more *rounds*. In a round, one validator, the *proposer*, broadcasts a block. Every validator then votes twice, first a *prevote* and then a *precommit*. A validator decides on the block once it holds the proposal and precommits for it from more than two thirds of the voting power. If the round ends without a decision, the next round begins with a different proposer.

Rounds are the whole algorithm. There is no second procedure for replacing a failed leader, and that is what its authors changed from [PBFT](/wiki/economics/defi/consensus/pbft), the 1999 protocol it is modelled on: "there is no separation between the normal and the recovery mode". The implementation described here is CometBFT, a fork of the original, Tendermint Core.

## A round

| Step | Who sends | What is sent |
|---|---|---|
| Propose | the round's proposer | the block |
| Prevote | every validator | the block's identifier, or nil |
| Precommit | every validator | the block's identifier, or nil |

Only the proposal carries the block. The votes carry its identifier.

A validator prevotes for the proposed block if the block is valid and the validator is not [locked](#locking) on a different one. Otherwise it prevotes nil. A validator that holds the proposal and prevotes for it from more than two thirds of the voting power sends a precommit for it. Otherwise it precommits nil. CometBFT's documentation calls that set of prevotes a *polka*: "Every pre-commit must be justified by a polka in the same round."

Each step has a timeout, so that a silent proposer or missing votes cannot hold the round open. The timeouts grow with the round number, by a fixed increment each round, and reset at every new height. A later round therefore waits longer than an earlier one, and at some round the wait exceeds the network's real delay.

The fractions are of voting power, not of the number of validators. The paper writes the total voting power as *n* and the faulty share as *f*, assumes *n* > 3*f*, and counts 2*f* + 1 messages as messages from senders whose combined power is at least 2*f* + 1.

## Locking

A validator that precommits a block *locks* on it, recording the block and the round. From then on it prevotes nil for any other block, with one exception described below.

The lock is what carries safety from one round to the next. Suppose more than two thirds of the voting power precommits block *B* in round 3, and some validator decides on it, but the votes reach others too late and round 4 begins. Every validator that sent one of those precommits is locked on *B*. Fewer than one third are faulty, so the validators still willing to prevote for a different block hold less than two thirds between them, and no other block can gather the prevotes it needs.

Locks alone could deadlock, with validators locked on different blocks from different rounds. Each validator therefore also tracks its *valid value*: the most recent block for which it has seen a proposal and prevotes from more than two thirds of the voting power, together with the round in which that happened. A proposer that has a valid value must propose it again in place of a new block, and it attaches the round. A locked validator accepts a proposal for a different block when two things hold. It has itself received prevotes for that block from more than two thirds of the voting power in the attached round, and that round is later than the round of its own lock. The round number alone would not be enough, since a dishonest proposer could attach any number. The comparison of rounds is as the paper's text states it. The paper's pseudocode accepts an equal round as well.

## Choosing the proposer

The proposer for each round is fixed in advance by a weighted round robin. Every validator has a priority. At each round every priority rises by that validator's voting power, the validator with the highest priority becomes the proposer, and its priority then drops by the total voting power. Over many rounds each validator proposes in proportion to its voting power.

## What it assumes about the network

The model is *partial synchrony*: there is a bound ∆ on message delay, and a moment after which the network respects it, the global stabilization time (GST). The validators do not know when that moment is. The paper also assumes a gossip network in which a message received by one honest validator reaches every honest validator within ∆ once that moment has passed. Its guarantee that a decision is eventually reached rests on that assumption.

Agreement does not depend on ∆ or on when the network settles. Termination does.

The single mode of operation has a cost. The HotStuff paper points out that a proposer here has to wait out a fixed interval sized for the worst-case delay before proposing, so the chain cannot move at the speed of a fast network: "Tendermint and Casper introduce a mandatory ∆ delay before each leader proposal". Casper there is [Casper FFG](/wiki/economics/defi/consensus/casper-ffg), the protocol Ethereum later adopted. The same paper counts the signatures validators must check at O(*n*²) per decision, with or without a leader failure.

## At the limits

**One third or more of the voting power offline: the chain stops.** A decision needs more than two thirds, so the CometBFT specification says "any 1/3+ coalition of validators can halt the blockchain by not broadcasting their votes", where 1/3+ is its shorthand for "1/3 or more". No conflicting block is produced. The chain resumes when more than two thirds of the voting power is back. Four validators of equal power is the smallest set that survives the loss of one.

**More than one third Byzantine, during a network partition: two conflicting blocks become possible, and the signers are identifiable.** Each of two conflicting sets of precommits needs more than two thirds of the voting power, so validators holding more than one third must have signed on both sides, and the two parts of the network must have been kept from seeing each other's votes. Those double signatures are evidence, and CometBFT gossips evidence and commits it to the chain. What happens next is up to the application. On the Cosmos Hub a validator that double-signs loses 5% of its stake and is removed permanently, which is the kind of penalty [proof of stake](/wiki/economics/defi/sybil-resistance/proof-of-stake#slashing) calls slashing. The specification is plain about the limit of this: with that much voting power Byzantine, evidence "is susceptible to censorship and should therefore be considered added security on a 'best effort' basis".

## Engine and application

CometBFT separates agreeing on the order of transactions from executing them. The consensus engine orders transactions and hands them to the application through the Application BlockChain Interface (ABCI), a socket protocol, so the application can be written in any language and need not know how agreement was reached.

CometBFT's first release, on 27 February 2023, describes it as "a fork of Tendermint Core". Its specification keeps "Tendermint" as the name of the algorithm and uses "CometBFT" for the software.

## On the Cosmos Hub

The Cosmos Hub runs CometBFT with 180 validators: the 180 candidates with the most stake delegated to them. Stake that is withdrawn stays locked, and exposed to slashing, for 21 days. Over the 10,000 blocks ending at block 33,354,977, at 04:43 UTC on 11 October 2026, the Hub averaged 5.71 seconds per block.

## Sources

- Buchman, Kwon & Milosevic, [The latest gossip on BFT consensus](https://arxiv.org/abs/1807.04938) (2018)
- CometBFT specification, [Byzantine Consensus Algorithm](https://github.com/cometbft/cometbft/blob/main/spec/consensus/consensus.md), [Proposer Selection Procedure](https://github.com/cometbft/cometbft/blob/main/spec/consensus/proposer-selection.md) and [Evidence](https://github.com/cometbft/cometbft/blob/main/spec/consensus/evidence.md), read 10 October 2026
- CometBFT documentation, [What is CometBFT](https://github.com/cometbft/cometbft/blob/main/docs/introduction/README.md), and the [v0.34 changelog](https://github.com/cometbft/cometbft/blob/v0.34.x/CHANGELOG.md) for the first release
- Yin, Malkhi, Reiter, Gueta & Abraham, [HotStuff: BFT Consensus in the Lens of Blockchain](https://arxiv.org/abs/1803.05069) (2019), for the comparison in its Table 1
- Cosmos Hub, [Validator FAQ](https://github.com/cosmos/gaia/blob/main/docs/docs/validators/validator-faq.md), and chain parameters read from a public node on 10 October 2026
