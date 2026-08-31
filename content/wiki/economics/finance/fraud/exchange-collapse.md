---
title: "Exchange Collapse"
weight: 55
---

A custodial exchange keeps customer coins in wallets it controls and records who owns what in a database it also controls. Nothing on the [blockchain](/wiki/economics/finance/defi/blockchain) distinguishes a coin held for a customer from a coin the exchange is free to lend, trade, or pledge; that distinction lives only in the exchange's ledger and in the terms of service the customer accepted. A collapse is the moment the wallets and the ledger stop matching and withdrawals are suspended.

Three different failures produce that same page, and [crypto fraud](/wiki/economics/finance/fraud) coverage runs them together. Coins can be **stolen from the exchange**, which makes it a victim as well as a defendant. Customer assets can be **commingled and used** by an affiliate, which is conversion of other people's property. Or the exchange can have run **a real business that took duration and credit risk against demand deposits**, borrowing short and lending long, which is what a bank does minus capital requirements, liquidity rules, a lender of last resort, and deposit insurance.

## What a customer actually owns

"Not your keys, not your coins" is usually offered as a security slogan; the sharper version is about legal claim. A deposit buys a database entry and a contractual relationship, and in a bankruptcy the operative question is whether the deposited assets are property of the estate — answered by the terms of use rather than by the transaction history.

On 4 January 2023, Judge Martin Glenn of the bankruptcy court for the Southern District of New York (SDNY) held that the Celsius Earn program's terms transferred all right and title in deposited assets to Celsius, so roughly $4.2 billion of Earn balances belonged to the estate and Earn depositors ranked as general unsecured creditors. Assets held under the separately worded Custody terms were treated differently. Two customers of the same company, holding the same coin, landed on opposite sides of the line because they had clicked through different contracts.

Unsecured claims are also dollarized at the petition date. FTX filed on 11 November 2022 with bitcoin near $16,000, and when the estate began distributing in 2025 it paid more than the face value of those dollar claims while bitcoin traded several times higher: a creditor made whole in dollars was not made whole in coins. [Full-reserve backing](/wiki/economics/finance/defi/full-reserve-backing) avoids the question, and no customer can verify from outside that a venue practises it.

## Theft from the exchange

Mt Gox handled most global bitcoin trading before it halted withdrawals in February 2014 and filed for bankruptcy protection in Tokyo, roughly 850,000 BTC short, of which about 750,000 belonged to customers. Some 200,000 turned up in an old wallet weeks later. The proceeding converted to civil rehabilitation and creditor distributions began in July 2024 — a decade of claims administration, settled in coins worth far more than when they went missing, which is what recovery means when custody fails.

## Commingling

FTX routed customer dollar deposits to bank accounts held by North Dimension, an entity controlled by Alameda Research, the trading affiliate owned by the same founder. Alameda was exempted from the exchange risk engine's auto-liquidation and carried what amounted to an unlimited credit line against those balances, collateralised substantially by FTT, the token FTX itself issued.

When the assets backing a liability are a token the same group issues, the collateral's value is a function of the group's solvency, which is the thing the collateral was supposed to establish. The balance sheet holds only while nobody sells. A CoinDesk report on 2 November 2022 showed Alameda's balance sheet dominated by FTT, Binance said it would sell its position, withdrawals ran, and the recursion resolved in nine days. Reported trading volume offered no independent warning, being a marketing figure that [wash trading](/wiki/economics/finance/fraud/wash-trading) inflates freely.

Sam Bankman-Fried was convicted on seven counts on 2 November 2023 and sentenced in March 2024 to 25 years. Caroline Ellison, who ran Alameda, pleaded guilty, cooperated, and was sentenced to two years. Commingling differs from an [exit scam](/wiki/economics/finance/fraud/exit-scam) in intent rather than effect: the operators generally expect to put the money back.

## Duration and credit risk against demand deposits

