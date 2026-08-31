---
title: "Ponzi Scheme"
weight: 40
---

A Ponzi scheme pays returns to existing investors out of deposits from new ones and calls the payments profit from some economic activity. The activity need not exist. What the operator needs is a story about where the yield comes from, deposits arriving faster than withdrawals, and enough friction on redemptions to keep the second condition true. Charles Ponzi's 1920 original offered 50% in 45 days on arbitrage in international postal reply coupons and ran about eight months.

On a [blockchain](/wiki/economics/finance/defi/blockchain) the deposits are irreversible, no bank reconciles them, and the redistribution can run in a contract anyone can read and nobody can switch off. It sits in the investment-fraud group of [crypto fraud](/wiki/economics/finance/fraud) beside the [exit scam](/wiki/economics/finance/fraud/exit-scam).

## Ponzi, pyramid, multi-level marketing

A **Ponzi** has a central operator and passive investors: deposits go to one place, the operator quotes a return, and no investor has a job beyond depositing. A **pyramid** pays for recruitment — a participant's return comes from the entry fees of the people they enroll and of the people those enroll, so the sales work is pushed down the tree and the compensation plan is itself the stated source of income. **Multi-level marketing (MLM)** sells a product and pays commission on a downline, and the Federal Trade Commission's test is whether compensation is driven by retail sales outside the network or by recruitment.

Crypto schemes are usually hybrids — a Ponzi core with a recruitment bonus bolted on, since recruitment is the only thing that keeps the required deposit growth achievable. The Securities and Exchange Commission (SEC) charged Forsage as a fraudulent crypto pyramid *and* Ponzi scheme in a single phrase.

## The arithmetic that fixes the collapse date

Paid out of deposits, a promised rate compounds, and so does the new money needed to service it.

```text
$1,000,000 on deposit, 1% per day paid entirely from new deposits

  day        owed to depositors      new money needed that day
    0                $1,000,000                        $10,000
   70                $2,006,763                        $20,068
  140                $4,027,099                        $40,271
  280               $16,217,528                       $162,175
  365               $37,783,434                       $377,834
  730            $1,427,587,910                    $14,275,879
```

1% a day is 37.8x a year. A scheme opening with $1 million on deposit has to find $36.8 million of new money in its first year and $1.39 billion in its second. The doubling time is ln 2 / ln 1.01 = 69.7 days, so the required inflow doubles every ten weeks from launch however small the launch was, and the ceiling is the recruitable population and the money it holds rather than anything the operator decides. Reaching that same 37.8x at 10% a year takes 38 years, which is roughly the return Bernard Madoff quoted; when his scheme started is disputed, with Madoff claiming the early 1990s and prosecutors alleging the 1970s or 1980s.

## Why crypto suits it

A confirmed deposit has no chargeback and no return window, and a scheme taking deposits to an address it controls produces no statement a third party has to reconcile or sign. The yield story is unfalsifiable by construction: "arbitrage bot", "AI trading desk", "mining pool" and "flash-loan arbitrage" each name an activity that genuinely pays someone, the strategy is proprietary so the trades are never shown, and the reported returns come out smooth, which no real trading return is. Recruitment then runs on messaging and video platforms without stopping at a border, which the arithmetic requires it not to.

## On-chain Ponzis

Some schemes put the redistribution logic in a public, verified [smart contract](/wiki/economics/finance/defi/smart-contract). Forsage is the canonical case: participants bought "slots" in a matrix and the contract forwarded each payment straight to the addresses above them in the tree, on Ethereum and later on BNB Chain and Tron. Anyone could read it and compute their own expected return before paying. The SEC's August 2022 action charged eleven individuals over a scheme it valued at more than $300 million, after cease-and-desist orders from regulators in the Philippines and Montana had failed to stop contracts with no off switch.

Publishing the source does not make it not a fraud, because the code is the fraud: it is the mechanism by which later deposits pay earlier ones, executed exactly as written with no discretion left to anybody. An off-chain scheme hides the mechanism and asks the depositor to take the operator's word for a strategy nobody can inspect; an on-chain one shows the mechanism and is mostly unread. Auditability is not a defence when the audited thing is a redistribution loop.

