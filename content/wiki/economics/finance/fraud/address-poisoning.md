---
title: "Address Poisoning"
weight: 80
---

Address poisoning attacks the habit of copying a recipient address out of a wallet's own transaction history. The attacker generates an address that matches the victim's real counterparty in the first and last few characters, arranges for it to appear in the victim's history, and waits. Nothing is signed under false pretences and no contract misbehaves: the victim's next payment is authorised, correctly formed, and sent to the wrong place.

That makes it the odd one out among wallet attacks. A [wallet drainer](/wiki/economics/finance/fraud/wallet-drainer) needs the victim on a hostile page, and [approval phishing](/wiki/economics/finance/fraud/approval-phishing) needs a signature the victim does not understand. Poisoning needs neither, only an interface that abbreviates.

## The abbreviation is the attack surface

An Ethereum address is 20 bytes, written as 40 hex characters. No interface shows all 40 in a list, so wallets and explorers truncate to a prefix and a suffix and the comparison collapses to eight characters:

```text
real counterparty   0x7a1c9f3b4e2d8a05c6f1e93b7d45aa28c0ff91b3
attacker's clone    0x7a1ce2740b8d19af3c5b6e01d2794ca3f88f91b3

both display as     0x7a1c…91b3
```

Those two addresses (illustrative, not real) differ in 30 of their 40 characters and are identical in every abbreviated view. Producing the clone is [vanity address](/wiki/economics/finance/defi/vanity-addresses) mining with the pattern split across both ends: four leading and four trailing characters fix eight of the forty, an expected search of 16^8 ≈ 4.3 billion candidates. At the 10^8–10^9 keys per second that page gives for GPU mining of externally owned accounts, that is seconds to under a minute on one card. Six characters a side costs 16^4 ≈ 65,000 times more — weeks to months on the same card, hours on a rented cluster.

## Getting into the history

The clone address has to appear in the victim's transaction list, and there are three cheap ways to put it there.

**Zero-value token transfers.** The [ERC-20](/wiki/economics/finance/defi/ethereum/erc-20) standard requires transfers of zero value to be treated as normal transfers and to emit the `Transfer` event, so a transfer of nothing is indistinguishable in the logs from a transfer of something. The attacker sends 0 tokens from the clone to the victim, and any wallet rendering token events shows an entry carrying an address the victim now half-recognises.

**`transferFrom` with zero value.** Standard implementations check the allowance without requiring it to be non-zero, so any address can emit `Transfer(victim → clone, 0)` without the victim's permission. The entry then reads as an outbound payment the victim appears to have made to the clone, which is a stronger lure than an inbound one: the address is not merely familiar, it looks previously used.

**Fake tokens.** A contract reporting the name and symbol of a token the victim already holds can emit whatever events it likes, including a large credit from the clone. The victim sees a plausible amount of a familiar asset arriving from a familiar-looking counterparty — [fake token](/wiki/economics/finance/fraud/fake-token) machinery pointed at the address book rather than at the price.

Attackers watch for real transfers and land the poison immediately afterwards, so the fake entry sits directly adjacent to the genuine one in the history.

## Why it works

A 20-byte address carries 160 bits of entropy, which nobody memorises and nobody proofreads. Every interface therefore abbreviates, and every abbreviation is a truncation the attacker can target: two distinct strings that a human comparison treats as equal. That is a [canonicalization attack](/wiki/cs/canonicalization-attack) with the human as the component doing the lossy normalisation.

The economics favour spraying. A zero-value transfer on a low-fee chain costs a fraction of a cent, so poisoning millions of addresses costs a few thousand dollars, and the campaign only needs one victim who was about to move a large balance. Almost none of the transactions pay off, and at that unit cost they do not have to.

## Cases

**May 2024, roughly $68 million.** The victim made a small test transfer to a genuine counterparty; the attacker generated a lookalike of that counterparty, planted it in the history, and the 1,155 wrapped bitcoin (WBTC) that followed went to the clone. SlowMist and Lookonchain reported the transfer on 3 May 2024, and it remains the largest publicly reported poisoning loss. The attacker swapped the WBTC to ether and then returned the funds in full about a week later, after being traced and contacted on-chain — not the normal outcome.

**August 2023, 20 million USDT.** On-chain trackers reported a victim sending 20 million USDT to a poisoned address, after which Tether froze the receiving address. Recovery depended entirely on the issuer holding that power; the same mistake made in ether has no equivalent remedy.

## Defence

**Keep an address book and send from it.** A saved, verified contact is the only control that removes the copy-paste step, turning recipient selection into picking a name rather than matching hex.

**Verify the whole address, not the abbreviation.** Compare the full 40 characters, or at least the middle, against a source outside the chain history: an invoice, a signed message, a channel the counterparty controls. Confirming the first and last four confirms exactly the part the attacker chose to match.

**Treat test transfers as weak.** Sending a small amount first proves the address you already have is spendable; it does not stop you copying a different one for the real payment. It also announces the transfer to anyone watching, and the gap between test and main send is exactly when a poison entry gets placed.

**Prefer wallets and explorers that hide zero-value and unknown-token transfers.** Filtering the spam removes most of the bait, though it does nothing about the fake-token variant, which reports a plausible non-zero amount.

**Name services help, with their own version of the problem.** Sending to an Ethereum Name Service (ENS) name is easier to verify by eye than hex, but names have lookalikes too — homoglyphs, added characters, alternative suffixes — and a resolved name still has to be resolved from a trustworthy source.

## Where the law lands

The transfer is voluntary, correctly signed, and final, so recourse runs through the narrow channels open to any crypto theft: an issuer that can freeze its token, or an exchange that can hold a deposit when the funds are [cashed out](/wiki/economics/finance/fraud/cashing-out). Reports go to the FBI's Internet Crime Complaint Center (IC3) and, for large amounts, to chain-analysis firms that can trace the hops. Anyone contacted afterwards by a firm promising reversal has met a [recovery scam](/wiki/economics/finance/fraud/recovery-scam), the second-stage business that also follows [giveaway scams](/wiki/economics/finance/fraud/giveaway-scam) and the other patterns in [anatomy of a crypto scam](/wiki/economics/finance/fraud/anatomy-of-a-crypto-scam).

## External links

- [EIP-20 specification](https://eips.ethereum.org/EIPS/eip-20) — the clause requiring zero-value transfers to fire `Transfer` like any other
- [SlowMist](https://slowmist.medium.com/) — incident write-ups, including the May 2024 wrapped-bitcoin case
- [Chainalysis blog](https://www.chainalysis.com/blog/) — crime-report material on poisoning campaigns and tracing
- [MetaMask Help Center](https://support.metamask.io/) — wallet-side guidance on verifying recipients and hiding spam transfers
- [FBI Internet Crime Complaint Center annual reports](https://www.ic3.gov/AnnualReport/Reports) — reported US losses by category
