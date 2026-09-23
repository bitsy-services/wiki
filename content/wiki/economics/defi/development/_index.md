---
title: "Development"
weight: 80
bookCollapseSection: true
---

Building a contract and reading the results back out. [Solidity patterns](/wiki/economics/defi/development/solidity) covers the language most contracts on Ethereum-compatible chains are written in and the Foundry toolchain used to write, test and deploy them. [The Graph](/wiki/economics/defi/development/the-graph) covers the other direction — indexing chain events into something a front end can query, by publishing a schema and the mapping code that fills it. [Groth16](/wiki/economics/defi/development/groth16) is a [zero-knowledge proof](/wiki/cs/zero-knowledge-proofs) system — the most widely deployed one — and shows up whenever a contract needs to verify a computation it cannot afford to re-run.

Shipping a token does not end at deployment. Getting its icon and metadata onto wallets, explorers and aggregators is [Token registration](/wiki/economics/defi/token-registration), and keeping the same companies' scanners from flagging it is [Token false alarms](/wiki/economics/defi/token-false-alarms); both are sections of their own, one level up.

## Wiki Pages

{{< section >}}