## Where the line with real yield sits

The question that separates the categories is what the counterparty is paying for. [Staking](/wiki/economics/finance/defi/staking) yield is protocol issuance plus priority fees plus [maximal extractable value](/wiki/economics/finance/defi/maximal-extractable-value), bounded by a public issuance schedule. Lending yield is a borrower who wants leverage or working capital, at a rate that moves with utilization. [Yield farming](/wiki/economics/finance/defi/yield-farming) returns are trading fees from swappers plus incentive tokens the protocol prints, and that second component is dilution paid by future holders rather than revenue. If nobody can name the payer, the depositors are the payer. Two tells follow from the arithmetic rather than the story: a fixed daily or weekly rate is not what any market pays, and a referral bonus paid on deposits rather than on profits is a recruitment cost that can only come out of principal.

## Cases

**BitConnect (2016–2018).** A lending program paying up to roughly 1% a day, attributed to a proprietary "volatility software" trading bot, with tiered referral commissions on top. The lending platform closed on 16 January 2018 and the token lost substantially all its value within hours. The Department of Justice's February 2022 indictment of founder Satish Kumbhani described approximately $2.4 billion obtained from investors; the SEC had brought civil charges in 2021, and lead US promoter Glenn Arcaro pleaded guilty to conspiracy to commit wire fraud. Kumbhani left India; India's Enforcement Directorate reported tracking him to Ahmedabad in February 2025 while seizing about $190 million in the case, and no public record indicates an arrest.

**PlusToken (2018–2019).** A wallet application sold across China and South Korea promising monthly returns from an unspecified arbitrage desk, wrapped in a multi-level referral structure. Chinese courts sentenced 27 people in 2020 to terms running to about eleven years, in proceedings reporting victim counts in the millions. Chainalysis attributed a measurable share of 2019 bitcoin sell pressure to liquidation of the scheme's holdings.

**Terra/LUNA (2022).** Anchor Protocol paid about 19.5% on deposits of the UST stablecoin from a reserve topped up by the project rather than earned from borrowers, which is the Ponzi shape at the yield layer. Whether the system as a whole was a Ponzi or an under-collateralized peg that failed under redemption pressure is a real disagreement among people who understand it. Neither case that succeeded rested on a Ponzi theory: the April 2024 civil fraud verdict against Terraform Labs and Do Kwon turned on misrepresentations about the ecosystem, and Kwon's guilty plea in August 2025, which drew a 15-year sentence that December, was to conspiracy and wire fraud.

## Where the law lands

A Ponzi interest is a security under the *Howey* test whatever it is denominated in: money invested in a common enterprise with an expectation of profit derived from the efforts of others. The offering is therefore unregistered under Section 5 of the Securities Act and fraudulent under the antifraud provisions, and the SEC charges both. Criminal exposure is ordinary wire fraud (18 U.S.C. § 1343), with money laundering and conspiracy counts on the proceeds. "High-yield investment program (HYIP)" is a category the SEC and the FBI name explicitly in investor warnings, describing this pattern exactly. What a registry does and does not assert about an operator is covered under [regulation](/wiki/economics/finance/regulation); an [initial coin offering](/wiki/economics/finance/fraud/ico-fraud) sells a token against a promise instead of paying a running return, and [pig butchering](/wiki/economics/finance/fraud/pig-butchering) produces Ponzi-shaped account statements with no other depositors behind them at all.

## External links

- [SEC press releases](https://www.sec.gov/newsroom/press-releases) — the Forsage, BitConnect and Terraform actions, with complaints attached
- [Justice Department press releases, Southern District of New York](https://www.justice.gov/usao-sdny/pr) — the BitConnect indictment and most large US crypto fraud prosecutions
- [FBI Internet Crime Complaint Center annual reports](https://www.ic3.gov/AnnualReport/Reports) — reported investment-fraud losses by year and category
- [Chainalysis blog](https://www.chainalysis.com/blog/) — on-chain tracing of PlusToken and the annual Crypto Crime Report summaries
