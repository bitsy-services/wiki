---
title: "Registering on Dexscreener"
weight: 110
---

Dexscreener is a chart and pair tracker for [decentralized exchanges (DEXs)](/wiki/economics/defi/dex). It lists every pool on the exchanges it supports without an application — "as soon as they are added to a [liquidity pool](/wiki/economics/defi/liquidity-pool) and have at least one transaction" — so a token's price chart appears with no involvement from its team. What a team can buy is the token's profile: the icon, header image, description, website and social links shown beside the chart. The product is called Enhanced Token Info, it costs $299, and it is processed within minutes to twelve hours. It is one of the few routes that puts a logo beside a token in its first week.

## A profile is paid for, not inherited

Dexscreener's documentation says it "automatically looks for token information from external token lists, such as CoinGecko's". The live data does not bear that out for listed tokens: on 16 September 2026, Uniswap's UNI and Shiba Inu's SHIB, both [on CoinGecko](/wiki/economics/defi/token-registration/coingecko), had no Dexscreener profile on Ethereum, and Chainlink's LINK had one because someone had paid for it. Someone had also paid for a UNI profile in November 2025, and that order was cancelled.

The blank grey circle on a Dexscreener pair is therefore not a signal about the token. It means no profile order has been approved for that token on that chain.

## The order form

The order form sits on Dexscreener's marketplace and needs a signed-in account. Its fields, from the form's own validation code:

| Field | Required | Rules | Schema key |
| --- | --- | --- | --- |
| chain, token address | yes | one of each | `chain_ids`, `address` |
| Icon | yes | square, at least 100 px wide, PNG, JPG, WebP or GIF, 4.5 MB at most | `logo_png` |
| Header | no | 3:1, at least 600 px wide, same formats and size | `banner` |
| Description | no | plain text; URLs are rejected | `description` |
| Website | no | "should contain project address and links to socials"; not a social network, not `dextools.io` or `join.pump.fun` | `website` |
| Docs | no | same rules as Website | `links.docs` |
| X | no | an `x.com` or `twitter.com` profile | `links.x` |
| Telegram | no | a public link; invite links are rejected | `links.telegram` |
| Discord, TikTok, Instagram, Reddit, Farcaster | no | each on its own network's host | `links.*` |
| Additional links | no | up to five, each a label and a URL | `links.*` |
| Locked addresses | no | wallets holding locked supply — not [locked liquidity](/wiki/economics/defi/locked-liquidity), which the form warns against confusing; burn addresses are checked automatically | `locked_wallets` |
| Supply description | no | why and how supply is locked | — |
| two confirmations | yes | see below | — |

The schema keys refer to the [token property schema](/wiki/economics/defi/token-registration#the-token-property-schema). Telegram is the strictest: a `t.me/+…` or `joinchat` invitation fails with "Invite links are not allowed, please use a public link instead".

The two required confirmations are the whole of the ownership check: "I understand that all supplied data must be verifiable through official channels such as website and socials", and that Dexscreener "reserves the right to reject or modify the provided information." Nothing asks for a signature or refers to the contract's deployer, and a factory deployment has not been an obstacle — AIXBT on Base, a [clone](/wiki/economics/defi/permissionless-token-factory) created by a factory contract, has an approved profile. What the review checks is that the website publishes the token's address and links to the same socials.

## Before and after ordering

The form checks the token first. One Dexscreener has not yet seen is refused with a request to email support "before placing an order to ensure DEX Screener is able to support it". A token with a profile already is refused with a pointer to support or to the community takeover product, which lets a new team claim the profile of a token its original team abandoned.

That second refusal is also the only route for changes after purchase. There is no edit form: "To request changes within the token info or to enquire about other matters, please email us at support@dexscreener.com." Get the order right the first time.

Payment is by card or cryptocurrency. The price is displayed as $299, reduced from $499, and the page says "Most orders are processed within just a few minutes, but please allow up to 12 hours". Refunds must be requested within 14 days and cover only Dexscreener-side delay, double charges and cancellations; a pre-sale order for a token that never goes live is not refunded, though support may offer a credit.

## One address on every chain

An order carries one chain and one address, and a profile does not carry over to the same token elsewhere, even at an identical address. LayerZero's ZRO, at one address on every chain it uses, had a profile on Base, where an order was approved in February 2026, and on Arbitrum, but none on Ethereum, OP Mainnet, BNB Smart Chain or Polygon. A token on six chains that wants a logo on all six needs six orders, $1,794 at the displayed price. No multi-chain discount is advertised.

| Chain | Dexscreener chain ID |
| --- | --- |
| Ethereum | `ethereum` |
| Base | `base` |
| Arbitrum One | `arbitrum` |
| OP Mainnet | `optimism` |
| Polygon | `polygon` |
| BNB Smart Chain | `bsc` |

A wrong chain ID is not an error. The API answers HTTP 200 with an empty array, which looks exactly like an unindexed token.

## Check

The token endpoint returns the token's pairs, with an `info` object only when a profile exists:

```bash
curl -s "https://api.dexscreener.com/tokens/v1/ethereum/0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"
```

For UNI the pairs come back and `info` is absent. A profiled token's `info` carries `imageUrl`, `header`, `openGraph`, `websites` as label and URL pairs, and `socials` as type and URL pairs. This endpoint returned a single pair for UNI; `/token-pairs/v1/<chain>/<address>` returned thirty.

The order history shows whether a profile was bought and what became of it:

```bash
curl -s "https://api.dexscreener.com/orders/v1/ethereum/0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"
```

```json
{"orders":[{"chainId":"ethereum","tokenAddress":"0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984","type":"tokenProfile","status":"cancelled","paymentTimestamp":1762877217386}],"boosts":[]}
```

The live response is an object with `orders` and `boosts`, although Dexscreener's published API specification describes a bare array. `status` moves through `processing`, `on-hold`, `approved`, `rejected` and `cancelled`. `/orders` allows 60 requests a minute and `/tokens` 300.
