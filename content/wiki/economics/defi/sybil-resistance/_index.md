---
title: "Sybil Resistance"
weight: 17
bookCollapseSection: true
---

Sybil resistance is whatever stops one participant in an open network from counting as many. A network that lets anyone join cannot tell a thousand independent participants from one participant running a thousand nodes, so it cannot safely give each node a vote. A Sybil-resistance mechanism ties influence to something that costs more to have more of, such as computation, locked-up currency or disk space. Splitting that resource across many identities then gains nothing.

This is what "proof of work", "proof of stake" and their relatives are. Each is a way for a participant to show, at little cost to whoever checks, that it controls some quantity of a scarce resource. The network then weights participants by that quantity.

They are often called consensus mechanisms, and that blurs two jobs. A Sybil-resistance mechanism decides who has a say and how much. A [consensus protocol](/wiki/economics/defi/consensus) decides how those with a say come to agree. Bitcoin pairs proof of work with the longest-chain rule. Kaspa pairs proof of work with a different rule, and Cardano pairs the longest-chain rule with stake. The two layers vary independently, and this section is about the first. Where a mechanism also dictates part of the agreement rule, the page says so and links across.

## The attack

John Douceur named the problem in 2002, writing about peer-to-peer systems in general: "if a single faulty entity can present multiple identities, it can control a substantial fraction of the system". His paper argues that the problem cannot be designed away. "Without a logically centralized authority, Sybil attacks are always possible except under extreme and unrealistic assumptions of resource parity and coordination among entities."

The name is from *Sybil*, a 1973 book about a woman with multiple personalities. The paper's acknowledgments credit Brian Zill with suggesting it.

Two responses exist, and every mechanism here is one of them.

- **Have an authority.** Someone decides who is admitted. That is [proof of authority](/wiki/economics/defi/sybil-resistance/proof-of-authority), and in a different form [proof of personhood](/wiki/economics/defi/sybil-resistance/proof-of-personhood).
- **Stop counting identities.** Have each participant demonstrate a resource, and count the resource. How many identities hold it then makes no difference. Bitcoin's paper puts the choice in one line: "If the majority were based on one-IP-address-one-vote, it could be subverted by anyone able to allocate many IPs. Proof-of-work is essentially one-CPU-one-vote."

A survey by Bano and co-authors calls the resource-based schemes that came after Bitcoin *proof-of-X*: protocols "that replace wasteful computations with useful work derived from alternative commonly accessible resources, or remove computational work altogether."

## What the resource has to be

Three properties recur across the pages below.

- **Costly to have more of.** Influence then tracks expense, and the number of identities is irrelevant.
- **Cheap for others to verify.** Anyone must be able to check a claim without trusting the claimant.
- **Countable once.** One unit of the resource must not back two identities, or two competing histories, at the same time. Proof of work gets this by binding each puzzle solution to one block. Proof of stake gets it from the ledger, which records each coin once. Disk-based schemes have to work for it, since the same bytes could otherwise be shown to two challengers.

## Two questions that sort them

Lewis-Pye and Roughgarden give the general form. A protocol runs against a *resource pool*: a function that assigns every public key a non-negative balance at every moment. For proof of work the balance is a key's computing power. For proof of stake it is "fully determined by 'on-chain' information".

Two questions about the pool separate the mechanisms.

**Is the resource on the ledger?** If it is, the protocol knows the total and each participant's share. It can require signatures from a fixed fraction of the whole, and it can destroy the holdings of a participant caught cheating. If the resource is outside the ledger, as computing power is, the total is unknown and can change without notice. The same authors prove a consequence: "No protocol is both adaptive and has finality", where *adaptive* means it keeps running when the size of the pool is unknown. Their reason is that "extended periods of asynchrony cannot be distinguished from a waning resource pool". A chain that cannot tell a slow network from departed participants has to keep going, and so cannot promise that a block is final. The [Consensus](/wiki/economics/defi/consensus#finality-or-availability) overview takes this further.

