---
title: "Rug Pull"
weight: 20
---

A rug pull is the removal, by the people who issued a token, of the value backing it. Nothing about the token breaks: balances stay where they are, transfers still succeed, and the explorer still reports the same total supply. What disappears is the other side of every trade — the [liquidity pool](/wiki/economics/finance/defi/liquidity-pool) holders would have sold into — and with it any price at which they can leave.

The mechanism follows from how a [decentralized exchange](/wiki/economics/finance/defi/dex) prices an asset rather than from a defect in any contract. A rug pull sits in the market-and-issuance group of [crypto fraud](/wiki/economics/finance/fraud) beside the [honeypot token](/wiki/economics/finance/fraud/honeypot-token), which blocks the exit inside the transfer function instead of draining the pool, and [hidden admin controls](/wiki/economics/finance/fraud/hidden-admin-controls), the general case of both.

## Why withdrawing the pool zeroes the exit

A pair holding `x` tokens against `y` units of a quote asset prices trades with the [constant product formula](/wiki/economics/finance/defi/constant-product-formula), `x * y = k`. Selling `dx` tokens into it returns:

```text
dy = y * dx / (x + dx)      ->  y   as dx -> infinity
```

The quote reserve `y` is a hard ceiling on what every holder combined can ever take out. Liquidity provider (LP) tokens are a proportional claim on both reserves, so a deployer who seeded the pool alone holds essentially the entire LP supply and redeems both sides in one transaction.

```text
before removal                        after removal
  reserves  1,000,000 TOKEN             reserves  100 TOKEN
                  200 ETH                            0.02 ETH
  k = 2.0e8                             k = 2.0
  mid price 0.0002 ETH/TOKEN            mid price 0.0002 ETH/TOKEN  (unchanged)
  LP supply 14,142, ~100% deployer      LP redeemed: 200 ETH + 999,900
                                        TOKEN out to the deployer

  sell 10,000 TOKEN -> 1.98 ETH         sell 10,000 TOKEN -> 0.0198 ETH
  holders can extract <= 200 ETH        holders can extract <= 0.02 ETH
```

A proportional withdrawal leaves the quoted mid price exactly where it was, because both reserves shrank by the same factor. Depth is what vanished. The first holder to sell any size walks the curve into dust reserves and takes 1% of what the same sale returned a block earlier, so the chart collapses on that trade rather than on the withdrawal.

## The taxonomy

**Hard rug.** The deployer redeems the LP position in one transaction and keeps the quote reserve. Burning the LP token does the opposite: it strands both reserves in the pair permanently, and is the lock rather than the rug. Where the pool is a Uniswap v3 or v4 position rather than a v2 pair, the position is an [NFT](/wiki/economics/finance/defi/nft) held by a position manager, so what matters is who owns that token rather than a balance.

**Sell-tax and blacklist rugs.** Rather than take the pool, the deployer changes the terms of leaving it: a transfer fee raised to 100%, a blacklist applied to holders, a global pause. The pool stays and withdrawals stop. These are owner-settable functions, covered on [hidden admin controls](/wiki/economics/finance/fraud/hidden-admin-controls); built in from the first block instead, the same restriction is a honeypot.

**Soft rug.** The team sells its own allocation through the curve over weeks and abandons the project. A locked pool does not prevent this: a treasury holding 30% of supply drains the quote reserve by selling like any other seller, and the lock guarantees only that the emptied pair contract remains. No single transaction is the offence, so it is charged, when it is charged, as securities or wire fraud resting on what was promised during the sale.

## What a liquidity lock guarantees

[Locked liquidity](/wiki/economics/finance/defi/locked-liquidity) puts the LP position where it cannot be pulled from: a locker contract with a release timestamp, a burn to a dead address, or a holder contract with no withdrawal path. Four standard defeats, in the order that costs holders the most:

- **Supply held outside the pool.** The lock is a statement about the pair, not about the token. A team wallet with 30–40% of supply takes the quote reserve out through the front door while every screenshot of the locker stays accurate.
- **Partial locks.** "Liquidity locked" names an amount only if it names the fraction; locking 20% of the LP supply satisfies the phrase and leaves 80% withdrawable.
- **Upgradeable code.** A locker behind a proxy, or a token behind a proxy, can be replaced after the lock is shown, and then enforces whatever it was swapped to.
- **Short terms.** The unlock timestamp is public, so a 30-day lock is a countdown to a known date.

## Cases

**Squid Game token, November 2021.** A token on BNB Chain marketed on the Netflix series, with no connection to it. The contract restricted who could sell, so most buyers had no exit while the price ran to a reported peak near $2,861. The developers then removed the liquidity, the price fell to approximately zero within minutes, and reported proceeds were roughly $3.3 million.

**AnubisDAO, October 2021.** A token launched on 28 October 2021 by an anonymous team, with a one-page site and no product, raising roughly 13,556 ETH — about $60 million at the time — through a liquidity bootstrapping sale. Around twenty hours later the pooled funds were moved to a new address and dispersed. No arrests have been reported.

## Checking before you buy

- **Find who can move the liquidity.** For a v2-style pair, read the holders of the pair's LP token; an externally owned account holding the majority can withdraw at any block. For a v3 or v4 position, read the owner of the position NFT.
- **Open the lock and read its terms.** A real lock names the locked amount, the LP token, and the unlock timestamp. Compare that amount against LP total supply.
- **Sum the token balances outside the pool.** A wallet above roughly 5% of supply can move the price with no admin function at all, and wallets funded by one address count as one wallet.
- **Confirm the source is verified, and read the transfer path.** Unverified bytecode on a token asking for money is a purchase made without information.
- **Treat renounced ownership as weak evidence.** It gives up `onlyOwner` on one contract and nothing else — [why renounced ownership is a weak signal](/wiki/economics/finance/fraud/hidden-admin-controls#why-renounced-ownership-is-a-weak-signal) has the three ways it fails.

## Where the law lands

United States enforcement reaches rug pulls through two theories rather than as theft, since the contract performed the transfers it was written to perform. The Securities and Exchange Commission (SEC) treats most token sales as investment contracts, making an unregistered sale a violation of the Securities Act whatever became of the money; [financial regulation](/wiki/economics/finance/regulation) covers that test. The Department of Justice (DOJ) charges the promises made during the sale as wire fraud, with money laundering on the proceeds. Frosties, an NFT mint that raised roughly $1.1 million in January 2022 and was abandoned immediately, drew exactly that pairing: prosecutors in the Southern District of New York charged Ethan Nguyen and Andre Llacuna in March 2022 with conspiracy to commit wire fraud and money laundering, and Nguyen pleaded guilty.

Both theories require identifying a pseudonymous deployer, so most rug pulls produce no case. One carried out by an identified operator who took custody first is closer to an [exit scam](/wiki/economics/finance/fraud/exit-scam); the structure shared across both is in [anatomy of a crypto scam](/wiki/economics/finance/fraud/anatomy-of-a-crypto-scam).

## External links

- [How Uniswap works](https://docs.uniswap.org/contracts/v2/concepts/protocol-overview/how-uniswap-works) — the pair mechanics that make a proportional withdrawal drain the exit
- [SEC press releases](https://www.sec.gov/newsroom/press-releases) — the enforcement record on unregistered token offerings
- [Justice Department news](https://www.justice.gov/news) — wire fraud and money laundering charges arising from token launches
- [FBI Internet Crime Complaint Center annual reports](https://www.ic3.gov/AnnualReport/Reports) — reported United States losses by fraud category
