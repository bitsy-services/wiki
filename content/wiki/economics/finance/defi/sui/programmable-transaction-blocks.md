---
title: "Programmable Transaction Blocks"
weight: 30
---

A **Programmable Transaction Block** (PTB) is a single Sui transaction built as an ordered sequence of *commands* that execute atomically: either every command succeeds and the whole block commits, or any failure reverts the entire block. The defining feature is that the **output of one command can be fed as the input to a later one**. Results behave like registers — typed, transient values that live only for the duration of the transaction — so you can wire heterogeneous operations together: [Move](/wiki/economics/finance/defi/sui/sui-move) calls, [object](/wiki/economics/finance/defi/sui/object-model) transfers, coin splits and merges, package publishing, and building Move vectors, all in one shot.

## No Glue Contract Required

The closest analogue on [Ethereum](/wiki/economics/finance/defi/ethereum/) is the "multicall" or router pattern: to batch N actions atomically, you must deploy a smart contract that performs them in its own function body, because the [EVM](/wiki/economics/finance/defi/ethereum#the-ethereum-virtual-machine-evm) gives the client no way to chain arbitrary calls within one transaction. That deployed contract is on-chain glue that has to be written, audited, and maintained.

Sui inverts this. The PTB *is* the composition layer, assembled client-side and submitted as data, so calls can be chained across protocols the caller does not control and has never deployed code against, with no intermediary contract in between. This is why PTBs are central to how [dApps](/wiki/economics/finance/defi/dapp) and DeFi aggregators are built on Sui — the composability lives in the transaction, not in a bespoke contract.

## Anatomy

A PTB carries a list of **inputs** (objects and pure values) and a list of **commands** that consume those inputs and each other's results. A block can hold up to roughly **1024 commands**, which is enough to encode substantial multi-step flows in one atomic unit. The common command types:

- `splitCoins` — split one or more new coins off an existing coin (often the gas coin).
- `mergeCoins` — fold several coins into one.
- `transferObjects` — send a list of objects to a recipient.
- `moveCall` — invoke a function in a published Move package.
- `makeMoveVec` — assemble individual values into a Move `vector` to pass to a `moveCall`.
- `publish` — publish a new Move package.

## The Classic Example

The canonical pattern is: split an exact amount off the gas coin, hand it to a DeFi method, then transfer whatever comes back — all in one atomic block. The example below uses the current TypeScript SDK, the `@mysten/sui` package and its `Transaction` builder.

```typescript
import { Transaction } from "@mysten/sui/transactions";

const tx = new Transaction();

// Split 1000 MIST off the gas coin into a fresh coin.
const [coin] = tx.splitCoins(tx.gas, [1000]);

// Pass that coin into a Move call (e.g. a swap or deposit).
const result = tx.moveCall({
  target: "0xPACKAGE::pool::deposit",
  arguments: [tx.object("0xPOOL_ID"), coin],
});

// Transfer whatever the call returned to the recipient.
tx.transferObjects([result], tx.pure.address("0xRECIPIENT"));
```

Note that `tx.gas` references the gas coin directly — `splitCoins` peels a new coin off it without a separate funding object. The `[coin]` and `result` values are command outputs, not concrete objects; they only resolve when the network executes the block.

> An earlier SDK, `@mysten/sui.js`, exposed this through a `TransactionBlock` class. That package is deprecated; current code uses `@mysten/sui` with `Transaction`. The on-chain concept is identical — only the client class was renamed.

## What it buys

- **Composability without on-chain glue.** Chain actions across unrelated protocols with no router contract to deploy or trust.
- **Atomicity.** Partial execution is impossible, so multi-step DeFi flows (split → swap → stake → transfer) cannot leave funds stranded mid-sequence.
- **Fewer round-trips and lower cost.** One signature, one transaction, one gas payment for what would otherwise be several transactions or a custom contract deployment.
- **Aggregator-friendly.** Routers and [DEX](/wiki/economics/finance/defi/dex) aggregators compose pool calls dynamically per request instead of shipping a new contract for each strategy.

## External Links

- [Programmable Transaction Blocks](https://docs.sui.io/concepts/transactions/prog-txn-blocks) — Sui concept documentation
- [Sui TypeScript SDK](https://sdk.mystenlabs.com/typescript) — `@mysten/sui` reference and the `Transaction` builder
