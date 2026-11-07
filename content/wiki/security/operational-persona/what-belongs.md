---
title: "What Belongs in an Operational Persona"
weight: 10
---

Four kinds of item belong in an [operational persona](/wiki/security/operational-persona), a set of accounts, credentials, recovery methods and technical context run as one identity: the accounts it holds, the credentials that prove control of them, the recovery methods that regain control when a credential is lost, and the technical context it acts from. The test for any single item has two parts. An item belongs to one persona when losing or leaking it affects no other persona, and when nothing it publishes appears on another persona's side.

An item that fails the test gets split into one per persona, dropped, or written down as an accepted exception in each persona that uses it. The inventory below belongs to `brinewick`, the pseudonym a developer called Ines uses for a hobby project. Her work identity, `ines@acme.example`, is a separate persona.

| Part | What it is | In `brinewick` |
| --- | --- | --- |
| Accounts | Records at services, with the identifiers they publish | Mailbox `brinewick@brinewick.example`, a second mailbox at another provider for the registrar login, domain registrar, GitHub, package registry, forum |
| Credentials | What proves control of an account | A password per account, `~/.ssh/hobby_ed25519`, a GPG key for its password store, one-time-password seeds, API tokens, the sessions in its browser profile |
| Recovery methods | What regains control after a credential is lost | Printed recovery codes, two security keys |
| Technical context | The environment the persona acts from | `~/hobby/` and its Git settings, the `github-hobby` SSH alias, a browser profile, a [`pass`](/wiki/security/pass) store |

## Accounts

The accounts that get forgotten are the ones nobody signs in to. A domain registrar controls the domain, the domain controls the mailbox, and the mailbox can reset most of the other accounts, so the registrar login is the most powerful item in the table and the least used. Mail and DNS hosting, package registries, continuous-integration services, cloud consoles and [coding assistants](/wiki/ai/claude-accounts/per-directory) each hold a login and a history of their own.

An account opened with a "Sign in with Google" button depends on the provider account behind the button, so that provider account belongs to the same persona. A payment card on file is part of the account as well, with [its own failure mode](/wiki/security/operational-persona/isolation-failures/payment-trail).

Every account publishes identifiers: a handle, an avatar, an address. Those values become [links](/wiki/security/operational-persona/isolation-failures/shared-identifiers) when they appear in two personas.

### One service, two personas

Each account belongs to one persona, so two personas that need one service need two accounts, and the service's terms decide whether that is allowed. GitHub's terms say "One person or legal entity may maintain no more than one free Account". Ines stays inside that sentence because her work account is a managed account, which Acme's identity provider creates inside Acme's paid enterprise, and `brinewick` is the one free account she maintains.

Without that, the options are one account and no separation at that service, a paid plan for the second, which puts [a card on file](/wiki/security/operational-persona/isolation-failures/payment-trail), or another code host, such as GitLab or Codeberg, for the pseudonym. Separate accounts for separate work differ from a second account that gets past a per-person limit, and the second kind [falls outside this section](/wiki/security/operational-persona#limits).

## Credentials

A credential is whatever a service accepts as proof of control: a password, a private key, a time-based one-time password (TOTP) seed, an API token. A session cookie counts too, as a service treats whoever presents it as signed in, and [a security key does nothing about a session an attacker already holds](/wiki/security/yubikey#webauthn-and-fido2).

A key's private half is a secret and its public half is an identifier. GitHub publishes each account's public keys at `https://github.com/<username>.keys`, so [one key on two accounts links them](/wiki/security/identity-separation#how-identities-get-linked). Each persona gets its own.

A hardware token divides by what it runs. A [security key's WebAuthn credentials](/wiki/security/yubikey#webauthn-and-fido2) can serve personas on different services: the specification's privacy section says authenticators ensure that credentials are "not correlatable as belonging to the same user", so that services can correlate users only through "additional information, e.g., a willfully reused username or e-mail address". The key is still one object, and losing it locks out every persona that relies on it. The OpenPGP applet on the same device has one slot each for a signing, a decryption and an authentication key, so a [GPG](/wiki/security/gpg) key held there serves one persona, and a second persona needs a second device.

## Recovery methods

The US National Institute of Standards and Technology (NIST) sorts account recovery into four classes in its digital identity guidelines.

| Class | What it is | What it brings into the persona |
| --- | --- | --- |
| Saved recovery codes | A secret issued at enrollment and kept offline | No new dependency, as long as the storage stays inside the boundary |
| Issued recovery codes | A code sent on request to a registered address: mailbox, phone or postal | An address, inside the boundary only if the persona owns it |
| Recovery contacts | A trusted person who receives the code | Someone outside who now knows the account exists |
| Repeated identity proofing | Proving identity again from documents | The legal name, which ends a pseudonym |

The paths these methods create form a [recovery graph](/wiki/security/operational-persona/recovery-graph). A phone number used for issued codes is itself an account at a carrier, with [the carrier's support desk in front of it](/wiki/economics/fraud/sim-swap).

## Technical context

[Technical context](/wiki/security/operational-persona/technical-context) is the environment the persona acts from. For the inventory, it means listing the directory that holds the repositories and their Git settings, the SSH configuration and agent, the browser profile, the password store and its remote, and the tool logins on disk. It also covers the operating-system user, whose home directory appears in stack traces; the time zone, which Git records in each commit; and the network route.

## What does not belong

Some parts come with the operator, the person acting as the persona, and cannot be split: writing style, waking hours, friends. They appear in no inventory and cross every boundary regardless. [Behavioural correlation](/wiki/security/operational-persona/isolation-failures/behavioural-correlation) and [social graph linkage](/wiki/security/operational-persona/isolation-failures/social-graph) are the failures that follow.

Other items are shared by choice or budget: one laptop, one home network, one security key. Write each down as an accepted exception in the inventory of every persona that uses it, with the failure it accepts and without naming the other persona. One laptop, for instance, accepts that [malware on it reaches every persona it holds](/wiki/security/operational-persona/technical-context#layers-of-separation).

## Check

```bash
# login files in default locations
ls -d ~/.config/gh/hosts.yml ~/.npmrc ~/.aws/credentials ~/.pypirc ~/.docker/config.json 2>/dev/null
```

Each path printed is a file every persona on this operating-system user reads, unless its tool is pointed elsewhere. The listing cannot see a system credential store, where [`gh` keeps its token by default](/wiki/security/operational-persona/technical-context#fail-closed).

Then go down the inventory and ask of each item which personas a leak would affect, and whether what it publishes appears anywhere else. A second name in either answer is a crossing, an item that spans the boundary. Split it or write it down.

## Further reading

- NIST, [SP 800-63B-4: Authentication and Authenticator Management](https://pages.nist.gov/800-63-4/sp800-63b.html), the section on account recovery
- W3C, [Web Authentication](https://www.w3.org/TR/webauthn-2/), section 14.2 on non-correlatable credentials
- [OpenPGP Smart Card Application](https://gnupg.org/ftp/specs/OpenPGP-smart-card-application-3.4.pdf), version 3.4.1, for the card's key slots
- GitHub, [Terms of Service](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service), section B.3, and [About Enterprise Managed Users](https://docs.github.com/en/enterprise-cloud@latest/admin/managing-iam/understanding-iam-for-enterprises/about-enterprise-managed-users)
