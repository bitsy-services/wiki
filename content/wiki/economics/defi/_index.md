---
title: "DeFi"
weight: 10
bookCollapseSection: true
---

Decentralised finance is what you get when the machinery of conventional finance is rebuilt on a public [blockchain](/wiki/economics/defi/blockchain). The clearing house becomes a [smart contract](/wiki/economics/defi/smart-contract); the market maker becomes a pot of tokens and a formula; the ledger is world-readable and the functions are world-callable. What you gain is composability and the absence of a gatekeeper — any protocol can call any other, and nobody has to approve your account first. What you give up is the ability to undo a mistake.

This is the largest section of the wiki. It runs from what a [currency](/wiki/economics/defi/blockchain/currency) is up to the specific mechanisms Bitsy is building, in ten sections that read in order: the substrate first, then what trades on it, then what is built on top.

[Blockchain](/wiki/economics/defi/blockchain) is the ledger itself and what it accounts for — currency, cryptocurrency, tokens fungible and not, the nonce that orders an account's transactions, and the gateways between a bank account and a chain. [Smart contract](/wiki/economics/defi/smart-contract) is the program that lives at an address and runs when called: what makes one final, what a decentralized application and a decentralized autonomous organization add on top, and where the hardware enclave fits. [Chains](/wiki/economics/defi/chains) is the instances — [Ethereum](/wiki/economics/defi/chains/ethereum), which the rest of the section assumes, and the chains and storage networks chosen for one property each.

[Markets](/wiki/economics/defi/markets) is the heart of it: the [decentralized exchange](/wiki/economics/defi/markets/dex), the automated market maker and the invariant that prices a pool, [Uniswap](/wiki/economics/defi/markets/uniswap) as the canonical implementation, and what supplying the liquidity costs — impermanent loss, extractable value, and the two standard ways of being paid to leave capital in place. [Oracles](/wiki/economics/defi/oracles) fills the two gaps a contract cannot fill itself: it cannot see off-chain, and it cannot wake up. [Options](/wiki/economics/defi/options) is the derivatives layer, from what a call is up through Bitsy's fully collateralized cash-backed synthetic options and the fee machinery that funds them.

[Par token](/wiki/economics/defi/par-token) is the instrument Bitsy's other mechanisms add up to — a token that cannot trade below parity because there is nothing beneath it to sell into — and the section holds the guarantees it is composed from. [Development](/wiki/economics/defi/development) is building a contract and reading the results back out: Solidity and its toolchain, The Graph for indexing, Groth16 for verifying a computation a contract cannot afford to re-run. [Token registration](/wiki/economics/defi/token-registration) and [token false alarms](/wiki/economics/defi/token-false-alarms) are the unglamorous halves of shipping a token: the standard has no icon field, so the logo beside a balance comes from a dozen separate submissions to organizations that mostly do not share data, and the same organizations run the scanners that decide whether a wallet warns about your token.

The law that binds all of this is next door in [Regulation](/wiki/economics/regulation), including [DeFi and US regulatory restrictions](/wiki/economics/regulation/defi-us-regulatory-restrictions), the jurisdictional fight over which agency a token answers to. [Fraud](/wiki/economics/fraud) is what the mechanisms here make possible when pointed the other way.

## Wiki Pages

{{< section >}}
