---
title: "Trusted Execution Environment"
weight: 12
---

A **trusted execution environment (TEE)** is a secure area of a processor that runs code and holds data inside a hardware-isolated *enclave*. Code executing in the enclave is shielded from everything outside it — including the operating system, the hypervisor, and anyone with physical access to the machine. Memory is encrypted by the CPU and only decrypted inside the enclave boundary, so even a fully compromised host cannot read the enclave's working state.

A TEE provides **confidential computation**: a program processes secret inputs and produces results without the machine operator ever seeing the secrets in the clear. This is a different guarantee from a [zero-knowledge proof](/wiki/cs/zero-knowledge-proofs), which proves a statement is true while revealing nothing — a ZKP convinces a verifier *about* a computation, whereas a TEE *performs* the computation privately inside sealed hardware.

## Remote Attestation

A party that is not sitting at the machine gets its handle on all this through **attestation**: the CPU produces a signed *quote*, a hardware-rooted statement of exactly what code is running inside the enclave (its measurement hash) and that the silicon is genuine and up to date. The client verifies that quote against the manufacturer's certificate chain before sending the enclave any secrets. Without it there is nothing to distinguish an enclave from a logging shim that answers the same way.

## Implementations

- **Intel SGX** (Software Guard Extensions) — application-level enclaves; the long-standing basis for confidential-computing platforms.
- **Intel TDX** (Trust Domain Extensions) — newer, VM-level confidentiality (a whole guest VM as a trust domain), easier to port existing workloads into.
- **AMD SEV-SNP** (Secure Encrypted Virtualization) and **ARM TrustZone / CCA** (Confidential Compute Architecture) — comparable approaches from other vendors.

## Trust Model and Limitations

A TEE moves trust from the host operator to the **chip manufacturer** and its attestation service: the assumption is that Intel, AMD, or ARM built the hardware correctly and still holds its signing keys. TEEs also have a long history of **side-channel attacks** (Foreshadow, Plundervolt, SGAxe, and others) that extract enclave secrets by observing timing, power, speculative execution, or memory-access patterns. Mitigations ship continuously, but TEE confidentiality should be treated as *strong in practice, not unconditional*.

In the blockchain world, TEEs underpin [confidential smart contracts](/wiki/economics/finance/defi/sapphire) — most prominently [Oasis Sapphire](/wiki/economics/finance/defi/sapphire), the confidential [EVM](/wiki/economics/finance/defi/ethereum/) — as well as confidential off-chain compute, trusted oracles, and key-management services.

## External Links

- [Wikipedia: Trusted Execution Environment](https://en.wikipedia.org/wiki/Trusted_execution_environment)
- [Confidential Computing Consortium](https://confidentialcomputing.io/) — vendor-neutral standards body
- [Intel SGX overview](https://www.intel.com/content/www/us/en/developer/tools/software-guard-extensions/overview.html)
- [Intel TDX overview](https://www.intel.com/content/www/us/en/developer/tools/trust-domain-extensions/overview.html)
- [A Survey of Published Attacks on Intel SGX (arXiv)](https://arxiv.org/abs/2006.13598)
