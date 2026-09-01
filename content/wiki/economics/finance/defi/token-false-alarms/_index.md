---
title: "Token False Alarms"
weight: 75
bookCollapseSection: true
---

A false alarm is a security surface telling a user something adverse about a token that is behaving exactly as its authors intended. The tools that produce them read a contract's *capabilities* — the presence of a `mint` selector, a pausable modifier, a proxy storage slot — and report each one as a risk. [Hidden admin controls](/wiki/economics/finance/fraud/hidden-admin-controls) makes the point from the reader's side: the function tells you what is possible, not what is intended. This section is the deployer's side of the same fact, and the arithmetic is unforgiving. Circle's USDC has a blacklist because a regulated dollar needs one; a [honeypot](/wiki/economics/finance/fraud/honeypot-token) has a blacklist because it is a trap. One boolean carries both.

## The measurement

The obvious way to test a detector is to scan tokens everybody already trusts, and it is the wrong way: those are the tokens the vendors have manually allowlisted, so the experiment measures the allowlist. The population that matters is the ordinary honest token — real, verified, in continuous use, and famous nowhere.

Ten of them, queried against GoPlus's free Token Security API on 2026-08-31. GoPlus's own integration list — last revised in March 2025, and self-reported — names Bitget Wallet, OneKey, SafePal, TokenPocket, CoinMarketCap, DEXTools and Dexscreener among the products consuming it, so a finding here is not one site's opinion:

The last column is GoPlus's `trust_list`, its hand-curated allowlist of "famous and trustworthy" tokens — the field that, in practice, is what a clean verdict rests on.

| Token | What it is | Risk fields returned as `1` | `trust_list` |
| --- | --- | --- | --- |
| yvUSDT-1 | Yearn V3 vault, $5.8M | `honeypot_with_same_creator` | absent |
| gtWETH | MetaMorpho vault, curator Gauntlet | `is_mintable`, `slippage_modifiable` | absent |
| steakEURCV | MetaMorpho vault, curator Steakhouse | `is_mintable`, `slippage_modifiable` | absent |
| mhyETH | MetaMorpho vault, run by Index Coop | `is_mintable`, `slippage_modifiable` | absent |
| mwEURC | MetaMorpho vault, Moonwell, on Base | `is_mintable`, `slippage_modifiable` | absent |
| LDY | Ledgity governance token | `is_mintable` | absent |
| ALMANAK | Almanak, fixed supply | *(none)* | absent |
| LIQ | iAero, fixed supply | *(none)* | absent |
| LMTS | Limitless, on Base | *(none)* | absent |
| MOR | Morpheus, on Arbitrum | *(none)* | absent |

Six of the ten carry at least one risk flag and none of the ten carries a `trust_list` entry. The four that come back clean are conventional fixed-supply tokens with no administrative surface at all, which narrows the finding to something sharper than "honest tokens get flagged": an honest token gets flagged when its legitimate design includes an admin function, and the vault shares fail as a category. All four MetaMorpho vaults return the same pair of flags because they share one audited factory codebase — `is_mintable` because an [ERC-4626](/wiki/economics/finance/defi/ethereum/erc-4626) vault mints shares on deposit, which is the entire product, and `slippage_modifiable` because the curator can set a fee.

The most severe string in the vendor's vocabulary landed on the Yearn vault. `honeypot_with_same_creator` is documented as "the number of honeypot tokens created by this creator", and GoPlus attributes creation to a Yearn deployer key rather than to the Balloon Vault Factory that Blockscout names, then convicts the vault by association with something else that key touched. The response names no honeypot, so the claim cannot be checked or rebutted from it.

## Three failure modes

Grouping every complaint under "false positive" hides the fact that the three have different symptoms, different causes, and different remedies.

**Flag.** A machine returns a positive finding on a token behaving as designed. USDT returns `is_mintable`, `is_blacklisted`, `transfer_pausable`, `owner_change_balance`, `slippage_modifiable` and `external_call` all set to `1` in one response — six accusations against the largest stablecoin in circulation, every one of them a true statement about the bytecode.

**No-signal.** The token is outside the machine's coverage, and absence gets rendered as risk — [the blank field](/wiki/economics/finance/defi/token-false-alarms/the-blank-field). GoPlus documents twenty-one fields as tri-state — `"1"` true, `"0"` false, no return unknown — and says of `trust_list` that "No return doesn't mean it is risky", with the same caveat in looser wording on two more. A consumer reading absent-as-false, or absent-as-danger, is reading a verdict the API never issued.

**Suppression.** The token is hidden with no banner and no notice, so there is nothing to [appeal](/wiki/economics/finance/defi/token-false-alarms/clearing-a-flag). Etherscan hides transfers of poor-reputation tokens across the site by default, announced 2024-01-29. This is the mode with no complainant: the deployer never learns it happened, because no user sees a warning to report.

## Six machines

The word "scanner" covers six mechanisms that share almost nothing. Which one fired determines both what the finding means and who can undo it.

