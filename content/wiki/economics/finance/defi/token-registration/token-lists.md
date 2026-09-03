---
title: "Token Lists"
weight: 30
---

A token list is a JSON document that maps chain identifier and contract address to a name, symbol, decimals count and logo URL. It is the only registration route where you are the publisher rather than the applicant: you write the file, you host it, and a user adds it to their interface by pasting a URL. Uniswap wrote the specification in 2020 and most swap interfaces and several wallets read the format.

## The document

```json
{
  "name": "Bitsy Par Tokens",
  "timestamp": "2026-08-31T00:00:00.000Z",
  "version": { "major": 1, "minor": 0, "patch": 0 },
  "logoURI": "https://example.org/assets/list-logo.png",
  "keywords": ["par", "collateralized"],
  "tags": {
    "par": {
      "name": "Par token",
      "description": "Redeemable one-for-one against its original asset"
    }
  },
  "tokens": [
    {
      "chainId": 1,
      "address": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
      "name": "Example Token",
      "symbol": "EXA",
      "decimals": 18,
      "logoURI": "https://example.org/assets/logo-256.png",
      "tags": ["par"]
    }
  ]
}
```

`name`, `timestamp`, `version` and `tokens` are required at the top level; a token entry requires `chainId`, `address`, `decimals`, `name` and `symbol`. Everything else, `logoURI` included, is optional as far as the schema is concerned and mandatory as far as the reader is concerned.

Four constraints reject more lists than anything else:

- The list `name` is capped at 30 characters and matched against `^[\w ]+$`. Letters, digits, underscores and spaces only — an em dash, an ampersand or a hyphen in your project name fails validation.
- `address` casing must stay stable between publishes. The schema itself accepts any casing, but consumers key tokens by the exact `chainId`+`address` string, so recasing an address reads as a removal plus an addition and forces a major version bump — a breaking-change warning shown to every user, for no change at all. Pick the [EIP](/wiki/economics/finance/defi/ethereum/eip)-55 checksummed form and never touch it again.
- `timestamp` must be a date-time string, and it has to move forward on every publish.
- Token `name` is capped at 60 characters and `symbol` at 20.

## Versioning is a protocol, not a courtesy

Consumers diff versions to decide whether to warn the user, so the three numbers carry defined meanings:

| Change | Bump |
| --- | --- |
| A token is removed, or an address or chain identifier changes | major |
| A token is added | minor |
| Name, symbol, decimals or `logoURI` of an existing token changes | patch |

Changing an address is a removal plus an addition, so it is a major bump, not a patch. Interfaces surface a major bump to the user as a potentially breaking change and a patch silently — which is exactly what you want when you are only swapping in a better icon.

## Validate before publishing

The schema ships in the package, so validation is four lines and belongs in continuous integration:

```javascript
import fs from 'node:fs';
import { createRequire } from 'node:module';
import Ajv from 'ajv';
import addFormats from 'ajv-formats';

const schema = createRequire(import.meta.url)(
  '@uniswap/token-lists/src/tokenlist.schema.json',
);

const ajv = new Ajv({ allErrors: true, verbose: true });
addFormats(ajv);
const validate = ajv.compile(schema);

const list = JSON.parse(fs.readFileSync('tokenlist.json', 'utf8'));
if (!validate(list)) {
  console.error(validate.errors);
  process.exit(1);
}
```

Reach into `src/` for the schema rather than the package root. The upstream documentation shows `import { schema } from '@uniswap/token-lists'`, which resolves under a bundler consuming the TypeScript sources but throws under Node: the published tarball declares `main: dist/index.js` and ships no `dist/`.

A list that fails validation is not partially loaded; the interface refuses it whole and shows the user an error, so one malformed entry takes down every token on the list.

## Hosting

Three options, in ascending order of durability:

- **An HTTPS URL.** Simplest, and it needs a permissive cross-origin resource sharing (CORS) header — the fetch is made by a browser from someone else's origin, so without `access-control-allow-origin` the list silently fails to load. This is the single most common reason a self-hosted list "doesn't work."
- **[IPFS](/wiki/cs/ipfs), [pinned](/wiki/cs/ipfs/pinning).** Content-addressed, so the hash changes on every publish and consumers pinned to the old hash keep the old list.
- **An Ethereum Name Service (ENS) name with a [`contenthash` record](/wiki/cs/ipfs/ipns-and-dnslink#contenthash-on-a-name-service) pointing at the IPFS hash.** The specification's preferred form: the name is stable, the content underneath it is not, and updating the list is a transaction rather than a server deploy.

Uniswap's interface accepts all three under *Manage → Lists*: a URL, an ENS name, or a raw IPFS hash.

## Your list is not the default list

Publishing a list makes the token available to anyone who imports it. It does not put the token in front of anyone who does not. The list shipped enabled in the Uniswap interface is a separate, curated repository with its own criteria, and there is no submission path from one to the other.

That is a smaller limitation than it sounds. The list URL is a link you can put in a Discord pin, a docs page, or the swap button on your own site, and users who arrive by that link see the correct name and icon before they have transacted. Combined with [`wallet_watchAsset`](/wiki/economics/finance/defi/token-registration/on-chain-metadata#pushing-the-icon-at-the-wallet), it covers the audience that matters on launch day, which is people who already came to you — and it covers them without approval from anyone.
