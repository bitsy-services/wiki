---
title: "Registering on CoinMarketCap"
weight: 140
---

CoinMarketCap (CMC) says "the majority of assets are now listed automatically": its DexScan service creates a page for each trading pair on a [decentralized exchange (DEX)](/wiki/economics/finance/defi/dex) from on-chain data, without a name check, a logo or a review. What a token team applies for is a **verified listing** — one reviewed coin page with a project name, logo, links, supply figures and every chain's contract address, identified by a Unified Cryptoasset ID (UCID). The application is a request form on CoinMarketCap's support site. The free route has, in CoinMarketCap's words, outcomes that "can range from days to months/years"; the paid one, CMC Priority (CMCP), costs USD 5,000 per page with a turnaround of about a business day.

The verified listing matters beyond CoinMarketCap. [Trust Wallet](/wiki/economics/finance/defi/token-registration/trust-wallet) requires one before it will accept a token, and names CoinMarketCap as its price source.

## DexScan already has the token

CoinMarketCap calls those automatic pages **unverified listings**: "DEX pair pages that are created through automated processes using on-chain data but have not been reviewed by CMC. Unverified listings may not contain information such as project name, websites, socials, and logos." A DexScan page can show a logo, but its own text says that "the logo and social links are from third-party sources" that CoinMarketCap has not verified, and it does not name those sources.

There is no DexScan profile form. Its page for an unverified token tells the owner to "apply for listing on CMC", which means the new-listing form below; that form suggests putting the DexScan page's URL in its *Website 2* field. Once a coin page is verified, its DexScan pages take the coin's logo and links.

CoinMarketCap describes four listing states besides the unverified one:

- **Verified** — "manually reviewed", with a UCID.
- **Preview or untracked** — does not meet the tracking guidelines but shows strengths in CoinMarketCap's evaluation; the form accepts `NA` as the contract address for a token with no contract yet.
- **Tracked** — "Will have a CMC Rank" and appears in CoinMarketCap's API. The guidelines for a tracked listing are a functional website and block explorer, active trading "on at least one (1) exchange (with material volume) that has tracked listing status on CoinMarketCap", and a reachable representative, and CoinMarketCap adds that "meeting them does not guarantee a listing."
- **Inactive.**

## The form

The submission site offers thirteen or more forms, and a request on the wrong one is dropped: "Applications that are submitted to the wrong option(s) on the form will be discarded." A new token uses form 1, **[New Listing] Add cryptoasset**, reached from `coinmarketcap.com/request/`. CoinMarketCap states the form is "the ONLY way" to request a listing and that reaching out by email or social media only gets you sent back to it.

Form 1 has 66 fields. The ones that matter, with their required flags as the form defines them:

| Field | Required | Rules | Schema key |
| --- | --- | --- | --- |
| Subject | yes | "[Project's full name] - [Symbol] - [Request]" | — |
| Relationship with the Project | yes | "CEO, founder, employee, community member" and so on | — |
| Project Launch Date | yes | `YYYY-MM-DD`, with evidence where possible | `launch_date` |
| Project Name | yes | the full name | `name` |
| Project Ticker/Symbol | yes | no `$` unless the ticker has one | `symbol` |
| Cryptoasset Tags | yes | from CoinMarketCap's list | `category`, `labels` |
| One-liner description | yes | "a snappy and concise tagline" | `tagline` |
| Detailed Project Description | yes | "Recommended word count: 450 - 600 words", third person, no hyperbole | `description_long` |
| Platform | yes | "all token platforms that the asset is currently on" | `chain_ids` |
| Link to Logo | yes | a URL, ideally ending `.png`; "(1) Transparent background; (2) Square (200x200); unequal dimensions will be rejected! (3) PNG format" | `logo_png` at 200 × 200 |
| Website 1 | yes | | `website` |
| Website 2 | no | the DexScan page is suggested | — |
| Platform and Contract Address 1 | yes | platform from a dropdown | `chain_ids`, `address` |
| Number of Decimals | no | | `decimals` |
| Block Explorer 1 | for trading tokens | an explorer URL containing the address | derived |
| Contract Addresses 2 and 3 | no | same shape as the first | `chain_ids`, `address` |
| Block Explorers 2–5 | no | comma-separated URLs containing the address | derived |
| Source Code, Whitepaper | no | | `links.github`, `links.whitepaper` |
| Announcement, Message Boards | no | | `links.bitcointalk`, `links.blog`, `links.medium` |
| Twitter | yes | | `links.x` |
| Chat 1 | yes | Discord, Telegram, Slack | `links.telegram` or `links.discord` |
| Reddit, Facebook, LinkedIn, Video Channel | no | | `links.*` |
| Circulating Supply | yes | the exact number of units | `circulating_supply` |
| Total Supply | no | | `total_supply` |
| Max Supply | yes | `0` if infinite | `max_supply` |
| supply API endpoints | no | each returning only the number | `total_supply_api`, `circulating_supply_api` |
| List of CMC-supported exchanges | no | pair URLs and screenshots | `pools` |
| CMC Priority | yes | yes or no | — |
| Country of Origin | yes | where most of the team is | `country` |
| Team/Backers/Investors | yes | | `team` |
| Traction/Adoption/Partnerships | yes | | `traction` |
| Rich list and reserve addresses | no | a spreadsheet template, used for ranking | `locked_wallets` |
| Proof/Supporting evidence | yes | "Please ensure that the requested updates match what is found on the project's website/social media accounts" | — |

