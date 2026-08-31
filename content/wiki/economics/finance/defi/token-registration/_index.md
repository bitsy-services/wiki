---
title: "Token Registration"
weight: 70
bookCollapseSection: true
---

[ERC-20](/wiki/economics/finance/defi/ethereum/erc-20) specifies `name()`, `symbol()` and `decimals()`. It specifies no icon, no website, no description, and no way to record who deployed the contract. Every logo that has ever appeared beside a token balance came from an off-chain database keyed by chain identifier and contract address, maintained by a company with its own form, its own acceptance criteria, and its own queue.

So "registering a token" is not one action. It is six or seven submissions to organizations that do not share data with each other, three of which will reject a contract deployed this month on principle. The work splits cleanly in two: the parts you can do yourself on the day you deploy, and the parts that require somebody else to approve you.

## What each surface actually reads

| Surface | Where its icon comes from |
| --- | --- |
| Uniswap and most swap interfaces | a [token list](/wiki/economics/finance/defi/token-registration/token-lists) the user has enabled |
| MetaMask token detail and search | MetaMask's token service, sourced from the [data aggregators](/wiki/economics/finance/defi/token-registration/aggregators) |
| MetaMask after [`wallet_watchAsset`](/wiki/economics/finance/defi/token-registration/on-chain-metadata#pushing-the-icon-at-the-wallet) | the image URL your dapp passed in the prompt |
| Etherscan token page | the [explorer's](/wiki/economics/finance/defi/token-registration/block-explorers) own submission form |
| Trust Wallet | the [`trustwallet/assets`](/wiki/economics/finance/defi/token-registration/wallet-registries) repository |
| Dexscreener, DEXTools | their own paid profile products; the trading pair itself appears automatically |
| CoinGecko, CoinMarketCap | their listing forms, which most other trackers then copy |

The redundancy is the reason a token can carry a correct logo on Etherscan and a blank grey circle in a wallet on the same afternoon. Nothing propagates. Each row is a separate application.

## The gating structure

Three prerequisites unlock most of the rest, and they unlock in a fixed order.

```text
  deploy
    │
    ├─ verify the source on the explorer ──► explorer token update (free)
    │                                        │
    │                                        └─► ownership proof reusable
    │                                            for later edits
    ├─ create a pool with real liquidity ──► Dexscreener / DEXTools listing
    │                                        (automatic; profile is paid)
    │                                        │
    │                                        └─► CoinGecko and CoinMarketCap
    │                                            will now accept a submission
    │                                            │
    │                                            └─► MetaMask, portfolio
    │                                                trackers, and the
    │                                                Trust Wallet criteria
    └─ publish a token list + wallet_watchAsset ──► works on day one,
                                                    asks nobody
```

CoinGecko requires the asset to be trading on a venue it already tracks, which for a new token means a [decentralized exchange](/wiki/economics/finance/defi/dex) pool with non-trivial [liquidity](/wiki/economics/finance/defi/liquidity-pool). Trust Wallet requires a CoinMarketCap listing plus 10,000 holders. That chain — pool, then aggregator, then wallet registry — is why the wallet-registry route is realistically months away from a launch, and why the self-service routes are worth doing first rather than last.

## Assemble the packet once

Every form below asks for the same nine things in a slightly different shape. Write them down before you open the first one, because several forms cannot be edited after submission.

- **Contract address**, in [EIP-55](https://eips.ethereum.org/EIPS/eip-55) checksummed form, and the chain identifier (1 for Ethereum mainnet, 8453 for Base, and so on). EIP-55 encodes a checksum in the *letter casing* of the hex digits, which is why a checksummed address looks like a random mix of cases and why several registrars treat a case-only difference as a different string. `cast to-check-sum-address` produces it.
- **Name, symbol, decimals**, exactly as the contract returns them. A mismatch is the most common rejection.
- **Logo**, in the several sizes and formats the registrars demand — see [making the icon](/wiki/economics/finance/defi/token-registration/icon).
- **Description**, 2–4 sentences, written flat. Etherscan rejects superlatives and comparative claims outright.
- **Website**, live, on your own domain, with the contract address published on it. Reviewers check that the address on your site matches the one in the form; this is the cheapest anti-impersonation test they have.
- **Contact email at that domain.** A Gmail address gets the submission deprioritized or dropped.
- **Social links** — X, Discord, Telegram, GitHub — that exist and have posts.
- **Supply figures**: total, circulating, and the vesting or lock schedule that explains the gap.
- **Audit report** and, if applicable, the [liquidity lock](/wiki/economics/finance/defi/locked-liquidity) transaction.

## Order of operations

1. Deploy, then **verify the source** on the block explorer for every chain you deployed to. Nothing else proceeds until this is done.
2. Render the icon assets and publish them at a stable URL — your own domain, [IPFS](/wiki/cs/ipfs), or [Arweave](/wiki/economics/finance/defi/arweave). Every later form asks for a link, not an upload.
3. Publish a [token list](/wiki/economics/finance/defi/token-registration/token-lists) at a URL you control, and wire `wallet_watchAsset` — the wallet method that prompts a user to add a token — into your own interface. Both work immediately.
4. Submit the [explorer token update](/wiki/economics/finance/defi/token-registration/block-explorers). Free, and once per chain.
5. Seed the pool, then submit to [CoinGecko and CoinMarketCap](/wiki/economics/finance/defi/token-registration/aggregators). Expect two to six weeks.
6. Once the holder and transaction counts qualify, submit to the [wallet registries](/wiki/economics/finance/defi/token-registration/wallet-registries).

Consider putting the [ERC-1046](/wiki/economics/finance/defi/token-registration/on-chain-metadata) `tokenURI` on the contract at step 1. It is one immutable string, it costs deployment gas and nothing else, and it is the only metadata that no company can revoke or lose.

## The part nobody's form fixes

Curated lists are also the entire defence against [fake tokens](/wiki/economics/finance/fraud/fake-token): a contract can claim any name and symbol it likes, so a logo beside a balance is a statement about who filled in a form, not about who deployed the contract. Getting your own token registered raises the cost of impersonating it — an impostor now has to clear the same queues — but it does not stop one from being deployed. Identity remains the address.

## Wiki Pages

{{< section >}}
