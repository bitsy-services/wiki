---
title: "Persona Lifecycle"
weight: 50
---

An [operational persona](/wiki/security/operational-persona), a managed set of accounts, credentials, recovery methods and technical context, is created root first, kept alive by signing in and testing recovery on a schedule shorter than its shortest expiry, rotated by adding each new part before removing the old one, and retired by closing accounts before their addresses lapse. Each part runs on its own clock, so a persona in occasional use can lose a part years before anyone notices.

## Creation order

1. Generate the offline root: a passphrase for the persona's key and a sheet to hold its recovery codes.
2. Build the [technical context](/wiki/security/operational-persona/technical-context): directory, Git and SSH settings, browser profile. All of this comes before any login.
3. From that context, open the mailbox and register the domain. Give the registrar login [a second mailbox at another provider](/wiki/security/operational-persona/recovery-graph#closed-is-not-enough), so that it does not depend on the domain it controls.
4. Open the other accounts one at a time, adding each to the [inventory](/wiki/security/operational-persona/cohesion#one-inventory-per-persona) with its recovery edges as it is created.
5. Publish last.

The order follows from what the first actions write. A first login leaves a row in the service's logs, and a first commit leaves a permanent record, so anything done before the context exists is done as someone else. [Separation is cheap early and nearly impossible late](/wiki/security/identity-separation#cheap-early-nearly-impossible-late).

## What expires

| Part | Clock | What follows |
| --- | --- | --- |
| Domain | The registration term, then a grace period, a redemption period and pending delete | Anyone can register it, set up mail and request password resets |
| Mailbox at a free provider | Two years without use at Google; one sign-in required every two years at Microsoft | The account and its contents can be deleted |
| Phone number | Disconnection, then an aging period of at least 45 days in the US | The carrier reissues it to someone else |
| Handle | A rename | On GitHub, the old name can be claimed by anyone |
| Signing key | The expiry date set at creation | New signatures stop verifying |
| Recovery codes | One use each | The last one spent leaves that path empty |
| Device holding one-time-password seeds | Loss or failure | The seeds go with it unless backed up |

The domain reaches every account at once, which makes it the worst case. PyPI, the Python package index, describes "a type of supply-chain attack where someone buys an expired domain and uses it to take over PyPI accounts through password resets", and it happened to the `ctx` package in 2022. PyPI's generalized timeline gives a renewal grace period of 0 to 45 days, a 30-day redemption period and 5 days of pending delete, after which the domain is released. Since June 2025 it has unverified over 1,800 addresses on domains entering those phases.

Phone numbers fail the same way on a larger scale. Lee and Narayanan report that 35 million US numbers are disconnected each year and reissued as standard practice. Of 259 available numbers they sampled at two carriers, 171 still had a linked account on at least one of six popular websites. When they held 200 recycled numbers for a week, 19 kept receiving sensitive calls and messages, such as authentication passcodes.

On GitHub, a changed username "becomes available for anyone else to claim", and if the new owner creates a repository with the same name as an old one, that "will override the redirect entry". A key's expiry is gentler: GitHub stores a verification record for each commit it has verified, and those commits stay verified "even if signing keys are rotated, revoked, or if contributors leave the organization".

## Exercise

Once a year beats every inactivity timer in the table. Sign in to each account from the persona's own context, read its recovery settings against the inventory, use one recovery code and regenerate the set, renew whatever is due, and update the inventory's `exercised:` line.

The context matters here. A convenience login from another browser or network, made only to keep an account alive, writes the kind of [link between personas](/wiki/security/operational-persona/isolation-failures) that the boundary exists to prevent. Renewal notices go to the persona's mailbox, so the mailbox needs reading too.

## Rotation

Credentials and identifiers rotate differently. A password or token can change at any time, unseen. A key has a public half that others may rely on: add the new key to each account, sign it with the old one where the format allows, and only then remove the old one.

An identifier (address, handle, domain) is a move. Add the new address to each account, make it the recovery address, and keep the old address receiving mail until the last account has moved. In every case the new path is in place and tested before the old one is cut.

After a compromise, walk the [recovery graph](/wiki/security/operational-persona/recovery-graph) forward from the compromised node. Every node it has an edge to is compromised too, and rotation runs from the root outward. A walk that reaches another persona has found a path that should not exist, and that persona needs the same treatment.

## When a link is discovered

A link between personas cannot be repaired, since [an observer who has seen it keeps what it learned](/wiki/security/identity-separation#cheap-early-nearly-impossible-late). What happens next depends on the persona's purpose. If it still needs containment alone, it carries on, and only its unlinkability is gone. If unlinkability was the reason for its existence, retire it and start another, carrying over no handle, key, address or recovery method.

## Retirement

1. Close or hand over each account, working from the leaves of the recovery graph towards the root.
2. Keep the domain registered until no live account names an address on it. Keep it longer if the address appears anywhere you cannot change, such as package metadata. Whoever registers it next receives what is sent to it.
3. Revoke any key others might trust.
4. Delete the local context: the directory, the browser profile, the agent and the tool logins.
5. Destroy the inventory last, since the earlier steps need it.

## Further reading

- PyPI, [Preventing Domain Resurrection Attacks](https://blog.pypi.org/posts/2025-08-18-preventing-domain-resurrections/) (2025), and the [`ctx` advisory](https://python-security.readthedocs.io/pypi-vuln/index-2022-05-24-ctx-domain-takeover.html)
- Google, [Inactive Google Account Policy](https://support.google.com/accounts/answer/12418290), and Microsoft, [Services Agreement](https://www.microsoft.com/en-us/servicesagreement), section on account use
- Lee & Narayanan, [Security and Privacy Risks of Number Recycling at Mobile Carriers in the United States](https://recyclednumbers.cs.princeton.edu/), eCrime 2021
- GitHub Docs, [About commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification) and [Username changes](https://docs.github.com/en/account-and-profile/concepts/username-changes)
