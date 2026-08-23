---
title: "Regulation"
weight: 20
bookCollapseSection: true
---

The rules that decide who is allowed to move money, and what they have to say about it afterwards. This section covers US financial regulation from the perspective of someone building systems that touch it — not the compliance officer's view, but the engineer's: what the statute actually requires, why the requirement has the shape it does, and where it stops fitting once value moves on a [blockchain](/wiki/economics/finance/defi/blockchain) instead of through a correspondent bank.

Nothing here is legal advice. It is an attempt to explain a body of law well enough that design decisions can be made against it deliberately rather than by rumour.

## The regime

[Anti-money laundering](/wiki/economics/finance/regulation/anti-money-laundering) is the framing objective: interrupt the process by which criminal proceeds acquire a legitimate explanation. The [Bank Secrecy Act](/wiki/economics/finance/regulation/bank-secrecy-act) is the US implementation of it and the anchor page of this section — the 1970 statute, misleadingly named, that made banks into reporting agents for the government and produced almost every piece of financial paperwork an American encounters. [FinCEN](/wiki/economics/finance/regulation/fincen) is the Treasury bureau that administers it, and whose interpretive guidance has done more to shape the crypto industry than any legislation.

## What it requires of you

[Know your customer](/wiki/economics/finance/regulation/know-your-customer) is the obligation users actually meet: identify the customer, understand their expected behaviour, keep checking. [Money services business](/wiki/economics/finance/regulation/money-services-business) is the category that determines whether the obligation applies to you at all — the box nearly every crypto business lands in, and the one that turns a software company into a regulated financial institution. The [Travel Rule](/wiki/economics/finance/regulation/travel-rule) is the specific requirement that identifying data accompany a transfer between institutions, and the clearest case of a rule written for one architecture being applied to another.

## The adjacent regimes

[OFAC sanctions](/wiki/economics/finance/regulation/ofac-sanctions) is administered by the same department and run by the same compliance teams, but works on a different principle: it requires you to block rather than to report, it binds every US person rather than defined institutions, and it is strict-liability. It is also where the confrontation between immutable code and enforcement has been sharpest, in the sanctioning and eventual delisting of Tornado Cash.

[Regulation E](/wiki/economics/finance/regulation/regulation-e) points the other way entirely. Where the rest of this section conscripts institutions into law enforcement, Regulation E allocates a private loss between a bank and its own customer after an electronic payment goes wrong — and it is the rule now failing hardest, because it was drafted in 1978 and is being applied to the irrevocable instant transfers of [Zelle](/wiki/economics/finance/payments/zelle) and its equivalents.

## Elsewhere in the wiki

[DeFi and US regulatory restrictions](/wiki/economics/finance/defi/defi-us-regulatory-restrictions) covers the securities and derivatives side — the jurisdictional fight between the Securities and Exchange Commission (SEC) and the Commodity Futures Trading Commission (CFTC) — and stays in the [DeFi](/wiki/economics/finance/defi) section because it is about that subject specifically. [Interbox](/wiki/economics/finance/defi/interbox) is the worked example of designing around this material rather than merely complying with it.

## Wiki Pages

{{< section >}}
