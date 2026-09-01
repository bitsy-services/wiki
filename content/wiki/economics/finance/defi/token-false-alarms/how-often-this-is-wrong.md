---
title: "How Often This Is Wrong"
weight: 50
---

A detector vendor reports precision: of the alarms it raised, what share were correct. A deployer experiences the complementary quantity: given that my token is honest, what is the chance I get flagged. That is `1 − specificity`, and the two numbers are not the same. Precision is inflated by the base rate of scams in the population sampled; `1 − specificity` is untouched by it. Every published figure in this field is the first quantity, and nobody publishes the second.

## The arithmetic

Precision is `(p × sensitivity) / (p × sensitivity + (1 − p) × (1 − specificity))`, where `p` is prevalence. Sensitivity is the share of scams the detector catches and specificity the share of honest tokens it spares. Take a detector that is 95% on both and run it against the base rates people actually cite, per 10,000 tokens:

| Base rate of scams | True positives | False positives | Precision | P(flagged \| honest) |
| --- | --- | --- | --- | --- |
| 76.4% | 7,258 | 118 | 98.4% | 5.0% |
| 53.6% | 5,092 | 232 | 95.6% | 5.0% |
| 24.4% | 2,318 | 378 | 86.0% | 5.0% |
| 8.5% | 808 | 458 | 63.8% | 5.0% |
| 3.6% | 342 | 482 | 41.5% | 5.0% |

The last column does not move. A vendor can truthfully report 98% precision while one honest deployer in twenty is flagged, and can report it *because* the population is mostly scams rather than because the detector is good at sparing honest tokens.

The lever that would help a deployer is specificity, not the base rate. Holding prevalence at 3.6% and sensitivity at 95%, precision runs 41.5% at 95% specificity, 78.0% at 99%, and 97.3% at 99.9%. Moving specificity from 95% to 99.9% cuts the honest deployer's exposure by a factor of fifty. Nothing published tells you where any vendor sits on that axis.

## "The base rate" is at least four numbers

Every figure below is real and measured. They disagree by a factor of twenty because they sample different populations and define "scam" differently.

**Chainalysis, 2023, Ethereum.** Just over 370,000 tokens launched, about 168,600 tradeable on a [DEX](/wiki/economics/finance/defi/dex). Roughly 90,400 met its criteria — 24.4% of all launches, 53.6% of the DEX-listed subset. The criteria were three prongs: purchased five or more times by users unconnected to the biggest holders, more than 70% of pool liquidity removed by a single address, and current liquidity of $300 or less. Chainalysis disclaims the reading everyone takes from it: "This methodology does not mean these tokens were the subjects of pump and dump schemes."

**Chainalysis, 2024, all chains.** 2,063,519 tokens launched, 873,957 DEX-listed, 74,037 showing possible [pump-and-dump](/wiki/economics/finance/fraud/pump-and-dump) patterns — 3.59% of launches, 8.5% of DEX-listed. Every threshold changed between the two reports: 70% became 65%, the $300 liquidity prong became an inactive pool, the five-purchaser prong became more than 100 pool transactions, and the population went from Ethereum to all chains. **24.4% and 3.59% are not comparable numbers**, and treating the drop as a trend is a mistake the reports themselves do not make.

**Solana, first half of 2025.** Chen and co-authors labelled 100,063 newly issued tokens across Orca, Raydium and Meteora and marked 76,469 — 76.4% — as [rug-pull](/wiki/economics/finance/fraud/rug-pull) candidates. They call it a lower bound: the observation window is twenty-four hours, and they chose their threshold as "the largest value that still admits gradual variants".

**Pump.fun.** Solana Compass, citing The Block's on-chain tracker in June 2026: "fewer than 2% of all Pump.fun tokens have ever graduated from the platform's bonding curve to a decentralized exchange", against 11.9 million cumulative launches.

Chainalysis's 2023 criteria caught 53.6% of DEX-listed Ethereum tokens, and those tokens were **1.3% of Ethereum DEX trade volume**. The population where scam prevalence is highest is almost exactly the population nobody trades. A scanner's base rate and its relevance to a real user are close to inversely related, which is why an argument that starts "most new tokens are scams" and ends "so the detector is well calibrated for you" does not follow.

The criteria also catch honest failure. An honest launch that did not work, whose founder later withdrew the pool, satisfies the 2023 prongs. Chainalysis says as much about the population: "There are many reasons that could explain the failure to reach more liquid trading volumes." Only 5.7% of 2023 Ethereum launches held more than $300 of DEX liquidity at the time of measurement, so the criteria are separating a small live cohort from a very large dead one, and dead is not the same as fraudulent.

