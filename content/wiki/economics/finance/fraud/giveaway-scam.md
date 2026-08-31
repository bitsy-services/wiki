---
title: "Giveaway and Impersonation Scams"
weight: 65
---

A giveaway scam offers to send back more than it receives: transfer 1 ETH to the address on screen and 2 ETH comes back, restricted to the next hour, endorsed by someone with a name. The arithmetic is impossible and the offer is broadcast rather than aimed, so the operation is indifferent to how many people work that out. Reaching another hundred thousand accounts costs nothing once the distribution channel is stolen, and a single transfer covers the cost of the campaign.

That economics separates it from every [fraud](/wiki/economics/finance/fraud) with a human in the loop. [Pig butchering](/wiki/economics/finance/fraud/pig-butchering) needs an operator to spend weeks per target and dies at a low conversion rate; a giveaway campaign survives a conversion rate too small to measure, because the marginal cost per target is a post that was going to be sent anyway.

## The offer

Three components do the work, and none is the promise itself.

**A deadline.** "First 5,000 participants", a countdown timer, a stream about to end. It is always short enough to preclude the pause in which the arithmetic gets checked or anyone else gets asked.

**Social proof.** Reply chains under the post are populated by the operation's own accounts confirming receipt, often with a block explorer screenshot. The screenshot shows a real transaction, usually an unrelated one, whose addresses match nothing in the offer — the weakest element in the construction and the least often examined.

**Borrowed authority.** Nothing about the offer itself is checkable, so the check collapses onto whether the source — a founder, a company, an exchange, a government account — is who it claims to be, which is the one thing the operation manufactures.

## Impersonation surfaces

Roughly in descending order of effectiveness:

**Compromised or purchased verified accounts.** On 15 July 2020 an attacker used an internal Twitter administration tool to take over roughly 130 accounts — Barack Obama, Elon Musk, Joe Biden, Apple, Uber among them — and posted a doubling offer from about 45 of them. Around $118,000 in bitcoin arrived over a few hours before the posts were removed, from several hundred transfers. Graham Ivan Clark, 17 at the time, pleaded guilty in Florida state court in March 2021 and was sentenced as a youthful offender; three other participants were charged federally. The account takeover, not the offer, was the whole of the innovation.

**Hijacked livestream channels.** A channel with an existing subscriber count is taken over, renamed, and set to loop genuine conference footage of a public figure with an address and a QR code composited over it. The video is real, so the authenticity check a viewer knows how to run returns the right answer, and the fraudulent part is a rectangle of overlay.

**Cloned support accounts.** A bot watches for posts containing "wallet", "stuck", or "support" and replies within seconds from a lookalike handle, moving the conversation to a form or a "validation" page that is a [wallet drainer](/wiki/economics/finance/fraud/wallet-drainer). The victim initiated the help request, which removes the one heuristic — unsolicited contact — that catches most of the category.

**Paid search ads.** An ad slot above the real project's organic result, pointing at a domain one code point away from the genuine one, is a purchase rather than a compromise: cheap, instant, and defeated only by [reading what the address bar says](/wiki/cs/canonicalization-attack).

## Deepfakes

Synthetic video and voice of a public figure fronting a fake platform grew sharply from 2023 for a cost reason: producing a convincing likeness fell below the revenue of a single conversion. The fake never has to survive forensic examination, only a first viewing on a phone at low resolution, and that threshold has been reachable on consumer hardware since then.

In early 2024, Hong Kong police reported that an employee of a multinational firm transferred about 200 million Hong Kong dollars — roughly US$25 million — across fifteen transactions after a video conference in which every other participant, including the chief financial officer, was synthetic. Those were bank transfers rather than crypto: the case establishes that the technique clears a controlled corporate process with approval steps. The FBI warned in December 2024 that generative tools were being used at scale for scam profiles, voice clones, and promotional video.

## Address substitution

A quieter variant supplies a corrected address rather than an offer: a reply under a legitimate donation post, an edited message in a group chat, a "the address above is outdated" follow-up. It merges into [address poisoning](/wiki/economics/finance/fraud/address-poisoning), where the lookalike is planted in the victim's own transaction history, and into [fake tokens](/wiki/economics/finance/fraud/fake-token), where the substituted item is a contract rather than a destination. [Vanity address](/wiki/economics/finance/defi/vanity-addresses) mining makes the lookalike cheap enough to spray against the truncated `0x1a2b…9f8e` display most wallets show; address poisoning has the search cost.

The chain shape makes this terminal rather than annoying. A confirmed transfer has no chargeback, no return window, and no intermediary with a dispute process, so the whole defence has to happen before the send. Proceeds move toward [cashing out](/wiki/economics/finance/fraud/cashing-out) within minutes of a campaign being noticed, and the addresses that paid into a public one stay visible on chain — a target list for a [recovery scam](/wiki/economics/finance/fraud/recovery-scam) that assembles itself.

## What to check

- Treat any inbound offer that requires a send as terminal. No distribution of anything — airdrop, refund, verification, unlock — is funded by a payment from the recipient in the same asset.
- Verify the domain independently. Type it, or use a bookmark you made earlier; never navigate from the link in the message, and never from a search ad.
- Check the account's history rather than its badge. Creation date, handle character substitutions, and whether it posted anything before this week are all visible; the verification mark is purchasable and the display name is free.
- Compare an address in full, or not at all. Checking the first and last four characters is the check that vanity mining is built to defeat.

## Where the law lands

Charges here are ordinary wire fraud, computer intrusion, and money laundering rather than anything crypto-specific. The Federal Trade Commission (FTC) added a direct tool in April 2024, when its Government and Business Impersonation Rule took effect, making impersonation of an agency or a business independently actionable with civil penalties and refunds, without proving a separate deceptive act.

## External links

- [FBI Internet Crime Complaint Center annual reports](https://www.ic3.gov/AnnualReport/Reports) — reported losses by category, including impersonation and confidence fraud
- [FTC Data Spotlight](https://www.ftc.gov/news-events/data-visualizations/data-spotlight) — the reports on crypto scam losses originating on social media
- [FTC consumer advice](https://consumer.ftc.gov/) — plain-language guidance and the reporting channel for impersonation
- [Chainalysis blog](https://www.chainalysis.com/blog/) — on-chain measurement of giveaway and impersonation campaign proceeds
- [Department of Justice press releases](https://www.justice.gov/news) — charging documents for the 2020 Twitter compromise and later impersonation cases
