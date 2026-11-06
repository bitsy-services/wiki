---
title: "How Persona Isolation Fails"
weight: 60
bookCollapseSection: true
---

Isolation between two [operational personas](/wiki/security/operational-persona), the sets of accounts and credentials one person runs as separate identities, fails when something belongs to both sides of the boundary: an identifier, an acquaintance, a recovery path, a browser or device, a network address, a company's records, a payment, or the habits of the operator, the person acting as both. Each gives an observer a way to join two sets of records that were meant to stay apart. The table orders them by what that join costs the observer, cheapest first.

| Failure | What crosses | Who can use it | Can configuration stop it? |
| --- | --- | --- | --- |
| [Shared identifier](/wiki/security/operational-persona/isolation-failures/shared-identifiers) | A handle, address, key, phone number or analytics ID on both sides | Anyone with a search engine | Yes, before it is published |
| [Social graph](/wiki/security/operational-persona/isolation-failures/social-graph) | Follows, contacts, people who know both | Anyone, where follow lists are public; otherwise the platform | Only by keeping the circles apart |
| [Recovery crossing](/wiki/security/operational-persona/recovery-graph#a-crossing-breaks-both-properties) | A reset or login path from one persona into the other | Whoever holds the far end; strangers, through hints on reset forms; the service, when asked | Yes |
| [Browser and device](/wiki/security/operational-persona/isolation-failures/browser-and-device) | Cookies, a fingerprint, a device identifier | Each site and the third parties it embeds | Mostly |
| [Network address](/wiki/security/operational-persona/isolation-failures/network-address) | The IP address at sign-in | Each service, anyone who can read its logs, the local network | Partly |
| [Shared custodian](/wiki/security/operational-persona/isolation-failures/shared-custodian) | One company's records covering both | The company, an intruder, a court | By splitting providers, for what they hold |
| [Payment trail](/wiki/security/operational-persona/isolation-failures/payment-trail) | A card, bank account or funding address | Banks and processors under legal demand; anyone, on a public ledger | Rarely |
| [Behavioural correlation](/wiki/security/operational-persona/isolation-failures/behavioural-correlation) | Places, hours, writing and coding style | Anyone with samples from both sides | No |

All of these break unlinkability, the property that an observer cannot tell two personas have one operator. Four also break containment, the property that a leak in one persona gives no control over another: a reused password, a recovery crossing, a compromised shared device, and a custodian holding credentials for both.

These pages describe how one person's own contexts get connected. Operating accounts a service has barred, and passing as several people, [fall outside the section](/wiki/security/operational-persona#limits).

## One link is enough

An operator has to be right on every commit and every login, and an observer needs one log entry. [A link has to be seen only once](/wiki/security/identity-separation#cheap-early-nearly-impossible-late), and deleting the evidence does not delete what was learned. [A context that fails closed](/wiki/security/operational-persona/technical-context#fail-closed) answers this directly: a mistake that produces an error never reaches a log.

## The boundary is drawn against an observer

RFC 6973 defines unlinkability relative to whoever is looking: "the inability of an observer or attacker to distinguish whether two items of interest are related or not (with a high enough degree of probability to be useful to the observer or attacker)".

The third column of the table is therefore the practical one. A pseudonym meant to keep strangers away from a home address needs the first rows closed and can tolerate a custodian that knows. A pseudonym meant to survive a legal demand cannot rest on any service holding a record that connects it to its operator. The spokesperson for Proton, an encrypted mail service, put the distinction this way: "Proton provides privacy by default and not anonymity by default because anonymity requires certain user actions".

## Weak signals add up

An observer rarely needs proof. The same RFC asks only for probability "high enough" to be useful, and evidence combines. Goga and colleagues matched 63% of Flickr users to their Twitter accounts at a 1% false-positive rate from location, timing and language together, against 77% from usernames. The investigative group Bellingcat treats a shared camera model as support only, useful beside a firmer link such as a shared analytics ID. A short list of candidates lowers the bar further, as when [a reporter found Mitt Romney's secret Twitter account](/wiki/security/operational-persona/isolation-failures/social-graph) by starting from his family's follower lists.

## Wiki Pages

{{< section >}}

## Further reading

- [RFC 6973: Privacy Considerations for Internet Protocols](https://www.rfc-editor.org/rfc/rfc6973), section 3.2 on unlinkability
- Goga, Lei, Parthasarathi, Friedland, Sommer & Teixeira, [Exploiting Innocuous Activity for Correlating Users Across Sites](https://doi.org/10.1145/2488388.2488428), WWW 2013
- Bellingcat, [Unveiling Hidden Connections with Google Analytics IDs](https://www.bellingcat.com/resources/2015/07/23/unveiling-hidden-connections-with-google-analytics-ids/) (2015)
- Lorenzo Franceschi-Bicchierai, [Encrypted services Apple, Proton and Wire helped Spanish police identify activist](https://techcrunch.com/2024/05/08/encrypted-services-apple-proton-and-wire-helped-spanish-police-identify-activist/), *TechCrunch* (2024)
