---
title: "Wash Trading"
weight: 35
---

Wash trading is trading with yourself. The same beneficial owner stands on both sides, so no ownership changes and no risk is transferred, but the trade settles and prints like any other. What it manufactures is the record — volume, a last-sale price, a floor, a position in a ranking — rather than a price the market has to sustain.

A [pump and dump](/wiki/economics/finance/fraud/pump-and-dump) needs someone else to buy; wash trading needs someone else to read. Its victims are downstream of the record: the bidder who checks a floor price, the listing committee ranking venues by volume, the market maker allocating inventory to the busiest book, and the protocol distributing tokens in proportion to volume traded. Each is making a decision off a number that the person on both sides of the trade produced on purpose. The same self-dealing turns up as one stage inside larger schemes, where it manufactures the price history a [pump](/wiki/economics/finance/fraud/pump-and-dump) is then sold into.

## One owner, both sides

The trade itself is real. Two wallets, one owner: wallet A sells to wallet B, and both the asset and the money genuinely move. Settlement is honest and the economics are void, since the owner's net position is unchanged except for whatever the venue took. That fee is the only brake on the practice, and any venue that pays for volume is setting the other side of the comparison itself.

## Marketplaces that paid for volume

Selling a [non-fungible token](/wiki/economics/finance/defi/nft) (NFT) back and forth between two wallets under one owner, at escalating prices, writes a last-sale price into the token's history and, if the collection is thin, sets its floor. An [ERC-721](/wiki/economics/finance/defi/ethereum/erc-721) transfer is indifferent to who controls the destination, and the marketplace records whatever price was paid.

LooksRare, which launched in January 2022 as a competitor to OpenSea, added a subsidy on top: trading rewards emitted in its own token to both the buyer and the seller, allocated by share of daily volume. Reported volume immediately exceeded OpenSea's, and analysts including CryptoSlam and Nansen attributed the majority of it to wallets trading with themselves.

```text
One round trip: wallet A sells to wallet B, same owner.
Nothing changes hands.

  sale price                            100.00 ETH
  marketplace fee, 2% of the sale        -2.00
  creator royalty, 0% collection          0.00
  gas, both sides                        -0.02
  ----------------------------------------------
  cost of the round trip                  2.02 ETH

  volume credited                       200.00 ETH
    100 to the seller, 100 to the buyer — both earn

  break-even reward rate
    2.02 / 200 = 1.01% of credited volume,
    paid in the platform token

Profitable while  reward value > fee + royalty + gas.
A 10% creator royalty moves break-even to 6.01% and ends it.
```

Below that break-even line the behaviour is merely deceptive; above it, it is the highest-return trade on the platform and requires no view about any asset. Wash traders therefore concentrated on expensive items in collections charging no creator royalty, since a royalty is a pure loss on a trade that goes nowhere.

Emissions were a fixed daily quantity split pro rata, so each new wash trader diluted the rest, and volume expanded until the reward rate fell toward the round-trip cost. The subsidy was denominated in a token whose price responded to the reported volume it was inflating, which is a loop rather than a market.

## Exchange volume

Unregulated venues report volume to aggregators, and volume determines ranking, which determines listings, market-maker attention and user acquisition. The number is self-reported and unaudited.

In March 2019 Bitwise Asset Management filed an analysis with the Securities and Exchange Commission (SEC) in support of a bitcoin exchange-traded fund proposal, concluding that roughly 95% of reported bitcoin spot volume across the 81 exchanges it surveyed was fake or non-economic, and that about $273 million a day of real volume sat on ten venues. *Crypto Wash Trading*, by Lin William Cong, Xi Li, Ke Tang and Yang Yang, circulated as a National Bureau of Economic Research working paper and published in Management Science, put wash trading at roughly 70% of reported volume on the unregulated exchanges in its sample, against near zero on regulated ones.

The transferable part of that work is the statistics, which need only a trade tape and no wallet-level data:

- **Leading digits.** The first significant digits of genuine trade sizes track Benford's law closely, because real sizes span orders of magnitude. Sizes drawn from a script's uniform random generator do not.
- **Round-number clustering.** Humans trade 1.0, 0.5 and 0.25 units far more often than 0.9137. Fabricated flow either lacks that clustering entirely or, when the operator has thought about it, overshoots.
- **Tail shape.** Real trade-size distributions have a heavy power-law tail produced by the occasional very large order. Fabricated ones are usually truncated, because the operator sizes trades against a fixed inventory.

