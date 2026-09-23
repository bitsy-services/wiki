---
title: "Registering on CoinGecko"
weight: 130
---

A CoinGecko listing is a coin page: one record per asset, carrying a name, symbol, logo, description, links, supply figures, and a map from each blockchain the asset lives on to its contract address there. The record is created when a request form on CoinGecko's partner platform passes a staff review. Review is free and takes up to five days, or 24 hours for $1,000. There is one hard prerequisite: the token must already be trading on an exchange CoinGecko tracks.

The listing matters more than the traffic CoinGecko sends, because other software reads the record and asks the token team for nothing:

| Reader | What it takes from the CoinGecko record |
| --- | --- |
| [Uniswap](/wiki/economics/defi/token-registration/uniswap) | the logo, about 48 hours after CoinGecko has it |
| [GeckoTerminal](/wiki/economics/defi/token-registration/geckoterminal) | name, logo, description and links, on every chain in the record |
| [MetaMask](/wiki/economics/defi/token-registration/metamask) | one of the lists it counts before detecting a token |
| [DefiLlama](/wiki/economics/defi/token-registration/defillama) | the base of its price data |
| [Blockscout](/wiki/economics/defi/token-registration/blockscout) | project information, per Blockscout's documentation, on its instances for the chains in the record |
| [DEXTools](/wiki/economics/defi/token-registration/dextools) | description, links and logo, on the chains in the record |
| Trezor | "most of the info about networks and tokens", per its firmware documentation |

## CoinGecko and GeckoTerminal

[GeckoTerminal](/wiki/economics/defi/token-registration/geckoterminal) is CoinGecko's own tracker for decentralized exchange pools. The two share a company, a help centre, a review team — GeckoTerminal's verified badge means the information "has been verified by the CoinGecko team" — and a submission site, where GeckoTerminal is the second tab of the same request-form menu. They hold different things, and a token gets into each differently:

| | CoinGecko | GeckoTerminal |
| --- | --- | --- |
| What a page is | one reviewed record per asset, covering every chain | one page per token per chain, built from its pools |
| How a token gets one | a listing request, reviewed by staff | trading in a pool on a supported exchange; nobody applies |
| What the team submits | the listing itself | token info — logo, description, links — for one chain |
| Cost of a review | free, or $1,000 for 24 hours | $199 per request |
| Chain names | `ethereum`, `arbitrum-one`, `polygon-pos` | `eth`, `arbitrum`, `polygon_pos` |

