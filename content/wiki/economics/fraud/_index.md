---
title: "Fraud"
weight: 25
bookCollapseSection: true
---

Crypto fraud is not one crime repeated on a new substrate. It is a dozen separate businesses that happen to share a settlement layer, and most of them resemble their pre-crypto ancestor more than they resemble each other. A [rug pull](/wiki/economics/fraud/rug-pull) is a deploy transaction with a backdoor in it. [Pig butchering](/wiki/economics/fraud/pig-butchering) is a labour-intensive confidence trick staffed by trafficked workers in compounds along the Mekong. [Wash trading](/wiki/economics/fraud/wash-trading) is a market-structure problem that predates the telegraph. Grouping them under one heading is useful only because the [blockchain](/wiki/economics/defi/blockchain) changes the same four things for all of them.

## What the chain actually changes

**Settlement is final.** A confirmed transfer has no chargeback, no return window, and no arbitration body. Card networks make fraud a cost of doing business precisely because they can reverse it; a chain cannot. This is the same property that gives [Zelle](/wiki/economics/payments/zelle) its [fraud problem](/wiki/economics/payments/zelle/fraud-and-liability), applied to a rail with no bank on either end.

**Issuance is permissionless.** Deploying a token costs a few dollars of gas and requires no registration, no prospectus, and no counterparty's consent. A [permissionless token factory](/wiki/economics/defi/par-token/permissionless-token-factory) will mint a convincing imitation of any asset on request, and a [decentralized exchange](/wiki/economics/defi/markets/dex) will list it without asking who deployed it.

**Identity is thin at the edges and absent in the middle.** A regulated exchange performs [know your customer](/wiki/economics/regulation/know-your-customer) checks; the wallet that receives the stolen funds does not. Fraud concentrates in the gap, and enforcement concentrates at the two points where the gap closes — the on-ramp and the [cash-out](/wiki/economics/fraud/cashing-out).

**The ledger is public.** This one cuts the other way and is routinely understated. Every hop of a stolen balance is recorded permanently, in the clear, and attributable to whatever the endpoints eventually reveal. Chain analysis has produced convictions in cases that would have been unworkable against a cash business, and the seven-year gap between a theft and its unwinding is an artefact of subpoena timelines rather than of missing evidence.

The FBI's Internet Crime Complaint Center (IC3) recorded roughly $9.3 billion in crypto-related fraud losses reported by US victims in 2024, against $5.6 billion in 2023. Reported losses are a floor: the modal victim of an investment scam does not file, and the figure excludes protocol exploits, which are counted as theft rather than fraud.

## Four groups

**Market and issuance fraud** attacks the asset itself. The token is real, the contract is deployed, and something about its construction or its trading guarantees the buyer loses: liquidity that can be withdrawn ([rug pull](/wiki/economics/fraud/rug-pull)), a transfer function that refuses to sell ([honeypot](/wiki/economics/fraud/honeypot-token)), an owner key that can mint or freeze at will ([hidden admin controls](/wiki/economics/fraud/hidden-admin-controls)), coordinated buying that manufactures a price ([pump and dump](/wiki/economics/fraud/pump-and-dump)), or self-dealing volume that manufactures the appearance of a market ([wash trading](/wiki/economics/fraud/wash-trading)).

**Investment fraud** attacks the offering. No asset need exist at all: a [Ponzi scheme](/wiki/economics/fraud/ponzi-scheme) pays old investors with new deposits until deposits stop, an [initial coin offering](/wiki/economics/fraud/ico-fraud) sells a token against a roadmap that was never going to be built, an [exit scam](/wiki/economics/fraud/exit-scam) takes custody legitimately and then leaves, and an [exchange collapse](/wiki/economics/fraud/exchange-collapse) discovers that customer deposits were never segregated in the first place.

**Social engineering** attacks the holder. The contracts behave correctly and the victim signs anyway: a months-long relationship ending in a fake trading platform ([pig butchering](/wiki/economics/fraud/pig-butchering)), an impersonated celebrity promising a doubled return ([giveaway scam](/wiki/economics/fraud/giveaway-scam)), a signature request that transfers everything ([wallet drainer](/wiki/economics/fraud/wallet-drainer), [approval phishing](/wiki/economics/fraud/approval-phishing)), a lookalike address planted in the transaction history ([address poisoning](/wiki/economics/fraud/address-poisoning)), a carrier account transferred to somebody else ([SIM swap](/wiki/economics/fraud/sim-swap)), a job interview that installs a backdoor ([fake job offer](/wiki/economics/fraud/fake-job-offer)), an imitation of a token you already hold ([fake token](/wiki/economics/fraud/fake-token)), or a second approach offering to recover what the first one took ([recovery scam](/wiki/economics/fraud/recovery-scam)).

**Laundering and cash-out** is the part every other group depends on. Stolen value is worthless until it becomes spendable, which requires either an institution that does not ask ([cashing out](/wiki/economics/fraud/cashing-out)) or a person whose identity absorbs the question ([money mules](/wiki/economics/fraud/money-mule)). It is also the stage with the most enforcement leverage, because it is the only one that must touch the regulated system.

[Anatomy of a crypto scam](/wiki/economics/fraud/anatomy-of-a-crypto-scam) runs across all four: the structure most of them share, and the handful of points where an outsider can tell.

## Wiki Pages

{{< section >}}
