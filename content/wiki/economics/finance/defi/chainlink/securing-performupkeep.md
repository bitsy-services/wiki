---
title: "Securing performUpkeep"
weight: 6
---

`performUpkeep` is an external function that anyone can call — not just [Chainlink Automation](automation) nodes. If your implementation has side effects (transferring funds, changing critical state), you need to ensure that unauthorized callers can't exploit it.

There are two complementary strategies: **re-validation** (making the function safe for anyone to call) and **access control** (restricting who can call it). Use both when possible.

## Strategy 1: Re-Validate On-Chain

The simplest defense. Inside `performUpkeep`, re-check the same condition that `checkUpkeep` evaluated off-chain. If the condition no longer holds, revert.

```solidity
import {AutomationCompatibleInterface} from "@chainlink/contracts/src/v0.8/automation/AutomationCompatible.sol";

contract RevalidationExample is AutomationCompatibleInterface {
    uint256 public lastTimestamp;
    uint256 public immutable interval;

    function checkUpkeep(bytes calldata)
        external view override
        returns (bool upkeepNeeded, bytes memory)
    {
        upkeepNeeded = (block.timestamp - lastTimestamp) >= interval;
    }

    function performUpkeep(bytes calldata) external override {
        // Re-validate: if the interval hasn't elapsed, revert.
        require(
            (block.timestamp - lastTimestamp) >= interval,
            "Not ready"
        );
        lastTimestamp = block.timestamp;
        // ... actual logic ...
    }
}
```

This makes `performUpkeep` **idempotent** — calling it when the condition isn't met is a no-op (reverts). An attacker gains nothing by calling it directly because either:

- The condition is met, in which case the work was going to happen anyway.
- The condition isn't met, in which case the call reverts.

Re-validation is essential even when you also use access control, because the on-chain state can change between the off-chain `checkUpkeep` simulation and the on-chain `performUpkeep` execution.

## Strategy 2: Forwarder-Based Access Control

Restrict `performUpkeep` to calls from the upkeep's [forwarder](forwarder) contract. The forwarder address is stable and unique per upkeep, making it a reliable access control check.

```solidity
import {AutomationCompatibleInterface} from "@chainlink/contracts/src/v0.8/automation/AutomationCompatible.sol";

contract ForwarderGuardedExample is AutomationCompatibleInterface {
    address public automationForwarder;
    address public immutable admin;

    constructor(address _admin) {
        admin = _admin;
    }

    /// @notice Set after registration, once the forwarder address is known.
    function setForwarder(address _forwarder) external {
        require(msg.sender == admin, "Only admin");
        require(automationForwarder == address(0), "Already set");
        automationForwarder = _forwarder;
    }

    modifier onlyForwarder() {
        require(msg.sender == automationForwarder, "Only forwarder");
        _;
    }

    function checkUpkeep(bytes calldata)
        external view override
        returns (bool, bytes memory)
    {
        // ...
    }

    function performUpkeep(bytes calldata performData)
        external override onlyForwarder
    {
        // Still re-validate the condition here.
        // ...
    }
}
```

## When Access Control Matters Most

Re-validation alone is sufficient when `performUpkeep` is naturally idempotent — the function does the same thing regardless of who calls it, and the condition gate prevents premature execution.

Add forwarder-based access control when:

- **Order-dependent logic** — e.g. processing a queue where the sequence of execution matters and a front-runner could manipulate it.
- **MEV-sensitive operations** — if `performData` encodes a price or trade route, an attacker who calls `performUpkeep` with crafted data could extract value.
- **Gas griefing** — a caller invokes `performUpkeep` to waste gas (and your LINK balance) even though the real condition isn't met, in cases where the re-validation check is expensive.

## Anti-Patterns

**Checking `tx.origin`** — `tx.origin` is the EOA that submitted the transaction, not the Automation infrastructure. It rotates across node operators, can be spoofed in internal calls, and is broadly considered [an unreliable access control mechanism](https://docs.soliditylang.org/en/latest/security-considerations.html#tx-origin).

**Maintaining an allowlist of node addresses** — node transmitter addresses change as the network evolves. You'd need to keep the allowlist in sync with the [registry](registry), which is fragile and unnecessary when the forwarder pattern exists.

**No validation at all** — relying on `checkUpkeep` to gate execution is insufficient. `checkUpkeep` runs off-chain; it doesn't prevent direct on-chain calls to `performUpkeep`.

## Decision Tree

```text
Is performUpkeep naturally idempotent?
├── Yes → Re-validation is sufficient for most cases
│         └── Does it handle MEV-sensitive data? → Add forwarder guard
└── No  → Use forwarder access control + re-validation
```

## Further Reading

- [Chainlink Docs — Security Considerations](https://docs.chain.link/chainlink-automation/concepts/best-practice)
- [Forwarder](forwarder) — how the per-upkeep proxy works
- [Automation Architecture](https://docs.chain.link/chainlink-automation/concepts/automation-architecture)
