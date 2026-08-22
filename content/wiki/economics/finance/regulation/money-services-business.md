---
title: "Money Services Business"
weight: 50
---

A money services business (MSB) is the [Bank Secrecy Act](/wiki/economics/finance/regulation/bank-secrecy-act) category for a business that moves or converts value without being a bank. It matters here because it is the box almost every [cryptocurrency](/wiki/economics/finance/defi/cryptocurrency) business lands in, and because landing in it converts a software company into a regulated financial institution overnight.

## The categories

[FinCEN](/wiki/economics/finance/regulation/fincen) enumerates seven capacities at 31 CFR 1010.100(ff):

- **Money transmitter** — accepts currency, funds, or other value that substitutes for currency from one person and transmits it to another location or person. The broadest and most consequential of the seven, and the one nearly every crypto business lands in.
- **Dealer in foreign exchange** — exchanges the currency of one or more *countries* for another, above $1,000 per customer per day. The wording is why an exchanger of convertible virtual currency is not a dealer in foreign exchange: virtual currency is not the currency of a country, so the activity falls to money transmission instead.
- **Check casher**
- **Issuer or seller of traveler's checks or money orders**
- **Provider of prepaid access**, and separately **seller of prepaid access** — the stored-value categories, split into two capacities by the 2011 prepaid access rule.
- **The US Postal Service**

Money transmission has no *de minimis* threshold, and that is the asymmetry to notice. Dealers in foreign exchange, check cashers, and issuers or sellers of traveler's checks and money orders are caught only above $1,000 per person per day, and sellers of prepaid access only above $10,000. Money transmission has no such floor, so no volume of activity is small enough to fall outside it on size alone.

Size is not the same as scope, though. Three limitations run across the MSB definition as a whole:

- Banks and foreign banks are excluded.
- So is anyone registered with and functionally regulated or examined by the Securities and Exchange Commission (SEC) or the Commodity Futures Trading Commission (CFTC) — which is why a broker-dealer is not an MSB.
- So is a natural person conducting any of the first five activities on an infrequent basis and not for gain or profit.

The definition also reaches only businesses operating wholly or in substantial part within the United States. Several further carve-outs sit inside the money transmitter capacity specifically; the two builders actually reach for are payment processors, and transfers that are integral to the sale of goods or the provision of services.

## What being an MSB costs

Three separate burdens, and the first one is the smallest.

**Federal registration.** Register with FinCEN within 180 days of starting, renew every two years, and appear on a public register. It is a notification, not an approval, and it is cheap.

**A full BSA program.** Written policies, a designated compliance officer, ongoing training, independent testing, risk-based [KYC](/wiki/economics/finance/regulation/know-your-customer), transaction monitoring, and [Suspicious Activity Reports](/wiki/economics/finance/regulation/bank-secrecy-act#suspicious-activity-reports) at a $2,000 threshold — lower than the $5,000 that applies to banks. Records retained five years, and the [Travel Rule](/wiki/economics/finance/regulation/travel-rule) applied to qualifying transmittals.

**State money transmitter licensing.** This is the real barrier. Registration is federal, but *licensing* is state by state — roughly 50 jurisdictions, each with its own application, surety bond, minimum net worth requirement, examination schedule, and fee. Total cost to license nationwide is commonly quoted in the several millions of dollars and takes years. The Money Transmission Modernization Act, a model law adopted by a growing number of states, is an attempt at harmonisation, and it has helped at the margins without changing the shape of the problem.

Failing to hold a required licence is not merely a regulatory matter: 18 U.S.C. § 1960 makes operating an unlicensed money transmitting business a federal crime, and it does not require the government to prove the money was dirty.

## The control test

The question every crypto business asks is whether it is a transmitter. FinCEN answered the specific half in 2013, with the administrator/exchanger/user split; the 2019 guidance supplied the general principle underneath it, **independent control** over someone else's value.

- **Administrators and exchangers** of convertible virtual currency — anyone who issues and redeems it, or who exchanges it for fiat or other value on behalf of customers — are money transmitters.
- **Users** who obtain virtual currency to buy goods or services are not.
- **Custodial wallets** hold customer value and are transmitters. **Non-custodial wallets**, where the provider never holds the keys, are not — the 2019 guidance is explicit that a person who supplies only software, with no independent control, is not acting as a transmitter.

That last distinction is the load-bearing one for everything on this wiki, and it is under more strain in the courts than in the guidance. Prosecutions of privacy-tool developers have proceeded on the theory that facilitating transfers is enough regardless of custody, and a [DEX](/wiki/economics/finance/defi/dex) with an immutable [smart contract](/wiki/economics/finance/defi/smart-contract) has no operator who could register even if the theory were accepted. [DeFi and US regulatory restrictions](/wiki/economics/finance/defi/defi-us-regulatory-restrictions) covers the specific cases.

A related structural argument is that transmission means delivery to *another person*, so a service that only moves a user's own funds between their own accounts — the design [Interbox](/wiki/economics/finance/defi/interbox) rests on — is arguably not transmitting at all. The argument is a real one, but it is not a plain reading of the text: the definition says "to another **location or person**", and the regulation's explicit same-person carve-out covers only the *physical* transportation of currency, which implies the general case is otherwise in scope. Whether a same-person design sits outside money transmission turns on FinCEN administrative rulings and the specific facts, not on the words alone — and, either way, on the architecture genuinely enforcing the constraint.

## External links

- [31 CFR 1010.100(ff)](https://www.ecfr.gov/current/title-31/section-1010.100#p-1010.100(ff)) — the MSB definition
- [FinCEN MSB registration](https://www.fincen.gov/money-services-business-msb-registration) — how and when to register
- [FinCEN 2019 CVC guidance](https://www.fincen.gov/resources/statutes-regulations/guidance/application-fincens-regulations-certain-business-models) — the control test applied to crypto business models
- [CSBS Money Transmission Modernization Act](https://www.csbs.org/money-transmission-modernization-act) — the Conference of State Bank Supervisors' state harmonisation effort
