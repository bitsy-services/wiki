---
title: "Proof of Elapsed Time"
weight: 80
---

Proof of elapsed time is a way of choosing who produces the next block by having every validator wait for a random length of time, with the shortest wait winning. The waiting is supervised by a [*trusted execution environment*](/wiki/economics/defi/smart-contract/tee): a protected region of a processor, called an enclave, whose code the machine's owner cannot alter and whose outputs the processor signs. The enclave draws the wait time, and when the time has passed it issues a signed certificate saying so. The validator presents that certificate as its right to publish the block.

The design reproduces the lottery of [proof of work](/wiki/economics/defi/sybil-resistance/proof-of-work) without the work. In Bitcoin the time a miner takes to find a block is random, and whoever is first wins. Here the random delay is assigned directly and nothing is computed while it runs. The scarce resource is the processor itself. In the specification's words, "the probability of election is proportional to the resources contributed (in this case, resources are general purpose processors with a trusted execution environment)."

It was built for Hyperledger Sawtooth, an enterprise blockchain platform, on Intel's Software Guard Extensions (SGX). Sawtooth is now archived, and the mechanism is of interest mainly for what it shows about resting a consensus on trusted hardware.

## The lottery

The specification gives the procedure in a few lines: "Individual peers sample an exponentially distributed random variable and wait for an amount of time dictated by the sample. The peer with the smallest sample wins the election."

Two functions inside the enclave carry it out.

- One creates a timer for a proposed block, with a duration drawn by the enclave.
- The other checks that the timer was created by the enclave and has expired, and if so produces "an attestation that can be used to verify that validator did wait the allotted time before claiming the leadership role."

Other validators accept a block if its certificate carries a valid attestation. They do not need to trust the validator that produced it. They need to trust that the certificate could only have come from a real enclave running the real code.

## What is being trusted

Three things stand behind that certificate.

**The enclave's isolation.** The validator's operator controls the machine and would like a shorter wait. The scheme holds only if the operator cannot read or change what happens inside the enclave.

**The manufacturer's attestation.** A validator joins by proving to the others that it runs the correct code in a real enclave, and the proof is checked through Intel's attestation service. Validators whose hardware keys Intel has revoked are excluded. Intel is therefore a party to the consensus.

**A statistical backstop.** The specification expects that an enclave might be broken and adds a check on outcomes. Each validator's wins are compared with the number expected by chance: "A z-test is used to test the hypothesis that a validator won elections at a higher average rate than expected." A validator that wins too often is refused. The specification's claim is that a compromised platform "cannot affect the correctness of the system, but can hinder progress". The test limits how often one identity can win. It does not detect that an enclave is compromised, and an attacker with several compromised machines appears as several validators each winning at an unremarkable rate.

## Why it did not last

The attack surface is the hardware, and the hardware was attacked. In 2018 the Foreshadow paper presented "a practical software-only microarchitectural attack that decisively dismantles the security objectives of current SGX implementations". Its authors extracted "full cryptographic keys from Intel's vetted architectural enclaves", including the keys used for attestation, and used them for "forging arbitrary local and remote attestation responses". A forged attestation is exactly what a dishonest validator would need here: a wait certificate for a wait that never happened. The paper names blockchain systems among those threatened. Intel issued mitigations afterwards.

The platform also narrowed. Intel's datasheet for its 12th-generation Core processors lists SGX among technologies the processor "has deprecated" and that "are no longer supported". A scheme whose unit of voting power is an ordinary desktop processor with an enclave has no such unit on that generation of Intel's desktop processors.

Hyperledger Sawtooth's own repository now describes it in the past tense, "Hyperledger Sawtooth was a project", and says it "has been archived and is no longer active within Hyperledger". The last change there was in February 2024. The same page says the code is now maintained by a separate group, the Splinter community.

Sawtooth also shipped a version of the lottery that simulated the enclave in ordinary software, for development. The specification says this "forgoes Byzantine fault tolerance": without real hardware, nothing stops a validator from lying about its wait.

## What it leaves behind

The idea outlived the implementation in two respects.

It makes plain what proof of work's puzzle is for. The puzzle is a way to get an unpredictable, unforgeable delay out of machines that nobody trusts. If a trusted party can supply the delay, the puzzle is unnecessary, and the system is then exactly as secure as that party.

And trusted hardware remains in use on blockchains for a different purpose. The enclave can keep a contract's data confidential while leaving consensus to some other mechanism. [Sapphire](/wiki/economics/defi/chains/sapphire) is an example.

The name is also used for an unrelated construction. The Spacemesh network called its sequential-computation servers "proof of elapsed time". That was a proof that computation had been done one step after another for a period, with no trusted hardware involved, and is described under [proof of space](/wiki/economics/defi/sybil-resistance/proof-of-space#three-uses-of-one-name).

## Sources

- Hyperledger Sawtooth, [PoET 1.0 Specification](https://github.com/hyperledger-archives/sawtooth-core/blob/1-0/docs/source/architecture/poet.rst), and the [sawtooth-core README](https://github.com/hyperledger-archives/sawtooth-core/blob/main/README.md), read 10 October 2026
- Van Bulck et al., [Foreshadow: Extracting the Keys to the Intel SGX Kingdom with Transient Out-of-Order Execution](https://foreshadowattack.eu/foreshadow.pdf) (2018)
- Intel, [12th Generation Intel Core Processors Datasheet, Volume 1 of 2](https://cdrdv2.intel.com/v1/dl/getContent/655258), revision 011 (May 2025)
