---
title: "Locked Liquidity"
weight: 87
---

Locked liquidity is an [AMM](/wiki/economics/finance/defi/amm) position whose principal can never be withdrawn — not by its creator, not by anyone. It is the difference between "the team *promises* not to pull the pool" and "the pull function does not exist." A [liquidity floor](/wiki/economics/finance/defi/liquidity-floor) or a peg is only as credible as the guarantee that the backing stays put; locked liquidity is that guarantee made structural.

## Three ways to lock

- **Time-lock.** A locker contract holds the position and releases it after a deadline. Common for launches; only as good as "until the timer ends," and the cliff is a known risk date.
- **Burn.** Send the [LP](/wiki/economics/finance/defi/liquidity-pool) token (or V2 LP shares) to a dead address. Irreversible, but crude — you also burn the ability to ever collect fees, and V3/V4 positions are [NFTs](/wiki/economics/finance/defi/nft) with accrued fees, so burning is lossy.
- **No withdrawal path.** Own the position via a contract that simply never implements decrease-liquidity. Principal is unreachable because no code can reach it; fees remain collectable. This is the strongest and most precise form.

## Fee-only ownership

The refined pattern separates two rights that LP ownership normally bundles:

- **Authority over principal** — move ticks, decrease liquidity, withdraw, pause. *Removed entirely.*
- **The fee stream** — collect accrued swap fees. *Retained, and given to some party.*

A position held by a clone that exposes only "harvest fees, then withdraw the harvested fees" gives its owner an income claim with zero authority over the locked capital, ticks, or pause. The principal is not owned by anyone in any meaningful sense; only its exhaust is. This is exactly the Fountain primitive both Bitsy fair-launch factories build on.

## Why it matters

A floor or peg backed by withdrawable liquidity is not a floor — it is a floor *until the backer changes their mind*. Locking converts a behavioral promise into an invariant:

- A [liquidity floor](/wiki/economics/finance/defi/liquidity-floor) cannot be relocated lower if the position cannot be moved.
- [Full-reserve backing](/wiki/economics/finance/defi/full-reserve-backing) cannot be quietly drained if there is no drain.
- A [par token](/wiki/economics/finance/defi/par-token)'s reserves are credible precisely because the position holding them has no decrease path.

## Prior art

- **LP lockers** — UNCX/Unicrypt, team.finance: third-party time-lock and lock services for launch liquidity.
- **Burned LP launches** — the memecoin convention of sending LP to `0xdead` as a rug-proof signal.
- **Protocol-owned liquidity (POL)** — protocols holding their own LP so it cannot be yanked by mercenary capital, though POL is usually still governance-movable.

## Caveats

- **Locking is symmetric.** A position locked with bad parameters — wrong tick, wrong fee tier, wrong pair — is *also* permanent. Immutability removes the rug and the undo in one stroke. Get the parameters right before sealing.
- **"Locked" must mean the right thing.** A time-lock is not a no-path lock. Read which one a system actually uses; the security properties are not interchangeable.
- **Fees are not principal.** A retained fee claim is not authority over the backing. Conflating the two is the usual misreading.

## External links

- [Uniswap V4 — periphery & position management](https://github.com/Uniswap/v4-periphery)
- [EIP-1167 — Minimal Proxy Contract](https://eips.ethereum.org/EIPS/eip-1167) — the clone pattern fee-only ownership is usually built on
