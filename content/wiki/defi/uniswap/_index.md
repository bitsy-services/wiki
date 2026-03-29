---
title: "Uniswap"
weight: 2
bookCollapseSection: true
---

Uniswap lets you swap one [ERC-20](https://en.wikipedia.org/wiki/ERC-20) token for another directly on-chain, without an order book or counterparty. Instead of matching buyers and sellers, it uses [liquidity pools](https://en.wikipedia.org/wiki/Constant_function_market_maker) — smart contracts that hold reserves of two tokens and price swaps algorithmically. Anyone can trade against a pool, and anyone can deposit tokens into one to earn fees.

It is the dominant [decentralized exchange](https://en.wikipedia.org/wiki/Decentralized_exchange) on [Ethereum](https://en.wikipedia.org/wiki/Ethereum) and most [L2s](https://en.wikipedia.org/wiki/Blockchain_scaling#Layer_2), handling billions of dollars in daily volume.

## Protocol Versions

Uniswap has gone through several major versions. Each is a separate set of smart contracts — older versions remain deployed and functional.

**V2** introduced the core AMM model: every pool holds a 50/50 reserve of two tokens, priced along a constant-product curve (`x * y = k`). Simple and battle-tested, but capital-inefficient — liquidity is spread evenly across all possible prices, so most of it sits idle.

**V3** added [concentrated liquidity](https://docs.uniswap.org/concepts/protocol/concentrated-liquidity). Liquidity providers choose a price range for their capital, so the same dollar amount can generate far more trading depth where it matters. V3 also introduced multiple [fee tiers](https://docs.uniswap.org/concepts/protocol/fees#fee-tiers) per pair (0.01%, 0.05%, 0.3%, 1%). This is the most widely integrated version today.

**V4** moves all pools into a single "singleton" contract for gas savings and introduces [hooks](https://docs.uniswap.org/contracts/v4/overview) — plugin contracts that can customize pool behavior (dynamic fees, on-chain limit orders, custom oracles, etc.). V4 is newer and has less tooling and documentation than V3.

**UniswapX** is a separate [intent-based](https://docs.uniswap.org/contracts/uniswapx/overview) system that runs alongside the on-chain protocol. Users sign an order off-chain, and competing "fillers" find the best execution — potentially routing across multiple DEXs or using private liquidity. On-chain settlement acts as a fallback.

## Swap Routers

When integrating Uniswap programmatically, you interact with a **router contract** that handles token transfers, pool selection, and multi-hop paths. There are three routers, each supporting different protocol versions:

| Router | Protocols | Best For |
|---|---|---|
| **UniversalRouter** | V2 + V3 + V4 | **New integrations** — best gas efficiency, uses [Permit2](https://docs.uniswap.org/contracts/permit2/overview) for signature-based approvals |
| **SwapRouter02** | V2 + V3 | Simpler Solidity interface when you don't need Permit2 or V4 |
| **SwapRouter** (V3) | V3 only | Simplest interface — good for learning; covered in the [ISwapRouter guide](iswap-router) |

For a detailed comparison of all three (approval flows, gas costs, when to use each), see [SwapRouter vs SwapRouter02 vs UniversalRouter](swap-routers).

For deployment addresses across all supported chains, see the [official Uniswap deployment list](https://docs.uniswap.org/contracts/v3/reference/deployments/).

## Key Infrastructure

These contracts support the routers above. You don't swap through them directly, but you'll encounter them in most integrations:

- **[Permit2](https://docs.uniswap.org/contracts/permit2/overview)** — a shared approval contract. Instead of granting each router a separate ERC-20 allowance (an on-chain transaction), you approve Permit2 once per token, then sign off-chain permits for each swap. This saves gas and means you don't need new approvals when Uniswap deploys new router versions.
- **QuoterV2** — simulates a swap off-chain (via `eth_call`) and returns the expected output amount. Use this to calculate a safe `amountOutMinimum` for [slippage](https://en.wikipedia.org/wiki/Slippage_(finance)) protection before submitting a real swap.

## Wiki Pages

{{< section >}}
