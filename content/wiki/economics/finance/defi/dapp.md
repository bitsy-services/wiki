---
title: "Decentralized Application"
weight: 7
---

A decentralized application (dApp) is software that runs its core logic on a [blockchain](/wiki/economics/finance/defi/blockchain) through [smart contracts](/wiki/economics/finance/defi/smart-contract) rather than on servers controlled by a single operator. The frontend can be a normal website or mobile app, but the backend -- the part that holds funds, enforces rules, and records state -- lives on-chain and executes exactly as written.

The term covers a huge range: [DEXs](/wiki/economics/finance/defi/dex) like [Uniswap](/wiki/economics/finance/defi/uniswap), lending protocols, [prediction markets](/wiki/economics/finance/defi/prediction-market), games, [DAOs](/wiki/economics/finance/defi/dao), and more. What they share is that users interact with contracts directly from their own wallet, and no one can unilaterally change the rules once the contracts are deployed.

## Architecture

A dApp has two layers:

- **Frontend.** A conventional web or mobile interface. It reads chain state through an RPC provider and submits transactions on the user's behalf. Some projects host their frontend on [IPFS](/wiki/cs/ipfs) or [Arweave](/wiki/economics/finance/defi/arweave) so it cannot be taken down, but most still use traditional hosting.
- **Backend (smart contracts).** One or more contracts deployed to a blockchain like [Ethereum](/wiki/economics/finance/defi/ethereum/). These handle all state that needs to be trustless -- token balances, pool reserves, governance votes. Once deployed, the code is immutable unless the contract is explicitly upgradeable.

The wallet (MetaMask, Rabby, a hardware signer) bridges the two layers. It holds the user's private key, signs transactions locally, and sends them to the network.

## How a swap works on Uniswap

1. The user opens the Uniswap web app and connects their wallet.
2. They select an [ERC-20](/wiki/economics/finance/defi/ethereum/erc-20) token pair and enter an amount.
3. The frontend calls the router contract's `swap` function, encoding the parameters into a transaction.
4. The wallet prompts the user to sign. Once signed, the transaction goes to the [Ethereum](/wiki/economics/finance/defi/ethereum/) network.
5. Uniswap's smart contracts pull tokens from the user's wallet, route through one or more [liquidity pools](/wiki/economics/finance/defi/liquidity-pool), and send the output tokens back -- all atomically in a single transaction.

No intermediary custodies the funds at any point.

## Categories

| Category | What it does | Examples |
|---|---|---|
| DeFi | Lending, trading, [yield farming](/wiki/economics/finance/defi/yield-farming) | Uniswap, Aave, Compound |
| Governance | On-chain voting and treasury management | [DAOs](/wiki/economics/finance/defi/dao), Gnosis Safe |
| Gaming / [NFTs](/wiki/economics/finance/defi/nft) | Ownership of in-game assets | Axie Infinity, OpenSea |
| Storage | Decentralized file hosting | Filecoin, Arweave |

## Trade-offs

**Censorship resistance.** Because the contracts live on a public blockchain, no single entity can shut them down. Even if a frontend is taken offline, anyone can interact with the contracts directly or deploy an alternative frontend.

**Transparency.** Contract code and all transactions are publicly auditable. A pool's reserves, a protocol's fee parameters, and every trade that moved them can be read off the chain directly rather than taken from a disclosure the operator chose to publish.

**Scalability.** Blockchains have limited throughput. On Ethereum mainnet, gas costs spike during congestion. Layer-2 rollups (Optimism, Arbitrum, Base) improve this by batching transactions off-chain and posting proofs on-chain, with the batched transaction data going into [blobs](/wiki/economics/finance/defi/ethereum/blobs).

**User experience.** Users must manage wallets, approve token spending, pay gas fees, and understand transaction finality. Account abstraction and embedded wallets remove several of those steps, at the cost of reintroducing a party — a key-share custodian, a bundler, a paymaster — that can be compelled or can simply go down.

**Smart contract risk.** Bugs in contracts can lead to permanent loss of funds. There is no customer support to reverse a transaction. Audits and formal verification reduce but do not eliminate this risk.

## External links

- [Ethereum.org -- Introduction to dApps](https://ethereum.org/en/dapps/)
- [EIP process for new standards](https://eips.ethereum.org/)