Celsius, Voyager, and BlockFi took deposits payable on demand, promised yields well above anything a liquid dollar asset paid, and funded them with lending and trading. Voyager held an unsecured loan to Three Arrows Capital of about 15,250 BTC and $350 million in USDC; Three Arrows defaulted in June 2022 and Voyager filed for Chapter 11 in July. That month the Federal Deposit Insurance Corporation (FDIC) and the Federal Reserve sent Voyager a cease-and-desist over its claim that customer dollars were FDIC-insured, when the insurance covered the failure of Voyager's partner bank rather than the failure of Voyager.

BlockFi settled with the Securities and Exchange Commission (SEC) and state regulators for $100 million in February 2022 over its unregistered interest-bearing accounts, then filed in November 2022 with exposure to FTX. Celsius filed in July 2022, and its chief executive at the time, Alex Mashinsky, pleaded guilty in December 2024 to commodities fraud and to a scheme to manipulate the price of the company's own token, and was sentenced to 12 years in May 2025. No theft or backdoor was needed in any of the three: the deposits were spent on assets that could not be sold fast enough on the day everyone asked at once.

## Proof of reserves

The standard post-2022 response is a Merkle-tree attestation: each customer balance is hashed into a leaf, leaves are combined pairwise up to a published root, and a customer verifies a short inclusion path to confirm their own balance is in the tree, with the total at the root standing as claimed liabilities. Assets are shown separately by signing from the addresses claimed at a stated block height. That proves something narrow — those addresses held that much at one block height, and, if enough customers check their own leaves, the liability total was not quietly understated.

- Assets can be borrowed for the snapshot, since nothing binds them to the exchange between attestations. Nothing in the published timeline of the 320,000 ETH that moved from Crypto.com to Gate.io in October 2022 and returned days later shows that happening — the transfer landed after Gate.io's snapshot, and Crypto.com's chief executive said it had gone to a wrong whitelisted address — but the episode is what made the general point concrete, because no attestation on either side would have revealed it.
- Liabilities can sit off the tree entirely: a loan taken against the exchange's own assets, an obligation to a sister company, a judgment.
- Signing from an address proves the ability to sign, not exclusive control, so two entities can attest to the same coins, and nothing binds the state between snapshots.

A reserves attestation published without a liabilities attestation asserts that a company has some money, which nobody disputed. Mazars produced an agreed-upon-procedures report for Binance in December 2022 and then withdrew from crypto work; agreed-upon procedures expresses no opinion and is not an audit. Vitalik Buterin's November 2022 proposal replaces the tree with a zero-knowledge (ZK) proof that balances sum to the published total and that none is negative, stopping an exchange from shrinking its stated liabilities with a negative leaf without publishing the distribution of customer balances.

## Where the law lands

A custodial exchange in the United States registers with FinCEN as a [money services business](/wiki/economics/finance/regulation/money-services-business) and runs [know your customer](/wiki/economics/finance/regulation/know-your-customer) and anti-money-laundering programs, none of which is a solvency regime: no federal capital requirement, no segregation mandate, no insurance on the coins. New York's Department of Financial Services imposes custody and capital conditions on its virtual currency licensees. Charges arrive after the fact as ordinary fraud — wire fraud, securities fraud, conspiracy — because for most venues no reserve requirement exists to fail.

## What a depositor can check

Read the terms of use for language transferring title or granting a right to lend; that clause decides where you stand in a bankruptcy, and it is the difference between the Celsius Earn and Custody outcomes. Treat a reserves report with no liabilities proof as unverified. Read a withdrawal delay described as an upgrade as the failure it usually is.

## External links

- [Vitalik Buterin: proof of solvency and beyond](https://vitalik.eth.limo/general/2022/11/19/proof_of_solvency.html) — the November 2022 argument for zero-knowledge liability proofs
- [FTX Chapter 11 restructuring docket](https://restructuring.ra.kroll.com/FTX/) — filings, claims process, and distribution notices
- [Mt Gox trustee announcements](https://www.mtgox.com/) — the civil rehabilitation timeline and repayment notices
- [SEC press releases](https://www.sec.gov/newsroom/press-releases) — settlements with crypto lending programs, including BlockFi
- [US Attorney's Office, Southern District of New York](https://www.justice.gov/usao-sdny) — the FTX and Celsius prosecutions
