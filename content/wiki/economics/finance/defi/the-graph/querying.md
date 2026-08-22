---
title: "Querying Subgraphs"
weight: 20
---

Every deployed subgraph exposes a [GraphQL](https://en.wikipedia.org/wiki/GraphQL) endpoint. You can query it from any HTTP client — no special SDK is required.

## Endpoint URL

Decentralised network queries go through the Gateway:

```text
https://gateway.thegraph.com/api/<API_KEY>/subgraphs/id/<SUBGRAPH_ID>
```

- **API_KEY** — create one at [Subgraph Studio](https://thegraph.com/studio/).
- **SUBGRAPH_ID** — the deployment ID shown on [Graph Explorer](https://thegraph.com/explorer).

## Basic Query

Fetch recent swaps from the [Uniswap](/wiki/economics/finance/defi/uniswap) V3 subgraph:

```graphql
{
  swaps(first: 5, orderBy: timestamp, orderDirection: desc) {
    id
    timestamp
    pool {
      token0 { symbol }
      token1 { symbol }
    }
    amount0
    amount1
    amountUSD
  }
}
```

## TypeScript Client

The lightweight `graphql-request` library is a good default:

```typescript
import { request, gql } from "graphql-request";

const SUBGRAPH_URL =
  "https://gateway.thegraph.com/api/<API_KEY>/subgraphs/id/<SUBGRAPH_ID>";

const query = gql`
  {
    swaps(first: 5, orderBy: timestamp, orderDirection: desc) {
      id
      amountUSD
    }
  }
`;

const data = await request(SUBGRAPH_URL, query);
console.log(data.swaps);
```

For heavier use, consider [urql](https://formidable.com/open-source/urql/) or [Apollo Client](https://www.apollographql.com/docs/react/) which add caching and React integration.

## Filtering

The auto-generated `where` argument supports equality, comparison, and containment filters:

```graphql
{
  pools(where: { feeTier: 3000, totalValueLockedUSD_gt: "1000000" }) {
    id
    token0 { symbol }
    token1 { symbol }
    totalValueLockedUSD
  }
}
```

Suffix conventions: `_gt`, `_gte`, `_lt`, `_lte`, `_in`, `_not_in`, `_contains`, `_starts_with`.

## Pagination

Subgraphs cap results at **1 000 entities** per query. For larger datasets, paginate using `first` + `skip` or, for better performance, cursor-based pagination with `id_gt`:

```graphql
# Page 1
{ swaps(first: 1000, orderBy: id, orderDirection: asc) { id amountUSD } }

# Page 2 — use the last id from page 1
{ swaps(first: 1000, orderBy: id, orderDirection: asc, where: { id_gt: "<last_id>" }) { id amountUSD } }
```

Cursor-based pagination (`id_gt`) is faster than `skip` for deep pages.

## Time-Travel Queries

Query the subgraph state at a specific block with the `block` argument:

```graphql
{
  pool(id: "0x8ad599c...", block: { number: 17000000 }) {
    totalValueLockedUSD
  }
}
```

This is useful for building historical snapshots or comparing state across blocks.

## Full-Text Search

If the subgraph schema defines a `@fulltext` directive, you can search across text fields:

```graphql
{
  tokenSearch(text: "wrapped ether") {
    id
    symbol
    name
  }
}
```

Full-text search must be declared in `schema.graphql` at build time — it cannot be added at query time.

## Performance Tips

- **Request only the fields you need** — over-fetching nested relations is the most common cause of slow queries.
- **Cache on your backend** — the decentralised gateway charges per query. A short TTL (30–60 s) dramatically reduces costs for dashboards.
- **Batch related queries** into a single GraphQL request to reduce round trips.
- **Avoid deep `skip` pagination** — switch to `id_gt` cursors for datasets beyond a few thousand entities.
- **Use `_meta`** to check indexing status before trusting results:

```graphql
{
  _meta {
    block { number }
    hasIndexingErrors
  }
}
```

If `hasIndexingErrors` is `true`, the data may be incomplete.
