---
title: "Clearing a Flag"
weight: 60
---

Remediation is not one process. It is a dozen vendor queues, each keyed to a different machine, most of which will not tell you they exist. Changing the contract does not help: the [ENS token](/wiki/economics/finance/defi/token-false-alarms/capability-flags#what-actually-moves-the-flag) is behind a 48-hour timelock with a hard-capped mint and still reports `is_mintable`, and both PEPE and 1INCH have renounced ownership and still report the flags their unreachable setters produce. Once a flag exists, it is a queue problem.

So the first move is diagnosis, and it is free.

## Find out which machine fired

MetaMask exposes the only free per-hostname self-check in the landscape, unauthenticated:

```bash
curl 'https://dapp-scanning.api.cx.metamask.io/v2/scan?url=https://app.uniswap.org'
# {"hostname":"app.uniswap.org","recommendedAction":"VERIFIED"}

curl 'https://dapp-scanning.api.cx.metamask.io/v2/scan?url=https://uniswap.org'
# {"hostname":"uniswap.org","recommendedAction":"NONE"}
```

Two caveats make this less conclusive than it looks. Verification is per **hostname**, not per organisation — `app.uniswap.org` is verified and the apex domain is not — so check every host you serve from. And it reflects the server-side scanner only: `etherscan.org` returns `NONE` here while the client-side fuzzy matcher blocks it, because that matcher strips the last label and compares `etherscan` against an eight-entry list at an edit distance of one. A clean response is not proof you are unblocked.

Tokens and addresses run through a different pipeline with a different vocabulary — `security-alerts.api.cx.metamask.io` returning `Benign`, `Warning`, `Malicious` or `Spam` — so a clean domain scan says nothing about your token, and vice versa. And one list cannot be checked at all: MetaMask's command-and-control blocklist is matched against SHA-256 hashes of the hostname, and the check is not gated by the allowlist, so it is the one place you cannot learn whether you are listed.

Against the on-chain flags, query GoPlus, honeypot.is and RugCheck directly — the recipes are on [designing and self-checking](/wiki/economics/finance/defi/token-false-alarms/designing-and-self-checking#check-yourself).

## Domain blocklists

**MetaMask's `eth-phishing-detect`** is a public Git repository, which is why it is the one channel here whose performance anyone can measure. The block page itself files the issue: its "report a detection problem" link builds a prefilled GitHub issue titled `[Legitimate Site Blocked] <hostname>`. There is a formal template at `.github/ISSUE_TEMPLATE/02-blocklist-removal.yaml`, auto-labelled and auto-assigned to the user-safety team.

The repo says outright that a pull request beats an issue: "adding it to the allowlist is the fastest and simplest way to unblock that specific website quickly", and "Opening a valid pull request to add a website to the allowlist will generally be faster than opening an issue asking us to do so." One trap — the on-disk JSON keys are still the legacy names, so the file you edit is `whitelist` inside `src/config.json`, not `allowlist`.

```bash
yarn add:allowlist legitimate-site.tld
git commit -m "Allowlist legitimate-site.tld (#12345)"   # one domain per commit
# then open a PR whose body contains "Fixes #12345"
```

The median request closes in 36 hours and the repository had five open issues in total on 2026-08-31; [how often this is wrong](/wiki/economics/finance/defi/token-false-alarms/how-often-this-is-wrong#the-one-public-denominator) has the full distribution and the named cases. Two things temper it. Silent `not_planned` closures with no maintainer comment do happen. And a clearance is not permanent — `opensea.org` was unblocked in January 2023 after seven months and is on the blocklist again today.

**ChainPatrol** feeds the same list and takes disputes at `app.chainpatrol.io/dispute` — three fields, and a statement that "we will only consider disputes that are submitted by the domain owner or an authorized representative". It is bidirectional, covering assets "incorrectly flagged as either allowed or blocked", and it publishes a formal reversal lifecycle — `PENDING RETRACTION` → `RETRACTION SENT` → `RETRACTED` — which no other vendor here does, backed by provider relationships it says it uses for retractions as well as takedowns. Its programmatic endpoint needs an API key obtained by emailing support, so the web form is the route for a flagged developer.

**Phantom** routes three of its four warning types to a single Google Form and tells you to wait first: the new-domain warning "disappears automatically once the domain has been reviewed, typically within a few days", and the form is for when it persists past a week. Its blocklist repository documents only how to *add* a URL — there is no removal template, and its instruction to "open an issue" is dead, because issues are disabled on the repository. `review@phantom.com` appears in this context only in third-party issue bodies written by domain owners; it is in no Phantom-authored source.

**Google Safe Browsing** splits on Search Console ownership: a verified owner requests review inside the Security Issues report, and everyone else uses the phishing-error form at `google.com/safebrowsing/report_error/`. Published turnarounds are scattered across several pages rather than the one the appeal runs through: the Security Issues report gives a single undifferentiated "A review can take from a few days to a few weeks to complete", the social-engineering page says "A review can take several days to complete", "up to several weeks" for hacked spam comes from a 2013 Search Central post, and the Safe Browsing transparency FAQ puts browser-warning clearance within 24 hours. Do not resubmit — "Submitting a reconsideration request when the issue hasn't been fixed can cause longer turnaround time for the next request, or even get you marked as a repeat offender."

## Transaction and token classifiers

**Blockaid** takes reports at `report.blockaid.io`, whose entire route table is `/`, `/error`, `/mistake`, `/scam`, `/summary`, `/submittionSuccessfully`, `/tx` and `/verifiedProject` — the misspelling is theirs. Three entry cards matter:

- `/mistake` — "Report a false positive result"
- `/verifiedProject` — "Verify a project to prevent false malicious flags"
- `/scam` — the other direction

The verification route is the one worth using *before* launch. Base's own chain documentation points developers at it pre-emptively and lists what reduces the odds of a flag: verified public contract source, published audits, no geo-blocking or access restrictions, no opaque on-chain interactions, consistent interface behaviour, multiple connection methods, and limited user fund exposure.

Blockaid publishes no turnaround and no false-positive rate. Its API report endpoint requires an `x-request-id` from a prior scan, which only a wallet integrator can produce, so it is not a developer channel; its technical docs sit behind a login. Safe filed a feature request in March 2025 asking for a one-click report button and it remains open.

**MetaMask's in-product report** is narrower than it appears. Expanding an alert and clicking "Report an issue" covers **transaction alerts only** — "If you received a warning on a URL, token, or address scan, use Option 2 to contact our support team instead." Support states that "Reviews may take several business days depending on complexity and verification requirements."

**GoPlus** publishes one line of support documentation — an email address — and operates two console routes its own documentation site never mentions:

| Route | Cost | Stated turnaround |
| --- | --- | --- |
| `console.gopluslabs.io/feedback` | free | none |
| `console.gopluslabs.io/manual-review` | $199 | two business days |

The paid one says what it does: "A manual audit of the contract will be performed according to your request. If the reported issue is confirmed, the data will be updated accordingly." It is the firmest published turnaround of any vendor here.

One category error worth avoiding: `is_blacklisted` and `is_whitelisted` describe whether *your contract* contains a blacklist or whitelist function. They say nothing about GoPlus's own lists, and appealing them as list memberships wastes the ticket.

**TokenSniffer** has an un-flagging workflow and no documented dispute channel. Its `/corrections` endpoint lists tokens un-flagged in the last twenty-four hours and is Enterprise-tier only. `is_pending` on a token means a human is looking at it. The accurate statement is that no dispute path is publicly documented — its help subdomain sits behind a challenge page, which is exactly where one would live.

## Explorers

**Etherscan runs two systems and only one has a door.**

Public name tags — the red banners — can be disputed at `etherscan.io/contactus?id=9`, and the proof is a **signed message**, never a transaction:

```text
[Etherscan.io dd/mm/yyyy hh:mm:ss] I, the owner of the address [address], hereby
request that the Public Name Tag assigned to it and other information therein be
removed from Etherscan].
```

The unbalanced bracket is Etherscan's. For a contract, sign from the creating address and adapt the wording to "I, the creator of the contract address". The neighbouring process for *claiming* a contract in order to update its token info documents the awkward cases that name-tag removal does not: a multisig signer signs a variant binding the claim to an Etherscan username, with a warning not to publish that signed message since it reveals the username, and the lost-key and community-takeover branches end at "Our team will guide you through the rest of the process".

Etherscan reserves the right to refuse. Its policy names four categories where a tag may be kept regardless, and two of them cover a flagged project directly: a phishing or exploit name tag, and a project name tag such as a deployer label. On timing: "While we try our best to respond in a timely manner, we often have a backlog of inquiries."

Token **reputation** — the `SUSPICIOUS`, `UNSAFE` and `SPAM` states behind the tooltip — has no appeal at all: "We reserve the right to make the final judgment to accept/deny a token reputation award on this page and we are not obligated to provide any feedback on the reason for a rejection on token reputation award." The page carrying that sentence is bylined December 2019 and has no revision date. Solscan, by contrast, offers a "Reputation Update" request type explicitly for upgrading a token's status to Neutral.

Getting information *added* is well documented and free, and its prerequisites are the same two everything else needs: verified source, then ownership proved by signed message. Submissions are final — "you will not be able to edit or amend any part of the submission once it has been sent" — and informal escalation is forbidden in writing: requests go through the official form only, and the guidance tells submitters not to "contact our team members personally through their social profiles or other channels to expedite your requests." Every sibling explorer is a separate submission surface.

**Blockscout** is per-instance, which means there is no single Blockscout to appeal to. The scam badge is an operator decision, exposed twice on the same object — a `reputation` enum of `ok` and `scam`, plus an `is_scam` boolean — and two deployment settings can hide a badged address from search entirely. Expedited review costs 99 USDC or USDT, non-refundable, and buys a decision in one to seven business days rather than approval. Its duplicate tiebreak is quantitative — liquidity, volume, active traders, token age, transaction count — so a legitimate but smaller token loses to a larger one with the same name. The only dispute mechanism it documents is a radio button on the Public Tags form for reporting an incorrect public tag, which is a different object from the badge that hides you.

## Curation and listing

**Uniswap** has three gates and you must pick the right one, because two of them reject the other's appeals outright.

| Symptom | Route |
| --- | --- |
| `Malicious`, `Impersonator`, `Honeypot`, `Spam` | `report.blockaid.io/mistake` |
| Token absent or "Not Available" | `compliance@uniswap.org`, subject "Appeal request" |
| `isn't traded on leading U.S. centralized exchanges` | none — it is a listing fact |

The compliance address is the one named human appeal channel here that needs no account and publishes a clock: include the asset name, contract address and reason, and "The Uniswap Labs compliance team will acknowledge receipt of the request within 1 business day."

**Jupiter**, on Solana, publishes the most specific terms of any queue here. Standard review is free with no timeline, ordered by submission age, trading volume and community "Smart Likes"; Express Review costs 1,000 JUP and "guarantees a first review within 24-48 hours", with the fee burned rather than retained; the refund clause is narrower than the promise, applying "only if the 24-hour first review commitment is not met". Anyone may submit on any token's behalf. Because Phantom consumes Jupiter's strict list, this single action also clears Phantom's unverified-token warning — the highest-leverage move available to a Solana token.

**RugCheck** sells verification and publishes its eligibility criteria, which read as a checklist: revoke mint authority, revoke freeze authority, lock liquidity, publish metadata, avoid a duplicate ticker, and wait out the new-token window. Being verified elsewhere does not help — RENDER carries `jup_verified` and `jup_strict` and still scores 76.

## Compliance labels

There is no door. Neither Chainalysis nor TRM Labs publishes an address-label dispute process for an outside party, and the venue that screened you is the only party with a working one. This is covered under [liquidity and holders](/wiki/economics/finance/defi/token-false-alarms/liquidity-and-holders#the-compliance-sibling).

## What publishes a clock

| Channel | Cost | Published turnaround |
| --- | --- | --- |
| GoPlus Manual Review | $199 | two business days |
| Jupiter Express Review | 1,000 JUP | first review in 24–48 hours |
| Blockscout expedited | 99 USDC | one to seven business days |
| Etherscan Priority Support | paid | 48 business hours |
| Uniswap compliance | free | acknowledgement in one business day |
| `eth-phishing-detect` | free | none stated; measured median 36 hours |
| Blockaid, Phantom, ChainPatrol, TokenSniffer | free | none |
| Etherscan token reputation | — | no channel exists |

Four of the five channels that commit to a clock charge for it. The free channel with the best measured performance is the one that runs in public where anyone can count it, which is not a coincidence.

## Why a cleared flag persists

An approved appeal is not the end of the warning. MetaMask's own issue tracker carries an open report of a Blockaid "Malicious site" warning persisting after Blockaid confirmed removal, with the reporter documenting that four separate lists return "Unknown" for the same domain. Nothing in this landscape publishes a cache lifetime, a re-scan cadence after a contract change, or a propagation delay from a merged list entry to a cleared warning.

Redistribution makes it worse. Etherscan sells a bulk metadata export aimed at compliance and risk monitoring — "Address screening and AML workflows", in anti-money laundering pipelines, delivered as a downloadable archive to pipelines with no reason to re-fetch. A flagged contract page also carries its label in the `og:description` meta tag, so the string propagates through every link unfurl and search snippet that ever touched it. And GoPlus's licence requires integrators to display its findings branded and unmodified, which is why one vendor's flag appears verbatim in a dozen products whose operators you cannot contact.

Budget for the appeal being the easy part.

## External links

- [MetaMask dapp scanning endpoint](https://dapp-scanning.api.cx.metamask.io/v2/scan?url=https://example.com) — the free self-check
- [eth-phishing-detect list reference](https://github.com/MetaMask/eth-phishing-detect/blob/main/doc/lists-ref.md) — why a pull request beats an issue
- [ChainPatrol dispute](https://app.chainpatrol.io/dispute) — the form that feeds the same blocklist
- [report.blockaid.io](https://report.blockaid.io/) — false positives, and pre-launch project verification
- [Base: avoiding malicious flags](https://docs.base.org/specifications/security/avoid-malicious-flags) — the closest thing to official pre-flag guidance from a chain
- [Etherscan public name tag removal](https://info.etherscan.com/public-name-tag-removal/) — the signed-message template and the refusal categories
- [Etherscan token reputation](https://info.etherscan.com/etherscan-token-reputation/) — the ladder with no appeal
- [Google Search Console security issues](https://support.google.com/webmasters/answer/9044101) — the review request and its turnarounds
- [Jupiter token verification](https://docs.jup.ag/user-docs/launch/vrfd/token-verification) — the only published refund condition in the field
