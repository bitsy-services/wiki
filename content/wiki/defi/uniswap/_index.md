---
title: "Uniswap"
weight: 2
bookCollapseSection: true
---

Uniswap is the dominant on-chain [DEX](https://en.wikipedia.org/wiki/Decentralized_exchange) protocol on Ethereum and most [EVM](https://en.wikipedia.org/wiki/Ethereum#Virtual_machine) [L2s](https://en.wikipedia.org/wiki/Blockchain_scaling#Layer_2). It uses [concentrated-liquidity](https://docs.uniswap.org/concepts/protocol/concentrated-liquidity) [AMM](https://en.wikipedia.org/wiki/Constant_function_market_maker) pools (V3) and an [intent-based architecture](https://docs.uniswap.org/contracts/uniswapx/overview) (V4 / UniswapX) for token swaps.

## Current Contracts

| Contract | Purpose | When to Use |
|---|---|---|
| **UniversalRouter** | Unified entry point for V2, V3, and V4 swaps with Permit2 approvals | New integrations — best gas efficiency and approval UX |
| **SwapRouter02** | Combined V2 + V3 routing | Simpler alternative if you only need swap routing without Permit2 |
| **SwapRouter** (V3) | Original V3-only swap router | Legacy integrations; covered in [ISwapRouter guide](iswap-router.md) |

For deployment addresses across all supported chains, see the [official Uniswap deployment list](https://docs.uniswap.org/contracts/v3/reference/deployments/).

## Key Supporting Services

- **Permit2** — token approval manager shared across Uniswap contracts. Replaces per-contract `approve` calls with signature-based permits. [Docs](https://docs.uniswap.org/contracts/permit2/overview)
- **QuoterV2** — simulates swaps off-chain to get expected output amounts for slippage calculations.
- **UniswapX** — off-chain order system where fillers compete to give users the best price, with on-chain settlement as fallback. [Docs](https://docs.uniswap.org/contracts/uniswapx/overview)
- **V4 Hooks** — Uniswap V4 introduces customizable pool logic via hook contracts. [Docs](https://docs.uniswap.org/contracts/v4/overview)

## Wiki Pages

{{< section >}}
