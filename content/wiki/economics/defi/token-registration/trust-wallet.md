---
title: "Registering on Trust Wallet"
weight: 170
---

Trust Wallet takes a token's logo and description from `trustwallet/assets`, a public GitHub repository with one folder per token per chain. Each folder holds exactly two files, `logo.png` and `info.json`, and getting a token in means a pull request that adds them, a fee of 500 TWT — Trust Wallet's own token — or 2.5 BNB per pull request, and a review against criteria that include 10,000 holders. The repository's README states the consequence directly: "brand new tokens are not accepted". For a token launched this month, this page is a description of a milestone rather than a step.

Trust Wallet's own help pages also say where its prices come from — "Trust Wallet sources pricing data from CoinMarketCap (CMC)" — and a [CoinMarketCap listing](/wiki/economics/defi/token-registration/coinmarketcap) is one of the acceptance criteria below, so that submission comes first.

## The folder

```text
blockchains/
  ethereum/
    assets/
      0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984/
        logo.png
        info.json
```

The folder name is the contract address in [Ethereum Improvement Proposal (EIP)](/wiki/economics/defi/chains/ethereum/eip) 55 checksummed form — the mixed-case spelling that encodes a checksum in the letter case. The repository's check compares the folder name against its own checksum computation and fails a lowercase folder. File names are compared as exact strings, so `logo.PNG` and `Info.JSON` fail too, and nothing but those two files may sit in the folder.

A token that is no longer maintained is marked `"status": "abandoned"`, and the documentation says its `logo.png` is removed; the review bot, by contrast, says files "should not be deleted in a PR" and that deprecated tokens "should be deactivated only". Expect the maintainers to handle deprecation.

## `info.json`

The live file for Uniswap's token, in full:

```json
{
    "name": "Uniswap",
    "website": "https://uniswap.org",
    "description": "UNI is the Uniswap protocol token. Uniswap is a decentralized protocol for automated liquidity provision on Ethereum.",
    "explorer": "https://etherscan.io/token/0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
    "research": "https://research.binance.com/en/projects/uniswap",
    "type": "ERC20",
    "symbol": "UNI",
    "decimals": 18,
    "status": "active",
    "id": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
    "tags": ["defi", "governance"],
    "links": [
        { "name": "discord", "url": "https://discord.com/invite/XErMcTq" },
        { "name": "x", "url": "https://x.com/UniswapProtocol" },
        { "name": "blog", "url": "https://uniswap.org/blog/uni/" },
        { "name": "coinmarketcap", "url": "https://coinmarketcap.com/currencies/uniswap/" },
        { "name": "coingecko", "url": "https://coingecko.com/en/coins/uniswap/" }
    ]
}
```

The repository's Go validator requires `name`, `type`, `symbol`, `decimals`, `description`, `website`, `explorer`, `status` and `id`. The rules it enforces on them are narrower than the documentation suggests:

