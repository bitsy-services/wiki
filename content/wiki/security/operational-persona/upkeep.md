---
title: "Persona Upkeep"
weight: 50
---

The parts of an [operational persona](/wiki/security/operational-persona), a set of accounts, credentials, recovery methods and technical context run as one identity, expire on separate clocks, and a persona in occasional use can lose a part years before anyone notices. Upkeep means signing in and testing recovery more often than the shortest of those clocks, and changing a part by adding the new one before removing the old.

## What expires

| Part | Clock | What follows |
| --- | --- | --- |
| Domain | The registration term, then a grace period, a redemption period and pending delete | Anyone can register it, set up mail and request password resets |
| Mailbox at a free provider | Two years without use at Google. At Microsoft, a sign-in every year for an Outlook.com inbox and every two years for the account | The account or inbox can be closed or deleted, with its contents |
| Phone number | Disconnection, then an aging period of at least 45 days in the US | The carrier reissues it to someone else |
| Handle | A rename | On GitHub, anyone can claim the old name |
| GPG signing key | The expiry date set at creation | New signatures stop verifying |
| Recovery codes | One use each | The last one spent empties that path |
| Device holding one-time-password seeds | Loss or failure | The seeds go with it unless backed up |

A domain reaches every account on it that has no second factor. PyPI, the Python package index, describes "a type of supply-chain attack where someone buys an expired domain and uses it to take over PyPI accounts through password resets". When it happened to the `ctx` package in 2022, the owner account had no second factor. The password reset came 12 minutes after the domain was registered, and the first malicious upload 38 minutes after. PyPI says accounts active since January 2024 have a second factor, which an attacker would also need short of a full account recovery, and since June 2025 it has unverified over 1,800 addresses on domains entering expiry. Its generalized timeline gives a renewal grace period of 0 to 45 days, a 30-day redemption period and 5 days of pending delete before the domain is released.

Phone numbers fail the same way. Lee and Narayanan report that 35 million US numbers are disconnected each year and reissued as standard practice. Of 259 available numbers they sampled at two carriers, 171 still had a linked account on at least one of six popular websites. When they held 200 recycled numbers for a week, 19 kept receiving sensitive calls and messages, such as authentication passcodes.

On GitHub, a changed username "becomes available for anyone else to claim", and if the new owner creates a repository with the same name as an old one, that "will override the redirect entry". A GPG key's expiry is gentler. GitHub stores a verification record when it verifies a commit, and within the repository's network that commit stays verified "even if signing keys are rotated, revoked, or if contributors leave the organization".

## Exercise

Twice a year beats every inactivity timer in the table. Sign in to each account, read its recovery settings against the [inventory](/wiki/security/operational-persona/cohesion#one-inventory-per-persona), and renew whatever is due. On one account each round, use a recovery code and store the new set. Then update the `exercised:` date on each inventory entry.

Run this from the persona's own [context](/wiki/security/operational-persona/technical-context). A convenience login from another browser or network, made only to keep an account alive, writes the kind of [link between personas](/wiki/security/operational-persona/isolation-failures) that the boundary exists to prevent. Renewal notices go to the persona's mailbox, so the mailbox needs reading too.

## Rotation

Credentials and identifiers rotate differently. A password or token can change at any time, unseen. A key has a public half that others may rely on: add the new key to each account, sign it with the old one where the format allows, and only then remove the old one.

An identifier (address, handle, domain) is a move. Add the new address to each account, make it the recovery address, and keep the old address receiving mail until the last account has moved. A mailbox on a domain the persona owns avoids most of these moves, as the address stays when the mail provider changes, at the cost of one more part that can lapse. In every case the new path is in place and tested before the old one is cut.

After a compromise, walk the [recovery graph](/wiki/security/operational-persona/recovery-graph) forward from the compromised node. Every node it reaches is suspect, and rotation runs outward from the root, the offline item no online account can reset. A walk that reaches another persona has found a path that should not exist, and that persona needs the same treatment.

## When a link is discovered

A link between personas cannot be repaired, since [an observer who has seen it keeps what it learned](/wiki/security/identity-separation#cheap-early-nearly-impossible-late). What happens next depends on what the boundary was for. If it was for containment, so that a leak in one persona gives no control over another, the persona carries on. If it was for unlinkability, so that no observer could connect the two, retire the persona and start another with no handle, key, address or recovery method carried over.

A suspension is a different case. A new persona returning to a service that has barred its operator is [ban evasion, outside this section](/wiki/security/operational-persona#limits).

## Retiring a persona

Close or hand over each account before its address goes. Keep the domain registered until no live account names an address on it, and longer if the address appears somewhere you cannot change, such as package metadata: whoever registers it next receives what is sent to it. Revoke any key others might trust, and run `gh auth logout`, since a token in a system credential store outlives the deleted directory. Delete the local context, and destroy the inventory last.

## Further reading

- PyPI, [Preventing Domain Resurrection Attacks](https://blog.pypi.org/posts/2025-08-18-preventing-domain-resurrections/) (2025), and the [`ctx` advisory](https://python-security.readthedocs.io/pypi-vuln/index-2022-05-24-ctx-domain-takeover.html)
- Google, [Inactive Google Account Policy](https://support.google.com/accounts/answer/12418290), and Microsoft, [Services Agreement](https://www.microsoft.com/en-us/servicesagreement), section on account use
- Lee & Narayanan, [Security and Privacy Risks of Number Recycling at Mobile Carriers in the United States](https://recyclednumbers.cs.princeton.edu/), eCrime 2021
- GitHub Docs, [About commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification) and [Username changes](https://docs.github.com/en/account-and-profile/concepts/username-changes)
