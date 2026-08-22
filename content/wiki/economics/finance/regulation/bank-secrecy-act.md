---
title: "Bank Secrecy Act"
weight: 20
---

The Bank Secrecy Act (BSA) is the statute that turned American banks into reporting agents for the federal government. Passed in 1970 and amended roughly once a decade since, it is the spine of the US [anti-money-laundering](/wiki/economics/finance/regulation/anti-money-laundering) regime: the source of the paperwork a teller fills in when you deposit a large amount of cash, the reason a bank asks who ultimately owns the company opening an account, and — originally through a 2013 reinterpretation rather than any new law — the reason a [cryptocurrency exchange](/wiki/economics/finance/defi/cryptocurrency-gateway) wants a photograph of your driver's licence.

**This is not legal advice.** It is a description of a statute, written for engineers who need to understand why the systems they build have the shape they do. Anyone with actual compliance exposure should retain counsel.

## The name is backwards

The Act does not create bank secrecy. It abolishes it.

Neither half of the 1970 Act is called the Bank Secrecy Act. Title I is the financial-recordkeeping half, now at 12 U.S.C. §§ 1829b and 1951–1959; Title II is the Currency and Foreign Transactions Reporting Act, which is where the reporting duties come from. The popular name is best read against the legislative history, which dwells on the secret *foreign* accounts — Swiss and Caribbean — that Congress meant to pierce. The theory was that criminal enterprises generate cash, cash has to enter the banking system to be useful, and the entry point is therefore the place to watch. Rather than have the government surveil the banks, the government conscripted the banks to surveil their customers and hand over the results.

That inversion is the whole design, and it explains almost every downstream oddity. Your bank is not your fiduciary in this matter. It is a deputised reporter with a legal obligation to file paperwork about you, a legal prohibition on telling you it did, and a statutory immunity from being sued by you for filing it.

The reporting statute is codified at 31 U.S.C. §§ 5311–5336. The regulations that actually bind anyone are at 31 CFR Chapter X, written and enforced by [FinCEN](/wiki/economics/finance/regulation/fincen).

## What the statute requires

Four headings, running from the most routine to the most specialised.

### Currency Transaction Reports

A financial institution must file a Currency Transaction Report (CTR, FinCEN Form 112) for any cash transaction — or set of cash transactions by or on behalf of the same person in the same business day — exceeding $10,000. It is automatic and mechanical: no suspicion requirement, and no notice to you beyond the teller mentioning it. The only discretion is a narrow exemption system for established commercial customers, overhauled and made mandatory in 1994 specifically to bring the filing volume down.

The $10,000 figure was set in 1970 and has never been indexed to inflation. In 2026 dollars the 1970 threshold would sit somewhere north of $80,000, which means the reporting net now catches an enormous volume of ordinary commerce that Congress never intended to capture. FinCEN receives on the order of 20 million CTRs a year.

### Structuring

Because the threshold is a bright line, the obvious response is to stay under it. Congress criminalised that response in 1986: under 31 U.S.C. § 5324 it is a federal felony to break up transactions for the purpose of evading the reporting requirement.

Note what this does and does not depend on:

```text
Deposit $19,000 in one day                → CTR filed. No offence.
Deposit $9,500 Monday + $9,500 Tuesday,
  in order to avoid the CTR               → No CTR. Felony.
```

The money can be entirely lawful — wages, a legitimate business's daily till — and the structuring offence still stands, because the thing being prohibited is evasion of the report, not laundering. Through the 2000s and early 2010s the Internal Revenue Service (IRS) used this to seize the accounts of convenience stores and restaurants whose owners deposited cash under $10,000 out of habit or on their insurer's advice. The practice attracted enough outrage to produce an IRS policy change in 2014 and, eventually, a statutory limit in 2019 confining structuring forfeitures to funds derived from an unlawful source.

### Suspicious Activity Reports

Where the CTR is mechanical, the Suspicious Activity Report (SAR, FinCEN Form 111) is discretionary and therefore far more consequential. A bank must file one when it knows, suspects, or has reason to suspect that a transaction involves funds from illegal activity, is designed to evade the BSA, has no apparent lawful purpose, or is being used to facilitate criminal activity. The dollar trigger is low — $5,000 for banks, $2,000 for a [money services business](/wiki/economics/finance/regulation/money-services-business), the non-bank category covering money transmitters, check cashers and the like — and the filing deadline is 30 days from initial detection.

