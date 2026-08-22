---
title: "DeFi on Sui"
weight: 80
---

Sui's DeFi ecosystem is young, fast-growing, and architecturally distinct from the EVM world. The [object model](/wiki/economics/finance/defi/sui/object-model) and parallel execution that define the chain are not just performance footnotes here — they enable a class of on-chain primitive, the native order book, that is impractical on a globally-locked chain like Ethereum. This page maps the landscape protocol-by-protocol, then turns to the honest part: how mature the ecosystem actually is, and what has gone wrong.

## DeepBook — the native order book

The flagship Sui DeFi primitive is **DeepBook** (now **DeepBook v3**), a fully on-chain **central limit order book** (CLOB) maintained by Mysten Labs. Rather than another application competing for users, DeepBook is positioned as a public good: a shared-liquidity layer that other protocols route through. Aggregators, AMMs, and wallets can all source liquidity from the same order book, so depth is pooled rather than fragmented across a dozen siloed pools.

Why is an on-chain CLOB notable at all? Most DeFi runs on **automated market makers** ([AMMs](/wiki/economics/finance/defi/dex)) precisely because a real order book is expensive on chain: every limit order, cancel, and match is a state write, and on a chain with a global execution lock those writes serialize and cost gas that makes professional market-making uneconomic. AMMs sidestep this by replacing the order book with a pricing curve, at the cost of slippage, impermanent loss, and worse price discovery for large or illiquid pairs. Sui changes the economics. Because [parallel execution](/wiki/economics/finance/defi/sui/object-model) lets transactions touching disjoint objects run concurrently, and because gas is fractions of a cent, posting and cancelling orders at high frequency becomes viable. The result is sub-second matching and an order book that feels closer to a centralized exchange than to a constant-product AMM — the order-book model traditional traders expect, settled on chain.

DeepBook v3 introduced its own fee-and-governance token, **DEEP**, with a 10 billion hard cap (the majority earmarked for ecosystem incentives and market-maker rewards). DEEP serves several roles: traders may pay fees in DEEP at a discount relative to paying in the input token; staking DEEP further reduces taker fees and earns a share of protocol revenue; and holders govern per-pool parameters (fee tiers, staking requirements) through on-chain voting. v3 also added **flash loans** — uncollateralized borrows that must be repaid within the same transaction — which compose naturally with Sui's [programmable transaction blocks](/wiki/economics/finance/defi/sui/programmable-transaction-blocks) to enable arbitrage and atomic multi-step strategies.

## AMM DEXs

Despite DeepBook's prominence, AMMs remain where most retail liquidity sits. **Cetus** is the largest, offering concentrated-liquidity ([CLMM](/wiki/economics/finance/defi/dex)) pools where LPs concentrate capital in a chosen price band for higher fee capture. **Turbos**, **Kriya**, **Aftermath**, and **FlowX** round out the field with their own CLMM and weighted-pool designs. A recurring pattern: many of these integrate DeepBook liquidity directly, so a swap routed through an AMM front-end may settle partly against the native order book — the shared-liquidity thesis in practice.

## Lending

The major money markets are **Suilend** (the largest lending protocol, with its own SEND token and a SpringSui liquid-staking offshoot), **Navi**, and **Scallop**. All three follow the familiar pooled-deposit, over-collateralized-borrow model, with isolated or tiered risk parameters per asset.

## Liquid staking

Native SUI staking locks tokens with a validator; **liquid staking** issues a transferable receipt token that accrues rewards while remaining usable as DeFi collateral — see [staking](/wiki/economics/finance/defi/staking) for the general mechanism and its risks (depeg, slashing, validator concentration). On Sui the main issuers are **Haedal** (the largest by TVL), **Volo** (acquired by Navi), and **Aftermath** (afSUI). These liquid staking tokens let SUI holders earn the base staking yield and simultaneously lend, LP, or borrow against the same capital.

## Stablecoins and bridges

**Native USDC** is live, issued directly by Circle and redeemable through Circle Mint — Sui was the first Move-based L1 to land it. Older **bridged USDC (wUSDC)** brought over Ethereum USDC via **Wormhole** and is *not* Circle-redeemable; protocols have been migrating away from it toward the native asset. A native **USDsui** stablecoin (reward-bearing, built on Bridge's Open Issuance platform) launched in late 2025. Cross-chain transfers run through **Sui Bridge**, the protocol's native bridge for moving assets to and from Ethereum, alongside third-party bridges like Wormhole.

## Aggregators and routers

Sui's [programmable transaction blocks](/wiki/economics/finance/defi/sui/programmable-transaction-blocks) make composability a first-class feature rather than a contract-level afterthought: a single transaction can chain a flash loan, a swap split across DeepBook and several AMMs, and a deposit, all atomically. DEX aggregators and routers exploit this to split orders for best execution across the fragmented AMM liquidity plus the shared DeepBook book.

## State of the ecosystem and risks

Be candid about maturity. Sui DeFi is real but small and lightly battle-tested relative to Ethereum. TVL peaked around **$2.6 billion in October 2025** and had fallen to roughly **$561 million by February 2026**, driven by both the Cetus exploit below and broad market weakness. Fewer protocols, fewer independent audits, and far less adversarial history mean smart-contract risk should be assumed higher here than on more mature chains.

Risks, worst first:

- **Smart-contract / fund-loss risk.** In **May 2025, Cetus was exploited for roughly $220–223 million** — the largest incident in Sui's history. The root cause was an arithmetic **overflow bug** in the AMM's liquidity math: a flawed `checked_shlw` overflow check (comparing against the wrong bit threshold) let an attacker mint enormous liquidity by depositing a single token unit, then drain pools. Around $60M was bridged out to Ethereum before it could be stopped; the remaining ~$162M was **frozen on Sui by validator action**, and Cetus later compensated users with treasury funds plus a Sui Foundation loan. This is a flashing-red reminder that Move's resource safety prevents *some* bug classes (reentrancy, accidental loss) but does nothing for application-level arithmetic errors.
- **Centralization vs. recovery tension.** The same validator coordination that froze the stolen funds is a double-edged sword. It recovered users' money — a genuine safety net — but it also demonstrated that a quorum of validators can censor specific transactions in an emergency. That is decentralization theater to some and prudent crisis response to others; either way it is a property of the chain DeFi users should understand before trusting it with size.
- **Liquidity and depeg risk.** Thin TVL means large positions move prices and can be hard to exit; liquid staking tokens and bridged assets carry their own depeg surface.
- **[MEV](/wiki/economics/finance/defi/maximal-extractable-value) exposure.** Owned-object transactions that skip [consensus](/wiki/economics/finance/defi/sui/consensus) avoid ordering games, narrowing the MEV surface for some flows. But shared-object DeFi — AMM swaps, order-book matching, liquidations — still orders through consensus and is not immune to sandwiching or back-running. The posture is better than a naive EVM mempool, not MEV-free.

For the broader chain architecture that makes all of this possible, see the [Sui section](/wiki/economics/finance/defi/sui/).

## External Links

- [Sui Documentation](https://docs.sui.io/) — official developer docs
- [DeepBook](https://www.deepbook.tech/) — the native on-chain order book
- [DefiLlama: Sui](https://defillama.com/chain/Sui) — live TVL, fees, and protocol rankings
- [The Cetus AMM $200M Hack: How a Flawed Overflow Check Led to Catastrophic Loss](https://dedaub.com/blog/the-cetus-amm-200m-hack-how-a-flawed-overflow-check-led-to-catastrophic-loss/) — technical post-mortem
