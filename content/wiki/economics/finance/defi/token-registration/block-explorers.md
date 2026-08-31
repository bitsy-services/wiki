---
title: "Block Explorers"
weight: 40
---

The explorer token page is the first result when anyone searches the contract address, and it is the cheapest registration to obtain: free, no liquidity requirement, no holder count, and turnaround measured in days. It is also the one with a hard prerequisite — the contract source must be verified before the form will open.

## Step one: verify the source

Verification publishes source that recompiles to the deployed bytecode. It proves nothing about who deployed the contract, but every later step depends on it, and an unverified token contract reads as a warning sign to anyone who looks.

With [Foundry](/wiki/economics/finance/defi/solidity/foundry):

```bash
forge verify-contract \
  --chain 1 \
  --compiler-version v0.8.24+commit.e11b9ed9 \
  --num-of-optimizations 200 \
  --constructor-args "$(cast abi-encode 'constructor(string,string)' 'Example Token' 'EXA')" \
  --etherscan-api-key "$ETHERSCAN_API_KEY" \
  --watch \
  0xYourTokenAddress \
  src/ExampleToken.sol:ExampleToken
```

The constructor arguments are where this fails. They are not stored in a way the explorer can recover, so they have to be supplied encoded per the contract application binary interface (ABI) and byte-exact; a trailing space inside a string argument produces a mismatch with no useful error. Recovering them after the fact means reading the deployment transaction's calldata and slicing off the creation bytecode. Save the encoded arguments at deploy time and this never comes up.

Since the V1 endpoints were retired in August 2025, one Etherscan key works across every chain the family covers — you pass a `chainid` rather than swapping keys and base URLs. That unification stops at the API. Token information is still submitted per explorer.

## Step two: prove you own the address

Etherscan gates the token update form behind an ownership proof, done by signing a message from the contract's deploying address. Two routes: connect the deployer wallet to Etherscan and sign in the browser, or copy the message template, sign it offline, and paste the signature back into the form. If the deployer is a multisig, any one of its signers can sign on its behalf. For a bridged token, the signature comes from the deployer on the origin chain rather than from the bridge contract.

The proof persists. Later edits to the token page are made directly from it without signing again — which is worth knowing before you rush the first submission, because that submission itself cannot be edited.

## Step three: the form

Etherscan's guidelines are specific about three things and vague about the rest.

- **Logo:** SVG at 32 × 32, or PNG at 64 × 64. Other formats are accepted, with a stated disclaimer that the result may not look good — which in practice means an oversized upload gets downsampled by their pipeline rather than by yours.
- **Description:** written from a neutral stance, with no superlatives and no comparative claims. "A collateral receipt redeemable one-for-one against its original asset" passes. "The most capital-efficient collateral primitive in DeFi" does not.
- **Email:** on the project's own domain. A free-mail address is a rejection signal.

Every link submitted must resolve, including the ones in the social fields. Submissions are final and cannot be edited before review, resubmitting the same address puts you behind yourself in the queue, and contacting staff privately is explicitly discouraged.

Updates are free. Etherscan sells a priority support plan with a 24-hour turnaround for anyone who needs the queue skipped; the standard queue has no published time and varies with volume.

The same form and the same guidelines are reproduced across the family — BscScan, Basescan, Arbiscan, Polygonscan, and the rest — with a separate ownership verification and a separate submission for each chain. A token deployed to five chains is five submissions.

## Blockscout

Blockscout runs many rollup and appchain explorers and takes a different shape. It also requires a verified contract, and it asks for a direct icon URL at 48 × 48 rather than an upload, so the asset must already be hosted somewhere public. Its submissions run through a review queue, and a paid prioritization option for jumping it was announced for September 2026.

Blockscout additionally reads the Token Name Service dataset, which supplies name, logo, description, project URL, and social links from a separate source. Where an instance has that integration switched on, a token registered there inherits its metadata without a per-explorer submission — the one place in this whole landscape where a single registration propagates.

## What the badge does and does not say

A verified-source label means the published code compiles to the deployed bytecode. It says nothing about who deployed it or whether the code is safe, and an updated token page with a logo and links means only that somebody signed a message and filled in a form. Both are curation, not consensus, and [fake tokens](/wiki/economics/finance/fraud/fake-token) clear the first bar routinely — verifying a copied source contract is as easy as verifying an original.
