---
title: "Wallet Drainers"
weight: 70
---

A wallet drainer is a hosted script that turns a wallet connection into a sequence of signature requests. The victim arrives at an attacker-controlled page and connects; the script reads every asset the address holds across every chain the wallet will talk to, prices them, and asks for the cheapest signature that moves the most valuable one. The person who put the page in front of the victim usually wrote none of it: they rented it, and the developer takes a percentage of everything it takes.

What those signatures authorise — the allowance model, off-chain permits, and the cost of treating a signature as harmless — is on [approval phishing](/wiki/economics/finance/fraud/approval-phishing). This page covers the delivery and the industry behind it. [Address poisoning](/wiki/economics/finance/fraud/address-poisoning) empties the same wallet without phishing any signature at all.

## Connecting is passive

Connecting a wallet discloses an address and grants read access. The site can then make ordinary read-only calls against a [blockchain](/wiki/economics/finance/defi/blockchain) node — `eth_getBalance`, `balanceOf`, `allowance` — that anyone could have made with the address alone. A victim who connected and closed the tab has lost nothing.

Exposure begins at the first signature, and the ranking step in between decides the take:

```text
connect       address disclosed, nothing signed
   |
enumerate     balances, token holdings, NFT positions, staked
   |          positions, and existing allowances, across chains
   |
rank          price each holding, subtract the gas the theft costs
   |          on that chain, sort by realisable value
   |
request       cheapest signature that moves the largest position
   |
repeat        next asset down the list, until the victim stops
```

An asset already covered by a live allowance to a contract the attacker controls costs no signature at all. Native ether is the hardest to take, since moving it needs a transaction the wallet renders as a plain outgoing value transfer, so it comes last, after the token and [non-fungible token (NFT)](/wiki/economics/finance/defi/nft) positions that a single signature can carry. Every refusal ends the session, so a victim who baulks at prompt three has already given up prompts one and two.

## Why the volume is high

Drainer kits are sold as a service. The developer supplies the script, the hosting, the obfuscation, a dashboard, and a support channel; the affiliate supplies traffic. The split is enforced in the drainer's own contract, which routes the developer's share automatically, and the commonly cited cut is 20–30%. Group-IB's research on Inferno Drainer put its cut at 20%, and counted roughly $80 million taken from about 137,000 victims between November 2022 and November 2023, after which the operators announced a shutdown and the kit resurfaced in 2024 anyway.

That decouples the technical skill from the social-engineering skill, so neither is a bottleneck: whoever compromises a Discord server needs no grasp of `permit` semantics, and whoever wrote the signature logic never speaks to a victim. Families that have operated at scale include Monkey Drainer, retired in March 2023 after ZachXBT's on-chain investigations; Inferno; Angel; Pink, whose operators announced they were ceasing operations in October 2024; and Venom. A shutdown is usually a transfer of business, the departing operator naming a successor kit for its affiliates.

Scam Sniffer's annual phishing reports put wallet-drainer losses at roughly $295 million across about 324,000 victim addresses in 2023, and roughly $494 million across about 332,000 addresses in 2024. Those count addresses rather than people, and only activity attributed to drainer infrastructure already known to the tracker, so they are a floor.

## Where the traffic comes from

Roughly in descending order of yield:

- **Compromised project accounts.** An announcement from the project's own verified account reaches an audience already expecting a mint. In September 2023 Vitalik Buterin's X account was taken over through a [SIM swap](/wiki/economics/finance/fraud/sim-swap) and used to post a fake commemorative NFT mint; roughly $691,000 was drained before the post came down.
- **Paid search ads on the project's own name**, sitting above the real result, with a displayed domain that is not the one the click resolves to.
- **Discord webhook compromise.** A stolen webhook posts into the announcements channel with the server's own branding, no account takeover required.
- **Lookalike domains hosting cloned [dapp](/wiki/economics/finance/defi/dapp) front ends**, typically a byte-identical copy of the real interface with one script swapped, so it survives a careful look at the page itself.
- **Physical QR codes** on flyers, stickers, and conference material, where the destination is invisible until it loads.

[Fake token](/wiki/economics/finance/fraud/fake-token) airdrops feed the funnel from the other end, arriving unsolicited in the wallet with a claim site named in the metadata, and [giveaway and impersonation scams](/wiki/economics/finance/fraud/giveaway-scam) supply the rest.

## Staying off the blocklists

The page is inert whenever a scanner looks at it. Drainer kits serve the payload conditionally from the server: a request from a known crawler range, a headless user agent, or a data centre address gets a benign page, and the draining logic is fetched only once a browser has passed the checks. Geofencing drops the jurisdictions the operator would rather not be prosecuted in. Domains are registered in bulk and rotated faster than blocklists propagate, so a domain not yet flagged carries no information about whether it is safe.

## What actually helps

**A separate wallet for mints and airdrops**, funded with what the transaction needs and nothing else. A drainer wants a signature rather than a key, so the control that matters most is the one that bounds what a correct signature can cost. It caps the loss rather than preventing it, and it is the only item here that still works after everything else has failed.

**A hardware wallet with clear signing.** The private key never reaches the host, so malware and a cloned front end cannot extract it, and the device displays the call it is being asked to sign — for typed data outside the vendor's supported set it shows a hash and refuses unless blind signing is enabled. It cannot protect a user who reads a malicious `permit` and approves it, because the device signs faithfully what was confirmed.

**Reading the wallet's decoding rather than the site's description.** The site controls its own text and its button labels; it does not control what the wallet says the transaction does. A mint page asking for `setApprovalForAll` on a collection the user already owns is describing itself incorrectly.

**Revoking approvals** that are no longer needed, which is a per-token, per-chain transaction that costs gas.

## Where the law lands

Enforcement has landed on infrastructure and on the cash-out rather than on kit authors, who sit in jurisdictions where any charge would have to be brought locally. Registrars and ad platforms remove domains and campaigns, reported deposit addresses get flagged when funds reach an exchange with [anti-money laundering](/wiki/economics/finance/regulation/anti-money-laundering) obligations, and prosecutions are brought as wire fraud and money laundering against whoever touched the proceeds at the [cash-out](/wiki/economics/finance/fraud/cashing-out) stage. Victims are then approached a second time by [recovery scams](/wiki/economics/finance/fraud/recovery-scam) offering to reverse a transfer nobody can reverse.

## External links

- [Group-IB blog](https://www.group-ib.com/blog/) — research on Inferno Drainer and other kits, including the affiliate split
- [Scam Sniffer](https://scamsniffer.io/) — annual phishing reports and the domain blocklist feed
- [ZachXBT](https://zachxbt.mirror.xyz/) — investigations that identified several drainer operators
- [Ledger blog](https://www.ledger.com/blog) — post-mortem of the December 2023 Connect Kit supply-chain compromise
- [FBI Internet Crime Complaint Center (IC3) annual reports](https://www.ic3.gov/AnnualReport/Reports) — reported US losses by fraud category
