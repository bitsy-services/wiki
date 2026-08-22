---
title: "Groth16"
weight: 62
---

Groth16 is a zero-knowledge proof system -- specifically, a zk-SNARK (zero-knowledge Succinct Non-interactive ARgument of Knowledge). It allows a prover to convince a verifier that a computation was performed correctly, without revealing the computation's inputs, and the verifier can check this in constant time regardless of how complex the original computation was.

Groth16 is the most widely deployed zk-SNARK in production [blockchain](/wiki/economics/finance/defi/blockchain) systems. It powers the shielded transactions in Zcash, underpins several zk-rollup designs on [Ethereum](/wiki/economics/finance/defi/ethereum/), and is used in cross-chain bridges, privacy protocols, and identity systems.

## Intuition

Imagine you solved a Sudoku puzzle and want to prove it to someone without showing the solution. A zero-knowledge proof lets you do exactly this -- the verifier becomes convinced the solution is valid but learns nothing about what the solution actually is.

Groth16 generalizes this: any computation that can be expressed as an arithmetic circuit (additions and multiplications over a finite field) can be proven and verified. The proof is tiny (three elliptic curve points, roughly 128 bytes) and verification is fast (a handful of pairing operations), no matter how large the circuit.

## How it works

### Step 1: Express the computation as a circuit

The computation to be proven is written as an arithmetic circuit -- a directed acyclic graph of addition and multiplication gates over a prime field. In practice, developers write circuits in domain-specific languages like Circom or use libraries like Arkworks.

The circuit is then converted to a Rank-1 Constraint System (R1CS), a set of constraints of the form:

**a** · **b** = **c**

where **a**, **b**, and **c** are linear combinations of the circuit's variables (inputs, outputs, and intermediate wires). Every valid execution of the circuit satisfies all constraints simultaneously.

### Step 2: Trusted setup

Groth16 requires a per-circuit trusted setup ceremony. This generates a pair of structured reference strings -- the **proving key** and the **verification key** -- derived from secret randomness (often called "toxic waste").

The ceremony works as follows:

1. A participant generates random field elements τ, α, β, γ, δ.
2. These are used to compute encrypted evaluations of polynomials at τ on an elliptic curve (points of the form [τ^i]₁ and [τ^i]₂ in the two groups of a pairing-friendly curve).
3. The raw randomness is destroyed. If any single participant in a multi-party ceremony honestly destroys their contribution, the setup is secure.

The security assumption is that the toxic waste is never reconstructed. If it were, an attacker could forge proofs -- convincing the verifier of false statements. Multi-party computation ceremonies (like Zcash's "Powers of Tau") mitigate this by requiring only one honest participant.

### Step 3: Proof generation

Given a valid witness (the private inputs that satisfy the circuit), the prover computes three elliptic curve group elements:

- **A** ∈ G₁
- **B** ∈ G₂
- **C** ∈ G₁

These are computed from the witness, the proving key, and random blinding factors that ensure zero-knowledge. The proof π = (A, B, C) is roughly 128 bytes regardless of the circuit size.

### Step 4: Verification

The verifier checks the proof using a pairing equation:

**e(A, B) = e(α, β) · e(∑ public_inputs, γ) · e(C, δ)**

where e is a bilinear pairing on the chosen elliptic curve (typically BN254 or BLS12-381). This equation holds if and only if the prover knew a valid witness. Verification requires a fixed number of pairing operations and is independent of the circuit's complexity.

On [Ethereum](/wiki/economics/finance/defi/ethereum/), the BN254 pairing is available as a precompiled contract ([EIP](/wiki/economics/finance/defi/ethereum/eip)-196 and EIP-197), making Groth16 verification cost roughly 200,000--300,000 gas -- cheap enough for on-chain use.

## Where Groth16 is used

### Zcash shielded transactions

Zcash was the first major deployment of Groth16. Shielded transactions prove that a spend is valid (the sender owns the notes, the amounts balance) without revealing sender, receiver, or amount.

### zk-Rollups

Several Ethereum L2 rollups use Groth16 (or plan to) for proving batch validity. The rollup operator executes thousands of transactions off-chain, generates a Groth16 proof that the state transition is correct, and posts only the proof on-chain. The L1 [smart contract](/wiki/economics/finance/defi/smart-contract) verifies the proof and accepts the new state root.

### Cross-chain bridges

Groth16 enables trustless bridging: a contract on one chain can verify that an event occurred on another chain without relying on an [oracle](/wiki/economics/finance/defi/oracle-node) or multisig bridge. The proof is generated off-chain from the source chain's state and verified on-chain at the destination.

### Privacy protocols

Tornado Cash and similar mixers used Groth16 to prove that a withdrawal corresponds to a valid deposit without linking the two. The proof confirms membership in a Merkle tree of deposits without revealing which leaf.

## Comparison with other proof systems

| System | Trusted setup | Proof size | On-chain verification cost | Notes |
|--------|--------------|-----------|--------------------------|-------|
| **Groth16** | Per-circuit ceremony | ~128 bytes | ~200--300k gas | Smallest proof, cheapest verification |
| **PLONK** | Universal (one-time) | ~400--500 bytes | ~500k+ gas | Reusable setup across circuits |
| **Halo 2** | None | ~5--10 KB | Not yet practical on-chain | Recursive composition, no trusted setup |
| **STARKs** | None | ~50--200 KB | Very expensive on-chain | Quantum-resistant, used off-chain or with proof recursion |

Groth16's advantage is its minimal proof size and verification cost. Its disadvantage is the per-circuit trusted setup -- changing the circuit requires a new ceremony. Systems like PLONK trade slightly larger proofs for a universal setup, and STARKs eliminate the trusted setup entirely at the cost of much larger proofs.

## Tooling

The most common development stack for Groth16:

- **Circom** -- a domain-specific language for writing arithmetic circuits, compiled to R1CS.
- **snarkjs** -- a JavaScript library that handles trusted setup, proof generation, and Solidity verifier generation.
- **ZoKrates** -- an alternative higher-level toolkit for writing and compiling zk-SNARK programs.

A typical workflow: write a circuit in Circom, compile it, run a trusted setup with snarkjs, generate proofs from witnesses, and deploy a Solidity verifier contract that exposes a `verifyProof()` function.

## External links

- [On the Size of Pairing-based Non-interactive Arguments](https://eprint.iacr.org/2016/260) -- the original Groth16 paper by Jens Groth
- [Circom documentation](https://docs.circom.io/) -- circuit language used with Groth16
- [snarkjs repository](https://github.com/iden3/snarkjs) -- JavaScript tooling for Groth16 proof generation and verification
- [Why and How zk-SNARK Works](https://arxiv.org/abs/1906.07221) -- accessible explanation of the cryptographic foundations
