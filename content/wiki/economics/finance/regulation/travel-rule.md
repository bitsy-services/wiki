---
title: "Travel Rule"
weight: 60
---

The Travel Rule requires that identifying information about the originator and beneficiary of a funds transfer *travel with the transfer* — that each institution in the chain passes the details to the next one, so an investigator reading a payment message at any hop can see who is on both ends.

It dates to 1995, sits at 31 CFR 1010.410(f) under the [Bank Secrecy Act](/wiki/economics/finance/regulation/bank-secrecy-act), and applies to transmittals of $3,000 or more by banks and non-bank financial institutions alike — including any [money services business](/wiki/economics/finance/regulation/money-services-business) that transmits funds. It was designed for a world in which every hop is a licensed institution with a legal identity and a message format to put the data in. Applying it to [blockchain](/wiki/economics/finance/defi/blockchain) transfers runs into four problems, all of them architectural rather than political.

## What must travel

For a covered transmittal, the originator's institution must include and pass on:

- The originator's name, address, and account number
- The amount and execution date
- The identity of the recipient's institution
- The beneficiary's name, address, and account number, if received

The receiving institution must retain what it gets. A 2020 [FinCEN](/wiki/economics/finance/regulation/fincen) rulemaking proposed dropping the threshold to $250 for cross-border transfers; it was never finalised, and the $3,000 figure — unindexed since 1995, like most [BSA](/wiki/economics/finance/regulation/bank-secrecy-act) thresholds — still stands.

## FATF Recommendation 16 and VASPs

In 2019 the Financial Action Task Force extended its equivalent of the rule to virtual asset service providers (VASPs), a category covering exchanges, custodians, and some wallet providers. The FATF threshold is $1,000, lower than the US one, and because FATF compliance is assessed through mutual evaluations that affect a whole country's access to correspondent banking — the accounts its banks hold abroad in order to settle cross-border payments — the standard propagated quickly. Most jurisdictions with a functioning crypto sector now have some version of it.

## Why it does not fit

A bank wire is a message *about* a value transfer, carried on a network that has fields for exactly this data. A blockchain transaction *is* the value transfer, and it has no such fields. The consequences follow directly.

**There is no channel.** Nothing in a standard transfer carries a name and address, and nothing should — a public ledger is the last place to publish customer identity. So the data has to move over a side channel that the chain knows nothing about, which means the two VASPs must find each other, agree on a protocol, and authenticate one another before the on-chain transfer settles. Competing standards emerged — the Travel Rule Protocol (TRP), IVMS101 as a common data model, and various proprietary networks — and interoperability between them is still incomplete.

**Addresses are not accounts.** The rule assumes a beneficiary institution exists and can be identified from the transfer instruction. An address on a public chain reveals nothing about whether it belongs to an exchange, an individual, or a [smart contract](/wiki/economics/finance/defi/smart-contract). Determining the counterparty VASP from an address is a heuristic exercise performed by analytics vendors, not a lookup.

**Self-custody has no counterparty.** When a customer withdraws to their own wallet, there is no receiving institution to send anything to. Jurisdictions have diverged here: some require the sending VASP to collect and verify a declaration of ownership, some require proof of control over the destination address, and some exempt the case. This is where the rule most directly touches ordinary users: it is the mechanism behind a [gateway or exchange](/wiki/economics/finance/defi/cryptocurrency-gateway) asking a customer to sign a message from a wallet they already own.

**The sunrise problem.** The rule binds a VASP only where its jurisdiction has implemented it. Until implementation is universal, a compliant VASP routinely transacts with counterparties under no obligation to reciprocate — so it collects data it cannot send and expects data that never arrives.

The net effect is a rule that imposes substantial cost on regulated intermediaries and is, by construction, inapplicable to the transfers between self-custodied wallets that it would most want to observe. That gap is a recurring theme in the [DeFi regulatory picture](/wiki/economics/finance/defi/defi-us-regulatory-restrictions).

## External links

- [31 CFR 1010.410(f)](https://www.ecfr.gov/current/title-31/section-1010.410#p-1010.410(f)) — the rule itself
- [FinCEN/Federal Reserve Travel Rule guidance](https://www.fincen.gov/resources/statutes-regulations/guidance/funds-travel-regulations-questions-answers) — questions and answers on scope
- [FATF Recommendation 16 and virtual assets](https://www.fatf-gafi.org/en/topics/virtual-assets.html) — the international extension to VASPs
- [IVMS101](https://www.intervasp.org/) — the interVASP data model most Travel Rule protocols encode
