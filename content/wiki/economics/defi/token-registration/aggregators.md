---
title: "Data Aggregators"
weight: 50
---

Market-data sites come in two kinds, and registering with each kind means something different. **Aggregators** — CoinGecko and CoinMarketCap — hold one reviewed record per asset, with every chain's contract address in it, and a token team applies for that record. **Pool trackers** — GeckoTerminal, Dexscreener and DEXTools — index trading pairs on decentralized exchanges automatically, one page per chain, and what a token team buys is the profile attached to a page. DefiLlama is a third case: it lists protocols by the value they hold, not tokens.

| Site | Automatic | What the team submits | Cost | Shape |
| --- | --- | --- | --- | --- |
| [CoinGecko](/wiki/economics/defi/token-registration/coingecko) | nothing | a listing request | free in up to 5 days; $1,000 for 24 hours | one record, all chains |
| [CoinMarketCap](/wiki/economics/defi/token-registration/coinmarketcap) | an unverified DexScan page — CoinMarketCap's automatic page — per pair | a listing request | free, "days to months/years"; USD 5,000 for about a business day | one record, all chains |
| [GeckoTerminal](/wiki/economics/defi/token-registration/geckoterminal) | a page per pool | token info, until CoinGecko lists the token | $199 per request | one per chain |
| [Dexscreener](/wiki/economics/defi/token-registration/dexscreener) | a page per pair, once it has a trade | Enhanced Token Info | $299 per order | one per chain |
| [DEXTools](/wiki/economics/defi/token-registration/dextools) | a page per pair | Token Info & Social Updates, unless CoinGecko already supplied it | $195 displayed | one per chain |
| [DefiLlama](/wiki/economics/defi/token-registration/defillama) | a price, if CoinGecko or a deep pool supplies one | a pull request for a protocol | no fee stated | one record, one token address |

For a token deployed on six chains the difference in shape is the difference between one application and six orders.

## The trading prerequisite

Every row starts with a market. CoinGecko requires a token to be "actively tradable on a cryptocurrency exchange tracked by CoinGecko", and CoinMarketCap's guideline for a tracked listing is active trading "on at least one (1) exchange (with material volume)". The pool trackers need a pool: Dexscreener lists a pair once it has "at least one transaction", and DEXTools once "your token is being traded". CoinGecko's own rejection guide says a token traded only on self-service venues may be turned down for "lack of liquidity", without publishing a number.

That sets the calendar for the whole registration effort — pool first, aggregators second, wallet registries third — and it is why the [self-service routes](/wiki/economics/defi/token-registration/on-chain-metadata) are worth doing before any of this.

## CoinGecko is upstream of most of the rest

A CoinGecko record is read, without any further submission, by:

- [Uniswap's interface](/wiki/economics/defi/token-registration/uniswap), for the logo;
- GeckoTerminal, which copies name, logo and links onto each chain in the record and then closes its own form;
- DEXTools, which shows CoinGecko-sourced profiles on the chains in the record;
- [Blockscout](/wiki/economics/defi/token-registration/blockscout), which "displays what CoinGecko returns";
- [MetaMask](/wiki/economics/defi/token-registration/metamask), as one of the lists it counts before detecting a token;
- DefiLlama, as the base of its prices.

Two qualifications. The copying is per chain: UNI's CoinGecko record has no Base address, and both GeckoTerminal and DEXTools show UNI on Base with no profile, so a record that omits a chain leaves that chain blank on the trackers that copy it. And Dexscreener is the exception: its documentation says it looks for token information in lists "such as CoinGecko's", but UNI, listed on CoinGecko, had no Dexscreener profile when checked.

So for a multi-chain token, the most valuable single submission is a CoinGecko listing with every chain in it, and the paid pool-tracker profiles are worth buying only for the weeks before that listing exists — or, for Dexscreener, for as long as the chart matters.
