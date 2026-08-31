---
title: "Anatomy of a Crypto Scam"
weight: 10
---

The frauds in this section have almost nothing in common at the level of technique. A [honeypot token](/wiki/economics/finance/fraud/honeypot-token) is a few lines in a transfer function; [pig butchering](/wiki/economics/finance/fraud/pig-butchering) is six months of conversation conducted by a trafficked worker reading from a script. What they share is a set of problems every one of them has to solve in the same order, and the order is what makes them recognisable to somebody who does not know the specific technique.

Four problems, and each has a cost the operator has to pay.

## Reach, credibility, irreversibility, realisation

**Reach** is getting in front of somebody who holds value. It is the cheapest stage and therefore the least useful place to look for tells: an unsolicited message costs nothing to send, and a scam that converts one target in fifty thousand is still profitable if the messages are free. This is why the volume frauds — [giveaway scams](/wiki/economics/finance/fraud/giveaway-scam), [address poisoning](/wiki/economics/finance/fraud/address-poisoning), spam [fake tokens](/wiki/economics/finance/fraud/fake-token) — are structured as sprays and why blocking them individually never reduces their number.

**Credibility** is making the offer survive a look. It is the expensive stage, and the one where the operator's constraints show. Building it costs either money (a cloned exchange front end, a purchased verified account, a deepfaked video call), time (the months of relationship in a pig-butchering approach), or a borrowed reputation (an impersonated project, a compromised Discord, a paid influencer). The tells live here because credibility is manufactured and manufacturing leaves marks.

**Irreversibility** is getting value across a line it cannot come back over. This is the stage the [blockchain](/wiki/economics/finance/defi/blockchain) supplies for free, and the reason these frauds concentrate on this rail rather than on cards. A card payment is provisional for months. A confirmed transfer is provisional for zero seconds, and there is no arbitration body to appeal to — the same property that gives [Zelle](/wiki/economics/finance/payments/zelle) its [liability problem](/wiki/economics/finance/payments/zelle/fraud-and-liability), with no bank on either end to absorb the loss.

**Realisation** is converting the proceeds into something spendable. It is the stage the operator cannot skip and the one where enforcement actually works, because it is the only point that must touch an institution with a name on file. Everything on [cashing out](/wiki/economics/finance/fraud/cashing-out) and [money mules](/wiki/economics/finance/fraud/money-mule) is about this stage, and so is most of the [anti-money-laundering](/wiki/economics/finance/regulation/anti-money-laundering) regime.

```text
  reach          credibility        irreversibility      realisation
  ------         -----------        ---------------      -----------
  free           expensive          free (the chain)     expensive, risky
  no tells       the tells          point of no return   where cases are made
  ~0 defence     reader's leverage  binary               law enforcement's leverage
```

The two stages that cost the operator something are the two where a defender has leverage, and they are at opposite ends. A reader gets one shot, before the transfer. An investigator gets one shot, after it.

## Where the line sits

"Do not send money to strangers" is useless advice for the same reason "do not click links" is: it does not say when. The useful version is knowing, for a given fraud, which action is the irreversible one, because everything before it is free to walk away from and everything after it is not.

```text
fraud                     the irreversible act
-----                     --------------------
rug pull                  buying the token
honeypot token            buying the token
pig butchering            the deposit to the platform address
giveaway scam             the outbound transfer
approval phishing         signing the approval — not the later transfer
wallet drainer            signing, likewise
address poisoning         confirming a send to the pasted address
exchange collapse         the deposit; the withdrawal request is already too late
SIM swap                  nothing the victim does — the port completes without them
```

[Approval phishing](/wiki/economics/finance/fraud/approval-phishing) moves the point of no return to a *signature* that costs no gas, produces no transaction, and appears nowhere in the victim's history — the theft happens later, at a time the attacker chooses, and the victim's own records will not show what authorised it. And a [SIM swap](/wiki/economics/finance/fraud/sim-swap) has no victim action at all: the carrier does it, which is why the defence has to be configured months in advance rather than exercised in the moment.

## Tells that do not require knowing the scam

Domain knowledge does not generalise; structure does. Each of these is a property of the interaction rather than of the technology, so it works on a fraud the reader has never seen.