These tests identify the fabrication rather than the fabricator, and work on any venue that publishes a tape. An exchange reporting volume it does not have is frequently the same exchange reporting reserves it does not have; see [exchange collapse](/wiki/economics/finance/fraud/exchange-collapse).

## Self-trading on-chain

Swapping back and forth on a [decentralized exchange](/wiki/economics/finance/defi/dex) generates volume for a points program or an expected airdrop. Price impact does not cost anything on a round trip, because the second swap unwinds the displacement of the first, so the cost is the fee twice: 0.60% of notional on a 0.30% pool, plus gas. Fifty round trips of $10,000 credit $1 million of volume and cost about $3,000 in fees. If the trader is also the pool's only liquidity provider, that fee accrues to their own position and the real cost falls to gas alone.

Where the line sits is a question about the counterparty. An arbitrageur buying on one venue and selling on another moves inventory and closes a real price gap. A market maker quotes both sides and carries genuine risk against strangers. A searcher extracting [maximal extractable value](/wiki/economics/finance/defi/maximal-extractable-value) is adversarial toward other traders but is trading with them. Wash trading has no third party at all, so nothing is transferred and no price is discovered — which is also the legal test, phrased as whether beneficial ownership and market risk changed hands.

## Detection

On-chain the analysis is a graph problem, and unusually tractable for a fraud:

1. **Build the transfer graph** for the asset and look for closed loops — value returning to an address it left, directly or through two or three hops.
2. **Trace funding to first inbound transfer.** A shared funder behind both sides of a trade is the strongest single signal available.
3. **Check timing.** Near-constant intervals between trades, or trades that consistently occupy the same position within a block, indicate one script rather than two traders.
4. **Check the economics.** Round trips that lose money on fees while producing no change in inventory have to be paid for by something, and that something is the motive.

What this gets you is a cluster of addresses that behave as one. What it does not get you is a person. A common funding source is equally consistent with one owner, a custodian paying gas for its users, an exchange hot wallet, or a bot service that funds client wallets. The step from cluster to identity requires off-chain records, and it is where analytics firms both earn their fees and make their public mistakes.

## Where the law lands

Section 4c(a) of the Commodity Exchange Act prohibits wash sales, but by its terms it reaches transactions in futures or on or subject to the rules of a registered entity, not spot trades on an unregistered venue. The wider hook is Section 6(c)(1) of the same Act with Commodity Futures Trading Commission (CFTC) Rule 180.1, which reach manipulative or deceptive devices in connection with a sale of any commodity in interstate commerce, spot included.

In March 2021 the CFTC settled with Coinbase for $6.5 million over, among other things, self-matched trades between two accounts the company itself controlled that were reported as genuine volume, and separately a former employee's wash trading in litecoin. Coinbase neither admitted nor denied the findings. In October 2024 the Department of Justice and the FBI charged several market-making firms, Gotbit among them, following an operation in which the FBI deployed its own token, NexFundAI, and recorded firms offering to wash-trade it and to run coordinated buying alongside. Several defendants later pleaded guilty. The counts were fraud and conspiracy rather than wash-sale counts, which is the recurring pattern: the deception gets charged, not the self-dealing as such.

For an NFT, or a token that is neither a security nor traded on a registered venue, there may be no specific prohibition at all. What remains is fraud, which requires that somebody relied on the fabricated record and lost money. Absent that, the record is a false number with no offence attached to it, and the venue that paid for it has a different problem from the trader who supplied it. Section 1091 of the Internal Revenue Code carries the same name and none of the same content: it disallows a loss where a position in stock or securities is repurchased within 30 days, and reaches neither digital assets nor manufactured volume. Agency jurisdiction is mapped in [US regulatory restrictions on DeFi](/wiki/economics/finance/defi/defi-us-regulatory-restrictions).

## External links

- [CFTC press releases](https://www.cftc.gov/PressRoom/PressReleases) — the March 2021 Coinbase order and subsequent spot-market actions
- [Justice Department, District of Massachusetts press releases](https://www.justice.gov/usao-ma/pr) — the October 2024 market-maker charges arising from the NexFundAI operation
- [SEC comment file for the 2019 Bitwise bitcoin fund filing](https://www.sec.gov/comments/sr-nysearca-2019-01/srnysearca201901.htm) — contains the analysis of fake bitcoin spot volume and the exchange-by-exchange method
- [Chainalysis blog](https://www.chainalysis.com/blog/) — periodic measurements of NFT wash trading and self-funded wallet clusters
