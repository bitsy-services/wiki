---
title: "Registering on Uniswap"
weight: 70
---

There is no Uniswap form for a token image. The logo beside a token on app.uniswap.org, the interface to the [Uniswap protocol](/wiki/economics/defi/uniswap), is a string called `project.logoUrl`. Uniswap's own backend hands it to the interface when the page loads, and it is copied from [CoinGecko](/wiki/economics/defi/token-registration/coingecko). Uniswap Labs states the rule in as many words: "Uniswap Labs sources token information and token logos from CoinGecko." Change the logo on CoinGecko, wait about 48 hours, and it changes on Uniswap.

That string is not read from the token's contract, and — though Uniswap wrote the [token list](/wiki/economics/defi/token-registration/token-lists) specification — it is not read from a token list either. Of 159 top-volume tokens sampled across Ethereum, Base and Arbitrum on 8 September 2026, 152 carried a CoinGecko logo URL and 7 a GitHub one. None carried a Uniswap-hosted one.

Registration on Uniswap is two separate things that a project staring at a blank grey circle usually takes for one. The **image** comes from CoinGecko and is obtainable. The **warning screen** a user must dismiss before swapping comes from a curated set that Uniswap Labs maintains internally, and is mostly not obtainable. Clearing one does nothing for the other.

## The four states

The backend answers unauthenticated requests, so the quickest way to see which state a token is in is to ask it the question the interface asks:

```bash
curl -s -X POST https://interface.gateway.uniswap.org/v1/graphql \
  -H 'content-type: application/json' \
  -H 'origin: https://app.uniswap.org' \
  -d '{"query":"query { token(chain: BASE, address: \"0x...\") { symbol project { logoUrl safetyLevel isSpam } protectionInfo { result attackTypes } } }"}'
```

`chain` takes `ETHEREUM`, `BASE`, `ARBITRUM` and the other supported network names; an address the backend has never indexed returns `"token": null` rather than an error. Three fields decide what a user sees, and they move independently:

| State | `logoUrl` | `safetyLevel` | `isSpam` | In the interface |
| --- | --- | --- | --- | --- |
| Deployed, not on CoinGecko | `null` | `null` | `true` | grey circle, *Spam token detected* |
| On GeckoTerminal, not CoinGecko | `null` | `null` | `true` | unchanged |
| On CoinGecko | CoinGecko URL | `MEDIUM_WARNING` or `STRONG_WARNING` | `false` | logo, *Not listed on leading U.S. exchanges* |
| In Uniswap's curated set | CoinGecko URL | `VERIFIED` | `false` | logo, no flag |

The interface collapses the two warning levels into one outcome. `getTokenListFromSafetyLevel` maps `VERIFIED` to `TokenList.Default` and `BLOCKED` to `TokenList.Blocked`, and everything else — both warning levels, and `null` — falls through a `default:` branch to `TokenList.NonDefault`, which is what raises the *Not listed on leading U.S. exchanges* flag. So `MEDIUM_WARNING` and `STRONG_WARNING` are indistinguishable to a user, and moving between them is not worth pursuing. Only reaching `VERIFIED` changes anything.

