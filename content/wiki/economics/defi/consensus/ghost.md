---
title: "GHOST"
weight: 20
---

GHOST is a rule for choosing which chain of blocks is the true one when a blockchain has forked. It starts at the first block and repeatedly steps to the child block whose *subtree* is heaviest, where a block's subtree is the block plus everything built on top of it on any branch. It stops at a block with no children, and the path it walked is the chain.

The name stands for Greedy Heaviest-Observed Sub-Tree (GHOST). Sompolinsky and Zohar proposed it in 2013 as a replacement for the longest-chain rule of [Nakamoto consensus](/wiki/economics/defi/consensus/nakamoto-consensus), which weighs each competing chain by its own blocks alone. Under GHOST a block on an abandoned side branch still adds weight to every ancestor it shares with the main chain. In the paper's words, "blocks that are off the main chain can still contribute to its weight."

In the original proposal weight is [proof of work](/wiki/economics/defi/sybil-resistance/proof-of-work). Ethereum's proof-of-stake chain uses a descendant, [LMD-GHOST](#lmd-ghost), in which weight is the stake of the validators whose latest vote falls in the subtree.

## The problem it addresses

A block takes time to reach every miner. If blocks are produced quickly relative to that delay, miners often build on a block that is no longer the latest, and their blocks land on side branches. Under the longest-chain rule that work is lost: it lengthens nothing. An attacker working in private suffers no such losses, so it has to outpace only the main chain's actual growth, which is slower than the honest miners' combined rate of block production. The paper's summary is that "at high throughput, substantially weaker attackers are able to reverse payments they have made".

GHOST counts the side branches. The picture below is an illustration, not a figure from the paper. The honest miners have produced six blocks, but because of forks their longest chain is three blocks long. An attacker has built four blocks in private.

```text
genesis ─┬─ 1 ─┬─ 2a ── 3a          honest: 6 blocks, longest chain 3
         │     ├─ 2b
         │     └─ 2c ── 3c
         │
         └─ A ── B ── C ── D        attacker: 4 blocks, one chain
```

The longest-chain rule picks the attacker's chain, four blocks against three. GHOST compares subtrees at the first fork: block 1's subtree holds six blocks and block A's holds four, so it steps to block 1 and the attacker's chain loses.

The paper's claim is that under GHOST the attacker needs as much power as the honest network however high the block rate is set. It states this as a limit in a model of block arrival and delay, and says only that the result "suggests" the threshold. It also names two costs. The main chain grows "somewhat" more slowly than under the longest-chain rule, and throughput is still limited by bandwidth, since nodes have to transmit every block including those that end up on side branches.

## Ethereum's proof-of-work chain

Ethereum's specification of the time, the Yellow Paper, says its scheme "is a simplified version of the GHOST protocol", and the GHOST paper says "a variant of it has been implemented as part of the Ethereum project". The fork-choice arithmetic was nevertheless a heaviest-chain rule. The Yellow Paper defines the canonical chain as the one with the greatest total difficulty, and a block's total difficulty as its parent's total difficulty plus its own. The sum runs along the chain and has no term for blocks off it.

What Ethereum took from GHOST was payment for those blocks. It called a stale block that a later block referenced an *ommer*, "a gender-neutral term to mean 'sibling of parent'"; the commoner word is *uncle*. A block could reference at most two ommers, each no more than six generations back. The ommer's miner received a share of the block reward that fell by one eighth for each generation of distance, starting at seven eighths, and the miner who included it received an extra 1/32 of the block reward. Ommers have not existed since Ethereum left proof of work in 2022.

## LMD-GHOST

LMD-GHOST is the fork-choice rule of Ethereum's proof-of-stake chain. Validators publish *attestations*, signed votes for the block each one sees as the head of the chain. The weight of a block is the total stake of the validators whose most recent attestation is for that block or for a descendant of it. LMD stands for *latest message driven*: each validator counts once, by its latest vote only.

The walk is the same greedy one, with two differences. It starts from the most recent *justified* checkpoint, a block that [Casper FFG](/wiki/economics/defi/consensus/casper-ffg) has already half-finalized, and never from the first block. And a block cannot be removed from the chain once Casper FFG has finalized it, whatever the weights say. The paper that specifies the combination, known as Gasper, credits the adaptation of GHOST to votes to Vlad Zamfir.

In the specification, stake is counted as *effective balance*, and validators that have been penalized for voting two ways are left out.

### Proposer boost

Plain LMD-GHOST can be stalled. In a *balancing attack*, adversarial proposers start two competing branches, and then "a handful of adversarial votes per slot, released under carefully chosen circumstances, suffice to steer honest validators' votes so as to keep the system in a tie". A 2021 paper showed that an adversary with 15% of the stake could do this without controlling network delays, at the validator count of the time.

The response in the specification is *proposer boost*. A block that arrives on time in its own slot is given extra weight for that slot only: the constant `PROPOSER_SCORE_BOOST` is 40, a percentage of the stake assigned to vote in one slot, which is the total active stake divided by the 32 slots of an epoch. A timely block therefore starts with a lead that a few withheld votes cannot overturn.

Ethereum's documentation says the boost "substantially reduces the likelihood of a successful balancing or bouncing attack", and also that it "only defends against 'cheap reorgs'" and "can be gamed by larger stakeholders".

## Related protocols

[GHOSTDAG](/wiki/economics/defi/consensus/ghostdag), by the same two authors with Shai Wyborski, drops the requirement of a single chain and orders every block, including the ones GHOST only counts. [GRANDPA](/wiki/economics/defi/consensus/grandpa), Polkadot's finality protocol, applies the heaviest-subtree idea to votes when it finalizes a chain.

## Sources

- Sompolinsky & Zohar, [Secure High-Rate Transaction Processing in Bitcoin](https://eprint.iacr.org/2013/881) (2013; full version)
- Wood, [Ethereum: A Secure Decentralised Generalised Transaction Ledger](https://web.archive.org/web/20210530091843/https://ethereum.github.io/yellowpaper/paper.pdf) (the Yellow Paper, Petersburg version, May 2021)
- Buterin et al., [Combining GHOST and Casper](https://arxiv.org/abs/2003.03052) (2020)
- Ethereum consensus specifications, [`specs/phase0/fork-choice.md`](https://github.com/ethereum/consensus-specs/blob/master/specs/phase0/fork-choice.md), read 10 October 2026
- Schwarz-Schilling, Neu, Monnot, Asgaonkar, Tas & Tse, [Three Attacks on Proof-of-Stake Ethereum](https://arxiv.org/abs/2110.10086) (2021)
- ethereum.org, [Ethereum proof-of-stake attack and defense](https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/attack-and-defense/), read 10 October 2026
