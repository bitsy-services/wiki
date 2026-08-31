---
title: "Cashing Out"
weight: 115
---

Stolen crypto is a number in a public database. It buys nothing and pays no rent, so every fraud upstream of this page — the [rug pull](/wiki/economics/finance/fraud/rug-pull), the [pig butchering](/wiki/economics/finance/fraud/pig-butchering) portfolio, the drained wallet — is unrealised until the balance becomes currency, and that conversion means touching a regulated institution or a person willing to stand in for one. That requirement is the whole enforcement surface, and it is where most crypto prosecutions are built. Several of the best-known laundering techniques now buy time rather than anonymity.

## Placement, layering, integration

The classical [anti-money laundering](/wiki/economics/finance/regulation/anti-money-laundering) frame splits laundering into placement, layering, and integration. Crypto inverts the first: placement is already done, because the proceeds arrive natively in a system that accepts them without introduction. The work concentrates in layering, and the difficulty concentrates at the exit, where the chain meets a bank.

```text
victim wallet
  |  authorized transfer, or a signature the victim did not understand
  v
collection wallet                      one address per campaign
  |  consolidation, then 20-50 hops in uneven amounts
  v
bridge to another chain                breaks same-chain tracing
  |
  v
mixer, or swaps through a decentralized exchange
  |  withdrawal size and timing chosen to blend into the pool
  v
deposit address at an exchange, owned by a nested service
  |  the exchange sees the nested service, not the underlying customer
  v
over-the-counter broker  ->  bank account in a mule's name
  |
  v
cash, gift cards, or an invoice settled on the other side of a border
```

## Chain hopping and bridges

A bridge locks an asset on the source chain and mints or releases a representation on the destination, so the trail continues in a different database with different address formats and a tracing tool that follows a single ledger loses it. The Democratic People's Republic of Korea (DPRK) operators who took roughly $620 million from the Ronin bridge in March 2022, an attribution the FBI made publicly the following month, moved the proceeds across chains before mixing them. Analytics firms now attribute the major bridges routinely by matching lock and mint events on amount, timing, and recipient, and sell cross-chain graphs as a product: chain hopping adds weeks to an investigation without severing the link.

## Mixers and the anonymity set

A mixer pools deposits from many users and pays withdrawals from the pool, so an outgoing transfer has no direct edge to any incoming one. The protection is statistical, and the statistic is the anonymity set: the number of unrelated deposits a withdrawal could plausibly have come from. Deposit an unusually large amount into a pool of small ones and withdraw a similar amount an hour later, and size and timing re-link the two with no cryptographic break. Mixers work best for small sums withdrawn patiently, which is the opposite of what a thief holding a large balance wants.

Tornado Cash defined the legal question. The Office of Foreign Assets Control ([OFAC](/wiki/economics/finance/regulation/ofac-sanctions)) designated it in August 2022, adding the smart contract addresses themselves to the specially designated nationals (SDN) list and prohibiting US persons from transacting with them. In *Van Loon v. Department of the Treasury*, decided in November 2024, the Fifth Circuit held that the immutable pool contracts are not "property" under the International Emergency Economic Powers Act, because nobody can own or control them, so OFAC exceeded its statutory authority in listing those addresses. The court did not hold that mixing is lawful, that the developers were wrongly charged, or that OFAC cannot sanction people who run mixers; an unownable contract is simply not a blockable asset. The addresses were delisted in March 2025.

The criminal cases ran separately. Alexey Pertsev, a Tornado Cash developer, was convicted of money laundering in the Netherlands in May 2024 and sentenced to 64 months; the conviction is under appeal, and he has since been conditionally released to prepare it. Roman Storm was tried in the Southern District of New York in 2025 and convicted of conspiring to operate an unlicensed money transmitting business, the jury deadlocking on the money laundering and sanctions counts. Neither outcome is final: Storm has not been sentenced, his acquittal motion is undecided, and the deadlocked counts are set for retrial in April 2027.

## Privacy coins

Monero breaks tracing at the protocol level rather than by pooling: ring signatures hide which output is spent, stealth addresses hide the recipient, and confidential transactions hide the amount, leaving no public balance to follow. The constraint is liquidity at the edges. Binance delisted Monero in February 2024 and other large venues have done the same, so converting a meaningful amount now requires a hop through a smaller exchange and produces the concentrated, unusual flow that monitoring is built to notice. Zcash has stronger cryptography, but most of its transactions use transparent addresses and shielded use has historically been a small enough share of its activity to stand out.

