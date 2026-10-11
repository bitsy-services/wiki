---
title: "Proof of History and Tower BFT"
weight: 150
---

Proof of History is a chain of hashes that Solana uses as a clock. One machine runs a hash function over and over, each time feeding in the previous output, and publishes the count and the output at intervals. Because each output is needed to compute the next, the chain can be produced only one step at a time, so a chain of a given length shows that some amount of time went into making it.

It is not a way of reaching agreement, and it does not decide who may take part. The paper that introduced it says it is to be "used alongside a consensus algorithm". On Solana that algorithm is Tower BFT, a voting protocol among validators weighted by [stake](/wiki/economics/defi/sybil-resistance/proof-of-stake). BFT stands for Byzantine fault tolerant: able to withstand participants that behave arbitrarily. This page covers the clock, the voting built on it, and Alpenglow, the protocol proposed to replace both. The [Consensus](/wiki/economics/defi/consensus) overview has the general problem.

## The hash chain

Anatoly Yakovenko's paper defines Proof of History as "a sequence of computation that can provide a way to cryptographically verify passage of time between two events". The function is a cryptographic hash such as SHA-256, "run in a sequence on a single core, its previous output as the current input, periodically recording the current output, and how many times its been called."

```text
hash 1 = H(seed)
hash 2 = H(hash 1)
hash 3 = H(hash 2)
...
hash 300 = H(hash 299)
```

Nobody can know hash 300 without computing the 299 before it, and the steps cannot be shared among machines. In the paper's words, "we can thus infer from the data structure that real time has passed between index 0 and index 300."

An event is placed in time by mixing it into the chain: its data, or a hash of it, is appended to the input of the next step. That shows the event existed before every later hash was computed. The bound runs one way only. The paper says it "can guarantee that the data was created sometime before the next hash was generated", and nothing about how long before.

Checking is faster than making. A verifier holding the published outputs can cut the chain into segments and check each on a separate processor core, since each segment starts from a known value.

The paper does not call the construction a verifiable delay function. That term, for a function that takes a set time to compute and is quick to check, was attached to it later.

## What the clock is for

Validators that agree on a clock do not need to exchange messages to work out whose turn it is. Solana divides the chain into *ticks* and groups 64 ticks into a *slot*, the period in which one validator, the leader, produces a block. Leaders are assigned for an *epoch* of 432,000 slots at a time, by a schedule every validator computes locally from the stake distribution, weighted by stake. Each leader holds four consecutive slots.

The slot's target length has been 400 milliseconds. A proposal drafted in May 2026, which gives 400 as the current value, would lower it in stages to 200. The development branch of the software development kit already carries 300 as its default, with a warning that the default may not match the network, so the value in force on a given date has to be checked. It is a target in any case: the network "does not produce slots at exactly the target rate".

## Tower BFT

Tower BFT is the rule validators follow when they vote on forks. A validator votes for a block by signing its hash, and each vote carries a *lockout*: a period, measured in slots on the clock, during which the validator may not vote for a block on a competing fork.

Lockouts double. A new vote starts with a lockout of 2 slots, and each later vote on the same fork doubles the lockout of every earlier vote beneath it in the validator's stack. A vote that has 5 later votes on top of it is locked for 2⁶ = 64 slots, and one with 31 on top for 2³². The deeper a block is in a validator's own voting history, the longer that validator is committed to it. At 32 votes deep a vote reaches the maximum lockout and leaves the stack.

A block is called *confirmed* when validators holding two thirds of the stake have voted for it, and *finalized* when, in addition, 31 confirmed blocks have been built on top of it. The authors of Alpenglow give the resulting time to finality as 12.8 seconds.

The clock is what makes lockouts enforceable without communication, since "locked for 32 slots" means the same thing to every validator. The documentation describes destroying the stake of a validator that breaks a lockout as "proposed". The Alpenglow proposal says of Tower BFT that it "does not have a security proof, which is concerning."

## Outages

The network has stopped producing blocks more than once. Two reports from the project itself:

- **14 September 2021**, 17 hours. A flood of automated transactions at a token launch exhausted validators' memory, "which caused many validators to crash forcing the network to slow down and eventually stall."
- **6 February 2024**, about five hours. A bug caused validators to recompile the same program in an endless loop, and block finalization stopped from 09:53 to 14:55 UTC.

Both were software failures that took down enough validators to stop the two-thirds vote, which is how a [voting protocol](/wiki/economics/defi/consensus#finality-or-availability) fails: it stops. Neither was a fault in the clock or in the voting rule.

## Alpenglow

Alpenglow is the consensus protocol specified in Solana Improvement Document 326 (SIMD-0326), which was still marked as under review in October 2026. It changes "the core consensus protocol from the current one, based on Proof-of-History and TowerBFT".

- **Consensus stops depending on the clock.** Validators use short timeouts measured locally: "Their purpose is akin to Proof-of-History, but without any notion of synchronized time."
- **Lockouts go.** A block is finalized by "one round of votes for the block from 80% of the stake", or failing that by "two rounds of votes for the block from 60% of the stake".
- **The fault assumption changes.** The proposal calls it "20+20": up to 20% of stake adversarial and a further 20% unresponsive. It states the trade directly. Alpenglow "does not have the 33% byzantine security that can be achieved with two-round voting protocols".

Anza's announcement of May 2025 put the expected time to finality at "about 150 ms (median)", a figure from "simulations with the current mainnet stake distribution, not counting computation overhead".

**As of 10 October 2026 Alpenglow was not running on Solana's mainnet.** The feature tracker kept by Anza, which maintains the main validator client, listed it under "Pending Mainnet Beta Activation". It had been activated on the test and development networks. Proof of History and Tower BFT were still what the mainnet ran.

## Sources

- Yakovenko, [Solana: A new architecture for a high performance blockchain](https://solana.com/solana-whitepaper.pdf), version 0.8.13
- Anza documentation, [Tower BFT](https://docs.anza.xyz/implemented-proposals/tower-bft), [Commitment](https://docs.anza.xyz/consensus/commitments) and [Leader rotation](https://docs.anza.xyz/consensus/leader-rotation), read 10 October 2026
- Solana SDK, [`clock/src/lib.rs`](https://github.com/anza-xyz/solana-sdk/blob/master/clock/src/lib.rs), read 10 October 2026
- [SIMD-0326: Alpenglow](https://github.com/solana-foundation/solana-improvement-documents/blob/main/proposals/0326-alpenglow.md) and [SIMD-0525: Reduce Slot Times](https://github.com/solana-foundation/solana-improvement-documents/pull/525), read 10 October 2026
- Anza, [Alpenglow: A New Consensus for Solana](https://www.anza.xyz/blog/alpenglow-a-new-consensus-for-solana) (19 May 2025)
- Anza, [Agave feature gate tracker](https://github.com/anza-xyz/agave/wiki/Feature-Gate-Tracker-Schedule), read 10 October 2026
- Solana, [outage report of 20 September 2021](https://solana.com/news/9-14-network-outage-initial-overview) and [outage report of 9 February 2024](https://solana.com/news/02-06-24-solana-mainnet-beta-outage-report)
