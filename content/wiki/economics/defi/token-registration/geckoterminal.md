---
title: "Registering on GeckoTerminal"
weight: 100
---

GeckoTerminal is CoinGecko's tracker for decentralized exchange pools. It indexes pools on the exchanges it supports automatically and for free, so a token appears there — with a price chart and a trade history — once its first pool is on a supported exchange, and nobody has to apply. What a token team can submit is the *token info* attached to that token on one chain: logo, banner, description, website, social links and categories. As of September 2026 that submission costs $199 and is reviewed within 24 hours.

Once a token is listed on [CoinGecko](/wiki/economics/defi/token-registration/coingecko), GeckoTerminal stops taking token info for it and copies CoinGecko's instead. For most projects, then, GeckoTerminal's own form matters only in the gap between the first pool and the CoinGecko listing. [CoinGecko and GeckoTerminal](/wiki/economics/defi/token-registration/coingecko#coingecko-and-geckoterminal) sets the two side by side.

## Listing is automatic

GeckoTerminal's help centre puts it plainly: "listing on GeckoTerminal is FREE", and a token traded on a supported exchange can be found by searching its contract address. A freshly indexed token has a page and a pool, but its info is empty: no logo, no website, no description. A token that has never traded on a supported exchange has no page at all.

## The Update Token Info form

The *Update Token Info* button on a pool page leads to `https://www.geckoterminal.com/request-form/update-token`. CoinGecko's request-form menu at `https://partner.coingecko.com/request-form/new` also carries a *GeckoTerminal* tab. The fields, from the form itself:

| Field | Required | Rules | Schema key |
| --- | --- | --- | --- |
| Owner or Dev Telegram Handle | no | a handle, not a URL | `contact_telegram` |
| Project Name | yes | | `name` |
| Website | no | a URL | `website` |
| GeckoTerminal Link | yes | the URL of an existing pool, `https://www.geckoterminal.com/<network>/pools/<address>` | derived from `pools` |
| Network, Contract Address | yes | set from the pool; the address "is case-sensitive" | `address` |
| Icon Image | no | PNG or JPG, square, at least 30 px, under 2 MB | `logo_png` |
| Project Banner | only for a CoinGecko-listed token | PNG or JPG, at least 1280 × 430, under 2 MB | `banner` |
| Description | no | 2,000 characters at most | `description` |
| Category | no | up to five | `category`, `labels` |
| Social Links | no | handles, not URLs; see below | `links.*` |
| Additional Information | no | 2,000 characters at most | — |
| Linkback to GeckoTerminal | yes | yes or no | — |
| Acknowledgement | yes | the information is public on the project's site, and "the token CONTRACT must also be verified" | — |
| Email | yes | confirmed with a six-character one-time code | `email` |

The schema keys refer to the [token property schema](/wiki/economics/defi/token-registration#the-token-property-schema).

The social fields reject the URLs most people paste. Telegram, X, TikTok, Facebook, YouTube, Instagram, Medium and Reddit take a bare handle; GitHub takes an organisation or `org/repo`, not a link; Discord must be a `discord.gg/…` or `discord.com/invite/…` URL; Farcaster and Zora take profile URLs. A generator that stores full URLs under `links.*` has to strip them down for this form.

A community takeover — a new team taking over an abandoned token — is a toggle on the same form, and requires a written justification of up to 2,000 characters plus evidence.

## What the review checks

- **The address is published by the project.** "We require the contract address to be clearly listed on your official project website, official documentation, or verified social media profile."
- **The contract is verified.** The form requires it but does not define it; source verification on the chain's block explorer is the natural reading, and [block explorers](/wiki/economics/defi/token-registration/block-explorers) covers doing it.
- **The website and socials work** and carry adequate information.
- **A public verification post**, by the same procedure CoinGecko uses, is listed as a tip in the help article, though the form has no field for its link.

Nothing in the flow refers to the contract's deployer, so a token created by a factory contract should meet no special obstacle. The token info API does carry a `developer_address` field, which was empty for every token sampled, and GeckoTerminal does not document how it would attribute a factory deployment.

Rejection reasons, from the help article: the contract cannot be verified on the website or social media given; insufficient information; an inaccessible website or social profile; a recent duplicate request; the token already being on CoinGecko; rejected category tags.

## Cost and wait

The update article, revised on 9 September 2026, states that "GeckoTerminal Fast Pass is required" for a submission to be reviewed. The price is "$199 per request, excluding tax", paid in USDT or USDC, and each Fast Pass covers one request. A rejection still consumes it. GeckoTerminal says the only official paid route is a Fast Pass "purchased through the official GeckoTerminal website"; anyone else offering to update token info for a fee is not GeckoTerminal. The response comes by email "as fast as a few minutes and always within 24 hours". The form's code still contains a free *Regular Pass* with a five-day review, but it is switched off. An older help article about the verified badge still describes "standard processing" of three to five days, which predates the change.

The Fast Pass includes "a free CoinGecko listing evaluation": the token is assessed for CoinGecko at no extra cost. That is an evaluation, not a listing.

A token whose info has been reviewed carries a verified badge, and GeckoTerminal says only verified tokens appear in its trending cards.

## Once the token is on CoinGecko

GeckoTerminal "automatically tracks token information from CoinGecko", and the form locks. A CoinGecko-listed token sees an "Already on CoinGecko" notice, the logo, description, category and social fields are disabled, and the only thing left to submit is the banner. Name and ticker changes for any token go through a support ticket, not this form.

The copying runs one way. Information entered on GeckoTerminal does not flow to CoinGecko, and it does not reach Uniswap either: [registering on Uniswap](/wiki/economics/defi/token-registration/uniswap#geckoterminal-does-not-count) tested three tokens with GeckoTerminal-only logos and found none of them on Uniswap. GeckoTerminal's landing page says verified info puts a project "in front of apps like Rainbow, Uniswap, and Crypto.com" through its API; for Uniswap's interface the test says otherwise.

## One address on every chain

GeckoTerminal keys tokens by network and address — its identifiers read `eth_0x…`, `base_0x…` — so the same address on six chains is six separate token pages, each with its own info. A submission names one pool, which fixes one network, and one Fast Pass covers one request. A token on six chains that is not yet on CoinGecko therefore needs six submissions, $1,194 before tax; GeckoTerminal does not state this outright, but nothing in the form allows more than one network per request.

The cheaper route for a multi-chain token is the CoinGecko listing with every chain in its `platforms` map. GeckoTerminal then copies the info onto each chain's page, and only onto those: UNI's CoinGecko record omits Base, and GeckoTerminal's UNI page on Base has no logo.

GeckoTerminal's network identifiers differ from CoinGecko's:

| Chain | Chain ID | GeckoTerminal network |
| --- | --- | --- |
| Ethereum | 1 | `eth` |
| Base | 8453 | `base` |
| Arbitrum One | 42161 | `arbitrum` |
| OP Mainnet | 10 | `optimism` |
| Polygon | 137 | `polygon_pos` |
| BNB Smart Chain | 56 | `bsc` |

`polygon_pos` uses an underscore, while GeckoTerminal's identifier for Polygon zkEVM uses a hyphen, `polygon-zkevm`. `GET https://api.geckoterminal.com/api/v2/networks?page=1` returns the list a hundred at a time, with each network's CoinGecko platform identifier alongside; there were three pages and 229 networks, and a fourth page returns HTTP 400.

## Check

The info endpoint shows what GeckoTerminal will display:

```bash
curl -s https://api.geckoterminal.com/api/v2/networks/eth/tokens/0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984/info
```

Trimmed:

```json
{"data":{"id":"eth_0x1f9840a85d5af5bf1d1762f925bdaddc4201f984","type":"token","attributes":{
 "name":"Uniswap","symbol":"UNI",
 "image_url":"https://coin-images.coingecko.com/coins/images/12504/large/uniswap-logo.png?1720676669",
 "banner_image_url":null,"coingecko_coin_id":"uniswap","websites":["https://uniswap.org"],
 "twitter_handle":"Uniswap","gt_verified":true,"categories":["Defi"],
 "developer_address":null}}}
```

- A 404 means GeckoTerminal has never indexed the token on that network, usually because it has no pool on a supported exchange.
- A 200 with `image_url: null` and `gt_verified: false` means the token is indexed and has no info. A 200 on its own proves nothing.
- A non-null `coingecko_coin_id` means the info is coming from CoinGecko and the form is closed to you.

The public API is documented at 30 calls a minute and throttles bursts harder than that; a sixth call inside two seconds returned HTTP 429. Space calls a few seconds apart when checking several networks.
