---
title: "Proof of Burn and Proof of Transfer"
weight: 50
---

A proof of burn shows that someone has destroyed cryptocurrency on purpose. The coins are sent, in an ordinary transaction, to an address that nobody can spend from, and the transaction sitting permanently in that chain's history is the proof. Anyone can check it, and the coins are gone for good. A proof of transfer is the same payment sent to other participants in place of the unspendable address.

Both turn spending into standing. They have been used in two ways: once, to hand out a new token to whoever burned an old one, and continuously, as the cost of competing to produce each block of a chain. Only the second makes them a [Sybil-resistance mechanism](/wiki/economics/defi/sybil-resistance), in which the scarce resource is currency given up, the chain's own or another chain's. The Bitcoin wiki's page on the idea observes that the coins burned have so far all been mined by [proof of work](/wiki/economics/defi/sybil-resistance/proof-of-work) somewhere, so that "the ultimate source of scarcity remains the proof-of-work-mined 'fuel'."

The Bitcoin wiki's summary of the idea, which later authors credit to Iain Stewart in 2012: miners "should show proof that they burned some coins - that is, sent them to a verifiably unspendable address. This is expensive from their individual point of view, just like proof of work; but it consumes no resources other than the burned underlying asset."

## What makes a burn a proof

In Bitcoin an address is the hash of a spending condition. Coins sent to an address for which no satisfiable condition is known cannot be moved again. The simplest way to make such an address is to choose one that is obviously not the output of a hash, such as a readable string padded with a repeated letter.

Karantias, Kiayias and Zindros gave the first formal definition in 2019, with three properties:

- **Unspendability.** An address that verifies as a burn address cannot be spent from.
- **Binding.** The burn can be tied to some data, such as the identity of whoever should get credit for it.
- **Uncensorability.** A burn address is indistinguishable from an ordinary one, so miners on the source chain cannot refuse burn transactions.

A scheme is secure in their definition if it has the first two. The third is optional, and a well-known fixed burn address does not have it.

## Burning once: distribution

Counterparty, a token system built on Bitcoin, created its whole token supply this way. Its documentation says the process "was active between January 2nd and February 3rd of 2014", and that anyone could "destroy bitcoins by sending them" to the address `1CounterpartyXXXXXXXXXXXXXXXUWLpVr`, receiving between 1,000 and 1,500 tokens per bitcoin, more for burning earlier. Counterparty's own ledger of those burns adds up to about 2,125 bitcoin.

The stated attraction was fairness. A burn "does not provide the founders with starting capital", since nobody receives what is destroyed. This use is a distribution method, and Counterparty produces no blocks of its own.

## Burning continuously: mining

Stewart's proposal was for burning as an ongoing mining process, under the slogan "Burnt coins are mining rigs!". A burn buys a simulated mining rig: a chance, repeated over many blocks, of being chosen to produce one. Real rigs wear out, and the proposal has the simulated ones do so too, with each burn's strength decaying over time so that a participant must keep burning to keep its share.

Slimcoin, launched in 2014, implemented a version of this in which participants burn its own coin. Its whitepaper draws the same comparison: "Burning coins can be parallel to buying hardware for proof-of-work mining." Slimcoin is a hybrid in which blocks are also produced by proof of work and [proof of stake](/wiki/economics/defi/sybil-resistance/proof-of-stake), and a burn-minted block may only follow a proof-of-work block. No chain was found that relies on burning alone.

## Proof of transfer: Stacks

Stacks is a chain that records its progress in Bitcoin transactions. Its original specification, from 2018, had miners burn bitcoin. A 2020 proposal, Stacks improvement proposal 007, replaced most of the burning: "rather than destroying the base cryptocurrency, miners transfer the base cryptocurrency as a reward to owners of the new cryptocurrency". In its initial phase it kept burning in two cases, and it scheduled a later "sunset" back to burning. The first version went live in January 2021.

The mechanism has three parts.

**Miners bid in bitcoin.** For each Bitcoin block, a would-be Stacks miner sends a Bitcoin transaction committing some amount. One bidder is chosen by a lottery weighted by the amount sent, using a verifiable random function (VRF), a function whose random output comes with a proof that it was computed honestly. The winner produces Stacks blocks and earns newly issued Stacks tokens. The bitcoin is spent whether or not the bid wins.

