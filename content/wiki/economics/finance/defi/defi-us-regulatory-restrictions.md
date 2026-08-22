---
title: "DeFi and US Regulatory Restrictions"
weight: 60
---

The US regulatory environment for DeFi is fragmented across multiple agencies, each with overlapping and sometimes conflicting jurisdictions. This page is a snapshot as of early 2026 -- the landscape shifts frequently through enforcement actions, court rulings, and proposed legislation.

**This is not legal advice.** Anyone building or using DeFi protocols with US exposure should consult qualified legal counsel.

## Key regulatory bodies

### SEC (Securities and Exchange Commission)

The SEC regulates securities -- investment contracts, stocks, bonds, and instruments that the Howey Test classifies as securities. The SEC's position has been that many crypto tokens qualify as securities, particularly those sold in fundraising events where buyers expect profits from the efforts of others.

The SEC has brought enforcement actions against token issuers, [DEX](/wiki/economics/finance/defi/dex) operators, and lending platforms. The core question in each case is whether the token or service constitutes an unregistered securities offering.

### CFTC (Commodity Futures Trading Commission)

The CFTC regulates commodity futures and derivatives. It has classified Bitcoin and Ether as commodities, which gives it jurisdiction over derivatives, futures, and options based on those assets. DeFi protocols offering perpetual swaps, options, or futures to US users risk CFTC enforcement -- this is why platforms like dYdX, Polymarket, and others have historically geo-blocked US IP addresses.

### FinCEN (Financial Crimes Enforcement Network)

[FinCEN](/wiki/economics/finance/regulation/fincen) enforces [anti-money laundering](/wiki/economics/finance/regulation/anti-money-laundering) (AML) and [know-your-customer](/wiki/economics/finance/regulation/know-your-customer) (KYC) rules under the [Bank Secrecy Act](/wiki/economics/finance/regulation/bank-secrecy-act). Any entity that qualifies as a [money services business](/wiki/economics/finance/regulation/money-services-business) (MSB) must register with FinCEN, implement an AML program, and file suspicious activity reports. Whether a DeFi protocol's developers or [DAO](/wiki/economics/finance/defi/dao) constitute an MSB is an open legal question -- FinCEN has signaled that it considers some DeFi activities to fall within its purview. The [regulation](/wiki/economics/finance/regulation) section covers this side of the picture in detail.

## Major enforcement actions and precedents

- **SEC v. Ripple (2020--2023)** -- the SEC sued Ripple Labs for selling XRP as an unregistered security. The court ruled that programmatic sales on exchanges were not securities, but institutional sales were. The mixed outcome left the industry without clean precedent.
- **CFTC v. Ooki DAO (2022)** -- the CFTC brought an enforcement action against a DAO itself (not just its founders), arguing that DAO token holders who voted to continue offering leveraged trading to US users were collectively liable. The court agreed, establishing that decentralized governance does not shield participants from regulatory liability.
- **SEC v. LBRY (2022)** -- the court found that LBRY Credits (LBC) were securities when sold to fund development, even though they also had utility as a protocol token.
- **Tornado Cash sanctions (2022--2025)** -- [OFAC](/wiki/economics/finance/regulation/ofac-sanctions) sanctioned the Tornado Cash [smart contract](/wiki/economics/finance/defi/smart-contract) addresses, effectively banning US persons from interacting with the protocol. This was the first time sanctions were applied to a piece of software rather than an entity. In *Van Loon v. Treasury* (2024) the Fifth Circuit held that immutable contracts are not blockable "property" because nobody owns or controls them, and Treasury delisted the protocol in March 2025 -- a narrow win that left the criminal theories against developers intact.

## How restrictions affect DeFi users and builders

### For users

- **Geo-blocking** -- many DeFi protocols block US IP addresses or require attestation that the user is not a US person. This is enforced at the front-end level; the underlying [smart contracts](/wiki/economics/finance/defi/smart-contract) remain permissionless on-chain.
- **Tax reporting** -- US users must report crypto gains and losses. The Internal Revenue Service (IRS) treats cryptocurrency as property, and every swap, including token-to-token trades on a DEX, is a taxable event.
- **OFAC compliance** -- interacting with sanctioned addresses (knowingly or not) carries civil and potentially criminal liability. [Sanctions are strict-liability and bind every US person](/wiki/economics/finance/regulation/ofac-sanctions), not just regulated institutions.

### For builders

- **Token launches** -- distributing tokens to US persons risks SEC enforcement if the token is classified as a security. Many projects exclude US residents from airdrops and token sales.
- **Protocol design** -- features like admin keys, fee switches, and governance tokens can influence whether a protocol or its token is classified as a security. [Finalized smart contracts](/wiki/economics/finance/defi/finalized-smart-contract) with no admin controls reduce (but do not eliminate) regulatory surface area.
- **DAO liability** -- after Ooki DAO, participating in governance of a protocol that violates US regulations may expose individual token holders to liability.
- **Front-end liability** -- even if a smart contract is immutable and permissionless, operating a front-end that provides access to US users can create regulatory liability for the entity running that front-end.

## The path forward

Several legislative proposals have attempted to provide clarity -- the FIT21 Act, the Responsible Financial Innovation Act, and others -- but none had been enacted as of early 2026. The general direction of these proposals is to create a clearer division between the SEC and CFTC, establish a registration framework for digital assets, and provide safe harbors for sufficiently decentralized protocols.

Until legislation passes, the regulatory framework for DeFi in the US remains defined primarily by enforcement actions and court decisions, creating a patchwork of precedents rather than coherent rules.

## External links

- [CFTC Digital Assets page](https://www.cftc.gov/digitalassets) -- official CFTC guidance on digital asset regulation
- [SEC Crypto Assets page](https://www.sec.gov/securities-topics/crypto-assets) -- SEC enforcement actions and guidance related to crypto
- [DeFi Education Fund](https://www.defieducationfund.org/) -- advocacy organization focused on DeFi regulatory policy
- [FinCEN guidance on virtual currency](https://www.fincen.gov/resources/statutes-and-regulations) -- AML/KYC requirements for virtual currency businesses
