---
title: "BABE and GRANDPA"
weight: 90
---

Polkadot splits consensus between two protocols that run side by side. Blind Assignment for Blockchain Extension (BABE) decides which validator produces each block. GRANDPA decides which blocks are final. The Polkadot Wiki expands GRANDPA as "GHOST-based Recursive ANcestor Deriving Prefix Agreement".

BABE on its own would give a chain like Bitcoin's, in which a block is only ever probably permanent. GRANDPA is a *finality gadget*: a voting protocol among the validators that marks a block as final, after which no node will revert it.

What sets GRANDPA apart from other voting protocols is what a vote covers. A validator votes for the block it considers the newest, and that vote counts for every ancestor of the block as well. Validators who disagree about the last few blocks still agree on the chain up to some point, and GRANDPA finalizes up to that point. One round of voting can finalize any number of blocks.

Stewart and Kokoris-Kogias published GRANDPA in 2020. Their abstract describes the trade the split avoids: classic protocols "forfeit liveness in the face of asynchrony in order to preserve safety, whereas most deployed blockchain protocols forfeit safety in order to remain live."

## Block production: BABE

Time is divided into slots of 6 seconds, grouped into epochs of 4 hours.

In each slot every validator runs a private lottery. It evaluates a verifiable random function (VRF), which gives a pseudo-random number and a proof that the number is correct, and it may produce a block if the number is below a threshold. The threshold is set so that a slot has a lottery winner with probability one quarter. A slot can have no winner, or several. The Polkadot Wiki calls the scheme "comparable as an algorithm to Ouroboros Praos", and the [Ouroboros](/wiki/economics/defi/consensus/ouroboros#the-lottery) page describes that lottery in detail.

So that empty slots do not leave gaps, every slot also has a *secondary* producer, assigned by a public schedule, who makes the block if nobody wins the lottery.

When there are forks, a producer builds on the chain GRANDPA has finalized, and beyond that point on the fork containing the most lottery-won blocks. That is not always the longest fork.

## Finality: GRANDPA

The voters are the validators. With *n* of them, the protocol assumes at most *f* are Byzantine, meaning arbitrarily faulty, where *n* = 3*f* + 1. A *supermajority* is more than two thirds of the voters.

A round has two votes, and one voter, the round's *primary*, opens it by broadcasting its view of the round before, unless it has already finalized that. A vote is the hash of a block, signed.

1. **Prevote.** Each voter broadcasts a prevote for the block at the head of the best chain it sees.
2. **Precommit.** Each voter looks at the prevotes it has received and finds the highest block that a supermajority voted for, counting a vote for a block as a vote for each of its ancestors. It precommits to that block. The paper calls this the 2/3-GHOST function, after the [GHOST](/wiki/economics/defi/consensus/ghost) rule that weighs a block by everything built on it.
3. **Finalize.** A voter that sees a supermajority of precommits for a block, or for its descendants, finalizes that block and with it every ancestor.

Voters may see different subsets of the votes and so compute different blocks in step 2. The paper's argument is that, provided at most *f* voters vote two ways, all such blocks lie on one chain, so they differ only in how far along it each voter is prepared to go.

The finalized block need not be the next one after the last finalized block. It may be far ahead. After a period in which block production ran and voting did not, one successful round finalizes the whole backlog.

## What is guaranteed

**Safety without timing assumptions.** As long as at most *f* voters are Byzantine, two blocks on different chains are never both finalized, however messages are delayed.

**Accountability if that fails.** The paper's Theorem 4.1 says that if two conflicting blocks are finalized with valid commit messages, "there are at least f + 1 Byzantine voters who all voted in a particular vote", and that "there is a synchronous procedure to find" such a set, which is to say one that needs timely communication. Identified validators can be slashed, meaning their stake is taken.

**Progress when the network is timely.** A new block is finalized once the network delivers messages within a bound, the round's primary is honest, and the honest voters already agree on the best chain. The paper also proves that no deterministic finality gadget can guarantee progress on a fully asynchronous network.

## Why two protocols

Voting among hundreds of validators is slower than producing a block. With the two separated, the Polkadot Wiki says, blocks can be "rapidly produced, and the slower finality mechanism" runs "in a separate process to finalize blocks without risking slower transaction processing or stalling."

[Casper FFG](/wiki/economics/defi/consensus/casper-ffg), Ethereum's finality gadget, is the nearest relative, and the GRANDPA paper says its approach "is similar". The difference is in what gets finalized. Casper votes on checkpoints at fixed intervals, one per epoch. GRANDPA has no checkpoints and finalizes whatever prefix the voters currently agree on.

## On Polkadot

In October 2026 the Polkadot Wiki, reading the value from the chain, showed 600 validators in the active set. They are chosen by *nominated* [proof of stake](/wiki/economics/defi/sybil-resistance/proof-of-stake#variants): token holders back validators they trust with their own stake, and an election picks the set. The election and the staking accounts now run on Asset Hub, a separate chain in the Polkadot system.

Block production was still BABE in the runtime source at that date. A successor named Safrole, formerly Sassafras, is described on the wiki as "an upgrade to BABE" that "provides anonymity in the validator selection process". The wiki gives no deployment date.

## Sources

- Stewart & Kokoris-Kogias, [GRANDPA: a Byzantine Finality Gadget](https://arxiv.org/abs/2007.01560) (2020)
- Polkadot Wiki, [Polkadot's Consensus Protocols](https://wiki.polkadot.com/learn/learn-consensus/), [Chain State Values](https://wiki.polkadot.com/general/chain-state-values/) and [Polkadot Block Production: SAFROLE](https://wiki.polkadot.com/learn/learn-safrole/), read 10 October 2026
- Polkadot Protocol Specification, [Block Production](https://spec.polkadot.network/sect-block-production), read 10 October 2026
- Polkadot Fellowship, [relay-chain runtime constants](https://github.com/polkadot-fellows/runtimes/blob/main/relay/polkadot/constants/src/lib.rs), read 10 October 2026
