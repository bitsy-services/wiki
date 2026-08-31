---
title: "DeFi"
weight: 10
bookCollapseSection: true
---

Decentralised finance is what you get when the machinery of [finance](/wiki/economics/finance) is rebuilt on a public [blockchain](/wiki/economics/finance/defi/blockchain). The clearing house becomes a [smart contract](/wiki/economics/finance/defi/smart-contract); the market maker becomes a pot of tokens and a formula; the ledger is world-readable and the functions are world-callable. What you gain is composability and the absence of a gatekeeper — any protocol can call any other, and nobody has to approve your account first. What you give up is the ability to undo a mistake.

This is the largest section of the wiki. It runs from what a [currency](/wiki/economics/finance/defi/currency) is up to the specific mechanisms Bitsy is building, and the pages below are grouped by what they are *for*. The sidebar lists them in reading order.

## Foundations

The vocabulary everything else assumes. A [blockchain](/wiki/economics/finance/defi/blockchain) is an append-only ledger maintained by parties who do not trust each other; a [cryptocurrency](/wiki/economics/finance/defi/cryptocurrency) is what it accounts for; a [smart contract](/wiki/economics/finance/defi/smart-contract) is code that lives at an address and runs when called. On top of those sit the [decentralized application](/wiki/economics/finance/defi/dapp), the [DAO](/wiki/economics/finance/defi/dao) that governs one, and the loose banner of [Web3](/wiki/economics/finance/defi/web3) covering the lot. Tokens come in two shapes — fungible, where one unit substitutes for any other, and [non-fungible](/wiki/economics/finance/defi/nft), where each has its own identity.

Several properties of that substrate matter enough to have their own pages: a [finalized smart contract](/wiki/economics/finance/defi/finalized-smart-contract) is one nobody — including its author — can change; a [nonce](/wiki/economics/finance/defi/nonce) is what keeps transactions ordered and unrepeatable; [vanity addresses](/wiki/economics/finance/defi/vanity-addresses) are what you get by mining the address derivation itself. A [trusted execution environment](/wiki/economics/finance/defi/tee) is the hardware answer to a problem chains solve socially, and a [cryptocurrency gateway](/wiki/economics/finance/defi/cryptocurrency-gateway) is the on-ramp between this world and a bank account. Fees on a busy chain are also why [micro-transactions](/wiki/economics/finance/defi/micro-transactions) remain hard.

## Chains and platforms

