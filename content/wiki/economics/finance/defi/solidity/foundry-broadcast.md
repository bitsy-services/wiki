---
title: "Foundry Broadcast"
weight: 20
---

[Foundry](/wiki/economics/finance/defi/solidity/foundry) scripts use `vm.startBroadcast()` and `vm.stopBroadcast()` to mark which parts of a Solidity script should produce real on-chain transactions. A common misconception is that everything between the two calls executes as a single atomic transaction. It does not — each state-changing statement becomes its own transaction.

## How broadcast works

A broadcast block looks like this:

```solidity
vm.startBroadcast(deployerPrivateKey);

MyToken token = new MyToken();          // tx 1: deploy
token.initialize(owner, supply);        // tx 2: external call

vm.stopBroadcast();
```

Foundry processes this in two phases:

### Phase 1 — Local simulation

Before anything touches a real network, Foundry runs the entire script in a local [EVM](/wiki/economics/finance/defi/ethereum#the-ethereum-virtual-machine-evm). This simulation executes in a single context, so `token.initialize(...)` can reference the address returned by `new MyToken()` even though they will eventually be separate transactions. If any statement reverts during simulation, the script aborts and nothing is broadcast.

### Phase 2 — Sequential broadcast

After simulation succeeds, Foundry replays the recorded state-changing operations as individual transactions, each with an incrementing [nonce](/wiki/economics/finance/defi/nonce). The transactions are submitted in the order they appeared in the script.

By default (without `--slow`), Foundry fires off all transactions without waiting for confirmations. This is fast, but creates a risk: if an earlier transaction reverts on-chain — because network state changed between simulation and broadcast — every later transaction that depends on it will likely fail too, since they were already submitted.

With the `--slow` flag, Foundry waits for each transaction to be confirmed before sending the next. This lets the script stop early on failure instead of wasting gas on doomed transactions.

```bash
# Fast (default): send all at once
forge script script/Deploy.s.sol --broadcast --rpc-url $RPC_URL

# Slow: wait for confirmations between transactions
forge script script/Deploy.s.sol --broadcast --rpc-url $RPC_URL --slow
```

## What generates a transaction (and what doesn't)

Only state-changing operations on external contracts produce transactions:

| Operation | Generates a transaction? |
|---|---|
| `new MyContract()` | Yes — contract deployment |
| `contract.someFunction()` | Yes — external call that modifies state |
| `address.call{value: 1 ether}("")` | Yes — value transfer |
| `uint x = contract.viewFunction()` | No — read-only call |
| `uint x = 42;` | No — local variable |
| `someInternalHelper()` | No — internal function |
| `vm.label(addr, "token")` | No — cheatcode |

Cheatcodes (`vm.*`), pure Solidity operations (variable assignments, arithmetic, internal function calls), and view/pure external calls are all executed only during simulation and never produce transactions.

## Example: deploy and initialize

A realistic deploy script that creates a proxy and initializes it:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Script} from "forge-std/Script.sol";
import {MyToken} from "../src/MyToken.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";

contract DeployScript is Script {
    function run() external {
        address owner = vm.envAddress("OWNER");
        uint256 initialSupply = 1_000_000e18;

        vm.startBroadcast(vm.envUint("PRIVATE_KEY"));

        // tx 1: deploy implementation
        MyToken implementation = new MyToken();

        // tx 2: deploy proxy, pointing at implementation
        ERC1967Proxy proxy = new ERC1967Proxy(
            address(implementation),
            abi.encodeCall(MyToken.initialize, (owner, initialSupply))
        );

        vm.stopBroadcast();

        // This runs only in simulation — no transaction generated
        console.log("Proxy deployed at:", address(proxy));
    }
}
```

During simulation, Foundry executes the full script in one EVM context, so the `proxy` deployment can reference `address(implementation)` even though the implementation hasn't been deployed on-chain yet. After simulation passes, Foundry sends two separate transactions with consecutive nonces.

## The atomicity gap

The two-phase model creates a window where on-chain state can diverge from what was simulated. Consider:

1. Simulation succeeds against block N.
2. Between simulation and broadcast, someone else deploys a contract at the same `CREATE2` address.
3. Transaction 1 (the deploy) reverts on-chain.
4. Without `--slow`, transaction 2 was already sent and fails because it references a contract that was never deployed.

This is not a hypothetical — it comes up in practice on busy networks, especially with scripts that interact with shared protocol state ([AMM](/wiki/economics/finance/defi/amm) pools, governance contracts, registries).

### Achieving true atomicity

If multiple operations must succeed or fail together, the only solution is to execute them within a single transaction. Wrap the logic in a contract:

```solidity
contract AtomicDeployer {
    constructor(address owner, uint256 supply) {
        MyToken token = new MyToken();
        token.initialize(owner, supply);
        // If initialize reverts, the entire deployment reverts
    }
}
```

Now `forge script` produces one transaction — the `AtomicDeployer` constructor — and the deploy-then-initialize sequence is genuinely atomic. The tradeoff is that the deployer contract itself is deployed on-chain and consumes additional gas.

## Summary

| Aspect | Behavior |
|---|---|
| Simulation | Single EVM context; statements can reference each other |
| Broadcast | Each state-changing statement → separate transaction |
| Default mode | All transactions sent without waiting for confirmations |
| `--slow` mode | Waits for confirmation between transactions |
| Atomicity | Not guaranteed across transactions; use a wrapper contract if needed |
