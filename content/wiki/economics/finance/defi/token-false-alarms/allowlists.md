---
title: "Allowlists"
weight: 40
---

Every heuristic in this section has exactly one reliable off-switch, and it is not a property of the contract. GoPlus's `trust_list`, honeypot.is's `very_low` band, RugCheck's silent exemption for USDC, MetaMask's `VERIFIED`, Uniswap's `SafetyLevel.Verified`, Jupiter's strict list — clean is membership. A token that satisfies every published criterion and is on no list stays flagged, and a token on the list stays clean whatever its bytecode says.

## Membership does not suppress the findings

The most common misreading is that an allowlist entry cancels the flags. It does not; it sits beside them, and the decision to suppress belongs to whoever renders the response.

USDT returns `trust_list: "1"` in the same object as six risk flags set to `1`. 1INCH returns `trust_list: "1"` alongside `honeypot_with_same_creator: "1"`. GoPlus's own instruction to suppress is attached to a different field — `is_in_cex`, whose notice reads "When `listed` is 1, other risk alerts can generally be ignored, and the token can be considered safe" — and even that is advice to the integrator rather than behaviour of the API.

Membership on 2026-08-31, Ethereum mainnet:

| `trust_list: "1"` | No `trust_list` |
| --- | --- |
| USDT, USDC, DAI, UNI, WBTC, 1INCH, ENS (the Ethereum Name Service token), COMP, LINK | stETH, wstETH, sDAI, AAVE, PEPE, PAXG |

Nothing about the second column explains it. It is not market capitalisation, age, exchange listing or proxy status — USDC is a proxy and has it; wstETH and sDAI are not proxies and do not. Three of the six are confounded by proxy suppression, since GoPlus ran few heuristics on them to begin with. wstETH and sDAI are the clean cases: full field sets returned, `is_mintable: "1"` unsuppressed, no allowlist entry to cancel it.

There is no documented way in. Enumerating GoPlus's entire fifty-seven-page documentation index yields no trust-list page, no application form, no appeal procedure and no criteria; the support page carries a rate limit and an email address. `is_in_cex` returned the identical two-name list — Binance and Coinbase — for every token that had it, which suggests a small hand-curated set rather than exchange data.

The same shape recurs. honeypot.is documents its best band as unreachable by construction: `very_low` is "Only whitelisted tokens can get this rating, such as WETH, USDC, USDT etc..." — so `low` is the ceiling for everyone else, and the vendor has said it intends to raise the bar for that too, possibly adding liquidity-lock and time-since-launch requirements. RugCheck's exemption is starker because it is silent: USDC's mint has both a mint authority and a freeze authority set on chain, the two properties that cost RENDER 75,000 risk points, and USDC returns an empty risks array with `validated: false`. RugCheck's own verification is therefore not the mechanism, no allowlist appears anywhere in its schema, and the exemption is simply unexplained.

Being on somebody else's list does not transfer. RENDER carries `jup_verified: true` and `jup_strict: true` and still scores 76.

## MetaMask counts sources, then does not

MetaMask says plainly that it keeps no list — "MetaMask doesn't maintain an authoritative list of tokens" — and that verification is earned rather than applied for: "MetaMask does not manually apply the verified token badge on an individual basis. In general, verification for a token can be achieved based on two metrics: The token is available on one or more recognized trading platforms; The token has demonstrated sufficient market activity."

What it actually does is count upstream occurrences. The client fetches `/tokens/{chainId}?occurrenceFloor={n}`, with `n` taken from a live endpoint that returned `3` for Ethereum mainnet and `1` for every newer chain on 2026-08-31, falling back to a hard-coded `3` for anything unlisted. Three independent sources must carry your token before the wallet displays it by default.

The floor is not enforced on either end. Requesting floors of 1, 3, 4, 6 and 10 all returned an identical response; a floor of 10 still returned entries with an occurrence count of 1; and the controller strips the `occurrences` field from its own type. There is no filter behind the parameter.

