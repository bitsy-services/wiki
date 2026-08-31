---
title: "Data Aggregators"
weight: 50
---

CoinGecko and CoinMarketCap are two websites, and registering with them is worth more than the traffic they send, because they are the upstream source for a long tail of software that never asks you for anything. MetaMask's token service, most portfolio trackers, tax tools, and the acceptance criteria of at least one major wallet registry all resolve token metadata through aggregator data. A logo submitted once here surfaces in a dozen places that have no submission form of their own.

The price of that leverage is that both require the token to be trading first.

## The trading prerequisite

CoinGecko will not list an asset that is not already trading on a venue it tracks. For a new token that means a pool on a tracked [decentralized exchange](/wiki/economics/finance/defi/dex) with enough [liquidity](/wiki/economics/finance/defi/liquidity-pool) and volume to look like a market rather than a placeholder. Seeding a pool with a few hundred dollars and applying the same day produces a rejection.

This is the dependency that sets the calendar for the whole registration effort: pool first, aggregators second, wallet registries third, and the aggregator review alone runs two to six weeks.

## CoinGecko

Submission is through the listing request form, and the specifics that get applications sent back are unglamorous:

- **Logo:** PNG at 200 × 200.
- **Contract address** for every chain, each one checksummed and matching a verified contract.
- **Supply:** total and circulating, with the vesting or lock schedule that accounts for the difference. An unexplained gap between the two is the most common reason for a follow-up email.
- **Description**, website, whitepaper, and social accounts with actual activity.

CoinGecko runs several distinct forms — new coin, information update, chain listing, exchange listing — and a submission on the wrong one is not rerouted. Their support directory lists them; pick from it rather than guessing.

## CoinMarketCap

Same shape, same 200 × 200 PNG, one form. Two of their stated rules are enforced rather than advisory: the form is the only channel, and reaching out by email or social media accelerates nothing. Priority also goes to complete submissions, so a form with three optional fields left blank sits behind the ones that are filled in.

CoinMarketCap carries a second-order consequence. Trust Wallet's asset criteria require a CoinMarketCap listing outright, so this submission is a precondition for the [wallet registries](/wiki/economics/finance/defi/token-registration/wallet-registries) rather than an end in itself.

## Dexscreener and DEXTools

These behave differently and are frequently misunderstood. Neither is a listing venue: both index pools automatically, so a pair appears within minutes of the pool being created, with no application and no fee. What they sell is the *profile* — the logo, description, website, and social links attached to that pair.

Dexscreener's Enhanced Token Info is a paid product on their marketplace, displayed at $299 as of August 2026, and it is one of the very few routes that will attach a logo to a token deployed the same week. DEXTools sells an equivalent update. Both are worth the money only in the specific case where a launch has real trading volume and the free registrars are still weeks out; neither confers anything the free routes will not eventually confer.

The blank grey circle on a Dexscreener pair is therefore not a signal about the token — it is a signal that nobody has paid $299 yet, and treating it as due diligence is a mistake in both directions.

## DefiLlama

DefiLlama tracks protocol total value locked (TVL) rather than tokens, and its registration route is a pull request against the adapters repository rather than a form: a small JavaScript module that reports your protocol's locked balances, plus a metadata entry carrying the name, logo, chain list, and links. It is free, it is reviewed by maintainers on GitHub, and it is the right destination once there is a protocol holding deposits rather than only a token trading in a pool.

## What to expect

| Registrar | Cost | Prerequisite | Typical wait |
| --- | --- | --- | --- |
| CoinGecko | free | trading on a tracked venue | 2–6 weeks |
| CoinMarketCap | free | trading, complete submission | weeks |
| Dexscreener pair | free | a pool exists | minutes |
| Dexscreener profile | $299 | a pool exists | days |
| DefiLlama | free | a protocol with deposits | days to weeks, review-dependent |

Submit to the free ones the day the pool has real depth, and treat the wait as the reason to have done the [self-service routes](/wiki/economics/finance/defi/token-registration/on-chain-metadata) first.
