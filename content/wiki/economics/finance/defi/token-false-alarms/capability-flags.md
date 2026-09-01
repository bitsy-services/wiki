---
title: "Capability Flags"
weight: 10
---

A capability flag is a boolean asserting that a token contract *can* do something. GoPlus returns about forty-five of them, TokenSniffer runs twenty-six named tests, Quick Intel publishes twenty-two numbered checks, and MetaMask ships fifty-one token-risk labels; the four are different vocabularies over one operation, which is reading the bytecode for a function selector or a storage pattern. None of them has a field that can hold a bound, a delay, or the kind of account holding the key. Searching GoPlus's response documentation for "timelock", "immutable" and "audit" returns nothing under any of the three.

## What actually moves the flag

Four tokens, read on 2026-08-31, are enough to locate the rule. ENS here is the Ethereum Name Service governance token, not the naming system itself.

| Token | Mint function | Owner | `is_mintable` |
| --- | --- | --- | --- |
| ENS | `onlyOwner`, capped at 2% per 365 days by `constant`s | 48-hour `TimelockController` | `1` |
| UNI | gated by a `minter` address, capped at 2% per 365 days | governance Timelock | `0` |
| 1INCH | `onlyOwner`, uncapped | `address(0)` — renounced | `1` |
| PEPE | no mint function; supply fixed in the constructor | `address(0)` — renounced | `0` |

ENS and UNI implement the same design — a mint bounded to two percent of supply per year, held by a governance timelock — and score opposite. 1INCH's mint is permanently unreachable, because `owner()` returns the zero address, and scores as present. PEPE has no mint at all and scores as absent. The variable that tracks the flag is neither the capability, nor its bound, nor whether anyone can still call it: it is the *gating idiom*. ENS and 1INCH use OpenZeppelin's `Ownable`; UNI uses a bespoke `minter` address; PEPE has no function to gate. So the operative rule for a deployer is narrower and stranger than "detectors flag privileged functions":

- **Deleting the function clears the flag.** PEPE's `is_mintable` and `slippage_modifiable` read `0` because those functions do not exist in its source.
- **Renouncing mostly does not.** PEPE renounced and still returns `is_blacklisted`, `transfer_pausable`, `is_anti_whale` and `anti_whale_modifiable`; 1INCH renounced and still returns `is_mintable`.
- **Capping never does.** ENS's cap is two `require` statements against `constant` values, inlined into the bytecode with no storage slot and no setter, and the flag is identical to an uncapped mint's.

The vendor hedges rather than claims otherwise. Three GoPlus fields carry the sentence "This function generally relies on ownership. When the contract does not have an owner (or if the owner is a black hole address) and the owner cannot be retrieved, this function will most likely be disabled." The word "renounce" does not appear in the document at all, and "most likely" is doing the work: the boolean keeps reporting `1`.

For the blacklist family, the documentation says the opposite outright, and is right to. `is_blacklisted` notes that "For contracts without an owner (or the owner is a black hole address), the blacklist will not be able to get updated. However, the existing blacklist is still in effect", and `is_whitelisted` and `personal_slippage_modifiable` carry the same construction for the whitelist and for an already-set tax rate. Renouncing freezes the blacklist; it does not clear it, and anyone listed before renouncement is listed permanently.

## The capped setter nobody reads

Tether's fee setter has been hard-bounded since 2017, in the setter itself, under a comment saying so:

```solidity
// TetherToken.sol, solc 0.4.18 — the fee applied in transfer()
uint fee = (_value.mul(basisPointsRate)).div(10000);
if (fee > maximumFee) { fee = maximumFee; }

function setParams(uint newBasisPoints, uint newMaxFee) public onlyOwner {
    // Ensure transparency by hardcoding limit beyond which fees can never be added
    require(newBasisPoints < 20);
    require(newMaxFee < 50);
    basisPointsRate = newBasisPoints;
    maximumFee = newMaxFee.mul(10**decimals);
}
```

