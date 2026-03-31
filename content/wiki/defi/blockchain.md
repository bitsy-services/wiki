---
title: "Blockchain"
weight: 1
---

A blockchain is a distributed ledger made up of blocks -- records containing a cryptographic hash of the previous block, a timestamp, and transaction data (typically structured as a Merkle tree). Because each block references the one before it, altering any historical record would require recomputing every subsequent block, making the ledger effectively immutable once written.

This property -- append-only, tamper-evident history shared across many nodes -- is what makes blockchains useful as trust infrastructure. No single party controls the ledger, and no single party needs to be trusted.

## How It Works

Every participant in a blockchain network holds a copy of the ledger. When new transactions occur, they are broadcast to the network, validated by participants, and assembled into a new block. Once the network reaches consensus that the block is valid, it is appended to the chain and propagated to all nodes.

The consensus mechanism determines how agreement is reached. The two dominant approaches are:

- **Proof of Work (PoW)**: Miners compete to solve a computationally expensive puzzle. The winner proposes the next block and earns a reward. Bitcoin uses PoW. It is secure but energy-intensive.
- **Proof of Stake (PoS)**: Validators lock up [cryptocurrency](/wiki/defi/cryptocurrency) as collateral ("staking") and are selected to propose blocks proportionally to their stake. [Ethereum](/wiki/defi/ethereum/) uses PoS since its 2022 Merge upgrade. It consumes far less energy than PoW.

## Permissioned vs. Permissionless

Permissionless blockchains (Bitcoin, Ethereum) are open networks -- anyone can join, validate transactions, and read the full history without approval from a central authority. This openness is what enables [decentralized applications](/wiki/defi/web3) and [DeFi](/wiki/defi/dex) to function without gatekeepers.

Permissioned blockchains (Hyperledger Fabric, R3 Corda) restrict who can participate. They trade openness for performance and privacy, and are used mostly in enterprise settings. They share the data structure of blockchains but not the trust model.

## Smart Contracts

[Smart contracts](/wiki/defi/smart-contract) are programs stored on a blockchain that execute automatically when predefined conditions are met. They enable agreements to be enforced without intermediaries -- the blockchain itself acts as the execution environment and the arbiter.

Ethereum popularized smart contracts and remains the dominant platform for them. Smart contracts are the foundation of [decentralized exchanges](/wiki/defi/dex), [liquidity pools](/wiki/defi/liquidity-pool), [DAOs](/wiki/defi/dao), and most of what falls under DeFi.

## Decentralized Domain Names

Blockchains can serve as the backend for censorship-resistant naming systems. Namecoin introduced the `.bit` TLD, and Ethereum's [ENS](https://ens.domains) manages `.eth` names. These systems replace traditional DNS with on-chain records that no registrar can unilaterally revoke.

## Other Applications

Beyond finance and naming, blockchains have been applied to:

- **Supply chain tracking** -- transparent provenance records that resist tampering
- **Content distribution** -- creator-controlled distribution and royalty enforcement
- **Energy trading** -- peer-to-peer energy markets without a central utility
- **Identity** -- self-sovereign identity systems where users control their own credentials

The breadth of these applications varies widely in maturity. Financial use cases (cryptocurrency, DeFi) are the most developed; others remain largely experimental.

## Environmental Impact

PoW mining consumes substantial electricity -- Bitcoin's network rivals the energy usage of some small countries. This has driven significant criticism and motivated the shift toward PoS. Ethereum's transition to PoS in September 2022 reduced its energy consumption by roughly 99.95%. New blockchain projects overwhelmingly choose PoS or other low-energy consensus mechanisms.

## External Links

- [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf) -- Satoshi Nakamoto's original 2008 paper
- [Wikipedia: Blockchain](https://en.wikipedia.org/wiki/Blockchain)
- [Ethereum Name Service (ENS)](https://ens.domains)
