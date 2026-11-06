---
title: "Shared Custodian"
weight: 50
---

A shared custodian is a company whose records cover two [operational personas](/wiki/security/operational-persona), managed identity sets meant to stay separate, or connect them. The boundary can hold against every outside observer and still be plain to that company, and to anyone who reaches its records through a bug, a breach or a legal demand.

## How the records get out

A bug needs no malice. From June 2021 until a report in January 2022, Twitter's login flow would tell anyone who submitted a phone number or email address which account it belonged to. A pseudonym with a real number on file was one query from being named, and [the flaw is covered with the recovery graph](/wiki/security/operational-persona/recovery-graph#a-crossing-breaks-both-properties).

A breach reads what the company kept readable. LastPass, a password manager, reported in 2022 that an intruder copied customer vault backups containing "both unencrypted data, such as website URLs, as well as fully-encrypted sensitive fields such as website usernames and passwords". A vault holding two personas' logins is then a list of sites one person uses, readable without the master password: the hobby forum beside the employer's sign-in page.

A legal demand reads the rest, one company at a time. In the [Spanish case](/wiki/security/operational-persona/recovery-graph#a-crossing-breaks-both-properties) Wire, Proton and Apple each held one link in a chain from a pseudonymous account to a name, and each responded. An order can also reach data a company was not collecting. Proton said in 2021 that under Swiss law it "can be forced to collect information on accounts belonging to users under Swiss criminal investigation", on an order for a specific account, and a Swiss court ruling later that year narrowed what email services must hand over.

## What counts as shared

A custodian is anything that sees across the boundary, and most are chosen for convenience.

| Service | What it joins |
| --- | --- |
| One password manager account | Every site in the vault |
| One phone platform account | Contacts, backups, and everything synced from every app |
| Browser sync | Bookmarks, passwords and settings, stored in the account the profile signs in to |
| One registrar or DNS host login | Every domain in it |
| One cloud or hosting account | Every project and its billing |
| One coding assistant account | [Every conversation held under it](/wiki/ai/claude-accounts/how-many-accounts) |

Two accounts at one company weaken the join without removing it: the company can still compare addresses, devices and cards across them. One account holding both personas hands the link over as a stored fact.

## What lowers it

Split providers where the threat calls for it, and give each provider less to hold. A recovery address is optional at many services and, [once set, is readable by the service](/wiki/security/operational-persona/recovery-graph#a-crossing-breaks-both-properties). A password store can live where no vendor reads it: [`pass`](/wiki/security/pass) encrypts each entry to the persona's own key, and its remote sees ciphertext, though it [does see the entry names](/wiki/security/pass#security-notes-ordered-by-blast-radius).

Some custody cannot be removed. A mail provider handles the mail it delivers, a registrar holds a registrant record, and a bank [knows its customer](/wiki/economics/regulation/know-your-customer). The working assumption is that each custodian will one day disclose what it holds, so the question for each is what that disclosure would connect.

## Check

Take each persona's inventory and list the company behind each item. A company that appears in two personas' lists is a custodian of both. For each one, note whether it holds two accounts or one, and what it would give up if asked.

## Further reading

- LastPass, [Notice of recent security incident](https://web.archive.org/web/2023/https://blog.lastpass.com/2022/12/notice-of-recent-security-incident/) (2022), archived copy
- Proton, [Important clarifications regarding arrest of climate activist](https://proton.me/blog/climate-activist-arrest) (2021)
- Lorenzo Franceschi-Bicchierai, [Encrypted services Apple, Proton and Wire helped Spanish police identify activist](https://techcrunch.com/2024/05/08/encrypted-services-apple-proton-and-wire-helped-spanish-police-identify-activist/), *TechCrunch* (2024)
- Google, [Manage Chrome with multiple profiles](https://support.google.com/chrome/answer/2364824)
