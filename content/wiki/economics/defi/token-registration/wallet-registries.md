---
title: "Wallet Registries"
weight: 60
---

Before token lists existed, wallets shipped their icons as a directory of files in a public repository, and adding a token meant opening a pull request against it. Three of those repositories still take submissions, and each now has its own page. They differ less in format than in who they let in:

| Registry | Channel | Cost | Bar to entry | Pace |
| --- | --- | --- | --- | --- |
| [Trust Wallet](/wiki/economics/defi/token-registration/trust-wallet) | pull request to `trustwallet/assets` | 500 TWT or 2.5 BNB per pull request | CoinMarketCap listing, audit, 10,000 holders and 15,000 transactions | human review after the fee is paid |
| [MetaMask](/wiki/economics/defi/token-registration/metamask) | pull request to `MetaMask/contract-metadata` | none | signs of activity, a website citing the address | 310 pull requests open; one outside submission took eight weeks |
| [ethereum-lists](/wiki/economics/defi/token-registration/ethereum-lists) | pull request to `ethereum-lists/tokens` | none | a valid file; sixteen chains only | months between merges |

All three key a token by its checksummed address inside a per-chain folder, so a token deployed at the same address on six chains is six sets of files, whichever registry takes it.

## Most of what a wallet shows is not in any of them

The direction of travel is away from curated repositories. MetaMask decides what to detect by counting how many third-party lists carry a token — swap routers, bridges, CoinGecko, CoinMarketCap, Trust Wallet, and its own repository among them — and its current code wants three. The sources carrying the most tokens are swap and bridge routers, whose inclusion rules were not examined, and a [CoinGecko listing](/wiki/economics/defi/token-registration/coingecko) is another. Each repository above is one input among many.

Trust Wallet is the exception: its repository is still the whole source for the logo it shows, and its entry bar is the highest.

## Where the effort belongs instead

For a token that launched this month, the Trust Wallet route is closed by its holder count, the MetaMask repository is a slow maybe, and `ethereum-lists` reaches few wallets and not every chain. The effort belongs in the routes that are open on day one: a [token list](/wiki/economics/defi/token-registration/token-lists) you host, [`wallet_watchAsset`](/wiki/economics/defi/token-registration/on-chain-metadata#pushing-the-icon-at-the-wallet) in your own interface, and the [explorer update](/wiki/economics/defi/token-registration/block-explorers). Revisit this page when the holder count is five digits.
