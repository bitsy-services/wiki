---
title: "Yield Farming"
weight: 25
---

Yield farming is the practice of deploying crypto assets across DeFi protocols to earn returns -- trading fees, interest, or token rewards. It is also called **liquidity mining** when the rewards come in the form of a protocol's governance token.

The basic idea: protocols need liquidity to function. [Decentralized exchanges](/wiki/economics/finance/defi/dex) need tokens in [liquidity pools](/wiki/economics/finance/defi/liquidity-pool). Lending platforms need depositors. Rather than wait for capital to arrive organically, protocols offer incentives -- often their own token -- to attract it. Yield farmers chase those incentives, moving capital to wherever the returns are highest.

## Mechanics

A typical yield farming position involves stacking multiple sources of return:

1. **Base yield** -- trading fees from providing liquidity to an [AMM](/wiki/economics/finance/defi/amm) pool, or interest from lending on a platform like Aave or Compound.
2. **Incentive rewards** -- additional tokens distributed by the protocol to [LPs](/wiki/economics/finance/defi/liquidity-pool) who stake their LP tokens in a farming contract. This is the "mining" in liquidity mining.
3. **Compounding** -- reinvesting earned rewards back into the position to generate compound returns. Yield aggregators like Yearn automate this.

### Example

A farmer supplies ETH and USDC to a [Uniswap](/wiki/economics/finance/defi/uniswap) pool and receives LP tokens, then stakes those LP tokens in a farming contract that distributes a governance token (UNI, or a partner project's). The return is the pool's 0.3% swap fees plus the reward tokens, minus whatever the position loses to divergence.

## Measuring returns

### APR vs. APY

**APR (annual percentage rate)** is simple interest -- if you earn 1% per month, the APR is 12%.

**APY (annual percentage yield)** accounts for compounding. That same 1% per month, compounded, gives an APY of about 12.68%:

```text
APY = (1 + APR/n)^n - 1
```

where `n` is the number of compounding periods per year.

Protocols advertise APY because the number is always larger, but the actual return depends on how frequently rewards are harvested and reinvested. Gas costs can eat into compounding gains, especially on [Ethereum](/wiki/economics/finance/defi/ethereum/) L1.

### TVL (total value locked)

TVL is the total dollar value of assets deposited in a protocol. It is a rough proxy for trust and adoption, but a high TVL also dilutes per-dollar returns -- more capital chasing the same pool of fees and rewards means lower yield per depositor.

## Risks

The headline APY is a gross number. It prices none of the risks below, and several of them routinely exceed it.

### Impermanent loss

Farming an AMM pool makes the farmer an LP, with an LP's exposure to [impermanent loss](/wiki/economics/finance/defi/impermanent-loss). A pool paying 30% APY in fees stays ahead of IL until the pair's price ratio moves by roughly 6×, and behind it after. Stablecoin and correlated-asset pools keep that ratio near 1, which is why their much lower advertised yields are not necessarily worse.

### Smart contract risk

Yield farmers often stack positions across several protocols at once — deposit in Aave, borrow, LP on Uniswap, stake the LP token in a farm. The position fails if any one of those four contracts fails, so the failure probabilities compound in the wrong direction while the yields add up in the advertised one.

### Token reward dilution

Farming rewards paid in a protocol's governance token are only valuable if the token holds its price. Many farming tokens face constant sell pressure from farmers dumping rewards, driving the price down over time. A 500% APY paid in a token that drops 90% is a net loss.

### Rug pulls

In the worst case, the farming contract or token contract is malicious. The deployer drains deposited funds or mints unlimited tokens. This is most common with unaudited, anonymous projects offering implausibly high APYs.

### Gas costs

On Ethereum L1, each deposit, stake, harvest, and compound transaction costs gas. For small positions, gas can consume a large fraction of the yield. L2 chains and alt-L1s (Arbitrum, Optimism, Base) make farming viable at smaller scales.

## Strategies

**Single-sided staking.** Deposit a single asset (e.g., stETH) into a protocol that pays yield. Simpler and avoids impermanent loss, but typically lower returns.

**LP farming.** Provide a token pair to an AMM pool and stake the LP tokens for additional rewards. Higher returns, higher risk.

**Leveraged farming.** Borrow against deposited collateral to increase the size of a farming position. Amplifies both gains and losses. Liquidation risk is the main danger.

**Yield aggregation.** Use a vault (Yearn, Beefy) that automatically compounds rewards and rotates between strategies. Convenience and gas savings at the cost of a management fee and an additional smart contract dependency.

## A brief history

Yield farming exploded in the "DeFi Summer" of 2020. Compound launched its COMP token distribution in June 2020, and farmers quickly discovered they could earn outsized returns by borrowing and re-lending in loops. SushiSwap's "vampire attack" on Uniswap liquidity followed, and within weeks dozens of food-themed farming protocols (Yam, Pickle, Sushi) appeared. TVL across DeFi went from ~$1B in June 2020 to over $15B by September.

The mania cooled as token prices fell and unsustainable APYs collapsed, but the underlying mechanism -- using token incentives to bootstrap liquidity -- remains a core DeFi growth strategy.

## External links

- [Ethereum.org -- DeFi](https://ethereum.org/en/defi/)
- [DefiLlama -- Protocol yields](https://defillama.com/yields)
- [Compound governance -- COMP distribution](https://compound.finance/governance/comp)
