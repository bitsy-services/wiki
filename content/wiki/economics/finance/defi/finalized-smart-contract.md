---
title: "Finalized Smart Contract"
weight: 8
---

A finalized smart contract is one that has been deployed to a [blockchain](/wiki/economics/finance/defi/blockchain) with no mechanism for anyone -- including its original developer -- to modify its code or behavior. Once finalized, the contract runs exactly as written for as long as the blockchain exists.

This is the strongest form of the immutability property that makes [smart contracts](/wiki/economics/finance/defi/smart-contract) useful in the first place. A finalized contract cannot be censored, paused, upgraded, or tampered with by governments, corporations, or the developers who wrote it.

## What finalization means in practice

A smart contract on [Ethereum](/wiki/economics/finance/defi/ethereum/) is finalized when all of the following are true:

- **No proxy pattern** -- the contract is not behind an upgradeable proxy. It executes its own logic directly.
- **No admin functions** -- there are no owner-only functions that can change parameters, pause operations, or migrate state.
- **No self-destruct** -- the contract cannot be destroyed by its deployer (note: the `SELFDESTRUCT` opcode was deprecated in [EIP](/wiki/economics/finance/defi/ethereum/eip)-6780, but contracts deployed before the change may still have it).
- **Ownership renounced or absent** -- if the contract inherited an ownership model, ownership has been transferred to the zero address or was never set.

## The upgradability spectrum

Most DeFi contracts are not fully finalized. Instead, they sit somewhere on a spectrum:

| Pattern | Mutability | Tradeoff |
|---------|-----------|----------|
| **Finalized** | None | Maximum trust, zero recourse if a bug is found |
| **Timelock + multisig** | Slow, transparent | Changes are visible days in advance; users can exit |
| **Transparent proxy** | Admin-controlled | Allows bug fixes but requires trust in the admin |
| **UUPS (universal upgradeable proxy standard) proxy** | Admin-controlled | Similar to transparent proxy, slightly more gas efficient |
| **Diamond (EIP-2535)** | Modular | Individual facets can be upgraded independently |
| **Beacon proxy** | Admin-controlled | Multiple proxies upgraded simultaneously via a shared beacon |

The transparent proxy and UUPS patterns are the most common in production DeFi. They allow the development team to fix critical bugs or respond to exploits, but they require users to trust that the admin keys are held securely and used responsibly.

## Why finalization matters

### Fund-loss risk from upgradeable contracts

An upgradeable contract's admin can, in principle, deploy a malicious implementation that drains user funds. Even with a multisig and timelock, this is a trust assumption. Finalized contracts eliminate this vector entirely.

### Censorship resistance

A finalized contract cannot be forced to comply with a court order, sanctions list, or government directive. This was a central issue in the Tornado Cash case -- the protocol's [smart contracts](/wiki/economics/finance/defi/smart-contract) continued to function on-chain even after [OFAC sanctions](/wiki/economics/finance/regulation/ofac-sanctions), because they were finalized and no one had the ability to modify them. The Fifth Circuit ultimately held that an immutable contract is not blockable property at all, and the designation was lifted. See [DeFi US regulatory restrictions](/wiki/economics/finance/defi/defi-us-regulatory-restrictions) for more on the legal implications.

### Composability guarantees

Other protocols that integrate with a finalized contract can rely on its behavior never changing. This is critical for [DeFi](/wiki/economics/finance/defi/dex) composability -- a lending protocol that accepts a certain token as collateral needs to trust that the token contract's transfer logic will not be altered.

## When finalization is appropriate

Finalization is the right choice when the contract's logic is simple, well-audited, and unlikely to need changes:

- **Token contracts** -- [ERC-20](/wiki/economics/finance/defi/ethereum/erc-20) tokens with straightforward transfer logic.
- **Simple vaults** -- contracts that hold funds according to fixed rules (vesting, escrow).
- **Verifier contracts** -- on-chain proof verification with no parameters to tune.

It is a poor choice for complex protocols that may need to respond to discovered vulnerabilities, changing market conditions, or evolving standards.

## External links

- [OpenZeppelin Proxy Patterns](https://docs.openzeppelin.com/contracts/5.x/api/proxy) -- documentation on upgradeable proxy implementations
- [EIP-2535: Diamond Standard](https://eips.ethereum.org/EIPS/eip-2535) -- the multi-facet proxy pattern
- [EIP-6780: SELFDESTRUCT deprecation](https://eips.ethereum.org/EIPS/eip-6780) -- changes to the SELFDESTRUCT opcode
