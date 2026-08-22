---
title: "Chainlink Automation"
weight: 1
---

[Chainlink](https://en.wikipedia.org/wiki/Chainlink_(blockchain)) Automation (formerly Keepers) lets you trigger on-chain function calls on a schedule or in response to custom conditions — without running your own bot infrastructure.

## When to Use It

- **Periodic maintenance** — harvesting yield, rebasing tokens, updating [oracles](https://en.wikipedia.org/wiki/Blockchain_oracle).
- **Conditional execution** — [liquidations](https://en.wikipedia.org/wiki/Liquidation#Decentralized_finance), limit-order fills, rebalancing when a threshold is crossed.
- **Replacing cron bots** — any off-chain script that just calls a contract method can usually move to Automation.

## Core Concepts

| Term | Meaning |
|---|---|
| **Upkeep** | A registered job — the thing Automation monitors and executes. |
| **Trigger** | What fires the upkeep: *time-based* (cron) or *custom logic* (conditional). |
| **`checkUpkeep`** | View function Automation calls off-chain to ask "should I execute?" |
| **`performUpkeep`** | State-changing function Automation calls on-chain when `checkUpkeep` returns true. |
| **[LINK](https://en.wikipedia.org/wiki/Chainlink_(blockchain)#LINK_token) funding** | Each upkeep has a LINK balance that pays node operators per execution. |

## Supported Networks

Automation is live on Ethereum mainnet, Arbitrum, Optimism, Polygon, Avalanche, BSC, and Base (among others). Check the [Chainlink docs](https://docs.chain.link/chainlink-automation/overview/supported-networks) for the current list and [registry](registry) addresses.

## Step-by-Step: Register a Custom-Logic Upkeep

### 1. Implement the Automation Interface

Your contract must expose `checkUpkeep` and `performUpkeep`:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {AutomationCompatibleInterface} from "@chainlink/contracts/src/v0.8/automation/AutomationCompatible.sol";

contract MyAutomatedContract is AutomationCompatibleInterface {
    uint256 public lastTimestamp;
    uint256 public interval;

    constructor(uint256 _interval) {
        interval = _interval;
        lastTimestamp = block.timestamp;
    }

    /// @notice Called off-chain by Automation nodes.
    /// @return upkeepNeeded true when the interval has elapsed.
    /// @return performData passed through to performUpkeep.
    function checkUpkeep(bytes calldata /* checkData */)
        external
        view
        override
        returns (bool upkeepNeeded, bytes memory performData)
    {
        upkeepNeeded = (block.timestamp - lastTimestamp) >= interval;
        performData = ""; // encode extra context here if needed
    }

    /// @notice Called on-chain when checkUpkeep returns true.
    function performUpkeep(bytes calldata /* performData */) external override {
        // Re-validate the condition on-chain (nodes could be stale).
        require(
            (block.timestamp - lastTimestamp) >= interval,
            "Interval not elapsed"
        );
        lastTimestamp = block.timestamp;

        // --- your logic here ---
    }
}
```

> **Important:** Always re-check the condition inside `performUpkeep`. Between the off-chain check and on-chain execution, state can change.

### 2. Deploy & Verify

Deploy to your target network and verify on the [block explorer](https://en.wikipedia.org/wiki/Block_explorer) so the Automation UI can read the [ABI](https://docs.soliditylang.org/en/latest/abi-spec.html).

```bash
forge create src/MyAutomatedContract.sol:MyAutomatedContract \
  --constructor-args 3600 \
  --rpc-url $RPC_URL \
  --private-key $DEPLOYER_KEY \
  --verify
```

### 3. [Register](registration) the Upkeep

**Option A — UI**

1. Go to [automation.chain.link](https://automation.chain.link/).
2. Connect your wallet and select the correct network.
3. Click **Register new Upkeep**.
4. Choose **Custom logic** as the trigger.
5. Paste your contract address — the UI will detect `checkUpkeep` / `performUpkeep`.
6. Set a name, gas limit, and starting LINK balance (5 LINK is a safe minimum for testing).
7. Confirm the transaction.

**Option B — Programmatic (Solidity)**

Call the [registrar](registrar) contract directly:

```solidity
IAutomationRegistrar registrar = IAutomationRegistrar(REGISTRAR_ADDRESS);

RegistrationParams memory params = RegistrationParams({
    name: "My Upkeep",
    encryptedEmail: "",
    upkeepContract: address(myContract),
    gasLimit: 500_000,
    adminAddress: msg.sender,
    triggerType: 0, // 0 = conditional, 1 = log trigger
    checkData: "",
    triggerConfig: "",
    offchainConfig: "",
    amount: 5 ether // 5 LINK (18 decimals)
});

LINK.approve(address(registrar), params.amount);
uint256 upkeepId = registrar.registerUpkeep(params);
```

### 4. Fund & Monitor

- Top up LINK before the balance runs out — Automation pauses unfunded upkeeps.
- Use the dashboard at [automation.chain.link](https://automation.chain.link/) to view history, gas usage, and remaining balance.
- Set up a low-balance alert (the UI supports email notifications).

## Step-by-Step: Time-Based (Cron) Upkeep

If you just need a function called on a schedule, you can skip `checkUpkeep` entirely:

1. Register via the UI and choose **Time-based** trigger.
2. Enter a [cron expression](https://en.wikipedia.org/wiki/Cron#CRON_expression) (e.g. `0 */6 * * *` for every 6 hours).
3. Select the target contract and function — the UI lets you pick from the ABI.
4. Fund with LINK and confirm.

No interface changes to your contract are required for time-based upkeeps.

## Log-Trigger Upkeeps

Automation can also fire in response to a specific event log:

```solidity
// Emit this event when you want Automation to react.
event ThresholdCrossed(uint256 indexed value);
```

Register with trigger type **Log trigger**, specify the event signature and optional topic filters. Automation watches for matching logs and calls `performUpkeep` with the log data encoded in `performData`.

## Gas & Cost Considerations

- **Gas limit** — set it high enough for worst-case execution. Unused gas is not charged.
- **Premium** — Automation charges a percentage premium on top of gas (varies by network, typically 20–80 %).
- **`checkUpkeep` cost** — runs off-chain, so it doesn't cost gas, but keep it lightweight to avoid simulation timeouts (target < 5 M gas).
- **Batch awareness** — if many upkeeps fire in the same block, the network can get congested. Design `performUpkeep` to be gas-efficient.

## Testing Locally

Use a [Foundry](https://book.getfoundry.sh/) fork test to simulate the Automation cycle:

```solidity
function test_automationCycle() public {
    // Warp past the interval.
    vm.warp(block.timestamp + 3601);

    (bool needed, bytes memory data) = myContract.checkUpkeep("");
    assertTrue(needed);

    myContract.performUpkeep(data);
    assertEq(myContract.lastTimestamp(), block.timestamp);
}
```

## Security Checklist

- [ ] `performUpkeep` re-validates the trigger condition on-chain.
- [ ] `performUpkeep` is [access-controlled or idempotent](securing-performupkeep) — anyone can call it, not just Automation nodes.
- [ ] No unbounded loops in `checkUpkeep` (simulation gas limit applies).
- [ ] LINK funding is monitored to prevent upkeep pausing at a critical moment.
- [ ] Contract is verified on the block explorer for transparency.

## Further Reading

- [Chainlink Automation Docs](https://docs.chain.link/chainlink-automation)
- [Automation-Compatible Contract Reference](https://docs.chain.link/chainlink-automation/guides/compatible-contracts)
- [Supported Networks & Registry Addresses](https://docs.chain.link/chainlink-automation/overview/supported-networks)
- [Automation Architecture (how nodes coordinate)](https://docs.chain.link/chainlink-automation/concepts/automation-architecture)
- [Forwarder](forwarder) — per-upkeep proxy for stable `msg.sender`
- [Securing `performUpkeep`](securing-performupkeep) — access control and re-validation patterns
