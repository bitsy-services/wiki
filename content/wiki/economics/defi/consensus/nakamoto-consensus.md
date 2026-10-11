---
title: "Nakamoto Consensus"
weight: 10
---

Nakamoto consensus is the rule by which Bitcoin's nodes agree on one history of transactions. Among all the valid chains of blocks a node has seen, it treats the one with the most accumulated [proof of work](/wiki/economics/defi/sybil-resistance/proof-of-work) as the true history, and it tries to add its own next block to the end of that chain. A block may be added by whoever first solves a hash puzzle built on the previous block.

That is the whole mechanism. Nodes send no votes, keep no list of participants, and exchange no message saying that agreement has been reached. A node needs only the blocks themselves, so anyone can join or leave without telling anyone.

The cost of that openness is that agreement is never final. A block can always be displaced by a competing chain that overtakes the one it sits on. What the rule provides is that the chance of this falls quickly with each block added on top, as long as attackers hold less than half of the network's computing power.

The name comes from Satoshi Nakamoto's 2008 Bitcoin paper, which does not use it. The paper says only "this consensus mechanism".

## The rule

The paper states the rule as the longest chain: "Nodes always consider the longest chain to be the correct one and will keep working on extending it." Elsewhere it glosses *longest* as most work: "The majority decision is represented by the longest chain, which has the greatest proof-of-work effort invested in it."

The implementation follows the gloss. Bitcoin Core adds up the work each block represents, which depends on how hard the puzzle was when the block was found, and selects "the chain with the most work in it". The two readings pick the same chain unless the puzzle's difficulty differs between branches.

Blocks are meant to arrive ten minutes apart on average. The puzzle's difficulty is recalculated every 2,016 blocks, which is two weeks' worth at that rate, from the time the previous 2,016 actually took. One recalculation can change the difficulty by a factor of four at most.

## Forks and confirmations

Two miners sometimes find a block at nearly the same moment, and the network briefly holds two chains of equal weight. The paper's handling is that nodes "work on the first one they received, but save the other branch in case it becomes longer. The tie will be broken when the next proof-of-work is found and one branch becomes longer". The losing block is discarded.

Because any recent block may still lose such a race, or be deliberately overtaken, a recipient waits until some number of blocks, *z*, have been added after the one holding the payment. Section 11 of the paper computes the probability that an attacker who is *z* blocks behind ever catches up, for an attacker who finds the next block with probability *q*:

| Attacker's share *q* | Blocks behind *z* | Probability of catching up |
|---|---|---|
| 10% | 5 | 0.0009137 |
| 10% | 6 | 0.0002428 |
| 30% | 5 | 0.1773523 |
| 30% | 10 | 0.0416605 |

The same section gives the number of blocks needed to push that probability below 0.1%: 5 blocks against an attacker with 10% of the power, 24 against 30%, and 340 against 45%.

The calculation assumes the honest blocks took the average time to find and that the attacker follows one particular strategy. A later formal analysis by Garay, Kiayias and Leonardos calls it "oversimplified", since an attacker can also try to split the honest miners across branches.

## The limit is half the computing power

The paper's condition is in its abstract: "As long as a majority of CPU power is controlled by nodes that are not cooperating to attack the network, they'll generate the longest chain and outpace attackers."

An attacker above that line can out-build everyone else indefinitely, and so can replace any recent stretch of the chain. The paper is specific about what that does and does not allow. It does not allow "creating value out of thin air or taking money that never belonged to the attacker", because other nodes still reject invalid transactions. "An attacker can only try to change one of his own transactions to take back money he recently spent." Paying someone, receiving the goods, and then replacing the chain with one in which the payment never happened is called a *double spend*.

Chains have been reorganized this way. In January 2019 Coinbase reported fifteen reorganizations of the Ethereum Classic chain, twelve of which contained double spends "totaling 219,500 ETC (~$1.1M)". The deepest replaced 123 blocks. Coinbase did not estimate the attacker's share of the computing power, and its own description of majority control is "a known limitation to the proof-of-work model".

Two later results qualify the one-half figure.

