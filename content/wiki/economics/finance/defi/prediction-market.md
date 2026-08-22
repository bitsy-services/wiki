---
title: "Prediction Market"
weight: 45
---

A prediction market is a platform where participants trade contracts whose payout depends on the outcome of a future event. The market price of each contract reflects the crowd's estimated probability of that outcome. If a "Yes" share on "Will ETH be above $5,000 on December 31?" trades at $0.35, the market is pricing a 35% probability.

In DeFi, prediction markets run on [smart contracts](/wiki/economics/finance/defi/smart-contract) that handle market creation, trading, and settlement without intermediaries. The [blockchain](/wiki/economics/finance/defi/blockchain) provides the settlement guarantee: once the outcome is determined, the contract pays winners automatically and irreversibly.

## How they work

### Outcome tokens

A market starts with a question and a set of mutually exclusive outcomes. For a binary market ("Yes" / "No"), the protocol mints one token for each outcome. A complete set -- one Yes token plus one No token -- always redeems for exactly $1 (or 1 USDC, etc.) at settlement, regardless of which outcome wins.

This means:
- If you buy a Yes token for $0.35 and the event happens, you receive $1. Profit: $0.65.
- If the event does not happen, your token is worth $0.00. Loss: $0.35.

Prices are free to move between $0 and $1 as new information arrives. Trading is continuous -- participants buy and sell outcome tokens on an order book or through an [AMM](/wiki/economics/finance/defi/amm).

### Resolution

When the event concludes, someone (or some mechanism) reports the actual outcome. The smart contract then:

1. Marks the winning outcome.
2. Allows holders of the winning token to redeem for the full payout.
3. Makes losing tokens worthless.

Resolution is the hardest design problem. The market is only as trustworthy as the entity determining the outcome. Different platforms handle this differently (see below).

## Major platforms

### Polymarket

Polymarket is the largest prediction market by volume. It runs on Polygon and uses a central limit order book (CLOB) model rather than an AMM for matching trades, giving tighter spreads and better price discovery on liquid markets. Markets cover politics, crypto prices, sports, geopolitics, and cultural events.

Resolution on Polymarket uses UMA's optimistic oracle: a proposer asserts the outcome, and anyone can dispute it within a challenge window. If disputed, UMA token holders vote on the correct outcome.

### Augur

Augur was one of the first decentralized prediction markets, launched on [Ethereum](/wiki/economics/finance/defi/ethereum/) in 2018. It allows anyone to create a market on any event. Resolution relies on a decentralized oracle system where REP token holders report outcomes and stake tokens on their reports. Incorrect reporters lose their stake, creating an economic incentive for honest reporting.

Augur pioneered the concept but struggled with low liquidity and a complex UX. Augur V2 (Augur Turbo) simplified the experience but never reached Polymarket's scale.

### Gnosis (now part of the Gnosis ecosystem)

Gnosis developed the **Conditional Tokens Framework**, an open standard for outcome tokens that other platforms can build on. Rather than running a consumer-facing prediction market, Gnosis focused on infrastructure: conditional token contracts, [AMM](/wiki/economics/finance/defi/amm) tooling, and the Safe multisig wallet.

Gnosis's conditional tokens support combinatorial markets -- markets where outcomes can be combined across multiple events (e.g., "Party X wins *and* GDP growth exceeds 3%").

## Resolution mechanisms compared

| Platform | Oracle mechanism | Trust model |
|---|---|---|
| Polymarket | UMA optimistic oracle | Optimistic with dispute window; UMA holders vote on disputes |
| Augur | REP staking + dispute rounds | Decentralized; reporters have economic skin in the game |
| Gnosis conditional tokens | Pluggable (Reality.eth, Chainlink, custom) | Depends on the oracle chosen by the market creator |

The choice of oracle determines the market's credibility. Centralised resolution (a single trusted reporter) is fast but introduces counterparty risk. Decentralised oracle systems are more robust but slower and more expensive to operate.

## Market types

**Binary.** Two outcomes: Yes or No. The most common format. Example: "Will Bitcoin reach $100k in 2026?"

**Categorical.** Multiple mutually exclusive outcomes. Example: "Which team will win the World Cup?" Each outcome gets its own token; a complete set of all tokens redeems for $1.

**Scalar.** The payout is proportional to where the actual value falls within a range. Example: "What will ETH's price be on June 30?" If the range is $1,000 to $5,000 and the actual price is $3,000, a Long token pays $0.50 and a Short token pays $0.50.

## Why prediction markets matter

Prediction markets are among the most direct applications of the "wisdom of crowds" idea: when people have money at stake, they aggregate and reveal information more honestly than polls or pundit forecasts. Empirically, prediction markets have been strong forecasters for elections, policy outcomes, and economic indicators.

In DeFi specifically, prediction markets are interesting because:

- They create a price signal for any verifiable event, which other protocols can consume.
- They demonstrate the power of [smart contract](/wiki/economics/finance/defi/smart-contract) settlement -- no bookmaker, no counterparty, no delayed payout.
- They push the boundaries of decentralised oracle design, a problem that matters well beyond prediction markets.

## Risks

- **Oracle manipulation.** If the resolution oracle can be bribed or manipulated, the market is compromised. This is the fundamental attack surface.
- **Regulatory uncertainty.** Prediction markets that resemble gambling or derivatives may face legal restrictions depending on jurisdiction. Polymarket restricted US users after CFTC scrutiny.
- **Thin liquidity.** Niche markets may not attract enough participants for reliable price discovery. Prices in illiquid markets can be noisy and misleading.

## External links

- [Polymarket](https://polymarket.com/)
- [Augur whitepaper](https://augur.net/whitepaper.pdf)
- [Gnosis Conditional Tokens documentation](https://docs.gnosis.io/conditionaltokens/)
- [UMA optimistic oracle](https://docs.uma.xyz/)
