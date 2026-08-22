---
title: "Clones with Immutable Args"
weight: 1
---

## Overview

[Minimal proxies](https://eips.ethereum.org/EIPS/eip-1167) (EIP-1167 clones) are the cheapest way to deploy many instances of the same contract. Each clone delegates every call to a shared **implementation** contract, so you only pay for ~45 bytes of creation code instead of re-deploying the full bytecode.

The limitation is that clones share the implementation's storage layout, so each instance still needs its own initialiser call to set instance-specific state — and that initialiser writes to storage, which is expensive.

OpenZeppelin's [`Clones`](https://docs.openzeppelin.com/contracts/5.x/api/proxy#Clones) library (v5.2+) solves this by **appending arbitrary immutable data to the clone's bytecode** at deploy time. The data lives in code, not storage, so reading it costs only `CODECOPY` — far cheaper than `SLOAD`. No initialiser is needed for values that never change.

## When to Use It

- **Factory patterns** where each clone needs a handful of fixed parameters (token address, fee, owner, pool ID, etc.).
- **Gas-sensitive deployments** — you create many instances and want to avoid storage writes during init.
- **Immutable configuration** — the values genuinely never change for the lifetime of the clone.

Avoid it when the "immutable" values might need upgrading, or when the data payload is very large (bytecode size affects deployment cost).

## How It Works

1. The factory calls `Clones.cloneWithImmutableArgs(implementation, data)`.
2. The library deploys an EIP-1167 proxy with `data` appended after the delegatecall footer.
3. Inside the clone, `Clones.fetchCloneArgs()` reads the appended bytes from the clone's bytecode.

Because the data is part of the deployed bytecode it is truly immutable — no one can change it after deployment.

## Example: Token Reward Pool Factory

The implementation contract reads its immutable args via `Clones.fetchCloneArgs()` and unpacks them with `abi.decode`:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Clones} from "@openzeppelin/contracts/proxy/Clones.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

/// @notice A minimal reward pool whose token, owner, and amount are baked into bytecode.
contract RewardPool {
    using SafeERC20 for IERC20;

    function rewardToken() public view returns (IERC20) {
        (address token,,) = _immutableArgs();
        return IERC20(token);
    }

    function owner() public view returns (address) {
        (, address owner_,) = _immutableArgs();
        return owner_;
    }

    function rewardAmount() public view returns (uint256) {
        (,, uint256 amount) = _immutableArgs();
        return amount;
    }

    function claim(address recipient) external {
        require(msg.sender == owner(), "not owner");
        rewardToken().safeTransfer(recipient, rewardAmount());
    }

    function _immutableArgs() internal view returns (address, address, uint256) {
        bytes memory data = Clones.fetchCloneArgs(address(this));
        return abi.decode(data, (address, address, uint256));
    }
}
```

The factory deploys clones with ABI-encoded data:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Clones} from "@openzeppelin/contracts/proxy/Clones.sol";
import {RewardPool} from "./RewardPool.sol";

contract RewardPoolFactory {
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
        bytes memory data = abi.encode(token, owner, rewardAmount);
        pool = Clones.cloneWithImmutableArgs(implementation, data);
        emit PoolCreated(pool, token, owner);
    }
}
```

## Deterministic Deploys

Use `cloneDeterministicWithImmutableArgs` to deploy to a predictable [CREATE2](https://eips.ethereum.org/EIPS/eip-1014) address. This is useful when other contracts or off-chain systems need to know the address before deployment:

```solidity
bytes memory data = abi.encode(token, owner, rewardAmount);
bytes32 salt = keccak256(abi.encode(token, owner));
pool = Clones.cloneDeterministicWithImmutableArgs(implementation, data, salt);
```

Predict the address off-chain or from another contract with `predictDeterministicAddressWithImmutableArgs`.

## Gotchas

{{< hint danger >}}
**Decode mismatch loses funds.** If the `abi.encode` in the factory and `abi.decode` in the implementation disagree on types or order, the getters silently return garbage. Write a test that round-trips every arg.
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

## Alternatives

| Library | Notes |
|---|---|
| [Solady `LibClone`](https://github.com/Vectorized/solady/blob/main/src/utils/LibClone.sol) | Gas-optimised alternative with immutable-args support and appendable clones. |
| [wDAI ClonesWithImmutableArgs](https://github.com/wDAI-Finance/clones-with-immutable-args) | The original implementation that popularised the pattern. Uses manual byte-offset getters instead of `abi.decode`. |

## Further Reading

- [EIP-1167: Minimal Proxy Contract](https://eips.ethereum.org/EIPS/eip-1167)
- [OpenZeppelin Clones API](https://docs.openzeppelin.com/contracts/5.x/api/proxy#Clones)
