---
title: "Fake Tokens and Spoofed Contracts"
weight: 92
---

A token contract can claim any name and symbol it likes. In [ERC-20](/wiki/economics/finance/defi/ethereum/erc-20) those two fields are ordinary strings in contract storage, returned by ordinary view functions, with no registry behind them, no uniqueness constraint, and no authority that checks them against anything. Deploying a second contract that calls itself "USD Coin" with the symbol `USDC` costs a few dollars of gas and requires nobody's permission, and a [permissionless token factory](/wiki/economics/finance/defi/permissionless-token-factory) will produce one from a web form.

Impersonation at the asset level is not a bug in any particular wallet or exchange; it is what a namespace with no allocation authority produces by default, and every defence against it is a layer of curation bolted on afterwards by somebody other than the chain.

## What actually identifies a token

The contract address, and nothing else. Two deployments can be identical in every field a user sees.

```text
  contract at address A          contract at address B
    name()      "USD Coin"           name()      "USD Coin"
    symbol()    "USDC"               symbol()    "USDC"
    decimals()  6                    decimals()  6
    (display figures; the raw returns carry six more zeros)

  one of them is Circle's; the other was deployed this morning
```

The fields themselves are unremarkable, which is the trouble — nothing in the standard treats them as a claim to be validated. Illustratively, and omitting the transfer logic:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract Impostor {
    string public name = "USD Coin";
    string public symbol = "USDC";
    uint8 public decimals = 6;
    // transfer, approve, balanceOf: whatever the deployer wants them to do
}
```

Wallets and explorers paper over this with curated allowlists: a [token list](/wiki/economics/finance/defi/token-registration/token-lists) mapping a chain identifier and address to a display name and logo, a "verified" badge on an explorer page, a search index that ranks the real asset first. Those lists are maintained by companies — wallet vendors, explorer operators, data aggregators — and reflect their submission processes and staffing rather than any on-chain fact. The trust is real and it is entirely off-chain, which matters in the two places the curation has not reached: a chain or an interface that has no list, and an asset new enough that the list has not been updated. An explorer's "verified contract" label is a narrower claim still: it says the published source compiles to the deployed bytecode, not that the deployer is who they say they are.

## Where fakes get placed

**A pool for the fake pair.** Anyone can create a [liquidity pool](/wiki/economics/finance/defi/liquidity-pool) for any two tokens on a [decentralized exchange](/wiki/economics/finance/defi/dex); the router does not ask who deployed either side. The pool gives the imitation a price, a chart, and an entry in every aggregator that indexes pools rather than allowlists.

**Search inside wallets and aggregators.** A user typing a symbol into a swap interface gets a list of matches, and on a chain with weak curation the order of that list is the only thing distinguishing the real asset from six copies.

**Submissions to explorers and token lists.** Logos, social links, and project descriptions attached to a contract are supplied by [whoever submits them](/wiki/economics/finance/defi/token-registration) and are generally reviewed at submission speed rather than audited.

**"New listing" announcements.** The window between a genuine project announcing a token and the token existing is when imitations are most valuable, because there is no canonical address to compare against yet and buyers are primed to act quickly. This is the same tempo trick that makes a [giveaway scam](/wiki/economics/finance/fraud/giveaway-scam) work.

## Airdropped spam tokens

Unsolicited tokens arriving in a wallet are not gifts and usually are not even bait for a purchase. The token is deployed, distributed to thousands of addresses, and given a price by a pool the deployer created and controls, so the wallet's portfolio view — which multiplies balance by whatever price the aggregator found — displays a substantial fictitious sum. The user tries to sell it. Selling requires an interface, the token's own site is the one the search finds, and the transaction it asks for is not a swap: it is a token approval, or a signature granting spend rights over assets the user actually holds. From there it is ordinary [approval phishing](/wiki/economics/finance/fraud/approval-phishing) executed by a [wallet drainer](/wiki/economics/finance/fraud/wallet-drainer). The fake token is bait for a signature, not an asset, and its balance never needed to be sellable.

The same delivery mechanism serves [address poisoning](/wiki/economics/finance/fraud/address-poisoning): a zero-value or dust transfer from a contract the attacker controls writes a lookalike address into the victim's transaction history, where it waits to be copied out of the recent-activity list. In May 2024 a trader sent 1,155 wrapped bitcoin, roughly $68 million at the time, to an address of that kind; the funds were returned some days later after the attacker was traced, which is not the usual ending.

## Spoofed contract source

Verification on an explorer establishes that source matches bytecode. It does not establish that the source does what it appears to do at runtime. A contract can read clean and still delegate its transfer path to another contract the deployer owns, or take a fee rate, a pause flag, or a blocklist from a separate address that can be rewritten later. A proxy is the cleanest version: the implementation the reader inspected can be replaced after verification, and the address the user interacts with never changes. [Hidden admin controls](/wiki/economics/finance/fraud/hidden-admin-controls) covers the full pattern. A verified badge and a matching name are both compatible with a contract whose behaviour is set from an address the reader never looked at.

## Spoofed collections

The same imitation works on [NFTs](/wiki/economics/finance/defi/nft), and more cheaply, because there is no liquidity to seed. A duplicate [ERC-721](/wiki/economics/finance/defi/ethereum/erc-721) contract can point its metadata at the original's files, so the images, traits, and descriptions resolve identically and the marketplace listing is visually indistinguishable from the real collection. Only the contract address differs. OpenSea said in January 2022 that more than 80% of the items created with its free minting tool were plagiarized works, fake collections, or spam — a marketplace-scale measurement of what costless issuance produces.

## Checking an address before you send funds

1. **Take the address from the project's own documentation or issuer site**, not from a search result, a social post, or a message. This catches the entire class of fakes that live in search and chat, and it misses a compromised documentation site — so confirm the domain itself, not just the page.
2. **Compare it against the explorer's verified-contract entry and at least one independent source** — the project's repository, the wallet's built-in token list, a second explorer. Agreement across sources that do not copy each other catches imitations that were never submitted anywhere. It does not tell you the deployer's identity.
3. **Look at pool depth and holder count.** A day-old contract with a $40,000 pool and 60 holders is not the asset with a billion-dollar float. Both numbers can be manufactured, cheaply in the case of holders and expensively in the case of depth, so treat this as a filter for lazy fakes rather than proof — [wash trading](/wiki/economics/finance/fraud/wash-trading) produces convincing volume charts for a small budget.
4. **Read the deployer and the first transactions.** A real launch has a funding history, a deployment months or years before the current interest, and a distribution consistent with its story. A fake generally has a deployer funded shortly beforehand, a mint concentrated in a few addresses, and a contract age measured in hours. A patient attacker defeats this one.

None of these establish that a token whose address you have verified is a good investment; they establish only that it is the token you meant to buy. A correctly identified contract can still be a [honeypot](/wiki/economics/finance/fraud/honeypot-token) or a [rug pull](/wiki/economics/finance/fraud/rug-pull).

## Where the law lands

No statute prohibits deploying a contract that returns a particular string. Prosecutions treat the imitation as evidence of intent within an ordinary wire fraud case, and rights holders occasionally bring trademark claims, which are effective against a marketplace with a takedown process and useless against a contract. Where the fake is marketed as an investment, the securities and commodities [regulators](/wiki/economics/finance/regulation) have jurisdiction over the offering rather than over the deployment. The practical consequence is that identification is the user's job, and the tooling that assists it is commercial.

## External links

- [The ERC-20 standard](https://eips.ethereum.org/EIPS/eip-20) — where `name` and `symbol` are specified as optional metadata with no uniqueness requirement
- [Token Lists](https://tokenlists.org/) — the community standard behind wallet allowlists, and a good look at who maintains them
- [Etherscan token approval checker](https://etherscan.io/tokenapprovalchecker) — lists and revokes the approvals a spam-token interaction may have granted
- [Circle developer documentation](https://developers.circle.com/) — an example of an issuer publishing its own canonical contract addresses, which is where such an address should come from
- [Chainalysis blog](https://www.chainalysis.com/blog/) — periodic measurement of token-impersonation and approval-phishing losses