The enum is not the whole story, because the rendering draws a distinction it does not. A token the backend has never indexed carries no safety data and produces no warning card; a token it looked at and declined to verify produces the card. The warning means *we looked and did not verify*, which is a narrower claim than it appears. `BLOCKED` is the level no amount of listing reaches — a compliance decision served from a separate unsupported-token list, and the one gate here with a human appeal. [Allowlists](/wiki/economics/defi/token-false-alarms/allowlists#uniswap-three-gates-three-owners) takes all three gates apart.

A freshly deployed token sits in the first row before it has done anything at all: `isSpam: true`, and a verdict of `SPAM` from Blockaid, the screening vendor whose findings the interface renders. That is the default state rather than a finding about the contract, which is the shape of problem [token false alarms](/wiki/economics/defi/token-false-alarms) covers. Uniswap Labs states that it cannot adjust a Blockaid label, so the nominal remedy is a [mistake report to Blockaid](/wiki/economics/defi/token-false-alarms/clearing-a-flag). In the tokens sampled here the flag tracked the listing instead: every CoinGecko-listed token returned `false` and every unlisted one `true`.

## GeckoTerminal does not count

[GeckoTerminal](/wiki/economics/defi/token-registration/geckoterminal) is CoinGecko's [decentralized exchange](/wiki/economics/defi/dex) tracker. It indexes a new pool within minutes, it shows a chart immediately, and it accepts a logo and project details from the token team through *Update Token Info* on the pool page, reviewed within a day for $199. None of that reaches Uniswap.

Three tokens found trading on Base carrying a GeckoTerminal image and no CoinGecko listing each returned `logoUrl: null` from Uniswap's backend. The metadata flows one way between the two products: GeckoTerminal copies a CoinGecko listing's info, and GeckoTerminal's own documentation states the other side of it — "If the token is listed on CoinGecko, the token's info cannot be updated from GeckoTerminal." Nothing entered on GeckoTerminal travels up to CoinGecko, and Uniswap reads CoinGecko. GeckoTerminal's landing page does claim that verified info puts a project "in front of apps like Rainbow, Uniswap, and Crypto.com"; for Uniswap's interface, the three tokens above say otherwise.

The practical consequence is that the same-day route that looks like it should work is the one that does not. A GeckoTerminal profile is what a trader sees on the chart, which can be worth $199 while a CoinGecko listing is pending, but it is not a step toward a Uniswap logo.

## Getting the image: the CoinGecko listing

The image comes from a [CoinGecko listing](/wiki/economics/defi/token-registration/coingecko), which has its own page: the form, the verification post, the costs, and the multi-chain record. CoinGecko will not list an asset that is not already trading on a venue it tracks, so a pool with real [liquidity](/wiki/economics/defi/liquidity-pool) comes first. Three things from that page decide the Uniswap outcome:

- **The logo file** is a 200 × 200 PNG, JPG or WebP, transparent background preferred, uploaded in the form's *Attachments* section rather than fetched from a URL you host. It is one of the sizes [the icon page](/wiki/economics/defi/token-registration/icon) renders.
- **The verification post** — a public post from a social account the project's website links to, then a reply quoting the request identifier — is required on every listing and every update, and a missing one is a stated reason for rejection.
- **Cost and wait.** A regular review is free and takes up to five days. Fast Pass guarantees a review within 24 hours for $1,000 on a new listing, or $200 on an update such as a new logo. Neither buys a listing, only a decision. Then add Uniswap's own 48 hours of propagation before the image appears on app.uniswap.org.

For a token already listed on CoinGecko, changing the logo is the *Update Coin or Token Info* form with only the *Attachments* section filled in, and the same verification post is still required.

## The warning is a curation state, not a security finding

`safetyLevel` is not a verdict about the contract. Two tokens with real markets — `WNXM` on Ethereum and `DEGEN` on Base — both return `protectionInfo.result: BENIGN` with an empty `attackTypes` array while carrying `MEDIUM_WARNING` and `STRONG_WARNING` respectively. Blockaid finds nothing wrong with either. The warning reports that a token is outside Uniswap's curated set, and nothing more.

That set is closely related to the `Uniswap/default-token-list` repository, published at `tokens.uniswap.org` and still updated most weeks. Across 60 top-volume Ethereum tokens the correspondence was exact: all 32 on the list were `VERIFIED`, and none of the other 28 were. It is not a law, though. On Base, `AAVE`, `LINK`, `MORPHO` and `DUAL` are `VERIFIED` while absent from the list, and `DEGEN` is on the list and carries `STRONG_WARNING`. The list is the visible part of an internal set, not the set itself.

The repository documents one route in: file an issue from its token-request template. The queue behind that route is worth quoting in numbers. There are 1,291 open issues labelled `token request` against 220 closed, and the oldest still-open request was filed in November 2019. Meanwhile tokens are added most weeks — and every one of the 35 most recently merged additions was opened by Uniswap Labs staff or their automation, attributed in the pull request body to an internal Slack thread or a request sheet. None came from the public queue.

So the honest advice is that the badge is not something a project drives. File the issue, because it costs ten minutes and the alternative is nothing, and then plan on the warning being there.

## What Uniswap's interface no longer does

Publishing your own token list is still the right move for the reasons the [token lists](/wiki/economics/defi/token-registration/token-lists) page gives, but Uniswap's web interface is no longer one of the places it pays off. The interface used to accept a list URL under *Manage → Lists*; it does not now. In the current source, `tokens.uniswap.org` does not appear at all, `@uniswap/default-token-list` survives only in `package.json` and two test fixtures, and the one list still fetched at runtime is CoinGecko's Avalanche list, behind a comment reading "Lists we use as fallbacks on chains that our backend doesn't support" and a `TODO(WEB-3839): delete this when lists are removed from redux`. Token resolution moved to the backend, and the backend reads CoinGecko.

What still works without anyone's approval is the address. A user who pastes a contract address into the search field can find and swap the token today, warning screen and all, with no listing anywhere — the repository's own issue template opens by asking submitters to confirm they understand that "token listing is not required to use the Uniswap Interface with a token." A link into the interface with the token address in the URL is a launch-day route that asks permission from nobody, and it is the reason the [self-service registration routes](/wiki/economics/defi/token-registration/on-chain-metadata) are worth doing first. It is also the shape an impersonator uses, since a contract can claim any name and symbol it likes and only the address distinguishes it — so publish that link from somewhere a reader can already trust, and see [fake tokens](/wiki/economics/fraud/fake-token).

## Tokens launched through pools.trade

Uniswap's own launchpad, pools.trade, mints tokens on Robinhood Chain. Its metadata is fixed at creation: Uniswap Labs states that "tokens created via pools.trade cannot be changed after creation." There is no later correction through CoinGecko or anywhere else, so the name, symbol and image supplied at mint time are the permanent ones. Get them right before signing.

## Check

Confirm what the interface will actually render, rather than what you submitted. Replace the address below with your own — as written it queries UNI, which returns `VERIFIED` and will look like success:

```bash
curl -s -X POST https://interface.gateway.uniswap.org/v1/graphql \
  -H 'content-type: application/json' \
  -H 'origin: https://app.uniswap.org' \
  -d '{"query":"query { token(chain: ETHEREUM, address: \"0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984\") { symbol project { logoUrl safetyLevel isSpam } protectionInfo { result attackTypes } } }"}'
```

- `logoUrl` non-null and pointing at CoinGecko means the image has propagated. If CoinGecko shows the new logo and this still shows the old one, the 48 hours have not elapsed.
- `isSpam: false` means the Blockaid spam flag is gone. Every CoinGecko-listed token sampled returned `false` and every unlisted one `true`, so expect it to move with the listing rather than through a separate appeal.
- `safetyLevel: VERIFIED` is the only value that removes the warning flag. Anything else, including `MEDIUM_WARNING`, renders identically to a user.

Fetch the URL it returns before assuming it is right — CoinGecko serves a resized copy from its own domain, and a logo that was submitted with a flattened alpha channel arrives with the white box still in it.
