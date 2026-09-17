---
title: "Registering on Etherscan"
weight: 80
---

Etherscan's token page — the first search result for a contract address — shows a logo, description and project links only after someone who has proved control of the contract submits them through Etherscan's Token Update Application Form. The update is free and needs no liquidity or holder count. It has three prerequisites, in order: an Etherscan account, source code verified on the explorer, and a signed message proving ownership of the contract address. Each explorer in the Etherscan family — Basescan, Arbiscan, BscScan and the rest — takes its own submission.

The ownership proof is written for a contract deployed directly from a wallet. A token deployed through a factory contract — a contract that creates other contracts, and the usual way a token gets the [same address on every chain](/wiki/economics/finance/defi/vanity-addresses#create2-salt-mining) — falls outside the documented path; [who signs for a factory-deployed token](#who-signs-for-a-factory-deployed-token) covers what that means.

## Verify the source

Verification publishes source code that recompiles to the deployed bytecode. It proves nothing about who deployed the contract, but the ownership tool refuses an address whose source is not verified, and an unverified token contract reads as a warning sign to anyone who looks.

With [Foundry](/wiki/economics/finance/defi/solidity/foundry):

```bash
forge verify-contract \
  --chain 1 \
  --compiler-version v0.8.24+commit.e11b9ed9 \
  --num-of-optimizations 200 \
  --constructor-args "$(cast abi-encode 'constructor(address)' 0xYourInitialHolder)" \
  --etherscan-api-key "$ETHERSCAN_API_KEY" \
  --watch \
  0xYourTokenAddress \
  src/ExampleToken.sol:ExampleToken
```

The constructor arguments have to be supplied encoded per the contract application binary interface (ABI), byte for byte as they were deployed. Save the encoded arguments at deploy time. Recovering them later means reading them off the end of the deployment transaction's creation code — Foundry's `--guess-constructor-args` flag attempts this — and two cases differ. A transaction sent through the *deterministic deployer*, a minimal factory at `0x4e59b44847b379578588920cA78FbF26c0B4956C` on every Ethereum Virtual Machine (EVM) chain, carries a 32-byte *salt* — the value that, with the code, fixes the resulting address — in front of the creation code. And a *minimal-proxy clone*, a tiny contract that forwards every call to one shared implementation, has no constructor arguments at all.

Etherscan's version 1 API stopped working on 15 August 2025. Version 2 takes one key and a `chainid` parameter for every chain in the family, and its documentation states that "source code and ABI endpoints are available on all chains for every API plan, including the Free Tier". The free tier does not cover everything else: Base, OP Mainnet and BNB Smart Chain are listed as paid-plan chains. Verification is per chain either way — "Verifying on one chain's explorer does not verify the contract on any other."

A contract whose bytecode matches one already verified can be verified as a *similar match*, though Etherscan now restricts that to authors who have verified address ownership and asked to be included. A [minimal-proxy clone](/wiki/economics/finance/defi/permissionless-token-factory) was checked for this page and showed "Source Code Verified" and "Minimal Proxy" with the implementation's source on its code tab. Whether that status is assigned automatically, and whether it satisfies the ownership tool's verified-source check, is not documented.

## Prove you own the address

Ownership is claimed under *Verified Address* in the account menu: add the contract address, then either connect the wallet and sign in the browser or copy the message, sign it elsewhere, and paste the signature back. The documented signer is the contract's creator. Once an address is verified, the account can submit token updates, token sale information and name-tag changes for it without signing again, and one account can hold several verified addresses.

Two cases the self-serve tool does not handle go through a *General Inquiry* ticket on the contact form instead, each with a signed message in a template Etherscan supplies:

- **A multisig deployer.** "Any signer of the multisig address can verify contract ownership on behalf of the multisig."
- **A bridged token.** The deployer on the origin chain signs, and the ticket gives both addresses and the full signed message.

## Who signs for a factory-deployed token

A contract created by another contract has no private key behind its creator. Etherscan's one readable article on the case, published in December 2019, is direct about the consequence: "our method of ownership verification will not work with these contract addresses." Its remedy is a statement signed by "the creator of the contract address that created your contract address" — or, for a factory, "the main contract or the defined owner in the contract" — sent through the contact form with the contract address.

What Etherscan displays points somewhere else. In four contracts checked on 16 September 2026, its "Contract Creator" field showed the account that sent the outer transaction, not the factory, even two contracts away. The deterministic deployer in the table creates whatever code it is sent:

| How the contract was created | "Contract Creator" shown |
| --- | --- |
| Uniswap's Permit2, deployed by a wallet through the deterministic deployer at `0x4e59b44847b379578588920cA78FbF26c0B4956C` | the wallet, labelled "Uniswap: Permit2 Deployer" |
| a contract deployed through the same deployer an hour before it was checked | the sending wallet; the code tab adds "created by the contract code at 0x4e59…" |
| a contract deployed by a wallet, through a Safe multisig, through the same deployer | the wallet that executed the Safe transaction |
| a minimal-proxy clone created by calling a permissionless factory's creation function | whoever called that function |

The version 2 API draws the same distinction explicitly, returning a `contractCreator` and, separately, a `contractFactory`.

Whether the self-serve tool accepts a signature from that displayed account for a factory-created contract is not documented, and the tool sits behind a login. The practical order is to try it with the displayed account first and, if it refuses, fall back to the contact form with a signed statement. Who can sign that statement depends on the factory:

- **Through the deterministic deployer**, the article's signer does not exist. The deployer was put on each chain by a one-time transaction whose key nobody holds, so "the creator of the contract address that created your contract address" cannot sign. What remains is the account that sent the deployment, plus whatever other proof support accepts — the article allows that "other methods of verification could also be utilized".
- **Through a clone factory**, the account that deployed the factory — the article's "main contract" case.
- **A contract with an `owner()` function** has a further candidate in the article's "defined owner"; a contract without one does not.

Three consequences follow for a token deployed at the same address on every chain:

- **Keep the sending account.** On each chain, the creator Etherscan shows is whichever account sent that chain's deployment transaction. Deploy from an account you control and will still control, and record it for every chain — the schema's `deployments` key.
- **A clone's creator is its caller.** For a token created by calling a permissionless factory, the account shown is the caller. If a stranger makes the call, the stranger is the displayed creator.
- **Deploy early on the chains you intend to use.** A deterministic deployment can be [repeated on a new chain by anyone](/wiki/economics/finance/defi/vanity-addresses#salt-mining-has-no-cryptographic-risk) who has the creation code, producing the same contract at the same address with the stranger as the displayed creator there. If the self-serve tool accepts the displayed creator — which is undocumented — that stranger would be the one able to claim the token page on that chain. No incident of this is reported; the protections are to deploy on every chain you plan to support before anyone else has a reason to, or to deploy through a factory that mixes the caller's address into the salt.

## The form

The Token Update Application Form opens from the token page's *More* menu, *Update Token Info*, or at `/tokenupdate/<address>` on any explorer in the family. It is behind a login, so its full layout is not public. Etherscan's own screenshot shows the top: a **Request Type** — "New/First Time Token Update", "Existing Token Info Update" or "Token/Contract Migration" — then **Basic Information**, starting with *Token Contract Address* and *Requester Name*. Etherscan's guidelines say that section covers "website, official email address, description, sector, team members, logo, et al"; Moonbeam's documentation for Moonscan, an explorer built by Etherscan, lists the minimum as request type, contract address, requester name and email, official project website, official project email, a link to a logo, and a project description.

What Etherscan stores is visible in its `tokeninfo` API: description, website, email, blog, Reddit, Slack, Facebook, X, Bitcointalk, GitHub, Telegram, WeChat, LinkedIn, Discord, whitepaper and image. The token page also shows CoinMarketCap and CoinGecko links.

The guidelines are specific about a few things:

- **Logo:** SVG at 32 × 32 or PNG at 64 × 64, supplied as a download link that is not private. Etherscan serves the logo it keeps as a 32-pixel SVG.
- **Description:** neutral. The help text on Etherscan's companion token sale form spells this out — a neutral point of view that excludes "unsubstantiated claims ('first', 'most', 'best', and etc) unless proven otherwise" — and caps its description at 300 characters; whether the token update form has the same cap is not visible. "A collateral receipt redeemable 1:1 against its original asset" is neutral; "the most capital-efficient collateral primitive in DeFi" is not.
- **Email:** an address on the project's own domain, "or the official primary email address as shown on the website". A free-mail address has to be published on the site to count.
- **Links:** every link must work, and social profiles must be full URLs, "https://twitter.com/etherscan and not like this - @etherscan". A personal LinkedIn profile must show its owner's involvement in the project.

## Cost and wait

The update is free. Etherscan's priority support page offers "a paid, expedited option that guarantees a response within 48 business hours", covering token details, metadata and display issues; the price appears only after the request is submitted, and the page says it "does not guarantee approval or a specific outcome". An older guidelines article still describes a 24-hour turnaround. For standard channels the same page says responses "may take up to 7-10 business days".

The rules that lose time:

- "Every submission is final and you will not be able to edit or amend any part of the submission once it has been sent."
- A second submission for the same address "will result in a longer processing/waiting time"; follow up by replying to the original email.
- Contacting staff personally to speed things up is ruled out, as is "offering us money or any other 'incentives'".
- Submissions that impersonate, infringe or misrepresent are rejected, and a token page can later be delisted for fraud, impersonation, user reports or an abandoned project.

## Field map

What the form needs, against the [token property schema](/wiki/economics/finance/defi/token-registration#the-token-property-schema):

Only the first two rows are field labels seen in Etherscan's screenshot; the rest are named from its guidelines, Moonscan's minimum list and the stored `tokeninfo` fields, since the form itself is behind a login.

| Form field | Schema key | Notes |
| --- | --- | --- |
| Token Contract Address | `address` | seen; once per explorer |
| Requester Name, Requester Email | — | seen; the person submitting, not the token |
| ownership signature | `deployments` | the account shown as creator on that chain |
| official project website | `website` | Moonscan's list; must publish the address |
| official project email | `email` | Moonscan's list |
| logo link | `logo_svg` at 32 × 32, or `logo_png` at 64 × 64 | guidelines; a download link |
| project description | `description` | Moonscan's list; neutral, and 300 characters is the safe length |
| sector | `category` | guidelines |
| social profiles | `links.*` | stored fields; full URLs |
| CoinMarketCap and CoinGecko links | built from `coinmarketcap_id`, `coingecko_id` | shown on the token page |

## One address on every chain

Each explorer in the family has its own login page, its own form and its own queue, and the Optimism edition of the guidelines links its own `optimistic.etherscan.io/tokenupdate/`. A token on six chains is six submissions, each after its own source verification. Whether one account and one ownership proof carry across explorers is not documented.

| Chain | Explorer |
| --- | --- |
| Ethereum | `etherscan.io` |
| Base | `basescan.org` |
| Arbitrum One | `arbiscan.io` |
| OP Mainnet | `optimistic.etherscan.io` |
| Polygon | `polygonscan.com` |
| BNB Smart Chain | `bscscan.com` |

Each clone of a factory is a separate token with its own address, and nothing documents token information carrying over from an implementation to its clones; the clone checked for this page showed Etherscan's placeholder image on its token page. Plan on a submission per clone.

## Check

The token page is free to read: `https://etherscan.io/token/<address>`, or the same path on the chain's explorer. A processed update shows the logo beside the name and the links in the profile section; an unprocessed one shows the placeholder image.

The API version needs a paid key — `tokeninfo` is "a PRO endpoint, available to the Standard Plan and above":

```bash
curl -s "https://api.etherscan.io/v2/api?chainid=1&module=token&action=tokeninfo&contractaddress=0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984&apikey=$ETHERSCAN_API_KEY"
```

Without a key it returns `{"status":"0","message":"NOTOK","result":"Missing/Invalid API Key"}`. With one, `image` holds the logo URL and `blueCheckmark` is `"true"` for a token Etherscan has verified.