[Ethereum](/wiki/economics/finance/defi/ethereum) is the reference implementation of a programmable chain and the platform most of this section assumes. The others here were each chosen for a specific property: [Sui](/wiki/economics/finance/defi/sui) for object-centric throughput, [IOTA](/wiki/economics/finance/defi/iota) for feeless machine-to-machine transfer, [Sapphire](/wiki/economics/finance/defi/sapphire) for a confidential [EVM](/wiki/economics/finance/defi/ethereum#the-ethereum-virtual-machine-evm) where state and calldata are encrypted, and [Arweave](/wiki/economics/finance/defi/arweave) for pay-once permanent storage.

## Trading and market making

The heart of DeFi. A [decentralized exchange](/wiki/economics/finance/defi/dex) replaces the order book with an [automated market maker](/wiki/economics/finance/defi/amm) — a [liquidity pool](/wiki/economics/finance/defi/liquidity-pool) priced by an invariant, usually the [constant product formula](/wiki/economics/finance/defi/constant-product-formula) or its weighted cousin, the [constant mean formula](/wiki/economics/finance/defi/constant-mean-formula). [Uniswap](/wiki/economics/finance/defi/uniswap) is the canonical implementation, and its concentrated liquidity rests on [virtual reserves](/wiki/economics/finance/defi/virtual-reserves): a trick for making limited capital behave like a much deeper pool.

Providing that liquidity is not free. [Impermanent loss](/wiki/economics/finance/defi/impermanent-loss) is what the pool costs you when the price moves, [volatility](/wiki/economics/finance/defi/volatility) is the input that determines how much, and [maximal extractable value](/wiki/economics/finance/defi/maximal-extractable-value) is what block producers take from the ordering of your trade. [Staking](/wiki/economics/finance/defi/staking) and [yield farming](/wiki/economics/finance/defi/yield-farming) are the two standard ways of being paid to leave capital in place, and [transfer on join/exit vs. mint/burn](/wiki/economics/finance/defi/transfer-on-join-exit-vs-mint-burn) is the accounting choice underneath any of them.

## Oracles and automation

A smart contract cannot see outside its own chain, and it cannot wake itself up. Both gaps have to be filled from outside. An [oracle node](/wiki/economics/finance/defi/oracle-node) brings external data in, [Chainlink](/wiki/economics/finance/defi/chainlink) is the dominant network for doing so, and a [staked consensus oracle](/wiki/economics/finance/defi/staked-consensus-oracle) is the design pattern that makes reported values expensive to lie about. [Oracle-free pricing](/wiki/economics/finance/defi/oracle-free-pricing) sidesteps the whole category by reading price off the geometry of an on-chain position instead. For the waking-up problem, a [decentralized keeper](/wiki/economics/finance/defi/decentralized-keeper) runs the cron jobs of DeFi — liquidations, settlements, feed updates.

## Derivatives and prediction

[Options](/wiki/economics/finance/defi/options) is a section in its own right, running from what a call is up through Bitsy's fully-collateralized cash-backed synthetic options. Alongside it, a [prediction market](/wiki/economics/finance/defi/prediction-market) prices the probability of an event rather than an asset, and [prediction market event time](/wiki/economics/finance/defi/prediction-market-event-time) is the surprisingly awkward question of *when* an event is deemed to have happened.

## Bitsy protocol design

The mechanisms behind Bitsy's own contracts, several of which are novel enough to warrant a page each. [Full-reserve backing](/wiki/economics/finance/defi/full-reserve-backing) and [locked liquidity](/wiki/economics/finance/defi/locked-liquidity) are the structural guarantees; together they produce a [liquidity floor](/wiki/economics/finance/defi/liquidity-floor), a price nothing can trade below because there is nothing beneath it to sell into. A [par token](/wiki/economics/finance/defi/par-token) is the instrument those properties add up to, and a [permissionless token factory](/wiki/economics/finance/defi/permissionless-token-factory) is how one gets deployed without asking anyone.

The revenue side is the [collateralization fee](/wiki/economics/finance/defi/collateralization-fee), charged against staked collateral and collected by the [Fee Box](/wiki/economics/finance/defi/fee-box). [Interbox](/wiki/economics/finance/defi/interbox) is a separate proposal: moving fiat from a US bank account to a self-custodied wallet on the strength of the KYC the bank already did.

## Tooling

[Solidity patterns](/wiki/economics/finance/defi/solidity) covers the language and the Foundry toolchain used to build and deploy these contracts. [The Graph](/wiki/economics/finance/defi/the-graph) covers reading the results back out — indexing chain events into something you can query. [Groth16](/wiki/economics/finance/defi/groth16) is the zero-knowledge proof system that shows up whenever a contract needs to verify a computation it cannot afford to re-run. [Token registration](/wiki/economics/finance/defi/token-registration) is the unglamorous other half of shipping a token: [ERC-20](/wiki/economics/finance/defi/ethereum/erc-20) has no icon field, so the logo beside a balance comes from six or seven separate submissions to companies that do not share data.

## Law and adjacent uses

[DeFi and US regulatory restrictions](/wiki/economics/finance/defi/defi-us-regulatory-restrictions) is a snapshot of a fragmented and fast-moving enforcement landscape, concentrating on the jurisdictional fight between the Securities and Exchange Commission (SEC) and the Commodity Futures Trading Commission (CFTC); the [regulation](/wiki/economics/finance/regulation) section next door covers the other half — the [Bank Secrecy Act](/wiki/economics/finance/regulation/bank-secrecy-act), [KYC](/wiki/economics/finance/regulation/know-your-customer), and [sanctions](/wiki/economics/finance/regulation/ofac-sanctions). [Smart contracts in real estate](/wiki/economics/finance/defi/smart-contracts-in-real-estate) looks at the most-cited non-financial application and where it actually runs aground.

## Wiki Pages

{{< section >}}
