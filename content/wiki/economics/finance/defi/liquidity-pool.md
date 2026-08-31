---
title: "Liquidity Pool"
weight: 15
---

A liquidity pool is a smart contract that holds reserves of two or more tokens and allows anyone to trade against those reserves according to a deterministic pricing function. Pools are the core primitive of [AMM](/wiki/economics/finance/defi/amm)-based [decentralized exchanges](/wiki/economics/finance/defi/dex).

On a traditional exchange, liquidity comes from market makers who post bids and asks on an order book. On-chain, that model is impractical -- gas costs and block times make continuous order management expensive. Liquidity pools solve this by letting anyone deposit tokens into a contract that automatically quotes prices using a formula like the [constant product](/wiki/economics/finance/defi/constant-product-formula). Traders swap against the pool's reserves; liquidity providers (LPs) earn a share of the fees.

## Anatomy of a pool

A typical two-token pool (e.g., ETH/USDC) has:

- **Reserves** -- the token balances the contract holds. The ratio of reserves determines the current price.
- **Pricing invariant** -- a formula constraining how reserves change on each trade. For a constant-product pool: `reserve_a * reserve_b = k`.
- **Fee** -- a percentage (commonly 0.3%) charged on each swap and added to the reserves, growing the pool over time.
- **LP tokens** -- [ERC-20](/wiki/economics/finance/defi/ethereum/erc-20) tokens minted to depositors, representing a pro-rata claim on the pool's reserves and accumulated fees.

## Providing liquidity

An LP deposits tokens into the pool's smart contract. A standard constant-product pool requires both tokens in the current reserve ratio, so a 50/50 ETH/USDC pool takes equal value of each. The contract mints LP tokens in proportion to the depositor's share of the total reserves.

Withdrawing burns those LP tokens and returns that share of whatever the reserves now hold. The amounts differ from what went in: trades have shifted the ratio, and fees have accumulated on top.

### Worked example

A pool holds 10 ETH and 25,000 USDC (ETH at $2,500). A deposit of 1 ETH and 2,500 USDC mints LP tokens worth 10% of the pool. Trading fees then raise the reserves to 10.5 ETH and 26,250 USDC, and the same 10% share is now 1.05 ETH + 2,625 USDC — a 5% return on both legs.

That calculation holds the ETH price fixed. If it moved, the reserve ratio moved with it, and [impermanent loss](/wiki/economics/finance/defi/impermanent-loss) offsets some or all of the fee income.

## Risks

### Impermanent loss

When the price ratio of the pooled tokens moves away from the ratio at deposit time, the LP ends up with less value than someone who simply held the two tokens. The loss is "impermanent" only if prices revert. In practice, for volatile pairs, impermanent loss is often permanent and can exceed fee income. See [impermanent loss](/wiki/economics/finance/defi/impermanent-loss) for the mechanics and math.

### Smart contract risk

Pools are only as safe as their code. [Uniswap](/wiki/economics/finance/defi/uniswap) contracts have been extensively audited and have held billions without exploit, but forks and newer protocols carry higher risk. [Rug pulls](/wiki/economics/finance/fraud/rug-pull) -- where the deployer withdraws the liquidity backing a token they sold -- are a real threat for pools involving unvetted tokens, as are [honeypot tokens](/wiki/economics/finance/fraud/honeypot-token) whose transfer path refuses to sell.

### Concentration risk

In concentrated-liquidity pools (Uniswap V3+), LPs choose a price range. If the market price moves outside that range, the position earns zero fees and is fully converted into the less valuable token. Active management or automated position managers become necessary.

## Pool types beyond constant product

| Type | How it works | Good for |
|---|---|---|
| Constant product | `x * y = k` -- simple, universal | General-purpose token pairs |
| StableSwap (Curve) | Blends constant-sum and constant-product | Stablecoins, like-kind assets |
| Weighted (Balancer) | Multi-token pools with custom weights (e.g., 80/20) | Index-like exposure, reduced [IL](/wiki/economics/finance/defi/impermanent-loss) for certain weightings |
| Concentrated liquidity | LPs provide liquidity in a chosen price range | Capital-efficient trading on active pairs |

## Use cases beyond trading

The same contract shape shows up well outside trading:

- **[Yield farming](/wiki/economics/finance/defi/yield-farming)** -- protocols incentivize LPs with additional token rewards on top of trading fees.
- **Lending** -- platforms like Aave and Compound use pool-based models where depositors supply tokens that borrowers draw from.
- **Synthetic assets** -- protocols use pools to maintain collateral backing for synthetic tokens.

## External links

- [Uniswap -- How Uniswap works](https://docs.uniswap.org/concepts/uniswap-protocol)
- [Wikipedia -- Constant function market maker](https://en.wikipedia.org/wiki/Constant_function_market_maker)
- [Balancer -- Liquidity pools](https://docs.balancer.fi/)
- [Curve -- StableSwap whitepaper](https://curve.fi/files/stableswap-paper.pdf)