The schema keys refer to the [token property schema](/wiki/economics/finance/defi/token-registration#the-token-property-schema). A block of optional fields — media coverage, emission schedule, sale dates — carries the note that they "could improve the chances of a free listing", and CoinMarketCap's criteria say complete submissions with evidence "will be prioritized for review".

## Proving you speak for the project

CoinMarketCap does not ask who deployed the contract. The form's verification step is a public post: "please make a public post using one of the accounts (e.g. social media) associated with the URLs found on the project's official website", mentioning the ticket number and the token's DexScan URL, and then give the post's URL. The form explains why: "This would prevent scammers from planting fake contract addresses." It also warns against tagging CoinMarketCap's own X account, because scammers watch those mentions for victims.

For paid requests the terms add that every requested update "must be visible on the project's official website/socials (especially contract address)", and that CoinMarketCap "will run the contract address through scanning tools".

None of this depends on the deployer, and a factory deployment has not blocked a listing in the one case checked: AIXBT on Base, a minimal-proxy clone — a tiny contract that forwards every call to shared code, stamped out by a [token factory](/wiki/economics/finance/defi/permissionless-token-factory) — holds a verified listing. The one visible effect is on DexScan, whose token record carries a creator field: for AIXBT it is empty, where for [Uniswap's](/wiki/economics/finance/defi/uniswap) directly deployed token it holds the deploying account, so DexScan's creator-based display came up blank for AIXBT.

## Cost and wait

| | Free | CMC Priority |
| --- | --- | --- |
| New listing or coin update | no fee; "days to months/years" | USD 5,000 per page, "~24 hr ETA (business days)" after payment |
| Circulating supply update | no fee | not sold |

Free-tier turnaround times "are highly variable and are not guaranteed, as there is an element of competitive benchmarking against other projects". CMC Priority is chosen with a yes on the form and paid by invoice. It covers up to twelve items per job: price, two websites, two block explorers, two contract addresses, two social URLs, technical documentation, maximum supply and total supply. CoinMarketCap will not sell anything that affects rank — "To avoid pay-2-win, we do not accept payment for rank-related updates" — so circulating supply stays on the free forms. A piecemeal follow-up may be billed as a new job, payments are non-refundable, and a pilot fast lane claims a listing "<2 hrs after payment is confirmed" for complete requests that reply with "Proceed with CMCP" and proof of control, and says it "works best on" Ethereum, Solana and BNB Smart Chain.

A rejection comes with no reasons owed: applicants accept that CoinMarketCap "is not obligated to inform me or provide any reasons for such refusal".

## Updating a listing

Form 7, **[Existing Cryptoasset] Update info**, handles logos, links, rebrands, tags and new contract addresses. It asks for the coin's CoinMarketCap URL — a token without one must go back to form 1 — a description of the change, and proof. Form 4 handles supply figures. A website change must explain why the old site cannot redirect to the new one, and URL updates are "delayed if we observe any incongruities".

## Rules that cost a listing

- Phishing emails and lookalike domains impersonate CoinMarketCap's listing team, and its staff never send the first direct message; a request for payment that did not come through the form's own invoice is not from CoinMarketCap.
- Duplicate requests and repeated status questions "will add to the queue and delay the process"; spamming the form can blacklist the project.
- "Attempting to bribe CMC staff will result in the blacklisting and delisting of the project."
- "Avoid piecemeal submissions."
- A listed token can be removed for low liquidity or suspicious trading, abandoned development, information that proves false, regulatory problems, or intellectual-property infringement.

## One address on every chain

A verified coin page holds every chain's contract address. LayerZero's ZRO, which sits at one address everywhere, is one page listing that address on seven chains. Form 1 has structured slots for three addresses; further chains go in the *Platform* text and as block explorer URLs, and chains added later are a form 7 update, or billable items in a CMC Priority job. The record is only as complete as the request: Uniswap's page lists UNI on Ethereum, BNB Smart Chain, Polygon and Arbitrum but not on Base or OP Mainnet, where UNI also trades.

DexScan stays per chain — one page per network and address — with a cross-chain block linking the pages that map to the same coin.

| Chain | Form dropdown | Platform ID | DexScan network |
| --- | --- | --- | --- |
| Ethereum | `1-Ethereum` | 1 | `ethereum` |
| Base | `199-Base` | 199 | `base` |
| Arbitrum One | `51-Arbitrum (Ethereum)` | 51 | `arbitrum` |
| OP Mainnet | `42-Optimism` | 42 | `optimism` |
| Polygon | `25-Polygon` | 25 | `polygon` |
| BNB Smart Chain | `14-BNB Smart Chain (BEP20)` | 14 | `bsc` |

## Check

CoinMarketCap's listing criteria link an API query that uses a key CoinMarketCap publishes for the purpose, `UNIFIED-CRYPTOASSET-INDEX`. It returns the ID of a tracked listing, which is the schema's `coinmarketcap_id`; a verified token still in preview may not appear:

```bash
curl -s "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?CMC_PRO_API_KEY=UNIFIED-CRYPTOASSET-INDEX&listing_status=active&symbol=UNI"
```

```json
{"data":[{"id":7083,"name":"Uniswap","symbol":"UNI","slug":"uniswap",
  "platform":{"id":1,"name":"Ethereum","token_address":"0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"}}]}
```

The response is trimmed; a symbol query can return several coins, so match on `token_address`. It is a shared key, offered as a courtesy.

A DexScan page shows what an unverified token displays: `https://dex.coinmarketcap.com/token/<network>/<address>/`, with the address in lowercase.
