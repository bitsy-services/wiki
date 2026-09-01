---
title: "Pump and Dump"
weight: 30
---

A pump and dump is an accumulation, a manufactured burst of buying, and an exit into that buying, run by the same person in that order. Nothing about the asset changes across the three steps: the price rises because order flow arrived on a book too thin to absorb it, and returns to roughly where it started once the flow stops and the organiser's supply meets it.

Congress wrote a prohibition on it into Section 9(a)(2) of the Securities Exchange Act in 1934, and the crypto version inherited the mechanics intact. A 1990s microcap boiler room bought a block of an obscure stock, put a floor of salespeople on the phones, and unloaded the block into the retail buying they generated. Permissionless issuance changed three inputs and none of the mechanics: creating the asset costs a few dollars of gas rather than a shell registration, the sales floor is a Telegram channel, and the accumulation happens on a public [blockchain](/wiki/economics/finance/defi/blockchain) where anyone can see it.

## Pool depth sets the size of the exit

The scheme requires a market too thin to absorb the organiser's exit at anything near the pumped price, and on a [decentralized exchange](/wiki/economics/finance/defi/dex) that thinness is a number anyone can read: the reserves in the [liquidity pool](/wiki/economics/finance/defi/liquidity-pool). Under the [constant product formula](/wiki/economics/finance/defi/constant-product-formula), price is the ratio of the two reserves and their product is fixed, so buying with a sum equal to the whole quote-side reserve doubles that side, halves the token side, and quadruples the price.

```text
Constant product pool, fees ignored.   x * y = k

start   25,000 USDC | 25,000,000 TOKEN     price $0.00100
        k = 6.25e11
        the organiser separately holds 10,000,000 TOKEN,
        acquired before any promotion

PUMP — the crowd buys with 25,000 USDC (one whole quote reserve)
  USDC    25,000 -> 50,000
  TOKEN   25,000,000 -> 6.25e11 / 50,000 = 12,500,000
  bought  12,500,000 at an average of $0.00200
  price   50,000 / 12,500,000 = $0.00400              4x

  buying m times the quote reserve multiplies price by (1 + m)^2
    m = 1 -> 4x      m = 3 -> 16x      m = 9 -> 100x

DUMP — the organiser sells 10,000,000 into the same pool
  TOKEN   12,500,000 -> 22,500,000
  USDC    6.25e11 / 22,500,000 = 27,778
  out     50,000 - 27,778 = 22,222 USDC
  price   27,778 / 22,500,000 = $0.00123

  quoted value of the stake at the peak      $40,000
  realised                                   $22,222
  ceiling on any exit, ever                  $50,000
                                             (the entire quote side)
```

Proceeds are bounded by the quote-side reserve, a small and knowable number, rather than by the market capitalisation, which is a multiplication and not a quantity of money. A one billion supply quoted at $0.004 prints a $4 million capitalisation against $50,000 of stablecoin in the pool. The shape scales: a launch showing a $500 million valuation over a pool holding $600,000 returns about a fifth of the notional on a sale of half a percent of supply, and takes the price down 96% doing it. Organisers avoid deeper pools because depth raises the cost of the pump more than it raises the proceeds of the dump.

## Organised pump groups

Telegram and Discord groups run the scheme as a recurring product on a published schedule. A coin is named at a fixed time, members buy on the announcement, and the price spikes and collapses within minutes. Jiahua Xu and Benjamin Livshits, at USENIX Security in 2019, collected hundreds of these events and found that the price typically peaks within seconds of the announcement and is back near its pre-announcement level within minutes — regularly enough that they built a model predicting which coin would be pumped next.

The announcement is tiered: organisers hold before anything is said, paying members are told seconds to minutes before free members, and free members are told last. Each tier's exit is the tier below it, so the paying members lose about as reliably as the free ones and have been charged as participants anyway. On-chain the same tiering reappears as transaction ordering, where priority is bought through [maximal extractable value](/wiki/economics/finance/defi/maximal-extractable-value) infrastructure instead of a subscription.

## Paid promotion

Section 17(b) of the Securities Act makes it unlawful to publicise a security for consideration from an issuer, underwriter or dealer without disclosing that consideration and its amount. It is a disclosure offence: the promotion need not be false, and the promoter need not have sold anything.

In November 2018 the Securities and Exchange Commission (SEC) settled Section 17(b) charges against Floyd Mayweather Jr. and the music producer Khaled Khaled over promotion of Centra Tech's [initial coin offering](/wiki/economics/finance/fraud/ico-fraud). Mayweather had taken $300,000 from three issuers including $100,000 from Centra Tech, Khaled $50,000 from Centra Tech, and neither disclosed it; they paid $600,000 and $150,000 in disgorgement and penalties plus interest, without admitting or denying the findings. In October 2022 Kim Kardashian settled the same charge over an Instagram post promoting EthereumMax, paying roughly $1.26 million against the $250,000 she had been paid, again without admitting or denying, and agreeing not to promote crypto asset securities for three years.

