---
title: "Chainlink"
weight: 10
bookCollapseSection: true
---

[Chainlink](https://en.wikipedia.org/wiki/Chainlink_(blockchain)) is a decentralized [oracle](/wiki/economics/defi/oracle-node) network that connects [smart contracts](/wiki/economics/defi/smart-contract) to real-world data, off-chain computation, and cross-chain services. It is the dominant answer to the problem that a contract cannot see anything outside its own chain.

These pages cover the half of Chainlink that solves the *other* gap: a contract also cannot wake itself up. **Chainlink Automation** is the managed [keeper](/wiki/economics/defi/decentralized-keeper) network that calls your functions on a schedule or when a condition you define becomes true, so you do not have to run bot infrastructure yourself.

## The pages, in order

Start with [Automation](/wiki/economics/defi/chainlink/automation) for what the service does and when it is worth using. The next three follow one upkeep through its life: [registration](/wiki/economics/defi/chainlink/registration) is how you create one and fund it with LINK, the [registrar](/wiki/economics/defi/chainlink/registrar) is the contract that accepts that request, and the [registry](/wiki/economics/defi/chainlink/registry) is where the upkeep lives and gets executed from for the rest of its life.

The last two are about the call arriving at your contract. The [forwarder](/wiki/economics/defi/chainlink/forwarder) is a per-upkeep proxy that gives you a stable, predictable `msg.sender` to check against. [Securing `performUpkeep`](/wiki/economics/defi/chainlink/securing-performupkeep) is why you must check it: the function is external, anyone can call it, and if it moves funds or changes critical state an unguarded implementation is an open door.

## Wiki Pages

{{< section >}}