**The bound depends on the network being fast.** Garay, Kiayias and Leonardos proved two properties of the protocol in 2015. *Common prefix* says that honest nodes' chains agree once the last *k* blocks are cut off, except with a probability that falls exponentially in *k*. *Chain quality* says that in any long enough run of blocks, the share contributed by honest miners has a floor. Both are proved for a fixed number of participants. The paper's security result for Bitcoin's ledger assumes "high network synchronicity" and an adversary with "strictly less than 1/2" of the power, and the paper adds that "the adversarial bound needed for security decreases as the network desynchronizes". A third property, *chain growth*, was named in follow-up work by Kiayias and Panagiotakos.

**A minority can take more than its share of the rewards.** Eyal and Sirer showed in 2013 that a group of miners can profit by keeping newly found blocks secret and releasing them to win races. Their threshold depends on γ, the fraction of honest miners who end up building on the group's block when two blocks compete. The strategy pays for any group larger than (1 − γ) / (3 − 2γ) of the network: one third when γ is 0, one quarter when γ is 1/2, and any size at all when γ is 1. This is an attack on who gets paid, not on the history of transactions, but it removes the incentive that is supposed to keep miners honest.
## Block rate is bounded by propagation

A block takes time to reach every node. When blocks are found faster, more of them are found by miners who have not yet heard of the latest block, and those blocks land on side branches. Work on side branches does not lengthen the main chain, so an attacker has less to outrun. Sompolinsky and Zohar put it this way: "more frequent block creation events ... result in more conflicts between blocks, which severely reduces the level of security from attacks."

A long interval between blocks is how the rule keeps most honest work on one chain. [GHOST](/wiki/economics/defi/consensus/ghost) is the proposal to count the side branches, and [GHOSTDAG](/wiki/economics/defi/consensus/ghostdag) the proposal to keep them.

## Who runs it

As of October 2026, from each project's own code or documentation:

| Chain | Target block interval | Notes |
|---|---|---|
| Bitcoin | 10 minutes | |
| Litecoin | 2.5 minutes | |
| Dogecoin | 1 minute | Difficulty is recalculated after every block |
| Bitcoin Cash | 10 minutes | Difficulty is recalculated after every block |
| Monero | | The puzzle function has been RandomX since November 2019 |
| Ethereum Classic | | Its site commits to "remaining on Proof of Work indefinitely" |
| Zcash | | The puzzle function is Equihash |

Ethereum ran a version of this rule until September 2022, when it moved to proof of stake under [Casper FFG](/wiki/economics/defi/consensus/casper-ffg).

The rule does not need proof of work in particular. It needs a lottery that picks who may add the next block, in proportion to something scarce. [Ouroboros](/wiki/economics/defi/consensus/ouroboros) runs a longest-chain rule with a lottery weighted by stake.

## Sources

- Nakamoto, [Bitcoin: A Peer-to-Peer Electronic Cash System](https://bitcoin.org/bitcoin.pdf) (2008)
- Bitcoin Core, [`src/validation.cpp`](https://github.com/bitcoin/bitcoin/blob/master/src/validation.cpp), [`src/pow.cpp`](https://github.com/bitcoin/bitcoin/blob/master/src/pow.cpp) and [`src/kernel/chainparams.cpp`](https://github.com/bitcoin/bitcoin/blob/master/src/kernel/chainparams.cpp), read 10 October 2026
- Garay, Kiayias & Leonardos, [The Bitcoin Backbone Protocol: Analysis and Applications](https://eprint.iacr.org/2014/765) (2015; revision of August 2020)
- Eyal & Sirer, [Majority is not Enough: Bitcoin Mining is Vulnerable](https://arxiv.org/abs/1311.0243) (2013)
- Sompolinsky & Zohar, [Secure High-Rate Transaction Processing in Bitcoin](https://eprint.iacr.org/2013/881) (2013)
- Nesbitt, [Deep Chain Reorganization Detected on Ethereum Classic (ETC)](https://web.archive.org/web/2019/https://blog.coinbase.com/ethereum-classic-etc-is-currently-being-51-attacked-33be13ce32de), The Coinbase Blog, 7 January 2019
- Ethereum Classic, [Proof of Work](https://ethereumclassic.org/why-classic/proof-of-work/), and the [Zcash Protocol Specification](https://zips.z.cash/protocol/protocol.pdf) dated 8 October 2026