**Holders lock tokens and are paid the bids.** Holders of the Stacks token who lock it up for a *reward cycle* of 2,100 Bitcoin blocks, about two weeks, receive the miners' bitcoin. Under the 2020 design it was paid directly to their Bitcoin addresses.

**The lockers sign the blocks.** Since an upgrade named Nakamoto, which took effect at Bitcoin block 867,867 in late October 2024, the participants who have locked tokens also act as signers. A Stacks block is accepted only with signatures carrying at least 70% of the total signing weight, and weight is the amount locked. The proposal for that upgrade, Stacks improvement proposal 021, claims that reversing a confirmed transaction becomes "at least as hard as reversing a Bitcoin transaction" once two further changes of miner have built on it, and admits the cost: "the chain can halt indefinitely if Stackers cannot agree on the chain tip". Stackers is its name for the participants who have locked tokens.

So the right to propose blocks is bought with another chain's currency, and the right to approve them comes from stake in the chain's own. The two halves use different resources.

### What changed in 2026

A further upgrade on 30 July 2026 replaced the arrangement described above, and Stacks' documentation now says to read the two proposals "as history rather than current behavior". Miners still bid bitcoin, the lottery is still weighted by the amount, and the cycle is still 2,100 blocks. The destination changed: "Miner BTC no longer pays stacker reward addresses directly and nothing is burned". Every bid goes to a single address feeding a reward pool, from which participants are paid in a fixed order. Holders of bitcoin can now take part by bonding bitcoin alongside a lock of Stacks tokens, where before only the token counted. The documentation says of bonding: "Access is not yet general."

The documentation also states that locked tokens are never taken as a penalty. A signer that fails to perform "forfeits rewards, not principal."

## Limits

**The security is the other chain's.** A burn or transfer is only as final as the source chain's history. If the Bitcoin transactions recording the bids were reorganized away, the standing they bought would go with them.

**Miners of the source chain have an edge.** They decide which transactions enter a Bitcoin block, including their own bids and their competitors'. This is the reason the formal definition asks for uncensorability, and a fixed public destination address does not provide it.

**A burn destroys value and a transfer redirects it.** Burning imposes the cost on the participant and benefits every other holder slightly. Transferring pays a specific group, which gives that group a reason to support the chain and makes the scheme an income stream as much as a security mechanism.

Destroying part of each transaction fee, as [Ethereum does](/wiki/economics/defi/chains/ethereum/blobs), is sometimes called burning as well. It is a monetary policy and plays no part in deciding who produces blocks.

## Sources

- Bitcoin Wiki, [Proof of burn](https://en.bitcoin.it/wiki/Proof_of_burn), read 10 October 2026
- Karantias, Kiayias & Zindros, [Proof-of-Burn](https://eprint.iacr.org/2019/1096) (2019)
- Counterparty documentation, [What is XCP](https://docs.counterparty.io/docs/basics/what-is-xcp/), and the project's [ledger of mainnet burns](https://github.com/CounterpartyXCP/counterparty-core/blob/master/counterparty-core/counterpartycore/lib/messages/data/mainnet_burns.csv)
- P4Titan, [Slimcoin: A Peer-to-Peer Crypto-Currency with Proof-of-Burn](https://github.com/slimcoin-project/slimcoin-project.github.io/raw/master/whitepaperSLM.pdf) (17 May 2014)
- Stacks, [SIP-007: Stacking Consensus](https://github.com/stacksgov/sips/blob/main/sips/sip-007/sip-007-stacking-consensus.md) (2020) and [SIP-021: Fast and Reliable Blocks through PoX-assisted Block Propagation](https://github.com/stacksgov/sips/blob/main/sips/sip-021/sip-021-nakamoto.md) (2023)
- Stacks documentation, [Proof of Transfer (PoX)](https://docs.stacks.co/learn/stacks-101/proof-of-transfer), [How Are Blocks Mined?](https://docs.stacks.co/learn/block-production/mining), [Signing](https://docs.stacks.co/learn/block-production/signing) and [Staking](https://docs.stacks.co/learn/block-production/staking), read 10 October 2026
