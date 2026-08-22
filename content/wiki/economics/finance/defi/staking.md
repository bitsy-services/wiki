---
title: "Staking"
weight: 30
---

Staking is the act of locking cryptocurrency in a protocol to earn rewards. The term covers two distinct mechanisms: **network staking**, where locked tokens secure a blockchain's consensus, and **DeFi staking**, where tokens are deposited into [smart contracts](/wiki/economics/finance/defi/smart-contract) to earn yield from protocol activity.

Both forms share the same core idea — you commit capital, accept illiquidity, and receive compensation for the service your capital provides.

## Network staking (Proof of Stake)

In a Proof-of-Stake (PoS) blockchain, validators lock tokens as collateral and are selected to propose and attest to blocks in proportion to their stake. Honest behaviour earns rewards (newly minted tokens plus transaction fees); dishonest behaviour triggers **slashing**, where some or all of the validator's stake is destroyed.

This creates a direct economic incentive to follow the rules — the more you have at stake, the more you have to lose.

### How it works in practice

1. A validator deposits the required minimum (32 ETH on [Ethereum](/wiki/economics/finance/defi/ethereum/), for example).
2. The protocol assigns the validator to propose or attest to blocks according to a pseudorandom schedule.
3. Rewards accrue per epoch (a fixed interval of blocks). They come from inflation and from priority fees.
4. To withdraw, the validator signals an exit and waits through an unbonding period — a cooldown designed to allow time for slashing if misbehaviour is detected.

### Delegated staking and liquid staking

Not everyone wants to run a validator. Two patterns address this:

- **Delegation** — token holders delegate their stake to a validator and share in the rewards (common on Cosmos-SDK chains, Polkadot, Solana).
- **Liquid staking** — a protocol (Lido, Rocket Pool) accepts deposits, runs validators, and issues a liquid receipt token (stETH, rETH) that can be traded or used in DeFi while the underlying tokens remain staked. This solves the illiquidity problem but adds smart contract risk.

## DeFi staking

In DeFi, "staking" is used loosely to describe depositing tokens into a protocol in exchange for rewards. Common variants:

- **[Liquidity pool](/wiki/economics/finance/defi/liquidity-pool) deposits** — providing assets to an [AMM](/wiki/economics/finance/defi/amm) [DEX](/wiki/economics/finance/defi/dex) earns trading fees and sometimes additional token incentives. This is sometimes called [yield farming](/wiki/economics/finance/defi/yield-farming) when the primary goal is earning governance token rewards.
- **Single-sided staking** — locking a governance token to earn a share of protocol revenue or additional token emissions.
- **Lockup-boosted rewards** — protocols like Curve use vote-escrowed tokens (veCRV) where longer lock periods grant higher reward multipliers and governance weight.

## Risks

| Risk | Description |
|------|-------------|
| **Slashing** | Validator misbehaviour or downtime can destroy part of the stake (network staking). |
| **Smart contract bugs** | Deposited tokens are only as safe as the contract holding them. |
| **Illiquidity** | Unbonding periods mean you cannot exit instantly. Market conditions can change during the wait. |
| **Price volatility** | Rewards are denominated in the staked token. A 10% APR (annual percentage rate) is meaningless if the token drops 50%. |
| **[Impermanent loss](/wiki/economics/finance/defi/impermanent-loss)** | Applies when staking in AMM liquidity pools. The pool rebalances against you as prices move. |

## External links

- [Ethereum staking overview](https://ethereum.org/en/staking/) — official guide to staking on Ethereum
- [Proof-of-Stake FAQ](https://vitalik.eth.limo/general/2017/12/31/pos_faq.html) — Vitalik Buterin's detailed PoS explainer
- [Liquid staking landscape](https://defillama.com/protocols/Liquid%20Staking) — DefiLlama tracker for liquid staking protocols
