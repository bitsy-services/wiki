---
title: "Zelle Alias"
weight: 20
---

Everything convenient about Zelle, and a large share of what goes wrong with it, comes from one substitution: instead of addressing a payment to a routing number and an account number, you address it to an **alias** — a US mobile number, an email address, or a Zelle tag.

An alias is not an account. It is a lookup key in a directory operated by Early Warning Services, mapping the identifier to exactly one deposit account at one participating institution. Enrollment is the act of claiming an alias; sending is a directory query followed by a [credit push](/wiki/economics/finance/payments/zelle/how-it-works#push-not-pull). Zelle is a naming layer, and it inherits the problems every naming layer has.

## A note on the word

Early Warning's own network-side material calls these **tokens**, and that is the word you will meet in product briefs and integration documentation. *Alias* is the term in Zelle's consumer-facing terms, and it is what the wider faster-payments literature uses: an alias directory is the generic name for this component, and the ISO 20022 message field is called a proxy.

This page says *alias*, for two reasons. It is the broader term — a tag is an alias but is not a token in any useful sense. And *token* already means two other things a reader of this wiki will have met: the surrogate value that replaces a card number under network tokenization, and the on-chain asset.

## Three kinds of alias

Two of the three are identifiers you already own somewhere else and merely assert to Zelle. The third is issued by Zelle itself.

- **A US mobile number.** Landlines, international numbers, and 1-800 numbers are ineligible.
- **An email address.** Any address you can receive a one-time code at.
- **A [Zelle tag](/wiki/economics/finance/payments/zelle/tag).** A handle you choose — six to forty characters, letters, digits, and hyphens — introduced for small businesses in 2025 and, as of mid-2026, still available only to them. It exists inside Zelle and nowhere else, so a business can print it on a menu without publishing an owner's phone number.

## Claiming an alias

You enroll from inside your bank's app. For a phone number or email address, the bank asserts to the network that you control the alias, having verified it by a one-time code sent to the number or address, and the directory records the binding. For a tag there is nothing to verify — the network only checks that nobody has taken it already. Three rules govern the result:

- **One alias, one account.** A given phone number resolves to exactly one place. You cannot split incoming payments across two banks, and you cannot receive at a bank where the alias is not enrolled.
- **Contact aliases are claimed, not assigned; tags are the reverse.** Nobody allocates you a phone number or an email address for Zelle's benefit. You assert an identifier you already control elsewhere, and the strength of the binding is the strength of that assertion — which is to say, the strength of your carrier's or mail provider's account security. A tag inverts this: the network allocates it, first come, and it has no existence outside the network to be compromised.
- **The binding is movable.** Enrolling the same alias at a second institution moves it; the network re-points the directory entry, and the first bank stops receiving.

That last property is what makes switching banks possible without losing your payment address.

## Enrollment hijacking

If the right to receive payments follows whoever most recently proved control of a phone number, then taking over the phone number takes over the payments. It is the standard playbook, and it takes two common forms. In a **subscriber identity module swap**, the attacker convinces a mobile carrier to port the victim's number onto a SIM they hold, receives the enrollment code, and enrolls the alias at an institution where they have opened an account. In a **stale-alias takeover**, the attacker simply obtains a recycled phone number that its previous owner never de-enrolled — carriers reissue disconnected numbers within months — and inherits an enrollment nobody revoked.

Either way, payments intended for the victim arrive in the attacker's account, and the sender has no signal that anything is wrong, because from the sender's side the directory answered normally. The victim frequently learns of it only when someone asks why the money never arrived.

Zelle did not invent the weakness; it inherited it, by choosing identifiers whose security is administered by a mobile carrier or a mail provider. The defenses are correspondingly upstream: a carrier port-out lock, an authenticator app or [hardware authenticator](/wiki/security/yubikey) in place of SMS codes wherever the bank permits it, and the discipline of de-enrolling an alias before giving up the number. Zelle's own contribution has been to shrink the attack surface — retiring the standalone app removed the easiest place to enroll a stolen alias, since every remaining enrollment path now runs through an institution that has done [know your customer](/wiki/economics/finance/regulation/know-your-customer) checks on the person claiming it.

A tag has no upstream to compromise: taking one over means compromising the bank login itself, which is a harder and much better-defended target. [What that buys and what it costs the sender](/wiki/economics/finance/payments/zelle/tag#what-changes-when-the-network-owns-the-namespace) is the subject of its own page.

## Misdirection by typo

Because an alias is a short string chosen by humans, the adjacent strings are also valid aliases belonging to real people. Transpose two digits of a phone number and the directory resolves it, the payment completes, and the money will be sitting in a stranger's account with [no recall path](/wiki/economics/finance/payments/zelle/how-it-works#push-not-pull). Bank interfaces mitigate this by displaying the registered first name and last initial of the resolved recipient before you confirm, which catches the case where you know the recipient's name and not the case where you were given the wrong number by a scammer.

Tags do not fix this and may make it worse. A handle is chosen to be memorable, which means its near-misses are memorable too, and [a squatter holding the hyphenated variant of a restaurant's tag](/wiki/economics/finance/payments/zelle/tag#impersonation-and-squatting) is the Venmo impersonation problem arriving in a network with no reversal.

Compare the same failure elsewhere. An [Ethereum](/wiki/economics/finance/defi/ethereum) address carries a checksum in the capitalisation of its hex digits, so a typo usually fails closed rather than resolving to a stranger. A wire transfer resolves an account number that is checkable against a name. A phone number has neither property: no check digits, no independent name binding, and a dense space in which nearly every neighbouring value is live.

## The unenrolled recipient

Sending to a contact alias nobody has claimed is the one case where the transfer is not immediate, and consequently the one case where a sender can change their mind.

The network holds the instruction and notifies the alias — a text message or an email — inviting the recipient to enroll at their bank in order to receive. Until they do, the payment is pending, and the sender can cancel it outright. If nobody enrolls within roughly fourteen days, the payment expires and the funds return.

This case exists only for phone numbers and email addresses, because only they can be reached outside Zelle. An unclaimed tag has no owner and no channel on which to invite one, so it simply fails to resolve.

The pending window is the only consumer-facing cancellation Zelle offers, so a sender who realizes their mistake within seconds should check whether the payment is still pending. It is also a race condition: an attacker who receives that invitation — because they hold the recycled number, or because a scam persuaded the victim to send to an alias the attacker controls — can enroll on the spot and convert a cancellable pending payment into a final one.

## Designing on top of an alias directory

For anything built on Zelle, the alias is the interface. The mapping is **opaque**: you cannot query the directory yourself, discover which bank holds an alias, or verify a binding out of band. You learn the result only by sending. It is **mutable** without notice to counterparties — an address that worked last month may now point somewhere else, and nothing tells you. And it is **identity-adjacent but not identity**: the bank behind an alias has verified a real person, which is exactly what makes the alias valuable as an identity signal, but the directory exposes only a first name and last initial.

[Interbox](/wiki/economics/finance/defi/interbox) is built on the third of these. It receives on a single alias, `usd@inter.box`, and [carries the routing in the payment memo](/wiki/economics/finance/defi/interbox#how-it-works) rather than in the address, so the directory holds one binding no matter how many assets and networks the service supports. What the alias contributes is the bank's verification of the *sender*, which is what stands in for a repeated identity check. Opacity and mutability are handled the only way they can be: by treating each received payment as the authoritative event and confirming out of band before anything irreversible happens on the other side.

## External links

- [Zelle: enrollment](https://www.zellepay.com/faq) — the operator's account of aliases and enrollment
- [Zelle: small businesses get their own handle](https://www.zelle.com/blog/small-businesses-get-their-own-handle-zelle-tag) — the tag announcement
- [FCC: cell phone fraud and SIM swapping](https://www.fcc.gov/consumers/guides/cell-phone-fraud) — the carrier-side attack and what a port-out lock does
- [FCC number reassignment database](https://www.fcc.gov/reassigned-numbers-database) — the mechanism by which recycled numbers are meant to be detectable
