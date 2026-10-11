---
title: "Proof of Authority"
weight: 60
---

Proof of authority is an arrangement in which a blockchain's blocks are produced by a fixed list of approved signers. A block is valid if it carries the signature of a key on the list and the signer has respected the protocol's rule for taking turns. Nobody competes for the right to produce a block and nothing is staked. What a participant needs is a place on the list, which is set when the chain starts and changed afterwards by a vote of the signers already on it.

The "proof" is an ordinary digital signature. The scarcity that other chains get from [computation](/wiki/economics/defi/sybil-resistance/proof-of-work) or [deposits](/wiki/economics/defi/sybil-resistance/proof-of-stake) comes here from admission being decided by people. Creating a thousand identities achieves nothing if none of them is on the list. In return, the chain is only as trustworthy as its signers, and ethereum.org's definition says so directly: it "requires trusting a set of authorized signers".

One way to place it among the alternatives comes from the documentation of a consensus library: proof of authority "can be thought of a PoS setting where all nodes have precisely the same stake". ethereum.org attributes the term to Gavin Wood, in 2017.

It is used for private and consortium chains, where the participants are known organizations, and it was the standard design for Ethereum's public test networks. Three protocols account for most of that use.

## Clique

Clique is specified in Ethereum Improvement Proposal 225 (EIP-225), written by Péter Szilágyi in March 2017 for the Rinkeby test network. It reuses the block format of proof-of-work Ethereum and replaces the puzzle with a signature.

The signers are kept in a sorted list. For each block number one signer is *in turn*: the one whose position in the list equals the block number modulo the number of signers. Any signer may sign any block, but the proposal suggests a weight of 2 for a block from the in-turn signer and 1 for a block from anyone else, and nodes follow the heaviest chain. Out-of-turn signers are told to wait a short random delay before signing, so the in-turn block normally arrives first, and a signer that is offline costs the chain only that delay.

Two rules limit what a stolen key can do.

- A signer may sign at most one block in every ⌊*N* / 2⌋ + 1 consecutive blocks, where *N* is the number of signers. With five signers that is one block in any three.
- The list is changed by votes that signers place in the headers of their own blocks. A proposal to add or remove a signer takes effect when ⌊*N* / 2⌋ + 1 signers have voted for it.

Clique has no notion of a final block. Two signers can produce competing blocks, and the fork is settled by weight, as it would be under proof of work.

## Aura

Aura, short for Authority Round, was the equivalent in the OpenEthereum client. Turns are assigned by the clock. Time is cut into steps of *t* seconds, the step number is the current UNIX time divided by *t*, and the signer for step *s* is number *s* modulo *n* in the list. Signing outside one's own step counts as misbehaviour.

Aura does state a finality rule: a block is final once the blocks built on top of it carry signatures from more than half the signers. The rule is given "under the assumption of a synchronous network", one that delivers every message within a step. OpenEthereum has been discontinued, and ethereum.org marks the Aura specification as deprecated.

## QBFT and IBFT 2.0

The third approach has the signers vote on every block. Hyperledger Besu, an Ethereum client, offers two such protocols for private networks: QBFT, and IBFT 2.0, a revision of the Istanbul BFT protocol (IBFT). They are Byzantine fault tolerant (BFT) voting protocols, meaning they tolerate some validators that behave arbitrarily, and IBFT 2.0 takes its handling of a failed proposer from [PBFT](/wiki/economics/defi/consensus/pbft#where-it-runs-now). Besu's documentation describes them as having "immediate finality", with no forks. It asks for at least four validators if the network is to tolerate one that misbehaves, and existing validators vote to add or remove others. Besu no longer supports Clique.

| Protocol | Whose turn | Forks | Finality |
|---|---|---|---|
| Clique | set by block number; others may step in | possible, the heavier chain wins | none |
| Aura | set by the clock | possible | once more than half the signers have built on a block, if the network is synchronous |
| QBFT, IBFT 2.0 | validators take turns to propose, then all vote | none | immediate |

## Where it has been used

**Ethereum test networks.** ethereum.org says that "most testnets started by using a permissioned proof-of-authority consensus mechanism". Rinkeby ran Clique from April 2017. In June 2022 the Ethereum Foundation announced that Rinkeby "will not transition to proof-of-stake" and would be shut down the following year. ethereum.org now lists Rinkeby, Kovan and Goerli as deprecated, and the test networks it maintains run proof of stake.

**Private networks.** This is the use Besu's protocols are documented for.

**BNB Smart Chain.** Its documentation names the consensus Proof of Staked Authority. As of the July 2025 documentation the active validators were the 45 ranked highest by stake, and as of March 2026 a block was produced about every 0.45 seconds.

**VeChain.** VeChain's main network ran proof of authority with identity-checked validators until its Hayabusa upgrade of 2 December 2025, which VeChain describes as a move to delegated proof of stake.

## Limits

**The signers can rewrite and censor.** A majority of Clique signers can produce the heaviest chain, exclude any transaction, and vote the other signers off the list. No deposit is at risk in the protocol. What restrains them is outside it: contracts between the organizations involved, and their reputations.

**The security of the chain is the security of the keys.** Whoever holds a signer's key is that signer. Clique's limit on consecutive blocks exists for this case. The specification gives the reason as "malicious signers (loss of signing key)".

**The voting variants stop when too many signers are absent.** Besu's protocols need two thirds of validators online to produce blocks.

**Nobody can join without being let in.** That is the design, and it is why public chains that began this way have tended to move to proof of stake.

## Sources

- Szilágyi, [EIP-225: Clique proof-of-authority consensus protocol](https://eips.ethereum.org/EIPS/eip-225) (2017)
- OpenEthereum documentation, [Aura - Authority Round](https://openethereum.github.io/Aura)
- Hyperledger Besu documentation, [Proof of authority consensus](https://docs.besu-eth.org/private-networks/concepts/poa), read 10 October 2026
- ethereum.org, [Proof-of-authority (PoA)](https://ethereum.org/developers/docs/consensus-mechanisms/poa/) and [Networks](https://ethereum.org/developers/docs/networks/), read 10 October 2026
- Ethereum Foundation Blog, [Ropsten, Rinkeby & Kiln Deprecation Announcement](https://blog.ethereum.org/2022/06/21/testnet-deprecation) (21 June 2022)
- BNB Chain documentation, [BNB Smart Chain overview](https://docs.bnbchain.org/bnb-smart-chain/overview/) and [Validator overview](https://docs.bnbchain.org/bnb-smart-chain/validator/overview/), read 10 October 2026
- VeChain, [VeChain's Renaissance: why Hayabusa matters](https://vechain.org/vechain%E2%80%99s-renaissance-why-hayabusa-matters), and the [StarGate documentation](https://docs.stargate.vechain.org/) for the date
- Ava Labs, [Simplex README](https://github.com/ava-labs/simplex/blob/main/README.md)
