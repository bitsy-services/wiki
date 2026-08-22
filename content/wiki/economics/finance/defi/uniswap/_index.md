---
title: "Uniswap"
weight: 2
bookCollapseSection: true
---

Uniswap lets you swap one [ERC-20](https://en.wikipedia.org/wiki/ERC-20) token for another directly on-chain, without an order book or counterparty. Instead of matching buyers and sellers, it uses [liquidity pools](https://en.wikipedia.org/wiki/Constant_function_market_maker) — smart contracts that hold reserves of two tokens and price swaps algorithmically. Anyone can trade against a pool, and anyone can deposit tokens into one to earn fees.

It is the dominant [decentralized exchange](https://en.wikipedia.org/wiki/Decentralized_exchange) on [Ethereum](https://en.wikipedia.org/wiki/Ethereum) and most [L2s](https://en.wikipedia.org/wiki/Blockchain_scaling#Layer_2), handling billions of dollars in daily volume.

## Protocol Versions

Uniswap has gone through several major versions. Each is a separate set of smart contracts — older versions remain deployed and functional.

**V2** introduced the core [AMM](/wiki/economics/finance/defi/amm) model: every pool holds a 50/50 reserve of two tokens, priced along a constant-product curve (`x * y = k`). Simple and battle-tested, but capital-inefficient — liquidity is spread evenly across all possible prices, so most of it sits idle.

**V3** added [concentrated liquidity](https://docs.uniswap.org/concepts/protocol/concentrated-liquidity). Liquidity providers choose a price range for their capital, so the same dollar amount can generate far more trading depth where it matters. V3 also introduced multiple [fee tiers](https://docs.uniswap.org/concepts/protocol/fees#fee-tiers) per pair (0.01%, 0.05%, 0.3%, 1%). This is the most widely integrated version today.

**V4** moves all pools into a single "singleton" contract for gas savings and introduces [hooks](https://docs.uniswap.org/contracts/v4/overview) — plugin contracts that can customize pool behavior (dynamic fees, on-chain limit orders, custom oracles, etc.). V4 is newer and has less tooling and documentation than V3.

**UniswapX** is a separate [intent-based](https://docs.uniswap.org/contracts/uniswapx/overview) system that runs alongside the on-chain protocol. Users sign an order off-chain, and competing "fillers" find the best execution — potentially routing across multiple [DEXs](/wiki/economics/finance/defi/dex) or using private liquidity. On-chain settlement acts as a fallback.

## Which Version Should I Use?

There are two decisions: which **pool version** your swaps route through, and which **router contract** you call. In practice, the router decides for you — modern routers can route through multiple pool versions in a single transaction.

### Choosing a pool version

You rarely need to pick this explicitly. The router (or the Uniswap frontend) will find the pool with the best price for your pair. But it helps to understand the trade-offs:

| | V2 | V3 | V4 |
|---|---|---|---|
| Liquidity model | Full-range (simple, passive) | Concentrated (more efficient, active management) | Concentrated + hooks |
| Maturity | Oldest, most forked | Most liquidity, most integrations | Newest, least tooling |
| When you'd target it directly | Pair only has a V2 pool; or you want the simplest on-chain integration | Default choice — deepest liquidity for most pairs | You need custom pool logic (dynamic fees, on-chain limit orders) |

**If you're unsure, target V3.** It has the deepest liquidity for nearly all major pairs and the most documentation.

### Choosing a router

This is the more consequential decision. It determines your approval flow, your Solidity interface, and which pool versions you can reach:

| Scenario | Use | Why |
|---|---|---|
| **New project, swaps initiated by an externally owned account (EOA)** | **UniversalRouter** | Best gas, Permit2 approvals, routes through V2 + V3 + V4 |
| **Contract-to-contract swap, want typed Solidity** | **SwapRouter02** | Clean function signatures, easier to compose and debug from Solidity |
| **Learning / prototyping** | **SwapRouter** (V3) | Simplest interface, most tutorials and examples; see the [ISwapRouter guide](iswap-router) |
| **Existing integration that works** | Keep what you have | No need to migrate unless you need V4 or Permit2 |

The UniversalRouter uses encoded command bytes instead of named functions, which makes it harder to read and debug in Solidity — that's why on-chain contracts often prefer SwapRouter02 even though UniversalRouter is technically superior.

For a full comparison (approval flows, gas costs, code examples), see [SwapRouter vs SwapRouter02 vs UniversalRouter](swap-routers).

For deployment addresses across all supported chains, see the [official Uniswap deployment list](https://docs.uniswap.org/contracts/v3/reference/deployments/).

## Key Infrastructure

These contracts support the routers above. You don't swap through them directly, but you'll encounter them in most integrations:

- **[Permit2](https://docs.uniswap.org/contracts/permit2/overview)** — a shared approval contract. Instead of granting each router a separate ERC-20 allowance (an on-chain transaction), you approve Permit2 once per token, then sign off-chain permits for each swap. This saves gas and means you don't need new approvals when Uniswap deploys new router versions.
- **QuoterV2** — simulates a swap off-chain (via `eth_call`) and returns the expected output amount. Use this to calculate a safe `amountOutMinimum` for [slippage](https://en.wikipedia.org/wiki/Slippage_(finance)) protection before submitting a real swap.

## Source Code

| Repository | Contains |
|---|---|
| [v2-periphery](https://github.com/Uniswap/v2-periphery) | `IUniswapV2Router02` — the V2 router interface |
| [v3-periphery](https://github.com/Uniswap/v3-periphery) | `ISwapRouter`, `IQuoterV2`, and other V3 periphery interfaces |
| [swap-router-contracts](https://github.com/Uniswap/swap-router-contracts) | `ISwapRouter02` — the combined V2 + V3 router |
| [universal-router](https://github.com/Uniswap/universal-router) | UniversalRouter — command-based, no typed Solidity interface |
| [permit2](https://github.com/Uniswap/permit2) | Permit2 signature-based approval system |
| [v4-core](https://github.com/Uniswap/v4-core) | V4 singleton pool contract and hook interfaces |
| [v4-periphery](https://github.com/Uniswap/v4-periphery) | V4 routing and position management |

## Pages in This Section

[Swap routers](/wiki/economics/finance/defi/uniswap/swap-routers) compares the three generations of router and helps you pick one; [ISwapRouter](/wiki/economics/finance/defi/uniswap/iswap-router) is the V3 interface in detail. [Ticks](/wiki/economics/finance/defi/uniswap/ticks) explains the integer price grid that concentrated liquidity is defined against, and [single-tick liquidity](/wiki/economics/finance/defi/uniswap/single-tick-liquidity) is the narrowest case the protocol allows -- a position one tick wide, which stops behaving like a curve and starts behaving like a fixed-price order. [Fee distribution](/wiki/economics/finance/defi/uniswap/fee-distribution) covers how earnings reach a liquidity provider without any code path ever iterating over LPs: a pull-based accumulator that keeps both swaps and claims O(1), and that positions have to be *poked* to realise.

## Wiki Pages

{{< section >}}
