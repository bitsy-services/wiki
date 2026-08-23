---
title: "Tokens and Enrollment"
weight: 20
---

Everything convenient about Zelle, and a large share of what goes wrong with it, comes from one substitution: instead of addressing a payment to a routing number and an account number, you address it to a **token** — a US mobile number or an email address.

A token is not an account. It is a lookup key in a directory operated by Early Warning Services, mapping the identifier to exactly one deposit account at one participating institution. Enrollment is the act of claiming a token; sending is a directory query followed by a [credit push](/wiki/economics/finance/payments/zelle/how-it-works#push-not-pull). The whole system is a naming layer, and it inherits the problems every naming layer has.

## Claiming a token

You enroll from inside your bank's app. The bank asserts to the network that you control the token, having verified it by a one-time code sent to the number or address, and the directory records the binding. Three rules govern it:

- **One token, one account.** A given phone number resolves to exactly one place. You cannot split incoming payments across two banks, and you cannot receive at a bank where the token is not enrolled.
- **Tokens are claimed, not assigned.** Nobody allocates you a Zelle identifier. You assert an identifier you already control elsewhere, and the strength of the binding is the strength of that assertion.
- **The binding is movable.** Enrolling the same token at a second institution moves it; the network re-points the directory entry, and the first bank stops receiving.

That last property is what makes switching banks possible without losing your payment address. It is also the seam.

## Enrollment hijacking

If the right to receive payments follows whoever most recently proved control of a phone number, then taking over the phone number takes over the payments. This is not a hypothetical: it is the standard playbook.

The attack has two common forms. In a **subscriber identity module swap**, the attacker convinces a mobile carrier to port the victim's number onto a SIM they hold, receives the enrollment code, and enrolls the token at an institution where they have opened an account. In a **stale-token takeover**, the attacker simply obtains a recycled phone number that its previous owner never de-enrolled — carriers reissue disconnected numbers within months — and inherits an enrollment nobody revoked.

Either way, payments intended for the victim arrive in the attacker's account, and the sender has no signal that anything is wrong, because from the sender's side the directory answered normally. The victim frequently learns of it only when someone asks why the money never arrived.

The defenses are all upstream of Zelle, which is the uncomfortable part: a carrier port-out lock, an authenticator app or [hardware authenticator](/wiki/security/yubikey) in place of SMS codes wherever the bank permits it, and the discipline of de-enrolling a token before giving up the number. Zelle's own contribution has been to shrink the attack surface — retiring the standalone app removed the easiest place to enroll a stolen token, since every remaining enrollment path now runs through an institution that has done [know your customer](/wiki/economics/finance/regulation/know-your-customer) checks on the person claiming it.

## Misdirection: the mundane failure

The dramatic failure gets attention; the common one is a typo.

Because a token is a short string chosen by humans, the adjacent strings are also valid tokens belonging to real people. Transpose two digits of a phone number and the directory will cheerfully resolve it, the payment will complete, and the money will be sitting in a stranger's account with [no recall path](/wiki/economics/finance/payments/zelle/how-it-works#push-not-pull). Bank interfaces mitigate this by displaying the registered first name and last initial of the resolved recipient before you confirm, which catches the case where you know the recipient's name and not the case where you were given the wrong number by a scammer.

Compare the same failure elsewhere. An [Ethereum](/wiki/economics/finance/defi/ethereum) address carries a checksum in the capitalisation of its hex digits, so a typo usually fails closed rather than resolving to a stranger. A wire transfer resolves an account number that is checkable against a name. A phone number has neither property: no check digits, no independent name binding, and a dense space in which nearly every neighbouring value is live.

## The unenrolled recipient

Sending to a token nobody has claimed is the one case where the transfer is not immediate, and consequently the one case where a sender can change their mind.

The network holds the instruction and notifies the token — a text message or an email — inviting the recipient to enroll at their bank in order to receive. Until they do, the payment is pending, and the sender can cancel it outright. If nobody enrolls within roughly fourteen days, the payment expires and the funds return.

This is worth knowing for two reasons. It is the only consumer-facing cancellation Zelle offers, so a sender who realizes their mistake within seconds should check whether the payment is still pending. And it is a race condition: an attacker who receives that invitation — because they hold the recycled number, or because a scam persuaded the victim to send to a token the attacker controls — can enroll on the spot and convert a cancellable pending payment into a final one.

## Designing on top of a token directory

For anything built on Zelle, the token is the interface, and it has properties worth naming explicitly.

The mapping is **opaque**: you cannot query the directory yourself, discover which bank holds a token, or verify a binding out of band. You learn the result only by sending. It is **mutable** without notice to counterparties — an address that worked last month may now point somewhere else, and nothing tells you. And it is **identity-adjacent but not identity**: the bank behind a token has verified a real person, which is exactly what makes the token valuable as an identity signal, but the directory exposes only a first name and last initial.

[Interbox](/wiki/economics/finance/defi/interbox) leans on the first and third of these deliberately. It publishes tokens of the form `usdc.polygon@inter.box`, so the *sender's* choice of destination address encodes the intended asset and network, and the bank's verification of the sender is what stands in for a repeated identity check. The mutability is handled the only way it can be: by treating each received payment as the authoritative event and confirming out of band before anything irreversible happens on the other side.

## External links

- [Zelle: enrollment](https://www.zellepay.com/faq) — the operator's account of tokens and enrollment
- [FCC: cell phone fraud and SIM swapping](https://www.fcc.gov/consumers/guides/cell-phone-fraud) — the carrier-side attack and what a port-out lock does
- [FCC number reassignment database](https://www.fcc.gov/reassigned-numbers-database) — the mechanism by which recycled numbers are meant to be detectable
