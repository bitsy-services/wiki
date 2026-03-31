---
title: "Cryptocurrency Gateway"
weight: 3
---

A cryptocurrency gateway is a service that converts between fiat [currency](/wiki/defi/currency) and [cryptocurrency](/wiki/defi/cryptocurrency) -- commonly called an on-ramp (fiat to crypto) or off-ramp (crypto to fiat). These gateways are the entry and exit points between the traditional financial system and the [blockchain](/wiki/defi/blockchain) economy.

## Centralized gateways

Most on/off-ramp activity today flows through centralized services that hold the necessary banking relationships and regulatory licenses.

### Exchanges

Centralized exchanges (Coinbase, Kraken, Binance) are the most common gateway. Users deposit fiat via bank transfer, wire, or card, buy crypto, and withdraw it to a self-custodial wallet. The reverse path -- deposit crypto, sell for fiat, withdraw to a bank -- serves as the off-ramp.

Exchanges typically require full identity verification (KYC) and are subject to the regulatory framework of each jurisdiction they operate in. In the US, this means registration as a Money Services Business with FinCEN and compliance with state money-transmitter laws.

### Payment processors

Services like MoonPay, Transak, and Ramp Network embed fiat-to-crypto conversion directly into [dApps](/wiki/defi/dapp) and wallets. A user clicks "buy crypto," enters a card number, and receives tokens in their wallet without leaving the application. These processors handle the KYC, banking, and compliance on behalf of the integrating application.

### Bitcoin ATMs and OTC desks

Bitcoin ATMs provide physical on-ramps, typically at higher fees. Over-the-counter (OTC) desks serve institutional or high-volume traders who need to move large amounts without impacting market prices.

## Decentralized and peer-to-peer approaches

Decentralized gateways attempt to remove the trusted intermediary from fiat-crypto conversion, though they face fundamental challenges -- fiat settlement is inherently centralized (banks, payment rails) even if the crypto side is not.

- **Peer-to-peer marketplaces** (Bisq, Paxful, LocalBitcoins) connect buyers and sellers directly. Escrow is handled by a [smart contract](/wiki/defi/smart-contract) or multisig on the crypto side, while the fiat leg relies on direct bank transfers between parties. Dispute resolution varies from reputation systems to human arbitrators.
- **Stablecoin bridging** -- rather than converting fiat directly, users acquire stablecoins (USDC, USDT) through a centralized gateway once and then operate entirely on-chain. This reduces the frequency of fiat touchpoints.

## Regulatory considerations

Gateways sit at the boundary between regulated finance and the permissionless crypto ecosystem, which makes them a focal point for regulators.

- **KYC/AML requirements** -- virtually all fiat-touching services must verify customer identity and report suspicious activity. This is mandated by FinCEN in the US, the FCA in the UK, and equivalent bodies elsewhere.
- **Money transmitter licensing** -- operating a gateway in the US requires state-by-state money transmitter licenses (or a federal charter), a costly and time-consuming process.
- **Geographic restrictions** -- many gateways restrict service in jurisdictions with unclear or hostile regulatory environments. See [DeFi US regulatory restrictions](/wiki/defi/defi-us-regulatory-restrictions) for the US-specific landscape.

The regulatory burden on gateways is one reason the [DeFi](/wiki/defi/dex) ecosystem favors stablecoin-denominated trading -- once a user is on-chain, they can interact with protocols without further fiat conversion.

## External links

- [FinCEN Money Services Business registration](https://www.fincen.gov/money-services-business-definition) -- US regulatory requirements for money services businesses
- [MoonPay documentation](https://www.moonpay.com/en-gb/business) -- example of an embedded fiat-to-crypto payment processor
- [Bisq network](https://bisq.network/) -- decentralized peer-to-peer exchange
