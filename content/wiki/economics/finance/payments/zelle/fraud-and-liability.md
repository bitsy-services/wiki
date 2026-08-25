---
title: "Fraud and Liability"
weight: 30
---

Zelle's fraud problem follows from two decisions taken together: build an irrevocable payment system for consumers, and decline to decide who bears the loss when a consumer is tricked into using it.

The mechanics are covered in [how it works](/wiki/economics/finance/payments/zelle/how-it-works) and [the Zelle alias](/wiki/economics/finance/payments/zelle/alias). This page is about the legal question they produce, which remains genuinely unresolved in the United States and has been settled elsewhere.

## Authorized and unauthorized

US consumer payment law divides electronic fraud into two categories, and the dispute is entirely about where the line between them falls.

**Unauthorized transfers** are those initiated by somebody other than the account holder without actual authority. A stolen debit card, a compromised login, a payment pushed by an intruder. [Regulation E](/wiki/economics/finance/regulation/regulation-e) — the rule implementing the Electronic Fund Transfer Act (EFTA) — squarely covers these. The consumer reports the error, the bank investigates, and liability is capped at $50 or $500 depending on how quickly it was reported. The bank bears the rest.

**Authorized push payment (APP) fraud** is different in one respect only: the victim pressed send. Somebody impersonating the bank's fraud department, or a landlord, or a contractor, or a romantic interest, persuaded them to make a payment they genuinely intended to make, to a recipient they genuinely intended to pay, on the basis of a false belief. Every technical control worked exactly as designed.

The industry's long-standing position is that Regulation E's error-resolution rights attach only to the first category, because the statute defines the protected event as an *unauthorized* transfer, and a payment the consumer initiated is authorized whatever induced it. That reading is not obviously wrong as a matter of text. It is also, applied to an instant irrevocable rail, a rule that places the entire loss on the party least equipped to detect the fraud.

```text
  Who pressed send?
        |
    +---+------------------------+
    |                            |
  a thief                    the victim
    |                            |
  "unauthorized"          "authorized push payment"
    |                            |
  Regulation E applies      Regulation E, as the banks
  bank absorbs the loss     read it, does not apply
                            consumer absorbs the loss
```