Which sources count is the more useful question, and the answer is unflattering to the curation layer. The heavy contributors are swap and bridge routing aggregators and price trackers — Rango, SonarWatch, CoinMarketCap, Li.Fi, CoinGecko — not wallet-curated lists. Uniswap's own default list appears on well under a quarter of one percent of mainnet entries in either sampling. Trust Wallet's contribution comes from a file whose timestamp reads November 2021. The practical route onto MetaMask's default display is being indexed by three bridge aggregators, which is not what "verified" suggests to a user reading the badge.

MetaMask's older on-repo allowlist is closed to newcomers and points at a dead link: `@metamask/contract-metadata` is marked effectively frozen, recommending instead that new tokens use the Ethereum Improvement Proposal (EIP) 747 wallet prompt — and its own link to the registration guide 404s.

## Uniswap: three gates, three owners

A token can be clean on every Blockaid check and still be unavailable in the Uniswap interface, because three independent mechanisms sit behind one product.

**The safety level** is a backend enum, not a token list the client parses. `getTokenListFromSafetyLevel` maps `Verified` to `Default` and *everything else* — including a token the backend has never heard of — to `NonDefault`. The web app no longer loads `tokens.uniswap.org` at all; its entire list-constants file is four lines naming a CoinGecko Avalanche fallback, and the code that resolved a list from an ENS contenthash is still there with no interface to point it at anything.

The rendering distinguishes two cases the enum does not. A token with no safety data produces no warning card at all; a token the backend declined to verify produces the card. So the warning means "we looked and did not verify", which is a narrower claim than it appears — and the string it renders is not a security finding: `{{tokenSymbol}} isn't traded on leading U.S. centralized exchanges.` The help centre defines the plain "Warning" label as "Token is not traded on a leading U.S. centralized exchange such as Coinbase, Kraken, or Gemini." Its severity is `Low`, the mildest non-zero rung. There is no appeal, because there is nothing to appeal: it is a listing fact.

**The Blockaid labels** — Malicious, Impersonator, Honeypot, Spam — are the security findings, and Uniswap disclaims both the ability to change them and any verification of them, in consecutive sentences: "Uniswap Labs is not able to adjust warnings on specific tokens." and "Blockaid is not an affiliate of Uniswap Labs, and Uniswap Labs does not independently verify information provided by Blockaid." Those go to `report.blockaid.io`.

**The Unsupported Token List** is a compliance decision, served at its own domain with 612 entries as of 2026-08-13, and it is the one gate with a real human appeal: email `compliance@uniswap.org` with "Appeal request" in the subject, naming the asset, contract address and reason, acknowledged within one business day. Its stated grounds are legal or regulatory action, fraud allegations by a major regulator, intellectual-property claims, and "technical, fraud, or other risks that could significantly affect user safety" — plus discretion. That fourth ground is broad enough to cover a genuine scam, so a third party reading the list as a risk signal is not simply wrong; what makes it a poor blocklist is the company it keeps, since its only tags are `synth`, `inverse` and `index` and its members include Synthetix synths and a tokenised index.

The default token list still exists as a GitHub repository, still merges additions, and still disclaims the queue in its own documentation: "Note filing an issue does not guarantee addition to this default token list. We do not review token addition requests in any particular order, and we do not guarantee that we will review your request." The queue visibly does not drain — roughly 1,400 issues open, the oldest token request dating from November 2019 — because that is not where the work happens. The repository's own agent-instruction file says requests come from tickets in a Linear project, and documents no editorial criteria at all: its quality checks are valid JSON, address validation, no duplicates, required fields, and the test suite. Whether a token deserves the list is decided somewhere with no public interface.

The issue template, meanwhile, still asks for a Uniswap **V2** pair address, and for a CoinMarketCap or CoinGecko link — which is where the circle closes.

## The circle

Follow each gate's prerequisites to the end and they refer to each other.

