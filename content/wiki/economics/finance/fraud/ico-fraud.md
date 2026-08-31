---
title: "Initial Coin Offering Fraud"
weight: 45
---

An initial coin offering (ICO) sells a token against a promise. The buyer sends ether to an address, a sale contract mints them a balance in a new [ERC-20](/wiki/economics/finance/defi/ethereum/erc-20) token, and what they hold afterwards is a ledger entry plus a document describing what the issuer intends to build. Nothing in the transaction obliges the issuer to build it, to hold the proceeds in escrow, to deliver on a date, or to return anything if they stop.

"ICO" names a period as much as a mechanism. Industry trackers put 2017–2018 sales above $20 billion across several thousand offerings, two of which — block.one's year-long EOS distribution and Telegram's private rounds — account for close to $6 billion of that between them. The failure rate was measured at the time, by studies measuring different things. Satis Group's July 2018 report classified offerings by lifecycle stage and put about 78% of them by count in an "identified scam" bucket, while noting those took a far smaller share of the dollars, since the largest sales were not the fraudulent ones. Benedetti and Kostovetsky's 2018 study tracked post-sale activity and found roughly half of projects showed no signs of life within four months. Intent at issuance and survival afterwards are separate questions, and no single percentage answers both.

## What replaced what

The structural comparison is with an initial public offering (IPO), where each component that an ICO dropped was doing a specific job.

A prospectus carries liability. Section 11 of the Securities Act makes the issuer, its directors, and its underwriters answerable for material misstatements in a registration statement without the buyer having to prove anyone lied deliberately. A whitepaper carries no liability at all, and enough of them were copied from other whitepapers that plagiarism detection became a standard first check.

An underwriter performs diligence and puts its own capital and franchise behind the offering. A Telegram group performs none, its moderators are paid by the issuer, and removing doubters is the job. Audited financial statements say what the company owns, owes, and spent, signed by a firm that can be sued for the signature; a GitHub repository shows only that code exists, not that it does what the whitepaper says, that anyone accountable controls the wallet holding the raise, or that the proceeds are still in it.

```text
  IPO component           ICO substitute       what was lost
  ----------------------  -------------------  --------------------------
  prospectus              whitepaper           liability for misstatement
  underwriter             Telegram group       third-party diligence
  audited financials      GitHub repository    verified use of proceeds
  escrow and lockups      none                 staged release of funds
  listing standards       permissionless pool  any gatekeeper at listing
```

## Degrees of fraud

Three cases look identical to a buyer at the moment of purchase and land very differently in court.

**Fabricated from the start.** No team, or a team of stock photographs, and a plagiarised whitepaper. This is theft wearing an offering's clothes, charged as wire fraud alongside securities fraud, and the easiest of the three to prove, because the misrepresentations are documentary: a listed advisor who never heard of the project, a partnership that does not exist.

**Real team, no ability to deliver.** Optimism about an unbuilt thing is not by itself fraud — the line is materiality plus knowledge, and a statement of belief about the future becomes actionable when the speaker knew the basis for it was false. Most of these resolve as unregistered-offering cases rather than fraud cases, because Section 5 liability does not require proving anybody lied.

**Real team, real product, wrong use of the money.** The offering said the raise would fund the protocol and it funded property, unrelated salaries, or the founders' own trading. Misappropriation against a stated use of proceeds is the strongest antifraud theory available, since the representation is specific, written, and falsifiable from bank records rather than from expert testimony about feasibility.

## Successor formats

Each successor moved the trust assumption somewhere else. None removed it.

The **initial exchange offering (IEO)** runs the sale on a centralized exchange that vets the project and lists the token. Trust moved to the exchange's diligence, which is funded by fees the issuer pays for the listing.

The **initial DEX offering (IDO)** runs the sale through a launchpad contract on a [decentralized exchange](/wiki/economics/finance/defi/dex), with the raise seeding a [liquidity pool](/wiki/economics/finance/defi/liquidity-pool). Trust moved to whoever controls that liquidity after the sale closes, which is exactly the [rug pull](/wiki/economics/finance/fraud/rug-pull) surface, and made [locked liquidity](/wiki/economics/finance/defi/locked-liquidity) a marketing feature.

The **simple agreement for future tokens (SAFT)**, proposed in 2017, sells an investment contract to accredited investors under a private-placement exemption and delivers the token later at network launch, on the theory that the delivered token is a functional good rather than a security. The theory has never succeeded in court; the Telegram case below is where a judge declined to sever the agreement from the token.

