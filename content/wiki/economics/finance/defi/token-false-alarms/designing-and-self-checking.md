---
title: "Designing and Self-Checking"
weight: 70
---

Only two kinds of design decision change what a scanner reports. One is removing a function from the deployed bytecode, so there is nothing to detect. The other is moving the token inside a list somebody else maintains — a recognised locker, an indexed trading pair, a verified source. Everything in between — capping a setter, adding a timelock, publishing an audit, renouncing ownership — is invisible to the schema. That is not an argument against doing those things, which protect real users against real risks. It is an argument against expecting them to change a boolean.

What remains under a builder's control is knowing. The endpoints below are free and keyless, and running them before launch costs an afternoon.

## Verify first, everywhere

Closed source is the one suppressor with no upside: "When the contract is closed-source, other risk items will return null." An unverified contract does not score badly, it scores *nothing*, and the blank is read as risk by everyone downstream. Verification is also what lets a static analyser reach the deployed address at all — Slither's compilation layer can pull source from Etherscan and its alt-chain siblings, so `slither 0xADDRESS` works only once an explorer holds the source.

Verify on every chain you deployed to. Etherscan's V2 API advertises "All 60+ EVM chains under one key. Set chainid to choose one" on its documentation home — every [Ethereum Virtual Machine](/wiki/economics/finance/defi/ethereum#the-ethereum-virtual-machine-evm) chain it indexes — so verifying on mainnet alone is a choice rather than a constraint. Then check the result on Sourcify, which is one unauthenticated request:

```bash
curl -s https://sourcify.dev/server/v2/contract/1/0xdAC17F958D2ee523a2206206994597C13D831ec7
# {"matchId":"1817159","creationMatch":"match","runtimeMatch":"match",
#  "verifiedAt":"2024-08-08T13:56:23Z","match":"match","chainId":"1", ... }
```

Sourcify grades an `exact_match` — byte-identical including the metadata hash — against a plain `match`, and "If you were to add a comment, change a variable or function name, the exact match will be broken." Do not treat exact match as a launch gate: USDT and DAI both sit at plain `match`.

honeypot.is applies a stricter test than either, and it is the one most likely to catch you out: its open-source check is transitive across the whole call path. "Unlike other detectors, it's not enough for the token itself to be open source. It requires every single contract called during the buy/sell process to be open source." One unverified library on the swap path taints a verified token, and the resulting `CLOSED_SOURCE` flag carries high severity.

## Delete rather than bound

