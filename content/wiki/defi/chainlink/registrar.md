---
title: "Chainlink Automation Registrar"
weight: 3
---

The Automation Registrar is the on-chain contract that accepts and processes [upkeep registration](registration) requests for [Chainlink Automation](automation). It acts as the gatekeeper between users who want to register upkeeps and the Automation [registry](https://docs.chain.link/chainlink-automation/concepts/automation-architecture#registry) that actually tracks and executes them.

## How It Works

The registrar exposes a `registerUpkeep` function that accepts a `RegistrationParams` struct and a [LINK](https://en.wikipedia.org/wiki/Chainlink_(blockchain)#LINK_token) payment. On receiving a valid request, it:

1. Transfers the LINK funding from the caller to the registry.
2. Creates a new upkeep entry in the registry.
3. Returns the `upkeepId` — a `uint256` that uniquely identifies the upkeep.

Depending on the network and configuration, registration may be **auto-approved** (instant) or require **manual approval** by the registry owner. Mainnet deployments typically auto-approve; testnets vary.

## Interface

The registrar implements `IAutomationRegistrar`. The key struct and function:

```solidity
import {IAutomationRegistrar} from "@chainlink/contracts/src/v0.8/automation/interfaces/IAutomationRegistrar.sol";

struct RegistrationParams {
    string name;
    bytes encryptedEmail;
    address upkeepContract;
    uint32 gasLimit;
    address adminAddress;
    uint8 triggerType;      // 0 = conditional, 1 = log trigger
    bytes checkData;
    bytes triggerConfig;
    bytes offchainConfig;
    uint96 amount;          // LINK funding in wei (18 decimals)
}

// Caller must first approve the registrar to spend `params.amount` of LINK.
function registerUpkeep(RegistrationParams memory params) external returns (uint256 upkeepId);
```

## Finding the Registrar Address

Registrar addresses differ per network and per registry version. The canonical source is the [Chainlink Automation Supported Networks](https://docs.chain.link/chainlink-automation/overview/supported-networks) page, which lists both the registry and registrar addresses for each chain.

Hardcoding addresses is fragile across upgrades. For production systems, consider reading the registrar address from a deployment config or environment variable.

## Registrar vs Registry

| | Registrar | Registry |
|---|---|---|
| **Purpose** | Accepts new upkeep registrations | Stores upkeeps, coordinates execution |
| **Who calls it** | Users / deployer scripts | Automation nodes |
| **LINK flow** | Receives LINK from caller, forwards to registry | Holds LINK balances, pays node operators |

The registrar is a thin coordination layer. Once an upkeep is registered, all subsequent interactions (funding, cancellation, configuration changes) go directly through the registry.

## Further Reading

- [Chainlink Automation Docs — Register an Upkeep](https://docs.chain.link/chainlink-automation/guides/register-upkeep)
- [Supported Networks & Contract Addresses](https://docs.chain.link/chainlink-automation/overview/supported-networks)
- [Automation Architecture](https://docs.chain.link/chainlink-automation/concepts/automation-architecture)