Two features make the SAR structurally different from any other report a business files about a customer:

- **Tipping off is a crime.** The institution may not tell the subject that a SAR was filed, or even that one is contemplated. If your account is closed the week after unusual activity, nobody involved is permitted to explain why.
- **The filer is immune.** 31 U.S.C. § 5318(g)(3) grants a safe harbour from civil liability for filing, including for filings that turn out to be wrong.

The combination — no downside for over-reporting, criminal exposure for under-reporting — produces exactly the incentive you would expect. Defensive filing is the norm; roughly 4 million SARs are filed annually, and the marginal one is filed to protect the institution rather than because anyone believes a crime occurred.

### Recordkeeping and the Travel Rule

Beyond reporting, the BSA imposes retention duties: five years for most records, including the identifying information behind funds transfers. The best-known of these is the [Travel Rule](/wiki/economics/finance/regulation/travel-rule), which requires that originator and beneficiary details accompany a transmittal of $3,000 or more as it moves between institutions. That rule was written for funds transfers between banks and money transmitters, and has since been aimed, awkwardly, at [blockchain](/wiki/economics/finance/defi/blockchain) transfers.

Two further reports round out the set. An FBAR — the Report of Foreign Bank and Financial Accounts, FinCEN Form 114 — is owed by any US person whose foreign financial accounts together exceed $10,000 at any point in the year — this is the direct descendant of the offshore-secrecy concern that named the Act. A CMIR — the Report of International Transportation of Currency or Monetary Instruments, Form 105 — is owed for physically carrying more than $10,000 in currency or monetary instruments across the border.

## The compliance program

Filing is only half of it. Since 1987 for banks, and since the PATRIOT Act for essentially every other financial institution, a regulated institution must maintain a written AML program. The requirements are conventionally called the pillars:

1. **Internal controls** — documented policies and procedures reasonably designed to achieve compliance.
2. **A designated compliance officer** — a named person with the authority and seniority to run the program.
3. **Ongoing training** — for the staff who actually touch transactions.
4. **Independent testing** — an audit by someone who does not report to the compliance officer.
5. **Customer due diligence** — added by the 2016 CDD Rule, effective 2018, which made risk-based [know your customer](/wiki/economics/finance/regulation/know-your-customer) an explicit program element and required institutions to identify the beneficial owners behind legal-entity accounts.

The first four pillars are near-universal. The fifth is not, and neither is the Customer Identification Program (CIP) rule that sits alongside it: both bind only *covered financial institutions* — banks, broker-dealers, mutual funds, futures commission merchants. A money services business is not one. Its identification duties come instead from the risk-based program requirement at 31 CFR 1022.210, the funds-transfer recordkeeping rules, and whatever its state licences impose. In practice an exchange ends up building much the same controls; the legal hook is simply different, which matters a great deal when an examiner asks which rule you believe you are following.

## How it grew

The 1970 Act was thin. Five later statutes and one regulation made it what it is.

**The Money Laundering Control Act of 1986** made laundering itself a federal crime — it had not been one — and created the structuring offence, closing the gap that made the CTR trivially avoidable.

**The Annunzio-Wylie Anti-Money Laundering Act of 1992** created the Suspicious Activity Report. Everything in the SAR section above comes from here rather than from the 1970 Act: the reporting authority at 31 U.S.C. § 5318(g), the prohibition on tipping off the subject, and the civil-liability safe harbour.

**The Money Laundering Suppression Act of 1994** cut both ways in a single bill. It overhauled the CTR exemption system to bring filing volume down, and in the same breath created the federal registration requirement for money services businesses and stripped out the knowledge-of-illegality element that the Supreme Court had just read into the structuring offence in *Ratzlaf v. United States*.

**The USA PATRIOT Act of 2001**, Title III, was the largest expansion. It made AML programs mandatory across the financial sector rather than just for banks (§ 352), required a formal Customer Identification Program for new accounts (§ 326), imposed enhanced due diligence (§ 312) on private banking and on correspondent accounts — the accounts a foreign bank holds at a US bank in order to reach the dollar system — gave Treasury the power to impose special measures on foreign jurisdictions and institutions of primary money-laundering concern (§ 311), and opened two information-sharing channels — government-to-institution (§ 314(a)) and institution-to-institution (§ 314(b)). Most of what a modern onboarding flow does, it does because of Title III.

