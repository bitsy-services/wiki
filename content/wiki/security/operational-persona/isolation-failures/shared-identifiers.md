---
title: "Shared Identifiers"
weight: 10
---

A shared identifier is a value specific enough to point at one party that appears on both sides of the boundary between two [operational personas](/wiki/security/operational-persona), managed identity sets meant to stay separate. An observer who finds it can join the two sets of records on that value, the way a database joins two tables on a key, using only what each side published.

[Identity separation](/wiki/security/identity-separation#how-identities-get-linked) covers the identifiers a developer produces daily: the commit address, the SSH key, the handle and the metadata in files. This page covers what makes a value work as a key, and the identifiers that arrive without anyone typing them.

## What makes a value a key

A key has to be specific and stable. `john` on two sites says little, and `brinewick` says a lot. Perito and colleagues measured this for usernames in 2011 by estimating how improbable each string is, and concluded that "a vast majority of users from our datasets can be uniquely identified among a population of 1 billion" by username alone. Stability comes from reuse: Pfitzmann and Hansen's privacy terminology traces linkability to "non-changing identifiers" and to attribute values that stay the same over time.

## Values nobody typed

### Analytics and advertising IDs

A site that embeds Google Analytics or AdSense carries an account number in its page source. "The string of code added to each page contains a unique user account number – and through this, multiple sites can be linked together," Bellingcat's guide explains, and reverse-lookup services index those numbers. Removing the snippet later does not help where a cached copy or a lookup service still records it.

### Certificates

Certificate Transparency is a system of public logs recording "the existence of Transport Layer Security (TLS) certificates as they are issued or observed". A certificate that names two domains records for anyone that one operator requested both, and the log keeps the record after the certificate expires.

### Domain records

A domain's registration record (WHOIS) can hold a name, an address and a contact email. The attacker who [took the journalist Mat Honan's accounts in 2012](/wiki/security/operational-persona/recovery-graph#what-counts-as-an-edge) got a billing address from a WHOIS search on Honan's personal domain, and Bellingcat's guide uses registrant email addresses to find a person's other sites.

### Passwords

A password reused on two accounts turns into an identifier once both services are breached, since services that sell breach data let investigators search by password. In a 2021 investigation of a ransomware access broker, Brian Krebs started from a Gmail address, recovered its backup address from the masked hint on Gmail's recovery form, and found that address's two passwords in breach records. Searching for those passwords surfaced further addresses, and one of those had registered an account under a person's name.

### Phone numbers

A phone number is one short string that many services accept as a lookup key. Hagen and colleagues reported in 2021 that contact discovery, the feature that matches an address book against a messenger's users, let them query 10% of US mobile numbers on WhatsApp and all of them on Signal at the time. On Zelle, a bank shows the sender [the registered first name and last initial](/wiki/economics/payments/zelle/alias#misdirection-by-typo) behind a number or address enrolled as a payment alias, so that value resolves to part of a legal name.

## How joins chain

The 2013 criminal complaint against Ross Ulbricht shows how cheap each step is. An agent searched for the earliest mentions of Silk Road and found a post on a mushroom forum dated 27 January 2011, by a user named `altoid`, who had joined apparently to post that one message. Two days later `altoid` promoted the site on the Bitcoin Talk forum.

On 11 October 2011, about eight months later, `altoid` posted again on Bitcoin Talk, in an unrelated thread, looking for an IT professional, and asked for replies to `rossulbricht at gmail dot com`. Google's subscriber records then gave the account holder's name. The handle had been made for one purpose, and its reuse for another connected the two.

## Check

Run these logged out, from neither persona's browser:

```bash
# names on every certificate issued for a domain
curl -s 'https://crt.sh/?q=brinewick.example&output=json' | jq -r '.[].name_value' | sort -u

# analytics and advertising IDs in a page
curl -s https://brinewick.example/ | grep -oE 'UA-[0-9]+-[0-9]+|G-[A-Z0-9]{8,}|ca-pub-[0-9]+' | sort -u
```

A domain from another persona in the first list, or an ID that also appears on another persona's site, links the two. Then search for each handle with [Sherlock](https://github.com/sherlock-project/sherlock), the username search tool, and for each address and key fingerprint in the other persona's published output.

## Further reading

- Perito, Castelluccia, Kaafar & Manils, [How Unique and Traceable are Usernames?](https://arxiv.org/abs/1101.5578), PETS 2011
- Bellingcat, [Unveiling Hidden Connections with Google Analytics IDs](https://www.bellingcat.com/resources/2015/07/23/unveiling-hidden-connections-with-google-analytics-ids/) (2015)
- [RFC 6962: Certificate Transparency](https://www.rfc-editor.org/rfc/rfc6962), and [crt.sh](https://crt.sh/), a search interface to the logs
- Brian Krebs, [Who is the Network Access Broker 'Babam'?](https://krebsonsecurity.com/2021/12/who-is-the-network-access-broker-babam/) (2021)
- Hagen, Weinert, Sendner, Dmitrienko & Schneider, [All the Numbers are US: Large-scale Abuse of Contact Discovery in Mobile Messengers](https://encrypto.de/papers/HWSDS21.pdf), NDSS 2021
- [Criminal complaint, *United States v. Ulbricht*](https://krebsonsecurity.com/wp-content/uploads/2013/10/UlbrichtCriminalComplaint.pdf) (2013), paragraphs 34 to 39