Information flows one way between them. Once a token is on CoinGecko, GeckoTerminal copies the record's name, logo, description and links onto its page for each chain whose address is in the record, and its own form closes to everything except the banner. Nothing entered on GeckoTerminal travels up to CoinGecko, so none of it reaches the software that reads CoinGecko — [Uniswap's interface](/wiki/economics/defi/token-registration/uniswap#geckoterminal-does-not-count) included.

The two are also cross-referenced. A CoinGecko verification post should include the token's GeckoTerminal link if it has one; CoinGecko's API returns a GeckoTerminal URL for each chain in a record; and GeckoTerminal's $199 Fast Pass comes with "a free CoinGecko listing evaluation", which is an assessment and not a listing.

For a new token the order follows from that: a pool first, which puts the token on GeckoTerminal automatically; GeckoTerminal token info only if the chart page matters while the CoinGecko request is pending; then the CoinGecko listing with every chain in it, after which GeckoTerminal keeps itself up to date.

## Before the form

- **A CoinGecko account.** Every request goes through CoinGecko's partner platform at `partner.coingecko.com`, which requires a login.
- **Trading on a tracked exchange.** The listing guide says the token "must be actively tradable on a cryptocurrency exchange tracked by CoinGecko", and a request whose token shows no active trading "will automatically fail". For a new token that means a [decentralized exchange](/wiki/economics/defi/markets/dex) pool CoinGecko already indexes. The rejection guide adds that tokens "traded only on self-serviceable centralized/decentralized exchanges may be rejected due to security concerns and lack of liquidity", and that the evaluation weighs liquidity, team presence and maturity against "several other evaluation factors that are undisclosed". No numeric minimum is published.
- **A website the project owns**, with information on purpose, team and social accounts. CoinGecko's methodology page states that sites on website builders such as Wix "will not be accepted". CoinGecko asks that the website and documentation carry the same details as the request, including the contract address.
- **A working block explorer** and a clearly explained circulating supply — team, foundation, vesting and locked tokens.

The one exception to the trading rule is a **Preview Listing**, a separate listing type "for coins or tokens that haven't launched yet". It needs a token generation event (TGE) date — the date the token is first released to the public — backed by official announcements, and a preview-listed token shows no price data until it is activated later through the update form.

## The listing form

The request-form menu at `https://partner.coingecko.com/request-form/new` lists every request type under a *CoinGecko* tab and a *GeckoTerminal* tab. *CoinGecko → New Coin/ Token Listing*, also reachable directly at `https://partner.coingecko.com/request-form/coins/new`, opens a three-step wizard, *Basic Coin Information → Supply Information → Additional Information*, in sixteen numbered sections. The form sits behind a login and a bot challenge, so what follows comes from the screenshots in CoinGecko's own help articles, which show six of the sixteen sections. The rows without a section number are inferred from the update and migration forms, which share components, and their required flags were not visible — "not shown" below.

| Section | Field | Required | Schema key |
| --- | --- | --- | --- |
| 2 | Public Verification Link | yes | — (see below) |
| 2 | Launch Announcement link | preview listings only | — |
| contract rows | chain, contract address, Contract Decimal Places, one row per chain | decimals yes; the rest not shown | `chain_ids`, `address`, `decimals` |
| 4 | Exchange Name and Exchange Trade URL, one row per trading pair | yes | `pools` |
| 8 | Token Generation Date, or "Yet to be confirmed" | yes | `launch_date` |
| 8 | Max Supply Amount, or "Is Infinite Supply" | yes | `max_supply` |
| supply | circulating supply, vested and locked wallets | not shown | `circulating_supply`, `circulating_supply_api`, `locked_wallets` |
| basic information | name, symbol, description, website, whitepaper | not shown | `name`, `symbol`, `description`, `website`, `links.whitepaper` |
| 12 | X, Telegram, Facebook, YouTube, subreddit, Discord and Medium links, three "other" links | no | `links.*` |
| developer information | source code repositories | not shown | `links.github`, `links.source_code` |
| 15 | Token Image: PNG, JPG or WebP, 200 × 200, transparent background preferred | yes | `logo_png` |
| 15 | Project Banner Image: PNG or JPG, at least 1360 × 430, 2 MB at most | yes | `banner` |
| 16 | Remarks | no | — |

The schema keys refer to the [token property schema](/wiki/economics/defi/token-registration#the-token-property-schema).

Three details in the help text cause rejections on their own:

- **Decimals.** Decimals are entered per chain, and "submitting incorrect decimal data will result in your listing request being rejected."
- **Market links.** Exchange rows must link "the EXACT Link to the market pairs"; for an [automated market maker](/wiki/economics/defi/markets/amm), CoinGecko asks for the pair's analytics page, and an exchange missing from its search list is one it does not track, which ends the request.
- **Social links.** Facebook links must be Pages, not groups, and Discord links must be permanent vanity invitations, which a server gets only at boost level 3.

If circulating supply is published through an API, CoinGecko polls it every 30 minutes and requires plain HTTPS with no authentication and a JSON response. If the site sits behind Cloudflare's firewall, the firewall must allow requests carrying CoinGecko's two headers, `X-Requested-With: com.coingecko` and `User-Agent: CoinGecko +https://coingecko.com/`.

## Proving you speak for the project

CoinGecko's listing and verification guides never mention who deployed the contract, though its naming methodology defines a token's issuer as "the entity that deployed the token contract". What the guides ask for is proof through a social account, in a fixed sequence:

1. Post publicly from an official account that the project's website links to — X, Facebook or Instagram — stating the intent to submit a request to CoinGecko, with the token's GeckoTerminal link if it has one.
2. Paste the post's URL into *Public Verification Link* (or into *Additional Information* if the field is absent) and submit. The confirmation email carries a request identifier: `CL` and five digits for a listing, `CU` for an update, `CM` for a contract migration, `SU` for a supply update.
3. Reply to the post with that identifier.

The reply is the step that ties the form to the account; the verification guide calls it "crucial", and a missing post is a listed reason for rejection. For a token deployed through a factory contract, whose creator on some explorers is the factory, a check that never asks for the deployer is convenient. The verification guide asks instead that the website and documentation "reflect the same information included in your CoinGecko request", so the website should state the address, and every chain it is deployed on, in the project's own voice.

## Cost and wait

| | Regular Pass | Fast Pass |
| --- | --- | --- |
| New listing, tag update, contract migration | free, up to 5 days | $1,000 per request |
| Coin update — logo, links, description, new market, new chain | free, up to 5 days | $200 per request |

The listing itself is free under CoinGecko's listing terms, and a Fast Pass buys a faster decision, not a listing: CoinGecko says it "does not influence or guarantee the outcome". It is non-refundable, covers one request and only its first review round, and can be bought after submitting from the request's page. CoinGecko calls it its "only official paid service for expedited listing evaluations" and says third-party "listing services" are not authorised; anyone selling a faster listing is selling something else. A separate help article gives the regular wait as three to five working days and adds that a token not listed two weeks after applying "likely" failed the evaluation.

Two ways to lose a request after submitting it: a reviewer's "Action Needed" question left unanswered for three days rejects it automatically, and resubmitting because nothing has happened yet can be marked as spam. CoinGecko also warns that asking a community to press it with "When list?" messages can disqualify the token.

## Updating a listing

*Update Coin or Token Info*, in the same menu, opens with a choice of update type: logo; name or symbol; website, community, whitepaper or GitHub URLs; description; new market; new contract address on a new chain; category tag; community takeover; contract migration or rebrand; other. The guide asks for only the sections the chosen update needs — for a logo, just the *Attachments* section — and every update needs the same verification post as a listing. Name and symbol changes have their own update type, but for a full rebrand the dropdown says to choose *Other Requests*, while a separate form handles contract migrations.

[Registering on Uniswap](/wiki/economics/defi/token-registration/uniswap) describes the one downstream effect most projects are after: Uniswap copies the new logo about 48 hours after CoinGecko publishes it.

## One address on every chain

CoinGecko represents a natively multi-chain token as **one** coin whose `platforms` field maps each chain to that chain's contract address. A token at the same address everywhere is ordinary here: of the 21,245 coins in CoinGecko's list on 16 September 2026, 1,306 carried an identical address on two or more of Ethereum, Base, Arbitrum One, OP Mainnet, Polygon and BNB Smart Chain. Each chain is a row in the form with its own decimals, and a chain added after the listing is a *New Contract Address Addition* update, eligible for the $200 Fast Pass.

Three consequences follow from that representation:

- **Supply is summed.** CoinGecko's supply rules say that for a token issued natively on several chains, "Total Supply is the sum of the Total Supply from each native chain", with uncirculated wallets listed chain by chain. A design that mints a full supply on every chain shows the sum as its total supply regardless; listing each chain's locked or escrow wallets lowers only the circulating figure.
- **Every chain must be in the record.** GeckoTerminal copies CoinGecko's logo and links only for the chain and address pairs in `platforms`. UNI's CoinGecko record has no Base entry, and GeckoTerminal's page for UNI on Base shows no logo; UNI on Arbitrum, which is in the record, shows CoinGecko's logo.
- **Some bridged copies are different coins.** CoinGecko's articles, written about stablecoins, say bridged or wrapped copies "are listed separately as entirely new tokens" unless the issuer itself minted them. UNI's own record nonetheless holds its bridged addresses on Arbitrum, OP Mainnet, Polygon and BNB Smart Chain, so the line falls at who issued the copy rather than at bridging as such. A token the project deploys itself on every chain is on the native side of it.

The platform identifiers CoinGecko uses:

| Chain | Chain ID | CoinGecko platform |
| --- | --- | --- |
| Ethereum | 1 | `ethereum` |
| Base | 8453 | `base` |
| Arbitrum One | 42161 | `arbitrum-one` |
| OP Mainnet | 10 | `optimistic-ethereum` |
| Polygon | 137 | `polygon-pos` |
| BNB Smart Chain | 56 | `binance-smart-chain` |

`binancecoin` is not BNB Smart Chain; it is the retired BNB Beacon Chain.

## Why requests are rejected

CoinGecko's listing rejection headings, in its words: "Limited Cryptoasset Presence", "Insufficient Information on Cryptoasset", "Trademark Infringement / Inappropriate Content" — final, with no appeal — "Impersonations / Ticker or Name Conflict", "Malicious Application / Missing submitter's role", "Smart Contract Issues", "Rug-pull Risk" — unlocked liquidity, or no trading, the setup for a [rug pull](/wiki/economics/fraud/rug-pull) — and "Duplicated / Spam Request".

For updates the list is shorter: insufficient or incorrect information, the wrong form, a duplicate, a missing verification post, and "Potential mal-intent detected". Symbols cannot be reserved.

Separately from rejection, CoinGecko places notices on listed tokens whose contracts have an owner-controlled mint function or a variable transfer tax. Those are the same capability findings that [token false alarms](/wiki/economics/defi/token-false-alarms) covers.

## Check

The public API answers without a key:

```bash
curl -s https://api.coingecko.com/api/v3/coins/ethereum/contract/0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984
```

Replace `ethereum` with the platform identifier and the address with yours. A listed token returns the coin record, trimmed here:

```json
{
  "id": "uniswap", "symbol": "uni", "name": "Uniswap",
  "platforms": {
    "ethereum": "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984",
    "arbitrum-one": "0xfa7f8980b0f1e64a2062791cc3b0871572f1f7f0"
  },
  "image": {
    "large": "https://coin-images.coingecko.com/coins/images/12504/large/uniswap-logo.png?1720676669"
  },
  "preview_listing": false
}
```

An unlisted address returns HTTP 404 with `{"error":"coin not found"}`. Addresses come back in lowercase whatever the case of the request.

- `id` is the value for `coingecko_id` in the schema. DefiLlama's questionnaire asks for it directly, and the CoinGecko links other registrars want are built from it.
- `platforms` should list every chain the token is deployed on; a missing chain is a *New Contract Address Addition* away.
- `image.large` is the logo Uniswap will copy. Fetch it and look at it on a dark background before assuming the transparency survived.

To check many chains at once, `https://api.coingecko.com/api/v3/coins/list?include_platform=true` returns every coin with its `platforms` map, about 3.7 MB. Keyless requests are rate-limited per IP address.

The status of a submitted request is at `https://partner.coingecko.com/request-form/submissions`, under *Request & Listing*.

## External links

- [CoinGecko request-form menu](https://partner.coingecko.com/request-form/new) — every request type, including *Update Coin or Token Info*
- [New coin or token listing](https://partner.coingecko.com/request-form/coins/new) — the listing form itself
- [Contract migration or rebrand](https://partner.coingecko.com/request-form/coins/contract-migration/new)
- [Supply update](https://partner.coingecko.com/request-form/supply-update/new)
- [Submitted requests](https://partner.coingecko.com/request-form/submissions) — status of your requests
- [Support directory](https://support.coingecko.com/hc/en-us/articles/23960919544345-Support-Directory-CoinGecko-Request-Forms) — which form handles which request
- [Verification guide](https://support.coingecko.com/hc/en-us/articles/23725417857817) — the public post and request-ID reply
- [Fast Pass FAQ](https://support.coingecko.com/hc/en-us/articles/37297414892697-CoinGecko-Fast-Pass-Frequently-Asked-Questions) — prices and what a Fast Pass covers
- [GeckoTerminal token info form](https://www.geckoterminal.com/request-form/update-token) — for a token not yet on CoinGecko

