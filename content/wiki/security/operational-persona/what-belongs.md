---
title: "What Belongs in an Operational Persona"
weight: 10
---

Four kinds of item belong in an [operational persona](/wiki/security/operational-persona), the managed set of identity parts that acts as one unit: the accounts it holds, the credentials that prove control of them, the recovery methods that regain control when a credential is lost, and the technical context it acts from. The test for any single item is what its loss would touch. An item belongs to a persona when losing or leaking it affects that persona and no other.

An item that fails the test gets split into one per persona, dropped, or recorded as a shared exception. The inventory below belongs to `brinewick`, the pseudonym a developer called Ines uses for a hobby project.

| Part | What it is | In `brinewick` |
| --- | --- | --- |
| Accounts | Records at services, with the identifiers they publish | Mailbox `brinewick@brinewick.example`, domain registrar, GitHub, package registry, forum |
| Credentials | What proves control of an account | A password per account, `~/.ssh/hobby_ed25519`, one-time-password seeds, API tokens, the sessions in its browser profile |
| Recovery methods | What regains control after a credential is lost | Printed recovery codes, a second security key |
| Technical context | The environment the persona acts from | `~/hobby/` and its Git settings, the `github-hobby` SSH alias, a browser profile, a [`pass`](/wiki/security/pass) store |

## Accounts

The accounts that get forgotten are the ones nobody signs in to. A domain registrar controls the domain, the domain controls the mailbox, and the mailbox can reset most of the other accounts, so the registrar login is the most powerful item in the table and the least used. Mail and DNS hosting, package registries, continuous-integration services, cloud consoles and [coding assistants](/wiki/ai/claude-accounts/per-directory) each hold a login and a history of their own.

An account opened with a "Sign in with Google" button depends on the provider account behind the button, so that provider account belongs to the same persona. A payment card on file is part of the account as well, and [money has its own failure mode](/wiki/security/operational-persona/isolation-failures/payment-trail).

Each account belongs to one persona. Two personas that need the same service need two accounts, and [some services forbid that](/wiki/security/identity-separation#the-case-against).

Every account publishes identifiers: a handle, an avatar, an address. Those values are harmless inside one persona and become [links](/wiki/security/operational-persona/isolation-failures/shared-identifiers) when they appear in two.

## Credentials

A credential is whatever a service accepts as proof of control: a password, a private key, a time-based one-time password (TOTP) seed, an API token. A session cookie counts too. A service treats whoever presents it as signed in, and [a security key does nothing about a session an attacker already holds](/wiki/security/yubikey#webauthn-and-fido2).

A key has two halves with different jobs. The private half is a secret, and the public half is an identifier: GitHub publishes each account's public keys at `https://github.com/<username>.keys`, so [one key on two accounts links them](/wiki/security/identity-separation#how-identities-get-linked). Each persona gets its own.

Hardware tokens divide by what they run. A [security key's WebAuthn credentials](/wiki/security/yubikey#webauthn-and-fido2) can serve two personas: the W3C specification requires credentials to be "not correlatable as belonging to the same user", as long as the username and address differ. The key is still one object, and losing it locks out both. The OpenPGP applet on the same device has one slot each for a signing, a decryption and an authentication key, so a [GPG](/wiki/security/gpg) key held there serves one persona, and a second persona needs a second device.

## Recovery methods

The US National Institute of Standards and Technology (NIST) recognizes four classes of account recovery in its digital identity guidelines, and each brings something different into the persona.

| Class | What it brings in | Where it leads |
| --- | --- | --- |
| Saved recovery codes | A secret kept offline | Stays inside the boundary, as far as the storage does |
| Issued recovery codes | An address: mailbox, phone or postal | Inside only if the persona owns that address |
| Recovery contacts | Another person, who receives the code | Outside, to someone who now knows the account exists |
| Repeated identity proofing | Identity documents | To the legal name, which ends a pseudonym |

The paths these methods create form a [recovery graph](/wiki/security/operational-persona/recovery-graph), which is the structure to inspect. A phone number used for issued codes is itself an account at a carrier, with [the carrier's support desk in front of it](/wiki/economics/fraud/sim-swap).

## Technical context

[Technical context](/wiki/security/operational-persona/technical-context) is the environment the persona acts from. For the inventory, it means listing the directory that holds the repositories and their Git settings, the SSH configuration and agent, the browser profile, the password store and its remote, and the tool logins on disk. It also covers the operating-system user, whose home directory appears in stack traces; the time zone, which Git records in each commit; and the network route.

## What does not belong

Some parts come with the operator, the person acting as the persona, and cannot be split: legal identity, writing style, waking hours, friends. They appear in no inventory and cross every boundary regardless. [Behavioural correlation](/wiki/security/operational-persona/isolation-failures/behavioural-correlation) and [social graph linkage](/wiki/security/operational-persona/isolation-failures/social-graph) are the failures that follow.

Other items are shared by choice or budget: one laptop, one home network, one security key. Record each as a shared exception in every persona that uses it, along with the failure it accepts. One laptop, for instance, accepts that [malware on it reaches every persona it holds](/wiki/security/operational-persona/technical-context#layers-of-separation).

## Check

```bash
# login files in default locations
ls -d ~/.config/gh/hosts.yml ~/.npmrc ~/.aws/credentials ~/.pypirc ~/.docker/config.json 2>/dev/null
```

Each path printed is a file every persona on this operating-system user reads, unless its tool is pointed elsewhere.

Then go down the inventory and ask of each item which personas a leak would affect tomorrow. An answer with two names is a crossing, an item that spans the boundary. Split it or record it.

## Further reading

- NIST, [SP 800-63B-4: Authentication and Authenticator Management](https://pages.nist.gov/800-63-4/sp800-63b.html), the section on account recovery
- W3C, [Web Authentication](https://www.w3.org/TR/webauthn-2/), section 14.2 on non-correlatable credentials
- [OpenPGP Smart Card Application](https://gnupg.org/ftp/specs/OpenPGP-smart-card-application-3.4.pdf), version 3.4, for the card's key slots
