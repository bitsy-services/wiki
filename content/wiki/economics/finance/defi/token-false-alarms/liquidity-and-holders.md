---
title: "Liquidity and Holders"
weight: 30
---

The heuristics that do not read code read four things: whether liquidity is locked, how concentrated the supply is, what else the deployer has deployed, and what the token's counterparties have touched. All four are presented as analysis of on-chain state. Three of them are lookups against a curated list, and the fourth is a threshold somebody picked. Nothing written in the token contract changes any of the answers.

## A lock is a name on a list

GoPlus states the rule without hedging: "About 'locked': We only support the token lock addresses or black hole addresses that we have included." A custom timelock, a Safe with a delay module, or a locker the vendor has not integrated reads as unlocked — not as unknown.

The list is short and the per-chain coverage is shorter. GoPlus names sixteen lockers and marks nine of them on Ethereum mainnet. Optimism recognises two. Linea, Scroll, zkSync Era and Mantle recognise one each. Fifteen chains — Tron, World Chain, Berachain, Sonic, Story, Soneium, Zircuit and others — recognise none at all, which leaves burning to a dead address as the only lock a scanner will see. On six further chains, including Unichain and Monad, the sole recognised locker is GoPlus's own product.

TokenSniffer's list is different, also per-chain, and also thin: Ethereum recognises Team Finance, UNCX, Unilocker, PinkLock, OnlyMoons and GemPad; Arbitrum recognises three; Fantom recognises one; and Optimism, Blast, Gnosis, Harmony, KuCoin Community Chain and Oasis are marked "Coming soon", so on six of its fifteen supported chains no lock can satisfy its ninety-five-percent test. Quick Intel names twelve lock providers and cannot keep the list consistent between two pages of its own documentation — one copy ends in ApexPad and the other omits it.

None of the three publishes a way to check in advance. GoPlus's locker endpoints document their response fields and name no locker brand anywhere, so a deployer choosing a locker is choosing blind unless they read the vendor's separate support table and hope it is current.

The practical consequence is that "locked" is a claim about your vendor relationships. [Locked liquidity](/wiki/economics/finance/defi/locked-liquidity) is a property of the position; being *seen* as locked is a property of the locker's address being in a table.

## Concentrated liquidity has no top holders

"Top ten [LP](/wiki/economics/finance/defi/liquidity-pool) holders" is a well-defined quantity in Uniswap V2, where the pair contract *is* a fungible token, and undefined afterwards.

Two details of V2 matter for anyone writing a burn heuristic. First, there is no way to destroy LP tokens without redeeming the underlying: `UniswapV2Pair.burn` redeems, and `UniswapV2ERC20._transfer` performs no recipient validation, so "burning the LP" means transferring it to a dead address and leaves `totalSupply` untouched. Second, every V2 pool holds LP tokens at the zero address by construction — `_mint(address(0), MINIMUM_LIQUIDITY)` with `MINIMUM_LIQUIDITY` set to 1000 — so a nonzero zero-address balance is the universal baseline rather than evidence of a burn, and any "percentage burned" calculation must subtract it.

