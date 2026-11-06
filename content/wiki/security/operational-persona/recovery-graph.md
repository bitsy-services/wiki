---
title: "Persona Recovery Graph"
weight: 20
---

A recovery graph is a directed graph with a node for each account or credential in an [operational persona](/wiki/security/operational-persona), and an edge from A to B wherever control of A is enough to take over or regain B. A persona is closed when no edge enters it from outside. An edge that does is a crossing: whoever controls its far end can get in, and the service storing it holds a record that connects the two sides.

Hammann and colleagues formalized the general structure in 2019 as an account access graph. "The primary authentication method for a user account is rarely the only way to access that account," their paper opens, naming recovery methods, password managers and single sign-on as the other routes. A later study drew the graphs of 20 participants under the title "I'm Surprised So Much Is Connected".

## One persona's graph

`brinewick` is the pseudonym of a developer called Ines. Here `A -> B` means control of A is enough to take B.

```text
registrar login               -> domain brinewick.example
domain brinewick.example      -> mail for @brinewick.example
mail for @brinewick.example   -> password reset at GitHub
mail for @brinewick.example   -> password reset at the registrar
printed codes                 -> GitHub, mail provider, registrar
ines@acme.example             -> password reset at the registrar    (crossing)
```

The last line is the defect. Ines registered the domain with the address she had open at the time. GitHub's records show no trace of her, yet a path runs from Acme's mail server to the `brinewick` account: anyone administering `ines@acme.example` can reset the registrar login, repoint the domain's mail and reset GitHub.

## What counts as an edge

| Route | Far end of the edge |
| --- | --- |
| Recovery address | The mailbox that receives reset links |
| SMS or voice code | The phone number, and so the carrier account behind it |
| Single sign-on ("Sign in with Google") | The provider account |
| Password manager or browser sync | The vault account, for every credential stored in it |
| Domain | The registrar and DNS host, for every address on the domain |
| Support desk | Whatever facts its script accepts |
| Postal mail, an unlocked phone | Physical access |

The support desk edge appears on no settings page. When the journalist Mat Honan's accounts were taken in 2012, the path ran through two support scripts: Amazon would display the last four digits of a card on file, and Apple accepted those digits with a billing address as proof of identity. "My accounts were daisy-chained together," Honan wrote. "Getting into Amazon let my hackers get into my Apple ID account, which helped them get into Gmail, which gave them access to Twitter."

## A crossing breaks both properties

Containment fails directly, as Honan's chain shows: whoever holds the far end can walk the path.

Unlinkability fails through the service, which has to store the far end in a form it can use. "We cannot encrypt this data as we need to be able to send an email to that address," Proton's spokesperson told TechCrunch in 2024, explaining a recovery address. The occasion was a set of court documents from a Spanish investigation into a pseudonymous activist. Served through Swiss police, Wire gave the email address registered on an account, a Protonmail address. Proton gave that mailbox's recovery address, an iCloud account. Apple gave a full name, two home addresses and a linked Gmail account. TechCrunch withheld the name, noting it was unclear whether that person was behind the activity.

The edge also leaks without a court. Reset forms show a masked hint so that the owner can recognize it, and Honan's attacker began by reading the masked recovery address on Google's recovery page, which showed enough characters to be useful. Martin Vigo's 2019 survey found services masking phone numbers differently, which lets the digits combine: eBay showed the first three and last two, LastPass the last four, giving seven of ten digits from an email address alone.

Bugs have gone further. From June 2021 until a report in January 2022, a flaw in Twitter's login flow told anyone who submitted a phone number or address which account held it, and Twitter's notice singled out "people with pseudonymous accounts who can be targeted by state or other actors". In 2025 Google retired a no-JavaScript username recovery form after a researcher showed it could reveal the phone number of any Google user.

## Closed is not enough

A closed graph can still lock its owner out. In the example, mail can reset the registrar and the registrar controls the mail, so losing both logins at once leaves neither able to restore the other.

A root is a node no online account can reset: printed codes, a hardware key, a memorized passphrase. Every node needs a path from a root that does not pass through the node itself. The registrar is the usual place to break a cycle: give its login a second mailbox at another provider, owned by the persona, so that it does not depend on the domain it controls.

