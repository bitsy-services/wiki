---
title: "Regulation E"
weight: 80
---

Regulation E is the rule that decides whether a consumer gets their money back after an electronic payment goes wrong. It sits at 12 CFR Part 1005, implements the Electronic Fund Transfer Act (EFTA) of 1978, and is administered by the Consumer Financial Protection Bureau (CFPB).

It is the closest thing US law has to a consumer bill of rights for payments. Written for a world of automated teller machines and preauthorized debits, it now governs [instant irrevocable transfers](/wiki/economics/finance/payments/zelle) it never contemplated, and the question that follows — who bears the loss when a consumer is talked into pressing send — has no federal answer.

Nothing here is legal advice.

## What it covers

Regulation E applies to **electronic fund transfers** from a consumer's account at a financial institution: card transactions, direct deposits, [automated clearing house](/wiki/economics/finance/payments#the-rails) debits, transfers initiated by phone or app. It does not apply to business accounts, and — importantly — it does not apply to wire transfers, which have always been governed by Article 4A of the Uniform Commercial Code and its very different assumption that the sender is a sophisticated party.

Three obligations do most of the work.

**Disclosure.** Terms, fees, and error-resolution rights must be given before the first transfer and on periodic statements.

**Error resolution.** A consumer who reports an error within 60 days of the statement on which it appeared triggers a mandatory investigation. The institution has ten business days to resolve it or must provisionally credit the account and take up to 45 days. This procedural clock is enforceable independently of who ultimately bears the loss.

**Liability caps for unauthorized transfers.** For transfers involving an access device, the consumer's exposure is capped at $50 if reported within two business days of learning of the loss, $500 if reported later but within 60 days of the statement, and is unlimited for transfers appearing on a statement more than 60 days old and never reported. Everything above the cap falls on the institution.

## The definition that does all the damage

An **unauthorized electronic fund transfer** is defined as one initiated by a person other than the consumer, without actual authority to initiate it, and from which the consumer receives no benefit.

It asks *who initiated the transfer*. It does not ask whether the consumer's decision to initiate was procured by deception.

This was an unremarkable line to draw in 1978. The frauds of the era involved somebody physically taking a card, or a machine malfunctioning, and in both cases the consumer plainly did not press the button. On an instant push rail, the dominant fraud is the opposite shape: the victim is manipulated into pressing the button themselves. The industry reads that case as authorized and therefore outside the rule. That reading is textually defensible and leaves the loss with the least-informed party on the least-reversible rail — the argument set out in detail on [Zelle's fraud and liability page](/wiki/economics/finance/payments/zelle/fraud-and-liability).

Two boundaries are less contested than the headline dispute suggests:

- A transfer made by a fraudster using credentials the victim was tricked into revealing **is** unauthorized. The victim disclosed credentials; the fraudster initiated the transfer. Deception in obtaining the credentials does not confer actual authority.
- A transfer the consumer initiated under a false belief about *who they were paying* is, on the prevailing reading, authorized — regardless of how convincing the deception was.

The line, in other words, is drawn at whose finger was on the button rather than at whose intent was genuine, and virtually every hard case in modern payments fraud sits on the far side of it.

## The CFPB position

The Bureau has pushed at this boundary from several directions without ever settling it.

Its guidance has consistently held that fraudulently induced credential disclosure produces an unauthorized transfer, closing off the argument that a victim who was phished has authorized whatever follows. Its 2021 questions and answers on [peer-to-peer](/wiki/economics/finance/payments) payments confirmed that Regulation E's error-resolution procedures apply to these services in full, including the requirement to investigate rather than reflexively deny.

Where it went furthest was the December 2024 enforcement action against Early Warning Services and three of its owner banks over [Zelle](/wiki/economics/finance/payments/zelle). That complaint mostly avoided the authorized-versus-unauthorized argument, alleging instead inadequate identity verification at enrollment, failure to act on known patterns of account takeover, and deficient investigation of claims that were covered. It was voluntarily dismissed with prejudice in March 2025 following a change of administration, so none of it was adjudicated.

The practical position today is that the procedural obligations are clear and enforced, the substantive question of who pays for scam-induced transfers is unresolved at the federal level, and the pressure has migrated to state consumer-protection statutes and private litigation.

## Where it fits with the rest of this section

Regulation E is a different animal from most of what this section covers. The [Bank Secrecy Act](/wiki/economics/finance/regulation/bank-secrecy-act) regime and [OFAC sanctions](/wiki/economics/finance/regulation/ofac-sanctions) conscript institutions into law enforcement — report this, block that. Regulation E instead allocates a private loss between an institution and its own customer. Its enforcement is largely a matter of consumers exercising rights rather than examiners auditing programmes.

It also has almost no purchase on [DeFi](/wiki/economics/finance/defi). Regulation E binds a *financial institution* holding a consumer *account*, and a self-custodied wallet is neither. A consumer who sends tokens to the wrong address has no error-resolution right, because there is no institution against whom to assert one — which is a straightforward statement of the tradeoff, not a gap waiting to be filled. Where a custodial [exchange or gateway](/wiki/economics/finance/defi/cryptocurrency-gateway) does hold consumer funds, whether it holds an "account" for these purposes has been argued both ways and never definitively resolved.

## External links

- [12 CFR Part 1005 (Regulation E)](https://www.ecfr.gov/current/title-12/chapter-X/part-1005) — the rule itself
- [Electronic Fund Transfer Act](https://www.consumerfinance.gov/rules-policy/regulations/1005/) — the CFPB's regulation page, with commentary
- [CFPB: electronic fund transfer FAQs](https://www.consumerfinance.gov/compliance/compliance-resources/deposit-accounts-resources/electronic-fund-transfers/electronic-fund-transfers-faqs/) — the guidance on peer-to-peer services and unauthorized transfers
- [Uniform Commercial Code Article 4A](https://www.law.cornell.edu/ucc/4A) — the very different regime governing wires
