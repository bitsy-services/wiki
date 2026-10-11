---
title: "Proof of Work"
weight: 10
---

A proof of work is a piece of data that shows its producer performed a certain amount of computation. The producer searches for a value that, combined with some fixed data and put through a hash function, gives a result below a target number. The only known way to find such a value is to try one after another, and the lower the target, the more tries it takes on average. Anyone can check a claimed value with a single hash.

In a blockchain the puzzle decides who may add the next block. Whoever finds a valid value first adds it, so each participant's chance is its share of all the hashing being done. Computation becomes the scarce thing that a participant must hold to have a say, which is what makes proof of work a [Sybil-resistance mechanism](/wiki/economics/defi/sybil-resistance): running a million nodes gives no advantage over running one with the same hardware.

Proof of work does not say which chain is the right one when there are two. That is the job of a fork-choice rule built on top of it: [Nakamoto consensus](/wiki/economics/defi/consensus/nakamoto-consensus) in Bitcoin, or [GHOST](/wiki/economics/defi/consensus/ghost) and [GHOSTDAG](/wiki/economics/defi/consensus/ghostdag) elsewhere.

## The puzzle in Bitcoin

A Bitcoin block begins with an 80-byte header. It holds a version number, the hash of the previous block's header, a single hash summarizing the block's transactions, a timestamp, the current target in compact form, and a 32-bit field called the *nonce* that exists to be varied. A miner hashes the header with SHA-256 applied twice. The block is valid if the result, read as a 256-bit number, is at or below the target. If it is not, the miner changes the nonce and hashes again.

Bitcoin's paper describes the condition as a hash that "begins with a number of zero bits", which is a simplification of the comparison the software makes. It gives the asymmetry in one sentence: "The average work required is exponential in the number of zero bits required and can be verified by executing a single hash."

Two properties of the header matter as much as the hash.

- **The work is bound to one block.** The header commits to the transactions and to the previous block, so a solution cannot be moved to a different block or prepared before the previous block is known.
- **The work accumulates.** Each header contains the hash of the one before, so changing an old block invalidates the puzzle solution of every block after it. Rewriting history means redoing all of that work and then catching up with the network.

The target is recalculated every 2,016 blocks so that blocks keep arriving about ten minutes apart, however much hardware joins or leaves.

## What the work is for

Bitcoin's paper gives the reason in terms of what would fail otherwise: "If the majority were based on one-IP-address-one-vote, it could be subverted by anyone able to allocate many IPs. Proof-of-work is essentially one-CPU-one-vote."

The resource has two properties that set it apart from the alternatives. It sits outside the ledger, in hardware and electricity, so the protocol cannot see who holds how much of it and cannot take it away from a participant who misbehaves. And it is spent: every block costs fresh work, so an old block carries the cost of making it. [Proof of stake](/wiki/economics/defi/sybil-resistance/proof-of-stake) is the opposite on both counts.

Miners are paid for the expense in new coins and fees. Bitcoin's subsidy started at 50 bitcoin per block and halves every 210,000 blocks. It has been 3.125 since block 840,000 in April 2024, and the next halving is at block 1,050,000.

## Where it came from

The idea is older than blockchains, and its first use was against spam.

- **1992.** Dwork and Naor proposed "to require a user to compute a moderately hard, but not intractable, function in order to gain access to the resource", with unsolicited email as the example. They called the functions *pricing functions* and built them from number-theoretic problems such as extracting square roots modulo a prime.
- **1997.** Adam Back's Hashcash used a hash: a sender had to find an input whose hash had a required number of leading zero bits. His requirement for such a function was that it "should be efficiently verifiable, but parameterisably expensive to compute". Bitcoin's paper cites Hashcash as its model.
- **1999.** Jakobsson and Juels formalized it under its present name: "We formalize the notion of a proof of work (POW)", a protocol in which "a prover demonstrates to a verifier that she has performed a certain amount of computational work in a specified interval of time". The same paper asks whether the work could be reused for something else, a question taken up under [proof of useful work](/wiki/economics/defi/sybil-resistance/proof-of-useful-work).

