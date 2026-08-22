---
title: Decentralized Keeper
weight: 65
---

A decentralized keeper is an autonomous agent -- or a network of such agents -- that monitors on-chain conditions and executes [smart contract](/wiki/economics/finance/defi/smart-contract) functions when those conditions are met. Keepers handle the "cron jobs" of DeFi: liquidations, [oracle](/wiki/economics/finance/defi/oracle-node) price updates, reward harvesting, limit-order execution, and any other task that a contract cannot trigger by itself because the EVM has no built-in scheduler.

## Why Keepers Exist

Smart contracts on [Ethereum](/wiki/economics/finance/defi/ethereum/) and other chains are reactive -- they run only when an external account submits a transaction. Many protocol-critical actions (liquidating an under-collateralized loan, settling an expired option, compounding [yield-farming](/wiki/economics/finance/defi/yield-farming) rewards) must happen promptly, yet the contract cannot call itself. Keepers bridge this gap by watching for trigger conditions off-chain and submitting the necessary transaction when the time comes.

## Why Decentralization Matters

A single centralized bot can perform the same mechanical task, but it introduces a single point of failure. If the operator goes offline, misses a block, or acts maliciously, the protocol suffers. Decentralized keeper networks distribute the work across many independent participants, which provides:

- **Liveness** -- if one keeper is down, others pick up the task.
- **Censorship resistance** -- no single party can withhold execution.
- **Economic alignment** -- keepers compete for rewards, which keeps execution prompt and costs competitive.

## Common Use Cases

| Task | Example protocols |
|---|---|
| Liquidations | Aave, Compound, Maker |
| Oracle price-feed updates | [Chainlink](/wiki/economics/finance/defi/oracle-node) data feeds |
| Yield harvesting and auto-compounding | Yearn, Beefy |
| Limit and stop-loss order execution | [DEX](/wiki/economics/finance/defi/dex) aggregators, on-chain order books |
| Rebalancing LP positions | Concentrated-liquidity managers |
| Options and futures settlement | On-chain derivatives protocols |

## Avoiding Duplicate Execution

When multiple keepers watch the same trigger, naive execution would waste gas on redundant transactions. Networks use several techniques to prevent this:

1. **On-chain state locks** -- the contract flips a flag or advances a nonce as part of the keeper's transaction, causing any competing transaction to revert.
2. **Turn-based rotation** -- keepers are assigned time slots or round-robin order so only one is eligible at any moment. [Chainlink Automation](/wiki/economics/finance/defi/chainlink/automation) uses a rotating-leader model.
3. **First-past-the-post rewards** -- only the transaction that actually changes state earns the reward; duplicate attempts simply burn gas, which is a strong economic disincentive.
4. **Off-chain coordination** -- some networks let keepers signal intent before submitting, reducing on-chain collisions.

## Major Implementations

### Chainlink Automation (formerly Chainlink Keepers)

[Chainlink Automation](/wiki/economics/finance/defi/chainlink/automation) is the most widely adopted keeper service. Developers register an "upkeep" by deploying a contract that implements two functions: `checkUpkeep` (a view function that returns whether work is needed) and `performUpkeep` (the state-changing call). Chainlink's decentralized node network monitors `checkUpkeep` off-chain and calls `performUpkeep` when it returns true. Upkeeps are funded with LINK tokens, and the network uses a rotating-leader design to avoid duplicate execution.

### Gelato Network

Gelato offers a flexible automation layer that supports time-based triggers, on-chain condition checks, and off-chain "resolver" functions written in TypeScript. It supports multiple chains and integrates tightly with smart-contract wallets. Tasks can be funded with the protocol's native token or with the network's fee token.

### Keep3r Network

Created by Andre Cronje, Keep3r is a more permissionless marketplace: any protocol can post a "job," and any bonded keeper can execute it. Keepers earn KP3R tokens for completed work. The system relies on bonding and slashing to deter misbehavior rather than on a managed node set.

## Risks and Limitations

**Gas-cost spikes** -- during periods of extreme network congestion, keeper rewards may not cover gas costs, causing delays in time-sensitive actions like liquidations. This is a liveness risk for any protocol that depends on prompt keeper execution.

**Incentive misalignment** -- if rewards are too low relative to gas costs or competing MEV opportunities, keepers may deprioritize a protocol's tasks. Some protocols mitigate this by offering dynamic, gas-adjusted rewards.

**[MEV](/wiki/economics/finance/defi/maximal-extractable-value) extraction** -- keepers that perform liquidations or large swaps can be sandwiched or front-run by MEV searchers, reducing their effective reward and potentially harming the protocol's users.

**Smart-contract risk** -- keepers interact with protocol contracts, so a vulnerability in either the keeper infrastructure or the target contract can be exploited. Both sides need thorough auditing.

**Oracle dependency** -- keepers that trigger based on price data inherit the risks of the underlying [oracle](/wiki/economics/finance/defi/oracle-node). Stale or manipulated feeds can cause incorrect liquidations or settlements.
