---
title: "Payment Trail"
weight: 60
---

A payment links two [operational personas](/wiki/security/operational-persona), the sets of accounts and credentials one person runs as separate identities, when one card, bank account or funding address pays for both. Money is where a persona meets legal identity: a bank has verified its customer under [know your customer](/wiki/economics/regulation/know-your-customer) rules, a processor stores the instrument, and a public ledger shows every transfer to anyone who looks.

## Cards and bank accounts

A card on file is a stable value at each merchant, and a billing address comes with it. Those details also travel: when the journalist [Mat Honan's accounts were taken in 2012](/wiki/security/operational-persona/recovery-graph#what-counts-as-an-edge), the last four digits one company displayed were what another accepted as proof of identity.

Receiving money exposes the holder as well. Before a Zelle payment is confirmed, the sender's bank shows [the registered first name and last initial](/wiki/economics/payments/zelle/alias#misdirection-by-typo) behind the phone number or address it was sent to.

Configuration cannot remove any of this from a bank's file. A persona with income either accepts that its bank knows its operator, the person running it, and prevents only public disclosure, or it handles no money. A registered company gives a persona a lawful name to invoice under, and the bank still [identifies the people who own it](/wiki/economics/regulation/know-your-customer).

## Public ledgers

On a public [blockchain](/wiki/economics/defi/blockchain) the payment is itself the published record. Meiklejohn and colleagues clustered Bitcoin addresses in 2013 with two rules, the first being "If two (or more) addresses are inputs to the same transaction, they are controlled by the same user". In a 2020 paper Victor applied three patterns to the first four years of [Ethereum](/wiki/economics/defi/chains/ethereum): exchange deposit addresses, airdrops (tokens given out to many addresses) and token authorizations ([approvals](/wiki/economics/fraud/approval-phishing) for another address to spend). The patterns clustered 17.9% of all active externally owned account addresses, the kind controlled by a private key. Deposit addresses were the most effective: addresses that pay into one exchange deposit address sit in one cluster.

A new Ethereum address holds no ether and usually needs some to pay for gas, the network's transaction fee, so its first incoming transfer points at whoever funded it, in plain view on a [block explorer](/wiki/economics/defi/token-registration/block-explorers). Withdrawing from an exchange ties that public record to the exchange's identity file.

## Many fronts, one source

The 2018 US indictment of twelve officers of Russian military intelligence (GRU), over the hacking and release of documents during the 2016 US election, describes an operation separated with care at the front and joined at the back. It alleges "hundreds of different email accounts, in some cases using a new account for each purchase", fictitious names, and two fictitious personas, DCLeaks and Guccifer 2.0, used to release the documents.

The indictment's summary is that the two ran on "overlapping computer infrastructure and financing". One dedicated email account "received hundreds of bitcoin payment requests from approximately 100 different email accounts". The same funding structure, "in some cases, the very same pool of funds", paid for "key accounts, servers, and domains". Funds in one bitcoin address bought a VPN account, a virtual private network login later used for the `@Guccifer_2` Twitter account, and the remainder leased the server that hosted the DCLeaks site. These are a grand jury's allegations.

The shape is a star, with many disposable identities in front and one source behind.

## Check

Read the `paid-by:` line of each [inventory](/wiki/security/operational-persona/cohesion#one-inventory-per-persona) entry, comparing inventories without saving the result. An instrument listed under two personas links them. For an address on a public chain, open its first incoming transaction on a block explorer: the sender is the funder anyone can see.

## Further reading

- Meiklejohn et al., [A Fistful of Bitcoins: Characterizing Payments Among Men with No Names](https://cseweb.ucsd.edu/~smeiklejohn/files/imc13.pdf), IMC 2013
- Victor, [Address clustering heuristics for Ethereum](https://fc20.ifca.ai/preproceedings/31.pdf), Financial Cryptography 2020
- [Indictment, *United States v. Netyksho*](https://www.justice.gov/usdoj-media/sco-durham/media/1126686/dl?inline=), No. 1:18-cr-00215 (D.D.C. 2018), paragraphs 45 and 57 to 64