```text
MetaMask default display
   └─ 3 upstream sources carry the token
        └─ dominated by CoinMarketCap, CoinGecko and bridge aggregators
             └─ CoinGecko requires "actively tradable on an exchange tracked by CoinGecko"
                  └─ requires a pool with real depth
                       └─ scanners penalise thin liquidity and unrecognised lockers

Trust Wallet listing
   └─ 10,000 holders AND 15,000 transactions (airdrops excluded)
   └─ AND a completed audit by a reputable firm
   └─ AND listed on CoinMarketCap
   └─ AND 500 TWT (Trust Wallet Token) or 2.5 BNB per pull request, non-refundable, no guarantee

Uniswap default list
   └─ a CoinMarketCap or CoinGecko link
        └─ see above
```

Trust Wallet's is the hardest published number in the entire landscape, and it is honest about what it is: the documentation says the fee model "was partly inspired by the concept of a Token Curated Registry", the fee is owed again for a logo change, and inclusions the team initiates itself are free. Its repository states outright that "brand new tokens are not accepted". CoinGecko is the mildest gate — tradability on a tracked exchange, with no depth or holder threshold published — and sells a Fast Pass that "guarantees faster processing, but does not guarantee that your request will be approved", with no refund.

The one place the circle opens is the layer nobody uses. The Token Lists standard is permissionless by construction — "Anyone can create and maintain a token list, as long as they follow the specification" — the schema requires only a name, timestamp, version and token array, and publishing is described in [token lists](/wiki/economics/finance/defi/token-registration/token-lists). It has never left `1.0.0-beta.*` since its first publish in 2020, the featured registry at tokenlists.org was last touched in August 2024 and still advertises three endpoints that no longer resolve, and the Uniswap web app ships no interface for adding one. A self-published list is real, free, and read by almost nothing.

Jupiter, on Solana, is the exception worth naming: its free queue is ordered by submission age, trading volume and "Smart Likes" from wallets it classifies as smart, anyone can submit on any token's behalf — "This is not limited to project teams or token creators" — and it documents its own carve-out for the well-connected: "Exceptions can apply for specific cases, such as pre-launch tokens, stablecoins, or projects with strong institutional backing." That is the only free, community-actionable lever in the whole survey.

## What this means for a launch

The gating structure is the same one [token registration](/wiki/economics/finance/defi/token-registration#the-gating-structure) describes for logos, because it is the same set of companies. The difference is the consequence: an unregistered token shows a grey circle, while an unlisted token shows a warning. Both are cured by the same slow sequence — pool, then aggregators, then wallet registries — and neither is cured by anything in the contract.

Which leaves an honest summary for a deployer: the flags on the [capability](/wiki/economics/finance/defi/token-false-alarms/capability-flags) pages can be engineered away by deleting functions, and the ones on this page cannot be engineered at all. They are waited out.

## External links

- [GoPlus response details](https://docs.gopluslabs.io/reference/response-details) — `trust_list`, `is_in_cex` and `launchpad_token`, with no admission route for any of them
- [Uniswap token warnings](https://support.uniswap.org/hc/en-us/articles/8723118437133) — the eight labels and which are Blockaid's
- [Uniswap unsupported token policy](https://support.uniswap.org/hc/en-us/articles/18783694078989) — the four stated grounds, plus discretion
- [Trust Wallet asset requirements](https://developer.trustwallet.com/developer/new-asset/requirements) — 10,000 holders, 15,000 transactions, an audit and a CoinMarketCap listing
- [Trust Wallet pull-request fee](https://developer.trustwallet.com/developer/new-asset/pr-fee) — 500 TWT or 2.5 BNB, non-refundable
- [Token Lists](https://github.com/Uniswap/token-lists) — the permissionless standard, still in beta
- [Jupiter token verification](https://docs.jup.ag/user-docs/launch/vrfd/token-verification) — the one queue a community can push on