Nineteen basis points is the ceiling on the rate and forty-nine tokens the ceiling on the absolute fee, so above roughly 26,000 USDT the absolute cap binds first and the effective rate falls toward zero. Both parameters read zero on chain today. GoPlus returns `slippage_modifiable: "1"`.

The bound is also weaker than it looks, which is the honest counterweight: `deprecate(address)` forwards `transfer`, `transferFrom`, `balanceOf`, `totalSupply` and `allowance` to an arbitrary successor contract, so the owner can leave the nineteen-basis-point ceiling by leaving the contract. A cap in a setter is a real constraint only for as long as the code containing it is the code that runs — which is the argument [finalized smart contract](/wiki/economics/finance/defi/finalized-smart-contract) makes at greater length.

## Every flag maps to a requirement

**Blacklist.** Circle's `Blacklistable.sol` declares a `blacklister` role and the modifier `notBlacklisted(address)`, applied to both parties on `transfer` and to all three on `transferFrom`. Since `FiatTokenV2_2` the blacklist bit lives *inside* the balance word — `_isBlacklisted()` is `balanceAndBlacklistStates[_account] >> 255 == 1`, with the balance in the low 255 bits — a change Circle made to cut transfer gas by 6–7%. Freezing an address is now literally a write to its balance slot, so any heuristic watching for owner-initiated balance-slot writes sees a compliance action as balance manipulation. Tether's equivalent is blunter: `destroyBlackFunds` sets a listed balance to zero and decrements total supply, and is the obvious candidate for USDT's `owner_change_balance` flag, though GoPlus names no triggering function for any finding it reports.

**Pause.** OpenZeppelin's `ERC20Pausable` ships no public `pause` or `unpause`; the developer must add them with access control, and the docs warn that omitting them leaves the mechanism "unreachable, and thus unusable". A `transfer_pausable` hit on an OpenZeppelin-based token therefore cannot arrive by accident — somebody wired it deliberately, which is exactly what a regulated issuer does and exactly what a [rug pull](/wiki/economics/finance/fraud/rug-pull) does.

**Mint.** An [ERC-4626](/wiki/economics/finance/defi/ethereum/erc-4626) vault mints shares on deposit and burns them on withdrawal; that is the standard's entire mechanism. There is no conforming vault whose share token is not mintable. sDAI — ownerless, no admin surface, one of the most boring contracts in circulation — returns `is_mintable: "1"` with every other flag zero, and the four MetaMorpho vaults on the [overview page](/wiki/economics/finance/defi/token-false-alarms#the-measurement) return it too. `ERC20Capped` fixes the cap immutably at construction and does not help: the field is defined as "the ability to mint tokens", full stop.

**External calls.** GoPlus's `external_call` is documented with no malice test at all — it fires when the contract calls another contract during a primary method. [ERC-777](/wiki/economics/finance/defi/ethereum/erc-20#related-standards) puts `tokensReceived` on the recipient of *every* transfer, resolved through the ERC-1820 registry; the standard's text contains no security considerations section and no mention of reentrancy, and OpenZeppelin removed `ERC777` outright in Contracts v5.0.0 without stating a reason. [ERC-1363](/wiki/economics/finance/defi/ethereum/erc-1363) is the same idea built to avoid the flag: `transferAndCall`, `transferFromAndCall` and `approveAndCall` are opt-in functions that leave plain `transfer` unhooked, which its own Backwards Compatibility section names as the design point. [ERC-1155](/wiki/economics/finance/defi/ethereum/erc-1155) offers no such escape — `onERC1155Received` is mandatory on every transfer to a contract.

**Anti-bot limits.** A maximum transaction size and a per-address cooldown are ordinary launch protection, and they score twice: `is_anti_whale` for having a limit, `anti_whale_modifiable` for being able to change it. They also break the simulator. GoPlus documents that "Sometimes token's anti-bot mechanism would affect our sandbox system, causing the display of 'buy_tax': '1'", that the same mechanism can produce a `cannot_buy` of `1`, and separately that a trading cooldown can make `sell_tax` return `1` — where `1` means a hundred percent tax or an unsellable token. Launch-guard code can therefore get a zero-tax token reported as a honeypot, by the vendor's own documentation.

