---
title: "Token Registration"
weight: 70
bookCollapseSection: true
---

[ERC-20](/wiki/economics/defi/ethereum/erc-20) specifies `name()`, `symbol()` and `decimals()`. It specifies no icon, no website, no description, and no way to record who deployed the contract. Every logo that has ever appeared beside a token balance came from an off-chain database keyed by chain identifier and contract address, maintained by a company with its own form, its own acceptance criteria, and its own queue.

So "registering a token" is not one action. It is a dozen submissions to organizations that mostly do not share data — where they do, it flows one way, outward from the two big aggregators and a few wallet lists — and most of them want a live market before they will look at a token. One, Trust Wallet, refuses brand-new tokens outright. The work splits cleanly in two: the parts you can do yourself on the day you deploy, and the parts that require somebody else to approve you.

## What each surface actually reads

| Surface | Where its icon comes from |
| --- | --- |
| [Uniswap](/wiki/economics/defi/token-registration/uniswap) | its own backend, which copies CoinGecko |
| Other swap interfaces | a [token list](/wiki/economics/defi/token-registration/token-lists) the user has enabled |
| MetaMask token detection | MetaMask's Token API, which [counts a dozen upstream lists](/wiki/economics/defi/token-registration/metamask) and wants three |
| MetaMask after [`wallet_watchAsset`](/wiki/economics/defi/token-registration/on-chain-metadata#pushing-the-icon-at-the-wallet) | the image URL your dapp passed in the prompt |
| Etherscan token page | [Etherscan's](/wiki/economics/defi/token-registration/etherscan) own submission form, once per chain |
| Blockscout explorers | CoinGecko's record, otherwise [Blockscout's](/wiki/economics/defi/token-registration/blockscout) own submission, once per instance |
| Trust Wallet | the [`trustwallet/assets`](/wiki/economics/defi/token-registration/trust-wallet) repository |
| [GeckoTerminal](/wiki/economics/defi/token-registration/geckoterminal) | its own paid form until the token is on CoinGecko, then CoinGecko's record |
| [Dexscreener](/wiki/economics/defi/token-registration/dexscreener) | its own paid profile, bought per chain; the trading pair appears automatically |
| [DEXTools](/wiki/economics/defi/token-registration/dextools) | CoinGecko's record on the chains in it, otherwise its own paid profile |
| CoinGecko, CoinMarketCap | [CoinGecko's](/wiki/economics/defi/token-registration/coingecko) and [CoinMarketCap's](/wiki/economics/defi/token-registration/coinmarketcap) listing forms |

The redundancy is the reason a token can carry a correct logo on Etherscan and a blank grey circle in a wallet on the same afternoon. What does propagate runs through a few hubs — CoinGecko's record above all, CoinMarketCap's for prices, and the lists MetaMask counts — and every other row is a separate application.

## The gating structure

Three prerequisites unlock most of the rest, and they unlock in a fixed order.

```text
  deploy
    │
    ├─ verify the source on the explorer ──► explorer token update (free)
    │                                        │
    │                                        └─► ownership proof reusable
    │                                            for later edits
    ├─ create a pool with real liquidity ──► Dexscreener / DEXTools listing
    │                                        (automatic; profile is paid)
    │                                        │
    │                                        └─► CoinGecko and CoinMarketCap
    │                                            will now accept a submission
    │                                            │
    │                                            └─► MetaMask, portfolio
    │                                                trackers, and the
    │                                                Trust Wallet criteria
    └─ publish a token list + wallet_watchAsset ──► works on day one,
                                                    asks nobody
```

CoinGecko requires the asset to be trading on a venue it already tracks, which for a new token means a [decentralized exchange](/wiki/economics/defi/dex) pool with non-trivial [liquidity](/wiki/economics/defi/liquidity-pool). Trust Wallet requires a CoinMarketCap listing plus 10,000 holders. That chain — pool, then aggregator, then wallet registry — is why the wallet-registry route is realistically months away from a launch, and why the self-service routes are worth doing first rather than last.

## Assemble the packet once

Every form below asks for the same nine things in a slightly different shape. Write them down before you open the first one, because several forms cannot be edited after submission. The [schema](#the-token-property-schema) that follows gives each of them a name a data file can use.

- **Contract address**, in [EIP-55](https://eips.ethereum.org/EIPS/eip-55) checksummed form, and the chain identifier (1 for Ethereum mainnet, 8453 for Base, and so on). EIP-55 encodes a checksum in the *letter casing* of the hex digits, which is why a checksummed address looks like a random mix of cases and why several registrars treat a case-only difference as a different string. `cast to-check-sum-address`, from the [Foundry](/wiki/economics/defi/solidity/foundry) toolkit, produces it.
- **Name, symbol, decimals**, exactly as the contract returns them. Several forms state a mismatch as a reason for rejection.
- **Logo**, in the several sizes and formats the registrars demand — see [making the icon](/wiki/economics/defi/token-registration/icon).
- **Description**, 2–4 sentences, written flat. Blockscout's form, and the companion sale form on Etherscan, ask for a neutral point of view with no unsubstantiated claims such as "first", "most" or "best".
- **Website**, live, on your own domain, with the contract address published on it. Reviewers check that the address on your site matches the one in the form; this is the cheapest anti-impersonation test they have.
- **Contact email at that domain.** Etherscan and Blockscout accept a free-mail address only if the website publishes it.
- **Social links** — X, Discord, Telegram, GitHub — that exist and have posts.
- **Supply figures**: total, circulating, and the vesting or lock schedule that explains the gap.
- **Audit report** and, if applicable, the [liquidity lock](/wiki/economics/defi/locked-liquidity) transaction.

## The token property schema

Every registrar asks for a subset of the same three dozen facts about a token, under its own labels. Recording them once, as one record per token with one key per fact, lets a single source produce the token's own web page, its token list entry, its [ERC-1046](/wiki/economics/defi/token-registration/on-chain-metadata) document — the JSON metadata file a contract can point to from a `tokenURI()` function — and the answers to every form below. The table after this one shows which registrar reads which key.

### Naming rules

Each key is valid, unchanged, as a JSON object key and as a key in a Markdown page's YAML front matter, and survives a static site generator reading either one. Five rules make that true:

- **Lowercase `snake_case`, starting with a letter.** [Hugo](/wiki/web/hugo) lowercases front matter keys and leaves data-file keys alone. Tested on Hugo 0.159: `logoURI` in front matter is stored as `logouri`, the same key in a JSON data file stays `logoURI`, and a lookup written for one misses the other. A key with no capitals is spelled the same way in both. Underscores rather than hyphens, because `links.source_code` works as a property path in both Go templates and JavaScript and `links.source-code` works in neither.
- **Not one of Hugo's own front matter fields**, unless the meaning is the same. `type` selects the page's layout and `url` moves the page — a token's standard is therefore `standard`, not `type`. `tags` and `categories` create taxonomy pages; the token's are `labels` and `category`. `description` is kept on purpose: it is the same thing, and Hugo puts it in the page's meta description.
- **Hex values and supplies are quoted strings.** A YAML parser reads an unquoted `0x10` as the integer 16. A 40-digit address survives unquoted only because it overflows a 64-bit integer, which is luck, not a rule. A supply with a fractional part, such as a circulating figure carried to 18 decimal places, cannot be held exactly by a JavaScript number.
- **Long text lives in the body.** `description_long` runs to hundreds of words, so in a Markdown file it is the page body below the front matter, and in a JSON file it is a string. Everything else, including the short prose of `team` and `traction`, stays in the front matter.
- **Nested only where the registrars nest.** Social and document links sit under `links`, named after the link names [Trust Wallet's](/wiki/economics/defi/token-registration/trust-wallet#infojson) validator accepts — fourteen of its sixteen, since its `coingecko` and `coinmarketcap` links are built from the ID keys — plus the extra networks other forms ask for. So `links.x`, not `twitter` or `x_url`. Each holds a full URL in the one spelling every validator accepts: `https://`, no `www.`, `https://x.com/…` rather than `twitter.com`, `https://discord.com/invite/…`, and a public `https://t.me/…` rather than an invitation. A form that wants a bare handle gets one cut from the URL. Lists of structured things — pools, locked wallets — are arrays of objects rather than maps keyed by chain ID, because a JSON object key must be a string and a YAML one need not be.

### Properties

| Key | Type | Holds |
| --- | --- | --- |
| `address` | string | the contract address in [EIP-55](https://eips.ethereum.org/EIPS/eip-55) checksummed form, identical on every chain |
| `chain_ids` | integer array | the chain ID of every chain the token is deployed on: `1` Ethereum, `8453` Base, `42161` Arbitrum One |
| `deployments` | object array | `{chain_id, deployer, tx_hash}` for each chain: the account that sent the deployment transaction — the creator Etherscan displays, and a signer Blockscout names — and so the likeliest account to sign an ownership proof |
| `name` | string | exactly what `name()` returns |
| `symbol` | string | exactly what `symbol()` returns; no whitespace, 20 characters at most |
| `decimals` | integer | exactly what `decimals()` returns |
| `standard` | string | the token interface, `erc20` |
| `token_uri` | string | the ERC-1046 metadata URI, if the contract has one |
| `tagline` | string | one line, 140 characters at most |
| `description` | string | one plain-text paragraph, 300 characters at most, no newlines, double spaces, URLs or superlatives |
| `description_long` | string | the full project description, 450 to 600 words, third person; in a Markdown file, the page body |
| `category` | string | one category, such as `DeFi` |
| `labels` | string array | tags from Trust Wallet's vocabulary: `defi`, `stablecoin`, `governance` |
| `logo_svg` | string | URL of the vector mark: paths only, no external references |
| `logo_png` | string | URL of the 256 × 256 PNG with transparency, under 100 kB, named `logo-256.png`; the other sizes sit beside it as `logo-<px>.png` |
| `banner` | string | URL of a 3:1 header image at 1500 × 500, PNG or JPG, under 2 MB; a 600 × 200 copy is rendered for DEXTools |
| `website` | string | the project's own site, which must publish `address`, every chain, and every link below |
| `email` | string | a contact address on the website's domain, or one the website publishes |
| `contact_telegram` | string | a Telegram username for an owner or developer |
| `links` | object | full URLs by name: `x`, `telegram`, `telegram_news`, `discord`, `github`, `source_code`, `whitepaper`, `docs`, `blog`, `medium`, `forum`, `reddit`, `youtube`, `facebook`, `instagram`, `tiktok`, `linkedin`, `slack`, `wechat`, `bitcointalk`, `opensea`, `farcaster`, `zora` |
| `audits` | string array | URLs of audit reports |
| `ens` | string | an Ethereum Name Service (ENS) name for the token or project |
| `country` | string | where most of the team is based |
| `team` | string | the team, backers and investors, as prose |
| `traction` | string | adoption, partnerships and shipped products, as prose |
| `launch_date` | string | ISO 8601 date of the token generation event (TGE) — its first public release |
| `max_supply` | string | whole tokens as a decimal string, or `infinite` |
| `total_supply` | string | whole tokens as a decimal string, summed across chains |
| `circulating_supply` | string | whole tokens as a decimal string, at the time of writing |
| `total_supply_api` | string | URL of an unauthenticated endpoint returning only the total supply |
| `circulating_supply_api` | string | URL of an unauthenticated endpoint returning only the circulating supply |
| `locked_wallets` | object array | `{chain_id, address, description, owner}` for each vesting, treasury or lock address |
| `pools` | object array | `{chain_id, dex, pool}` for each trading pool, where `pool` is an address or a pool ID |
| `token_list` | string | URL of the project's hosted [token list](/wiki/economics/defi/token-registration/token-lists) |
| `coingecko_id` | string | the CoinGecko coin ID, once listed, such as `uniswap` |
| `coinmarketcap_id` | integer | the CoinMarketCap ID, once listed, such as `7083` |
| `defillama_slug` | string | the DefiLlama protocol slug, once listed |

Everything a registrar wants that is not in the table is derived: another logo size is `logo_png` with `256` replaced — `logo-200.png` for CoinGecko and CoinMarketCap, `logo-512.png` for ERC-1046 — as [making the icon](/wiki/economics/defi/token-registration/icon#rasterizing) renders them, an explorer link is a host plus `address`, a CoinGecko link is a URL plus `coingecko_id`, a GeckoTerminal pool link is a network plus a `pools` entry, and a form that wants a bare handle gets one cut from the matching `links` URL. `category` and `labels` hold the project's own words, and each registrar with a fixed list needs a mapping onto it, the way chains do below: DefiLlama's largest category is `Dexs`, Blockscout, CoinMarketCap and DEXTools each have their own lists, and a token list's tag identifiers allow no hyphen and at most ten characters, so Trust Wallet labels such as `staking-native` and `deflationary` need renaming there. The three length-limited descriptions exist because the limits differ by more than a factor of ten: 140 characters on DEXTools, 300 on Blockscout, 450 words at the low end of CoinMarketCap's recommendation.

### Who asks for what

● required, ○ accepted. A blank means the registrar does not take the value. Uniswap has no column, because it takes nothing from the token team: it reads CoinGecko. A registrar's own sizes are noted where they differ from the key's.

Explorers and pool trackers:

| Key | [Etherscan](/wiki/economics/defi/token-registration/etherscan) | [Blockscout](/wiki/economics/defi/token-registration/blockscout) | [GeckoTerminal](/wiki/economics/defi/token-registration/geckoterminal) | [Dexscreener](/wiki/economics/defi/token-registration/dexscreener) | [DEXTools](/wiki/economics/defi/token-registration/dextools) |
| --- | --- | --- | --- | --- | --- |
| `address` | ● | ● | ● | ● | ● |
| `chain_ids` | ● a form per chain | ● a form per instance | ● a request per chain | ● an order per chain | ● an order per chain |
| `deployments` | ● the signer | ● the signer | | | |
| `name` | | ○ | ● | | |
| `tagline` | | | | | ○ |
| `description` | ● | ● | ○ | ○ | |
| `category` | ○ | ○ | ○ | | ○ |
| `labels` | | | ○ | | ○ |
| `logo_svg` | ● or `logo_png` | ● or `logo_png` | | | |
| `logo_png` | ● at 64 × 64 | ● at 48 × 48 | ○ | ● | ● at 200 × 200 |
| `banner` | | | ○ | ○ | ● at 600 × 200 |
| `website` | ● | ● | ○ | ○ | ○ |
| `email` | ● | ● | ● | | ○ |
| `contact_telegram` | | | ○ | | ● |
| `links` | ○ | ○ | ○ as handles | ○ | ○ |
| `audits` | | | | | ○ |
| `circulating_supply` | | | | | ○ |
| `locked_wallets` | | | | ○ | |
| `pools` | | | ● | | |
| `coingecko_id` | ○ | ○ | | | ○ |
| `coinmarketcap_id` | ○ | ○ | | | ○ |
| `defillama_slug` | | ○ | | | |

Aggregators, wallets, and the formats you publish yourself:

| Key | [CoinGecko](/wiki/economics/defi/token-registration/coingecko) | [CoinMarketCap](/wiki/economics/defi/token-registration/coinmarketcap) | [DefiLlama](/wiki/economics/defi/token-registration/defillama) | [MetaMask](/wiki/economics/defi/token-registration/metamask) | [Trust Wallet](/wiki/economics/defi/token-registration/trust-wallet) | [ethereum-lists](/wiki/economics/defi/token-registration/ethereum-lists) | [Token list](/wiki/economics/defi/token-registration/token-lists) | [ERC-1046](/wiki/economics/defi/token-registration/on-chain-metadata) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `address` | ● | ● | ○ one chain only | ● | ● | ● | ● | |
| `chain_ids` | ● one record | ● one record | ● | ● a file pair per chain | ● a folder per chain | ● three of the six chains | ● an entry per chain | |
| `name` | ● | ● | ● | ● | ● | ● | ● | ○ |
| `symbol` | ● | ● | ○ | ● | ● | ● | ● | ○ |
| `decimals` | ● per chain | ○ | | ● | ● | ● | ● | ○ |
| `standard` | | | | | ● derived from the chain | ○ | | |
| `tagline` | | ● | | | | | | |
| `description` | ● | | ● | | ● 600 bytes | | | ○ |
| `description_long` | | ● | | | | | | |
| `category` | ○ | ● | ● | | | | | |
| `labels` | | ○ | | | ● | | ○ | |
| `logo_svg` | | | | ● or `logo_png` | | | ○ | ○ |
| `logo_png` | ● at 200 × 200 | ● at 200 × 200 | ● square | ● | ● | ○ | ○ | ○ at 512 × 512 |
| `banner` | ● | | | | | | | ○ a 1080 × 566 crop |
| `website` | ● | ● | ● | ● | ● | ○ | | |
| `email` | | | | | | ○ | | |
| `links` | ○ | ● `x` and a chat | ● `x` | | ● | ○ | | |
| `audits` | | | ○ | | ● | | | |
| `ens` | | | | | | ○ | | |
| `country` | | ● | | | | | | |
| `team` | | ● | | | | | | |
| `traction` | | ● | | | | | | |
| `launch_date` | ● | ● | | | | | | |
| `max_supply` | ● | ● | | | | | | |
| `total_supply` | | ○ | | | | | | |
| `circulating_supply` | ○ | ● | | | | | | |
| `total_supply_api` | | ○ | | | | | | |
| `circulating_supply_api` | ○ | ○ | | | | | | |
| `locked_wallets` | ○ | ○ | ○ | | | | | |
| `pools` | ● | ○ | | | | | | |
| `coingecko_id` | | | ○ | | ○ | | | |
| `coinmarketcap_id` | | | ○ | | ● | | | |

Trust Wallet's `coinmarketcap_id` and `audits` are marked required because a CoinMarketCap listing and an audit are among its acceptance criteria, not because the file has fields for them; the CoinMarketCap link it produces is optional. CoinGecko's `name`, `symbol` and `description` are marked required on the strength of its update and migration forms; the listing form's own flags for them were not visible.

### One address on every chain

A token deployed through a deterministic factory — `CREATE2` from a fixed deployer, as [vanity addresses](/wiki/economics/defi/vanity-addresses#create2-salt-mining) describes — has the same `address` on every Ethereum Virtual Machine (EVM) chain. The schema takes advantage of that: `address` is a single string and `chain_ids` a list, with no per-chain address map to keep in sync. What does vary by chain is each registrar's name for the chain, and that belongs to the site, not the token. One table serves every token:

| Chain ID | Chain | Etherscan family | Blockscout | CoinGecko | CoinMarketCap | GeckoTerminal | Dexscreener | DEXTools | DefiLlama | Trust Wallet | ethereum-lists |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Ethereum | `etherscan.io` | `eth.blockscout.com` | `ethereum` | `1` | `eth` | `ethereum` | `ether` | `ethereum` | `ethereum` | `eth` |
| 8453 | Base | `basescan.org` | `base.blockscout.com` | `base` | `199` | `base` | `base` | `base` | `base` | `base` | — |
| 42161 | Arbitrum One | `arbiscan.io` | `arbitrum.blockscout.com` | `arbitrum-one` | `51` | `arbitrum` | `arbitrum` | `arbitrum` | `arbitrum` | `arbitrum` | `arb` |
| 10 | OP Mainnet | `optimistic.etherscan.io` | `explorer.optimism.io` | `optimistic-ethereum` | `42` | `optimism` | `optimism` | `optimism` | `optimism` | `optimism` | — |
| 137 | Polygon | `polygonscan.com` | `polygon.blockscout.com` | `polygon-pos` | `25` | `polygon_pos` | `polygon` | `polygon` | `polygon` | `polygon` | — |
| 56 | BNB Smart Chain | `bscscan.com` | — | `binance-smart-chain` | `14` | `bsc` | `bsc` | `bsc` | `bsc` | `smartchain` | `bsc` |

MetaMask needs no column: it keys by the chain ID itself, as `eip155:<chainId>`. The CoinMarketCap column is its platform ID, which is also the number at the front of each option in its form's platform list. A dash means the registrar has no entry for the chain.

The per-token values that do differ by chain are the ones that record something that happened on that chain — a pool, a locked wallet — and those carry their own `chain_id`.

The same address does not mean one submission. Registrars split into those that hold one record for the token and those that hold one per chain:

| One record, every chain in it | One submission per chain |
| --- | --- |
| CoinGecko, CoinMarketCap | Etherscan and each explorer in its family |
| DefiLlama, one record but a token address for one chain only | Blockscout, GeckoTerminal and DEXTools, for chains CoinGecko has not filled |
| | Dexscreener, always |
| | Trust Wallet, MetaMask and ethereum-lists, a folder or file per chain |
| | a token list, an entry per chain |

For the six chains above, that is six Etherscan-family forms, six Dexscreener orders at $299, and — unless a CoinGecko listing comes first — five Blockscout submissions, six GeckoTerminal requests at $199 and six DEXTools orders at $195, and six Trust Wallet folders that do not fit in one pull request. The one-record registrars are only as complete as the request: a chain missing from the CoinGecko record stays blank on every tracker that copies it.

### An example record

The same record as a Markdown page and as JSON. A Hugo site can read the first as a page and the second from `data/tokens/`, and a template finds the same key names in either:

```markdown
---
title: "Example Token"
address: "0xe1A00000000000000000000000000000000E1a00"
chain_ids: [1, 8453, 42161]
name: "Example Token"
symbol: "EXA"
decimals: 18
standard: "erc20"
tagline: "A collateral receipt redeemable 1:1."
description: "A collateral receipt redeemable 1:1 against its original asset."
category: "DeFi"
labels: ["defi"]
logo_svg: "https://example.org/tokens/exa/logo.svg"
logo_png: "https://example.org/tokens/exa/logo-256.png"
website: "https://example.org/tokens/exa/"
email: "tokens@example.org"
links:
  x: "https://x.com/example"
  github: "https://github.com/example"
max_supply: "1000000000"
launch_date: "2026-09-01"
pools:
  - { chain_id: 8453, dex: "uniswap-v4", pool: "0x…" }
coingecko_id: ""
---

The full project description goes here, as the page body.
```

```json
{
  "address": "0xe1A00000000000000000000000000000000E1a00",
  "chain_ids": [1, 8453, 42161],
  "name": "Example Token",
  "symbol": "EXA",
  "decimals": 18,
  "standard": "erc20",
  "tagline": "A collateral receipt redeemable 1:1.",
  "description": "A collateral receipt redeemable 1:1 against its original asset.",
  "category": "DeFi",
  "labels": ["defi"],
  "logo_svg": "https://example.org/tokens/exa/logo.svg",
  "logo_png": "https://example.org/tokens/exa/logo-256.png",
  "website": "https://example.org/tokens/exa/",
  "email": "tokens@example.org",
  "links": { "x": "https://x.com/example", "github": "https://github.com/example" },
  "max_supply": "1000000000",
  "launch_date": "2026-09-01",
  "pools": [
    { "chain_id": 8453, "dex": "uniswap-v4", "pool": "0x…" }
  ],
  "coingecko_id": "",
  "description_long": "The full project description goes here."
}
```

Every value is a placeholder, the address included: it is a made-up one with a valid checksum, and nothing is deployed there. `title` appears only in the front matter, because Hugo needs it for the page; a template can fall back to `name` where it is absent. A listing that has not happened yet is an empty string for the string IDs, as `coingecko_id` is here, or simply absent — `coinmarketcap_id`, an integer, has no empty form — so a template tests each ID for being set rather than for existing.

## Order of operations

1. Deploy, then **verify the source** on the block explorer for every chain you deployed to. Nothing else proceeds until this is done.
2. Render the icon assets and publish them at a stable URL — your own domain, [IPFS](/wiki/cs/ipfs), or [Arweave](/wiki/economics/defi/arweave). Etherscan, Blockscout and CoinMarketCap ask for a link; CoinGecko and the pool trackers take an upload, and Trust Wallet takes a committed file.
3. Publish a [token list](/wiki/economics/defi/token-registration/token-lists) at a URL you control, and wire `wallet_watchAsset` — the wallet method that prompts a user to add a token — into your own interface. Both work immediately.
4. Submit the explorer token update on [Etherscan](/wiki/economics/defi/token-registration/etherscan). Free, and once per chain. [Blockscout](/wiki/economics/defi/token-registration/blockscout) takes the same kind of submission, but may be filled from CoinGecko after step 5; submit now if its page matters before then.
5. Seed the pool — the [data aggregators](/wiki/economics/defi/token-registration/aggregators) all start from a market — then submit to [CoinGecko](/wiki/economics/defi/token-registration/coingecko) and [CoinMarketCap](/wiki/economics/defi/token-registration/coinmarketcap). CoinGecko reviews within five days for free, or within 24 hours for $1,000. A CoinGecko listing with every chain in it also fills in [GeckoTerminal](/wiki/economics/defi/token-registration/geckoterminal), [DEXTools](/wiki/economics/defi/token-registration/dextools) and Blockscout, and counts toward [MetaMask](/wiki/economics/defi/token-registration/metamask) detection. Blockscout's documentation says it shows what CoinGecko returns; check its project record after the listing before paying for a Blockscout review.
6. Once the holder and transaction counts qualify, submit to the [wallet registries](/wiki/economics/defi/token-registration/wallet-registries).

Consider putting the [ERC-1046](/wiki/economics/defi/token-registration/on-chain-metadata) `tokenURI` on the contract at step 1. It is one immutable string, it costs deployment gas and nothing else, and it is the only metadata that no company can revoke or lose.

## The part nobody's form fixes

Curated lists are also the entire defence against [fake tokens](/wiki/economics/fraud/fake-token): a contract can claim any name and symbol it likes, so a logo beside a balance is a statement about who filled in a form, not about who deployed the contract. Getting your own token registered raises the cost of impersonating it — an impostor now has to clear the same queues — but it does not stop one from being deployed. Identity remains the address.

The same companies run the scanners, and registration does not clear those either. [Token false alarms](/wiki/economics/defi/token-false-alarms) covers the other direction: what happens when an honest contract is flagged rather than merely unlabelled, and which of the queues above will hear an appeal.

## Wiki Pages

{{< section >}}