## Exchanges that do not ask, and brokers

Most volume goes somewhere less clever: an exchange with nominal verification, or an over-the-counter (OTC) broker who quotes a price, takes the coins, and wires currency from a bank account in another name.

- Suex, an OTC broker operating through accounts at larger exchanges, was designated by OFAC in September 2021, the first virtual currency exchange sanctioned by the United States; Treasury stated that a large share of its known transaction volume traced to illicit actors. Chatex, described as an affiliate, followed two months later.
- Garantex was designated in April 2022 alongside the German takedown of the Hydra darknet market, and its infrastructure was seized in a multinational action in March 2025. A successor appeared under a new name, which is the usual sequel.
- Bitzlato was named a primary money laundering concern by FinCEN in January 2023 while French authorities took down its servers; its founder pleaded guilty in the United States to running an unlicensed money transmitting business.
- Binance pleaded guilty in November 2023 to violating the Bank Secrecy Act and paid roughly $4.3 billion, on allegations that it had served US users for years without an adequate compliance program.

## Nested services

A nested service operates inside another exchange's account structure rather than holding its own banking and custody: it opens accounts at a large exchange, takes deposits from its own customers, and settles their trades through those accounts. The host sees one high-volume counterparty, and the underlying customers, with whatever verification they did or did not undergo, are invisible to it. Suex worked this way.

Chainalysis has reported for several years that a small number of deposit addresses at a handful of major exchanges receive a disproportionate share of all traceable criminal proceeds. Those addresses belong to nested services, so shutting one down closes a pipe rather than a leak, and [know your customer](/wiki/economics/finance/regulation/know-your-customer) at an exchange's perimeter says nothing about who is inside it.

## Off-ramps that skip banks

Crypto ATMs convert cash in both directions with weak identification at low amounts; the Federal Trade Commission (FTC) reported consumer losses at bitcoin ATMs above $110 million in 2023, roughly ten times the 2020 figure. Gift cards and prepaid cards move value in denominations too small to report and resell at a discount, and in-person cash trades involve no institution at all.

At scale the route is underground banking. Networks serving Southeast Asian scam compounds take crypto on one side and pay local currency on the other, settling the imbalance against trade invoices and informal ledgers rather than through correspondent banking. Elliptic reported that one Telegram-based guarantee marketplace serving these networks had facilitated more than $27 billion in transactions by the time it closed in May 2025, and FinCEN named the affiliated group a primary money laundering concern the same year.

## Where the cases are made

Every hop is recorded permanently and can be re-examined years later with tools that did not exist when the transfers happened, so an investigator who identifies one endpoint walks the graph backwards through everything before it.

Roughly 120,000 BTC left Bitfinex in a 2016 theft and sat largely unspent while the attackers tried to move it. In February 2022 the Department of Justice arrested Ilya Lichtenstein and Heather Morgan and seized about 94,000 BTC, then worth some $3.6 billion, the largest financial seizure the department had made. Lichtenstein pleaded guilty to money laundering conspiracy and admitted the theft, and Morgan pleaded guilty to conspiracy charges. The evidence was the laundering itself: accounts opened with fabricated identities, a darknet market, chain hops, gold and prepaid cards, every step recorded and none of it deletable.

[FinCEN](/wiki/economics/finance/regulation/fincen) registration and the [Travel Rule](/wiki/economics/finance/regulation/travel-rule) make the endpoints identifiable, since a transfer between two regulated institutions carries originator and beneficiary data with it. The stage that must touch the regulated system is the stage that generates evidence, so an [exit scam](/wiki/economics/finance/fraud/exit-scam) that succeeds technically can still end in an arrest, and the [money mule](/wiki/economics/finance/fraud/money-mule) standing at the exit is the most exposed person in the scheme. The full sequence from approach to withdrawal is in [anatomy of a crypto scam](/wiki/economics/finance/fraud/anatomy-of-a-crypto-scam).

## External links

- [OFAC recent actions](https://ofac.treasury.gov/recent-actions) — designations of exchanges, brokers, and mixers, with the underlying press releases
- [FinCEN news and enforcement](https://www.fincen.gov/news-room) — orders naming institutions as primary money laundering concerns
- [Chainalysis blog](https://www.chainalysis.com/blog/) — annual crime reports and the deposit-address concentration data
- [Elliptic research](https://www.elliptic.co/blog) — reporting on bridges, guarantee marketplaces, and Southeast Asian laundering networks
- [DOJ press releases](https://www.justice.gov/news) — the Bitfinex seizure and the mixer prosecutions
