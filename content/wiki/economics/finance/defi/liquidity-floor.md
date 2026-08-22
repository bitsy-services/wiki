---
title: "Liquidity Floor"
weight: 85
---

A liquidity floor is a price below which a token cannot trade because there is no liquidity there to sell into. The floor is not *defended* — there is no buyback, no peg keeper, no treasury bid. It is enforced by the **absence** of any position beneath it. A sell order has nowhere to go, so price stops.

## Floor by defense vs. floor by absence

There are two ways to stop a price from falling:

- **Defended floor.** Someone stands ready to buy at the floor — a treasury, a bonding mechanism, a market maker. It holds until the buyer's capital or willingness runs out. Algorithmic stablecoins and treasury-backed tokens use this; it fails exactly when it is most needed.
- **Absence floor.** There is simply no order book or [AMM](/wiki/economics/finance/defi/amm) depth below the floor price. There is nothing to sell *into*. Nothing has to be spent to hold the line because holding the line is the default state.

The absence floor has no capital to exhaust and no actor to bribe, coerce, or out-wait. Its failure mode is different: it fails only if someone *adds* liquidity below the floor.

## Constructing one on Uniswap

On a V3/V4 pool, price moves by crossing [ticks](/wiki/economics/finance/defi/uniswap/ticks). If no position covers any tick below some boundary `T`, then [V4's swap math](/wiki/economics/finance/defi/uniswap) cannot push price below `T` — there is no liquidity for a seller to consume there, so the swap reverts or partially fills at `T`.

The clean construction:

1. Seat the entire token supply as a [single-tick position](/wiki/economics/finance/defi/uniswap/single-tick-liquidity) at the floor tick, single-sided.
2. Add liquidity *nowhere else* — in particular, nothing below the floor tick.

Buyers can push price up through the seeded tick (and beyond, if more liquidity exists above). Sellers can push price back down only to the floor tick, where the original liquidity sits, and no further.

## Making the floor credible

An absence floor is only as strong as the guarantee that liquidity will *stay* absent below it. Three things harden it:

- **Immutability.** The contract cannot be upgraded to add a lower position.
- **[Locked liquidity](/wiki/economics/finance/defi/locked-liquidity).** The seeded position cannot be moved down or withdrawn and re-seated lower.
- **No privileged actor.** No owner, hook, or governance can place liquidity below the floor on the protocol's behalf.

Anyone *else* is still free to open a pool below the floor — but they would be buying the token above its floor and selling below it, subsidizing holders. The floor is robust because breaking it is irrational, not because it is forbidden.

## Prior art

- **Single-sided launch designs.** Seeding a launch token entirely above a floor tick, with nothing below, is a recurring Uniswap V4 launch pattern.
- **Sell walls.** The order-book ancestor: a large resting bid (or, here, the absence of asks) at a price level.
- **Olympus Range-Bound Stability.** The instructive contrast — RBS bounded a token's price with *defended* liquidity walls operated by governance. Same goal (a bounded price), opposite method (capital and discretion vs. absence and immutability).

## Caveats

- **It is only a floor.** Absence below a tick says nothing about the ceiling. Bounding price on *both* sides requires also capping the upside — e.g. a [single-tick position](/wiki/economics/finance/defi/uniswap/single-tick-liquidity) that holds the entire supply, so there is nothing to buy past the top of the tick either.
- **Decimals and tick alignment matter.** The floor tick must be reachable and aligned to `tickSpacing`; an off-by-one here moves the floor by basis points.
- **A par token combines this with other techniques.** On its own a liquidity floor just prevents downside. See [par token](/wiki/economics/finance/defi/par-token) for the floor used as one half of a hard two-sided peg.

## External links

- [Uniswap — Range orders](https://docs.uniswap.org/concepts/protocol/range-orders)
- [OlympusDAO — Range-Bound Stability](https://docs.olympusdao.finance/main/overview/range-bound) — the defended-wall contrast
