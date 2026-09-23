---
title: "Oracles"
weight: 50
bookCollapseSection: true
---

A smart contract cannot see outside its own chain, and it cannot wake itself up. Both gaps have to be filled from outside, and this section is the machinery that fills them.

An [oracle node](/wiki/economics/defi/oracles/oracle-node) brings external data in — a price, a settlement, a sensor reading — as a transaction the contract can read. [Chainlink](/wiki/economics/defi/oracles/chainlink) is the dominant network for doing so; its section here covers Automation, the part of the network that calls a contract on a schedule or when a condition holds, and how a contract verifies that the call came from it. A [staked consensus oracle](/wiki/economics/defi/oracles/staked-consensus-oracle) is the design pattern that makes a reported value expensive to lie about: operators post collateral and lose it when their report disagrees with the consensus. [Oracle-free pricing](/wiki/economics/defi/oracles/oracle-free-pricing) sidesteps the whole category by reading price off the geometry of an on-chain position instead.

For the waking-up problem, a [decentralized keeper](/wiki/economics/defi/oracles/decentralized-keeper) runs the cron jobs of DeFi — liquidations, settlements, feed updates — and Chainlink Automation is one implementation of the same idea.

## Wiki Pages

{{< section >}}
