---
title: "Algorand Consensus"
weight: 100
---

Algorand's consensus protocol is a Byzantine agreement protocol in which every step of every round is carried out by a different committee, drawn by a private lottery from all accounts in proportion to the currency they hold. Byzantine agreement is agreement among participants some of whom may lie or collude. A round produces one block.

An account finds out that it is on a committee by evaluating a verifiable random function (VRF) on its own secret key and a public value from the chain. A VRF returns a pseudo-random output together with a proof, checkable with the public key, that the output is correct. Nobody else knows the account was selected until it broadcasts its vote with the proof attached. Each member speaks once, and the next step has a new committee.

Gilad, Hemo, Micali, Vlachos and Zeldovich published the design in 2017. It sits between two older approaches. Protocols like [PBFT](/wiki/economics/defi/consensus/pbft) have every participant vote, which limits how many can take part. Chains like Bitcoin let anyone take part and allow temporary forks, so a transaction is trusted only after a wait. Algorand samples a committee small enough to vote quickly from a population of any size.

## Sortition

The paper calls the lottery *cryptographic sortition*. For each step, an account computes the VRF over the round's public seed and the name of the step. The output decides how many of the account's units of currency were drawn.

Each unit of currency is treated as a separate ticket, selected with probability τ / *W*, where τ is the expected committee size and *W* is the total currency. An account holding many units can be drawn several times, and its vote then counts that many times. Selection in proportion to holdings is what defeats fake identities, which makes this a form of [proof of stake](/wiki/economics/defi/sybil-resistance/proof-of-stake): "splitting a user's weight (currency) among Sybils does not affect the number of selected sub-users under his/her control."

Two properties protect the committee itself:

- **Selection is private.** "Since membership selection is non-interactive, an adversary does not know which user to target until that user starts participating".
- **Members are replaced after one message.** Participants "do not keep any private state except for their private keys, which allows Algorand to replace participants immediately after they send a message". Taking over a machine that has already voted gains the attacker nothing for the next step.

## A round today

The developer documentation describes three steps.

| Step | What the committee does | Expected committee weight | Votes needed |
|---|---|---|---|
| Propose | Selected accounts each propose a block | 20 | |
| Soft vote | Narrows the proposals to one, the one with the lowest VRF output, and votes for it | 2,990 | 2,267 |
| Certify vote | Checks that block and votes to certify it | 1,500 | 1,112 |

The sizes are expected weights in units of stake, not head counts, and they are the values in the reference implementation's parameter table. A committee is a random sample, so its thresholds sit above two thirds of its expected weight to leave room for sampling error: 2,267 of 2,990 is 75.8%, and 1,112 of 1,500 is 74.1%. Further steps with their own committees exist for rounds that fail to finish.

## What it assumes

**Honest money.** The paper assumes that honest users hold a fraction of the currency above some threshold *h*, "a constant greater than 2/3". Its published parameters are computed for *h* = 80%, because "as h approaches 2/3, the committee size grows quickly". The one-third figure is the limit of the theory and is not what the committees were sized for.

**Timing, for progress.** Liveness needs what the paper calls *strong synchrony*: most honest users, 95% in its example, can reach most other honest users within a known time.

**Timing, for safety.** Safety needs *weak synchrony*: the network may be "entirely controlled by the adversary" for "a long but bounded period of time", a day or a week in the paper's examples, and must then be strongly synchronous again for a period of hours. This is a stronger assumption than protocols such as PBFT and [HotStuff](/wiki/economics/defi/consensus/hotstuff) make. Those stay safe however long the network misbehaves.

Clocks are assumed to be loosely synchronized.

## Final and tentative blocks

The abstract's claim is that "users never have divergent views of confirmed transactions". The word *confirmed* carries a condition. The paper's agreement protocol, which it names BA⋆ (BA for Byzantine agreement), ends each round in one of two states:

- **Final consensus.** Any other user who reaches consensus in that round reached it on the same block. Transactions in the block are confirmed.
- **Tentative consensus.** Other users may have reached tentative consensus on a different block. Transactions are confirmed only when a later block reaches final consensus.

While the network is only weakly synchronous, the paper says BA⋆ "can reach tentative consensus on two different blocks, forming multiple forks", and the protocol then runs a further agreement on which fork to continue. Forks of tentative blocks are possible. Forks of final blocks are what the design rules out.

BA⋆ as published has a different step structure and different parameters from the deployed protocol: 26 expected proposers, and committees of 2,000 and 10,000. The table above describes the deployed protocol.

## Speed

The paper's prototype, run on 1,000 virtual machines simulating up to 500,000 users, confirmed "transactions in under a minute". That is a 2017 measurement of a research prototype. For the network today, the developer documentation equates 500 rounds with "about 24 minutes", which is a little under three seconds a round.

## Taking part

An account takes part by registering a *participation key*, valid for a range of rounds and separate from the key that spends its funds. Messages in each round are signed with a one-round key that is deleted afterwards, so a compromised node does not expose the account's money.

Since version 4.0 of the node software, the proposer of each block is paid: half of the block's fees, plus a bonus. To be eligible an account pays a 2 Algo fee when it registers and keeps a balance between 30,000 and 70 million Algo. Committee voters are not paid.

The penalty the documentation describes is suspension. An account expected to propose once every *n* rounds, where *n* is the total online stake divided by its own, is suspended from consensus if it produces no block in 20*n* rounds.

## Sources

- Gilad, Hemo, Micali, Vlachos & Zeldovich, [Algorand: Scaling Byzantine Agreements for Cryptocurrencies](https://eprint.iacr.org/2017/454) (2017)
- Algorand, [go-algorand `config/consensus.go`](https://github.com/algorand/go-algorand/blob/master/config/consensus.go), the reference implementation's consensus parameters, read 10 October 2026
- Algorand Developer Portal, [Protocol overview](https://dev.algorand.co/concepts/protocol/overview/), [Staking rewards](https://dev.algorand.co/concepts/protocol/staking-rewards/) and [Registration](https://dev.algorand.co/concepts/protocol/registration/), read 10 October 2026