- **The contact was inbound.** Almost no legitimate investment arrives as an unsolicited message, and the exceptions are ones you can verify from your side.
- **The verification path is supplied by the party being verified.** A link in the message, a support number in the email, a contract address pasted in a reply. The correct move is always to reach the counterparty by a route you already had.
- **Receiving money requires sending money.** Taxes, unfreezing fees, gas bonds, verification deposits, a payment to release a withdrawal. There is no legitimate structure that works this way, which is why it is the single most reliable tell on the list and why [recovery scams](/wiki/economics/finance/fraud/recovery-scam) fail this test the same way the original fraud did.
- **The deadline is not yours.** Urgency exists to prevent the check, so its presence is evidence about the offer rather than about the opportunity.
- **The counterparty is unreachable outside the channel.** No registered entity, no named principals, no jurisdiction — or names that appear only on the site itself.

## Checks that read as diligence and are not

The list of things that feel like verification and do not constrain the outcome is longer, and each of them has been used as the credibility layer for a real fraud.

- **"The contract is open source."** [Forsage](/wiki/economics/finance/fraud/ponzi-scheme) published its contract for the entire time it operated. The code implemented the scheme correctly; the scheme was the fraud.
- **"It has been audited."** An audit covers a commit, not a deployment. If the contract sits behind an upgradeable proxy, the audited implementation can be replaced afterwards — see [hidden admin controls](/wiki/economics/finance/fraud/hidden-admin-controls).
- **"Ownership is renounced."** Renouncing is one transaction on one contract. It says nothing about a proxy admin, a minter role, a second privileged address, or a supply the deployer already holds.
- **"Liquidity is locked."** For how long, what fraction, and by whom — a thirty-day lock on 20% of the pool is a countdown, not a guarantee. [Locked liquidity](/wiki/economics/finance/defi/locked-liquidity) has a specific meaning that most tokens claiming it do not meet, and a team allocation held outside the pool empties it without touching the lock at all, which is the [rug pull](/wiki/economics/finance/fraud/rug-pull) that leaves every screenshot accurate.
- **"It has a large market capitalisation."** Circulating supply times last trade price, where the last trade may have been [wash traded](/wiki/economics/finance/fraud/wash-trading) and the price is set by a pool that cannot absorb a 1% exit. Pool depth is the number that constrains anything; market cap is not.
- **"The volume is high."** See above. On a venue that reports its own figures, volume is a marketing metric, and buying that arrives on a schedule is a [pump](/wiki/economics/finance/fraud/pump-and-dump) rather than a market.
- **"It withdrew fine last time."** The permitted small withdrawal is a deliberate step in the pig-butchering script, bought at a cost the operator has already priced.

The common failure in that list is trusting an artefact the counterparty produced. An audit, a lock, a renouncement, a badge, and a volume figure are all assertions by or about the party asking for money, and the useful question is which of them a hostile deployer could not have arranged.

## Afterwards

An on-chain transfer to an address someone else controls cannot be reversed by the sender, the wallet, the chain, or a court. What remains is narrow and slow: report to the FBI's Internet Crime Complaint Center (IC3), notify the receiving exchange with the transaction hash if the funds moved to a custodial venue, where a freeze is occasionally possible in the first hours, and expect any actual return of funds to come through a seizure or a bankruptcy estate years later. Anyone who offers to recover it for a fee is running the [second scam](/wiki/economics/finance/fraud/recovery-scam) against the list the first one produced.

## External links

- [FBI Internet Crime Complaint Center annual reports](https://www.ic3.gov/AnnualReport/Reports) — reported US losses by category, including a separate crypto report
- [Chainalysis Crypto Crime Report](https://www.chainalysis.com/crypto-crime/) — annual on-chain estimates of scam, ransomware, and stolen-funds volume
- [FTC consumer protection data spotlights](https://www.ftc.gov/news-events/data-visualizations/data-spotlight) — the Federal Trade Commission's reporting on investment and romance scam losses
- [CFTC customer advisories](https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/index.htm) — the Commodity Futures Trading Commission's advisories, which describe live schemes in detail