**The CDD Rule (2016)** — a regulation rather than a statute — added the beneficial-ownership requirement described above: for a legal-entity customer, identify every individual owning 25% or more, plus one individual with significant control.

**The Anti-Money Laundering Act of 2020** modernised the statute for the first time in a generation. It created a beneficial-ownership registry at FinCEN under the Corporate Transparency Act — intended to shift the reporting burden from banks to companies themselves, though the bank-side obligation was never conformed and remains in force — established a whistleblower program, expanded Treasury's subpoena power over foreign banks with US correspondent accounts, and, importantly for this wiki, wrote "value that substitutes for currency or funds" into the statutory definition of a financial institution at 31 U.S.C. § 5312(a)(2), putting [cryptocurrency](/wiki/economics/finance/defi/cryptocurrency) businesses inside the statute rather than inside a guidance document. The registry itself has had a rough life: after litigation and a series of injunctions, a March 2025 interim final rule narrowed the reporting obligation to foreign companies, exempting domestic ones — still the operative position as of mid-2026.

## Who it applies to

"Financial institution" under the BSA is much broader than "bank". It reaches credit unions, broker-dealers, mutual funds, futures commission merchants, casinos, precious-metals dealers, insurance companies, and — the category that matters here — money services businesses: money transmitters, check cashers, dealers in foreign exchange, and providers and sellers of prepaid access.

FinCEN's 2013 guidance placed *administrators and exchangers* of convertible virtual currency inside the money-transmitter definition, while leaving *users* outside it. No statute changed; a definition was interpreted. That single document is why centralised exchanges look like banks and why the regulatory status of a [DEX](/wiki/economics/finance/defi/dex) — which has no administrator and arguably no exchanger — remains the open question it is. The 2019 guidance elaborated the application across specific business models, and the pressure point ever since has been non-custodial software: whether writing and publishing a tool that moves value makes you a transmitter of it. See [DeFi and US regulatory restrictions](/wiki/economics/finance/defi/defi-us-regulatory-restrictions) for how that has played out in enforcement.

## Penalties

Civil penalties run per violation and, for program failures, can be assessed per day. Willful violations carry up to five years' imprisonment under 31 U.S.C. § 5322, rising to ten where the violation accompanies another federal crime or a pattern of illegal activity exceeding $100,000 in a year. Prosecutors also reach for 18 U.S.C. § 1960, operating an unlicensed money transmitting business, which does not require proof that the money was dirty — only that the licence was missing.

The corporate numbers are what make this a board-level concern:

| Case | Year | Penalty |
|------|------|---------|
| HSBC | 2012 | $1.9B, deferred prosecution agreement |
| Danske Bank | 2022 | $2B, guilty plea to fraud conspiracy |
| Binance | 2023 | $4.3B combined; the CEO pleaded guilty to failing to maintain an effective AML program |
| TD Bank | 2024 | ~$3B plus a US asset cap; the first US bank to plead guilty to money-laundering conspiracy |

Individual liability for named compliance officers, once theoretical, is no longer.

## The Fourth Amendment question

The BSA was challenged immediately, and the challenge lost in a way that reshaped American privacy law well beyond banking.

In *California Bankers Association v. Shultz* (1974) the Supreme Court upheld the recordkeeping and reporting requirements. Two years later, *United States v. Miller* (1976) supplied the reasoning that has done the real work since: a bank depositor has no reasonable expectation of privacy in records held by the bank, because the information was voluntarily conveyed to a third party in the ordinary course of business. No expectation of privacy, no search, no warrant requirement.

This is the **third-party doctrine**, and it escaped banking almost at once — it is the reason phone records, email metadata, and subscriber information have historically been obtainable without a warrant. *Carpenter v. United States* (2018) carved out cell-site location data on the grounds that it is neither voluntarily shared nor limited in scope, but the Court was explicit that it was not disturbing *Miller*. Financial records remain outside the Fourth Amendment.

Congress responded to *Miller* with the Right to Financial Privacy Act of 1978, which imposes notice and process requirements on government access to bank records — with a large exception for anything filed under the BSA. The reports the Act compels are precisely the ones the privacy statute does not protect.