## Upgradeability silences the scanner

GoPlus's `is_proxy` entry says "When the contract is a proxy, other risk items may not be returned", and nearly every contract-security field repeats the condition. In practice the suppression is total:

| Token | `is_proxy` | Permission fields returned |
| --- | --- | --- |
| USDT | `0` | six, all set to `1` |
| USDC | `1` | none |
| stETH | `1` | none |
| AAVE | `1` | none |
| PAXG | `1` | none |

USDC has the most consequential blacklist in DeFi and reports no blacklist field. It looks cleaner than USDT not because it is safer but because analysis stopped. Adding an upgradeable proxy — itself a penalised shape, and the one that [subsumes every other admin control](/wiki/economics/finance/fraud/hidden-admin-controls#what-a-proxy-does-to-an-audit) — suppresses every other finding. ERC-1967 exists precisely so tooling *can* find the implementation slot; its motivation section says the lack of a common interface "makes it impossible to build common tools that act upon this information". Detection is not the hard part. Etherscan, which detects proxies by bytecode pattern and the `delegatecall` opcode rather than by slot, publishes the frankest false-positive admission in this field: "Contracts showing 'is this a proxy?' may not actually be a proxy contract — An example are contracts relying on libraries which also use the delegateCall opcode to forward storage data for manipulation."

## Rebasing and the wrapper

stETH does not store balances. It stores shares, and `balanceOf` derives the balance from the pooled-ether total that the oracle updates roughly daily, so every holder's balance changes with no transfer and no event. Ampleforth does the same through `_gonsPerFragment` and states the consequence in a source comment: "We do not guarantee that the sum of all balances equals the result of calling totalSupply()." Aave's aTokens scale by the liquidity index and emit a mint-shaped `Transfer` from the zero address for the accrued amount only when the position is next touched.

Lido's documented answer is wstETH, a non-rebasing wrapper whose price in stETH moves instead, built because "many lending and broader DeFi integrations" assume balances change only on transfer or mint. It trades one flag for another. wstETH returns `is_mintable: "1"` — wrapping mints — carries no `trust_list` entry, and returns `honeypot_with_same_creator: "1"`. stETH, being a proxy, returns twenty keys with no permission flag in either direction. Neither shape reads as clean.

AMPL gets no report at all — not a bad one, an empty one — and neither documented suppressor explains it. That failure has its own shape and its own page: [the blank field](/wiki/economics/finance/defi/token-false-alarms/the-blank-field#four-ways-a-field-goes-blank).

## Fee-on-transfer at the router boundary

A transfer fee is the one capability where the flag is the smaller problem. The token still trades; the *router* is what breaks, and it breaks differently at each [Uniswap](/wiki/economics/finance/defi/uniswap) version — [swap routers](/wiki/economics/finance/defi/uniswap/swap-routers) covers which one to call when.

V2's pair is fine. It derives input amounts from measured balances (`balance0 - (_reserve0 - amount0Out)`) and enforces the K invariant on what actually arrived, so a shortfall is tolerated. `UniswapV2Library` is what fails: `getAmountsOut` computes every hop from pre-trade reserves with no knowledge of a fee, so the plain router paths revert with `UniswapV2Router: INSUFFICIENT_OUTPUT_AMOUNT`. `UniswapV2Router02` carries exactly six function definitions with `SupportingFeeOnTransferTokens` in the name, and the gaps matter: there is no `swapTokensForExact*` variant and no non-ETH `removeLiquiditySupportingFeeOnTransferTokens`.

V3 rejects the token at the pool, not the router — `swap()` requires `IIA`, `mint()` requires `M0`/`M1`, `flash()` requires `F0`/`F1` — and Uniswap's position is a commitment rather than a backlog item: "We will not be making a router that supports fee-on-transfer tokens in the future."

V4's `PoolManager` credits the measured difference. `sync()` snapshots `balanceOfSelf()` and `_settle` computes `paid = reservesNow - reservesBefore`, so a shortfall on the way *in* is simply a smaller credit. That is a side effect of delta accounting rather than a feature — neither "fee-on-transfer" nor "rebasing" appears anywhere in the file — and it covers the settle path only. `take()` still moves an exact amount out, and the periphery above the singleton makes its own assumptions. V4 tolerating fee-on-transfer input is not V4 supporting fee-on-transfer tokens end to end.

One correction to the standard reading list, because it is a good illustration of the reference material aging faster than the chain. **PAXG no longer charges a transfer fee.** The deployed implementation contains no fee function among its seventy-seven dispatcher selectors, and the storage migration zeroes the old slots with the comment `sstore(14, 0) // was feeController`. Paxos's own repository documentation still describes `fee = debit.mul(feeRate).div(feeParts)`, and `d-xo/weird-erc20` still lists PAXG among fee-on-transfer tokens. Its asset-protection powers are live and have moved to `AccessControlDefaultAdminRules` with a three-hour admin delay, exposing `freeze`, `unfreeze`, `wipeFrozenAddress` and a working `pause` — none of which GoPlus scores, because PAXG is a proxy.

## The field no contract change reaches

One flag in the same response is not about the contract at all. `honeypot_with_same_creator` counts what else the deploying address has deployed, so no line of Solidity moves it — see [deployer history](/wiki/economics/finance/defi/token-false-alarms/liquidity-and-holders#deployer-history).

## What a deployer can act on

```text
lever                             clears           cost
--------------------------------  ---------------  ------------------------------
delete the function               yes              lose the capability entirely
make the value `constant`         yes              no setter, no later change
`immutable` constructor argument  yes              fixed at deploy, no storage slot
hard-cap inside the setter        no               keeps the capability, keeps flag
renounce ownership                mostly no        lose pause, blacklist, upgrade
timelock or multisig owner        no               no schema field can hold it
publish an audit                  no               no schema field can hold it
```

Only the top three move a boolean, and each of them is the same trade: the flag goes away because the ability goes away. There is a fourth lever, `metadata_modifiable`, that is cheap and usually overlooked — making `name` and `symbol` constant removes a setter most templates leave mutable for no reason.

GoPlus does document one free-text `note` field for exactly the fact its schema cannot hold, with the example `"note": "Contract owner is a multisign contract."` It goes unused on the tokens that would need it, governance-owned ones included — [the blank field](/wiki/economics/finance/defi/token-false-alarms/the-blank-field#there-is-a-field-for-the-missing-context-and-it-is-empty) carries the measurement.

The design conclusions, and how to check your own contract before anyone else does, are on [designing and self-checking](/wiki/economics/finance/defi/token-false-alarms/designing-and-self-checking).

## External links

- [GoPlus token security response fields](https://docs.gopluslabs.io/reference/response-details) — the field-by-field documentation quoted throughout
- [EIP-1967](https://eips.ethereum.org/EIPS/eip-1967) — standard proxy slots, written so tooling can read them
- [EIP-4626](https://eips.ethereum.org/EIPS/eip-4626) — the vault standard whose deposit path mints
- [EIP-1363](https://eips.ethereum.org/EIPS/eip-1363) — callbacks without a hook on plain `transfer`
- [d-xo/weird-erc20](https://github.com/d-xo/weird-erc20) — the catalogue of non-standard behaviours detectors are written against
- [Uniswap V3 unsupported tokens](https://developers.uniswap.org/docs/protocols/v3/concepts/unsupported-tokens) — the fee-on-transfer and rebasing position, stated by Uniswap
- [Circle's stablecoin-evm contracts](https://github.com/circlefin/stablecoin-evm) — `Blacklistable.sol` and the v2.2 balance-word packing
- [OpenZeppelin access control](https://docs.openzeppelin.com/contracts/5.x/access-control) — `Ownable`, `TimelockController`, and the recommendation to hand ownership to a contract
