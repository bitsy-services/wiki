---
title: "Registering on Blockscout"
weight: 90
---

Blockscout is an open-source block explorer, and the company behind it hosts it for many chains, each as a separate instance with its own address such as `eth.blockscout.com`. A token's project information on a Blockscout explorer — logo, description, website, links — comes from one of two places: a [CoinGecko](/wiki/economics/defi/token-registration/coingecko) listing, which Blockscout reads automatically — it queries [CoinMarketCap](/wiki/economics/defi/token-registration/coinmarketcap) too, but for market data — or a token info application submitted to that instance by the token's owner. The application requires a verified contract and a signed ownership proof, takes the logo as a link rather than an upload, and is reviewed either with no guaranteed timeline or, for 99 USDC or USDT, within seven days.

Blockscout is also the one explorer here whose self-serve ownership check is designed to accept a signature from the sender of a factory deployment — confirmed in its web front end, not yet end to end.

## The CoinGecko route

Blockscout's documentation says it "displays what CoinGecko returns", and gives the instruction for a token CoinGecko already tracks: "submit the correction directly to CoinGecko. Blockscout will reflect it automatically once CoinGecko's data updates." By that account, a [CoinGecko listing](/wiki/economics/defi/token-registration/coingecko) reaches every Blockscout instance for the chains in the listing without a per-instance submission. The one record inspected for this page, Uniswap's, does not show the route cleanly — its logo is a CoinGecko image, but its description and link spellings match Trust Wallet's file — so check the project record endpoint under [Check](#check) after a CoinGecko listing before deciding a submission is unnecessary.

An earlier Blockscout announcement, from November 2023, described reading token metadata from the Token Name Service, an Ethereum Name Service–based token registry. Blockscout's current documentation names only the aggregators and manual submission as sources, its public code has no reference to that service, and the registry's application domain no longer resolves. Treat the integration as retired: the registry's documentation and on-chain records remain, but nothing shows Blockscout reading them.

## Proving ownership

Log in to the instance, open the token, choose *Add Token Info* from its menu (or *Verified addrs* in the account), and sign the message the explorer prepares. Blockscout's form accepts a signature from any of three accounts:

- the contract's **creator**, which on Blockscout is the immediate parent — for a contract made by a factory, the factory itself, which cannot sign;
- the address returned by the contract's **`owner()`** function, if it has one;
- the **deployer**, defined in Blockscout's published service types as the "sender of the creation transaction when the contract was deployed by another contract".

The third option arrived in a frontend change merged on 17 August 2026 and live on the instances checked for this page. The corresponding backend work is tracked in a public issue that was still open on 16 September, and the service could not be tested without a login, so the path is documented but unconfirmed end to end. The error message the frontend shows for a wrong signer lists all three: "Only {creator, owner, deployer} can verify ownership of this contract."

The fallback is manual. Blockscout's documentation covers the case where "the original deployer wallet is not accessible or was never yours (for example after a multisig migration, a treasury wallet change, a team handoff, or a factory contract deployment)": email `submissions@blockscout.com` with the wallet, the token information and the relationship to the project, then supply the proof they ask for, "such as a signed message or a post from the project's verified social account."

Once verified, the address stays under *Verified Addresses* in the account and later updates need no new signature.

The source must be verified first; the service's error for an unverified contract is "Contract source code has not been verified." Blockscout's API treats a minimal-proxy clone as verified when its implementation is, but whether the ownership check applies the same rule is not documented.

## The form

The token info application form is open source, so its fields are known exactly:

| Field | Required | Rules | Schema key |
| --- | --- | --- | --- |
| Token name | prefilled | read-only | `name` |
| Token contract address | prefilled | read-only | `address` |
| Requester name, requester email | yes | | — |
| Project name | no | | `name` |
| Project industry | no | one of `Infra & Dev tooling`, `DeFi`, `Data`, `Bridge`, `NFT`, `Payments`, `Faucet`, `DAO`, `Games`, `Wallet`, `Other` | `category` |
| Official project email address | yes | on the project's domain, or the address shown on its website | `email` |
| Official project website | yes | | `website` |
| Docs | no | URL | `links.docs` |
| Support URL or email | no | | `email` |
| Icon URL | yes | a link to an SVG, or to a 48 × 48 PNG | `logo_svg`, or `logo_png` |
| Project description | yes | 300 characters at most, neutral, no unsubstantiated claims | `description` |
| GitHub, X, Telegram, OpenSea, LinkedIn, Facebook, Discord, Medium, Slack, Reddit | no | URLs | `links.*` |
| CoinMarketCap URL, CoinGecko URL, DefiLlama URL | no | URLs | built from `coinmarketcap_id`, `coingecko_id`, `defillama_slug` |
| Comment | no | 300 characters at most | — |
| Payment transaction hash | no | see below | — |

The schema keys refer to the [token property schema](/wiki/economics/defi/token-registration#the-token-property-schema). Blockscout's documentation calls the project email and website "Suggested", while the form's code marks both required; fill them in.

## Cost and review

Without payment, the documentation says, "we cannot guarantee any timeline for review, as we have 1,000s of tokens in the queue." With payment, the team will "review and approve or decline the listing within 7 days":

- The fee is 99 USDC or USDT, and the transaction hash goes in the form. The in-form text also accepts USDG or $99 of ETH.
- The documentation says to pay "on the chain where your token is listed", but publishes payment addresses only for Ethereum, Optimism, Base and Robinhood Chain. The payment block also appears on the Arbitrum, Polygon, Gnosis and Scroll instances, and not on Base's. For a token on any chain other than Ethereum, OP Mainnet, Base or Robinhood Chain, ask Blockscout where to pay before sending anything; the fee is not refunded.
- The fee "does not guarantee your token info will be listed" and is non-refundable; a rejected submission starts again, with a new fee for another expedited review.

The review checks the wallet, looks for duplicates and impersonation — where exact copies exist, "the token with the strongest liquidity, trading volume, and active trader count is treated as official" — and, if the project's website connects to wallets, tests that connection with an empty wallet for unusual permission requests. The listed rejection reasons are payment problems, an unqualified wallet, impersonation, phishing, suspicious wallet permissions, requests for keys or seed phrases, and misleading information. "Every submission is final once sent for review"; follow up on the original thread rather than resubmitting.

## One address on every chain

Every part of the service is keyed by instance: the ownership claim, the submission and the stored record all carry the chain. The documentation does not say so directly, but a token on five Blockscout-hosted chains is, by that design, five claims and five submissions, and five fees if each is expedited. Whether one login spans instances is not documented.

| Chain | Blockscout-hosted explorer |
| --- | --- |
| Ethereum | `eth.blockscout.com` |
| Base | `base.blockscout.com` |
| Arbitrum One | `arbitrum.blockscout.com` |
| OP Mainnet | `explorer.optimism.io`, also `optimism.blockscout.com` |
| Polygon | `polygon.blockscout.com` |
| BNB Smart Chain | none |

Each clone of a factory is its own token and needs its own submission; a clone checked for this page had a verified implementation and no icon.

## Check

The explorer's token endpoint shows the icon it will render:

```bash
curl -s "https://eth.blockscout.com/api/v2/tokens/0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"
```

It returns `name`, `symbol`, `decimals`, `holders_count`, `reputation` and `icon_url`; for Uniswap's token the icon is a CoinGecko image. `null` means no source has supplied one.

The project record behind the token page's information panel needs no key either:

```bash
curl -s "https://contracts-info.services.blockscout.com/api/v1/chains/1/token-infos/0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"
```

It returns the stored project record — `projectName`, `projectWebsite`, `iconUrl`, `projectDescription`, the links, and the price-data URLs. Replace `1` with the chain ID and the address with yours.
