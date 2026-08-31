---
title: "Money Mules"
weight: 110
---

Every [fraud](/wiki/economics/finance/fraud) eventually needs an account. Converting a victim's wire, an exchange balance, or a stolen card number into spendable value requires a bank or exchange account that survives [know your customer](/wiki/economics/finance/regulation/know-your-customer) checks, transaction monitoring, and the institution's own risk scoring. Opening one under a fabricated identity is slow and increasingly hard; renting one from a person who already has it is cheap, fast, and available in bulk.

A money mule is that person: someone whose verified identity absorbs the transaction. The mule receives funds, keeps a percentage, and forwards the rest onward as instructed, usually by a route that puts a second and third identity between the money and its origin. From the receiving institution's side, the transfer looks like a payment to a real customer whose documents checked out.

## Three ways a mule is recruited

**Witting.** The mule is paid a cut and knows the money is criminal. Recruitment happens on Telegram, in university group chats, and through existing criminal networks. This category supplies the most reliable accounts and the least useful defendants, because the recruiter is one anonymous handle away.

**Unwitting.** The mule is told a story. "Payment processing agent" and "financial operations associate" listings advertise a work-from-home role whose entire job description is receiving transfers and forwarding them, sometimes converting to crypto first; the reshipping variant has the victim receive parcels bought with stolen cards and post them abroad. Victims of [romance and investment scams](/wiki/economics/finance/fraud/pig-butchering) are asked to receive a transfer "because my account is frozen," which converts a victim into an intermediary in the same conversation. The recruitment pitch is close enough to a real job that it belongs beside the malware-delivery version on [fake job offers](/wiki/economics/finance/fraud/fake-job-offer).

Unwitting mules are prosecuted. Belief that the job was real is a defence to knowledge, not to having moved the money, and prosecutors reach the knowledge element through conscious avoidance: a jury may find the required knowledge where a defendant was aware of a high probability the funds were criminal and deliberately avoided confirming it. Ignoring the obvious question is not the same as not knowing the answer. Even where no charge follows, the account is closed and the closure is reported to shared account-screening databases, which can lock a person out of retail banking for years.

**Compromised.** No recruitment at all — the account is taken over, through phishing, credential stuffing, a [SIM swap](/wiki/economics/finance/fraud/sim-swap) that defeats one-time codes, or malware on the customer's device. The genuine owner learns about it when the bank calls.

## Account farming

The industrial version dispenses with recruitment per transaction. Accounts are opened in advance — with real identities bought or rented, or with synthetic ones built by pairing a valid identifier with a fabricated name and date of birth — then aged for months with small salary-like deposits and card purchases, so the behavioural model sees a boring customer with history rather than a new account. Aged accounts are sold as inventory, at a price far below the value of a single fraudulent transfer routed through one, which makes closure an accepted cost of the trade rather than a deterrent.

## The crypto version

Exchange accounts are farmed the same way, with one addition: a mule can be paid to complete verification with real documents and a live selfie, then hand over the credentials. Every withdrawal from that account is attributable to a real person who passed a real check.

Peer-to-peer trading desks inside large exchanges give the mule a second role. The scammer sells crypto to an ordinary buyer, the buyer pays the mule's bank account, the exchange releases the crypto from escrow, and the buyer becomes an unwitting layer: the funds arriving in their account came from a legitimate purchase they made. Victim money and clean money change places without either party seeing the swap.

The [Travel Rule](/wiki/economics/finance/regulation/travel-rule) shapes where this happens. It obliges an institution sending a qualifying transfer to pass originator and beneficiary information to the receiving institution, which means the identifying data follows the money only when both ends are regulated. Flows that touch one regulated entity and one private wallet, or none at all, carry no such record — so the rule pushes volume toward peer-to-peer desks, private wallets, and jurisdictions where the obligation is unenforced, rather than eliminating it.

## Why the receiving institution shrugs

In the United States, a bank that hosts a mule account bears almost none of the loss. The sending bank fields the customer's claim, and no rule allocates any part of the reimbursement to the institution whose books the money landed on; the receiving bank's exposure is regulatory rather than financial, and it arrives years later. The United Kingdom changed that calculation by splitting mandatory reimbursement evenly between sending and receiving firms, giving the receiving institution a direct financial reason to care about accounts opened to collect scam proceeds. The [Zelle fraud and liability](/wiki/economics/finance/payments/zelle/fraud-and-liability) page covers that regime and the American argument it sits against.

## Detection from the inside

An institution watching for mule behaviour looks for a pattern, not a transaction.

- Funds in and out the same day, leaving a balance near zero, repeatedly.
- A young account receiving from many senders with no relationship to each other or to the holder.
- Flow that contradicts the stated occupation and declared income by an order of magnitude.
- Cash deposits or withdrawals repeatedly just under the $10,000 currency transaction report (CTR) threshold. A CTR is triggered by currency rather than by transfers, so a $9,900 wire trips nothing; splitting cash to stay under the threshold is the separate federal offence of structuring under 31 U.S.C. § 5324, which turns on the purpose of evading the report.
- A dormant account that resumes activity at a new device, new address, and new payee set.
- One device fingerprint, phone number, or address appearing across accounts in unrelated names.
- Cash withdrawals or crypto purchases immediately following an inbound transfer, which convert a reversible entry into an irreversible one before the claim arrives.

## Where the law lands

The [Bank Secrecy Act](/wiki/economics/finance/regulation/bank-secrecy-act) requires the institution, not the mule, to file a suspicious activity report (SAR); the report is confidential and its existence may not be disclosed to the customer, so a mule account under investigation often behaves normally right up to closure.

Against the mule, the charges are 18 U.S.C. § 1956, which reaches transactions designed to conceal the source of criminal proceeds, and § 1957, which reaches spending more than $10,000 of criminally derived property and requires no concealment purpose at all. Operating an informal transfer service without registration is a separate offence under § 1960. The Department of Justice (DOJ) runs a recurring Money Mule Initiative with the FBI and postal inspectors, which mixes prosecutions with warning letters to people whose accounts show the pattern — an acknowledgement that a large share of the population moving the money did not set out to.

Downstream, the mule hands off to the professional stage of the pipeline, covered in [cashing out](/wiki/economics/finance/fraud/cashing-out).

## External links

- [FBI: money mules](https://www.fbi.gov/how-we-can-help-you/scams-and-safety/common-frauds-and-scams/money-mules) — the recruitment patterns and the bureau's warning language
- [Europol: money muling](https://www.europol.europa.eu/crime-areas/forgery-of-money-and-means-of-payment/money-muling) — the European Money Mule Action results and recruitment typologies
- [FinCEN advisories and guidance](https://www.fincen.gov/resources/advisoriesbulletinsfact-sheets) — red-flag indicators used by institutions when filing suspicious activity reports
- [DOJ Money Mule Initiative](https://www.justice.gov/opa/pr/justice-department-announces-landmark-money-mule-initiative) — the annual sweeps and the warning-letter programme