1. **Bytecode capability scanning** reads function selectors and storage patterns. GoPlus's ~45 result fields, TokenSniffer's 26 named Smell Tests, Quick Intel's 22 numbered flags and MetaMask's 51 token-risk labels are four vocabularies for one operation. [Capability flags](/wiki/economics/finance/defi/token-false-alarms/capability-flags) covers what it can and cannot see.
2. **Sandbox trade simulation** buys and sells against forked state and reports the outcome. It is the one machine whose positive finding is worth believing — the mechanism and its evasions are on [honeypot token](/wiki/economics/finance/fraud/honeypot-token#why-one-simulation-is-not-enough) — and GoPlus's own documentation concedes it false-positives on anti-bot code.
3. **Liquidity and holder heuristics** apply fixed thresholds and locker allowlists — TokenSniffer wants every wallet under 5% of supply and at least 95% of liquidity locked or burned. [Liquidity and holders](/wiki/economics/finance/defi/token-false-alarms/liquidity-and-holders).
4. **Deployer-graph association** convicts by shared creator, through fields like `honeypot_with_same_creator` that no contract change reaches — [deployer history](/wiki/economics/finance/defi/token-false-alarms/liquidity-and-holders#deployer-history).
5. **Domain blocklists** flag the project's website rather than its contract. MetaMask's `eth-phishing-detect` carries roughly 98,000 blocklist entries against 58 allowlist entries and an 8-entry fuzzy-match list; [clearing a flag](/wiki/economics/finance/defi/token-false-alarms/clearing-a-flag#domain-blocklists) covers getting off it.
6. **Curation allowlists** decide that a token is fine. Every heuristic above has exactly one reliable off-switch and it is membership in a list the token's authors do not control — [allowlists](/wiki/economics/finance/defi/token-false-alarms/allowlists).

## Which machine fired

The appeal route is determined entirely by the answer, and the symptoms are routinely misattributed. The strings below were read off the live products on 2026-08-31.

| What the user reports | Machine | Who owns the appeal |
| --- | --- | --- |
| `Warning! There are reports that this address was used in a Phishing scam.` | Etherscan name tags | Etherscan, signed-message ownership proof |
| `Reputation SUSPICIOUS` / `SPAM` tooltip | Etherscan token reputation | Nobody — no appeal channel exists |
| `Site flagged as unsafe` / `Risk signals detected` | MetaMask simulation and security partners | In-product report for transaction alerts; support otherwise |
| `This website might be harmful` | `eth-phishing-detect` | A pull request against the list, faster than an issue |
| `{SYMBOL} isn't traded on leading U.S. centralized exchanges.` | Uniswap curation | Nobody — it is a listing gate, not a security finding |
| Uniswap `Impersonator` / `Honeypot` / `Spam` | Blockaid token scanning | `report.blockaid.io/mistake` |
| Uniswap `Not Available` | Uniswap compliance list | `compliance@uniswap.org` |
| `This domain is new or has not been reviewed yet.` | Phantom domain age | Nobody — it clears in days |
| A risk badge in a wallet or screener | Bytecode capability scan | GoPlus feedback form, or $199 for a manual review |

The two rows that generate the most misdirected effort are the Uniswap pair. `isn't traded on leading U.S. centralized exchanges` is a statement about listings and is not produced by Blockaid, so appealing it to Blockaid achieves nothing; Uniswap Labs states it "is not able to adjust warnings on specific tokens", so appealing a Blockaid finding to Uniswap achieves nothing either.

Three strings that circulate widely in write-ups are not in any current product. Greps across freshly fetched Etherscan pages on 2026-08-31 found no instance of "reported for suspicious activity", "Contract source has not been verified", or "unrecognised token contract". MetaMask's "This is a deceptive request" was the localisation key `blockaidTitleDeceptive`, shipped through v13.45.0 and removed in v13.46.x; the remediation sites that rank for it are still selling a fix for a string that no longer exists.

How often any of this is wrong, and why the vendors publish detection counters but never an error rate, is on [how often this is wrong](/wiki/economics/finance/defi/token-false-alarms/how-often-this-is-wrong). What a builder can actually do before launch is on [designing and self-checking](/wiki/economics/finance/defi/token-false-alarms/designing-and-self-checking).

## Scope

Fungible tokens on [EVM](/wiki/economics/finance/defi/ethereum#the-ethereum-virtual-machine-evm) chains, plus Solana where the tooling differs instructively. [NFT](/wiki/economics/finance/defi/nft) spam classification is a separate machine with separate heuristics and is not covered.

Every live value on these pages carries the date it was read. Vendor field sets, thresholds, prices and product names in this area change faster than the documentation describing them, and several of the facts here already contradict the vendor's own docs — GoPlus publishes three mutually incompatible free-tier rate limits on three live pages, and `eth-phishing-detect`'s reference doc asserts a fuzzy-match tolerance of 2 while its config file says 1. Reproduce before relying.

## Wiki Pages

{{< section >}}
