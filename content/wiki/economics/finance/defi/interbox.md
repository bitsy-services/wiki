---
title: "Interbox"
weight: 90
---

Interbox is a proposed fiat-to-crypto transfer service that lets users move funds from a U.S. bank account to a self-custodied [crypto](/wiki/economics/finance/defi/cryptocurrency) wallet without creating an account on an exchange or repeating [KYC](/wiki/economics/finance/regulation/know-your-customer) checks. It relies on the KYC already performed by the user's bank, cryptographically linking the bank account to the wallet so that Interbox can verify ownership without collecting sensitive identity documents.

## The problem it solves

Buying crypto into a self-custodied wallet typically means signing up for an exchange, passing KYC (government ID, selfie, sometimes biometrics), waiting for verification, buying the asset, and then withdrawing to your wallet. Each exchange requires its own KYC, multiplying data exposure. Transaction holds of up to seven days are common.

Interbox shortcuts this by treating the bank's existing KYC as sufficient proof of identity. The user's bank account and crypto wallet are linked cryptographically -- no ID upload, no redundant verification. Transfers settle in minutes rather than days.

## How it works

There are two flows, depending on where the user initiates the transfer.

### Interbox-initiated

1. Visit [test.inter.box](https://test.inter.box) and specify the cryptocurrency, network, USD amount, and the alias (email or phone) tied to your bank account.
2. Connect your crypto wallet.
3. Confirm the transfer.
4. Open the digitally signed link sent to your bank alias and review the details.
5. Approve the payment request in your banking app.

Funds arrive in the wallet within minutes, depending on network settlement.

### Zelle-initiated

1. Send funds via Zelle -- the US bank-to-bank instant payment network -- to an Interbox alias that encodes the currency and network -- e.g. `eth.ethereum@inter.box`, `usdc.polygon@inter.box`, `usdt.tron@inter.box`.
2. Open the link Interbox sends to your bank alias.
3. Connect your wallet and confirm.

Funds arrive within seconds for fast-settlement networks.

## Compatibility

**Banks:** Any U.S. bank that supports Zelle.

**Wallets:** MetaMask and any [Ethereum](/wiki/economics/finance/defi/ethereum/)-compatible wallet via WalletConnect (Trust Wallet, Rainbow, Argent, Safe, etc.).

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

Interbox minimises data collection. It does not store personal or transactional data beyond communication records needed for troubleshooting. Off-chain data required to complete a transfer is deleted after settlement. Note that this is only tenable on the regulatory position described below: an MSB owes five-year retention and suspicious-activity reporting, neither of which is compatible with deleting the record.

The link between a bank account and a wallet is encrypted on-chain. Interbox will only disclose account linkage under a properly executed court order.

## Fees

A flat **1% service fee** per transaction, plus any network fees charged by the crypto provider. All fees are shown before the user confirms.

## Regulatory position

Interbox facilitates transfers between accounts owned by the same person -- it does not transfer funds between separate parties. The argument that follows is that money transmission under the [Bank Secrecy Act](/wiki/economics/finance/regulation/bank-secrecy-act) means delivering value to *another person*, so a same-person transfer is not transmission, and Interbox therefore sits outside the [money services business](/wiki/economics/finance/regulation/money-services-business) obligations -- the [AML](/wiki/economics/finance/regulation/anti-money-laundering) program and the state licensing -- that apply to exchanges and other money transmitters.

That is an argument rather than a plain reading. The regulation says "to another **location or person**," and its explicit same-person carve-out covers only the physical transportation of currency, so whether the position holds turns on FinCEN administrative rulings and the specific facts. It also depends on the architecture genuinely enforcing the same-person constraint, which is why the cryptographic account-to-wallet link is load-bearing rather than a convenience.

## External links

- [Interbox](https://inter.box)
- [Zelle](https://www.zellepay.com/)
- [WalletConnect](https://walletconnect.com/)