V3 replaces all of this with an [NFT](/wiki/economics/finance/defi/nft). Liquidity is an [ERC-721](/wiki/economics/finance/defi/ethereum/erc-721) minted by the `NonfungiblePositionManager`, fees accrue inside it, and there is no fungible balance to rank. `burn` reverts unless the position is already empty (`require(position.liquidity == 0 && position.tokensOwed0 == 0 && position.tokensOwed1 == 0, 'Not cleared')`), so live liquidity cannot be burned away at all — the position NFT has to be sent somewhere. Lockers adapted by escrowing the NFT: UNCX's V3 locker takes custody and revokes the owner's ability to move it between a start and an end date, while leaving fee collection available, which is the [fee-only ownership](/wiki/economics/finance/defi/locked-liquidity#fee-only-ownership) shape.

An escrowed position is not automatically a meaningful one. OpenZeppelin's January 2024 audit of that locker found a high-severity issue where a position with `tickLower` at `-maxTick` and `tickUpper` at zero passed the full-range validation, and a critical one where the conversion to full range could be sandwiched. Both were fixed before publication. The residual point stands regardless of those fixes: a locked V3 position can be narrow enough to sit outside the current price and hold nothing useful, and "locked" says nothing about the range.

V4 is worse for anyone indexing it. `BURN_POSITION` withdraws rather than destroys — its own dispatcher comment says it "will automatically decrease liquidity to 0 if the position is not already empty" — so there is no burn analogue at all. `PositionManager` does not implement `ERC721Enumerable`, so `tokenOfOwnerByIndex` is unavailable and position discovery requires a subgraph. And the NFT is a periphery convention, not a protocol requirement: any contract can call `PoolManager.modifyLiquidity` directly with its own salt and hold liquidity with no token and no periphery involvement, invisible to every locker, scanner and indexer that equates V4 liquidity with a `PositionManager` id.

The scanners have caught up unevenly, and in a direction opposite to the usual assumption. GoPlus documents `NFT_list` only when `liquidity_type` is `UniV3`, carrying each position's `NFT_id`, `amount` and an `in_effect` flag for whether it is live at the current price — so **V4 is the blind spot, not V3**; a V4 pool gets a bare `pool_manager` address and no position breakdown. TokenSniffer covers V3 pools on seven chains but reports them through a schema denominated in fungible LP tokens throughout, and lists no V4 support. Quick Intel says twice that it does not detect V3 LP burns at all.

## Thresholds somebody picked

TokenSniffer publishes its numbers, which is more than most, and they are absolutes:

| Test | Fails at |
| --- | --- |
| `testForHighCreatorTokenBalance` | creator holds 5% or more of supply |
| `testForHighOwnerTokenBalance` | owner holds 5% or more of supply |
| `testForHighWalletTokenBalance` | any other wallet holds 5% or more |
| `testForInadeqateLiquidityLockedOrBurned` | under 95% of liquidity locked or burned |
| `testForHighCreatorLPBalance` | creator holds 5% or more of the liquidity |

A vesting contract is a wallet. A treasury is a wallet. A staking contract holding deposits is a wallet. TokenSniffer publishes an `is_contract` flag on each of the top twenty holders and never says whether that flag feeds the concentration tests, so the treatment of a vesting schedule cannot be predicted from the documentation. It does special-case burn, locker, deployer and owner addresses as separate balances, which makes the silence about staking, bridge and exchange contracts a gap rather than an oversight.

The score these feed is also not always computed from them: "The score is always set to 0 for scam tokens (`is_flagged=true`)", where `is_flagged` is set "automatically or by a moderator". A human decision overrides all twenty-six tests, and the band boundaries — `low` at 85 or above, `medium` at 60 or above, `high` below 60 — apply to whatever comes out.

RugCheck, on Solana, publishes fixed point weights that make the arithmetic legible: mint authority still enabled costs 50,000 points, freeze authority 25,000, mutable metadata 100, and single-holder ownership costs the holder's basis points. Read on 2026-08-31, that produces:

| Token | Score | Driven by |
| --- | --- | --- |
| RENDER | 76 | mint authority and freeze authority enabled |
| mSOL | 71 | mint authority enabled |
| JTO | 30 | single holder at 21.25% |
| BONK, JUP, PYTH, W | 7 | mutable metadata alone |
| USDC | 1 | nothing |

mSOL retains mint authority because a liquid staking token must mint against deposits; without it the product does not work. USDC has the same two properties set on chain and scores 1, an exemption covered under [allowlists](/wiki/economics/finance/defi/token-false-alarms/allowlists#membership-does-not-suppress-the-findings).

The liquidity threshold fails the same way. RugCheck's own `lpLockedPct` on 2026-08-31 read under 25% for BONK and under 2% for JUP, PYTH, Wormhole, RENDER and mSOL — and exactly zero for USDC, which it scores at 1. Any consumer rule of the form "require N% of liquidity locked" is stricter than the scanner supplying the number, and fails almost every established token.

## Deployer history

`honeypot_with_same_creator` is a count — "the number of honeypot tokens created by this creator" — documented in the endpoint's schema reference and absent from the field documentation. On 2026-08-31 it returned `1` for Paxos Gold, for wstETH, for 1INCH, and for a Yearn V3 vault. For PAXG it is the *only* positive signal in the response, because everything else is suppressed by the proxy. No threshold is published, the response names no honeypot, and nothing distinguishes a serial scammer from a launchpad with one bad token among thousands.

The heuristic is not baseless, which is what makes it hard to argue with. Cernera and co-authors, measuring Ethereum and BNB Chain deployments for USENIX Security 2023, found roughly 60% of tokens active for under twenty-four hours, 1% of addresses creating 20–25% of all tokens, and one-day rug pulls generating $240 million. Deployer identity really does carry signal. It simply carries no defence: the property belongs to the address that sent the creation transaction, so the only lever is which address deploys, and using a fresh one for every launch is also what the population being modelled does.

GoPlus scores addresses directly too, through a separate endpoint with `mixer`, `sanctioned`, `money_laundering`, `blacklist_doubt`, `honeypot_related_address` and `number_of_malicious_contracts_created`. The `mixer` note contains its own warning about contagion: "Interacting with coin mixer may result in your address being added to the risk list of third-party institutions."

## The compliance sibling

The same guilt-by-association logic runs on addresses at far higher stakes, and the vendors describe the mechanism candidly. Chainalysis defines indirect exposure as reaching origins and destinations "no matter how many intermediary non-service addresses — or 'hops,' as they're colloquially known — are in between", stopping at services. TRM Labs names that stopping point as the source of the errors: exchange deposit addresses are omnibus, so "incorrectly tracing through a service risks generating false positives — potentially flagging legitimate customers based on phantom risk paths."

Nobody will tell you where the line is, because there is no line. TRM: "No regulatory body has set a universal hop threshold", and [OFAC](/wiki/economics/finance/regulation/ofac-sanctions) "has not defined a de minimis level". Elliptic argues hop count "is not a strong indicator of risk" at all, since anyone can create millions of wallets in seconds, and in March 2026 went further: "Legitimate users frequently have indirect exposure to services that may be considered high risk, such as mixers, DEXs or privacy protocols", which "can require contextual review rather than automatic escalation" — a decentralized exchange having become, by then, an ordinary destination for ordinary funds.

The tuning pressure runs one way. TRM's own page names the reason: New York's financial regulator's enforcement action against Block "demonstrated that setting internal thresholds too high — even 1% exposure to terrorism-linked wallets — can constitute a regulatory violation." An integrator that over-blocks annoys customers; one that under-blocks faces [anti-money-laundering](/wiki/economics/finance/regulation/anti-money-laundering) enforcement.

August 2022 supplied the worked example. After Tornado Cash was designated, a sender — Decrypt characterises them as a troll rather than an attacker — dusted hundreds of public wallets, including those of Jimmy Fallon, Brian Armstrong, Logan Paul, Beeple, Steve Aoki and the Ukraine donation address. Chainalysis put the total at about $52,000 in small payments and noted the recipients "have control of assets with exposure to Tornado Cash, which could have downstream compliance impacts." Aave, Uniswap, Balancer, Ren and Oasis front-ends blocked addresses through TRM's screening API; Justin Sun was locked out of Aave's interface while holding roughly $100 million in aTokens. dYdX said the quiet part in a blog post: it had unbanned certain accounts because "This sudden influx of flags affected many account holders that never directly engaged with Tornado Cash", while keeping restrictions in place.

Two things follow for anyone on the receiving end. Nobody can prevent it — Chainalysis states that "it is impossible to block incoming transactions regardless of custodial status, users remain vulnerable to dusting attacks" — and there is no door to knock on. Neither Chainalysis nor TRM publishes an address-label dispute process for an outside party. Chainalysis's data-quality page describes validation running outward through seized datasets, subpoena corroboration and court testing, and never inward. The one formal lever is a data-protection rectification request, with a thirty-day response commitment, whose listed categories of personal data do not mention wallet addresses at all. The venue that screened you is the only party with a working door, and Kraken is one of the few to publish a restriction-specific form for it.

One coda on staleness, since heuristics outlive their inputs: Tornado Cash was delisted by OFAC on 21 March 2025 following the Fifth Circuit's decision in *Van Loon v. Department of the Treasury*. Screening rules still written against the 2022 designation are flagging against a sanctions entry that no longer exists.

## External links

- [GoPlus supported lockers](https://docs.gopluslabs.io/reference/supported-locker) — the per-chain allowlist, with its own typos intact
- [TokenSniffer supported networks](https://tokensniffer.readme.io/reference/supported-networks) — which chains recognise which lockers
- [UNCX V3 liquidity locker audit](https://www.openzeppelin.com/news/uncx-uniswapv3-liquidity-locker-audit) — OpenZeppelin on what an escrowed position does and does not guarantee
- [Token Spammers, Rug Pulls, and SniperBots](https://arxiv.org/abs/2206.08202) — the measured base rate behind deployer-history scoring
- [Chainalysis on indirect exposure](https://www.chainalysis.com/blog/cryptocurrency-risk-blockchain-analysis-indirect-exposure/) — hops, services, and where traversal stops
- [TRM Labs on indirect risk](https://www.trmlabs.com/glossary/indirect-risk) — the same boundary described as a false-positive source
- [Elliptic on reducing false positives](https://www.elliptic.co/blog/how-to-reduce-aml-false-positives-in-crypto) — a screening vendor conceding that legitimate users have exposure
