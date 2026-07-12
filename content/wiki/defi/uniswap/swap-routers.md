---
title: "SwapRouter vs SwapRouter02 vs UniversalRouter"
weight: 2
---

Uniswap has shipped three generations of swap routers. Each builds on the last, adding protocol support and improving gas efficiency and approval UX. This page compares all three to help you choose the right one.

## At a Glance

| | **SwapRouter** | **SwapRouter02** | **UniversalRouter** |
|---|---|---|---|
| Protocols | V3 only | V2 + V3 | V2 + V3 + V4 + NFTs |
| Approval model | Per-token `approve` | Per-token `approve` | [Permit2](https://docs.uniswap.org/contracts/permit2/overview) signatures |
| Multi-call batching | No | `multicall()` | Command-based execution |
| ETH handling | Manual wrap/unwrap | Built-in wrap/unwrap | Built-in wrap/unwrap |
| Gas efficiency | Baseline | Moderate improvement | Best (single `transferFrom` per token) |
| Interface | `ISwapRouter` | `ISwapRouter02` | Encoded command bytes |
| Status | Legacy — widely deployed | Production — simpler integration | **Recommended** for new projects |

## SwapRouter (V3)

The original V3 swap router. It exposes a clean Solidity interface (`ISwapRouter`) with four functions: `exactInputSingle`, `exactInput`, `exactOutputSingle`, and `exactOutput`. See the [ISwapRouter guide](/wiki/defi/uniswap/iswap-router) for full details.

**Strengths:**
- Simplest to understand and integrate
- Battle-tested since V3 launch (May 2021)
- Extensive documentation and examples

**Limitations:**
- V3 pools only — no V2 fallback
- Requires a separate `approve` tx per token per contract
- No native ETH support — you must wrap/unwrap [WETH](https://en.wikipedia.org/wiki/Wrapped_tokens) manually
- No batching — each swap is a separate call

**Canonical address (most chains):** `0xE592427A0AEce92De3Edee1F18E0157C05861564`

## SwapRouter02

Combines V2 and V3 routing into a single contract. Adds `multicall()` for batching and built-in ETH wrapping.

**Strengths:**
- Routes through both V2 and V3 pools — finds better prices when V2 has deeper liquidity for a pair
- `multicall()` lets you batch multiple swaps or swap + unwrap in a single tx
- Built-in `unwrapWETH9` and `refundETH` convenience functions
- Familiar Solidity interface — similar parameter structs to SwapRouter

**Limitations:**
- Still uses the traditional `approve` model — users must send a separate approval tx per token
- No V4 pool support
- No command-based flexibility — you're limited to the functions the contract exposes

**Canonical address (Ethereum mainnet):** `0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45`

## UniversalRouter

The current recommended entry point. Uses a command-based architecture where you encode an array of commands (bytes) and inputs, then call `execute()`. Integrates with [Permit2](https://docs.uniswap.org/contracts/permit2/overview) for gasless, signature-based approvals.

**Strengths:**
- Supports V2, V3, V4, and NFT purchases in a single transaction
- [Permit2](https://docs.uniswap.org/contracts/permit2/overview) approvals — users approve the Permit2 contract once, then sign off-chain permits per swap (no per-router approval tx)
- Best gas efficiency — batches multiple operations, uses a single `transferFrom` per token
- Flexible command system — compose arbitrary sequences of swaps, wraps, transfers, and permits
- `SWEEP` and `PAY_PORTION` commands enable fee collection and token distribution without wrapper contracts

**Limitations:**
- Steeper learning curve — no human-readable function signatures; you encode commands as byte arrays
- Debugging is harder — reverts surface as command indices rather than named function errors
- Requires understanding the Permit2 flow (approve Permit2 once, then sign typed-data permits)
- Fewer Solidity examples in the wild compared to SwapRouter

**Canonical address (Ethereum mainnet):** `0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD`

## Approval Flow Comparison

### SwapRouter / SwapRouter02

```text
User → approve(router, amount) → ERC-20 token   [on-chain tx per token]
User → swap(...)               → Router          [on-chain tx]
```

Each new router contract requires a fresh approval. If you switch routers, users pay for new approval transactions.

### UniversalRouter + Permit2

```text
User → approve(permit2, type(uint256).max) → ERC-20 token   [one-time on-chain tx per token]
User → sign EIP-712 permit                                   [off-chain, free]
User → execute(commands, inputs)           → UniversalRouter [on-chain tx with permit bundled]
```

Users approve [Permit2](https://docs.uniswap.org/contracts/permit2/overview) once per token. After that, each swap only needs an off-chain signature — no extra approval transactions even when Uniswap deploys new router versions.

## Which Should You Use?

| Scenario | Router |
|---|---|
| **New integration, any protocol version** | UniversalRouter — best gas, best UX, future-proof |
| **Simple V2 + V3 swap, want a Solidity interface** | SwapRouter02 — easier to read and debug than UniversalRouter |
| **Learning Uniswap V3 mechanics** | SwapRouter — simplest interface, most examples |
| **Maintaining existing integration** | Keep what works — no need to migrate unless you need new features |
| **On-chain contract calling a router** | SwapRouter or SwapRouter02 — the typed Solidity interfaces are easier to compose in contracts than encoding UniversalRouter commands |

## Further Reading

- [UniversalRouter Overview](https://docs.uniswap.org/contracts/universal-router/overview)
- [Permit2 Overview](https://docs.uniswap.org/contracts/permit2/overview)
- [SwapRouter02 Source](https://github.com/Uniswap/swap-router-contracts)
- [ISwapRouter Guide](/wiki/defi/uniswap/iswap-router) — detailed walkthrough of the original V3 router
- [Uniswap Deployment Addresses](https://docs.uniswap.org/contracts/v3/reference/deployments/)
