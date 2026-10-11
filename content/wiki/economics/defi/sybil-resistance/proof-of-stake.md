---
title: "Proof of Stake"
weight: 20
---

Proof of stake is the practice of weighting the participants in a blockchain's consensus by how much of the chain's own currency each has locked up in it. A participant who wants to produce or vote on blocks, a *validator*, deposits coins in the ledger. The protocol then chooses block producers and counts votes in proportion to those deposits.

The deposit is the scarce thing that keeps one party from posing as many, which makes proof of stake a [Sybil-resistance mechanism](/wiki/economics/defi/sybil-resistance). A thousand validators holding one coin each carry the same weight as one validator holding a thousand.

Two facts about the resource separate it from [proof of work](/wiki/economics/defi/sybil-resistance/proof-of-work), and most of what is distinctive about proof-of-stake chains follows from them.

- **The resource is on the ledger.** The protocol knows exactly how much stake exists and who holds it, so it can require a fixed fraction of it to sign a block, and it can destroy the deposit of a validator proven to have cheated.
- **The resource is locked, not spent.** Signing a block costs nothing beyond running a computer. Old blocks carry no cost of production, and a validator that has withdrawn its deposit has nothing left to lose.

Stake supplies the weights and nothing more. The agreement itself is reached by a consensus protocol that uses those weights: a longest-chain rule in [Ouroboros](/wiki/economics/defi/consensus/ouroboros), rounds of voting in [Tendermint](/wiki/economics/defi/consensus/tendermint), a finality gadget in [Casper FFG](/wiki/economics/defi/consensus/casper-ffg) and [GRANDPA](/wiki/economics/defi/consensus/grandpa), sampled committees in [Algorand](/wiki/economics/defi/consensus/algorand). The returns and risks for the person staking are on the [Staking](/wiki/economics/defi/markets/staking) page.

## Entering and leaving

On Ethereum a validator activates with a deposit of at least 32 ETH. Its weight is its *effective balance*. Until 2025 that was capped at 32 ETH as well, so an operator with more stake ran many validators. Since the upgrade of 7 May 2025, which included Ethereum Improvement Proposal 7251 (EIP-7251), a validator that opts in can carry an effective balance of up to 2,048 ETH.

Leaving is slow on purpose. A validator that asks to exit joins a queue that limits how much stake may leave per epoch, an epoch being 6.4 minutes. Once it has exited, its funds stay locked for a further 256 epochs, about 27 hours. The stake has to stay within reach for long enough that misbehaviour can be proven and punished.

## Slashing

*Slashing* is the destruction of some or all of a validator's deposit for misbehaviour that can be proven from its own signatures. Ethereum's documentation lists three offences:

- proposing two different blocks for the same slot, the fixed interval in which one block may be proposed;
- voting for two different candidates for the same position, a *double vote*;
- casting a vote that surrounds an earlier one, a *surround vote*.

