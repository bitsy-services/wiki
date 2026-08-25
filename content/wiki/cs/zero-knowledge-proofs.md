---
title: "Zero-Knowledge Proofs"
weight: 30
---

A zero-knowledge proof (ZKP) is a cryptographic protocol that allows one party (the **prover**) to convince another party (the **verifier**) that a statement is true, without revealing any information beyond the truth of the statement itself.

## Three properties

A protocol qualifies as a zero-knowledge proof if it satisfies:

1. **Completeness.** If the statement is true and both parties follow the protocol honestly, the verifier will be convinced.
2. **Soundness.** If the statement is false, no cheating prover can convince an honest verifier (except with negligible probability).
3. **Zero-knowledge.** If the statement is true, the verifier learns nothing beyond the fact that it is true. Formally, anything the verifier could compute from the interaction, it could also compute without the interaction -- the proof can be *simulated*.

## The cave analogy

The classic illustration uses a circular cave with a locked door blocking the path at the far end. Peggy (the prover) claims to know the secret that opens the door. Victor (the verifier) wants to be convinced without learning the secret.

1. Peggy enters the cave and randomly takes path A or path B.
2. Victor, who cannot see which path Peggy chose, calls out which path he wants her to return by.
3. If Peggy knows the secret, she can always comply -- opening the door if necessary to reach the requested exit.
4. If she does not know the secret, she can only comply when Victor happens to name the path she already took -- a 50% chance.

After *n* rounds, a faker's probability of success is (1/2)^n. After 20 rounds, that is roughly one in a million. Victor becomes convinced Peggy knows the secret, yet he has learned nothing about what the secret is -- each individual round reveals only that Peggy exited from a particular side, which he could have staged himself with a coin flip.

## Interactive vs. non-interactive

The cave example is an **interactive** proof -- it requires real-time back-and-forth between prover and verifier. That rules out any verifier that is not a live counterparty: every [blockchain](/wiki/economics/finance/defi/blockchain) node would have to join the conversation in real time.

**Non-interactive zero-knowledge proofs (NIZKs)** remove the interaction requirement. The prover generates a single proof string that anyone can verify independently. The Fiat-Shamir heuristic is the standard technique for converting an interactive proof into a non-interactive one: the verifier's random challenges are replaced by hash function outputs derived from the prover's commitments.

Most modern ZKP systems are non-interactive. They fall into two broad families:

- **zk-SNARKs** (Zero-Knowledge Succinct Non-Interactive Arguments of Knowledge) -- produce small, fast-to-verify proofs but typically require a trusted setup ceremony. A [Groth16](/wiki/economics/finance/defi/groth16) proof is three group elements regardless of how large the circuit is, which is what Zcash's Sapling circuit and the circom/snarkjs toolchain emit.
- **zk-STARKs** (Scalable Transparent Arguments of Knowledge) -- avoid trusted setup by relying on hash functions rather than elliptic-curve pairings, at the cost of larger proof sizes.

## Applications

### Privacy-preserving transactions

[Cryptocurrency](/wiki/economics/finance/defi/cryptocurrency) systems like Zcash use zk-SNARKs to prove that a transaction is valid (correct balances, authorized sender) without revealing the sender, receiver, or amount. The [blockchain](/wiki/economics/finance/defi/blockchain) records only the proof, not the transaction details.

### Rollups

On [Ethereum](/wiki/economics/finance/defi/ethereum), ZK rollups batch hundreds or thousands of transactions off-chain, compute the resulting state, and post a single zero-knowledge proof to the main chain. The proof convinces the on-chain verifier that all batched transactions were executed correctly, without re-executing them. Verification costs the same whether the batch held ten transactions or ten thousand, so the per-transaction cost on the base layer falls with batch size while settlement still happens there.

### Authentication

A prover can demonstrate knowledge of a password or private key without transmitting it. This eliminates the risk of credential interception and removes the need for the verifier to store the secret at all.

### Verifiable computation

A weak client can outsource an expensive computation to an untrusted server and verify the result with a ZKP, spending far less effort on verification than the original computation required. This has applications in [oracle](/wiki/economics/finance/defi/oracle-node) networks, cloud computing, and auditable machine learning.
