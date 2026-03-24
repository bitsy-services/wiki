---
title: "ISwapRouter"
weight: 1
---

# ISwapRouter — Uniswap V3 Swap Guide

`ISwapRouter` is the interface your contract (or off-chain script) calls to execute token swaps through Uniswap V3 pools. It lives at:

```
@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol
```

The canonical deployment is the **SwapRouter** contract. On most chains the address is `0xE592427A0AEce92De3Edee1F18E0157C05861564`.

## Installation

```bash
# Foundry
forge install Uniswap/v3-periphery

# Hardhat / npm
npm install @uniswap/v3-periphery @uniswap/v3-core
```

In Foundry add the remapping:

```
@uniswap/v3-periphery/=lib/v3-periphery/
@uniswap/v3-core/=lib/v3-core/
```

## Interface Overview

`ISwapRouter` exposes four functions:

| Function | Use Case |
|---|---|
| `exactInputSingle` | Swap a fixed amount of **one token** for as much as possible of another (single pool). |
| `exactInput` | Same idea but across a **multi-hop path** (two or more pools). |
| `exactOutputSingle` | Receive an exact amount of the output token, spending as little as possible (single pool). |
| `exactOutput` | Exact-output across a multi-hop path. |

All four accept a struct of parameters and return the resulting amount.

## Exact-Input Single Swap

The simplest case: swap a known amount of token A for token B through one pool.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {ISwapRouter} from "@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract SimpleSwap {
    ISwapRouter public immutable router;

    constructor(address _router) {
        router = ISwapRouter(_router);
    }

    /// @notice Swap `amountIn` of tokenIn for tokenOut.
    /// @param tokenIn  Address of the token to sell.
    /// @param tokenOut Address of the token to buy.
    /// @param fee      Pool fee tier (500, 3000, or 10000).
    /// @param amountIn Amount of tokenIn to spend.
    /// @param amountOutMinimum Minimum acceptable output (slippage protection).
    /// @return amountOut Actual amount of tokenOut received.
    function swapExactInput(
        address tokenIn,
        address tokenOut,
        uint24 fee,
        uint256 amountIn,
        uint256 amountOutMinimum
    ) external returns (uint256 amountOut) {
        // Transfer tokens in and approve the router.
        IERC20(tokenIn).transferFrom(msg.sender, address(this), amountIn);
        IERC20(tokenIn).approve(address(router), amountIn);

        ISwapRouter.ExactInputSingleParams memory params = ISwapRouter
            .ExactInputSingleParams({
                tokenIn: tokenIn,
                tokenOut: tokenOut,
                fee: fee,
                recipient: msg.sender,
                deadline: block.timestamp,
                amountIn: amountIn,
                amountOutMinimum: amountOutMinimum,
                sqrtPriceLimitX96: 0 // no price limit
            });

        amountOut = router.exactInputSingle(params);
    }
}
```

### Parameter Breakdown

| Parameter | Notes |
|---|---|
| `tokenIn` / `tokenOut` | ERC-20 addresses. Order matters — it determines swap direction. |
| `fee` | Identifies which pool to use. Common tiers: **500** (0.05 %), **3000** (0.3 %), **10000** (1 %). |
| `recipient` | Where the output tokens are sent. |
| `deadline` | Unix timestamp after which the tx reverts. Use `block.timestamp` for atomic calls; add a buffer for user-submitted txs. |
| `amountIn` | Exact number of input tokens (in the token's smallest unit). |
| `amountOutMinimum` | Slippage guard. Set to 0 only in tests — in production derive it from a quote minus your tolerance. |
| `sqrtPriceLimitX96` | Cap how far the price can move during the swap. `0` means no limit. |

## Exact-Output Single Swap

When you need **exactly N** of the output token and are willing to spend up to a maximum of the input token:

```solidity
function swapExactOutput(
    address tokenIn,
    address tokenOut,
    uint24 fee,
    uint256 amountOut,
    uint256 amountInMaximum
) external returns (uint256 amountIn) {
    IERC20(tokenIn).transferFrom(msg.sender, address(this), amountInMaximum);
    IERC20(tokenIn).approve(address(router), amountInMaximum);

    ISwapRouter.ExactOutputSingleParams memory params = ISwapRouter
        .ExactOutputSingleParams({
            tokenIn: tokenIn,
            tokenOut: tokenOut,
            fee: fee,
            recipient: msg.sender,
            deadline: block.timestamp,
            amountOut: amountOut,
            amountInMaximum: amountInMaximum,
            sqrtPriceLimitX96: 0
        });

    amountIn = router.exactOutputSingle(params);

    // Refund unspent tokens.
    if (amountIn < amountInMaximum) {
        IERC20(tokenIn).approve(address(router), 0);
        IERC20(tokenIn).transfer(msg.sender, amountInMaximum - amountIn);
    }
}
```

> **Important:** Always refund the difference. The router only pulls what it needs, but you approved and transferred `amountInMaximum`.

## Multi-Hop Swaps

For tokens that don't share a direct pool (or where routing through an intermediary gives a better price), use `exactInput` or `exactOutput` with an encoded path.

A path is a tightly packed sequence of `(token, fee, token, fee, token, …)`:

```solidity
// DAI → (0.3 % pool) → WETH → (0.05 % pool) → USDC
bytes memory path = abi.encodePacked(
    DAI,
    uint24(3000),
    WETH,
    uint24(500),
    USDC
);

