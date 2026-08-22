---
title: "Know Your Customer"
weight: 40
---

Know Your Customer (KYC) is the set of obligations requiring a financial institution to establish who its customer is, understand what that customer is likely to do, and keep checking whether they are still doing it. It is the operational front end of [anti-money laundering](/wiki/economics/finance/regulation/anti-money-laundering) — the part users actually encounter, and the reason opening an account involves a photograph of a passport rather than a signature.

In the US the obligations come from two places: the Customer Identification Program (CIP) rule, added to the [Bank Secrecy Act](/wiki/economics/finance/regulation/bank-secrecy-act) by § 326 of the USA PATRIOT Act, and the 2016 Customer Due Diligence Rule, which added beneficial ownership and ongoing monitoring.

Both bind *covered financial institutions* — banks, broker-dealers, mutual funds, futures commission merchants. A [money services business](/wiki/economics/finance/regulation/money-services-business) is not one, and reaches much the same place by a different route: the risk-based AML program requirement at 31 CFR 1022.210, the [transmittal recordkeeping and Travel Rule requirements](/wiki/economics/finance/regulation/travel-rule), and the conditions attached to its state licences. The distinction is worth holding on to, because most crypto businesses are MSBs and will be examined against the rules that actually apply to them.

## The three layers

**Customer Identification Program (CIP).** The minimum. Before opening an account, collect name, date of birth, address, and an identification number (SSN or, for non-US persons, passport number or equivalent), then verify it — documentary (inspect the ID) or non-documentary (check against credit bureau and public records). Keep the records for five years after the account closes.

**Customer Due Diligence (CDD).** Understand the nature and purpose of the relationship well enough to establish a baseline of expected activity, so that departures from it can be detected. For a legal-entity customer, identify the beneficial owners: every individual holding 25% or more of the equity, plus one individual with significant managerial control. The 25% threshold is a compromise — it is trivially defeated by five owners holding 20% each, and it is the single most-criticised number in the rule.

**Enhanced Due Diligence (EDD).** Applied to higher-risk relationships: politically exposed persons, correspondent accounts for foreign banks, private banking above certain thresholds, customers in high-risk jurisdictions. Source of wealth and source of funds move from assumed to documented, and review frequency goes up.

None of these is a one-time gate. The CDD Rule made ongoing monitoring an explicit program element, so the baseline established at onboarding is something the institution is obliged to keep testing against.

## Why it is expensive and unpopular

KYC generates friction that falls almost entirely on legitimate users, for two structural reasons.

The first is that identity verification is a probabilistic process being asked to produce a binary output. False rejections are invisible to the regulator and costly only to the rejected applicant, so institutions tune conservatively. Applicants without conventional documentation — recent immigrants, the young, the unhoused, people whose legal name has changed — absorb the cost.

The second is that KYC does not compose. Each institution must perform its own; there is no accepted mechanism for one to rely on another's work. A user who has verified their identity with a bank, a broker, and three exchanges has surrendered the same documents five times and created five separate breach targets. The data is a permanent liability: identity documents cannot be rotated after a compromise the way a password can.

There is also a straightforward efficacy objection. KYC establishes that someone presented convincing documents at a point in time. It does not establish that they control the account afterwards, which is precisely the failure mode in account takeover, money muling, and coerced-account fraud — three of the more common laundering typologies.

## KYC in crypto

Anything custodial inherits the full regime. A [cryptocurrency gateway](/wiki/economics/finance/defi/cryptocurrency-gateway) or centralised exchange builds substantially what a bank builds — verified identity at onboarding, a documented risk assessment, ongoing monitoring — even though, as above, the CIP and CDD rules themselves do not reach it. The additional wrinkles are that outbound transfers may carry Travel Rule obligations and that every withdrawal address is screened against the [OFAC](/wiki/economics/finance/regulation/ofac-sanctions) list.

A [DEX](/wiki/economics/finance/defi/dex) has no equivalent, because there is no account and no operator to open one. The contract cannot decline a caller. This is the sharpest illustration of why the regulatory perimeter sits at the fiat edges rather than on-chain, and the pressure has accordingly moved to front-ends, which *can* refuse to serve a request.

Two directions of work try to reduce the damage rather than merely comply with it:

- **Reusable verification.** [Interbox](/wiki/economics/finance/defi/interbox) argues that a bank has already performed the diligence the statute wants, and that a cryptographic link between a verified account and a self-custodied wallet can carry the assurance without the documents being copied again.
- **Proof instead of disclosure.** [Zero-knowledge proofs](/wiki/cs/zero-knowledge-proofs) can establish membership in a credentialed set — over 18, not sanctioned, verified by an accredited institution — without revealing which member. This answers the technical problem cleanly. It does not yet answer the legal one, because the regulations specify records to be retained, not facts to be established.

## External links

- [FinCEN CDD Rule](https://www.fincen.gov/resources/statutes-regulations/federal-register-notices/customer-due-diligence-requirements) — the beneficial ownership requirements
- [FFIEC BSA/AML Manual: CIP](https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/01) — how examiners assess identification programs
- [FATF Recommendation 10](https://www.fatf-gafi.org/en/topics/fatf-recommendations.html) — customer due diligence as an international standard
- [W3C Verifiable Credentials](https://www.w3.org/TR/vc-data-model-2.0/) — the standards work on portable, cryptographically verifiable identity claims
