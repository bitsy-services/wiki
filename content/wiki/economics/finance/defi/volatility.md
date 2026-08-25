---
title: "Volatility"
weight: 22
---

Volatility measures how much an asset's price moves over a given period. In traditional finance it is a statistical concept -- the annualised standard deviation of returns. In DeFi it is an input rather than a description: it sets [impermanent loss](/wiki/economics/finance/defi/impermanent-loss), the loan-to-value ratio a lending protocol will accept, the premium on an option, and whether a [liquidity pool](/wiki/economics/finance/defi/liquidity-pool) position clears its costs.

[Cryptocurrency](/wiki/economics/finance/defi/cryptocurrency) markets are structurally more volatile than most traditional asset classes. Tokens trade 24/7 on fragmented venues with thin order books, and prices respond sharply to regulatory news, exploit events, and social-media momentum.

## Historical vs. implied

**Historical volatility (HV)** is backward-looking: take an asset's daily returns over some window (30 days is common), compute the standard deviation, and annualise it. ETH historical volatility often ranges from 50% to over 100% annualised, compared to roughly 15-20% for the S&P 500.

**Implied volatility (IV)** is forward-looking: it is the volatility number that, when plugged into an option pricing model, reproduces the market price of an option. IV reflects what traders *expect* volatility to be over the option's remaining life. When IV is higher than HV, the market is pricing in more uncertainty than recent history would suggest.

DeFi options protocols like Lyra and Premia surface IV on-chain, making it a tradeable quantity rather than just a risk measure.

## What depends on it

### Impermanent loss

IL is a direct function of price divergence between pool assets. The more volatile the pair, the more likely prices diverge, and the larger the IL. For a constant-product pool, the formula depends only on the price ratio -- and volatility determines how far that ratio is likely to travel. Stablecoin-stablecoin pools barely move that ratio and see near-zero IL; ETH/memecoin pools move it by multiples, and double-digit percentage losses follow directly from the table.

See the [impermanent loss](/wiki/economics/finance/defi/impermanent-loss) page for the formula and a table of IL at various price ratios.

### Concentrated liquidity range selection

In [Uniswap](/wiki/economics/finance/defi/uniswap) V3 and similar [AMMs](/wiki/economics/finance/defi/amm), [LPs](/wiki/economics/finance/defi/liquidity-pool) choose a price range for their liquidity. A narrower range earns more fees per unit of capital but goes out of range more often. Choosing a range is a volatility bet in both directions: wide enough to contain the price path over the intended holding period, narrow enough that the capital sits where trades actually happen.

High-volatility pairs demand wider ranges; low-volatility pairs reward tight ranges.

### Liquidations

Lending protocols like Aave and Compound liquidate borrowers whose collateral value drops below a threshold. Volatile collateral can cross that threshold quickly, leaving less time for the borrower to add margin. This is why lending protocols set lower loan-to-value ratios and higher liquidation penalties for volatile assets.

### Option pricing

On-chain options (Lyra, Premia, Hegic) price contracts using IV. When IV is high, premiums are expensive -- good for sellers, costly for buyers. When IV is low, buying options is cheaper but there is less expected movement to profit from. For an at-the-money option the premium is close to linear in IV, so a doubling of the volatility input roughly doubles what the contract costs.

## Measuring volatility on-chain

On-chain volatility oracles aggregate price data from [DEXs](/wiki/economics/finance/defi/dex) or [oracle networks](/wiki/economics/finance/defi/oracle-node) and compute realised volatility over rolling windows. These feeds are used by protocols that need a volatility input -- dynamic fee AMMs, options vaults, and risk engines.

Some approaches:

- **TWAP-based realised vol.** Compute returns from time-weighted average prices, then standard deviation. Resistant to single-block manipulation.
- **Implied vol from on-chain options.** Back out IV from the mid-market price of liquid on-chain options.
- **Off-chain feeds.** [Chainlink](/wiki/economics/finance/defi/chainlink/automation) and other oracle providers can relay volatility indices computed off-chain.

## Volatility and LP strategy

Practical takeaways for [liquidity pool](/wiki/economics/finance/defi/liquidity-pool) participants:

- **High-volatility pairs.** Expect significant IL. Fee income needs to be high enough to compensate. Concentrated positions will go out of range frequently.
- **Low-volatility pairs.** IL is minimal. Tight concentrated ranges capture most of the fee revenue. Stablecoin pairs and correlated asset pairs (e.g. ETH/stETH) fall here.
- **Regime shifts.** Volatility clusters -- calm periods are followed by turbulent ones. A range that worked last month may not survive a volatility spike. Active management or automated vault strategies (like those built on [ERC-4626](/wiki/economics/finance/defi/ethereum/erc-4626)) help adapt.

## External links

- [Investopedia -- Volatility](https://www.investopedia.com/terms/v/volatility.asp)
- [Uniswap V3 LP strategy and volatility](https://uniswap.org/blog/uniswap-v3)