ISwapRouter.ExactInputParams memory params = ISwapRouter.ExactInputParams({
    path: path,
    recipient: msg.sender,
    deadline: block.timestamp,
    amountIn: amountIn,
    amountOutMinimum: amountOutMinimum
});

uint256 amountOut = router.exactInput(params);
```

> For `exactOutput` the path is **reversed** — it starts with the output token and ends with the input token.

## Fee Tiers

Uniswap V3 pools are deployed per fee tier. Picking the right one matters for execution quality.

| Fee | Basis Points | Typical Use |
|---|---|---|
| **100** | 0.01 % | Stable-to-stable pairs (USDC/USDT). |
| **500** | 0.05 % | Correlated pairs (WETH/stETH) or high-volume majors. |
| **3000** | 0.3 % | Most standard pairs. |
| **10000** | 1 % | Exotic or low-liquidity tokens. |

If you're unsure which tier has the deepest liquidity, query the **Quoter** first.

## Getting a Quote

Use the `QuoterV2` contract (`IQuoterV2`) to simulate a swap off-chain and get the expected output. This is how you derive `amountOutMinimum`:

```solidity
import {IQuoterV2} from "@uniswap/v3-periphery/contracts/interfaces/IQuoterV2.sol";

(uint256 expectedOut, , , ) = quoter.quoteExactInputSingle(
    IQuoterV2.QuoteExactInputSingleParams({
        tokenIn: WETH,
        tokenOut: USDC,
        fee: 3000,
        amountIn: 1 ether,
        sqrtPriceLimitX96: 0
    })
);

// Apply 0.5 % slippage tolerance.
uint256 amountOutMinimum = (expectedOut * 995) / 1000;
```

> **Note:** `QuoterV2` uses `staticcall` under the hood — it reverts and decodes the revert data to return the quote. Call it off-chain (via `eth_call`) to avoid gas costs.

## Wrapping / Unwrapping ETH

The SwapRouter does **not** accept raw ETH. Wrap it first:

```solidity
IWETH9 weth = IWETH9(router.WETH9());
weth.deposit{value: msg.value}();
weth.approve(address(router), msg.value);
// … then swap with tokenIn = address(weth)
```

To unwrap after receiving WETH as output, set `recipient` to `address(this)`, then call `weth.withdraw(amount)` and forward the ETH.

## Testing with Foundry

Fork mainnet and run a real swap in a test:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/Test.sol";
import {ISwapRouter} from "@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract SwapRouterTest is Test {
    ISwapRouter constant ROUTER =
        ISwapRouter(0xE592427A0AEce92De3Edee1F18E0157C05861564);

    address constant WETH = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address constant USDC = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;

    function test_swapWETHForUSDC() public {
        // Give this test contract 1 WETH.
        deal(WETH, address(this), 1 ether);

        IERC20(WETH).approve(address(ROUTER), 1 ether);

        ISwapRouter.ExactInputSingleParams memory params = ISwapRouter
            .ExactInputSingleParams({
                tokenIn: WETH,
                tokenOut: USDC,
                fee: 3000,
                recipient: address(this),
                deadline: block.timestamp,
                amountIn: 1 ether,
                amountOutMinimum: 0, // acceptable in a fork test
                sqrtPriceLimitX96: 0
            });

        uint256 amountOut = ROUTER.exactInputSingle(params);
        assertGt(amountOut, 0, "Should receive USDC");

        emit log_named_uint("USDC received", amountOut);
    }
}
```

Run with:

```bash
forge test --match-test test_swapWETHForUSDC --fork-url $ETH_RPC_URL -vv
```

## Common Pitfalls

- **Forgetting `approve`** — the router pulls tokens via `transferFrom`. Without an approval the swap reverts with a generic ERC-20 error.
- **Setting `amountOutMinimum` to 0 in production** — this makes you vulnerable to sandwich attacks. Always derive it from a fresh quote.
- **Stale `deadline`** — if the deadline is in the past the tx reverts. For on-chain integrations use `block.timestamp`; for user txs add 5–20 minutes.
- **Wrong fee tier** — if the pool for that fee doesn't exist, the swap reverts. Check pool existence or use the Quoter to verify.
- **Exact-output refund** — forgetting to return unspent tokens to the caller after an `exactOutput` swap.

## Deployed Addresses

| Contract | Mainnet | Arbitrum | Optimism | Polygon | Base |
|---|---|---|---|---|---|
| SwapRouter | `0xE592…1564` | `0xE592…1564` | `0xE592…1564` | `0xE592…1564` | `0x2626…2B9d` |
| QuoterV2 | `0x61fF…E3f6` | `0x61fF…E3f6` | `0x61fF…E3f6` | `0x61fF…E3f6` | `0x3d4e…C4d8` |

Full list: [Uniswap V3 Deployments](https://docs.uniswap.org/contracts/v3/reference/deployments/).

## Further Reading

- [ISwapRouter Interface Reference](https://docs.uniswap.org/contracts/v3/reference/periphery/interfaces/ISwapRouter)
- [Uniswap V3 Swap Guide](https://docs.uniswap.org/contracts/v3/guides/swaps/single-swaps)
- [Multi-Hop Swap Guide](https://docs.uniswap.org/contracts/v3/guides/swaps/multihop-swaps)
- [QuoterV2 Reference](https://docs.uniswap.org/contracts/v3/reference/periphery/interfaces/IQuoterV2)
- [Uniswap V3 Core Whitepaper](https://uniswap.org/whitepaper-v3.pdf)
