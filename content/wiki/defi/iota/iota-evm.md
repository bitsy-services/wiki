---
title: "IOTA EVM"
weight: 3
---

IOTA EVM is IOTA's fully [Ethereum](/wiki/defi/ethereum/)-compatible smart-contract chain. It is the practical entry point for [DeFi](/wiki/defi/dex) on IOTA: existing [Solidity](/wiki/defi/solidity/) contracts, [ERC-20](/wiki/defi/ethereum/erc-20) tooling, MetaMask, Hardhat, and Foundry all work unmodified, with configuration changes only. It launched on mainnet in 2024 and continues to run as a Layer 2 alongside the [Move](/wiki/defi/iota/iota-rebased) Layer 1 introduced by the [Rebased](/wiki/defi/iota/iota-rebased) upgrade.

## Architecture

IOTA EVM is one chain produced by **IOTA Smart Contracts (ISC)**, the framework that runs sandboxed contract chains and anchors their state to IOTA Layer 1. From a developer's point of view it is an ordinary EVM chain; the ISC layer underneath handles settlement to L1 and asset movement. The native [IOTA token](/wiki/defi/cryptocurrency) is the gas currency, and a bridge moves value between L1 native assets and L2 EVM balances.

A consequence worth noting: IOTA EVM is *not* the Move L1 environment. Building L1-native applications means writing Move modules against the object ledger; IOTA EVM is the compatibility surface for porting Ethereum-ecosystem code. The Foundation has stated it intends to integrate EVM execution into Layer 1 directly, but as of mid-2026 that is still on the roadmap — the L2 chain described here remains the way to run Solidity on IOTA.

## Network Parameters

Mainnet connection details:

```text
Network name:  IOTA EVM
Chain ID:      8822
RPC URL:       https://json-rpc.evm.iotaledger.net
WebSocket:     wss://ws.json-rpc.evm.iotaledger.net
Currency:      IOTA
Explorer:      https://explorer.evm.iota.org
```

Adding the network to MetaMask or a wallet config is the only chain-specific step; the JSON-RPC surface is standard, so an existing deployment script just needs the new endpoint and chain ID:

```javascript
// hardhat.config.js
module.exports = {
  networks: {
    iotaEvm: {
      url: "https://json-rpc.evm.iotaledger.net",
      chainId: 8822,
      accounts: [process.env.DEPLOYER_KEY],
    },
  },
};
```

## DeFi on IOTA EVM

IOTA's stated focus is real-world assets, tokenisation, and machine payments rather than purely speculative on-chain finance, but the EVM chain hosts the usual DeFi building blocks — [DEXs](/wiki/defi/dex), lending markets, and bridges — because they port directly from Ethereum. The Foundation also highlights design choices intended to reduce some [maximal extractable value](/wiki/defi/maximal-extractable-value); as with any such claim, treat it as a design goal to verify against the live ordering behaviour, not a guarantee.

Because L1 gas is minimal and can be sponsored, a common pattern is to build user-facing [dApps](/wiki/defi/dapp) that abstract gas away entirely — the application pays, the user transacts as if the network were feeless.

## External Links

- [IOTA EVM product page](https://www.iota.org/products/evm)
- [IOTA EVM Mainnet launch announcement](https://blog.iota.org/iotas-evm-mainnet-launch/)
- [IOTA Smart Contracts documentation](https://docs.iota.org/developer/iota-evm/getting-started/tools)
- [Chainlist entry for chain 8822](https://chainlist.org/chain/8822) — canonical RPC list
