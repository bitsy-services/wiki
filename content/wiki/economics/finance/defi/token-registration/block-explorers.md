---
title: "Block Explorers"
weight: 40
---

A block explorer's token page is the first result when anyone searches a contract address, and its logo, description and links come from the explorer's own database, not the chain. Two explorer families cover most EVM chains — Ethereum Virtual Machine chains — and each has its own page here:

| | [Etherscan](/wiki/economics/finance/defi/token-registration/etherscan) family | [Blockscout](/wiki/economics/finance/defi/token-registration/blockscout) |
| --- | --- | --- |
| Covers | Etherscan, Basescan, Arbiscan, Polygonscan, BscScan, OP Mainnet's Etherscan, and the rest of the thirty-odd explorers Etherscan lists | Blockscout-hosted instances, including Ethereum, Base, Arbitrum One, OP Mainnet and Polygon |
| Channel | Token Update Application Form, one per explorer | token info application form, one per instance |
| Prerequisites | verified source, then a signed ownership proof | verified source, then a signed ownership proof |
| Who may sign | the creator Etherscan displays; its one readable article on factory deployments sends them to support | creator or `owner()`; the web front end also offers the sender of a factory deployment, backend unconfirmed |
| Logo | a link to a 32 × 32 SVG or 64 × 64 PNG | a link to an SVG or a 48 × 48 PNG |
| Cost | free; paid priority support, price shown after submitting | free; 99 USDC or USDT for a decision within seven days |
| Reads aggregators | CoinMarketCap, for market data | CoinGecko for logos and project data; both for market data |

Both are free to use, both need the contract's source code verified first, and both key everything by chain, so a token on six chains is six Etherscan-family submissions and, since Blockscout hosts no BNB Smart Chain explorer, up to five Blockscout ones — fewer where a CoinGecko listing already supplies the data. Neither documents token information carrying over from an implementation contract to the clones created from it.

## Verify the source first

Verification publishes source code that recompiles to the deployed bytecode. Both explorers refuse a token update for an unverified contract, and an unverified token contract reads as a warning sign to anyone who looks. [Registering on Etherscan](/wiki/economics/finance/defi/token-registration/etherscan#verify-the-source) has the Foundry command and the constructor-argument trap. Verification is per chain on both.

## What the badge does and does not say

A verified-source label means the published code compiles to the deployed bytecode. It says nothing about who deployed it or whether the code is safe, and an updated token page with a logo and links means only that somebody signed a message and filled in a form. Both are curation, not consensus, and [fake tokens](/wiki/economics/finance/fraud/fake-token) clear the first bar routinely — verifying a copied source contract is as easy as verifying an original.
