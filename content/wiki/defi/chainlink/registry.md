---
title: "Chainlink Automation Registry"
weight: 4
---

The Automation Registry is the core on-chain contract that stores, funds, and coordinates execution of all [registered](registration) upkeeps in [Chainlink Automation](automation). While the [registrar](registrar) handles onboarding new upkeeps, the registry is where they live for the rest of their lifecycle.

## Responsibilities

- **Upkeep storage** — maintains the list of active upkeeps, their configurations, and [LINK](https://en.wikipedia.org/wiki/Chainlink_(blockchain)#LINK_token) balances.
- **Node coordination** — Automation nodes read the registry to discover which upkeeps to monitor and simulate.
- **Execution accounting** — tracks gas used per `performUpkeep` call, deducts LINK accordingly, and pays node operators.
- **Admin operations** — exposes functions for upkeep owners to fund, pause, cancel, and reconfigure their upkeeps.

## Upkeep Lifecycle (Post-Registration)

Once an upkeep is [registered](registration) through the [registrar](registrar), all further interaction goes through the registry:

| Action | Registry Function | Notes |
|---|---|---|
| **Fund** | `addFunds(uint256 id, uint96 amount)` | Top up LINK. Caller must approve the registry to spend LINK first. |
| **Pause** | `pauseUpkeep(uint256 id)` | Temporarily stops execution. Only the admin can call. |
| **Unpause** | `unpauseUpkeep(uint256 id)` | Resumes a paused upkeep. |
| **Cancel** | `cancelUpkeep(uint256 id)` | Deregisters the upkeep. Remaining LINK is refundable after a cooldown (~50 blocks). |
| **Withdraw funds** | `withdrawFunds(uint256 id, address to)` | Claim remaining LINK after cancellation cooldown. |
| **Update gas limit** | `setUpkeepGasLimit(uint256 id, uint32 gasLimit)` | Change the max gas for `performUpkeep`. |
| **Update check data** | `setUpkeepCheckData(uint256 id, bytes checkData)` | Change the bytes passed to `checkUpkeep`. |
| **Transfer admin** | `transferUpkeepAdmin(uint256 id, address proposed)` | Initiate admin transfer (new admin must accept). |

## Registry Versions

Chainlink has shipped multiple registry versions as the protocol evolved:

| Version | Key Changes |
|---|---|
| **v1.0** | Original Keepers registry. Basic conditional upkeeps. |
| **v1.1** | Improved gas accounting, onchain verification. |
| **v2.0** | Rebranded to Automation. Added log triggers, off-chain computation, forwarder contracts. |
| **v2.1** | StreamsLookup support, improved gas overhead calculations. |

Each version deploys a new registry (and registrar) contract. Existing upkeeps on older registries continue working but don't get new features. The [migration functions](https://docs.chain.link/chainlink-automation/guides/migrate-upkeeps) let you move upkeeps to a newer registry.

## Funding Model

The registry holds LINK balances on behalf of each upkeep. When an Automation node executes `performUpkeep`:

1. The registry measures actual gas used.
2. It converts gas cost to LINK using the on-chain LINK/ETH price feed.
3. It adds the network-specific premium (typically 20–80%).
4. It deducts the total from the upkeep's LINK balance.

If the balance reaches zero, the registry pauses the upkeep until more LINK is added.

## Finding Registry Addresses

Registry addresses are network-specific and version-specific. The canonical reference is the [Supported Networks](https://docs.chain.link/chainlink-automation/overview/supported-networks) page in the Chainlink docs.

## Further Reading

- [Chainlink Automation Architecture](https://docs.chain.link/chainlink-automation/concepts/automation-architecture)
- [Supported Networks & Registry Addresses](https://docs.chain.link/chainlink-automation/overview/supported-networks)
- [Migrate Upkeeps to a New Registry](https://docs.chain.link/chainlink-automation/guides/migrate-upkeeps)
- [Automation Billing & Premiums](https://docs.chain.link/chainlink-automation/overview/automation-economics)
