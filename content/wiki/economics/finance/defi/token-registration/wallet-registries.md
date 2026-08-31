---
title: "Wallet Registries"
weight: 60
---

Before token lists existed, wallets shipped their icons as a directory of files in a public repository, and adding a token meant opening a pull request. Two of those repositories still matter: `trustwallet/assets`, which is maintained and gatekept, and MetaMask's `contract-metadata`, which is frozen. Both are worth understanding mainly to know when to stop trying.

## `trustwallet/assets`

The repository is a directory tree keyed by chain and address:

```text
blockchains/
  ethereum/
    assets/
      0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984/
        logo.png
        info.json
```

The folder name is the [EIP](/wiki/economics/finance/defi/ethereum/eip)-55 checksummed address in mixed case. Lowercase is rejected by continuous integration before review, as is `logo.PNG` or `Info.JSON` — the checks are case-sensitive on both the extension and the filename.

`logo.png` must be 256 × 256, with a recommended ceiling of 100 kB and a transparent background. `info.json` looks like this, taken from the entry for Uniswap's own token:

```json
{
    "name": "Uniswap",
    "website": "https://uniswap.org",
    "description": "UNI is the Uniswap protocol token. Uniswap is a decentralized protocol for automated liquidity provision on Ethereum.",
    "explorer": "https://etherscan.io/token/0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
    "type": "ERC20",
    "symbol": "UNI",
    "decimals": 18,
    "status": "active",
    "id": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
    "tags": ["defi", "governance"],
    "links": [
        { "name": "x", "url": "https://x.com/UniswapProtocol" },
        { "name": "coingecko", "url": "https://coingecko.com/en/coins/uniswap/" }
    ]
}
```

`id` repeats the checksummed address and has to match the folder name exactly. The `links` array uses fixed key names — `x`, `discord`, `telegram`, `github`, `blog`, `coinmarketcap`, `coingecko` — and an unrecognized one fails validation.

### The acceptance bar

The file format takes an afternoon. The criteria exclude the entire category of tokens that most want the listing:

- A live website with a whitepaper covering roadmap, tokenomics, and use case.
- A completed audit by a recognized security firm.
- A CoinMarketCap listing for price tracking — so the [aggregator submission](/wiki/economics/finance/defi/token-registration/aggregators) is a prerequisite, and it has its own weeks-long queue.
- **A minimum of 10,000 holders and 15,000 transactions, with airdropped tokens excluded from the count.**
- A non-refundable processing fee, payable in BNB or Trust Wallet's own token.

The repository says it plainly: brand-new tokens are not accepted. Ten thousand non-airdropped holders is not a launch-week number for anything, so this route is a milestone to revisit rather than a step in a launch checklist — and the fee is charged whether or not the submission is accepted.

## MetaMask's `contract-metadata`

This repository mapped contract addresses to icons and was, for years, the way a token got a picture in MetaMask. It is now effectively frozen, and its documentation directs new tokens to [`wallet_watchAsset`](/wiki/economics/finance/defi/token-registration/on-chain-metadata#pushing-the-icon-at-the-wallet) instead. Opening a pull request against it is not a plan.

What replaced it is not another repository. MetaMask resolves token metadata through a service fed by the [data aggregators](/wiki/economics/finance/defi/token-registration/aggregators), which is why a CoinGecko listing puts a logo in MetaMask without anyone at MetaMask ever seeing a submission. The migration from a curated repository to an aggregated feed is the general direction of travel: the wallet stopped maintaining a list and started buying one.

## `ethereum-lists/tokens`

A community repository of token metadata, accepting free pull requests with no holder count or fee, and consumed by a handful of tools and explorers. It is a low-cost thing to do and a low-value one — worth an afternoon if you are already assembling the files, not worth waiting on.

## Where the effort belongs instead

For a token that launched this month, all three of these are closed or worthless, and the effort belongs in the routes that are open on day one: a [token list](/wiki/economics/finance/defi/token-registration/token-lists) you host, `wallet_watchAsset` in your own interface, and the [explorer update](/wiki/economics/finance/defi/token-registration/block-explorers). Revisit this page when the holder count is five digits.
