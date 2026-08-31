---
title: "Pig Butchering"
weight: 60
---

A pig-butchering scam is a long-form investment fraud that uses a stranger's friendship as the delivery mechanism. First contact is unsolicited and mundane — a text message addressed to a wrong number, a match on a dating app, a connection request on a professional network. Money goes unmentioned for weeks. Once the relationship is established the operator introduces trading as an aside, walks the target through a small deposit to a platform that is not a market, shows a profit, permits a withdrawal, and then absorbs escalating deposits until the balance on the screen is large and the money behind it is gone. It is the largest [crypto fraud](/wiki/economics/finance/fraud) category by dollars lost and the least technical: nothing about it requires a contract bug, a compromised key, or a malicious signature.

The name renders the Chinese 杀猪盘 (*shā zhū pán*), "pig-butchering plate" — the target is the pig, the months of rapport are the fattening, the final deposits are the slaughter. Interpol asked in December 2023 that the term be retired in favour of "romance baiting", and survivor-advocacy groups prefer "relationship investment scam", on the ground that the original is the operators' own word for their marks and names the victim as livestock.

## The script

Amounts and intervals vary; the ordering does not.

```text
week 0       unsolicited contact — wrong number, dating app, professional network
weeks 1-6    ordinary conversation; no platform, no ask, no money
week 6       trading mentioned in passing as the sender's own side income
week 7       small first deposit to the platform the sender uses; shows a gain
week 8       withdrawal of principal plus gain SUCCEEDS
weeks 9-20   deposits escalate; on-screen balance compounds
week 20      withdrawal denied: "capital gains tax", "account unfreezing fee"
after        the fee is paid; a further fee appears; contact ends
```

The permitted early withdrawal converts an abstract promise into a verified experience. Everything before it is a claim by someone the target has never met; the withdrawal is evidence the target produced themselves, on their own device, with their own money. It costs the operator the gain plus the principal, typically a few hundred dollars. Every later refusal then reads as a problem with one transfer rather than with the platform, and the follow-up demand is shaped to match: a tax, a compliance deposit, an unfreezing fee. An obstacle with a price is answerable; a refusal is not.

## The platform

The front end shows an account balance, a price chart, an order history, and a withdrawal button, all served from the operator's own database. Some are built as a plausible [decentralized application](/wiki/economics/finance/defi/dapp) with a wallet-connect flow, so the target signs from a wallet they control and never hands over a password — and in some variants that signature is itself an [approval](/wiki/economics/finance/fraud/approval-phishing) that lets the operator move tokens without a further deposit. Others run a "mining pool" or "liquidity mining" story that maps onto real [yield farming](/wiki/economics/finance/defi/yield-farming) closely enough to survive a superficial check.

The deposit address is the operator's. The displayed balance is a number in a row of a database, and no position exists on any chain: no pool, no counterparty, no trade. It can show any figure, including one large enough to justify the next deposit.

## The compounds

The work is done from industrial compounds in Myanmar, Cambodia, and Laos, staffed substantially by people who were themselves trafficked — recruited through [fake job offers](/wiki/economics/finance/fraud/fake-job-offer) advertising customer-service or translation work at plausible salaries, then held on arrival with confiscated passports, debt bondage, and violence.

```text
Myawaddy, Karen State, Myanmar   KK Park, Shwe Kokko — walled compounds on the Thai border
Sihanoukville, Cambodia          repurposed casino and resort developments
Bokeo, Laos                      the Golden Triangle special economic zone
```

The UN human rights office reported in August 2023 that credible sources put at least 120,000 people in Myanmar and around 100,000 in Cambodia in situations of forced criminality of this kind. The United Nations Office on Drugs and Crime, in an October 2024 assessment, estimated losses to scam syndicates in East and Southeast Asia at between $18 billion and $37 billion for 2023. In February 2025, after Thailand cut electricity, fuel, and internet to areas serving Myawaddy, several thousand workers of dozens of nationalities were released and repatriated. Both ends of this fraud have victims.

## Scale

The FBI Internet Crime Complaint Center (IC3) reported $5.6 billion in crypto-related losses from US complaints in 2023, of which investment fraud — the category this scam falls in — accounted for about $3.96 billion; the 2024 figure was $9.3 billion overall. Chainalysis estimated 2024 scam revenue at $9.9 billion or more in its 2025 crime report. Both numbers are floors: on-chain attribution depends on identifying the receiving addresses, and victims of this fraud report it at a low rate.

## Where the money goes

Deposits move from the receiving address through consolidation wallets and cross-chain swaps toward whatever will convert them into local currency, so every operation depends on the [cash-out](/wiki/economics/finance/fraud/cashing-out) stage and on the [money mules](/wiki/economics/finance/fraud/money-mule) whose identities absorb the account-opening question. That is the only stage that must touch a regulated institution, and where nearly all enforcement leverage sits.

## Cases

**April 2023.** The Justice Department seized about $112 million in cryptocurrency across six accounts tied to this scam pattern, the largest such seizure to that point.

**November 2023.** Tether froze $225 million in its stablecoin — identified jointly with the Justice Department — held by a Southeast Asian syndicate running romance-investment scams, still the largest freeze of its kind.

**August 2024.** Shan Hanes, chief executive of Heartland Tri-State Bank in Elkhart, Kansas, was sentenced to 24 years for wiring $47.1 million of the bank's money into a pig-butchering scam over roughly two months. The bank failed.

**October 2025.** Prosecutors charged Chen Zhi, chairman of Cambodia's Prince Group, with wire fraud and money-laundering conspiracy and moved to forfeit approximately 127,271 bitcoin traced to compound operations; the US Treasury [sanctioned](/wiki/economics/finance/regulation/ofac-sanctions) the network the same week. The US charges remain unproven; Chen was arrested in Cambodia, extradited to China in January 2026, and formally arrested there that July on charges carrying a possible death sentence.

## What can be checked

These tells are structural — none requires a judgement about whether a person is sincere.

- An investment introduced by someone who initiated contact. The direction of the first message survives any amount of subsequent rapport.
- A platform with no price data on any third-party aggregator, and an app distributed by a link rather than a store listing.
- A withdrawal that requires a payment. No solvent venue funds a withdrawal from the customer's pocket, and taxes are not collected by exchanges as a precondition of release.
- A deposit address that changes between deposits, or differs from the one shown to a second account on the same platform.

## The second bite

Names, losses, and contact details of people who paid are worth money, and lists of them are sold onward, sometimes by the original operation. A second approach from a [recovery scam](/wiki/economics/finance/fraud/recovery-scam) — offering to trace and return the funds for a fee — typically follows within weeks.

## External links

- [FBI Internet Crime Complaint Center annual reports](https://www.ic3.gov/AnnualReport/Reports) — the annual and cryptocurrency-specific loss figures by category
- [United Nations Office on Drugs and Crime](https://www.unodc.org/) — regional assessments of scam-centre economics in Southeast Asia
- [UN Human Rights Office press releases](https://www.ohchr.org/en/media-centre) — where the August 2023 report on trafficking into scam operations was published
- [Chainalysis blog](https://www.chainalysis.com/blog/) — annual crime reports with on-chain scam-revenue estimates and methodology
- [Global Anti-Scam Organization](https://www.globalantiscam.org/) — victim-founded advocacy group; case documentation and reporting guidance