There may be no backstop. "GitHub Support will not be able to restore access to accounts with two-factor authentication enabled if you lose your two-factor authentication credentials or lose access to your account recovery methods," GitHub's documentation says. Repeated identity proofing, the last resort elsewhere, ends a pseudonym wherever it is offered. Losing one device can be enough: in Büttner and Gruschka's 2023 survey, 17 of 91 Apple users and 10 of 94 Google users might lose access to their accounts along with their phones.

## The weakest path sets the strength

Alternatives add up to the weakest of them. An account that accepts a security key or an SMS code is as strong as the SMS code, and [the YubiKey page](/wiki/security/yubikey#webauthn-and-fido2) calls such a fallback "a second, weaker door". Büttner and Gruschka score graphs on this rule: a node reached by alternatives takes the minimum of their strengths, and a node that requires several factors together takes the maximum.

The strength of a recovery address is the strength of the whole graph behind that mailbox. Their scoring assigns "low" to a recovery address when the mailbox's own graph is unknown, which is the right assumption for a mailbox you have not drawn.

## Phone numbers

A recovery phone is the edge services push hardest, and it has measured value. Google reported in 2019 that an SMS code sent to a recovery number helped block 100% of automated bots, 96% of bulk phishing attacks and 76% of targeted attacks.

It fits unlinkability poorly. A number usually sits on a contract with a legal name, it works as a [global lookup key](/wiki/security/operational-persona/isolation-failures/shared-identifiers#values-nobody-typed), and it can be [moved by a SIM swap](/wiki/economics/fraud/sim-swap) or [reassigned](/wiki/security/operational-persona/lifecycle#what-expires).

A persona that needs containment alone can reasonably take that trade with a number of its own. A persona that needs unlinkability leaves the phone out wherever a service allows, and relies on hardware keys and printed codes. Where a service insists, the number is an account like any other: owned by the persona, listed in its inventory, used by no other persona.

## Check

1. List every account in the inventory, including the registrar, the mail host and anything opened with single sign-on.
2. Open each account's security settings and read the recovery screen as well as the login screen. [A number removed from one is often still live on the other](/wiki/economics/fraud/sim-swap#defence-in-order-of-effect).
3. Write one line per edge in the `A -> B` form above.
4. Mark every line whose left side is outside this persona's inventory. Each is a crossing. Replace it, starting with the crossing nearest the root.
5. Confirm that every node has a path from a root that does not pass through the node.
6. On a low-value account, use one printed code from a fresh browser profile, then regenerate the set. The drill shows that the codes work and that you can find them.

## Further reading

- Hammann, Radomirović, Sasse & Basin, [User Account Access Graphs](https://doi.org/10.1145/3319535.3354193), CCS 2019
- Hammann, Crabb, Radomirović, Sasse & Basin, ["I'm Surprised So Much Is Connected": A Study on Users' Online Accounts](https://doi.org/10.1145/3491102.3502125), CHI 2022
- Büttner & Gruschka, [Evaluating the Influence of Multi-Factor Authentication and Recovery Settings on the Security and Accessibility of User Accounts](https://arxiv.org/abs/2403.15080), ICISSP 2024
- Mat Honan, [How Apple and Amazon Security Flaws Led to My Epic Hacking](https://www.wired.com/2012/08/apple-amazon-mat-honan-hacking/), *Wired* (2012)
- Lorenzo Franceschi-Bicchierai, [Encrypted services Apple, Proton and Wire helped Spanish police identify activist](https://techcrunch.com/2024/05/08/encrypted-services-apple-proton-and-wire-helped-spanish-police-identify-activist/), *TechCrunch* (2024)
- Martin Vigo, [From email to phone number, a new OSINT approach](https://www.martinvigo.com/email2phonenumber/) (2019)
- Twitter, [An issue affecting some anonymous accounts](https://web.archive.org/web/2024/https://privacy.twitter.com/en/blog/2022/an-issue-affecting-some-anonymous-accounts) (2022), archived copy
- Brutecat, [Leaking the phone number of any Google user](https://brutecat.com/articles/leaking-google-phones) (2025)
- GitHub Docs, [Recovering your account if you lose your 2FA credentials](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/recovering-your-account-if-you-lose-your-2fa-credentials)
- Google Security Blog, [How effective is basic account hygiene at preventing hijacking](https://security.googleblog.com/2019/05/new-research-how-effective-is-basic.html) (2019)
