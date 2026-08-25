---
title: "Zelle Tag"
weight: 25
---

A Zelle tag is a handle — `brooklynbarbeque` — that a small business claims inside the Zelle network and prints on a menu, a receipt, or a storefront window. Customers pay it the way they would pay a phone number, and the money lands in the business's deposit account in minutes.

It is the third kind of [Zelle alias](/wiki/economics/finance/payments/zelle/alias#three-kinds-of-alias), and the only one the network issues rather than takes on faith from a mobile carrier or a mail provider. That difference determines who can steal it, whether a mistaken payment can be cancelled, what the sender can verify before sending, and what a business's customers give up so that the business can be paid instantly and for free.

## The specification

- **Six to forty characters.** Letters, digits, and hyphens. No spaces, no other punctuation.
- **Not case sensitive.** `BrooklynBarbeque` and `brooklynbarbeque` are the same tag, which closes one impersonation route: nobody can register the capitalised twin of your handle and wait for a customer to squint at it.
- **First come, first served,** across the entire network. There is one namespace, shared by every participating institution.
- **Claimed from inside the bank's app,** in the same Zelle settings screen where a phone number or email address is enrolled.
- **Small business accounts only.** As of mid-2026 a consumer can send to a tag but cannot claim one. Zelle announced the feature on 15 August 2025 and banks rolled it out through the end of that year.

```text
brooklynbarbeque      valid
brooklyn-barbeque     valid — and a different tag, held by someone else
Brooklyn-Barbeque     the same tag as brooklyn-barbeque
brooklyn barbeque     invalid (space)
bbq                   invalid (under six characters)
```

Nothing about a tag is verified, because there is nothing to verify. Enrolling a phone number means proving to the network that you control something administered elsewhere; enrolling a tag means only that nobody has taken it yet.

## Why the network issued them

Before the tag, a sole proprietor who wanted to accept Zelle had to publish a personal mobile number or an email address. Every barber with a number on a sandwich board was handing out an identifier that also receives their two-factor codes. The tag exists so that a payment address can be published without publishing anything else.

The commercial motive is the usual one. Zelle's purpose has always been to keep the payment — and therefore the deposit and the customer relationship — inside the bank's own app rather than a technology company's balance. At the consumer end that fight was largely won by 2020. At the merchant end it was not: a small business taking cards pays one and a half to three and a half percent in [interchange](/wiki/economics/finance/payments#the-rails), and a business taking [Venmo or Cash App](/wiki/economics/finance/payments/zelle/zelle-vs-alternatives#against-the-consumer-apps) has a handle, a profile, and a balance living outside the banking system. The tag is the bank consortium's answer to the handle. Zelle counted roughly seven million small businesses already enrolled when it launched the feature, with business payment volume up threefold over the prior three years.

## What changes when the network owns the namespace

A phone number or email address is an identifier you own somewhere else and merely assert to Zelle, so the strength of the binding is the strength of your carrier's or your mail provider's account security. A tag has no somewhere else. Three consequences follow, and they do not all point the same way.

**There is no upstream to compromise.** [Enrollment hijacking](/wiki/economics/finance/payments/zelle/alias#enrollment-hijacking) — the subscriber identity module (SIM) swap, the recycled phone number nobody de-enrolled — depends on taking over the identifier at the carrier or mail provider and then re-enrolling it. Neither attack has a foothold against a tag. Stealing one means compromising the bank login itself, which is a harder target defended by an institution that has run [know your customer](/wiki/economics/finance/regulation/know-your-customer) checks on the account holder.

**There is no out-of-band channel either, and that removes the safety net under a typo.** Paying any enrolled alias is [final within minutes](/wiki/economics/finance/payments/zelle/how-it-works#push-not-pull), so the tag takes nothing away from a payment that goes where it was meant to. It changes what happens when one doesn't. Mistype a phone number and there is a decent chance you have hit a number nobody enrolled, in which case the network texts an invitation and the payment sits [pending and cancellable](/wiki/economics/finance/payments/zelle/alias#the-unenrolled-recipient) for about fourteen days before the funds come back. A tag cannot be texted or emailed, because it exists nowhere outside Zelle, so there is no pending state to land in: a mistyped tag either fails to resolve outright or pays whoever registered it, immediately and for good. The same property that kills the hijacking attack removes the accident's grace period.

**There is nothing to correlate.** A payment address that is also a phone number links a business's takings to a personal identity in every other database that phone number appears in. A tag reveals what the business chose to publish and no more. For a sole proprietor that is a real privacy gain.

## Impersonation and squatting

A handle is chosen to be memorable, which means its near-misses are memorable too. The failures below are ordered by what they cost.

**A near-miss tag takes real money, permanently.** `brooklyn-barbeque` and `brooklynbarbeque` are different tags held by different people, and both look right on a flyer. A customer typing from memory, or from a counterfeit sign taped over the real one, will have the mistake resolve and the payment complete with [no recall path](/wiki/economics/finance/payments/zelle/how-it-works#push-not-pull). This is the same [misdirection failure](/wiki/economics/finance/payments/zelle/alias#misdirection-by-typo) that mistyped phone numbers produce, except that the near-misses are chosen rather than random, so an attacker can sit on the good ones and wait.

The mitigation is the name the bank displays before you confirm. It works when the customer knows what name to expect and fails when they do not, which describes most first-time payments to a business.

**There is no search, so the tag has to travel over a channel someone can imitate.** Zelle publishes no browsable directory: you cannot look up a business's tag from inside your bank's app, and there is no profile page to compare against. The tag reaches the customer on a receipt, a sign, an invoice, or a website — every one of which can be forged. This is the fake-payment-request problem [Venmo has](/wiki/economics/finance/payments/zelle/zelle-vs-alternatives#against-the-consumer-apps), arriving in a network with no reversal and no feed in which an impersonator looks out of place.

**First come, first served, with no published dispute process.** Domain registries run formal proceedings for trademark holders; [Early Warning Services](/wiki/economics/finance/payments/zelle/how-it-works#early-warning-services), the bank consortium that operates Zelle, has described nothing comparable, and a tag is not a trademark. What happens when a squatter takes the obvious handle of a well-known business has not been publicly tested. The practical advice for a business: claim the plausible variants of your own name before someone else does.

## What the business gets, and what the customer gives up

For the merchant, the credit lands in minutes and cannot be taken back, there is no interchange, and there are no chargebacks — the finality that makes Zelle dangerous for consumers is what a business wants. Zelle also issues no Form 1099-K — the information return that reports a payee's gross receipts to the tax authorities — on the position that the money moves bank to bank and the network never settles it, so Zelle is not the third-party settlement organization the reporting rule places the obligation on.

Each of those is a cost borne by someone else.

| | Card payment | Zelle tag |
|---|---|---|
| Merchant cost | 1.5–3.5% interchange | Free, or a flat bank fee |
| Funds available | Days, provisionally | Minutes, finally |
| Goods not received | Chargeback | No remedy |
| Wrong recipient | Reversible | Gone |

A customer paying a business by tag has made an authorized push payment, and [Regulation E](/wiki/economics/finance/regulation/regulation-e) covers *unauthorized* electronic transfers — not authorized ones the sender was deceived into making, and not goods that never arrived. That distinction is the [Zelle fraud argument](/wiki/economics/finance/payments/zelle/fraud-and-liability#authorized-and-unauthorized), and it bites hardest when the payee is a business, because a stranger on the other end is then the normal case rather than the suspicious one.

The absence of a form drives some of the adoption and is misread. No form arriving means no third party has told the Internal Revenue Service (IRS) what you took in; it does not mean you took in nothing reportable. Business income is income whichever rail carried it, and the only thing a tag changes is who else has a copy of the number.

## Adoption so far

Zelle reported more than one million small businesses enrolled with a tag by mid-2026, adding roughly three and a half thousand a day over the first half of that year. Set against the rest of Zelle's business numbers, that is a fast start from a small base: over eight million enrolled small business accounts moved more than $200 billion in the same period, of which the tag-enrolled businesses received about $5.8 billion across *all* their aliases combined.

So roughly one enrolled business account in eight holds a tag, and those accounts take about three percent of small-business volume. Zelle does not publish how much of that arrives *at* the tag rather than at the same business's phone number, so the figures say nothing about how people actually pay a business that has one. They do show adoption concentrated at the smaller end of small business, which is the population the feature was aimed at.

## Building on a tag

A tag is one flat, opaque string. A sender cannot vary part of it to mean something, the way a local part or a subdomain can be varied in an email alias, so a system that wants the *address* to carry an instruction cannot use one.

Most systems should not want that. [Interbox](/wiki/economics/finance/defi/interbox) receives on a single alias and [puts the routing in the payment memo](/wiki/economics/finance/defi/interbox#how-it-works), where it rides inside a signed message rather than in a string the sender retypes — which is why one address serves every asset and network it supports. A design shaped like that loses nothing to the tag's flatness, and gains what the tag offers: an address that can be printed publicly, with no carrier account-recovery desk standing behind it and no personal identifier disclosed by publishing it.

The blocker is eligibility, not fitness. Only small business accounts can claim a tag, so whether this is an option at all depends on what kind of account is receiving — and until that changes, a service accepting Zelle payments from the public is publishing an email alias whether or not a tag would suit it better.

## External links

- [Small businesses get their own handle with Zelle tag](https://www.zelle.com/blog/small-businesses-get-their-own-handle-zelle-tag) — the August 2025 announcement, including the character rules
- [Zelle: I was asked to send money to a Zelle tag](https://www.zelle.com/faq/i-was-asked-send-money-zelle-tag-small-business) — the consumer-facing account, and the small-business-only eligibility
- [Zelle: using Zelle with a small business account](https://www.zelle.com/faq/small-business) — eligibility, fees, and the tax reporting position
- [Zelle newsroom](https://www.zelle.com/newsroom) — where the adoption figures are published
