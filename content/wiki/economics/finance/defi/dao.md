---
title: "Decentralized Autonomous Organization (DAO)"
weight: 6
---

A DAO is an organization governed by [smart contracts](/wiki/economics/finance/defi/smart-contract) on a [blockchain](/wiki/economics/finance/defi/blockchain) rather than by a traditional management hierarchy. Rules are encoded in code, the treasury is managed on-chain, and decisions are made through proposals that members vote on. No single person or board has unilateral control.

DAOs matter because they offer a credibly neutral governance structure. Once the smart contracts are deployed, the rules apply equally to everyone -- including the founders. This makes them a natural fit for managing DeFi protocols, shared treasuries, and any situation where participants need to coordinate without trusting a central operator.

## How DAOs Work

A DAO's lifecycle typically follows three phases:

1. **Smart contract development** -- The rules for membership, voting, and treasury management are written into contracts and audited. These define what proposals can do, how votes are tallied, and what thresholds are required for execution.
2. **Funding** -- The DAO raises capital, usually by issuing governance tokens. Token holders become stakeholders with voting rights.
3. **Operation** -- Members submit proposals (allocate funds, change parameters, onboard partners), the community votes, and passing proposals execute automatically.

The smart contracts are the authority. Funds cannot move without a vote, and the rules cannot change without a governance process.

## Membership Models

**Token-based** -- Anyone who holds the governance token can vote. Tokens are freely tradable on [decentralized exchanges](/wiki/economics/finance/defi/dex), making membership permissionless. Voting power scales with token holdings. [Uniswap](/wiki/economics/finance/defi/uniswap) and MakerDAO use this model.

**Share-based** -- Members receive shares in exchange for contributions (capital, labor, or other resources). Shares are typically non-transferable and can be redeemed from the treasury on exit. This model suits smaller, mission-driven groups like investment clubs or grant committees.

**Reputation-based** -- Voting power is earned through participation rather than purchased. Contributors gain influence by doing work for the DAO. This creates more egalitarian governance but is harder to scale.

## Notable Examples

- **MakerDAO** -- Governs the Maker Protocol and the DAI stablecoin. Token holders vote on collateral types, risk parameters, and protocol upgrades.
- **ConstitutionDAO** -- Raised $40 million in days to bid on a copy of the U.S. Constitution. Lost the auction but demonstrated the speed at which DAOs can coordinate capital.
- **Nouns DAO** -- One Noun NFT is auctioned daily, and all proceeds go to the treasury. Noun holders govern spending. The model has been widely forked.
- **Aragon** and **DAOstack** -- Frameworks for launching DAOs without writing smart contracts from scratch.

## Advantages Over Traditional Organizations

**Transparency** -- Every proposal, vote, and fund movement is on-chain and auditable by anyone.

**Reduced principal-agent problems** -- Token holders govern directly rather than delegating to executives whose incentives may diverge.

**Global participation** -- Anyone with an internet connection and a wallet can join a permissionless DAO.

## Risks and Challenges

**Smart contract vulnerabilities** -- A bug in the governance contract can be catastrophic. The 2016 DAO hack exploited a reentrancy flaw and drained $50 million in [Ether](/wiki/economics/finance/defi/ethereum/), ultimately leading to Ethereum's contentious hard fork.

**Governance capture** -- Token-based voting concentrates power in the hands of large holders ("whales"). Low voter turnout can make it easier for small coalitions to push proposals through.

**Coordination overhead** -- As membership grows, reaching consensus slows down. Many DAOs struggle with voter apathy and proposal fatigue.

**Legal ambiguity** -- Most jurisdictions do not recognize DAOs as legal entities. Wyoming became the first U.S. state to offer DAO LLC registration, but regulatory frameworks remain sparse globally.

## External Links

- [Ethereum.org: DAOs](https://ethereum.org/en/dao/)
- [DeepDAO](https://deepdao.io) -- analytics dashboard tracking DAO treasuries, membership, and governance activity
- [Wikipedia: Decentralized Autonomous Organization](https://en.wikipedia.org/wiki/Decentralized_autonomous_organization)
