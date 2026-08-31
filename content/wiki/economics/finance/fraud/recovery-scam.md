---
title: "Recovery Scams"
weight: 95
---

A recovery scam charges a fee to return money already lost to a different [fraud](/wiki/economics/finance/fraud). The approach comes from a "blockchain forensics firm", a "certified recovery agent", a law-enforcement liaison, or a class-action administrator, with a case number, a dashboard showing the traced funds, and a request for a retainer, a filing fee, or a tax. Payment produces a further fee rather than a return, and the sequence runs until the target stops paying.

## Why prior victims are the best list

Someone who has just lost money carries three properties no cold list has, and the combination converts at a higher rate than the fraud that produced the victim did. They are known to hold or have held cryptocurrency, which most prospecting spends its effort establishing. They are known to have acted on an unsolicited offer, which is behavioural evidence rather than a demographic guess. And they are working against sunk cost: a $2,000 fee set beside a $60,000 loss reads as a rational attempt on the larger number, and the pitch keeps that comparison in view.

Lists of prior victims — "sucker lists" in the trade, "reload lists" in the Federal Trade Commission's (FTC) consumer materials — are sold between operations, and sometimes sold by the operation that created them. On chain, part of the list assembles itself: every address that paid into a known scam address is public, permanently, on any block explorer.

## The variants

Ordered by what they cost the target.

**A seed-phrase "validation" tool.** A page asks for the recovery phrase, or for a signature, to "verify ownership before the funds are released". This is a [wallet drainer](/wiki/economics/finance/fraud/wallet-drainer) with a recovery story attached, and it takes everything left in the wallet rather than a fee.

**Advance-fee recovery services.** A tracing retainer, a "court filing fee", a bond, a share of the recovered sum payable in advance. Each payment is followed by a new obstacle with a price.

**Fake asset-recovery firms.** Cloned law-firm sites carrying a real firm's name, real attorney biographies, and one altered contact detail; case studies with unverifiable client initials; registration numbers that resolve to nothing.

**Agency impersonation.** The FBI warned publicly in 2024 about criminals impersonating its own Internet Crime Complaint Center (IC3), contacting people who had filed complaints and citing their case. Others impersonate the FTC, a bankruptcy trustee, or a court clerk. No agency arranges a payment with a victim.

**Fake class-action and estate distributions.** Real insolvencies generate real claim registers, and the registers are public court filings, so notices citing a genuine claim amount and case number defeat the check most people would run. Claimants of Celsius and FTX have both been targeted; the August 2023 breach at claims agent Kroll exposed contact data for FTX, BlockFi, and Genesis claimants, and phishing followed within days.

**The unfreezing fee.** The "customs duty" or "capital gains tax" demanded before a balance on a fake platform can be withdrawn is the tail of the original fraud, billed by the same operator against the same non-existent balance. Victims of [pig butchering](/wiki/economics/finance/fraud/pig-butchering) and [giveaway scams](/wiki/economics/finance/fraud/giveaway-scam) meet it in both forms.

## The technical dressing

Four claims carry most of the pitches, and none describes anything that exists.

*"We can reverse the transaction."* Nothing can. *"We can recover your private key."* Searching a 256-bit keyspace is not a service anyone sells; the legitimate version of that business recovers a forgotten password for a wallet file its owner still holds, which has no bearing on funds sent to somebody else's address. *"Sign here to validate your seed phrase."* That is the drainer. *"Fund the gas bond for the release contract."* Gas is paid by whoever sends a transaction, and no contract charges a recipient to release funds already theirs.

## Why nothing can be reversed

A transfer is a state change authorized by a signature from the sending key. Once it is included in a block and finalized, the balance is at the destination, and only the key controlling that destination can move it again. There is no operator of the network holding an undo, and no party a court can order to rewrite the ledger. A court can order a *recipient* to return funds, which requires identifying them and having jurisdiction; that order runs against the person, not the chain.

The single protocol-level exception in Ethereum's history was the 2016 hard fork after [The DAO](/wiki/economics/finance/defi/dao) was drained, which required the whole network to adopt an irregular state change and split the chain in two. It has not been repeated, and no mechanism exists to do it for one person's loss.

## What recovery actually looks like

**Seizure and remission.** Law enforcement seizes keys or freezes accounts, the government forfeits the assets, and victims petition for remission out of the forfeited pool. The 2016 Bitfinex hack produced a seizure of roughly 94,000 bitcoin in February 2022, guilty pleas from Ilya Lichtenstein and Heather Morgan in August 2023, and sentences in late 2024: eight years from theft to resolution.

**A bankruptcy estate.** FTX filed in November 2022, its plan took effect in January 2025, and distributions began the following month at petition-date claim values rather than current ones. Celsius creditors waited from July 2022 to distributions in early 2024.

**An exchange or issuer freeze.** If the funds reached a custodial venue, its compliance team can freeze the account pending legal process, and a stablecoin issuer can blacklist an address at the contract level: Tether froze $225 million identified with the Justice Department in November 2023. Both act on the destination rather than on the transfer, and this is the only route measured in hours, so reporting speed dominates.

None of these routes releases funds in exchange for a payment. A law firm or a tracing firm can legitimately bill for work, but what it sells is a report or litigation, never the balance itself, which it has no power to move.

## What to do

1. Preserve evidence first: transaction hashes, addresses, timestamps, the platform's domain, and screenshots of every conversation. Accounts and sites disappear within days.
2. File with the FBI Internet Crime Complaint Center at `ic3.gov`. The complaint number is what later connects a loss to a seizure and a remission.
3. If any hop landed at a centralized exchange — which a block explorer will show — send that exchange's compliance team the transaction hash immediately.
4. File with the state securities or banking regulator and with the FTC. Domestic exchanges and money transmitters report under [FinCEN](/wiki/economics/finance/regulation/fincen) rules, and complaints of this kind trigger those obligations.
5. Treat every subsequent inbound offer as the second attempt. Details of the original loss in a stranger's message are evidence of a sold list, not of an investigation, and the proceeds of both attempts follow the same path to [cashing out](/wiki/economics/finance/fraud/cashing-out).

## External links

- [FBI Internet Crime Complaint Center](https://www.ic3.gov/) — where to file, and the public service announcements on fake recovery services and on impersonation of the Center
- [FTC consumer advice](https://consumer.ftc.gov/) — refund and recovery scam guidance, including the reload-list mechanism
- [Department of Justice press releases](https://www.justice.gov/news) — seizures, forfeitures, and charges in crypto fraud cases
- [forfeiture.gov](https://www.forfeiture.gov/) — notices of federal forfeiture actions and the petition process victims use
- [Chainalysis blog](https://www.chainalysis.com/blog/) — what on-chain tracing can and cannot establish