- `id` must equal the folder name, character for character. A case-only difference gets its own error, "invalid case for id field".
- `description` is capped at 600 **bytes** — the check is Go's `len`, so a multi-byte character costs more than one — and may not contain a newline or two consecutive spaces.
- `decimals` must lie between 0 and 30.
- `status` is one of `active`, `spam` or `abandoned`.
- `type` names the chain's token standard, not the token's: `ERC20` on Ethereum, but `BASE` on Base and `BEP20` on BNB Smart Chain. The full mapping is under [one address on every chain](#one-address-on-every-chain).

`links` is an array of `name`/`url` pairs, and the names come from a fixed list of sixteen. Several also fix the start of the URL, which is where most link errors come from:

| `name` | URL must start with |
| --- | --- |
| `x` | `https://x.com/` |
| `github` | `https://github.com/` |
| `telegram`, `telegram_news` | `https://t.me/` |
| `discord` | `https://discord.com/` |
| `reddit` | `https://reddit.com/` |
| `facebook` | `https://facebook.com/` |
| `youtube` | `https://youtube.com/` |
| `coinmarketcap` | `https://coinmarketcap.com/` |
| `coingecko` | `https://coingecko.com/` |
| `medium` | anything containing `medium.com` |
| `whitepaper`, `blog`, `forum`, `docs`, `source_code` | any `https://` URL |

So `https://www.facebook.com/…`, `https://twitter.com/…` and `https://www.coingecko.com/…` all fail, even though each resolves. The check is skipped entirely for a file with fewer than two links, but the documentation calls `links` and `tags` required, and the review bot rejects a file with no tag, so plan on both.

Tags come from a short list — `stablecoin`, `wrapped`, `synthetics`, `nft`, `governance`, `defi`, `staking`, `staking-native`, `privacy`, `nsfw`, `binance-peg`, `deflationary`, `memes`, `gamefi` in the documentation, and three more (`heco-tag`, `pow`, `dapp`) in the live values API. The bot has rejected tags outside it.

### The bot and the check disagree about `x`

Two programs read a pull request: the repository's own continuous-integration check, and a closed-source fee bot. The check accepts `x` and has no `twitter`; the bot's error message lists `twitter` and not `x`, and complains about a link named `x`. The rename from `twitter` to `x` landed in the repository in January 2025. Pull requests using `x` have been merged over the bot's complaint, so use `x` and expect the message.

## The logo

`logo.png`, lowercase, PNG. The documentation recommends 256 × 256 and allows up to 512 × 512; the continuous-integration check accepts anything from 60 to 512 pixels a side and does not insist on a square, a leniency its own source comment attributes to old logos with dimensions like 195×163. Uniswap's own is 240 × 240. Treat 256 × 256 square as the target and the leniency as a thing not to rely on.

The 100 kB ceiling is enforced. The check divides the byte count by 1,024 with integer division and fails anything over 100, so a file must be under 103,424 bytes. [Making the icon](/wiki/economics/defi/token-registration/icon#getting-under-100-kb) covers getting there.

Trust Wallet displays logos through a circular mask. Its guidance is to keep transparency outside the mark only, not inside it.

## The acceptance bar

The requirements page, quoted in full because the list is short and every item is load-bearing:

- **Website & Documentation** — "A live website with a detailed white paper, including a clear roadmap, tokenomics, and use case."
- **Social Media & Support** — "An active social media presence and a responsive support team. Accounts with fake followers or bots will be rejected."
- **Security Audit** — "A completed full audit by a reputable security firm."
- **Originality** — "No plagiarized content, names, or logos from other projects or companies. Tokens that mimic the name, symbol, or branding of established projects and stablecoins (e.g. USDT, USDC, DAI) will be rejected."
- **Price Tracking** — "Token must be listed on CoinMarketCap for price tracking with detailed token information."
- **On-Chain Activity** — "Minimum of 10,000 holders and 15,000 transactions. Airdropped tokens are excluded from these counts. This threshold may be adjusted on a case-by-case basis."

The page adds that meeting all of them "does not guarantee a submission will be accepted". The bot reads holder counts per deployment: on one pull request it reported 564 holders on the Ethereum deployment and 81 on a TRON deployment, each against the 10,000 limit, while the submitter cited 73,000 on BNB Smart Chain. Whether maintainers then apply the rule per chain or per project is not stated anywhere.

## The fee

"A fee of 500 TWT or 2.5 BNB is required for each Pull Request." Payments in TWT are burned. The fee is charged again for any later change — a new logo, a rename — and is not refunded if the pull request is closed. Inclusions made by Trust Wallet's own team carry no fee.

The payment address is not fixed. The bot posts one in a comment on each pull request — a "BEP20 (Binance Smartchain) address" — and four pull requests examined here received four different addresses, so pay on BNB Smart Chain, to the address in your own pull request's comment. Payment is detected automatically after a few minutes and turns into an approving review from the bot, which is a condition of merge; the bot's notes say evaluating the pull request is done manually.

A pull request that goes quiet is closed: one received reminders every twelve hours and was closed after about two days, with the warning "Do NOT send payments for closed PR, as the fee may by lost!"

After a merge, Trust Wallet's help pages say the new logo reaches search within an hour, and that its apps cache images for a few hours on top of that.

## Two ways to open the pull request

A plain fork-and-commit works. So does the Assets web app at assets.trustwallet.com, which logs in with GitHub, forks the repository into your account, and opens the pull request for you under a title of the form `Add <name> (<type>)`. It is a front end to the same pull request, the same bot and the same fee — not a separate channel.

## One address on every chain

A token deployed at the same address on several chains gets one folder per chain, each named with the same checksummed address. LayerZero's ZRO token is in all six of the folders below, with identical `id`, `name`, `symbol`, `description` and `links`. Only `type` and `explorer` change:

| Chain | Folder | `type` | `explorer` host |
| --- | --- | --- | --- |
| Ethereum | `ethereum` | `ERC20` | `etherscan.io` |
| Base | `base` | `BASE` | `basescan.org` |
| Arbitrum One | `arbitrum` | `ARBITRUM` | `arbiscan.io` |
| OP Mainnet | `optimism` | `OPTIMISM` | `optimistic.etherscan.io` |
| Polygon | `polygon` | `POLYGON` | `polygonscan.com` |
| BNB Smart Chain | `smartchain` | `BEP20` | `bscscan.com` |

`smartchain` is the folder for BNB Smart Chain; `binance` is the retired BNB Beacon Chain. A wrong `type` produces a misleading error — a Base token submitted as `ERC20` was told its explorer "should be standard https://etherscan.io/token/…", because the bot derives the expected explorer from the type.

The fee is per pull request, and one pull request covering six chains received a single payment request — and was then refused by the same bot: "Too many changed files: 23 (max 10).Tokens in PR: (6)". Each chain costs two files, so at most five chains fit in one pull request. A six-chain token therefore needs two pull requests. No published rule says whether that means two fees; the per-pull-request wording implies it does, which puts the realistic cost at 1,000 TWT or 5 BNB, and every later logo change touches all six folders again.

## Field map

What the files need, against the [token property schema](/wiki/economics/defi/token-registration#the-token-property-schema):

| `info.json` field | Schema key | Notes |
| --- | --- | --- |
| folder name, `id` | `address` | EIP-55 checksummed, one folder per entry in `chain_ids` |
| `name` | `name` | |
| `symbol` | `symbol` | |
| `decimals` | `decimals` | |
| `description` | `description` | 600 bytes, one paragraph, no double spaces |
| `website` | `website` | |
| `explorer` | derived | from the chain and `address` |
| `type` | derived | from the chain, per the table above |
| `status` | — | `active` for a live token |
| `tags` | `labels` | only values from Trust Wallet's list |
| `links[]` | `links.*` | only the sixteen names above; `coingecko` and `coinmarketcap` built from `coingecko_id` and `coinmarketcap_id` |
| `logo.png` | `logo_png` | committed as a file, not linked |

## Check

The repository and its content delivery network both serve the files, and both paths are case-sensitive — the all-lowercase address returns 404:

```bash
curl -s https://raw.githubusercontent.com/trustwallet/assets/master/blockchains/ethereum/assets/0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984/info.json
curl -sI https://assets-cdn.trustwallet.com/blockchains/base/assets/0x6985884C4392D348587B19cb9eAAf157F13271cd/logo.png
```

Substitute your chain folder and address. A 200 on `info.json` under a chain folder means that chain's entry is merged; the absence of a folder under one of the six means that chain was left out of the pull requests.
