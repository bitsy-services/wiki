---
title: "Solidity Patterns"
weight: 5
bookCollapseSection: true
---

Reusable patterns, best practices, and how-to guides for [Solidity](https://en.wikipedia.org/wiki/Solidity) -- the language most [smart contracts](/wiki/economics/finance/defi/smart-contract) on [Ethereum](/wiki/economics/finance/defi/ethereum) and other [EVM](/wiki/economics/finance/defi/ethereum#the-ethereum-virtual-machine-evm) chains are written in. The code on these pages is meant to be copy-pasted, so it is written to be correct rather than short.

[Clones with immutable args](/wiki/economics/finance/defi/solidity/clones-with-immutable-args) is the deployment pattern: a minimal proxy that carries per-instance configuration in its own bytecode, giving you cheap deploys without the storage reads a conventional clone pays on every call. It is what makes a [permissionless token factory](/wiki/economics/finance/defi/permissionless-token-factory) affordable.

The other two cover the toolchain. [Foundry](/wiki/economics/finance/defi/solidity/foundry) is the Rust-based kit -- `forge` to build and test, `cast` to poke at contracts, `anvil` for a local node -- and the default for new work here. [Foundry broadcast](/wiki/economics/finance/defi/solidity/foundry-broadcast) covers the part that surprises people: everything between `startBroadcast` and `stopBroadcast` is *not* one atomic transaction, and assuming otherwise produces deploy scripts that half-succeed.

## Wiki Pages

{{< section >}}
