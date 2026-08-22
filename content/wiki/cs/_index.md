---
title: "Computer Science"
weight: 20
bookCollapseSection: true
---

The durable ideas underneath the rest of the wiki -- the ones that keep resurfacing in different clothes. This section is deliberately not a survey. Each page exists because the concept turned out to matter somewhere concrete, and the theory is easier to write down once than to re-derive every time it comes up.

Cryptographic *theory* lives here; the operational business of handling keys and secrets on a real machine is in [Security](/wiki/security).

## Structure and representation

[Directed acyclic graphs](/wiki/cs/dag) get a section of their own: acyclicity is a single constraint that buys topological ordering, memoisation, and incremental rebuilds, which is why build systems, schedulers, version control, and distributed ledgers all converge on the same shape.

[Entity addressing](/wiki/cs/entity-addressing) names a tension that runs through databases, domain modelling, language design, and web architecture: are your entities rows inside a container, or first-class objects with their own identity? The mismatch between layers that answered differently is what object-relational mapping (ORM) impedance and REST-over-RPC adapters are made of.

[IPFS](/wiki/cs/ipfs) is what content addressing looks like when it is the whole design: name data by the hash of its contents rather than by where it sits, and a [Merkle DAG](/wiki/cs/dag) follows necessarily. It sits here rather than under DeFi because the durable idea is the addressing scheme, not the storage market built on it -- though most of the pages that link here are on the DeFi side, and [Arweave](/wiki/economics/finance/defi/arweave) is its natural sibling.

[Homoiconicity](/wiki/cs/homoiconicity) is the property of a language whose programs are written in its own data structures -- code and data sharing one form, so the language can rewrite itself with ordinary tools.

## Cryptography

[Zero-knowledge proofs](/wiki/cs/zero-knowledge-proofs) let a prover convince a verifier that a statement is true while revealing nothing else. This is the theory behind [Groth16](/wiki/economics/finance/defi/groth16) and, more broadly, behind the ZK-rollups that most [Ethereum](/wiki/economics/finance/defi/ethereum) scaling now runs through.

## Canonicalization

Two pages on a class of bug worth recognising on sight. A [canonicalization attack](/wiki/cs/canonicalization-attack) exploits two components disagreeing about what an input *means* -- one normalises, the other doesn't, or they normalise differently, and an attacker crafts something that reads as safe to the checker and dangerous to the executor. [Canonicalization attacks on signed XML](/wiki/cs/canonicalization-attacks-on-signed-xml) is the worked case, and the reason so many SAML (Security Assertion Markup Language) implementations have been broken the same way: the signature covers what the canonicaliser saw, and the application acts on what the parser produced.

## Wiki Pages

{{< section >}}
