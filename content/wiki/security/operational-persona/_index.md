---
title: "Operational Persona"
weight: 50
bookCollapseSection: true
---

An operational persona is a deliberately managed set of accounts, credentials, recovery methods and technical context that acts as one identity, with a boundary separating it from other such sets. Its accounts recover through its own mailbox, its commits are signed with its own key, and its browser profile holds its own sessions.

Take the identities from [identity separation](/wiki/security/identity-separation): `Ines Varga <ines@acme.example>` at work, where Acme is her employer, and the pseudonym `brinewick` for a hobby project. The `brinewick` persona is a mailbox at `brinewick.example`, the registrar account that keeps that domain registered, a GitHub account, an SSH key for login and signing, printed recovery codes, the `~/hobby/` directory with its Git settings, and a browser profile. Ines is its operator, the person acting as it. Anything that spans the boundary, such as an item in two personas' inventories or a recovery path from one into the other, is a crossing.

Identity separation is the practice of keeping such sets apart, and its goal is an absence: no link between them. The persona is what that practice protects. Naming it lets the practice ask what is on each side, what holds each side together, and which items cross.

## What it is distinct from

### A single account

An account is one record at one service. A persona spans services and includes what no service holds: the key on disk, the codes on paper, the directory that selects the identity. If `brinewick` closes its GitHub account, the persona carries on with its mailbox, keys and remaining accounts.

Control decides what a persona contains, whatever a profile says. A GitHub account named `brinewick` whose password reset goes to `ines@acme.example` has a crossing in it: whoever controls that address can start the account's recovery, and can finish it if the account has no second factor.

### A social-media presentation persona

A presentation persona is the character an audience sees: the name, tone, avatar and subject matter an account shows. Marwick and boyd's study of Twitter users describes people shaping this for an "imagined audience", and the difficulty when social media collapses "multiple audiences into single contexts".

The two vary independently. One operational persona can carry a dry voice about compilers and a joking one about sailing. A writer who abandons a compromised set of accounts and starts again under the same name and voice has kept the presentation and replaced the operational persona. A new avatar changes no login or recovery path, and a new recovery mailbox changes nothing an audience can see. Building a community on a platform belongs to [Social](/wiki/social).

### The real-world person

The person has a legal name, a body, habits and friends. People and personas are many to many. One person can run several personas, and one persona can have several operators over time, as when a project's release account passes from one maintainer to the next with its keys and recovery codes. A persona can carry its operator's legal name, as Ines's work persona does, or a pseudonym, an optional attribute like any other.

The operator is also the component all of a person's personas share. Configuration can separate keys and cookies, while [habits](/wiki/security/operational-persona/isolation-failures/behavioural-correlation) and [contacts](/wiki/security/operational-persona/isolation-failures/social-graph) travel with the person.

## What the boundary holds

A boundary can promise containment, unlinkability or both. Containment means that losing or leaking one persona's credential gives no control over another. Unlinkability, the property identity separation is built around, means that an observer who sees both personas cannot tell they have one operator.

Ines has a third persona besides these two: personal accounts under her legal name. Anyone can know that she works at Acme and has those accounts, so the two need containment alone. Acme's administrators should have no route into her personal mail, and her personal accounts should survive the day she leaves. `brinewick` needs both properties. Its unlinkability is also relative to an observer, since keeping a pseudonym from the public is a smaller job than keeping it from a court, and [the ways isolation fails](/wiki/security/operational-persona/isolation-failures) sort by what each costs an observer.

## When to draw a boundary

Draw a new boundary when control, audience or stakes differ from those of every persona already running.

Control differs when someone else can reset the accounts. An employer's identity provider can reset or remove what it issues, so work accounts form their own persona, and personal accounts must not depend on them. Audience differs when what is published under one name should not reach the readers of another, the case [identity separation](/wiki/security/identity-separation#the-case-for) makes. Stakes differ when a compromise would cost far more than the rest would: a [key that moves funds](/wiki/security/pass#exported-private-keys) belongs in a persona that never browses the web.

Each persona is a complete set of items to [keep working](/wiki/security/operational-persona/upkeep), so the count stays at one per real difference. [How many Claude accounts](/wiki/ai/claude-accounts/how-many-accounts) reaches the same rule for a single product: one account for each organization whose code you work on.

## Limits

A persona changes what observers can connect, and obligations stay where they were. A bank must verify who its customer is under [know your customer](/wiki/economics/regulation/know-your-customer) rules, so a persona with a bank account has its operator's legal name in that bank's file. A domain registrant [owes accurate contact details](/wiki/security/operational-persona/isolation-failures/shared-identifiers#domain-records). Some services limit accounts per person, and [what belongs in a persona](/wiki/security/operational-persona/what-belongs#one-service-two-personas) covers GitHub's limit. A ban or suspension binds the person it was imposed on, and a new persona returning to that service is ban evasion, however clean its configuration.

Running several personas so that they pass as several independent people is a different act with its own names: a [Sybil attack](/wiki/economics/defi/sybil-resistance#the-attack) when the target is a network, a sock puppet when it is a forum. This section is about keeping your own contexts apart.

## Related terms

Pfitzmann and Hansen's privacy terminology calls the nearest object a *partial identity*, "a subset of attribute values of a complete identity" that represents "the person in a specific context or role", and calls administering such subsets *identity management*. Their definition covers attributes. *Operational persona*, this wiki's term, adds the machinery that keeps those attributes under control.

MITRE's ATT&CK knowledge base uses *persona* for something narrower: an identity an adversary builds for an operation, which "may be fictitious or impersonate real people". That is outside this section. Vendors of browsers for investigators sell control over what a target site can observe as *managed attribution*.

## Reading order

[What belongs in a persona](/wiki/security/operational-persona/what-belongs) lists the four kinds of item and gives a test for any one of them. [The recovery graph](/wiki/security/operational-persona/recovery-graph) draws the kind most often left unexamined as a structure of paths. [Technical context](/wiki/security/operational-persona/technical-context) covers the environment that selects the identity.

[Cohesion](/wiki/security/operational-persona/cohesion) and [upkeep](/wiki/security/operational-persona/upkeep) then cover how those parts stay one unit: agreeing with each other today, and still working in five years. [How persona isolation fails](/wiki/security/operational-persona/isolation-failures) sorts the ways a boundary breaks by what each costs an observer, with a page for each mechanism.

## Wiki Pages

{{< section >}}

## Further reading

- Pfitzmann & Hansen, [A terminology for talking about privacy by data minimization](https://dud.inf.tu-dresden.de/literatur/Anon_Terminology_v0.34.pdf), v0.34 (2010), section 13 on identity and partial identity
- [RFC 6973: Privacy Considerations for Internet Protocols](https://www.rfc-editor.org/rfc/rfc6973), for the definitions of unlinkability and pseudonym
- MITRE ATT&CK, [T1585: Establish Accounts](https://attack.mitre.org/techniques/T1585/)
- Marwick & boyd, [I tweet honestly, I tweet passionately: Twitter users, context collapse, and the imagined audience](https://doi.org/10.1177/1461444810365313), *New Media & Society* 13(1), 114–133
- Authentic8, [What is managed attribution?](https://authentic8.com/blog/what-is-managed-attribution), a vendor's definition