## What the academic detectors actually measured

Four papers get cited as evidence that detection works. Each reports a number that is narrower than the citation implies.

**HoneyBadger** (Torres et al., USENIX Security 2019) scanned 151,935 unique bytecodes and found 460 [honeypots](/wiki/economics/finance/fraud/honeypot-token) — a prevalence of 0.30%. Its headline 87.3% precision is 282 true positives against 41 false positives over 323 contracts, and those 323 are the roughly 70% of flagged contracts whose source Etherscan carried. That is a source-availability subsample, not a random one, and verified honeypots are disproportionately likely to be source-verified. Its per-heuristic table also reports several 100% precisions on denominators of 4, 9 and 12.

**Xia et al.** (2021) reported that 50.14% of tokens on Uniswap were scams. About two-thirds of that count is inferred rather than labelled: 4,048 tokens from ground-truth labelling, 3,122 from guilt-by-association expansion, 3,750 from classifier expansion. Its classifier's 96.45% precision comes from a protocol described as taking one of ten groups as the training set and the remaining nine as the test set — training on 10% and testing on 90% — scored against labels its own expansion partly generated. The paper also had to hand-exclude seven addresses "tagged by Etherscan as Contract Deployer" from the expansion, footnoting that a shared deployer "can be used by different users to create contracts with similar functionality" — which is precisely how an honest token launched through a shared factory inherits a scam label.

**CRPWarner** (*IEEE Transactions on Software Engineering*, 2024) is the most instructive, and the instruction is the opposite of what its numbers suggest. On 13,484 real Ethereum contracts it flagged 4,168 — 30.9% — at 84.9% precision. That precision is a sample statistic: 272 flagged contracts audited at a stated 95% confidence level and a 10% confidence interval, which is far too wide to support any point estimate of how many were wrong. More importantly, CRPWarner detects over-privileged *functions*, not rug pulls. A true positive means a hidden mint, sell limit or token-leaking function genuinely exists. The paper reads its own 30.9% as evidence that "the developers of these smart contracts have bestowed overpowering permissions". So a legitimate upgradeable, pausable or fee-bearing token counts as a **true positive** — the honest-project overcounting lives inside the 84.9%, not the 15.1%.

**A 2026 preprint** on rug-pull detection makes the methodological argument directly: "Leakage—using post-event data in training—produces non-causal models with misleadingly high accuracy." Its own reported figures are internally inconsistent and its 200-token test set has a 59% base rate, so it is worth reading for the argument rather than the numbers.

The Solana paper is the one that audited both directions, and quoting half of it is the common error. Its labelling false-positive rate is 0.26% with a 95% upper bound of 1.45%, from a stratified sample of 382 candidates. The complementary sample of 100 *non*-flagged tokens found nine confirmed missed rug pulls, "all of which unfold over three to seven days and therefore fall outside the 24-hour observation window". The paper explicitly declines to have those read as detection performance: "We report these numbers as dataset quality indicators under our conservative labeling strategy, rather than as detection performance."

What makes the separation easy there is worth stating, because it also explains when it fails. Rug-pull tokens in that dataset had a mean lifespan of 1.03 days, 83 holders and 4.17 transactions; legitimate ones averaged 416 days, 215,952 holders and 184,802 transactions. Those gaps are enormous, and a slow, quiet, honest launch sits in the middle of them.

## The vendors publish counters, not error rates

Blockaid's homepage carries four figures — 5.9 billion transactions scanned, $312 billion in assets secured, 527 million attacks prevented, $13.1 billion in theft prevented — and no false-positive rate, no flagged share and no monthly volume. Its dapp-scanning page adds 1.6 million malicious dapps blocked monthly and 75 million domains scanned; grepping the rendered page for "false positive", "accuracy" and "precision" returns nothing. The one figure it has published is from an April 2024 post and is stated as a bound: "All with less than 0.0002% being false positives." Press coverage converted that bound into a point estimate, and the unit is the problem regardless of the denominator.

That figure also cannot bound what a deployer cares about. A per-request rate says nothing about per-project harm, because a wrongly flagged dapp generates one false positive *per request it serves* — a thousand requests, a thousand false positives. One flagged project with modest traffic can account for an entire vendor's monthly false-positive budget, and a busy one exceeds it by orders of magnitude. Per-request and per-project error rates are different quantities, and no vendor publishes the second.

Blockaid has, to its credit, defended the tradeoff in public rather than denying it: "The statistical nature of these systems means that we have to work towards striking a balance: zero false positives inevitably means that malicious transactions will get through."