**Airdrops and points programs** dispense with a sale, so there is no offering to register: users are rewarded for usage with an allocation announced afterwards, on terms the issuer can change. Trust moved to an unenforceable expectation, which now does most of the work a token sale used to do.

## Cases

**Centra Tech (2017).** Raised roughly $25 million for a "Centra Card" said to run on the Visa and Mastercard networks. No such relationship existed, and the chief executive named in the company's materials was invented. Floyd Mayweather and Khaled Khaled settled SEC charges in November 2018 for promoting the sale without disclosing they were paid for it. Founders Sohrab Sharma, Robert Farkas, and Raymond Trapani were prosecuted in the Southern District of New York; Sharma pleaded guilty in 2020 and was sentenced to eight years in March 2021.

**OneCoin (2014–2017).** Sold "educational packages" bundled with tokens through a multi-level marketing network, and never had a blockchain: supply and price were rows in a database the operators controlled, which makes it the purest instance of the category, since the only thing sold was the claim. Prosecutors have described more than $4 billion taken in. Ruja Ignatova disappeared in October 2017 and was added to the FBI's Ten Most Wanted Fugitives list in 2022; she was removed from it in 2025, with the State Department reward still standing. Co-founder Sebastian Greenwood pleaded guilty and was sentenced to 20 years; Mark Scott, a former law-firm partner, was convicted in 2019 of laundering roughly $400 million of proceeds.

**Telegram (2018–2020).** Raised $1.7 billion from 171 initial purchasers in two private rounds to fund a network and issue a token called Gram, using purchase agreements sold under an accredited-investor exemption. Nobody alleged deception. The SEC sued in October 2019 on registration grounds alone, and in March 2020 the Southern District of New York granted a preliminary injunction, finding the SEC likely to succeed on the theory that the agreements and the Grams were parts of a single unregistered offering, so the planned resale of Grams into the public market was not a separate, exempt event. The case settled in June 2020 without a merits judgment. Telegram abandoned the project, returned most of the money, and paid an $18.5 million penalty.

## Where the law lands

The SEC's theory is registration first and deception second. Under *SEC v. W.J. Howey Co.* (1946), an investment contract exists where money is invested in a common enterprise with an expectation of profits derived from the efforts of others; the [DAO](/wiki/economics/finance/defi/dao) Report of July 2017 applied that to a token sale and stated that the federal securities laws apply to offers and sales of digital assets regardless of the terminology or the technology, which put every subsequent issuer on notice. Section 5 then makes an unregistered, unexempt offering unlawful on its own: no intent to deceive, no reliance, no injured buyer required.

An honest initial coin offering with a working product is unlawful in the United States if it was not registered and no exemption applied, and Telegram is the demonstration — money returned, penalty paid, nothing alleged about the truth of anything said. A fraudulent one is unlawful twice, under Section 5 and under the antifraud provisions (Section 17(a) of the Securities Act, and Section 10(b) with Rule 10b-5 of the Exchange Act), with wire fraud available on top. What that leaves a US resident able to buy is covered in [regulatory restrictions](/wiki/economics/finance/defi/defi-us-regulatory-restrictions) and [regulation](/wiki/economics/finance/regulation). A [pump and dump](/wiki/economics/finance/fraud/pump-and-dump) is what happened to a large fraction of the tokens that did reach an exchange, and an [exit scam](/wiki/economics/finance/fraud/exit-scam) is the same disappearance by an operator holding assets rather than selling a token.

## External links

- [SEC Report of Investigation: The DAO](https://www.sec.gov/litigation/investreport/34-81207.pdf) — the July 2017 report applying Howey to a token sale
- [SEC Framework for "Investment Contract" Analysis of Digital Assets](https://www.sec.gov/corpfin/framework-investment-contract-analysis-digital-assets) — staff guidance on how the Howey factors get applied to tokens
- [SEC press releases](https://www.sec.gov/newsroom/press-releases) — the Centra, Telegram and subsequent token-offering actions, with complaints attached
- [Justice Department press releases, Southern District of New York](https://www.justice.gov/usao-sdny/pr) — the Centra Tech and OneCoin prosecutions
- [FBI Ten Most Wanted Fugitives](https://www.fbi.gov/wanted/topten) — the list Ruja Ignatova was added to in 2022
