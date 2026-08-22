---
title: "Anti-Money Laundering"
weight: 10
---

Money laundering is the process of making the proceeds of crime usable — taking value that cannot be explained and giving it an explanation. Anti-money laundering (AML) is the body of law, regulation, and operational practice built to interrupt that process, and it is the reason financial institutions behave less like service providers and more like checkpoints.

## The three stages

The canonical model, which every compliance training deck reproduces, breaks laundering into three phases:

1. **Placement** — getting the value into the financial system. Cash deposits, cash-intensive front businesses, purchases of monetary instruments. This is the riskiest stage for the launderer and the one AML controls are most heavily aimed at.
2. **Layering** — obscuring the trail. Chains of transfers between accounts, jurisdictions, and legal entities, each one adding a hop that an investigator has to subpoena separately.
3. **Integration** — returning the value to the launderer with an apparently legitimate origin: a property sale, a consulting invoice, a capital gain.

The model is a simplification, and it fits cash-generating crime (narcotics, extortion) far better than it fits fraud, corruption, or tax evasion, where the funds may start out inside the banking system and never leave it. But it explains the placement-heavy emphasis of US law: the [Bank Secrecy Act](/wiki/economics/finance/regulation/bank-secrecy-act) is overwhelmingly concerned with the moment cash meets a bank.

## What an AML regime consists of

Across jurisdictions the components are near-identical, because they descend from the same source — the Financial Action Task Force (FATF), an intergovernmental body whose Forty Recommendations are the de facto global standard. Countries that fail FATF's mutual evaluations land on a grey or black list, which raises the cost of correspondent banking — the accounts domestic banks hold at foreign ones in order to settle cross-border payments — for every institution in the country. That mechanism, rather than any treaty, is what produces the convergence.

The standard components:

- **Customer identification** — [know your customer](/wiki/economics/finance/regulation/know-your-customer) at onboarding, and beneficial-ownership identification for entities.
- **Risk assessment** — customers, products, geographies, and channels rated for risk, with due diligence scaled accordingly.
- **Transaction monitoring** — automated surveillance of activity against expected behaviour, generating alerts for human review.
- **Reporting** — suspicious activity reports to a financial intelligence unit ([FinCEN](/wiki/economics/finance/regulation/fincen) in the US), plus threshold-based reports that require no suspicion at all.
- **Recordkeeping** — retention of identity and transaction records, and propagation of originator details between institutions under the [Travel Rule](/wiki/economics/finance/regulation/travel-rule).
- **Sanctions screening** — technically a separate regime; in practice run by the same team and the same software. See [OFAC sanctions](/wiki/economics/finance/regulation/ofac-sanctions).

## Why it is hard to evaluate

AML is unusual among regulatory regimes in that its central claim — that it reduces crime — has never been convincingly measured, in either direction.

The output metrics are all activity, not outcome: reports filed, alerts generated, accounts closed, penalties assessed. The one number that would matter, the share of criminal proceeds actually interdicted, is estimated at well under one percent and is not systematically tracked. Meanwhile the false-positive rate on transaction monitoring is routinely above 90%, which means the overwhelming majority of compliance labour is spent clearing innocent activity.

The rational institutional response to an unbounded penalty on a missed filing is to over-file and to shed risky customers wholesale — **de-risking**. Remittance corridors, non-profits in conflict zones, and [crypto](/wiki/economics/finance/defi/cryptocurrency) businesses lose banking access not because they are suspected of anything but because the expected compliance cost exceeds the expected revenue. The displacement argument — that the activity does not stop but moves somewhere with no reporting at all — is plausible and widely made, though it inherits the same measurement problem as everything else here.

None of which establishes that the alternative is better. It does mean that "AML requires it" is a claim about law, not a claim about effectiveness, and the two are worth keeping separate when designing systems.

## AML and permissionless systems

Every element above assumes an identifiable customer and an institution with the power to refuse them. A public [blockchain](/wiki/economics/finance/defi/blockchain) supplies neither: a [smart contract](/wiki/economics/finance/defi/smart-contract) has no onboarding step and no ability to decline. The regulatory pressure therefore concentrates at the edges — the [gateways](/wiki/economics/finance/defi/cryptocurrency-gateway) where fiat becomes crypto, and the front-ends and developers who make protocols usable. [DeFi and US regulatory restrictions](/wiki/economics/finance/defi/defi-us-regulatory-restrictions) covers how that pressure has been applied.

There is a real technical question underneath the political one: whether the assurances AML seeks — this counterparty is not sanctioned, these funds are not stolen — can be delivered by proof rather than by disclosure. [Zero-knowledge proofs](/wiki/cs/zero-knowledge-proofs) make credible-set membership provable without revealing identity, which is at least the right shape for the problem. Nothing in the current US regime accepts such a proof in place of a document.

## External links

- [FATF Recommendations](https://www.fatf-gafi.org/en/topics/fatf-recommendations.html) — the international standard the national regimes implement
- [FinCEN](https://www.fincen.gov/) — the US financial intelligence unit
- [UK JMLSG guidance](https://www.jmlsg.org.uk/guidance/current-guidance/) — a well-written worked example of a non-US AML regime
- [Pol, "Anti-money laundering: the world's least effective policy experiment?"](https://www.tandfonline.com/doi/full/10.1080/25741292.2020.1725366) — the most-cited academic critique of AML effectiveness
