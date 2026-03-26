---
title: "Clones with Immutable Args"
weight: 1
---

## Overview

[Minimal proxies](https://eips.ethereum.org/EIPS/eip-1167) (EIP-1167 clones) are the cheapest way to deploy many instances of the same contract. Each clone delegates every call to a shared **implementation** contract, so you only pay for ~45 bytes of creation code instead of re-deploying the full bytecode.

The limitation is that clones share the implementation's storage layout, so each instance still needs its own initialiser call to set instance-specific state — and that initialiser writes to storage, which is expensive.

[ClonesWithImmutableArgs](https://github.com/wDAI-Finance/clones-with-immutable-args) (originally by @wDAI, now widely forked) solves this by **appending arbitrary immutable data to the clone's bytecode** at deploy time. The data lives in code, not storage, so reading it costs only `CODECOPY` — far cheaper than `SLOAD`. No initialiser is needed for values that never change.

## When to Use It

- **Factory patterns** where each clone needs a handful of fixed parameters (token address, fee, owner, pool ID, etc.).
- **Gas-sensitive deployments** — you create many instances and want to avoid storage writes during init.
- **Immutable configuration** — the values genuinely never change for the lifetime of the clone.

Avoid it when the "immutable" values might need upgrading, or when the data payload is very large (bytecode size affects deployment cost).

## How It Works

1. The factory calls `ClonesWithImmutableArgs.clone(implementation, data)`.
2. The library deploys an EIP-1167 proxy with `data` appended after the delegatecall footer.
3. Inside the clone, a helper function reads the appended bytes from its own bytecode at a known offset.

Because the data is part of the deployed bytecode it is truly immutable — no one can change it after deployment.

## Installation

Using [Foundry](https://book.getfoundry.sh/):

```bash
forge install wDAI-Finance/clones-with-immutable-args
```

Add the remapping to `foundry.toml` (or `remappings.txt`):

```toml
[profile.default]
remappings = [
    "clones-with-immutable-args/=lib/clones-with-immutable-args/src/",
]
```

## Example: Token Reward Pool Factory

The implementation contract reads its immutable args instead of storing them:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Clone} from "clones-with-immutable-args/Clone.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

/// @notice A minimal reward pool whose token and owner are baked into bytecode.
contract RewardPool is Clone {
    using SafeERC20 for IERC20;

    // --- immutable args (read from appended bytecode) -----------------------

    /// @dev Bytes 0–19: the ERC-20 reward token address.
    function rewardToken() public pure returns (IERC20) {
        return IERC20(_getArgAddress(0));
    }

    /// @dev Bytes 20–39: the pool owner / admin.
    function owner() public pure returns (address) {
        return _getArgAddress(20);
    }

    /// @dev Bytes 40–71: a fixed reward amount (uint256).
    function rewardAmount() public pure returns (uint256) {
        return _getArgUint256(40);
    }

    // --- logic --------------------------------------------------------------

    function claim(address recipient) external {
        require(msg.sender == owner(), "not owner");
        rewardToken().safeTransfer(recipient, rewardAmount());
    }
}
```

The factory deploys clones with the data packed in order:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ClonesWithImmutableArgs} from "clones-with-immutable-args/ClonesWithImmutableArgs.sol";
import {RewardPool} from "./RewardPool.sol";

contract RewardPoolFactory {
    using ClonesWithImmutableArgs for address;

    address public immutable implementation;

    event PoolCreated(address indexed pool, address indexed token, address indexed owner);

    constructor() {
        implementation = address(new RewardPool());
    }

    /// @notice Deploy a new reward pool with the given immutable configuration.
    function createPool(
        address token,
        address owner,
        uint256 rewardAmount
    ) external returns (address pool) {
        // Pack args: address (20 B) + address (20 B) + uint256 (32 B) = 72 B
        bytes memory data = abi.encodePacked(token, owner, rewardAmount);
        pool = implementation.clone(data);
        emit PoolCreated(pool, token, owner);
    }
}
```

## Reading Immutable Args

The `Clone` base contract provides these helpers (among others):

| Helper | Returns | Reads |
|---|---|---|
| `_getArgAddress(offset)` | `address` | 20 bytes at `offset` |
| `_getArgUint256(offset)` | `uint256` | 32 bytes at `offset` |
| `_getArgUint64(offset)` | `uint64` | 8 bytes at `offset` |
| `_getArgUint8(offset)` | `uint8` | 1 byte at `offset` |
| `_getArgBytes(offset, length)` | `bytes memory` | arbitrary slice |

Offsets are **byte offsets** into the packed data you passed to `clone()`. Lay out your args, note each offset, and use the matching getter.

## Deterministic Deploys

Use `cloneDeterministic(implementation, data, salt)` to deploy to a predictable [CREATE2](https://eips.ethereum.org/EIPS/eip-1014) address. This is useful when other contracts or off-chain systems need to know the address before deployment:

```solidity
pool = implementation.cloneDeterministic(data, keccak256(abi.encode(token, owner)));
```

## Gotchas

{{< hint danger >}}
**Offset miscalculation loses funds.** If your offsets are wrong, getters silently return garbage. Double-check the byte layout — `address` is 20 bytes, `uint256` is 32, `uint128` is 16, etc. Write a test that round-trips every arg.
{{< /hint >}}

{{< hint warning >}}
**`msg.sender` context.** Clones use `delegatecall` to the implementation, but the proxy's own address is `address(this)`. If the implementation contract also exists standalone on-chain, make sure you are interacting with the clone address, not the implementation.
{{< /hint >}}

{{< hint warning >}}
**No reinitialisation.** There is no initialiser to call — the data is fixed at deploy time. If you need mutable state as well, set it via a separate `initialize()` function guarded by an `initialized` flag, exactly as you would with a normal proxy.
{{< /hint >}}

{{< hint info >}}
**Etherscan verification.** Proxy clones don't automatically show source on Etherscan. Use the "Is this a proxy?" feature to link to the implementation, or verify via the factory's creation event.
{{< /hint >}}

## Testing

A minimal Foundry test that verifies the immutable args round-trip:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Test} from "forge-std/Test.sol";
import {RewardPool} from "../src/RewardPool.sol";
import {RewardPoolFactory} from "../src/RewardPoolFactory.sol";

contract RewardPoolTest is Test {
    RewardPoolFactory factory;
    address token = makeAddr("token");
    address owner = makeAddr("owner");
    uint256 amount = 1 ether;

    function setUp() public {
        factory = new RewardPoolFactory();
    }

    function test_immutableArgs() public {
        address pool = factory.createPool(token, owner, amount);
        RewardPool rp = RewardPool(pool);

        assertEq(address(rp.rewardToken()), token);
        assertEq(rp.owner(), owner);
        assertEq(rp.rewardAmount(), amount);
    }
}
```

## Further Reading

- [EIP-1167: Minimal Proxy Contract](https://eips.ethereum.org/EIPS/eip-1167)
- [ClonesWithImmutableArgs repo](https://github.com/wDAI-Finance/clones-with-immutable-args)
- [Solady `LibClone`](https://github.com/Vectorized/solady/blob/main/src/utils/LibClone.sol) — a gas-optimised alternative that includes immutable-args support
