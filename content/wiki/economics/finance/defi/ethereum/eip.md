---
title: "EIP and ERC"
weight: 5
---

An **Ethereum Improvement Proposal (EIP)** is the design document through which
every change to [Ethereum](/wiki/economics/finance/defi/ethereum/) is proposed,
argued over, and ratified. An **Ethereum Request for Comments (ERC)** is one
category of EIP — the category covering application-level conventions such as
token interfaces.

The two names get used interchangeably in casual writing. They are not two
processes: ERC is a *subset* of EIP, and both draw from the same number
sequence, so the standard filed as EIP-20 is called
[ERC-20](/wiki/economics/finance/defi/ethereum/erc-20) everywhere else.

Since late 2023 they also live in different repositories. Every ERC document
moved to `ethereum/ERCs` — the old ones too, so `erc-20.md` is there rather
than in `ethereum/EIPs`, which now holds only the Core, Networking, Interface,
Meta and Informational proposals. "Look it up under EIPs" stopped working for
token standards at that point.

## The number is assigned once

An EIP number is issued when the proposal is first merged as a draft, before
anyone knows whether it will succeed. The number is not a version, a ranking, or
a date — it is just the next free integer. EIP-20 is early because it was
proposed in 2015, not because it is foundational.

Because the number is assigned once and never reused, a standard keeps its
number through every status change. ERC-20 sat as a draft for years before it
was finalised, and it was already the de facto token standard for most of that
time.

## Types and categories

EIP-1 defines three **types**, and only one of them is subdivided:

| Type | Category | What it changes | Who must adopt it |
|---|---|---|---|
| **Standards Track** | **Core** | Consensus rules — the protocol itself | Every node, via a coordinated network upgrade |
| **Standards Track** | **Networking** | The peer-to-peer layer (devp2p, gossip) | Client implementers |
| **Standards Track** | **Interface** | Client APIs such as JSON-RPC | Client implementers and tooling |
| **Standards Track** | **ERC** | Application-level conventions | Nobody — adoption is voluntary |
| **Meta** | — | The process itself | The people running it |
| **Informational** | — | Nothing; it offers guidance | Nobody |

So an ERC is not a peer of Meta and Informational — it is one of four categories
*inside* Standards Track. On the EIPs index a token standard shows as
`type: Standards Track, category: ERC`, and both fields matter when searching
for one.

**An ERC is not enforced by the protocol.** The
[EVM](/wiki/economics/finance/defi/ethereum#the-ethereum-virtual-machine-evm)
has no idea what ERC-20 is. A contract "is" an ERC-20 token purely because it
exposes the functions that wallets and
[DEXs](/wiki/economics/finance/defi/dex) expect to call. Nothing stops a
contract from exposing those functions and behaving badly — returning `false`
instead of reverting, taking a fee on transfer, or omitting a return value
entirely. Every one of those has shipped to mainnet and broken integrators who
assumed the standard was a guarantee.

A Core EIP is the opposite. Once it activates at a block height, every node
enforces it, and a contract cannot opt out.

## Status

An EIP moves through a fixed lifecycle:

```text
Idea → Draft → Review → Last Call → Final
         │       │
         └───────┴──→ Stagnant   (inactive 6+ months; can return to Draft)

  any pre-Final state ──→ Withdrawn   (the author gives up on it)
```

The Stagnant branch hangs off Draft and Review specifically — a proposal that
has reached Last Call is either finished or sent back for more work, not left
to rot. Separately, a handful of EIPs are **Living**: never final by design,
because they are meant to keep changing. EIP-1 itself is one.

Only **Final** means settled. In practice, adoption and status drift apart in
both directions — ERC-20 was universal while still a draft, and plenty of Final
ERCs have almost no deployments. Read the status to learn whether the *text* can
still change, not whether the standard is real.

## Reading an EIP

Every proposal carries the same sections, and several of them carry more
information than the specification does:

- **Motivation** — the problem being solved. If this doesn't describe a problem
  you have, the rest is noise.
- **Rationale** — why the design is what it is. This is where the rejected
  alternatives are recorded, and it usually answers "why is this so awkward?"
- **Backwards Compatibility** — what breaks. For an ERC extending an existing
  standard, this is where you learn whether existing integrations keep working.
- **Security Considerations** — mandatory. An EIP cannot reach Final without
  one, and a proposal that claims to have no security implications has to say so
  and defend it.

The [ERC-677](/wiki/economics/finance/defi/ethereum/erc-677) and
[ERC-1363](/wiki/economics/finance/defi/ethereum/erc-1363) pages are a good
worked example of the Rationale section mattering: both solve ERC-20's
`approve` + `transferFrom` two-step, and the differences between them are
entirely design-rationale differences, not capability differences.

## Standards with pages here

- [ERC-20](/wiki/economics/finance/defi/ethereum/erc-20) — fungible tokens
- [ERC-667](/wiki/economics/finance/defi/ethereum/erc-667) — the early `transferAndCall`; never merged as a proposal, and routinely confused with ERC-677
- [ERC-677](/wiki/economics/finance/defi/ethereum/erc-677) — the version that stuck
- [ERC-1363](/wiki/economics/finance/defi/ethereum/erc-1363) — transfer and approval callbacks
- [ERC-4626](/wiki/economics/finance/defi/ethereum/erc-4626) — tokenized vaults
- [ERC-8004](/wiki/economics/finance/defi/ethereum/erc-8004) — trustless agent identity

## External links

- [EIPs repository](https://github.com/ethereum/EIPs) — everything except ERCs
- [ERCs repository](https://github.com/ethereum/ERCs) — where ERCs have lived since the late-2023 split
- [eips.ethereum.org](https://eips.ethereum.org/) — rendered index by status and category
- [EIP-1](https://eips.ethereum.org/EIPS/eip-1) — the EIP describing the EIP process
- [ERC index](https://eips.ethereum.org/erc) — ERC-track proposals only
- [Ethereum Magicians](https://ethereum-magicians.org/) — where proposals are argued before they are drafted