The last two are the [two rules of Casper FFG](/wiki/economics/defi/consensus/casper-ffg#the-two-rules).

The penalty comes in three parts. Immediately, the validator loses 1/4096 of its effective balance, which is 0.0078125 ETH for a validator with 32. It is then removed from the validator set and its funds are locked for at least 8,192 epochs, about 36 days. Halfway through that period it loses a further fraction equal to three times the share of all stake that was slashed in the same period, up to its whole balance.

The third part is what makes slashing a defence against attacks and not just against mistakes. One validator that double-signs through a configuration error loses almost nothing. If validators holding a third of the stake are slashed together, which is what an attack on finality requires, three times one third is the whole deposit.

Slashing is not universal. [Avalanche](/wiki/economics/defi/consensus/avalanche#on-the-avalanche-network) and [Algorand](/wiki/economics/defi/consensus/algorand#taking-part) never destroy stake. They withhold rewards or suspend the account.

## Nothing at stake

A proof-of-work miner facing two competing forks has to choose where to point its hardware. A validator does not. Vitalik Buterin described the problem in 2014: in a design that simply copies proof of work with coins in place of mining rigs, "if there are multiple forks, the optimal strategy is to vote on all forks at once. This is the core of 'nothing at stake'."

Deposits and slashing are the answer. Signing on two forks is exactly the double vote that the slashing rules detect, and the evidence can be included in either chain.

## Long-range attacks

The answer has a time limit. In the same essay: "the user has to have the right to withdraw the security deposit eventually, and once the deposit is withdrawn there is no longer any incentive not to vote on a long-range fork starting far back in time using those coins."

An attacker who obtains the old keys of validators that once held more than two thirds of the stake and have since withdrawn can build an alternative history starting from that point. It costs nothing, since there is no work to redo. Nodes that were online at the time are not fooled, because they saw the real chain first. A node joining later has only the data in front of it, and both histories are signed by validators who were legitimate when they signed.

Buterin's name for what proof of stake accepts in exchange is *weak subjectivity*. A proof-of-work chain is objective in his terms: a new node with the protocol rules and all published blocks reaches the same conclusion as everyone else. A proof-of-stake chain needs one more input. Nodes refuse to revert more than a set number of blocks, and a node that is new or has been offline longer than the deposit lock must "get a recent block hash from a friend, a blockchain explorer, or simply their software provider". Ethereum implements this as weak subjectivity checkpoints, which its documentation calls "revert limits".

[Ouroboros Genesis](/wiki/economics/defi/consensus/ouroboros#choosing-a-chain) takes a different route and compares how densely each history was populated just after the fork, which lets a node start from the first block alone.

## Variants

The variants differ in who is allowed to validate and how other holders take part.

| Variant | How the validator set is formed | Example |
|---|---|---|
| Bonded | Anyone who deposits the minimum is a validator | Ethereum |
| Delegated | Token holders vote, and a small fixed number of the candidates with most votes produce blocks | TRON, which sets the number at 27 |
| Nominated | Holders back validators with their own stake, and an election picks the set from the backed candidates | Polkadot |
| Liquid | A pool deposits on behalf of many holders and issues them a tradable receipt | Pools on Ethereum, described under [Staking](/wiki/economics/defi/markets/staking#delegated-staking-and-liquid-staking) |

A small elected set votes quickly and is easy to coordinate, for better and for worse. [Proof of authority](/wiki/economics/defi/sybil-resistance/proof-of-authority) is the limiting case, where the set is appointed.

## History

An early design under the name was PPCoin, described by Sunny King and Scott Nadal in a paper of August 2012. It was a "hybrid design" in their words, in which "proof-of-stake replaces proof-of-work to provide most of the network security". Weight came from *coin age*, "currency amount times holding period", so that ten coins held for ninety days counted as 900 coin-days. The design also relied on "a centrally broadcasted checkpoint mechanism". The paper notes that the idea had been "discussed among Bitcoin circles as early as 2011".

Ethereum switched from proof of work on 15 September 2022. ethereum.org relays an estimate by the Crypto Carbon Ratings Institute that the change cut the network's electricity consumption "by more than 99.988%".

## Limits

**The thresholds are fractions of stake.** In the voting protocols, validators holding more than a third of the stake can stop finality by staying silent, and validators holding two thirds decide what is final. Whoever controls that much stake, whether by owning it or by holding other people's in a pool or an exchange, holds that power.

**New nodes need a trusted starting point.** This is the weak-subjectivity requirement above. It is small in practice and it is a real difference from proof of work.

**The protection is denominated in the chain's own currency.** The cost of acquiring a third of the stake, and the size of the deposit that slashing can destroy, move with the token's price.

## Sources

- King & Nadal, [PPCoin: Peer-to-Peer Crypto-Currency with Proof-of-Stake](https://decred.org/research/king2012.pdf) (19 August 2012)
- Buterin, [Proof of Stake: How I Learned to Love Weak Subjectivity](https://blog.ethereum.org/2014/11/25/proof-stake-learned-love-weak-subjectivity), Ethereum Foundation Blog (25 November 2014)
- Ethereum consensus specifications, [`specs/electra/beacon-chain.md`](https://github.com/ethereum/consensus-specs/blob/master/specs/electra/beacon-chain.md) and [`specs/phase0/beacon-chain.md`](https://github.com/ethereum/consensus-specs/blob/master/specs/phase0/beacon-chain.md), read 10 October 2026
- [EIP-7251: Increase the MAX_EFFECTIVE_BALANCE](https://eips.ethereum.org/EIPS/eip-7251)
- ethereum.org, [Proof-of-stake rewards and penalties](https://ethereum.org/developers/docs/consensus-mechanisms/pos/rewards-and-penalties/), [Weak subjectivity](https://ethereum.org/developers/docs/consensus-mechanisms/pos/weak-subjectivity/), [The Merge](https://ethereum.org/roadmap/merge/) and [Ethereum energy consumption](https://ethereum.org/energy-consumption/), read 10 October 2026
- TRON developer documentation, [DPoS](https://github.com/tronprotocol/documentation-en/blob/master/docs/mechanism-algorithm/dpos.md), read 10 October 2026
- Polkadot Wiki, [Polkadot's Consensus Protocols](https://wiki.polkadot.com/learn/learn-consensus/), read 10 October 2026