Two things make that line less crisp than it looks. When a scammer harvests credentials and makes the transfer themselves, it is unauthorized even though the victim handed over the credentials — the [CFPB](/wiki/economics/finance/regulation/regulation-e#the-cfpb-position) has been explicit that fraudulently induced credential disclosure does not convert the resulting transfer into an authorized one. And a bank's own conduct in handling a claim can be actionable independently of whether Regulation E requires reimbursement.

## Why the shape of the network amplifies it

Three of Zelle's design choices compound in a way none of them would alone.

**Irrevocability with a consumer user base.** Wire transfers are irrevocable too, but sending one requires visiting a branch or navigating a deliberately friction-laden flow, and the population that sends them skews commercial and experienced. Zelle put the same finality behind two taps in a banking app that more than 150 million US accounts are enrolled in.

**The bank's brand as the wrapper.** Because Zelle lives inside the bank's own app, the transaction carries the bank's implied endorsement. That endorsement is what makes the most effective scam category work: an impersonator claiming to be the bank's fraud team, instructing the victim to "move your money to a safe account." The victim believes the institution whose app they are using is the one protecting them.

**No party owns the dispute.** A card network has an arbitration process because the network sits between two banks with a rulebook and a fee stream to fund it. Zelle inherited its governance from a fraud-data consortium, not a card scheme. Early Warning Services operates the directory; the sending and receiving banks are the only parties with a customer, and neither has a contractual obligation to the other's.

## What has happened so far

**2022–2023: political pressure and a voluntary rule.** Sustained congressional attention, mostly from Senator Elizabeth Warren's office, pushed the banks to concede a subset of the problem. Effective mid-2023, participating institutions agreed to reimburse victims of *imposter* scams — where the fraudster posed as a bank or a government agency — going beyond what Regulation E requires. The concession is narrow by construction: it covers the scams where the bank's own brand was the lure, and not romance scams, marketplace scams, invoice fraud, or fake investment platforms.

**July 2024: the Senate report.** The Permanent Subcommittee on Investigations published findings on the three largest Zelle banks, reporting roughly $166 million in disputed scam and fraud claims across those institutions in 2023, and a reimbursement rate on unauthorized-transfer claims that had fallen sharply since 2019. The subcommittee's framing was that the banks had been slow to reimburse even in the category they conceded was covered.

**December 2024: the CFPB sues.** The Consumer Financial Protection Bureau (CFPB) filed suit against Early Warning Services, Bank of America, JPMorgan Chase, and Wells Fargo, alleging that they had rushed Zelle to market without adequate identity verification or fraud controls and had failed to investigate claims properly, with consumer losses exceeding $870 million over seven years. Notably, much of the complaint targeted the [enrollment problem](/wiki/economics/finance/payments/zelle/alias#enrollment-hijacking) — aliases that could be claimed and re-claimed with little verification — rather than resting solely on the authorized-versus-unauthorized line.

**March 2025: the CFPB dismisses its own case.** Following a change of administration and a broad retreat from pending enforcement, the Bureau voluntarily dismissed the suit with prejudice. Nothing was adjudicated. The legal question the complaint raised is exactly as open as it was before it was filed, and the venue has shifted towards state attorneys general and private litigation.

## How other countries answered

The United Kingdom faced the identical problem on Faster Payments and resolved it by regulation rather than litigation. Since 7 October 2024, the Payment Systems Regulator's rules make reimbursement of authorized push payment fraud **mandatory**, with the cost split evenly between the sending firm and the receiving firm, subject to a per-claim maximum and an optional small excess. Consumers who were not grossly negligent get their money back by default.

The rule's effect comes from the split. Making the *receiving* institution liable for half creates the only incentive that has ever meaningfully reduced this category of fraud: banks now have a direct financial reason to care about the accounts opened on their own books that exist to receive scam proceeds. Reimbursement rules aimed solely at the sending bank leave the mule-account pipeline untouched, because the institution hosting it bears none of the cost.

No US rule allocates loss to the receiving institution. That, more than the Regulation E argument, is the structural gap.

## What this means if you are building on it

For anyone integrating Zelle — including [Interbox](/wiki/economics/finance/defi/interbox), which treats an inbound Zelle payment as the trigger for an irreversible action on the other side — two things follow.

An inbound Zelle payment is, as a matter of network mechanics, final. There is no clawback the sender's bank can compel. That is what makes it usable as a settlement trigger, and it is the same property that makes the network attractive to fraudsters, so the two cannot be separated: any flow that converts a Zelle credit into something non-refundable is, by construction, a good cash-out for someone else's scam. The controls have to sit in the flow itself — an out-of-band confirmation with the sender before anything irreversible happens, velocity limits, and the willingness to freeze and return on suspicion — because the rail supplies none.

The identity signal is real but thin. A Zelle payment tells you a regulated US institution has performed [know your customer](/wiki/economics/finance/regulation/know-your-customer) checks on the sender, which is a stronger assertion than almost anything available on a [blockchain](/wiki/economics/finance/defi/blockchain). It does not tell you the sender understood what they were doing. A system that knows whose money was taken is not thereby a system that is hard to defraud.

## External links

- [CFPB v. Early Warning Services (complaint)](https://www.consumerfinance.gov/enforcement/actions/early-warning-services-llc-bank-of-america-na-jpmorgan-chase-bank-na-wells-fargo-bank-na/) — the case, including its voluntary dismissal
- [Senate Permanent Subcommittee on Investigations: Zelle fraud](https://www.hsgac.senate.gov/subcommittees/investigations/) — the 2024 report and hearing record
- [UK Payment Systems Regulator: APP fraud reimbursement](https://www.psr.org.uk/our-work/app-scams/) — the mandatory-reimbursement regime and the 50/50 split
- [FBI Internet Crime Complaint Center annual report](https://www.ic3.gov/AnnualReport/Reports) — where US scam-loss figures by category are published