The evidence for this is on [capability flags](/wiki/economics/finance/defi/token-false-alarms/capability-flags#what-actually-moves-the-flag): a hard cap in a setter does not clear the flag, and renouncing ownership mostly does not either. What does clear it is the function not existing.

`immutable` and `constant` are the mechanisms. An `immutable` value is fixed at construction and written into the deployed bytecode rather than storage, copied inline at every access site; a `constant` never occupies a slot at all. Neither has a setter for a scanner to find.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Token is ERC20 {
    // No setter exists, so no `slippage_modifiable`, and the value is
    // still readable by anyone who wants to check it.
    uint256 public constant FEE_BPS = 100;          // 1%, inlined into bytecode
    address public immutable TREASURY;              // fixed at construction

    constructor(address treasury) ERC20("Token", "TKN") {
        TREASURY = treasury;
    }
}
```

The trade is exactly what it looks like. A fee you can never change is a fee you can never fix, and a treasury address you can never change is one you can never rotate after a key compromise. Delete a setter because you have decided the parameter is final, not to improve a score.

Two cheap deletions are worth doing regardless. `metadata_modifiable` — the ability to change name and symbol — is a setter most templates leave in place for no reason; making both `constant` removes it. And if you keep `Ownable` but never intend to renounce, overriding `renounceOwnership()` to revert removes an operational footgun, though it moves no flag:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

abstract contract NoRenounce is Ownable {
    function renounceOwnership() public pure override {
        revert("ownership is required for pause and upgrade");
    }
}
```

OpenZeppelin's own guidance runs against the scanners here, and it is worth knowing which side you are choosing. Its access-control guide recommends handing ownership to a contract — "a Gnosis Safe, an Aragon DAO, or a totally custom contract", meaning a multisig or a [decentralized autonomous organization](/wiki/economics/finance/defi/dao) — and `TimelockController`'s own NatSpec gives its purpose as "time for users of the controlled contract to exit before a potentially dangerous maintenance operation is applied." Quick Intel's first listed check is `Renounced`. Renouncing satisfies that check and permanently disables pause, blacklist and every emergency control, which is the arrangement OpenZeppelin warns about. There is no design that satisfies both.

## Choose the counterparties the scanners can see

Three decisions that look like market-making choices are really scanner-visibility choices.

**Which asset you pair against.** GoPlus recognises a pool as a trading pair only when the counter-asset is on a list it publishes, and a token that fails that test loses its tax and liquidity fields along with the flag — [the blank field](/wiki/economics/finance/defi/token-false-alarms/the-blank-field#four-ways-a-field-goes-blank) has the cascade. Deep liquidity against a long-tail asset reads as no liquidity at all.

**Which locker you use.** Lock detection is a named-address allowlist, per chain, and the lists are short. Check the vendor's table before choosing, because the same design registers as locked on Ethereum and unlocked on most L2s, and on several chains the only recognised locker is the scanner vendor's own product.

**Which venue holds the liquidity.** honeypot.is covers Ethereum, BNB Smart Chain and Base, and only Uniswap V2 and V3-style pools. Liquidity in a V4 singleton is unsimulatable — eight of the ten ordinary tokens in the [overview measurement](/wiki/economics/finance/defi/token-false-alarms#the-measurement) got no answer from it, mostly for that reason.

**If your token rebases**, the documented escape is a non-rebasing wrapper on the wstETH model, which Lido built because "many lending and broader DeFi integrations" assume balances change only on transfer or mint. It trades one flag for another — wstETH reports `is_mintable` — but a wrapped balance is legible to far more software.

## Check yourself

There is no testnet dry-run anywhere. Of GoPlus's forty-three live chains exactly one is a testnet, and it is not one anybody deploys to for practice. Every check below runs against mainnet, and the honeypot simulator is the only one that works before liquidity exists.

```bash
TOKEN=0xC18360217D8F7Ab5e7c516566761Ea12Ce7F9D72

# 1. Capability flags. Branch on the body's `code`, never the HTTP status —
#    throttling, an unknown token and an unsupported chain are all HTTP 200.
curl -s "https://api.gopluslabs.io/api/v1/token_security/1?contract_addresses=$TOKEN"

# 2. Trade simulation. forceSimulateLiquidity is the only pre-pool check that exists.
curl -s "https://api.honeypot.is/v2/IsHoneypot?address=$TOKEN&chainID=1&forceSimulateLiquidity=true"

# 3. Verification across the whole call path, not just your contract.
curl -s "https://api.honeypot.is/v1/GetContractVerification?address=$TOKEN&chainID=1"

# 4. Source verification status.
curl -s "https://sourcify.dev/server/v2/contract/1/$TOKEN"

# 5. Your website, per hostname — check every host you serve from.
curl -s "https://dapp-scanning.api.cx.metamask.io/v2/scan?url=https://yourproject.example"
```

Read the GoPlus response tri-state. A field that is absent is unknown, not false — the trap is documented in [the blank field](/wiki/economics/finance/defi/token-false-alarms/the-blank-field), and coercing absent to zero is how integrators manufacture false alarms out of clean responses.

Two conformance tools sit alongside these and answer a different question. `slither-check-erc` verifies that your token behaves like the standard says — "All the functions are present", "Functions return the correct type", "Functions that must be `view` are `view`", "The functions emit the events" — across ERC-20, 223, 721, 777, 1155, 1363, 2612 and 4626. These are the defects that make wallets and routers misbehave in ways users then report as scams.

```bash
slither-check-erc MyToken.sol MyToken
slither . --exclude-informational
```

Slither has no scam or rug-pull detector and does not reproduce scanner heuristics; the only mention of scams in its documentation is a citation of third-party research that used it for feature extraction. It answers "is this correct", not "will this be flagged".

## Watch your own reputation

Every endpoint above is free and keyless, which makes the obvious thing cheap: run them on a schedule against your own token and domain, store the responses, and diff. The alternative is learning about a flag from a user in a Discord channel, some days after the wallet started showing it.

Two things make this more than hygiene. Flags change without any action on your part — TokenSniffer documents that a token's score can drop because a holder crossed five percent of supply or a liquidity lock expired, neither of which involves the deployer. And MetaMask publishes a live diff feed of its blocklist, so a domain block is observable within minutes rather than after a support ticket.

The cheapest useful version is a cron job that fetches the five endpoints, writes the JSON to a file per day, and alerts on any field that changed. It answers the one question none of these vendors will answer for you: *am I flagged right now?*

## Before launch

```text
step                                        clears / enables
------------------------------------------  ------------------------------------------
verify source on every chain                unblocks every other check downstream
verify every contract on the swap path      honeypot.is openSource is transitive
delete setters you will never use           removes the flag with the function
make name/symbol constant                   clears metadata_modifiable
pick a mainstream pair asset                is_in_dex, and the six fields it gates
pick a locker on the vendor's own list      lock detection is an allowlist
run the five self-checks above              tells you what users will see
submit to report.blockaid.io/verifiedProject   pre-emptive, before a flag exists
publish a token list                        the one route that asks nobody
```

The last two are worth doing on launch day rather than after a problem. Blockaid's portal has a `/verifiedProject` route for exactly this, and Base's chain documentation points developers at it pre-emptively — the only vendor route in this landscape designed to be used before a flag rather than after. A self-published [token list](/wiki/economics/finance/defi/token-registration/token-lists) is permissionless, costs nothing, and is read by less software than it should be, but it is the only step here that requires nobody's approval.

Everything else is [waiting out a queue](/wiki/economics/finance/defi/token-false-alarms/allowlists#the-circle), and knowing that in advance is worth more than any of the individual levers.

## External links

- [Sourcify verification](https://docs.sourcify.dev/docs/exact-match-vs-match/) — what exact match means and why plain match is normal
- [Etherscan contract verification](https://docs.etherscan.io/contract-verification) — one key, sixty-plus chains
- [honeypot.is API](https://docs.honeypot.is/ishoneypot) — the transitive open-source check and `forceSimulateLiquidity`
- [Slither ERC conformance](https://github.com/crytic/slither/blob/master/docs/src/tools/ERC-Conformance.md) — the checks that catch wallet-breaking defects
- [Base: avoiding malicious flags](https://docs.base.org/specifications/security/avoid-malicious-flags) — the closest thing to official pre-launch guidance
- [OpenZeppelin access control](https://docs.openzeppelin.com/contracts/5.x/access-control) — the timelock and multisig arrangement the scanners cannot see
