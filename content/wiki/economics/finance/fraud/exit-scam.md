---
title: "Exit Scam"
weight: 50
---

An exit scam is an operator that took custody of other people's assets legitimately, ran a service for a while, and then left with the balance. The service usually worked: withdrawals processed, support answered, fees collected, sometimes for years. What ends it is a decision taken at a moment of the operator's choosing to stop honouring withdrawals and move the pooled assets somewhere depositors cannot follow.

The history is the distinction. A [rug pull](/wiki/economics/finance/fraud/rug-pull) is fraudulent at deploy — the mechanism was in the contract before anybody bought. An [exchange collapse](/wiki/economics/finance/fraud/exchange-collapse) is insolvency: the assets are gone and the operator is still standing there, filing for bankruptcy. An exit scam is a business that could have continued, whose operator concluded the accumulated float was worth more than the franchise. The three blur at the end, and the same facts often support more than one label, so the [fraud](/wiki/economics/finance/fraud) taxonomy is a set of tendencies rather than a partition.

## Custody is the precondition

An exit scam requires the operator to hold assets that are not theirs, and that requirement bounds the category. Non-custodial designs foreclose it outright: where withdrawals are executed by the holder's own key against a contract with no privileged withdrawal path, there is no float to leave with. The guarantee is narrow: it removes the exit scam, not the upgradeable proxy or the privileged role that quietly reintroduces one ([hidden admin controls](/wiki/economics/finance/fraud/hidden-admin-controls) covers that surface).

Between full custody and none sit the attempts to make custody checkable from outside. [Full reserve backing](/wiki/economics/finance/defi/full-reserve-backing) is the claim that every unit of liability is matched one-for-one by an asset held; proof-of-reserve schemes try to demonstrate that without opening the books. Both exist to answer the question a depositor otherwise cannot: is the money still there this morning.

## The "hack" cover story

The most common staging is an announced external theft, because it is cheap and the observable facts fit both stories. The operator publishes an incident notice, moves the balance, and what an outsider sees — a large outflow to unfamiliar addresses, withdrawals stopping, a support channel going quiet — is what a real intrusion also produces.

Signals that lean towards the operator, in rough order of the weight they carry:

- **Destination addresses that cluster with the operator's own.** Tracing tools group addresses by co-spending and common funding, and proceeds landing in a cluster already tied to the operator's hot wallets, or funded from them, are difficult to explain as an intruder's.
- **No exploit transaction.** A genuine compromise of a contract leaves a call on the chain that did something the contract did not intend, and it can be pointed at. A withdrawal signed with the operator's own key leaves an ordinary transfer. Absence of an exploit narrows the story to stolen keys or the operator.
- **Withdrawal behaviour that predates the announcement.** Deposit sweeps that stopped, user withdrawals that began failing, or a quiet drawdown in the days before the incident are visible after the fact on a public ledger.
- **What did not happen afterwards.** No post-mortem, no tracing firm engaged, no freeze requests sent to exchanges, no bounty offered to the supposed thief.

None of these is proof. A real key compromise produces transactions made with the operator's key, because that is what a stolen key does, and an operator can engage a tracing firm precisely to furnish the story. In most of the cases below the finding of fraud came from books and testimony, with the chain supplying corroboration rather than the case.

## From insolvency to absconding

A large share of exit scams begin as a genuine loss. The operator is hacked for real, takes a bad trade, or is caught wrong-way in a market move, and the hole is smaller than the float. Disclosure would end the business, so the operator conceals it and trades to recover, paying withdrawals out of other customers' deposits meanwhile, which makes the service a [Ponzi scheme](/wiki/economics/finance/fraud/ponzi-scheme) for as long as the concealment lasts. If the recovery trade works, nobody ever learns it happened; if it does not, the hole outgrows the point where disclosure is survivable and leaving is the only move left.

That is the rogue trader failure mode with the supervisor deleted. Nick Leeson hid Barings' losses in an error account until they reached £827 million and the bank failed in 1995; Jérôme Kerviel's unauthorized positions cost Société Générale €4.9 billion in 2008. Both were caught by a reconciliation performed by someone who did not report to the trader, the control a crypto operator holding its own keys does not have.

## Darknet markets

Darknet markets are the archetype, because the escrow structure makes the incentive computable. The market holds each buyer's payment until delivery is confirmed, so its wallet always holds the sum of every pending order, and the balance peaks right after a busy sales period. The operator can watch it.

