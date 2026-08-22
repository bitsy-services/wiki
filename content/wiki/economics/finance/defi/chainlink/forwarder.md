---
title: "Chainlink Automation Forwarder"
weight: 5
---

An Automation Forwarder is a per-upkeep proxy contract that sits between the [Chainlink Automation](automation) network and your target contract. Instead of Automation nodes calling `performUpkeep` directly on your contract, they call it through the forwarder — giving your contract a stable, predictable `msg.sender` to verify.

## Why It Exists

Without a forwarder, `performUpkeep` is called by whichever Automation node wins the turn. The caller address rotates across a set of node-operated transmitter addresses that can change over time. This makes access control difficult: you can't simply check `msg.sender` against a known address.

The forwarder solves this by giving each upkeep its own dedicated proxy address. Your contract checks `msg.sender == myForwarder` and that's it.

## How It Works

```text
Automation Node  →  Forwarder (stable address)  →  Your Contract
```

1. When an upkeep is [registered](registration) on a v2.0+ [registry](registry), the registry deploys a forwarder contract for that upkeep.
2. Automation nodes call `performUpkeep` on the forwarder.
3. The forwarder delegates the call to your contract, preserving `performData`.
4. Your contract sees `msg.sender` as the forwarder address.

## Getting the Forwarder Address

After registration, query the registry for your upkeep's forwarder:

```solidity
import {IAutomationRegistryConsumer} from "@chainlink/contracts/src/v0.8/automation/interfaces/IAutomationRegistryConsumer.sol";

address forwarder = registry.getForwarder(upkeepId);
```

Or read it from the Automation dashboard at [automation.chain.link](https://automation.chain.link/) — the upkeep detail page shows the forwarder address.

## Using the Forwarder for Access Control

See [Securing `performUpkeep`](securing-performupkeep) for the full pattern. The short version:

```solidity
import {AutomationCompatibleInterface} from "@chainlink/contracts/src/v0.8/automation/AutomationCompatible.sol";

contract MyAutomatedContract is AutomationCompatibleInterface {
    address public immutable automationForwarder;

    constructor(address _forwarder) {
        automationForwarder = _forwarder;
    }

    function performUpkeep(bytes calldata performData) external override {
        require(msg.sender == automationForwarder, "Only forwarder");
        // ...
    }
}
```

If you don't know the forwarder address at deploy time (because registration hasn't happened yet), use a setter that the admin calls once after registration:

```solidity
address public automationForwarder;
address public immutable admin;

function setForwarder(address _forwarder) external {
    require(msg.sender == admin, "Only admin");
    require(automationForwarder == address(0), "Already set");
    automationForwarder = _forwarder;
}
```

## Forwarder vs Direct Call

| | With Forwarder | Without Forwarder |
|---|---|---|
| **`msg.sender`** | Stable, per-upkeep address | Rotating node transmitter addresses |
| **Access control** | Simple `== forwarder` check | Must maintain a set of allowed callers, or skip access control |
| **Registry version** | v2.0+ | All versions |
| **Setup** | Automatic on registration | N/A |

## Further Reading

- [Chainlink Docs — Using the Forwarder](https://docs.chain.link/chainlink-automation/guides/forwarder)
- [Automation Architecture](https://docs.chain.link/chainlink-automation/concepts/automation-architecture)
