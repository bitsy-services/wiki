---
title: "Building Subgraphs"
weight: 10
---

## Subgraph Anatomy

A subgraph consists of three files:

1. **`subgraph.yaml`** — manifest listing the contracts, networks, start blocks, and event handlers.
2. **`schema.graphql`** — entity definitions that become your queryable data model.
3. **`src/mapping.ts`** — [AssemblyScript](https://www.assemblyscript.org/) handlers that transform raw events into entities.

## Scaffold and Deploy

```bash
# Install the CLI
npm install -g @graphprotocol/graph-cli

# Scaffold from an existing contract ABI
graph init --from-contract 0x1F98431c8aD98523631AE4a59f267346ea31F984 \
  --network mainnet --abi UniswapV3Factory.json my-subgraph

cd my-subgraph

# Generate AssemblyScript types from the schema
graph codegen

# Build
graph build

# Deploy to Subgraph Studio (requires auth)
graph auth --studio <DEPLOY_KEY>
graph deploy --studio my-subgraph
```

## Manifest (`subgraph.yaml`)

The manifest declares which contracts and events to index. A minimal example:

```yaml
specVersion: 0.0.5
schema:
  file: ./schema.graphql
dataSources:
  - kind: ethereum
    name: Factory
    network: mainnet
    source:
      address: "0x1F98431c8aD98523631AE4a59f267346ea31F984"
      abi: Factory
      startBlock: 12369621
    mapping:
      kind: ethereum/events
      apiVersion: 0.0.7
      language: wasm/assemblyscript
      entities:
        - Pool
      abis:
        - name: Factory
          file: ./abis/Factory.json
      eventHandlers:
        - event: PoolCreated(indexed address,indexed address,indexed uint24,int24,address)
          handler: handlePoolCreated
      file: ./src/mapping.ts
```

Always set `startBlock` to the contract's deployment block — omitting it forces a scan from genesis.

## Schema (`schema.graphql`)

Entities map to database tables. Each entity needs an `id` field of type `ID!`:

```graphql
type Pool @entity {
  id: ID!
  token0: Bytes!
  token1: Bytes!
  feeTier: BigInt!
  createdAt: BigInt!
}

type Swap @entity {
  id: ID!
  pool: Pool!
  sender: Bytes!
  amount0: BigDecimal!
  amount1: BigDecimal!
  timestamp: BigInt!
}
```

Use `@derivedFrom` for reverse lookups without storing redundant data:

```graphql
type Pool @entity {
  id: ID!
  swaps: [Swap!]! @derivedFrom(field: "pool")
}
```

## Mappings (`src/mapping.ts`)

Mapping handlers receive typed event objects and write entities to the store:

```typescript
import { PoolCreated } from "../generated/Factory/Factory";
import { Pool } from "../generated/schema";

export function handlePoolCreated(event: PoolCreated): void {
  let pool = new Pool(event.params.pool.toHexString());
  pool.token0 = event.params.token0;
  pool.token1 = event.params.token1;
  pool.feeTier = event.params.fee;
  pool.createdAt = event.block.timestamp;
  pool.save();
}
```

Run `graph codegen` after any schema or ABI change to regenerate the typed classes.

## Data Source Templates

For contracts created dynamically (e.g. a factory deploying pools), use **templates** so the subgraph starts indexing each new instance automatically:

```yaml
# In subgraph.yaml
templates:
  - kind: ethereum
    name: Pool
    network: mainnet
    source:
      abi: Pool
    mapping:
      kind: ethereum/events
      apiVersion: 0.0.7
      language: wasm/assemblyscript
      entities:
        - Swap
      abis:
        - name: Pool
          file: ./abis/Pool.json
      eventHandlers:
        - event: Swap(indexed address,indexed address,int256,int256,uint160,uint128,int24)
          handler: handleSwap
      file: ./src/pool.ts
```

Instantiate the template from a mapping:

```typescript
import { Pool as PoolTemplate } from "../generated/templates";

export function handlePoolCreated(event: PoolCreated): void {
  // ... create Pool entity ...
  PoolTemplate.create(event.params.pool);
}
```

## Testing

The [Matchstick](https://thegraph.com/docs/en/developing/unit-testing-framework/) framework provides unit testing for subgraph mappings:

```bash
npm install --save-dev matchstick-as
graph test
```

## Common Pitfalls

- **Forgetting `graph codegen`** after schema changes leads to stale types and confusing compile errors.
- **Large `BigDecimal` divisions** can overflow — use the `BigDecimal.div()` method and handle precision carefully.
- **Immutable entities** (`@entity(immutable: true)`) improve indexing performance for append-only data like swaps, but cannot be updated after creation.
- **Call handlers** are slower than event handlers and not supported on all networks — prefer events when possible.
