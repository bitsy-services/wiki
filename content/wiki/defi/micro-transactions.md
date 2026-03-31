---
title: Micro-Transactions
weight: 63
---

A **micro-transaction** is a payment small enough that traditional payment infrastructure cannot process it economically -- typically fractions of a cent to a few cents. On [blockchains](/wiki/defi/blockchain) like [Ethereum](/wiki/defi/ethereum/), transaction fees often exceed the value being transferred, making naive on-chain micro-transactions impractical. Solving this problem is one of the key challenges for pay-per-use business models, streaming payments, and machine-to-machine commerce.

## Why Micro-Transactions Matter

Many useful payment patterns only work when individual transfers can be vanishingly small:

- **Streaming payments** -- paying for media, compute, or bandwidth by the second rather than by subscription.
- **Pay-per-use APIs** -- charging per request instead of requiring upfront commitments.
- **IoT and machine-to-machine payments** -- autonomous devices settling resource consumption in real time.
- **Content monetization** -- paying fractions of a cent per page view or article read, replacing advertising as a revenue model.

These patterns require transaction costs to be negligible relative to the payment amount. When a single [Ethereum](/wiki/defi/ethereum/) mainnet transaction costs several dollars in gas, sending $0.001 directly on-chain makes no economic sense.

## The Gas Cost Problem

Every transaction on a [blockchain](/wiki/defi/blockchain) competes for block space and must pay a fee to validators. On Ethereum mainnet, even a simple [ERC-20](/wiki/defi/ethereum/erc-20) transfer costs tens of thousands of gas units. During periods of high demand, this translates to fees that dwarf micro-transaction values by orders of magnitude.

The problem is not unique to Ethereum -- any chain with meaningful decentralization faces a version of this tradeoff between security and per-transaction cost.

## Approaches to Viable Micro-Transactions

### Layer 2 Rollups

Rollups (optimistic and zero-knowledge) batch many transactions into a single proof or data submission on the base layer. This amortizes the cost of L1 security across hundreds or thousands of individual transfers, reducing per-transaction fees to fractions of a cent. Rollups inherit the security guarantees of the underlying [blockchain](/wiki/defi/blockchain) while making micro-transactions economically viable.

### State Channels

State channels allow two parties to transact off-chain an arbitrary number of times, only settling the net result on-chain. The classic example is a payment channel: two participants lock funds in a [smart contract](/wiki/defi/smart-contract), exchange signed balance updates off-chain, and close the channel with a single on-chain transaction. This model is well-suited to high-frequency, low-value transfers between known counterparties -- such as streaming payments for a service.

The Lightning Network on Bitcoin and Raiden on Ethereum are prominent payment-channel implementations.

### Application-Specific Approaches

Some protocols sidestep the problem by aggregating micro-transactions at the application layer. A service might track usage off-chain and settle periodically -- say, once a day or when a balance threshold is reached. This trades immediacy for cost efficiency and introduces a degree of trust, but it can be a pragmatic choice when the parties have an ongoing relationship.

## Tradeoffs

No solution eliminates all friction. Rollups add finality delays and depend on the health of a sequencer. State channels require both parties to be online (or delegate to a watchtower) and are poorly suited to one-off payments with strangers. Application-layer aggregation reintroduces custodial risk. The right approach depends on the use case -- a streaming music service has different requirements than an IoT sensor mesh.
