---
title: "Interbox"
weight: 90
---

Interbox is a fiat-to-crypto transfer service that lets users move funds from a U.S. bank account to a self-custodied [crypto](/wiki/economics/finance/defi/cryptocurrency) wallet without creating an account on an exchange or repeating [KYC](/wiki/economics/finance/regulation/know-your-customer) checks. It relies on the KYC already performed by the user's bank, and asks the user to prove only one thing directly: that they control the wallet the money is going to.

Parts of it are built and parts are not. The service that issues destination codes runs at `port.inter.box`; the settlement half — receiving the [Zelle](/wiki/economics/finance/payments/zelle) payment and delivering the stablecoin — has no execution partner and is not automated. This page marks which is which, because the difference matters to the regulatory argument at the end.

## The problem it solves

Buying crypto into a self-custodied wallet typically means signing up for an exchange, passing KYC (government ID, selfie, sometimes biometrics), waiting for verification, buying the asset, and then withdrawing to your wallet. Each exchange requires its own KYC, multiplying data exposure. Transaction holds of up to seven days are common.

Interbox shortcuts this by treating the bank's existing KYC as sufficient proof of identity. No ID upload, no redundant verification, no exchange account. Transfers settle in minutes rather than days.

## How it works

One flow, in four steps.

1. Connect a crypto wallet at `port.inter.box` and choose a network and a stablecoin.
2. Sign an [EIP](/wiki/economics/finance/defi/ethereum/)-712 typed-data message naming the destination account, network, currency, fee and terms. Interbox verifies the signature and derives a short content-addressed identifier from it — an **Inter Box Code**.
3. Send the money via [Zelle](/wiki/economics/finance/payments/zelle) — the US bank-to-bank instant payment network — to `usd@inter.box`, with the Box Code in the payment memo.
4. The stablecoin arrives at the signed destination, minus the fee.

The memo carries the routing, and because the destination lives inside a signed message rather than in the address string, **one alias serves every asset and network**. A code is specific to one combination of account, network and currency; changing any of them means signing a new one.

Earlier descriptions of Interbox — including a second, site-initiated flow in which the user receives a signed link by email or text and approves a payment request in their banking app — describe a design that was not built.

## Compatibility

**Banks:** any U.S. bank that supports Zelle, which is roughly two thousand institutions — see [how Zelle works](/wiki/economics/finance/payments/zelle/how-it-works).

**Assets:** USD stablecoins only. USDC on Arbitrum, Avalanche C-Chain, Base, Optimism and Polygon; DAI on Arbitrum, Avalanche and Optimism; USDI on the Bitsy network. No volatile assets and no USDT.

**Wallets:** MetaMask and other injected [Ethereum](/wiki/economics/finance/defi/ethereum/) wallets. WalletConnect appears in older Interbox material but is not implemented.

## Architecture

| Component | Role | Status |
|---|---|---|
| Static frontend | Wallet connection, network and currency selection, typed-data signing, code display | Built |
| Cloudflare Worker | Verifies the signature, derives the Box Code, stores the signed message in a key-value store | Built |
| Zelle inbound | Detecting the payment and matching its memo to a stored code | Not built |
| Crypto execution | A licensed execution partner delivers the stablecoin to the signed destination | Not built; no partner engaged |
| Limits and controls | Velocity caps, cooling periods, cumulative limits, idempotency | Not built |

Because the assets are dollar stablecoins, there is no exchange-rate exposure between the payment and the delivery, which removes a class of problem a volatile-asset onramp has to solve.

## Security and privacy

Interbox collects nothing at the front end: no name, no email address, no phone number, no identity document. The wallet signature is the only user input, and what the service stores is the signed message itself.

**There is no cryptographic link between a bank account and a wallet.** Earlier Interbox material described one, encrypted and held on-chain, as the mechanism that proved both ends belonged to the same person. It was not implemented. The signed message names a destination account, a network, a currency, a fee and a terms URL — no bank alias — so nothing binds a Box Code to whoever pays it. The service's own terms page acknowledges the consequence, warning users about scammers who share Box Codes. The control is designed rather than built, and the claim has been withdrawn until it is.

How long records are kept is currently inconsistent between the service's terms, which commit to retaining code and transaction records for [AML](/wiki/economics/finance/regulation/anti-money-laundering) purposes, and older descriptions promising deletion after settlement. The tension is not merely editorial: an [MSB](/wiki/economics/finance/regulation/money-services-business) owes five-year retention and suspicious-activity reporting, neither of which is compatible with deleting the record — so the retention answer follows from the regulatory position below rather than the other way round.

## Fees

A flat **3% service fee** per transaction, signed into every Box Code and displayed before the code is issued, plus any network fees charged by the execution partner.

## Regulatory position

Interbox facilitates transfers between accounts owned by the same person -- it does not transfer funds between separate parties. The argument that follows is that money transmission under the [Bank Secrecy Act](/wiki/economics/finance/regulation/bank-secrecy-act) means delivering value to *another person*, so a same-person transfer is not transmission, and Interbox therefore sits outside the [money services business](/wiki/economics/finance/regulation/money-services-business) obligations -- the [AML](/wiki/economics/finance/regulation/anti-money-laundering) program and the state licensing -- that apply to exchanges and other money transmitters.

That is an argument rather than a plain reading. The regulation says "to another **location or person**," and its explicit same-person carve-out covers only the physical transportation of currency, so whether the position holds turns on FinCEN administrative rulings and the specific facts.

It also depends on the architecture genuinely enforcing the same-person constraint — which, as the section above records, it does not. Anyone can pay anyone's Box Code. Until the account-to-wallet link is built, "same person at both ends" describes how the service is meant to be used rather than a property of its design, and an argument that rests on a usage convention is a considerably weaker one. It is an instance of the shape noted on the [Bank Secrecy Act](/wiki/economics/finance/regulation/bank-secrecy-act) page — the gap between what a technology can attest and what a regulation will accept — widened here by the attestation not yet existing.

## External links

- [Interbox](https://inter.box) — the destination domain; the current service runs at `port.inter.box`
- [Zelle](https://www.zellepay.com/)
