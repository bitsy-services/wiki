---
title: "Registering on DEXTools"
weight: 120
---

DEXTools is a trading dashboard for [decentralized exchange (DEX)](/wiki/economics/defi/markets/dex) pairs. It does not list tokens in any sense a team applies for — "DEXTools does not 'list' tokens! but instead pulls data directly from the blockchain in real time" — so a pair appears as soon as the token trades on a supported exchange. The token's profile beside the pair — logo, banner, a 140-character description, categories and social links — comes either from CoinGecko, for tokens listed there, or from a paid marketplace order called *Token Info & Social Updates*, displayed at $195.

## Where a profile comes from

DEXTools copies CoinGecko. Its record for Uniswap's UNI names `coingecko: "uniswap"` as the source and carries CoinGecko's description and links on Ethereum, BNB Smart Chain, Arbitrum, OP Mainnet and Polygon, with no DEXTools order behind them. On Base, where [CoinGecko's record](/wiki/economics/defi/token-registration/coingecko) has no UNI address, the DEXTools profile is empty. DEXTools' own guide acknowledges the route: updating through "CoinGecko and Etherscan (and other block explorers) is still a viable choice", though slower to show.

The marketplace order is the direct route, and it has one hard limit: "you will only be able to update the data of tokens that do not yet have social information registered in DEXTools." A token that already has social information gets "The {{token}} token already has project information registered." Whether information copied from CoinGecko counts as registered for this check is not stated.

## The order form

The form, headed *Update your Token profile*, is the only channel DEXTools recognizes: "This is the only authorized method for updating information. Avoid scams." It needs a connected wallet, which becomes the account that owns the order.

| Field | Required | Rules | Schema key |
| --- | --- | --- | --- |
| Token | yes | selected by search; the chain follows | `chain_ids`, `address` |
| Your Telegram | yes | a username, "for contact only" | `contact_telegram` |
| Your email | no | for contact | `email` |
| Type of Update | yes | *New token update* or *Community Takeover* | — |
| links on the website | yes | confirm that every link submitted appears on the project website | — |
| Token Website | no | HTTPS only | `website` |
| Categories | no | up to three, from DEXTools' list | `category`, `labels` |
| Token Description | no | 140 characters at most | `tagline` |
| Circulating supply | no | a plain number; does not update itself | `circulating_supply` |
| Telegram, X | no | must match the project website | `links.telegram`, `links.x` |
| Project email | no | must match the project website | `email` |
| Discord, Instagram, TikTok, YouTube, Facebook, Reddit, Medium, GitHub | no | each must match the project website | `links.*` |
| Bitbucket | no | a repository link | `links.source_code` |
| CoinGecko, CoinMarketCap | no | listing links | built from `coingecko_id`, `coinmarketcap_id` |
| [non-fungible token (NFT)](/wiki/economics/defi/blockchain/nft) collection | no | a collection link | `links.opensea` |
| External Audit | no | a report link | `audits` |
| Logo | yes | 1:1, 200 × 200, 200 kB at most | `logo_png` at 200 × 200 |
| Banner | marked required | 3:1, 600 × 200, 2,000 kB at most | `banner` at 600 × 200 |
| trading-view image | no | 4:3, 1024 × 768, 1,000 kB at most | — |
| legal confirmations | yes | the images infringe no trademark and you hold the rights | — |

The schema keys refer to the [token property schema](/wiki/economics/defi/token-registration#the-token-property-schema). The limits are tight: 140 characters is less than half the 300 that Blockscout's form allows, which is why the schema carries a separate `tagline`, and the 200 kB logo limit is twice [Trust Wallet's](/wiki/economics/defi/token-registration/trust-wallet) and a small fraction of the megabytes [Dexscreener](/wiki/economics/defi/token-registration/dexscreener) and [GeckoTerminal](/wiki/economics/defi/token-registration/geckoterminal) accept.

## What is checked

The website is the only authority. "Fill the questionnaire with data from your official website"; "The DEXTools Tokenpair or Contract must be on the project website"; every social link "must match your project's website". The form warns that an order failing this "will be flagged and deleted and resubmission is required!"

Nothing refers to the contract's deployer, so a factory-deployed token should face no special obstacle, though no order was placed to test it. The connected wallet is an account, not a proof: "If you lose access to this wallet you will not be able to make changes unless you make a paid CTO claim" — a community takeover order, which is also the route for a new team taking over an abandoned token.

## Cost and wait

The form displays "Get it now for $195", and $95 for a token still on its launchpad's bonding curve — the stage where a launch platform sells the token at a price set by a formula, before any exchange pool exists. The amount actually charged is set by the server after the wallet connects and was not visible for this page; in DEXTools' 2023 campaign, Ethereum was priced higher than every other chain, so check the charge per chain before paying. Payment is by card, DEXTools' own DEXT token or other cryptocurrencies.

After the first update, "minor changes are free of charge", made from *My Orders*. A community takeover is not a minor change and is paid again. DEXTools' guide says updates for new tokens "may take 5-10 mins", and community takeovers wait for manual approval.

## One address on every chain

An order names one token on one chain, and DEXTools stores profiles per chain and address — UNI's profile exists on five chains and not on the sixth. A token on six chains is six orders unless CoinGecko fills them, and CoinGecko fills only the chains in its record.

| Chain | DEXTools chain |
| --- | --- |
| Ethereum | `ether` |
| Base | `base` |
| Arbitrum One | `arbitrum` |
| OP Mainnet | `optimism` |
| Polygon | `polygon` |
| BNB Smart Chain | `bsc` |

Ethereum is `ether` here, where Dexscreener and [DefiLlama](/wiki/economics/defi/token-registration/defillama) say `ethereum` and GeckoTerminal says `eth`.

## Check

There is no unauthenticated way to check from a script. DEXTools' pages and its internal data endpoint sit behind Cloudflare's bot protection, and the public API returns `{"message":"Forbidden"}` without a key. Open the pair in a browser — `https://www.dextools.io/app/en/<chain>/pair-explorer/<pair address>` — and look for the logo, banner and links in the token panel.
