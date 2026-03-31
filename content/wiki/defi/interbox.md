---
title: "Interbox"
weight: 90
---

Interbox is a proposed fiat-to-crypto transfer service that lets users move funds from a U.S. bank account to a self-custodied [crypto](/wiki/defi/cryptocurrency) wallet without creating an account on an exchange or repeating KYC checks. It relies on the KYC already performed by the user's bank, cryptographically linking the bank account to the wallet so that Interbox can verify ownership without collecting sensitive identity documents.

## The problem it solves

Buying crypto into a self-custodied wallet typically means signing up for an exchange, passing KYC (government ID, selfie, sometimes biometrics), waiting for verification, buying the asset, and then withdrawing to your wallet. Each exchange requires its own KYC, multiplying data exposure. Transaction holds of up to seven days are common.

Interbox shortcuts this by treating the bank's existing KYC as sufficient proof of identity. The user's bank account and crypto wallet are linked cryptographically -- no ID upload, no redundant verification. Transfers settle in minutes rather than days.

## How it works

There are two flows, depending on where the user initiates the transfer.

### Interbox-initiated

1. Visit [test.inter.box](https://test.inter.box) and specify the [cryptocurrency](/wiki/defi/cryptocurrency), network, USD amount, and the alias (email or phone) tied to your bank account.
2. Connect your crypto wallet.
3. Confirm the transfer.
4. Open the digitally signed link sent to your bank alias and review the details.
5. Approve the payment request in your banking app.

Funds arrive in the wallet within minutes, depending on network settlement.

### Zelle-initiated

1. Send funds via Zelle to an Interbox alias that encodes the currency and network -- e.g. `eth.ethereum@inter.box`, `usdc.polygon@inter.box`, `usdt.tron@inter.box`.
2. Open the link Interbox sends to your bank alias.
3. Connect your wallet and confirm.

Funds arrive within seconds for fast-settlement networks.

## Compatibility

**Banks:** Any U.S. bank that supports Zelle.

**Wallets:** MetaMask and any [Ethereum](/wiki/defi/ethereum/)-compatible wallet via WalletConnect (Trust Wallet, Rainbow, Argent, Safe, etc.).

## Architecture

| Component | Role |
|---|---|
| dApp frontend | User specifies currency, network, amount, alias; connects wallet and signs |
| dApp backend | Orchestrates communication with banks, crypto providers, and messaging APIs |
| Banking services | Zelle-compatible banks; Interbox queries for incoming payments via API |
| Crypto providers | Partners (e.g. Coinbase) handle exchange, deliver crypto to the user's wallet |
| Messaging | Twilio (SMS/RCS) and email for transaction confirmations and signed links |

Idempotency keys prevent duplicate processing. If the exchange rate shifts significantly during a transaction, the user may be offered the option to reject it.

## Security and privacy

Interbox minimises data collection. It does not store personal or transactional data beyond communication records needed for troubleshooting. Off-chain data required to complete a transfer is deleted after settlement.

The link between a bank account and a wallet is encrypted on-chain. Interbox will only disclose account linkage under a properly executed court order.

## Fees

A flat **1% service fee** per transaction, plus any network fees charged by the crypto provider. All fees are shown before the user confirms.

## Regulatory position

Interbox facilitates transfers between accounts owned by the same person -- it does not transfer funds between separate parties. This structure means it is not classified as a money transmitter and is exempt from the AML/KYC licensing requirements that apply to exchanges and payment processors.

## External links

- [Interbox](https://inter.box)
- [Zelle](https://www.zellepay.com/)
- [WalletConnect](https://walletconnect.com/)
