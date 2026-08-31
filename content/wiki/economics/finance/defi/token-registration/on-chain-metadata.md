---
title: "On-Chain Metadata"
weight: 20
---

Two mechanisms let a token carry its own icon without a company's approval: a metadata document referenced from the contract, and a wallet method your interface can call to push the icon at the user directly. Neither needs a form, a fee, or a queue, and both work in the same block the contract is deployed in.

## ERC-1046: a `tokenURI` on a fungible token

[ERC](/wiki/economics/finance/defi/ethereum/eip)-1046 is Final, and adds one function to [ERC-20](/wiki/economics/finance/defi/ethereum/erc-20):

```solidity
interface IERC1046 {
    function tokenURI() external view returns (string memory);
}
```

It resolves to a JSON document with an `interop` object saying which token interfaces the contract implements, plus the display fields:

```json
{
  "interop": { "erc1046": true },
  "name": "Example Token",
  "symbol": "EXA",
  "decimals": 18,
  "description": "Collateral receipt issued by the Example vault.",
  "image": "ipfs://bafybeic4example.../banner-1080x566.png",
  "icons": ["ipfs://bafybeic4example.../logo-512.png"]
}
```

The two image fields are not interchangeable. `icons` is the square, transparent-background one — the [token logo](/wiki/economics/finance/defi/token-registration/icon). `image` is specified with an aspect ratio between 1.91:1 and 4:5 inclusive, so it is a header graphic, not a second copy of the icon. Both ask bitmaps to be 320 to 1080 pixels wide, which puts the 512-pixel render in `icons` and rules the 256-pixel one out of either.

Implementing it costs one constant string. A `public constant` generates the getter, so there is no storage slot and no `SLOAD` on read:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ExampleToken is ERC20 {
    /// @notice ERC-1046 metadata document.
    string public constant tokenURI =
        "ipfs://bafybeic4example.../metadata.json";

    constructor() ERC20("Example Token", "EXA") {
        _mint(msg.sender, 1_000_000e18);
    }
}
```

Point it at content-addressed storage — [IPFS](/wiki/cs/ipfs) or [Arweave](/wiki/economics/finance/defi/arweave) — rather than a domain. A hardcoded constant on a [finalized contract](/wiki/economics/finance/defi/finalized-smart-contract) outlives the domain registration, and an unreachable metadata URL is worse than none, because it looks like abandonment. If the document may need to change, hold the string in storage behind an owner-gated setter and accept that you have added a privileged role someone now has to trust.

Almost no wallet or explorer fetches `tokenURI` on an ERC-20 today, and the field will not put a logo in MetaMask on its own. What it buys is a permanent, self-hosted assertion of the token's own metadata that no registrar can revoke, get wrong, or lose in a migration — at a cost of about thirty thousand gas at deployment — 149 bytes of extra runtime code for the string above, at 200 gas a byte.

## Pushing the icon at the wallet

[EIP](/wiki/economics/finance/defi/ethereum/eip)-747 is also Final and defines a provider method that prompts the user to add a token. Your own interface calls it and the icon appears — no registry involved, no waiting.

```javascript
await window.ethereum.request({
  method: 'wallet_watchAsset',
  params: {
    type: 'ERC20',
    options: {
      address: '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984',
      symbol: 'EXA',
      decimals: 18,
      image: 'https://example.org/assets/logo-256.png',
    },
  },
});
```

The call returns `true` as soon as the request is recognized as valid, not when the user accepts it, so the boolean tells you nothing about whether the token was added.

The finalized text of the EIP pared the ERC-20 options down to `address` and an optional `chainId`, deferring name, symbol and image to the ERC-1046 document. MetaMask's implementation still reads `symbol`, `decimals` and `image` from the call, and MetaMask is what runs on most of the machines that will execute this code. Send all four fields: the spec-compliant subset works everywhere, and the extra three are what actually renders the icon today.

The `image` may be an `https:` URL or a `data:` URI, and MetaMask's guidance is no larger than 512 × 512 and 256 kB. A data URI removes the fetch, so the icon cannot fail to load because of a CDN outage or a cross-origin header; it also means changing the icon requires shipping new frontend code.

MetaMask's own advice on this point is worth taking at face value: its `contract-metadata` repository, the old route for getting an icon into the wallet by pull request, is frozen, and its documentation directs new tokens to this method instead.

## Chains where the icon is simply on-chain

Ethereum's omission is not universal. Sui's [coin standard](/wiki/economics/finance/defi/sui) creates a `CoinMetadata` object alongside the `TreasuryCap` when a currency is created, and it has an `icon_url` field:

```text
coin::create_currency(witness, decimals, symbol, name, description, icon_url, ctx)
  -> (TreasuryCap<T>, CoinMetadata<T>)
```

Whoever holds the `TreasuryCap` can update the metadata afterwards, or freeze the object to make it permanent. Wallets and explorers read the field directly, so a Sui coin has a working icon at creation with no submission anywhere. On Solana, the Metaplex token metadata account holds a `uri` pointing at a JSON document whose `image` field carries the logo, which puts the resolution one hop off-chain but still leaves it entirely under the issuer's control.

The practical consequence for a multi-chain deployment: the [Ethereum](/wiki/economics/finance/defi/ethereum/) side needs the whole registration campaign, and the Sui and Solana sides need one constructor argument.
