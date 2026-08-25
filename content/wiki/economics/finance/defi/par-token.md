---
title: "Par Token"
weight: 90
---

A **par token** is a token whose price against one specific reference asset is structurally clamped to a hard, narrow band starting at parity — acquirable at a known maximum premium, exitable at no worse than par — backed at least 1:1 by the real reference asset, with no oracle, no redemption function, and no governance, permissionlessly instantiable for any [ERC-20](/wiki/economics/finance/defi/ethereum/erc-20).

It is not a new primitive but a specific *composition* of documented ones.

## A coined term, on purpose

"Par token" is a term of art coined for precision, the way "[flash loan](https://en.wikipedia.org/wiki/Flash_loan)" or "concentrated liquidity" were — because every off-the-shelf word misdescribes it in a way a technical reader will catch:

- **Wrapped** asserts an escrow plus a burn-to-redeem desk. There is no desk.
- **Mirror / synthetic** asserts oracle-priced exposure backed by *different* collateral. A par token holds the *real* asset, 1:1.
- **Pegged** (bare) asserts an actively *maintained*, roughly symmetric peg. This peg is *geometric* and one-sided: a hard floor at par, a ≤1-bp ceiling.

"Par" names the load-bearing property — a hard floor at parity with the reference asset — and carries no false redemption or synthetic connotation.

## The definition, stated to be attacked

> A par token's price against its reference asset is bounded to `[1.0000, 1.0001)` for the whole of circulating supply, by construction; backed ≥1:1 by the real reference asset accumulated in the position; with no oracle, no redemption function, no governance, and no party — issuer, [LP](/wiki/economics/finance/defi/liquidity-pool), keeper — able to alter, withdraw, or unwind any of it; permissionlessly instantiable for any ERC-20.

That sentence is falsifiable: a critic can try to name the missing actor, or a prior instance.

## The composition

A par token is exactly these six techniques, locked together:

1. [Single-tick liquidity](/wiki/economics/finance/defi/uniswap/single-tick-liquidity) — the entire supply seated in one [tick](/wiki/economics/finance/defi/uniswap/ticks) makes price a near-fixed rate inside a 1-bp corridor.
2. [Liquidity floor](/wiki/economics/finance/defi/liquidity-floor) — no liquidity below par means sells cannot push price under 1:1.
3. [Oracle-free pricing](/wiki/economics/finance/defi/oracle-free-pricing) — the corridor is a theorem about the position, not a feed; nothing to manipulate or stall.
4. [Locked liquidity](/wiki/economics/finance/defi/locked-liquidity) — the position has no decrease path, so the backing can never be unwound.
5. [Full-reserve backing](/wiki/economics/finance/defi/full-reserve-backing) — the reserve is the real originals accumulated 1:1 as buyers swap in.
6. [Permissionless token factory](/wiki/economics/finance/defi/permissionless-token-factory) — anyone can instantiate one for any ERC-20, no gate.

## What each part alone is missing

Each constituent is documented and unremarkable on its own, and none of them alone is a par token:

- Locked liquidity alone does not peg anything.
- A single-tick position alone is not permanent, oracle-free-by-design, or 1:1-collateralized.
- A liquidity floor alone bounds only the downside.

Single-sided full-supply seating, a permanent lock, *and* serving as the 1:1 reserve are goals that fight each other in naive designs. Making all three hold at once, with every discretionary actor deleted, produces a **closure**: an immutable, oracle-free, redemption-free, governance-free, permissionlessly-instantiable hard peg by construction.

## What it is *not*

- **Not redeemable at a desk.** There is no burn-to-redeem function. The exit is a sale back into the same locked position at ≥ par. "Economically recoverable" — true. "Redeemable 1:1" — false.
- **Not a synthetic.** It does not track the reference asset via an oracle. It *holds* the reference asset.
- **Not arbitrage-maintained.** Nothing acts to restore the peg. The peg is where the liquidity is.

## Prior-art relatives

A par token is a novel *composition*, scoped honestly: no public protocol matching the full closure has been found, though every constituent is documented.

- **Single-tick range orders** — Uniswap-documented; the fixed-price building block.
- **Floor-by-absence** — a recurring Uniswap V4 single-sided launch pattern.
- **Oracleless pricing** — Fluid (Instadapp) is the prominent named instance, applied to lending.
- **Olympus Range-Bound Stability** — the closest *integrated* relative: a price bounded by placed liquidity. But RBS was governance-run, treasury-backed, oracle-referenced, and a symmetric band — a par token is permissionless, real-asset-reserved, oracle-free, immutable, and asymmetric.
- **Currency boards and bearer instruments** — the traditional-finance economic analog: full reserve, fixed rate, no discretion; the issuer earns the [float](/wiki/economics/finance/defi/full-reserve-backing), not the principal — exactly a traveler's-cheque arrangement.

## Brand vs. instrument

"Par token" is the generic instrument class. **Reflector** is Uniteum's factory that issues them; a **Reflector issue** is one concrete par token. The split is deliberate and conventional — brand the protocol, define the instrument — the same way "Uniswap" is a protocol and "liquidity position" is the instrument. Reflector's corridor (`tick = 0`, `fee = 100`, `tickSpacing = 1`) is the canonical concrete realization of the definition above.

## External links

- [Reflector](https://uniteum.one/reflector/) — Uniteum's par-token factory (the canonical implementation)
- [Reflector — peg mechanics](https://uniteum.one/reflector/mechanics/) — the corridor and lock in contract terms
- [Uniswap — Range orders](https://docs.uniswap.org/concepts/protocol/range-orders)
- [Fluid — Oracleless lending](https://blog.instadapp.io/oracleless-lending-protocol-on-uniswap-v4/)
