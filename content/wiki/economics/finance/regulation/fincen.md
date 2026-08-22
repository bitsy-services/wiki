---
title: "FinCEN"
weight: 30
---

The Financial Crimes Enforcement Network (FinCEN) is the bureau of the US Treasury that administers the [Bank Secrecy Act](/wiki/economics/finance/regulation/bank-secrecy-act). It is the United States' financial intelligence unit: the place every Currency Transaction Report and Suspicious Activity Report is filed, and the agency that writes the regulations at 31 CFR Chapter X which determine what "compliance" concretely means.

It is small — on the order of 300 staff — and it has an outsized effect on how financial products are built, because it defines the categories that everything else keys off.

## What it actually does

**Collects.** FinCEN operates the [BSA](/wiki/economics/finance/regulation/bank-secrecy-act) database, receiving roughly 20 million currency transaction reports (CTRs) and 4 million suspicious activity reports (SARs) a year and making them queryable by thousands of law-enforcement and regulatory users across federal, state, and local agencies. FinCEN does not itself investigate crimes; it holds the data others investigate with.

**Writes rules.** The statute is short; the regulations are not. FinCEN decides who counts as a [money services business](/wiki/economics/finance/regulation/money-services-business), what an adequate [anti-money-laundering](/wiki/economics/finance/regulation/anti-money-laundering) program looks like, how far [know your customer](/wiki/economics/finance/regulation/know-your-customer) obligations extend, and where the reporting thresholds sit. Its most consequential act in this domain was not a rule at all but a 2013 interpretive guidance placing administrators and exchangers of convertible virtual currency inside the money-transmitter definition — a document that reshaped an industry without amending a single line of law.

**Delegates examination.** FinCEN does not have an examiner corps of its own. It delegates BSA examination to the functional regulators — the Office of the Comptroller of the Currency (OCC), the Federal Reserve, the Federal Deposit Insurance Corporation (FDIC), the National Credit Union Administration (NCUA), the Securities and Exchange Commission (SEC) and the Commodity Futures Trading Commission (CFTC) — and to the Internal Revenue Service (IRS) for institutions with no other federal supervisor, which includes most MSBs. In practice this means a crypto business's first BSA examination is usually conducted by the IRS.

**Enforces.** FinCEN assesses civil money penalties directly and refers criminal matters to the Department of Justice. Its largest actions have been against exchanges and banks with systemic program failures rather than against institutions that laundered money knowingly — the offence is usually the absent control, not the transaction.

**Registers.** MSBs register with FinCEN; the registry is public. Registration is not a licence and confers no approval — it is a notification, and it does not substitute for the state-by-state money transmitter licensing that is the far larger burden.

## The special-measures power

Section 311 of the USA PATRIOT Act lets Treasury designate a foreign jurisdiction, institution, account type, or class of transaction as a "primary money laundering concern" and impose one or more of five special measures. They escalate: the first is additional recordkeeping and reporting, the fifth is a prohibition on US institutions maintaining *correspondent accounts* — the accounts a foreign bank holds at a US bank in order to clear dollars. Because dollar clearing is close to non-optional in international finance, a fifth-measure designation is effectively a death sentence, and the mere proposal of one has been enough to collapse banks.

FinCEN proposed using this authority in 2023 against convertible virtual currency mixing as a *class of transaction* — the first time the power had been aimed at a category of activity rather than a named entity. The proposal was for the first special measure, recordkeeping and reporting on covered mixing transactions, not a correspondent-account cutoff. The framing is what matters: a class designation reaches software and protocols, not just companies.

## FinCEN and crypto

The trajectory has been consistent: extend existing categories rather than create new ones.

- **2013 guidance** — administrators and exchangers of convertible virtual currency are money transmitters; users are not.
- **2019 guidance** — a long application of that framework to specific business models, including wallets, mixers, and decentralised applications. It draws the line at control: if you have independent control over a customer's value, you are a transmitter.
- **2020 proposed rule** — recordkeeping and reporting for transactions between hosted wallets and self-hosted ones. It attracted an extraordinary volume of adverse comment and has not been finalised.
- **2023** — the § 311 proposal on mixing as a class of transaction.

Separately, and not crypto-specific, FinCEN was handed the beneficial-ownership registry created by the Corporate Transparency Act, which was enacted in the same division of the 2021 defence authorisation bill as the Anti-Money Laundering Act of 2020. A March 2025 interim final rule narrowed that reporting requirement to foreign companies.

The through-line for anyone building is the control test. Custody creates obligations; the absence of custody is the argument against them, and it is an argument that has held up better in guidance than it has in prosecutions. The adjacent [OFAC sanctions](/wiki/economics/finance/regulation/ofac-sanctions) regime, administered by a different Treasury office on a different principle, has been the sharper instrument against protocols — and the [Travel Rule](/wiki/economics/finance/regulation/travel-rule) is the FinCEN requirement that fits crypto worst.

## External links

- [FinCEN](https://www.fincen.gov/) — the agency
- [31 CFR Chapter X](https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X) — the regulations FinCEN writes
- [MSB registrant search](https://www.fincen.gov/msb-registrant-search) — the public register
- [FinCEN guidance library](https://www.fincen.gov/resources/statutes-regulations/guidance) — including the 2013 and 2019 virtual currency documents