The uncomfortable summary: a legal regime built on the premise that you have surrendered your privacy by using a bank cannot be escaped by not using a bank, because cash above the threshold is itself reportable, and deliberately keeping it below the threshold is a separate felony. This is the argument that motivates most cryptographic approaches to payment, and it is worth understanding on its own terms before evaluating whether those approaches answer it.

## Does it work?

The honest answer is that after fifty years, nobody can demonstrate that it does — and the measurement problem is not incidental.

The system produces roughly 20 million CTRs and 4 million SARs a year. What that volume is worth is largely unmeasured: a 2019 Government Accountability Office review (GAO-19-582) found that the agencies do not regularly collect metrics on how useful BSA reports are, nor feed that information back to the institutions filing them. The most-cited estimate of laundering interdiction, from a 2011 study by the UN Office on Drugs and Crime, puts the share of criminal proceeds seized at around 0.2%. Meanwhile the direct compliance cost to US financial institutions runs into the tens of billions of dollars annually.

The second-order costs are less visible and possibly larger. Because the penalty for a missed filing is unbounded and the revenue from a small account is not, institutions rationally shed entire customer categories: money transmitters serving remittance corridors, charities operating in conflict zones, cannabis businesses, and crypto firms. This is **de-risking**, and there is little sign it reduces the underlying activity rather than pushing it into channels with no reporting at all — which would be the opposite of the statute's purpose.

The defence is that a suspicion-based, warrant-free trawl of the payment system is a genuine investigative resource whose successes are necessarily invisible, and that the counterfactual — a financial system with no reporting obligations whatsoever — would be worse. That may be true. It is also unfalsifiable, which is part of why the regime has grown in almost every decade since 1970. The contractions have been narrow and specific: the 2019 limit on structuring forfeitures, which followed a Treasury inspector-general finding that the great majority of sampled seizures had taken legal-source funds, and the 2025 retreat on beneficial-ownership reporting, which followed litigation. Neither followed from anyone establishing that the surveillance itself was not working. That question has still not been put.

## What it means for crypto

Everything above lands on this wiki's subject matter in three specific places.

**Custodial services are banks.** Any business that holds customer cryptocurrency and converts it to or from fiat is a money transmitter, must register with FinCEN, and owes a full AML program: identity verification at onboarding, transaction monitoring, SARs at the $2,000 threshold, and the Travel Rule on outbound transfers. This is the entire explanation for why an exchange account feels like a bank account.

**Non-custodial software is the contested frontier.** A [finalized smart contract](/wiki/economics/finance/defi/finalized-smart-contract) has no operator to register, no customer to identify, and nobody able to file a SAR. Whether that is a gap in the law or a feature of the technology is being decided case by case, and the cases so far have gone badly for developers of privacy tooling. The adjacent [OFAC sanctions](/wiki/economics/finance/regulation/ofac-sanctions) regime — which is not the BSA, and works quite differently — has been the sharper instrument there.

**The KYC data itself is the liability.** Every exchange that onboards a user accumulates a copy of that user's identity documents, and every copy is a breach waiting to happen. [Interbox](/wiki/economics/finance/defi/interbox) is an argument that this duplication is unnecessary: the diligence has already been done once, by the bank, and a cryptographic link between a verified account and a self-custodied wallet could carry the assurance without carrying the documents. Nothing in the current rules lets one institution rely on another's work, which is what makes this a design proposal rather than a compliance option — and the gap between what the technology can attest and what the regulations will accept is the general shape of most interesting work in this area.

## External links

- [31 CFR Chapter X](https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X) — the operative regulations, in full
- [FinCEN: BSA requirements](https://www.fincen.gov/resources/statutes-regulations) — statutes, regulations, and guidance from the administering agency
- [FFIEC BSA/AML Examination Manual](https://bsaaml.ffiec.gov/manual) — the Federal Financial Institutions Examination Council's manual, and how examiners actually assess a compliance program
- [FinCEN 2013 virtual currency guidance (FIN-2013-G001)](https://www.fincen.gov/resources/statutes-regulations/guidance/application-fincens-regulations-persons-administering) — the document that brought crypto inside the regime
- [United States v. Miller, 425 U.S. 435 (1976)](https://supreme.justia.com/cases/federal/us/425/435/) — the third-party doctrine as applied to bank records
- [GAO-19-582: Bank Secrecy Act](https://www.gao.gov/products/gao-19-582) — the review finding that the usefulness of BSA reports is not routinely measured