TokenSniffer is the only scanner that publishes a self-measured rate — "Our measured false-positive rate is <1%" — alongside a `/corrections` endpoint listing tokens un-flagged in the last twenty-four hours, whose documented sample response shows 36 for one window. It states no denominator, window or method, so it is a vendor self-report rather than a measurement. Kerberus publishes "99.9%" and "zero user losses since launch" and no error rate at all.

The asymmetry has an incentive behind it and it is not sinister. A false negative costs a wallet vendor a drained user, press coverage and possibly liability. A false positive costs it a complaining deployer with no contractual relationship. There is no reason to expect the second number to be published, and it is not.

## The one public denominator

One vendor happens to run its appeals in public, which makes it the only place in this landscape with a countable population of false alarms. MetaMask's `eth-phishing-detect` repository, read on 2026-08-31:

| Measure | Value |
| --- | --- |
| Issues titled "[Legitimate Site Blocked]" | 7,699 of 15,776 issues (48.8%) |
| Issues labelled "blocklist removal" | 4,911 |
| Open right now | 1 |
| Median time from open to close (400 recent) | 36 hours |
| Interquartile range | 11 to 74 hours |
| Closed within a week | 96.2% |
| Closed as `completed` | 44.5% |

Half of all issue traffic on the repository is people saying "you blocked my legitimate site". That is the closest thing to a measured false-alarm volume anywhere in this field, and it exists only because the list is a public Git repository rather than a vendor endpoint.

The turnaround numbers cut the other way from the usual complaint, and the honest reading is that this particular channel works. The median request is closed in a day and a half, rejection is no slower than acceptance, and the entire repository had five open issues — the oldest three days old, all four of the non-newest waiting on the *requester* for more information. Cross-checking the domains in 400 closed issues against the live blocklist, 72 of 74 closed as `completed` are genuinely gone from it.

The tail is where the cost sits. PancakeSwap's domain took roughly twenty months to clear, in what looks like a backlog sweep rather than a response; a Binance domain took 8.5 months in 2018. And clearing is not permanent: `opensea.org` was unblocked in January 2023 after seven months and is on the blocklist again today.

| Project | Domain | Elapsed |
| --- | --- | --- |
| Superfluid | `arbitrum-one.rpc.x.superfluid.dev` | 2.5 hours |
| Coinbase | `cb-w.com` | 6.4 hours |
| Hop Protocol | `optimism-fee-refund-api.hop.exchange` | 10.8 hours |
| Balancer | `docs.balancer.fi` | 21 hours |
| PancakeSwap | `pancakeswap.finance` | ~20 months |

Balancer's was a cluster — six issues from six different reporters inside twenty-four hours across `app.balancer.fi`, `docs.balancer.fi` and `balancer.fi` — which is what a real project's users do when the wallet in front of them says the site might be harmful.

## What to take from the numbers

The scanners are not indiscriminate. A plain fixed-supply token with no admin surface comes back clean, as four of the ten ordinary tokens in the [overview measurement](/wiki/economics/finance/defi/token-false-alarms#the-measurement) did. The base rates are real, the deployer-history heuristics have genuine signal behind them, and a positive honeypot simulation is close to dispositive.

What the numbers do not support is the inference a deployer keeps meeting: that a high base rate makes a flag informative about *their* token. It does the opposite. The higher the prevalence in the sampled population, the better a mediocre detector's precision looks, and the less any individual alarm tells you — because the population being described is the one that launched and died within a day, and it is not the one you are in.

## External links

- [Chainalysis on pump and dump patterns, 2024](https://www.chainalysis.com/blog/crypto-crime-2024-pump-and-dump/) — the 2023 Ethereum criteria and the 1.3%-of-volume finding
- [Chainalysis market manipulation, 2025](https://www.chainalysis.com/blog/crypto-market-manipulation-wash-trading-pump-and-dump-2025/) — the 2024 all-chain figures, with every threshold changed
- [The Art of The Scam](https://www.usenix.org/conference/usenixsecurity19/presentation/ferreira) — HoneyBadger, and honeypot prevalence at 0.30%
- [Trade or Trick?](https://dl.acm.org/doi/10.1145/3491051) — Xia et al. on Uniswap scam tokens, and the deployer-expansion problem
- [CRPWarner](https://arxiv.org/abs/2403.01425) — over-privileged function detection, where legitimate tokens are true positives
- [From Hype to Collapse](https://arxiv.org/abs/2603.24625) — the Solana labelling study, audited in both directions
- [eth-phishing-detect issues](https://github.com/MetaMask/eth-phishing-detect/issues) — the only public appeal queue in the field
