---
title: Innovative Claims of CBSOs
weight: 84
---

[Cash-backed synthetic options](/wiki/economics/finance/defi/options/cash-backed-synthetic-option) (CBSOs) combine several properties that, taken together, distinguish them from both traditional options and existing DeFi derivatives. The claims below are separable: each states one property of the design and the conventional arrangement it departs from.

## Core Innovations

### Dual Volatility Management

Traditional options assume a stable settlement currency (USD) and a volatile underlying asset. CBSOs allow the settlement currency itself to be volatile (e.g., ETH), enabling hedging against *both* asset price movement and settlement-currency risk simultaneously. This is not possible in conventional options markets.

### Risk-Defined by Construction

Every CBSO caps the holder's profit and the minter's loss at the staked collateral amount. This makes every position a [risk-defined strategy](/wiki/economics/finance/defi/options/risk-defined-strategy) by construction -- not by convention or careful leg selection. The [smart contract](/wiki/economics/finance/defi/smart-contract) enforces the cap, eliminating the possibility of undefined risk that exists with naked options.

### Single-Transaction Spread Execution

In traditional markets, entering a [vertical spread](/wiki/economics/finance/defi/options/vertical-spread) requires two separate transactions (buy one leg, sell the other), with execution risk between them. CBSO minting produces the equivalent of a fully collateralized spread in a single atomic transaction. This eliminates leg risk and reduces transaction costs.

### Flexible Staking Currency

CBSOs are not limited to stablecoins as collateral. Any [ERC-20](/wiki/economics/finance/defi/ethereum/erc-20) token -- including volatile assets, governance tokens, or custom tokens -- can serve as the settlement currency. The system adjusts [oracle](/wiki/economics/finance/defi/oracle-node) costs proportionally to the value and [volatility](/wiki/economics/finance/defi/volatility) of the chosen currency.

### Synthetic Exposure Without Ownership

Holders gain exposure to an asset's price movement without ever owning or custodying the underlying asset. The payout is determined entirely by the [oracle](/wiki/economics/finance/defi/oracle-node) price feed at expiry, settled in the staked currency. This enables options-like exposure to assets (equities, commodities, indices) that do not natively exist on-chain.

### Strategy Composition via Bull and Bear Bets

By combining [bull bets](/wiki/economics/finance/defi/options/bull-bet) and [bear bets](/wiki/economics/finance/defi/options/bear-bet) at different [strike prices](/wiki/economics/finance/defi/options/strike-price), traders can replicate multi-leg strategies -- iron condors, butterfly spreads, calendar spreads -- entirely from composable on-chain tokens. See [emulating option strategies](/wiki/economics/finance/defi/options/emulating-option-strategies) for worked examples.

### Custom Asset Portfolios

CBSOs can be constructed against custom indices or baskets of assets, functioning as synthetic options on a bespoke portfolio. This is analogous to options on a custom mutual fund -- something that has no practical equivalent in traditional retail options markets.

## Operational Innovations

### Collateralization Fee with Prorated Refunds

The [collateralization fee](/wiki/economics/finance/defi/collateralization-fee) accrues based on the duration and amount of locked collateral. If a minter buys back and burns tokens before expiration, they receive a prorated refund. This incentivizes active position management and efficient capital use.

### Automatic Refund for Unsold Options

If minted CBSOs are never sold before expiry, the minter receives their collateral back (minus fees). Traditional unsold options simply expire worthless with no recovery mechanism.

### Decentralized Settlement via Oracles

Settlement relies on price data from decentralized [oracle nodes](/wiki/economics/finance/defi/oracle-node) rather than a centralized exchange or clearinghouse. The [finalized price](/wiki/economics/finance/defi/finalized-smart-contract) is immutable once locked, ensuring all options at a given expiry settle against the same value.

### On-Chain Auditability

Every CBSO -- its creation, transfer history, settlement, and fee collection -- is recorded on the [blockchain](/wiki/economics/finance/defi/blockchain). The entire lifecycle is transparent and independently verifiable without relying on a third party's records.