No settlement found that the promoted tokens were pumped. Section 17(b) reaches the silence about payment on its own, and it reaches only securities. Centra Tech itself was prosecuted separately as a fraud, and its founders were convicted — the touting cases were about the endorsement, not about the offering they endorsed.

## Insiders and snipers

The insider variant has a connected wallet accumulate before the promotion rather than after it: the deployer, the deployer's funder, or an address that received an allocation at launch. In the microcap era that accumulation surfaced only in discovery. On a public chain it is a matter of record, down to the block at which each large holder bought and the funding graph behind them.

Celebrity and political memecoin launches produce a repeatable signature in the first seconds of trading. A small set of wallets, funded from a common source within an hour or two of the launch, buys a large fraction of circulating supply in the launch block or the one after, at the bottom of a pool that is at its thinnest.

The `TRUMP` token, launched on Solana on 17 January 2025, placed roughly 80% of supply with entities affiliated with the issuer under a multi-year vesting schedule, and Chainalysis reported that the large majority of wallets which bought it lost money, with realised gains concentrated in a small number of early addresses. The `LIBRA` token, launched on 14 February 2025 and promoted in a post by Argentine President Javier Milei that was deleted hours later, reached a multi-billion-dollar nominal valuation and fell more than 90% the same day; on-chain analytics firms reported that a handful of connected wallets withdrew close to $100 million from the pools' liquidity positions. The `LIBRA` launch drew an Argentine judicial investigation and US class actions against the launch parties; nothing has been adjudicated in either. The chain establishes who bought when and who took out what, not who intended what, and that difference decides every charge below.

## How to tell

Before buying into anything with a promotion attached, in descending order of what it can cost:

1. **Sell a small amount first.** A contract that accepts buys and reverts sells is a [honeypot](/wiki/economics/finance/fraud/honeypot-token), and price analysis is irrelevant if the exit is closed.
2. **Check whether the liquidity can be withdrawn, and by whom.** Liquidity that is not locked or burned goes in one transaction, which is a [rug pull](/wiki/economics/finance/fraud/rug-pull) rather than a dump and takes the whole pool instead of half of it.
3. **Read the pool, not the market capitalisation.** The quote-side reserve divided by the headline valuation is the fraction of the notional that could be realised.
4. **Look at the top holders and their funding.** Wallets funded from one source shortly before launch, holding a large combined share, are the supply that will meet the promotion.
5. **Treat reported volume as unverified.** Volume is the cheapest number to fabricate; see [wash trading](/wiki/economics/finance/fraud/wash-trading).
6. **Look for the disclosure.** A promoter who was paid and says so is doing something legal.

Every one of those checks is also what an automated scanner runs, at scale and without judgment, which is why a large share of the tokens they flag are simply launches that failed rather than launches that lied — see [how often this is wrong](/wiki/economics/finance/defi/token-false-alarms/how-often-this-is-wrong) for what the base rates in the Chainalysis figures do and do not support.

## Where the law lands

Which statute applies depends on what the token is, which is the contested question. If it is a security, Section 10(b) of the Exchange Act and Rule 10b-5 reach the manipulation, Section 9(a)(2) reaches transactions effected to create actual or apparent active trading, and Section 17(b) reaches undisclosed paid promotion. If it is a commodity, Section 6(c)(1) of the Commodity Exchange Act and Commodity Futures Trading Commission (CFTC) Rule 180.1 reach manipulative and deceptive devices in the spot market, which is the provision the CFTC uses to reach spot crypto at all. If it is neither, what remains is wire fraud under 18 U.S.C. § 1343 — a scheme to defraud plus an interstate wire — which requires no view about the asset and is correspondingly the Department of Justice's preferred charge.

The classification moves. In February 2025 the SEC's Division of Corporation Finance published a staff statement taking the position that meme coins are generally not securities under the federal securities laws. Staff statements bind no court, but if that reading holds it removes Section 17(b) and Rule 10b-5 from exactly the launches where sniping is most visible, leaving statutes that require proof of deception rather than proof of manipulation. The boundary between the two agencies is covered in [US regulatory restrictions on DeFi](/wiki/economics/finance/defi/defi-us-regulatory-restrictions).

## External links

- [SEC press releases](https://www.sec.gov/newsroom/press-releases) — where the Section 17(b) touting settlements and the 2025 meme coin staff statement were published
- [CFTC press releases](https://www.cftc.gov/PressRoom/PressReleases) — enforcement actions asserting spot-market fraud jurisdiction over digital commodities
- [The Anatomy of a Cryptocurrency Pump-and-Dump Scheme](https://www.usenix.org/conference/usenixsecurity19/presentation/xu-jiahua) — Xu and Livshits at USENIX Security 2019: group structure, timing distributions, and a predictive model
- [FBI Internet Crime Complaint Center annual reports](https://www.ic3.gov/AnnualReport/Reports) — reported US losses by fraud category, updated yearly
