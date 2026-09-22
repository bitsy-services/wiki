---
title: "Registering on ethereum-lists"
weight: 180
---

`ethereum-lists/tokens` is a community-maintained GitHub repository holding one JSON file per token per chain, named after the token's address. A build step assembles the files into combined lists, and hardware-wallet firmware and a few older wallets import the result. Adding a token is a pull request with one file: no fee, no holder count, no audit. The cost is pace and coverage. The last token pull request merged on 4 April 2026, and the repository knows sixteen chains, which include Ethereum, Arbitrum and BNB Smart Chain but not Base, OP Mainnet or Polygon.

## The file

The path is `tokens/<network>/<address>.json`, and the file for Uniswap's token reads:

```json
{
  "symbol": "UNI",
  "address": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
  "decimals": 18,
  "name": "Uniswap",
  "type": "ERC20",
  "ens_address": "",
  "website": "https://uniswap.org/",
  "logo": {
    "src": "https://assets.coingecko.com/coins/images/12504/large/uniswap-uni.png",
    "width": "250",
    "height": "250",
    "ipfs_hash": ""
  },
  "support": { "email": "", "url": "" },
  "social": {
    "blog": "https://uniswap.org/blog/",
    "chat": "https://discord.com/invite/XErMcTq",
    "twitter": "https://twitter.com/UniswapProtocol"
  }
}
```

The `social` object is trimmed here: the real file lists thirteen keys, most of them empty strings.

The repository's Kotlin checker is the authority on what the file may contain, and it is strict in both directions:

- **Mandatory:** `name`, `symbol`, `address`, `decimals`.
- **Optional:** `comment`, `logo`, `support`, `website`, `social`, `ens_address`, `deprecation`, `type`, `invalid_erc20_symbol`, `invalid_erc20_decimals`, `address_eip1191`, `red_flags`.
- **Allowed by one check, missing from the other:** `community`, `github`, `img-16x16` and `img-128x128` pass the key list but are not fields of the data model the file is parsed into, and that parser is set to fail on unknown fields. Leave them out; this was read from the code, not tested.
- **Anything else fails** both checks.

Rules on the values:

- `address` must be a valid checksummed address in the Ethereum Request for Comment (ERC) 55 mixed-case form, and the filename must be exactly that address plus `.json`.
- `decimals` must be a number, and `website` must match `^https?://.*\..*`.
- `logo` is an object whose `src` is a URL — the repository stores no images — and whose `width` and `height` are **strings**, not numbers. The README asks for a square PNG, 128 × 128 recommended, with a transparent background; nothing checks it.
- `support`, if present, must carry an `email`.
- `social` accepts `blog`, `chat`, `forum`, `discord`, `github`, `gitter`, `reddit`, `twitter`, `medium`, `tiktok`, `bitcointalk`, `slack`, `telegram`, `vimeo`, `youtube`, `instagram`, `linkedin` and `facebook`. The key is still `twitter`, not `x`.
- The field for an Ethereum Name Service name is `ens_address`.

Two places where the README and the checker's Kotlin code disagree, and the code decides: the README spells the red-flag field `redFlags` where the code accepts `red_flags`, and it lists `github` and `community` at the top level, where the repository's own test fixture puts `github` under `social` instead.

Continuous integration runs an on-chain check on every changed file, calling `decimals()` and `symbol()` on the contract and comparing them with the file. A token whose contract returns something unusual sets `invalid_erc20_decimals` or `invalid_erc20_symbol` to `true` to skip that comparison.

## Sixteen chains, fixed in code

The folder name maps to a chain ID through a table compiled into the build:

```text
eth 1     esn 2      rop 3     rin 4     gor 5     ubq 8
rsk 30    kov 42     bsc 56    etc 61    ella 64   sonic 146
arb 42161 avax 43114 zks 324   vc 207
```

The build exits with an error on any folder not in that table. Ethereum is `eth`, Arbitrum One is `arb` and BNB Smart Chain is `bsc`; there is no folder for Base, OP Mainnet or Polygon, and adding one means changing the Kotlin table in the same pull request. The most recent attempt at a new chain folder was merged in January 2026 with a failing build and reverted three months later.

## Pace

The repository is not archived, and dependency-update branches keep its push date current, but the history of the main branch tells the real story: the last token addition merged on 4 April 2026, the one before that in January, and the one before that in October 2025. Ten pull requests were open on 16 September 2026, and recent outside submissions showed failing checks or were waiting on first-time-contributor approval. A stale bot marks a pull request after 42 days without activity and closes it seven days later.

## Who reads it

The README's list of users is WallETH, MyCrypto, MyEtherWallet, Trezor, pyetherbalance and Rainbow's token list. Of the three checked, all have gone quiet — Rainbow's token list is archived, and WallETH and MyCrypto last saw a push in 2024. Trezor is the one that matters: its firmware repository still pulls `ethereum-lists/tokens` in as a submodule and names it "another source of tokens" beside CoinGecko, which it uses for most token data. No block explorer is named as a consumer.

That makes this a low-cost, low-value route: worth the half hour if the files are already assembled for [Trust Wallet](/wiki/economics/defi/token-registration/trust-wallet), not worth waiting on.

## One address on every chain

One file per chain folder, each with the same filename. Of Ethereum, Base, Arbitrum One, OP Mainnet, Polygon and BNB Smart Chain, only three can be submitted as the repository stands. The optional `address_eip1191` field holds the address in the chain-specific checksum format of [Ethereum Improvement Proposal (EIP)](/wiki/economics/defi/ethereum/eip) 1191, and the checker validates it against the folder's chain ID; for a same-address token it is, if set, the one field that differs between the files.

## Field map

What the file needs, against the [token property schema](/wiki/economics/defi/token-registration#the-token-property-schema):

| File field | Schema key | Notes |
| --- | --- | --- |
| filename, `address` | `address` | checksummed; one file per supported entry in `chain_ids` |
| `name` | `name` | |
| `symbol` | `symbol` | checked against the contract |
| `decimals` | `decimals` | checked against the contract |
| `type` | `standard` | `ERC20` |
| `website` | `website` | |
| `logo.src` | `logo_png` | a URL; `width` and `height` as strings |
| `support.email` | `email` | |
| `social.*` | `links.*` | `links.x` goes in `social.twitter` |
| `ens_address` | `ens` | |

## Check

```bash
curl -s https://raw.githubusercontent.com/ethereum-lists/tokens/master/tokens/eth/0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984.json
```

A 200 means the file is on the main branch. The path is case-sensitive, like the checksum it contains.
