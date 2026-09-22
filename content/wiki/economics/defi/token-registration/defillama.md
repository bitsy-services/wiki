---
title: "Registering on DefiLlama"
weight: 150
---

DefiLlama lists protocols, not tokens. A listing is a page showing a protocol's total value locked (TVL) — the value of the assets its contracts hold — and it is created by a pull request to the `DefiLlama/DefiLlama-Adapters` repository adding an *adapter*: a small JavaScript module that computes that value from on-chain data. The protocol's name, logo, links and token are not files in the pull request. They are answers to a questionnaire in the pull request's description, which DefiLlama's staff turn into the listing themselves. No fee appears anywhere in the documented process.

A token with no protocol behind it has no listing route here, unless it is a stablecoin or a real-world asset. What it can get is a price, which DefiLlama's price server derives on its own, and nothing about the name or logo.

## The adapter

The documented steps: fork the adapters repository, add a folder under `projects/` named for the project, write the adapter in it, and open a pull request. The adapter exports one key per chain, each holding a `tvl` function and optionally further categories such as `staking`, plus optional top-level `methodology` and `start` exports; `node test.js projects/<name>/index.js` runs it locally. Two rules decide more rejections than the code does:

- TVL "must be computed from blockchain data". Adapters that fetch a number from the project's own API are no longer accepted for new projects.
- No new npm dependencies, and no edits to `pnpm-lock.yaml`.

The README asks submitters to "enable 'Allow edits by maintainers'" and not to announce the pull request on Discord, because the queue is monitored. A bot comments with the TVL the adapter computes. No minimum is stated: a merged listing examined for this page showed about $470.

## The questionnaire

The pull request template's new-listing block, in order:

| Question | Schema key |
| --- | --- |
| Name (to be shown on DefiLlama) | `name` |
| Twitter Link | `links.x` |
| List of audit links if any | `audits` |
| Website Link | `website` |
| Logo (High resolution, will be shown with rounded borders) | `logo_png` |
| Current TVL | — |
| Treasury Addresses (if the protocol has treasury) | `locked_wallets` |
| Chain | `chain_ids` |
| Coingecko ID (leave empty if not listed) | `coingecko_id` |
| Coinmarketcap ID (leave empty if not listed) | `coinmarketcap_id` |
| Short Description (to be shown on DefiLlama) | `description` |
| Token address and ticker if any | `address`, `symbol` |
| Category (choose only one) | `category` |
| Oracle provider(s), implementation details, documentation | — |
| forkedFrom (does your project originate from another project) | — |
| methodology (what is being counted as TVL, how it is calculated) | — |
| Github org/user (optional) | `links.github` |
| Does this project have a referral program? | — |

The schema keys refer to the [token property schema](/wiki/economics/defi/token-registration#the-token-property-schema). Only audit links, treasury, the CoinGecko and CoinMarketCap IDs, the token and GitHub are marked as conditional or optional. Category comes from the list at defillama.com/categories, where the largest are `Dexs`, `Yield` and `Lending`.

How those answers are stored shows up in the public API. The `twitter` field is a bare handle with no `@` and no URL; `github` is a list of organisation or user names, not repository URLs; `gecko_id` and `cmcId` hold the aggregator IDs, the second as a numeric string such as `"7083"`.

**The logo.** The template's one line is the whole written requirement. Logos live in the `DefiLlama/icons` repository and are committed by DefiLlama staff, then served as lossless WebP from `icons.llamao.fi`. Of 88 icons added in the weeks before this was written, all were square and 66 were 400 × 400, most of them JPEG. Supply a square image at least 400 × 400, and do not rely on transparency, since most stored icons are JPEG. The site draws them with rounded corners.

## After the merge

The documentation asks for 24 hours before the listing appears. Measured over the 99 new-listing pull requests merged between 1 August and 15 September 2026, the median time from opening to merge was 22 hours, the 90th percentile about five days, and the slowest eleven days; four listings sampled appeared in the API between two and seven hours after merge.

Changes to a listing's metadata after that go by email to `metadata@defillama.com`, with "proof that the change is legitimate" — for a new website, a banner or redirect on the old one; for a new social handle, a post on the old handle announcing the move. One section of the documentation points to a web form instead; the email route is the one the README, the template and the dedicated documentation page all give.

## One address on every chain

A protocol entry has one `address` field holding one token on one chain. Ethereum addresses are written bare and every other chain is prefixed with DefiLlama's chain key — `base:0x…`, `arbitrum:0x…`. Across all 8,271 protocol entries no `address` holds more than one value: Aave V3 spans 21 chains and records one Ethereum address. A token deployed at the same address everywhere can be recorded here for one chain only, and which one is the staff's call.

The price server treats each chain separately even when the address is identical. It keys tokens as `<chain>:<address>`, and querying Ethereum's UNI address under `base:` returns nothing. The keys for the common chains:

| Chain | Chain key | Name in a protocol's `chains` list |
| --- | --- | --- |
| Ethereum | `ethereum` | `Ethereum` |
| Base | `base` | `Base` |
| Arbitrum One | `arbitrum` | `Arbitrum` |
| OP Mainnet | `optimism` | `Optimism` |
| Polygon | `polygon` | `Polygon` |
| BNB Smart Chain | `bsc` | `Binance` |

Avoid `op` for OP Mainnet. DefiLlama's own software development kit maps `op` to a different chain, ID 54, even though the price server happens to accept it.

## Tokens without a protocol

There is no form for registering a bare token. The price server's documentation says its base data is "prices pulled from coingecko", extended by pricing bridged copies from their origin chain and, as a last resort, by reading "the pool with most liquidity" on a handful of exchanges — and those last prices are only ingested with "sufficient liquidity" and carry a `confidence` score. So a token gets a DefiLlama price by being on [CoinGecko](/wiki/economics/defi/token-registration/coingecko) or by trading in a deep enough pool.

Two dashboards do list individual tokens, each with its own route and eligibility rules: stablecoins, by a pull request to `DefiLlama/peggedassets-server` with a folder named after the token's CoinGecko ID, and real-world assets (RWA), by a Google Form whose eligibility rules require an identifiable responsible entity and a live product.

## Check

A listed protocol:

```bash
curl -s https://api.llama.fi/protocol/uniswap | head -c 600
```

The response carries `logo`, `url`, `twitter` and `github`. The slug `uniswap` resolves to a parent entry; each version has its own slug, such as `uniswap-v3`.

A price, for any token:

```bash
curl -s "https://coins.llama.fi/prices/current/base:0xYourTokenAddress"
```

An unpriced token returns `{"coins":{}}` with status 200, not an error. A priced one returns `decimals`, `symbol`, `price`, `timestamp` and `confidence` — and no name or logo, which is the point of this page.
