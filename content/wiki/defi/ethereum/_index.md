---
title: "Ethereum"
weight: 1
bookCollapseSection: true
---

Ethereum is a programmable [blockchain](/wiki/defi/blockchain) -- a decentralized computing platform where anyone can deploy [smart contracts](/wiki/defi/smart-contract) and build applications that run without centralized control. Launched in 2015, it was created by Vitalik Buterin and a team of co-founders to extend blockchain beyond simple value transfer. Where Bitcoin is digital money, Ethereum is a digital machine that can execute arbitrary logic.

Ethereum's native [cryptocurrency](/wiki/defi/cryptocurrency) is Ether (ETH). It serves two purposes: it is the unit of account for the network, and it pays for computation (transaction fees, called "gas").

## The Ethereum Virtual Machine (EVM)

The EVM is the runtime environment for smart contracts on Ethereum. Every node in the network runs the same EVM, executing the same bytecode and arriving at the same result -- this is how decentralized consensus works for computation, not just transactions.

Smart contracts are typically written in [Solidity](/wiki/defi/solidity/) and compiled to EVM bytecode. The EVM model has been so widely adopted that many other blockchains (Polygon, Arbitrum, Avalanche, BNB Chain) are "EVM-compatible," meaning they run the same bytecode and support the same tooling.

## Consensus: From Proof of Work to Proof of Stake

Ethereum originally used Proof of Work (PoW), the same consensus mechanism as Bitcoin. In September 2022, a long-planned upgrade called The Merge switched Ethereum to Proof of Stake (PoS), reducing energy consumption by roughly 99.95%.

Under PoS, validators lock up ETH as collateral ([staking](/wiki/defi/staking)) and are selected to propose and attest to new blocks. Validators who act honestly earn rewards; those who misbehave have their stake "slashed" (partially confiscated). This economic incentive structure secures the network without the energy cost of mining.

## Token Standards

Ethereum's token standards define how digital assets behave on the network. The major ones:

- **[ERC-20](/wiki/defi/ethereum/erc-20)** -- The standard for fungible tokens. Nearly every DeFi token (USDC, DAI, UNI, LINK) is an ERC-20. It defines a common interface for transfer, approval, and balance queries.
- **ERC-721** -- The standard for non-fungible tokens (NFTs). Each token has a unique ID and represents ownership of a distinct item.
- **ERC-1155** -- A multi-token standard that supports both fungible and non-fungible tokens in a single contract, reducing deployment costs.
- **[ERC-8004](/wiki/defi/ethereum/erc-8004)** -- A newer standard relevant to the Bitsy ecosystem.

These standards matter because they enable composability -- any application that understands ERC-20 can work with any ERC-20 token, which is why [DEXs](/wiki/defi/dex), [liquidity pools](/wiki/defi/liquidity-pool), and lending protocols can all interoperate.

## Ethereum and DeFi

Ethereum is the primary platform for decentralized finance. The major categories of DeFi applications on Ethereum include:

- **[Decentralized exchanges](/wiki/defi/dex)** -- [AMMs](/wiki/defi/amm) like [Uniswap](/wiki/defi/uniswap) that use [liquidity pools](/wiki/defi/liquidity-pool) and the [constant product formula](/wiki/defi/constant-product-formula) instead of order books
- **Lending and borrowing** -- Protocols like Aave and Compound that let users earn interest on deposits or take collateralized loans
- **Stablecoins** -- Tokens pegged to a fiat currency, most prominently USDC and DAI
- **[DAOs](/wiki/defi/dao)** -- On-chain governance organizations managing protocol treasuries and parameters
- **[Yield farming](/wiki/defi/yield-farming)** -- Strategies for maximizing returns across multiple DeFi protocols
- **[Oracles](/wiki/defi/oracle-node)** -- Services like Chainlink that bring off-chain data on-chain, enabling smart contracts to react to real-world events

The composability of Ethereum's smart contracts means these protocols can be layered on top of each other -- a property often called "money legos."

## Scalability and Layer 2

Ethereum's base layer processes roughly 15-30 transactions per second, which is insufficient for mass adoption. During high-demand periods, gas fees spike to levels that price out smaller users.

The scaling roadmap centers on Layer 2 (L2) solutions -- separate chains that process transactions off the main chain and post compressed proofs back to Ethereum for security:

- **Optimistic rollups** (Optimism, Arbitrum) -- Assume transactions are valid and only run fraud proofs if challenged
- **ZK-rollups** (zkSync, StarkNet) -- Use zero-knowledge proofs to cryptographically verify transaction batches

L2s reduce fees by orders of magnitude while inheriting Ethereum's security guarantees. Most new DeFi deployment activity has shifted to L2s.

A future upgrade called **danksharding** will further increase the data throughput available to rollups, aiming to make L2 transactions even cheaper.

## Ethereum vs. Bitcoin

Both are blockchains, but they serve different purposes. Bitcoin is optimized for a single use case: decentralized, censorship-resistant money. Its scripting language is intentionally limited. Ethereum sacrifices some of that simplicity for general-purpose programmability -- it can do anything Bitcoin does, but it can also run arbitrarily complex applications. The tradeoff is a larger attack surface and more complexity in the protocol.

## Wiki Pages

{{< section >}}
