---
title: "Payments"
weight: 15
bookCollapseSection: true
---

Moving money between two people is not one problem but two, and most of what is confusing about payment systems comes from conflating them. The first is **messaging**: telling somebody that a transfer should happen, from whom, to whom, and for how much. The second is **settlement**: the moment the obligation between the two institutions is actually discharged and nobody can take it back. Systems that look identical to the person tapping *send* can differ completely in how they answer those two questions, and the difference is what determines whether a mistake can be undone.

This section covers the rails that answer them in the United States, and in particular [Zelle](/wiki/economics/finance/payments/zelle) — the bank-owned network that most Americans now touch weekly, and the one [Interbox](/wiki/economics/finance/defi/interbox) is built on top of.

## The rails

The US has no single payment system. It has five, layered by age, and each embeds the assumptions of the era that produced it.

**The automated clearing house (ACH)** is the batch rail, and by volume the backbone: payroll, bill pay, and most account-to-account transfers. Instructions are collected into files, exchanged between two operators — the Federal Reserve's FedACH and The Clearing House's Electronic Payments Network — and settled net at fixed windows. Same-day windows exist, but the default experience is one to three business days. It is governed by the Nacha operating rules, and an entry can be *returned* after the fact.

**Wires** are the real-time gross settlement rail. Fedwire, run by the Federal Reserve, and CHIPS — the Clearing House Interbank Payments System, privately operated and netted — move large values with finality: once the receiving bank is credited, there is no mechanism to reverse it. They cost tens of dollars, run only on business days, and are correspondingly rare in consumer life.

**Card networks** invert the model. A card payment is a *pull*: the merchant asks your bank for money, and the request travels through an acquirer, a network, and an issuer, each taking a cut. Authorization, clearing, and settlement are three separate events, days apart. The reversibility that makes chargebacks possible is the whole product, and the interchange that pays for it is why cards cost merchants one and a half to three and a half percent.

**Instant rails** are the modern answer: real-time payments (RTP), launched by The Clearing House in 2017, and FedNow, launched by the Federal Reserve in 2023. Both are credit-push only, run 24/7/365, settle in seconds with immediate finality, and carry rich remittance data in the ISO 20022 message format. Both are still fighting for reach — a rail is only as useful as the fraction of banks that receive on it.

**Peer-to-peer (P2P) overlays** sit on top of the rest. [Zelle](/wiki/economics/finance/payments/zelle), Venmo, Cash App and PayPal are not rails at all; they are directories and user experiences that resolve a phone number or email address to a place money can go, then hand the actual movement to one of the four rails below them. What distinguishes them from each other is mostly *where the money sits in between*.

## Reversibility is the real axis

Speed is what payment systems advertise. Reversibility is what they actually differ on, and the two trade against each other directly, because a transfer can only be undone while somebody still holds the money.

```text
reversible <----------------------------------------------> final
  cards          ACH            Zelle        RTP / FedNow     wire
  (chargeback)   (return        (no consumer  (irrevocable    (irrevocable
                 window)         recall)       by design)      by design)
```

Every rail to the right of the middle made the same bargain: give up the ability to claw a payment back, and in exchange the recipient can be paid immediately without the sender's bank carrying credit risk. That is a good trade for a business receiving funds and a bad one for a consumer who has just been talked into paying a stranger — which is why the [fraud problem](/wiki/economics/finance/payments/zelle/fraud-and-liability) shows up on instant rails specifically, and why [Regulation E](/wiki/economics/finance/regulation/regulation-e), written in 1978 for a world of card-based errors, fits them so badly.

It is also the property that makes these rails legible to anyone who has worked on a [blockchain](/wiki/economics/finance/defi/blockchain). An irrevocable credit-push payment to an address you cannot verify is exactly the model, and exactly the failure mode, of a token transfer — the difference being that a bank knows its customer's name and a chain does not.

## Wiki Pages

{{< section >}}
