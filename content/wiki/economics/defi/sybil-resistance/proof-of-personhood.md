---
title: "Proof of Personhood"
weight: 70
---

A proof of personhood is a credential showing that its holder is a real human being who holds no other such credential. It says nothing else about the holder. A system that hands one to each person, and counts each credential once, gives every person exactly one voice.

As a [Sybil-resistance mechanism](/wiki/economics/defi/sybil-resistance) it replaces the tradable resource with the participant's own existence. [Proof of work](/wiki/economics/defi/sybil-resistance/proof-of-work) and [proof of stake](/wiki/economics/defi/sybil-resistance/proof-of-stake) give more influence to whoever commits more, and the people who proposed proof of personhood meant it as an objection to that. Bryan Ford's requirement is that it must not be feasible "to buy more (effective) voting power with more wealth, connections, or other resources", which, he notes, "excludes investment-based foundations for decentralized systems such as proof of work or proof of stake."

The difficulty is the uniqueness. Showing that a participant is human is the easier half. Showing that the same human has not already been counted, without building a register of who everyone is, is what the schemes below each attempt in a different way. Ford's distinction is that "identity is about distinguishing one person from another", while "personhood is about giving all real people inalienable digital participation rights independent of identity".

Only one running blockchain was found that weights its consensus this way, and it is small. The other systems here issue credentials that applications use for voting, distributions and access.

## Meeting in person

The original proposal, which Ford dates to 2008, is the *pseudonym party*. People gather at one place and time. Each attendee receives one token. Nobody is asked who they are, and attendees may hide their faces. A person cannot be in two places at once, so parties held at the same moment everywhere bound the number of tokens by the number of bodies. In the 2017 design by Borge and co-authors, a deadline closes the doors, attendees file past every organizer, and each is marked with ink on leaving, so that nobody collects twice. Tokens expire, and the party is repeated.

That paper goes on to a cryptocurrency in which the tokens are the voting weight, moving "from Bitcoin's ultimately unsuccessful 'one CPU one vote' decentralization principle to a minting mechanism that embodies a one PoP-token one vote principle." It is a short proposal and reports no deployment. Its trust assumption is that at least one organizer of each party, and one of the servers that record it, are honest.

The limits are practical: everyone has to turn up, repeatedly, and someone has to run the events.

## Everyone at once, online

Idena moves the simultaneous gathering online. All participants take a short test at the same moment worldwide, made of puzzles called *flips* that are meant to be easy for a person and hard for a program. The reasoning is the same as for the party: "A single person is not able to validate herself multiple times because of the limited timeframe for the answers submission." Validation lasts for one period and must be repeated at the next session.

Idena's documentation describes the chain as "driven by Proof-of-Person consensus with every node linked to a cryptoidentity, one person with equal voting power." The same documentation qualifies it. Some validated identities have their votes left out of consensus and governance, among them identities grouped into a pool, which share one vote between them, and identities holding less than a threshold of staked coins. Part of the reward is paid in proportion to stake raised to the power 0.9. The rules bring a stake requirement back into a system designed to do without one.

On 10 October 2026 Idena's own index reported 120 identities and 76 block producers online.

A general weakness of puzzle-based tests is noted in a 2020 review by Siddarth and co-authors. They "may prevent automated and bot attacks", but one person passing several times is a different attack, and "machine learning presents an evolving threat" to the puzzles themselves. Idena's synchronized session answers the first point. The second is a moving target.

## Biometrics

World, formerly Worldcoin, issues its credential after scanning a person's irises with a purpose-built device, the Orb. The device checks that it is looking at a live human and derives an *iris code*, a numeric summary of the texture of the iris. Uniqueness is checked by comparing the new code against all earlier ones. World's documentation says the comparison is run as a computation split among several parties, which outputs "only a single bit per invocation: whether the individual has previously verified", and that images "are deleted after verification."

By the account in World's own documents, the credential does not weight a blockchain's consensus. World Chain, the project's own chain, is a layer built on Ethereum and operated by a company. Verified humans get priority for their transactions. They do not produce blocks.

Vitalik Buterin's 2023 assessment names four risks of the design: privacy, since a register of iris codes may reveal more than intended; accessibility, since the device has to reach everyone; centralization, since the device is special hardware from one maker; and security, including coerced or purchased scans. Regulators have acted on the first. Spain's data protection agency ordered Tools for Humanity, the company that builds the Orb, in March 2024 to stop collecting and processing personal data in Spain, as a provisional measure.

## Social graphs and vouching

A third family infers uniqueness from relationships between accounts.

- **BrightID** builds what its documentation calls "an anonymous social graph" from connections that users make with one another, and awards verification on the basis of an account's position in it.
- **Proof of Humanity** is a registry in which an applicant submits a video and a deposit, an existing member vouches that the applicant is a unique person, and anyone may challenge the entry during a waiting period, with disputes going to an arbitration service.

The 2020 review's caution about this family is that it comes with no guarantee: the web-of-trust approach does not by itself ensure that a well-connected account is one person.

## What every version shares

**A credential can be sold or rented.** Whatever proves that a person is unique, the person can then hand the resulting key to someone else. No scheme here prevents it. The cost of a second voice is the price of another person's cooperation.

**Someone has to be trusted.** A party needs an honest organizer, a biometric scheme needs an honest device and operator, and a social graph needs its early members to be who they appear to be.

**Privacy and uniqueness pull against each other.** Uniqueness requires remembering something about everyone already counted. The less that record reveals, the harder it is to check.

Ford's own conclusion, after comparing the approaches in 2020, was that "at present anyway, federated pseudonym parties appear to be the only plausible means" of meeting all his goals. Buterin's, three years later and with biometrics in view: "There is no ideal form of proof of personhood."

## Sources

- Borge, Kokoris-Kogias, Jovanovic, Gasser, Gailly & Ford, [Proof-of-Personhood: Redemocratizing Permissionless Cryptocurrencies](https://bford.info/pub/dec/pop.pdf) (2017)
- Ford, [Identity and Personhood in Digital Democracy: Evaluating Inclusion, Equality, Security, and Privacy in Pseudonym Parties and Other Proofs of Personhood](https://arxiv.org/abs/2011.02412) (2020)
- Siddarth, Ivliev, Siri & Berman, [Who Watches the Watchmen? A Review of Subjective Approaches for Sybil-resistance in Proof of Personhood Protocols](https://arxiv.org/abs/2008.05300) (2020)
- Idena documentation, [whitepaper: technology](https://docs.idena.io/docs/wp/technology) and [economics](https://docs.idena.io/docs/wp/economics), and the Idena indexer, read 10 October 2026
- World, [World Whitepapers](https://whitepaper.world.org/), updated 25 March 2026
- Buterin, [What do I think about biometric proof of personhood?](https://vitalik.eth.limo/general/2023/07/24/biometric.html) (24 July 2023)
- Agencia Española de Protección de Datos, press release of 6 March 2024 on Worldcoin
- BrightID, [Getting verified](https://brightid.gitbook.io/brightid/getting-verified), and Kleros, [Proof of Humanity](https://docs.kleros.io/products/proof-of-humanity), read 10 October 2026
