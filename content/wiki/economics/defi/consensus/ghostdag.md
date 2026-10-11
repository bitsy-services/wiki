---
title: "GHOSTDAG"
weight: 30
---

GHOSTDAG is a proof-of-work consensus protocol in which each new block references every block its miner knows of that nothing references yet. The blocks therefore form a [directed acyclic graph](/wiki/cs/dag) (DAG) where Bitcoin has a single chain, and no block is thrown away. The protocol's job is to turn that graph into one ordered list of blocks that every node computes identically, with blocks from miners who followed the rules placed ahead of blocks an attacker built in secret.

It does this by colouring. Blocks that are well connected to one another are coloured *blue* and the rest *red*, and the order favours blue blocks. A parameter *k* sets what "well connected" means, and is chosen from how many blocks the network is expected to produce during one network delay.

Sompolinsky, Wyborski and Zohar published it as the practical form of a protocol called PHANTOM. The [Kaspa](#on-kaspa) network runs it at ten blocks per second. With *k* = 0 it reduces to Bitcoin's rule: "the longest chain is, by definition, the largest 0-cluster of the DAG."

## Why keep every block

In a chain, two blocks found at the same moment conflict, and one is discarded. Raising the block rate raises the number of discarded blocks, and the [wasted work weakens the chain](/wiki/economics/defi/consensus/nakamoto-consensus#block-rate-is-bounded-by-propagation). [GHOST](/wiki/economics/defi/consensus/ghost) counts the discarded blocks when choosing a chain but still discards their contents.

Here both blocks stay: "even when two blocks contain conflicting transactions, both blocks are incorporated into the blockDAG and referenced by all (honest) miners." Conflicts are settled afterwards, between transactions, once the blocks have an order.

## Past, future and anticone

Each block names earlier blocks as its parents. For a block *B*:

- its **past** is every block reachable from *B* by following parent references, all provably created before it;
- its **future** is every block from which *B* is reachable, all provably created after it;
- its **anticone** is everything else: blocks that neither reference *B* nor are referenced by it, directly or through other blocks.

```text
            ┌── B ◄── D ◄──┐
genesis ◄───┤              ├── F
            └── C ◄── E ◄──┘
```

In this graph the anticone of *B* is {*C*, *E*}. Nothing in the references says whether *B* came before *C*. The paper calls ordering a block against its anticone "the main challenge that we face".

The size of a block's anticone says something about how it was made. Suppose every block reaches every miner within *D* seconds. An honest block mined at time *t* references everything published before *t* − *D*, and everything mined after *t* + *D* references it. The honest blocks in its anticone are only those made in the window between, and proof of work limits how many blocks can be made in a window of that length. An attacker's secret chain is different. Its blocks reference none of the honest blocks made meanwhile and are referenced by none of them, so their anticones are large.

## Colouring

A set of blocks is a *k-cluster* if every block in it has at most *k* other members of the set in its anticone. Honest blocks, by the argument above, form a *k*-cluster for a suitable *k*.

PHANTOM colours blue the largest *k*-cluster in the graph. Finding it is NP-hard, which makes PHANTOM impractical for a graph that grows without end. GHOSTDAG finds a *k*-cluster greedily. Each block has a *selected parent*: the parent with the most blue blocks in its past. The block inherits that parent's blue set and then adds blocks from outside the selected parent's past, one at a time, keeping only those that leave the set a *k*-cluster. Following selected parents back from the newest block to the first traces a single chain through the graph, which plays the part Bitcoin's main chain does.

The paper describes red blocks as "outliers that were most likely mined by malicious or strategic nodes". The colour is a judgement from connectivity and is not proof of intent. An honest block that propagated slowly can be red.

## Ordering

The order is built along the same chain. A block's order is its selected parent's order, then the selected parent, then the remaining blocks outside that parent's past in an order consistent with their references. Red blocks are placed in the order too.

Transactions are then read off in block order, and each is accepted if it is consistent with those accepted before it. A transaction that conflicts with an earlier one is skipped. Its block stays in the graph.

## Choosing k

*k* is hard-coded, and changing it takes a hard fork. It is computed from an assumed upper bound on network delay, the block rate, and a tolerance δ, as the smallest value for which an honest block's anticone exceeds *k* with probability below δ.

The security result depends on that assumed bound being right. If the real delay is no larger than the assumed one, the paper proves that GHOSTDAG's ordering withstands an attacker with up to 1/2 · (1 − δ) of the computing power. If the real delay is larger, honest blocks start to fall outside the blue set and the guarantee no longer applies. The proof covers GHOSTDAG only. Of PHANTOM the paper says "We leave the formal analysis of PHANTOM for future work."

A larger *k* costs confirmation time: "A large k leads to slow confirmation times". The block rate has a ceiling for a different reason, which is that every node has to receive every block: "λ cannot be increased indefinitely, or otherwise the network becomes congested."

## On Kaspa

Kaspa's mainnet launched in November 2021 at one block per second. Its Crescendo hard fork, specified in Kaspa Improvement Proposal 14 (KIP-14) and activated on 5 May 2025, raised the rate to ten blocks per second. *k* went from 18 to 124 with it. Both values come from one of the two terms in the paper's formula, the one bounding the chance of a large anticone, with an assumed delay bound of 5 seconds and δ = 0.01. Kaspa's node does not compute the formula's other term, so the paper's theorem is not a statement about these exact parameters. Those were still the parameters in the node software in October 2026.

The proposed successor is DAGKnight, by Sutton and Sompolinsky, which removes the hard-coded *k*. Its paper describes "the first permissionless protocol which contains no a priori in-protocol bound over latency", so confirmation speeds up when the network is fast. The bound does not vanish. It moves to the user: "we require that the client specifies locally an upper bound over the maximum adversarial recent latency in the network". As of October 2026 the Kaspa proposal to adopt it, KIP-2, had the status Proposed.

## Sources

- Sompolinsky, Wyborski & Zohar, [PHANTOM GHOSTDAG: A Scalable Generalization of Nakamoto Consensus](https://eprint.iacr.org/2018/104) (revision of November 2021)
- Sutton & Sompolinsky, [The DAG KNIGHT Protocol: A Parameterless Generalization of Nakamoto Consensus](https://eprint.iacr.org/2022/1494) (2022)
- Kaspa, [KIP-14: The Crescendo Hardfork](https://github.com/kaspanet/kips/blob/master/kip-0014.md) and [KIP-2](https://github.com/kaspanet/kips/blob/master/kip-0002.md), read 10 October 2026
- Kaspa, [rusty-kaspa consensus parameters](https://github.com/kaspanet/rusty-kaspa/blob/master/consensus/core/src/config/params.rs), read 10 October 2026
- Kaspa, [project history](https://kaspa.org/lore), read 10 October 2026
