---
title: "Avalanche Consensus"
weight: 110
---

Avalanche consensus is a family of protocols in which a node reaches a decision by polling. Faced with two conflicting options, the node repeatedly asks a small random sample of the other validators which one they prefer, adopts the answer when a large enough majority of the sample agrees, and treats the matter as decided once the same answer has come back enough times in a row. There is no leader, and no step in which every validator hears from every other.

The guarantee is probabilistic by design. The parameters are chosen so that the chance of two honest nodes deciding differently is below a chosen bound ε. This differs from protocols descended from [PBFT](/wiki/economics/defi/consensus/pbft), where agreement is certain as long as fewer than a third of the participants are faulty, and resembles Bitcoin, where a reversal becomes vanishingly unlikely without ever being impossible.

The design was posted in 2018 under the pseudonym Team Rocket and later published with Yin, Sekniqi, van Renesse and Sirer. Its abstract calls the protocols "leaderless", "built around a metastable mechanism via network subsampling". The Avalanche network runs a version for linear chains called Snowman.

## Three parameters

| Parameter | Meaning |
|---|---|
| *k* | how many validators a node samples in each poll |
| α | how many of the *k* must give the same answer for the poll to count |
| β | how many consecutive successful polls it takes to decide |

## Built up in four steps

The paper develops the protocol in stages, each adding one piece of memory to the node. The options are called colours.

**Slush.** A node with no colour adopts the first one it hears about. In each round it samples *k* nodes, and if at least α of them report the same colour, it switches to that colour. After a fixed number of rounds it stops. Slush tolerates crashes only. It "is not tolerant to Byzantine faults", meaning faults in which a node lies.

**Snowflake.** The node keeps a counter of consecutive successful polls for its current colour. A poll for a different colour resets the counter. When the counter reaches β, the node decides.

**Snowball.** The node also keeps a running total, per colour, of every successful poll for that colour. It changes its preference only when another colour's total overtakes its current one, so a brief run of adversarial answers no longer flips it. The decision still takes β consecutive successes.

**Avalanche.** Many Snowball decisions run at once over a [directed acyclic graph](/wiki/cs/dag) (DAG) of transactions in which each transaction references earlier ones, so that one poll serves as a vote on a transaction and on everything it builds on.

The word *metastable* describes why sampling converges. A network split evenly between two colours is balanced only as a pencil standing on its point is balanced. Random samples push a few nodes one way, which makes that colour slightly more likely to turn up in the next sample, which converts more nodes. The paper's claim is that the mechanism "can move a large network to an irreversible state quickly".

## What is guaranteed

**Safety, with probability.** "When decisions are made by any two correct nodes, they decide on conflicting transactions with negligible probability (≤ ε)."

**No fixed fault threshold.** The parameters are set for an expected number of Byzantine nodes, and the paper does not give one tolerated fraction. It says that where quorum-based safety "breaks down immediately when the predetermined threshold f is exceeded, Snow's probabilistic safety guarantee degrades smoothly", and that the family "can be parameterized to tolerate more than a third of the Byzantine nodes by trading off liveness."

**Progress, under conditions.** The paper states that "our protocols are synchronous in order to guarantee liveness". Fast termination is shown for a number of Byzantine nodes on the order of the square root of the network's size.

**Progress only for honest transactions.** In the DAG protocol a transaction that conflicts with another may never be decided. An honest user does not issue conflicting transactions, so the paper's position is that only a double-spender's own transactions can stall: "liveness is not guaranteed for rogue transactions".

Who may be sampled is a separate question from how they agree, the question of [Sybil resistance](/wiki/economics/defi/sybil-resistance). The paper leaves it open, noting that the protocols "can adopt any Sybil control mechanism, although proof-of-stake is most aligned with their quiescent operation."

## Measurements in the paper

The headline figures come from a research prototype. With 2,000 nodes spread over 20 emulated cities, it averaged 3,401 transactions per second (TPS) with a median latency of 1.35 seconds and a maximum of 4.25 seconds. Without the emulated distances, throughput was about 7,000. Those runs used *k* = 10, which is not what the network uses today.

## On the Avalanche network

The node software, AvalancheGo, ships with these defaults:

| Parameter | Flag | Default |
|---|---|---|
| *k* | `--snow-sample-size` | 20 |
| α | `--snow-quorum-size` | 15 |
| β | `--snow-commit-threshold` | 20 |

A node therefore needs 15 of 20 sampled validators to agree, 20 polls in a row.

All three chains of Avalanche's primary network run **Snowman**, which decides on blocks in a single chain. Snowman is not in the paper. One of the three, the X-Chain, ran the DAG protocol until the Cortina upgrade on 25 April 2023. The DAG code has since been removed from the software.

Snowman lets any validator propose a block, which wastes effort when many propose at once. An added layer, Snowman++, "attempts to select a single proposer with the power to issue a block, but opens up block production to every validator if sufficient time has passed without blocks being generated."

Validators are admitted by [stake](/wiki/economics/defi/sybil-resistance/proof-of-stake). In October 2026:

- the minimum stake to validate was 2,000 AVAX;
- the minimum period was 48 hours, cut from two weeks by the Helicon upgrade of 22 September 2026;
- stake was never slashed. The documentation says Avalanche "does not take away any portion of a validator's already staked tokens". A validator that is not "online and responsive for at least 90% of their validation period" gets no reward.

## Sources

- Team Rocket, Yin, Sekniqi, van Renesse & Sirer, [Scalable and Probabilistic Leaderless BFT Consensus through Metastability](https://arxiv.org/abs/1906.08936) (version 2, 2020)
- AvalancheGo, [configuration reference](https://github.com/ava-labs/avalanchego/blob/master/config/config.md), [release notes](https://github.com/ava-labs/avalanchego/blob/master/RELEASES.md), [`snow/README.md`](https://github.com/ava-labs/avalanchego/blob/master/snow/README.md) and [`vms/proposervm/README.md`](https://github.com/ava-labs/avalanchego/blob/master/vms/proposervm/README.md), read 10 October 2026
- Avalanche documentation, [How to stake](https://build.avax.network/docs/primary-network/validate/how-to-stake) and [AVAX token](https://build.avax.network/docs/primary-network/avax-token), read 10 October 2026
