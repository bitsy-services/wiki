---
title: "Full-Reserve Backing"
weight: 88
---

Full-reserve backing means every unit of an issued instrument is backed one-for-one by the **real underlying asset** held in reserve — not by different collateral, not fractionally, not by an algorithm. The reserve is the same asset the instrument represents. It is the oldest idea in monetary engineering, and it predates DeFi by centuries.

## Full reserve vs. the alternatives

| Model | Backing | Fails when |
|---|---|---|
| Full reserve | 100% of the *same* asset | reserve custody is compromised |
| Fractional | Part reserve, part assumption that not everyone redeems at once | redemptions exceed the fraction (a run) |
| Over-collateralized synthetic | A *different* asset worth >100%, oracle-priced | the collateral crashes or the oracle lies |
| Algorithmic | A mechanism and a reflexive belief | belief evaporates |

Full reserve is the only model with no insolvency mode of its own. Its single failure surface is custody of the reserve. Everything else trades that simplicity for capital efficiency or yield — and inherits a run, a liquidation cascade, or a death spiral in exchange.

## The currency-board lineage

The traditional-finance archetype is the **currency board**: a monetary authority that issues local currency only against 100% reserves of an anchor currency, at a fixed rate, with *no discretionary policy* — no lender of last resort, no rate setting, just a rule. Hong Kong's dollar is the canonical example. The point of a currency board is precisely that there is nothing to trust except the reserve and the rule; the issuer cannot inflate, cannot intervene, cannot change its mind.

The same shape recurs in **bearer instruments**: a banknote, a gold or silver certificate, a cashier's check, **scrip**, a traveler's cheque. Each is a claim that holds its face value because it is fully prefunded — the issuer parked the real asset before the instrument circulated. The issuer's economics are not the principal (which it cannot touch) but the **float**: the time value of prefunded reserves held while the instrument is outstanding. American Express's traveler's-cheque business was never the cheque; it was the float on billions in interest-free prepaid funds.

This is the cleanest mental model for a fully-reserved on-chain instrument: *a gold certificate where the gold is an [ERC-20](/wiki/economics/finance/defi/ethereum/erc-20) and the vault is a [locked liquidity](/wiki/economics/finance/defi/locked-liquidity) position no one can open.*

## On-chain

Fully-collateralized wrappers and reserve-backed stablecoins are the DeFi instances — but most pair full reserve with a **redemption desk**: burn the instrument, the contract releases the reserve at exactly 1:1. A [par token](/wiki/economics/finance/defi/par-token) is the variant *without* a desk: the reserve is the originals that accumulate in a [single-tick](/wiki/economics/finance/defi/uniswap/single-tick-liquidity) position as buyers swap in, and you recover the asset by selling back through that same position at no worse than par — not by presenting a claim for redemption.

## Caveats

- **Backing is not redemption.** "Fully reserved" describes *how much* of *what* sits behind the instrument. It says nothing about *how* — or whether — a holder can get the asset back. A reserve with no withdrawal path is still a full reserve; it just is not a redemption desk. Conflating the two is the most common error (it is also why "[wrapped](/wiki/economics/finance/defi/transfer-on-join-exit-vs-mint-burn)" is the wrong word for a deskless instrument).
- **Custody is the whole risk surface.** Full reserve removes every insolvency mode *except* loss of the reserve. Where the reserve sits — a multisig, an externally owned account (EOA), an immutable locked position — is the entire security analysis.
- **No yield to the holder, by construction.** The float accrues to whoever holds the fee/principal float, not to the holder of the instrument. A fully-reserved instrument that paid the holder yield would have to put the reserve to work, which is exactly what makes a reserve fractional.

## External links

- [Currency board](https://en.wikipedia.org/wiki/Currency_board) — the full-reserve, rule-based monetary archetype
- [Gold certificate](https://en.wikipedia.org/wiki/Gold_certificate) — a fully-reserved bearer claim
- [Scrip](https://en.wikipedia.org/wiki/Scrip) — privately-issued par-value money substitute