Evolution went offline in March 2015 with the escrow intact; contemporary reporting put the balance around 43,000 bitcoin. Empire Market stopped responding in August 2020 after downtime blamed on denial-of-service attacks, with escrowed funds estimated in the tens of millions of dollars, and charges against alleged operators followed years later. Markets that resisted the temptation moved to multisignature escrow, where release requires two signatures out of buyer, vendor, and market — removing the operator's unilateral control of the pot at the cost of a user experience most buyers declined.

## Cases

**Thodex (Turkey, April 2021).** The exchange halted trading citing a "sale process" and founder Faruk Fatih Özer left the country the same week. He was located in Albania, extradited to Turkey, and convicted in 2023; he was found dead in a Turkish prison on 1 November 2025. Turkish sentencing aggregates per victim, so his term ran past eleven thousand years, a figure describing the counting rule rather than any expectation of service.

**QuadrigaCX (Canada, 2019).** Canada's largest exchange failed after founder Gerald Cotten was reported to have died in India in December 2018 holding sole knowledge of the keys to cold wallets said to contain roughly C$190 million of customer assets. The Ontario Securities Commission's June 2020 review found those wallets had been emptied months earlier, and that the shortfall came from Cotten trading customer funds against customers on his own platform using fabricated balances and covering the losses with other depositors' money — which the review characterised as a Ponzi scheme. The lost-keys story and the fraud finding both survive: the keys really were unrecoverable, and the wallets they protected were already empty. It sits here rather than under exchange collapse because the float had been dissipated long before the insolvency was filed — the death disclosed an exit that had already happened, rather than causing one.

**Africrypt (South Africa, 2021).** The brothers running the platform announced a hack in April 2021 and asked clients not to report it to the authorities. Employees were reported to have been cut off from back-end systems days earlier, and the brothers left the country; they deny absconding. Lawyers for investors initially claimed roughly 69,000 bitcoin; that figure was never substantiated and the amounts pursued in liquidation were far smaller. No criminal charges have been reported and the matter has run through liquidation rather than a criminal court, which makes it the one case here with no adjudicated finding. Access removed, hack announced, operators gone.

## What a depositor can check

**Proof of reserves, and what it does not establish.** Check whether liabilities were verified by someone independent, how often snapshots are taken, and whether the attesting firm accepts liability for its statement — [proof of reserves](/wiki/economics/finance/fraud/exchange-collapse#proof-of-reserves) has the mechanism and the four things it cannot show. A reserves page with no liability side is a wallet screenshot.

**Withdrawal behaviour.** Withdraw a small amount periodically, before you need to, and watch the timings. Rising minimums, new verification applied to withdrawals but not deposits, "wallet maintenance" outlasting any plausible chain upgrade, and a support backlog that grows only on the withdrawal queue are the precursors that show up first.

**Registration.** Check whether the operator is registered as a [money services business](/wiki/economics/finance/regulation/money-services-business) in the United States or licensed wherever it claims to be — on the regulator's own register, not on the operator's website. Registration is a weak signal about honesty and a strong one about reachability: a registered entity has an address, a named compliance officer, and an examination history.

## Where the law lands

Prosecutions run on wire fraud and money laundering rather than anything crypto-specific, with operating an unlicensed money transmitting business (18 U.S.C. § 1960) available where the service touched the United States. The binding constraint is location rather than statute: Özer was extradited from Albania roughly two years after leaving Turkey, and cases where the operator reaches a jurisdiction without an extradition treaty tend to end at asset tracing. The proceeds still have to be [cashed out](/wiki/economics/finance/fraud/cashing-out) to be worth anything, which is where the [anti-money laundering](/wiki/economics/finance/regulation/anti-money-laundering) system gets its only real look at them.

## External links

- [Ontario Securities Commission review of QuadrigaCX](https://www.osc.ca/quadrigacxreport) — the 2020 staff report, including the finding that it operated as a Ponzi scheme
- [Vitalik Buterin on proof of solvency](https://vitalik.eth.limo/general/2022/11/19/proof_of_solvency.html) — what Merkle-tree reserve proofs establish and where they stop
- [Chainalysis blog](https://www.chainalysis.com/blog/) — darknet market exit scam tracking and the annual Crypto Crime Report
- [Elliptic blog](https://www.elliptic.co/blog) — tracing write-ups on exchange and marketplace collapses
- [Justice Department news releases](https://www.justice.gov/news) — US charges against exchange and darknet market operators