**Is the resource spent or held?** Work is spent: each block costs fresh electricity, so an old block carries the cost of making it. Stake and disk space are held: they are committed for a while and then released. Signing with a held resource costs nothing extra, which opens two attacks the survey lists for these schemes. In the *nothing-at-stake* attack "miners are incentivized to extend every potential fork", because extending a chain is cheap. In the *long-range* attack an adversary obtains keys that "had considerable value in the past" and rewrites history from that point. Both are covered under [proof of stake](/wiki/economics/defi/sybil-resistance/proof-of-stake#nothing-at-stake).

| Mechanism | Resource | On the ledger | Spent or held |
|---|---|---|---|
| Proof of work | computation | no | spent |
| Proof of stake | the chain's own currency | yes | held |
| Proof of space | disk capacity | no | held |
| Proof of storage | stored data that someone wants kept | the disks are not; on Filecoin the tally of proven storage and the collateral are | held |
| Proof of burn, proof of transfer | currency given up, the chain's own or another chain's | on the chain where it is spent | spent |
| Proof of authority | a place on an approved list | | |
| Proof of personhood | being one distinct person | | |
| Proof of elapsed time | a processor with a trusted enclave | no | held |
| Proof of useful work | computation that has other value | no | spent |

## In this section

[Proof of work](/wiki/economics/defi/sybil-resistance/proof-of-work) comes first because the others are defined against it: a hash puzzle whose solution shows computation was done, and the origin of the whole idea in anti-spam schemes of the 1990s. [Proof of stake](/wiki/economics/defi/sybil-resistance/proof-of-stake) replaces the puzzle with a deposit in the chain's own currency, and is where slashing, nothing-at-stake and long-range attacks are explained.

The next two use disk. [Proof of space](/wiki/economics/defi/sybil-resistance/proof-of-space) has a participant fill storage with data that has no other use, and prove it is still there. [Proof of storage](/wiki/economics/defi/sybil-resistance/proof-of-storage) has it hold data that someone is paying to keep, which is a harder thing to prove and brings the mechanism close to a storage market.

[Proof of burn and proof of transfer](/wiki/economics/defi/sybil-resistance/proof-of-burn) spend currency, usually that of a different chain, destroying it or handing it to someone else, to earn standing.

Two mechanisms use no tradable resource. [Proof of authority](/wiki/economics/defi/sybil-resistance/proof-of-authority) is a list of approved signers. [Proof of personhood](/wiki/economics/defi/sybil-resistance/proof-of-personhood) tries to give each human being one vote, by ceremony, by biometrics or by vouching.

The last two are variations on proof of work that have seen little use. [Proof of elapsed time](/wiki/economics/defi/sybil-resistance/proof-of-elapsed-time) replaces the puzzle with a timer run inside trusted hardware. [Proof of useful work](/wiki/economics/defi/sybil-resistance/proof-of-useful-work) asks whether the computation could be worth something in its own right.

## Names that do not belong here

Some things called "proof of" are not about who gets a say. Solana's [proof of history](/wiki/economics/defi/consensus/proof-of-history) is a clock, and sits with the consensus protocols. A [zero-knowledge proof](/wiki/cs/zero-knowledge-proofs) shows that a statement is true or that a computation was carried out correctly, and says nothing about the prover's resources. A storage proof used only to audit a storage contract, as opposed to weighting consensus, is an audit, and the proof of storage page draws that line.

## Sources

- Douceur, [The Sybil Attack](https://www.freehaven.net/anonbib/cache/sybil.pdf), International Workshop on Peer-to-Peer Systems (2002)
- Nakamoto, [Bitcoin: A Peer-to-Peer Electronic Cash System](https://bitcoin.org/bitcoin.pdf) (2008)
- Bano, Sonnino, Al-Bassam, Azouvi, McCorry, Meiklejohn & Danezis, [SoK: Consensus in the Age of Blockchains](https://arxiv.org/abs/1711.03936) (2017)
- Lewis-Pye & Roughgarden, [Resource Pools and the CAP Theorem](https://arxiv.org/abs/2006.10698) (2020)

## Wiki Pages

{{< section >}}
