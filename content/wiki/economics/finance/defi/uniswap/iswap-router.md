---
title: "ISwapRouter — Uniswap V3 Swap Guide"
weight: 1
---

`ISwapRouter` is the interface your contract (or off-chain script) calls to execute token swaps through Uniswap V3 pools. It lives at:

```text
@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol
```

The canonical deployment is the **SwapRouter** contract. On most chains the address is `0xE592427A0AEce92De3Edee1F18E0157C05861564`.

> **Note:** Uniswap has since shipped **SwapRouter02** (combines V2 + V3 routing) and the **UniversalRouter** (V2, V3, Permit2, NFT purchases). For new integrations, evaluate those first — they offer better gas efficiency and approval flows via [Permit2](https://docs.uniswap.org/contracts/permit2/overview). This guide covers the original SwapRouter, which remains widely deployed and is the simplest to learn from.

## Installation

```bash
# Foundry
forge install Uniswap/v3-periphery

# Hardhat / npm
npm install @uniswap/v3-periphery @uniswap/v3-core
```

In Foundry add the remapping:

```text
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

## Fee Tiers

Uniswap V3 pools are deployed per fee tier. You pass the fee value to every swap call, so understand these before writing any swap code.

| Fee | [Basis Points](https://en.wikipedia.org/wiki/Basis_point) | Typical Use |
|---|---|---|
| **100** | 0.01 % | Stable-to-stable pairs (USDC/USDT). |
| **500** | 0.05 % | Correlated pairs (WETH/stETH) or high-volume majors. |
| **3000** | 0.3 % | Most standard pairs. |
| **10000** | 1 % | Exotic or low-liquidity tokens. |

If you're unsure which tier has the deepest liquidity for your pair, query the **Quoter** (see below) across all tiers and pick the one that returns the best output.

## Getting a Quote

Before executing a swap you need a quote to derive a safe `amountOutMinimum` ([slippage](https://en.wikipedia.org/wiki/Slippage_(finance)) protection). Use the `QuoterV2` contract off-chain:

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

// Apply slippage tolerance (0.5 % here — tune per pair and volatility).
uint256 amountOutMinimum = (expectedOut * 995) / 1000;
```

> **Note:** `QuoterV2` simulates the swap via `staticcall` — it reverts internally and decodes the revert data to return the quote. Call it off-chain (via `eth_call`) to avoid gas costs. Never call it on-chain in a transaction.

A 0.5 % tolerance is a reasonable starting point for major pairs. Volatile or low-liquidity pairs may need 1–3 %. The right value depends on how long your transaction might sit in the [mempool](https://en.wikipedia.org/wiki/Transaction_pool) — longer waits need wider tolerances.

## Exact-Input Single Swap

The simplest case: swap a known amount of token A for token B through one pool.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {ISwapRouter} from "@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract SimpleSwap {
    using SafeERC20 for IERC20;

    ISwapRouter public immutable router;

    constructor(address _router) {
        router = ISwapRouter(_router);
    }

    /// @notice Swap `amountIn` of tokenIn for tokenOut.
    /// @param tokenIn  Address of the token to sell.
    /// @param tokenOut Address of the token to buy.
    /// @param fee      Pool fee tier (100, 500, 3000, or 10000).
    /// @param amountIn Amount of tokenIn to spend.
    /// @param amountOutMinimum Minimum acceptable output — derive from a Quoter call.
    /// @param deadline Unix timestamp after which the tx reverts.
    /// @return amountOut Actual amount of tokenOut received.
    function swapExactInput(
        address tokenIn,
        address tokenOut,
        uint24 fee,
        uint256 amountIn,
        uint256 amountOutMinimum,
        uint256 deadline
    ) external returns (uint256 amountOut) {
        IERC20(tokenIn).safeTransferFrom(msg.sender, address(this), amountIn);
        IERC20(tokenIn).safeIncreaseAllowance(address(router), amountIn);

        ISwapRouter.ExactInputSingleParams memory params = ISwapRouter
            .ExactInputSingleParams({
                tokenIn: tokenIn,
                tokenOut: tokenOut,
                fee: fee,
                recipient: msg.sender,
                deadline: deadline,
                amountIn: amountIn,
                amountOutMinimum: amountOutMinimum,
                sqrtPriceLimitX96: 0
            });

        amountOut = router.exactInputSingle(params);
    }
}
```

### Parameter Breakdown

| Parameter | Notes |
|---|---|
| `tokenIn` / `tokenOut` | [ERC-20](https://en.wikipedia.org/wiki/ERC-20) addresses. Order matters — it determines swap direction. |
| `fee` | Identifies which pool to use. See the fee tier table above. |
| `recipient` | Where the output tokens are sent. |
| `deadline` | Unix timestamp after which the tx reverts. For atomic contract-to-contract calls `block.timestamp` is fine (it's always "now"). For user-submitted transactions, pass the deadline in as a parameter — otherwise a validator can hold the tx and execute it at an arbitrarily later time. |
| `amountIn` | Exact number of input tokens (in the token's smallest unit). |
| `amountOutMinimum` | Slippage guard. **Never set to 0 in production** — this makes you vulnerable to sandwich attacks. Derive it from a Quoter call minus your slippage tolerance. |
| `sqrtPriceLimitX96` | Cap how far the pool price can move during the swap. Encoded as a [Q64.96 fixed-point](https://en.wikipedia.org/wiki/Fixed-point_arithmetic) square root price. `0` means no limit. A non-zero value causes the swap to stop early (partial fill) if the price reaches the limit — useful for large swaps where you want to cap price impact. |

## Exact-Output Single Swap

When you need **exactly N** of the output token and are willing to spend up to a maximum of the input token. The setup is the same as exact-input — only the struct and the refund logic differ:

```solidity
function swapExactOutput(
    address tokenIn,
    address tokenOut,
    uint24 fee,
    uint256 amountOut,
    uint256 amountInMaximum,
    uint256 deadline
) external returns (uint256 amountIn) {
    IERC20(tokenIn).safeTransferFrom(msg.sender, address(this), amountInMaximum);
    IERC20(tokenIn).safeIncreaseAllowance(address(router), amountInMaximum);

    ISwapRouter.ExactOutputSingleParams memory params = ISwapRouter
        .ExactOutputSingleParams({
            tokenIn: tokenIn,
            tokenOut: tokenOut,
            fee: fee,
            recipient: msg.sender,
            deadline: deadline,
            amountOut: amountOut,
            amountInMaximum: amountInMaximum,
            sqrtPriceLimitX96: 0
        });

    amountIn = router.exactOutputSingle(params);

    // Refund unspent tokens — the router only pulls what it needs.
    if (amountIn < amountInMaximum) {
        IERC20(tokenIn).forceApprove(address(router), 0);
        IERC20(tokenIn).safeTransfer(msg.sender, amountInMaximum - amountIn);
    }
}
```

> **Important:** Always refund the difference. You transferred `amountInMaximum` but the router may have spent less. Without the refund, the surplus is stuck in the contract.

## Multi-Hop Swaps

For tokens that don't share a direct pool (or where routing through an intermediary gives a better price), use `exactInput` or `exactOutput` with an encoded path.

A path is a tightly packed sequence of `(token, fee, token, fee, token, …)`. You **must** use `abi.encodePacked` — standard `abi.encode` pads each element to 32 bytes and produces an invalid path that will revert.

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
    deadline: deadline,
    amountIn: amountIn,
    amountOutMinimum: amountOutMinimum
});

uint256 amountOut = router.exactInput(params);
```

> For `exactOutput` the path is **reversed** — it starts with the output token and ends with the input token.

## Wrapping / Unwrapping ETH

The SwapRouter does **not** accept raw ETH. Wrap it first:

```solidity
import {IWETH9} from "@uniswap/v3-periphery/contracts/interfaces/external/IWETH9.sol";

IWETH9 weth = IWETH9(router.WETH9());
weth.deposit{value: msg.value}();
IERC20(address(weth)).safeIncreaseAllowance(address(router), msg.value);
// … then swap with tokenIn = address(weth)
```

To unwrap after receiving WETH as output, set `recipient` to `address(this)`, then withdraw and forward:

```solidity
// After the swap completes and this contract holds WETH:
uint256 wethBalance = IERC20(address(weth)).balanceOf(address(this));
weth.withdraw(wethBalance);
(bool sent, ) = msg.sender.call{value: wethBalance}("");
require(sent, "ETH transfer failed");
```

> Your contract needs a `receive() external payable {}` function to accept ETH from the WETH withdraw call.

## Testing with Foundry

Fork mainnet and run a real swap in a [Foundry](https://book.getfoundry.sh/) test:

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
        console2.log("USDC received:", amountOut);
    }
}
```

Run with:

```bash
forge test --match-test test_swapWETHForUSDC --fork-url $ETH_RPC_URL -vv
```

## Common Pitfalls

> **Warning — fund loss risk:** The first two items can result in permanent loss of funds, not just reverted transactions.

- **Setting `amountOutMinimum` to 0 in production** — makes you vulnerable to [sandwich attacks](https://en.wikipedia.org/wiki/Sandwich_attack). A [MEV](https://en.wikipedia.org/wiki/Maximal_extractable_value) bot can manipulate the pool price before your swap and extract the difference. Always derive this value from a fresh Quoter call.
- **Exact-output refund** — forgetting to return unspent tokens to the caller after an `exactOutput` swap leaves funds permanently stuck in the contract.
- **Forgetting `approve`** — the router pulls tokens via `transferFrom`. Without an approval the swap reverts with a generic ERC-20 error.
- **Wrong fee tier** — if no pool exists for that fee, the swap reverts. Use the Quoter to verify the pool exists and has liquidity.
- **Stale `deadline`** — if the deadline is in the past the tx reverts. For on-chain integrations use `block.timestamp`; for user txs pass the deadline as a parameter with 5–20 minutes of buffer.
- **Using raw `approve` instead of `SafeERC20`** — tokens like USDT require the allowance to be zeroed before setting a new value. Raw `approve` calls will revert on these tokens. Use OpenZeppelin's `SafeERC20` library.

## Deployed Addresses

See the [official Uniswap V3 deployment list](https://docs.uniswap.org/contracts/v3/reference/deployments/) for full, copy-pasteable addresses across all supported chains.

## Further Reading

- [ISwapRouter Interface Reference](https://docs.uniswap.org/contracts/v3/reference/periphery/interfaces/ISwapRouter)
- [Uniswap V3 Swap Guide](https://docs.uniswap.org/contracts/v3/guides/swaps/single-swaps)
- [Multi-Hop Swap Guide](https://docs.uniswap.org/contracts/v3/guides/swaps/multihop-swaps)
- [QuoterV2 Reference](https://docs.uniswap.org/contracts/v3/reference/periphery/interfaces/IQuoterV2)
- [UniversalRouter Guide](https://docs.uniswap.org/contracts/universal-router/overview)
- [Permit2 Overview](https://docs.uniswap.org/contracts/permit2/overview)
- [Uniswap V3 Core Whitepaper](https://uniswap.org/whitepaper-v3.pdf)
