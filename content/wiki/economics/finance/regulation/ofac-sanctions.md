---
title: "OFAC Sanctions"
weight: 70
---

The Office of Foreign Assets Control (OFAC) administers US economic sanctions. It is part of Treasury, as [FinCEN](/wiki/economics/finance/regulation/fincen) is, and in practice the same compliance team handles both — but the two regimes are legally distinct in a way that matters enormously to anyone building financial software.

The [Bank Secrecy Act](/wiki/economics/finance/regulation/bank-secrecy-act) and the [anti-money-laundering](/wiki/economics/finance/regulation/anti-money-laundering) regime built on it require you to *report*. OFAC requires you to *stop*.

## The difference that matters

| | BSA / AML | OFAC |
|---|---|---|
| Obligation | Report and record | Block or reject the transaction |
| Who is covered | Defined financial institutions | **All US persons**, everywhere |
| Mental state | Willfulness for criminal liability | **Strict liability** for civil penalties |
| On a violation | File a report | Freeze the assets and report the blocking |

Two of those rows do the work. OFAC binds every US person and entity — not just regulated institutions, but individuals, open-source developers, and companies with no financial licence at all. And civil liability is strict: not knowing that a counterparty was sanctioned is not a defence. Intent affects the penalty, not the violation.

This is why sanctions screening, rather than AML reporting, is the compliance function most likely to reach someone who never thought of themselves as being in finance.

## The lists

The **Specially Designated Nationals and Blocked Persons List** (SDN List) is the central one: individuals, entities, vessels, and — since 2018 — cryptocurrency addresses. Property of an SDN in the possession of a US person must be blocked, meaning frozen and reported, not returned. The **50 Percent Rule** extends designation automatically to any entity owned 50% or more, directly or indirectly, by one or more SDNs, even when that entity is not itself listed. Alongside the SDN List sit country programs (comprehensive embargoes) and a set of sectoral and non-SDN lists with narrower prohibitions.

OFAC publishes crypto addresses as identifiers on SDN entries, which is what makes screening a withdrawal address a routine part of every exchange's outbound flow.

## Sanctioning software

The crypto-specific question is whether a sanctions regime designed for people and companies can be applied to code that has neither.

In August 2022 OFAC designated Tornado Cash, an [Ethereum](/wiki/economics/finance/defi/ethereum) mixing protocol, adding its [smart contract](/wiki/economics/finance/defi/smart-contract) addresses to the SDN List. This was the first designation aimed at autonomous, immutable software rather than at an entity. The immediate effects were unprecedented: US persons were prohibited from interacting with the contracts, front-ends went dark, developers had GitHub accounts suspended, and — because the contracts accepted deposits from anyone — third parties could send funds to an American's address from the sanctioned protocol, creating an interaction the recipient had no way to refuse.

The legal challenge turned on a narrow question with wide consequences. In *Van Loon v. Department of the Treasury* (Fifth Circuit, November 2024), the court held that the immutable Tornado Cash smart contracts are not "property" within the meaning of the International Emergency Economic Powers Act, because nobody can own or control them — a contract that cannot be altered, deleted, or directed by any person cannot be blocked, since there is nothing to block. Treasury removed the designation in March 2025.

The ruling is narrower than it is often reported to be. It does not hold that developers are beyond reach, that mixing is lawful, or that other authorities are unavailable — FinCEN's proposed special measures on mixing as a class, and criminal prosecutions under the unlicensed-money-transmission statute, both survive it untouched. What it establishes is a specific limit: the property-blocking mechanism requires an owner, and a [finalized smart contract](/wiki/economics/finance/defi/finalized-smart-contract) does not have one.

That is worth stating precisely because it is the clearest case so far of immutability functioning as a legal fact rather than merely a technical one — and of the enforcement response moving, immediately, to the parties who *can* be reached.

## Practical exposure

For anyone operating in this space:

- Receiving funds from a sanctioned address can create a blocking obligation regardless of consent — an inbound transfer is not something you can decline, and the resulting property is frozen rather than returned.
- Screening applies to **counterparty addresses**, not just customer names, and the SDN List changes without notice.
- Voluntary self-disclosure of an apparent violation substantially reduces the penalty, and is the standard advice once one is discovered.
- A [DEX](/wiki/economics/finance/defi/dex) front-end that blocks sanctioned addresses is doing OFAC compliance, not AML compliance; these are different controls with different triggers.

[DeFi and US regulatory restrictions](/wiki/economics/finance/defi/defi-us-regulatory-restrictions) sets this alongside the Securities and Exchange Commission and Commodity Futures Trading Commission pieces of the picture.

## External links

- [OFAC sanctions programs](https://ofac.treasury.gov/sanctions-programs-and-country-information) — the active programs
- [SDN List search](https://sanctionssearch.ofac.treas.gov/) — the searchable list, including crypto addresses
- [OFAC sanctions compliance guidance for the virtual currency industry](https://ofac.treasury.gov/media/913571/download) — Treasury's own expectations for crypto businesses
- [Van Loon v. Department of the Treasury](https://www.ca5.uscourts.gov/opinions/pub/23/23-50669-CV0.pdf) — the Fifth Circuit opinion on sanctioning immutable contracts
