---
title: "Decentralized Exchange"
weight: 5
---

A decentralized exchange (DEX) is a marketplace for trading tokens that runs on-chain, without a central operator holding custody of user funds. Trades settle directly between the user's wallet and a smart contract.

On a centralized exchange (CEX) like Coinbase or Binance, you deposit funds into the exchange's custody, place orders against an order book the exchange operates, and trust the exchange to process withdrawals. A DEX replaces all of that with smart contracts: your tokens never leave your wallet until the moment the trade executes on-chain. There is no account to create, no KYC gate, and no withdrawal queue.

## DEX architectures

Three main designs have emerged, each with different trade-offs around latency, gas cost, and liquidity depth.

### AMM-based DEXs

[Automated market makers](/wiki/defi/amm) replaced order books with [liquidity pools](/wiki/defi/liquidity-pool) -- smart contracts that hold reserves of two or more tokens and price trades using a deterministic formula. Traders swap against the pool rather than matching with a counterparty.

[Uniswap](/wiki/defi/uniswap) popularized this model. Other notable AMM DEXs include Curve (optimized for stablecoin and like-kind swaps) and Balancer (multi-asset pools with custom weightings).

AMMs are simple and permissionless, but they impose slippage on large trades and expose liquidity providers to [impermanent loss](/wiki/defi/impermanent-loss).

### Order-book DEXs

Some DEXs preserve the familiar order-book model but move settlement on-chain. In practice, most hybrid designs keep the order book off-chain for speed and only settle matched trades on-chain. dYdX and Loopring take this approach.

Pure on-chain order books exist but are expensive in gas and slow on L1 chains. They work better on high-throughput L2s or app-specific chains.

### Intent-based DEXs

A newer category where users sign an *intent* ("I want to sell 1 ETH for at least 2,500 USDC") and off-chain solvers compete to fill it at the best price. UniswapX and CoW Swap are leading examples. This model can tap both on-chain and off-chain liquidity and can protect users from MEV extraction.

## Why DEXs matter

**Self-custody.** You trade directly from your wallet. No exchange hack, insolvency, or withdrawal freeze can lock your funds.

**Permissionlessness.** Anyone can list a token by creating a liquidity pool, and anyone can trade it. There is no listing committee.

**Composability.** Because DEXs are smart contracts, other protocols can build on top of them -- aggregators, [yield farming](/wiki/defi/yield-farming) strategies, and automated portfolio managers all compose with DEX liquidity.

**Censorship resistance.** No single operator can block an address or delist a token (though frontends can impose restrictions, the contracts remain accessible).

## Trade-offs

- **Liquidity depth.** CEXs still dominate in raw liquidity for major pairs. DEXs rely on incentivized liquidity provision, which can dry up when rewards end.
- **Execution speed.** On-chain settlement means trades are limited by block times. L2 DEXs largely close this gap.
- **Gas costs.** Every swap is a transaction. On [Ethereum](/wiki/defi/ethereum/) L1 this can be expensive; L2s and alt-L1s reduce costs significantly.
- **UX complexity.** Managing wallets, signing transactions, and setting slippage tolerances is still harder than clicking "Buy" on a CEX.
- **MEV exposure.** Public mempools let searchers front-run or sandwich trades. Intent-based DEXs and private mempools are the main mitigations.

## DEX vs. CEX comparison

| | DEX | CEX |
|---|---|---|
| Custody | User retains control | Exchange holds funds |
| Listing | Permissionless | Curated by exchange |
| KYC | Not required at contract level | Typically required |
| Settlement | On-chain, final | Internal ledger, then on-chain withdrawal |
| Liquidity | Pool-based or solver-based | Order book with market makers |
| Regulatory risk | Contract is immutable; frontends can be restricted | Subject to jurisdiction-level regulation |

## External links

- [Wikipedia -- Decentralized exchange](https://en.wikipedia.org/wiki/Decentralized_exchange)
- [Ethereum.org -- Decentralized exchanges](https://ethereum.org/en/defi/#dex)
- [DefiLlama DEX volume rankings](https://defillama.com/dexs)
- [Paradigm -- An analysis of Uniswap markets](https://www.paradigm.xyz/2021/04/research-paper-uniswap-v3)