The original use survives. A [Nostr](/wiki/networking/nostr) relay can demand a small proof of work on each message, and the [IOTA Tangle](/wiki/economics/defi/chains/iota/tangle) asked for one on each transaction in place of a fee.

## Other puzzle functions

Other chains use functions other than SHA-256. Where a reason is given, it is to limit specialized hardware, or the concentration of mining attributed to it. The hardware in question is the application-specific integrated circuit (ASIC), a chip built to compute one function and nothing else.

| Chain | Function | What its own documents say |
|---|---|---|
| Litecoin, Dogecoin | scrypt | Dogecoin's documentation calls it "a simplified variant of the scrypt key derivation function". The documents read give no reason for the choice |
| Monero | RandomX, since 30 November 2019 | "optimized for general-purpose CPUs", using random code execution and memory-hard techniques "to minimize the efficiency advantage of specialized hardware" |
| Zcash | Equihash | It "attempted to address the problem of mining centralization by use of the Equihash memory-hard proof-of-work algorithm" |
| Ethereum Classic | Etchash, a modification of Ethereum's original Ethash | The large dataset the function reads was intended "to provide ASIC resistance" |

The record is mixed. Zcash's specification puts its own attempt in the past tense, and the Ethereum Classic proposal that introduced Etchash acknowledges that ASICs for the function exist.

## Merged mining

A small chain can borrow the work done on a larger one that uses the same function. Dogecoin has done this since block 371,337 in 2014, under a scheme called AuxPoW that "enables miners to submit work done while mining other coins, as work on the Dogecoin block chain". The first of two reasons its developers gave was security: "the effective hashrate of the coin is increased by these additional miners, making it harder to perform a 51% attack against the coin".

## Limits

**Whoever holds most of the hashing controls recent history.** The puzzle makes rewriting the chain expensive and does not make it impossible. The [conditions and the documented cases](/wiki/economics/defi/consensus/nakamoto-consensus#the-limit-is-half-the-computing-power) are on the Nakamoto consensus page.

**The protection is only as large as the hardware pointed at the chain.** A chain that attracts a small share of the machines able to compute its function can be overtaken by a fraction of the rest. That is the case merged mining exists to address.

**The cost is the mechanism.** A puzzle that was cheap to solve would be cheap to out-solve. Proposals to make the expense smaller, or to make it pay for something, are proposals for a different resource: [stake](/wiki/economics/defi/sybil-resistance/proof-of-stake), [disk space](/wiki/economics/defi/sybil-resistance/proof-of-space), or [useful computation](/wiki/economics/defi/sybil-resistance/proof-of-useful-work).

## Sources

- Nakamoto, [Bitcoin: A Peer-to-Peer Electronic Cash System](https://bitcoin.org/bitcoin.pdf) (2008)
- Bitcoin developer reference, [Block Chain](https://developer.bitcoin.org/reference/block_chain.html), and Bitcoin Core [`src/validation.cpp`](https://github.com/bitcoin/bitcoin/blob/master/src/validation.cpp), read 10 October 2026
- Dwork & Naor, [Pricing via Processing or Combatting Junk Mail](https://doi.org/10.1007/3-540-48071-4_10) (1992)
- Back, [Hashcash - A Denial of Service Counter-Measure](http://www.hashcash.org/papers/hashcash.pdf) (2002)
- Jakobsson & Juels, [Proofs of Work and Bread Pudding Protocols](https://doi.org/10.1007/978-0-387-35568-9_18) (1999)
- tevador, [RandomX README](https://github.com/tevador/RandomX/blob/master/README.md); [Zcash Protocol Specification](https://zips.z.cash/protocol/protocol.pdf), 8 October 2026; Ethereum Classic, [ECIP-1099: Calibrate Epoch Duration](https://github.com/ethereumclassic/ECIPs/blob/master/_specs/ecip-1099.md)
- Dogecoin, [release notes for Dogecoin Core 1.8](https://github.com/dogecoin/dogecoin/releases/tag/v1.8.0) (August 2014)
