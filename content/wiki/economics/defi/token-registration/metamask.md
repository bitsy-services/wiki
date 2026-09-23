---
title: "Registering on MetaMask"
weight: 160
---

MetaMask has no listing form. The name and icon it shows for a token come from its Token API, a MetaMask service that merges token lists from a dozen or more third parties — swap routers, bridges, [CoinGecko](/wiki/economics/defi/token-registration/coingecko), [CoinMarketCap](/wiki/economics/defi/token-registration/coinmarketcap), Trust Wallet — and counts, for each token on each chain, how many of those lists carry it. A token on enough of them is detected automatically in a user's wallet; the default threshold in MetaMask's current code is three. Getting a token in front of MetaMask users therefore means one of three things: be on enough upstream lists, get an entry into MetaMask's own `contract-metadata` repository, which counts as one of those lists, or have your own interface call [`wallet_watchAsset`](/wiki/economics/defi/token-registration/on-chain-metadata#pushing-the-icon-at-the-wallet), which needs nobody's approval.

## What the Token API returns

For a token that is on the lists:

```bash
curl -s "https://token.api.cx.metamask.io/token/1?address=0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"
```

```json
{"address":"0x1f9840a85d5af5bf1d1762f925bdaddc4201f984","symbol":"UNI","decimals":18,"name":"Uniswap",
 "iconUrl":"https://static.cx.metamask.io/api/v1/tokenIcons/1/0x1f9840a85d5af5bf1d1762f925bdaddc4201f984.png",
 "type":"erc20",
 "aggregators":["metamask","liFi","oneInch","rubic","squid","rango","sonarwatch","sushiSwap","trustWallet"],
 "occurrences":9,"storage":{"balance":4,"approval":3},"fees":{"minFee":0,"avgFee":0,"maxFee":0}}
```

`aggregators` names the upstream lists that carry the token, and `occurrences` counts them. `iconUrl` points at MetaMask's own copy of the icon, which is what the wallet renders.

A 200 response is not evidence of a listing. For a token on no list the same endpoint still answers 200, with the name and symbol read from the contract, `"aggregators":["dynamic"]`, and no `iconUrl` or `occurrences`. Only an address that is not a token at all returns `{"statusCode":404,"message":"Token not found"}`. The test is whether real list names appear in `aggregators`.

## The threshold

The list the wallet downloads for detection is `/tokens/<chainId>`, requested with an `occurrenceFloor` parameter. MetaMask's client code, in the `assets-controllers` package of `MetaMask/core`, takes the floor for each chain from a live endpoint and falls back to a constant:

```text
const DEFAULT_OCCURRENCE_FLOOR = 3;
```

```bash
curl -s https://token.api.cx.metamask.io/v1/suggestedOccurrenceFloors
# {"1":3,"143":1,"204":1,"232":1,"690":1,"1329":1,"4663":1,"10143":1,"59144":1,"98866":1}
```

Ethereum is listed at 3. Base, Arbitrum One, OP Mainnet, Polygon and BNB Smart Chain are not listed, so the client uses the fallback of 3 for them too. The detection controller then checks the user's balance of every token on that list and adds the ones with a non-zero balance.

The number users are more likely to have read is two: a 2021 Consensys post said the feature "can auto-detect tokens featured on two or more token lists". MetaMask's current help pages give no number at all.

How the server applies the floor is not documented, and it does not behave like a filter. On 16 September 2026, floors of 1, 3 and 10 on Ethereum returned 8,686, 9,330 and 9,331 tokens, and every response included tokens with a single occurrence. Of the 148 tokens with fewer than three occurrences in the list the wallet downloads, 140 carried `metamask` among their sources. The likely reading — not a published rule — is that an entry in MetaMask's own repository gets a token onto the detection list without meeting the floor.

## Which lists count

The sources differ by chain. On Ethereum, the list carried entries from Rubic, Rango, CoinGecko, SonarWatch, Li.Fi, CoinMarketCap, 1inch, `metamask`, SushiSwap, Ondo, Squid and Trust Wallet, among others; on Base, CoinMarketCap did not appear as a source at all. The sources carrying the most tokens are swap and bridge routers rather than curated lists; how each one decides which tokens to include was not examined here.

A [CoinGecko listing](/wiki/economics/defi/token-registration/coingecko) is therefore one occurrence, not a route on its own. So is a [Trust Wallet](/wiki/economics/defi/token-registration/trust-wallet) entry, and so is an entry in `contract-metadata`.

## `contract-metadata`

