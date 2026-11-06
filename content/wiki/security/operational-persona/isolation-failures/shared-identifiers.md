---
title: "Shared Identifiers"
weight: 10
---

A shared identifier is a value specific enough to point at one party that appears on both sides of the boundary between two [operational personas](/wiki/security/operational-persona), the sets of accounts and credentials one person runs as separate identities. An observer who finds it can join the two sets of records on that value, the way a database joins two tables on a key, using only what each side published.

[Identity separation](/wiki/security/identity-separation#how-identities-get-linked) covers the identifiers a developer produces daily: the commit address, the SSH key, the handle and the metadata in files. This page covers what makes a value work as a key, and the identifiers that are easier to miss.

## What makes a value a key

A key has to be specific and stable. Perito and colleagues measured specificity for usernames in 2011 by estimating how improbable each string is, and concluded that "a vast majority of users from our datasets can be uniquely identified among a population of 1 billion users, relying only on their usernames". Stability comes from reuse: Pfitzmann and Hansen's privacy terminology traces linkability to "non-changing identifiers" and to attribute values that stay the same over time.

## Less obvious identifiers

### Analytics and advertising IDs

A site that embeds Google Analytics or AdSense carries an account number in its page source. "The string of code added to each page contains a unique user account number – and through this, multiple sites can be linked together," explains a guide from Bellingcat, the investigative group, and reverse-lookup services index those numbers. A cached copy or a lookup service can keep the association after the snippet is removed.

### Certificates

Certificate Transparency is a system of public logs recording "the existence of Transport Layer Security (TLS) certificates as they are issued or observed". A certificate that names two domains suggests to anyone reading the logs that one operator requested both, and the log entry outlasts the certificate.

### Domain records

A domain's registration record (WHOIS) can hold a name, an address and a contact email. The attacker who [took the journalist Mat Honan's accounts in 2012](/wiki/security/operational-persona/recovery-graph#what-counts-as-an-edge) got a billing address from a WHOIS search on Honan's personal domain, and Bellingcat's guide uses registrant email addresses to find a person's other sites.

The record has to be accurate. ICANN, the body that oversees domain names, tells registrants "You must provide accurate information for publication in directories such as WHOIS". A privacy service hides the record from public lookups, and the registrar and the service still hold it, along with [whatever paid for the domain](/wiki/security/operational-persona/isolation-failures/payment-trail).

### Passwords

A password reused on two accounts turns into an identifier once both services are breached, since services that sell breach data let investigators search by password. Partway through a 2021 investigation of a ransomware access broker, Brian Krebs read a masked backup address on Gmail's recovery form, confirmed a guess at it when Gmail accepted the address, and found that address's two passwords in breach records. Searching for those passwords surfaced further addresses, and one of those had registered an account under a person's name.

### Phone numbers

A phone number is one short string that many services accept as a lookup key. Hagen and colleagues reported in 2021 that contact discovery, the feature that matches an address book against a messenger's users, let them query 10% of US mobile numbers on WhatsApp and all of them on Signal at the time. A number enrolled with a payment service can also [resolve to part of a name](/wiki/security/operational-persona/isolation-failures/payment-trail#cards-and-bank-accounts).

## How joins chain

The 2013 criminal complaint against Ross Ulbricht, over the anonymous drug market Silk Road, describes a chain built mostly from public posts. An agent searched for the earliest mentions of Silk Road and found a post on a mushroom forum dated 27 January 2011, by a user named `altoid`, who had joined apparently to post that one message. Two days later `altoid` promoted the site on the Bitcoin Talk forum.

On 11 October 2011, about eight months later, `altoid` posted again on Bitcoin Talk, in an unrelated thread, looking for an IT professional, and asked for replies to `rossulbricht at gmail dot com`. Subscriber records obtained from Google then gave the account holder's name.

## Check

Run these logged out, from neither persona's browser:

```bash
# names on every certificate issued for a domain
curl -fsSL 'https://crt.sh/?q=brinewick.example&output=json' | jq -r '.[].name_value' | sort -u

# analytics and advertising IDs in a page
curl -fsSL https://brinewick.example/ | grep -oE 'UA-[0-9]+-[0-9]+|G-[A-Z0-9]{8,}|(ca-)?pub-[0-9]+' | sort -u
```

A `curl` error means the request failed, and empty output with no error means no match. A domain from another persona in the first list, or an ID that also appears on another persona's site, links the two. Then search for each handle with Sherlock, the open-source username search tool, and for each address and key fingerprint in the other persona's published output.

## Further reading

- Perito, Castelluccia, Kaafar & Manils, [How Unique and Traceable are Usernames?](https://arxiv.org/abs/1101.5578), PETS 2011
- Bellingcat, [Unveiling Hidden Connections with Google Analytics IDs](https://www.bellingcat.com/resources/2015/07/23/unveiling-hidden-connections-with-google-analytics-ids/) (2015)
- [RFC 6962: Certificate Transparency](https://www.rfc-editor.org/rfc/rfc6962), and [crt.sh](https://crt.sh/), a search interface to the logs
- ICANN, [Registrant Benefits and Responsibilities](https://www.icann.org/resources/pages/benefits-2013-09-16-en)
- Brian Krebs, [Who is the Network Access Broker 'Babam'?](https://krebsonsecurity.com/2021/12/who-is-the-network-access-broker-babam/) (2021)
- Hagen, Weinert, Sendner, Dmitrienko & Schneider, [All the Numbers are US: Large-scale Abuse of Contact Discovery in Mobile Messengers](https://encrypto.de/papers/HWSDS21.pdf), NDSS 2021
- [Criminal complaint, *United States v. Ulbricht*](https://krebsonsecurity.com/wp-content/uploads/2013/10/UlbrichtCriminalComplaint.pdf) (2013), paragraphs 34 to 39
- [Sherlock](https://github.com/sherlock-project/sherlock), the username search tool