`MetaMask/contract-metadata` is a GitHub repository of token icons and metadata. Its README still opens by calling it "effectively frozen" and recommending the `wallet_watchAsset` route, through a link that now returns 404. The repository's activity says otherwise: at least fifteen pull requests were merged between 3 August and 11 September 2026, apparently most by MetaMask staff, and one from an outside contributor was merged on 13 August after about eight weeks and seven follow-up comments. MetaMask's own help article for token developers links to the repository's submission steps. It is open, slow, and discretionary.

The layout keys each file by a CAIP-19 asset identifier — the Chain Agnostic Improvement Proposal format `eip155:<chainId>/erc20:<address>` — with one metadata file and one icon per chain:

```text
metadata/eip155:8453/erc20:0xB095274743941e953c746F9C228DA9c18Bb6ec29.json
icons/eip155:8453/erc20:0xB095274743941e953c746F9C228DA9c18Bb6ec29.png
```

The metadata file is small:

```json
{
  "logo": "./icons/eip155:8453/erc20:0xB095274743941e953c746F9C228DA9c18Bb6ec29.png",
  "name": "Hunter Biden's Laptop",
  "symbol": "LAPTOP",
  "decimals": 18,
  "erc20": true
}
```

The repository's validation script requires `name`, `symbol` (20 characters or fewer), `decimals` (an integer from 0 to 255) and `logo`, and accepts icons as `.svg`, `.png`, `.jpg` or `.jpeg`. The address must be checksummed. `CONTRIBUTING.md` still describes an older `contract-map.json` layout and should be ignored in favour of the README.

The README's criteria for inclusion:

- a link to the project's website, and the website must reference the submitted address and explain the project;
- "clear signs of activity, either traffic on the network, activity on GitHub, or community buzz";
- verified source on a block explorer is "nice to have";
- for an Ethereum asset, a "NEUTRAL" or "OK" reputation on [Etherscan](/wiki/economics/defi/token-registration/etherscan);
- no ERC-721 or ERC-1155 tokens — Ethereum Request for Comment standards for non-fungible and multi-token contracts.

The icon style guide asks for a square artboard, artwork within 80% of the canvas, SVG where possible, and a solid background unless the mark reads clearly on both light and dark themes. It rules out animation, embedded `<image>` elements, `<foreignObject>` and nested `<svg>` elements.

The npm package `@metamask/contract-metadata` last shipped in April 2024 and is used only for a static Ethereum list when detection is switched off. The live Token API is evidently reading something newer: a token merged on 8 September 2026 already listed `metamask` among its sources the following week.

## `wallet_watchAsset`

The route that needs no one's approval is your own interface calling `wallet_watchAsset`, the provider method defined by [Ethereum Improvement Proposal (EIP)](/wiki/economics/defi/chains/ethereum/eip) 747, which prompts the user to add the token with the symbol, decimals and image your code supplies. [On-chain metadata](/wiki/economics/defi/token-registration/on-chain-metadata#pushing-the-icon-at-the-wallet) covers the call. MetaMask's documentation recommends detecting the user's current chain first, since a token added on the wrong network produces "unexpected results". It is the only one of the three routes that works on launch day.

## One address on every chain

Everything here is per chain. The API, the floor, the icon URL and the list membership are all keyed by chain ID, so the same address can have nine sources on Ethereum and none on Base. A `contract-metadata` entry for six chains is twelve files — one metadata file and one icon under each `eip155:<chainId>` folder — with the same address segment in every path. The repository sets no fee and no limit on files per pull request; one merged pull request covered two chains.

## Field map

What the routes need, against the [token property schema](/wiki/economics/defi/token-registration#the-token-property-schema):

| Field | Schema key | Used by |
| --- | --- | --- |
| address in the CAIP-19 path | `address` | `contract-metadata`, once per entry in `chain_ids` |
| `name` | `name` | `contract-metadata` |
| `symbol` | `symbol` | `contract-metadata`, `wallet_watchAsset` |
| `decimals` | `decimals` | `contract-metadata`, `wallet_watchAsset` |
| icon file | `logo_svg`, or `logo_png` | `contract-metadata` (committed file) |
| `image` | `logo_png` | `wallet_watchAsset` (URL or data URI, 512 × 512 and 256 kB at most) |
| website referencing the address | `website` | `contract-metadata` review |

## Check

```bash
curl -s "https://token.api.cx.metamask.io/token/8453?address=0xYourTokenAddress"
```

Look for list names other than `dynamic` in `aggregators`, and for an `iconUrl`. Then fetch the icon itself, with the address in **lowercase** — the checksummed spelling returns 403:

```bash
curl -sI https://static.cx.metamask.io/api/v1/tokenIcons/8453/0xyourtokenaddressinlowercase.png
```

The full detection list for a chain is `https://token.api.cx.metamask.io/tokens/<chainId>`; for Ethereum it was 3.4 MB and 9,330 entries, cached for five minutes.
