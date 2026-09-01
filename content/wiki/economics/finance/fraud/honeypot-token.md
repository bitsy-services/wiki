---
title: "Honeypot Token"
weight: 25
---

A honeypot token is one that can be bought and cannot be sold. The trap sits in the transfer path from the first block, so the price history reveals nothing: buys confirm, the holder count climbs, the chart rises, and every attempt to exit reverts or returns nothing. A [rug pull](/wiki/economics/finance/fraud/rug-pull) removes the pool after the fact and leaves a real, if worthless, market behind; a honeypot never had an exit, and the deployer is the only address that ever realises a price.

Because the restriction lives in the token rather than in the [decentralized exchange](/wiki/economics/finance/defi/dex), the pair contract behaves correctly throughout. A sale on a [constant-product](/wiki/economics/finance/defi/constant-product-formula) pair is a transfer of the token *to* the pair address, so any condition the token places on `to == pair` is a condition on selling and on nothing else. Buys, which are transfers *from* the pair, sail through untouched. This is one instance of [hidden admin controls](/wiki/economics/finance/fraud/hidden-admin-controls), distinguished by being hostile at deployment rather than switched on later.

## Mechanisms

The snippets below are illustrative and minimal: an [ERC-20](/wiki/economics/finance/defi/ethereum/erc-20) from OpenZeppelin v5, where every transfer, mint, and burn routes through the `_update` hook, cut down to the line that does the work.

**An allowlist on the sell side.**

```solidity
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract Allowlisted is ERC20, Ownable {
    address public pair;
    mapping(address => bool) public canSell;

    constructor() ERC20("Token", "TKN") Ownable(msg.sender) {}

    function _update(address from, address to, uint256 value) internal override {
        if (to == pair) require(canSell[from], "not allowed");
        super._update(from, to, value);
    }
}
```

**A sell tax with no upper bound.** The tax pattern is ordinary; the missing bound is the trap.

```solidity
uint256 public sellFeeBps = 300;                    // 3% at launch

function setSellFee(uint256 bps) external onlyOwner { sellFeeBps = bps; }

function _update(address from, address to, uint256 value) internal override {
    if (to == pair && sellFeeBps > 0) {
        uint256 fee = value * sellFeeBps / 10_000;
        super._update(from, owner(), fee);
        value -= fee;
    }
    super._update(from, to, value);
}
```

`setSellFee(10_000)` routes the entire transfer to the owner. Nothing reverts, so a check that asks only whether the transaction succeeded records a success while the seller receives zero.

**A transaction cap or cooldown set to nothing.** Maximum transaction sizes and per-address cooldowns are on thousands of legitimate launches as anti-bot measures, which is what makes them useful cover.

```solidity
uint256 public maxTxAmount;                         // 0 for everyone not exempt
uint256 public cooldown = 365 days;
mapping(address => uint256) public lastBuy;

function _update(address from, address to, uint256 value) internal override {
    if (to == pair) {
        require(value <= maxTxAmount, "over max");
        require(block.timestamp >= lastBuy[from] + cooldown, "cooldown");
    }
    if (from == pair) lastBuy[to] = block.timestamp;
    super._update(from, to, value);
}
```

**Balance rewriting.** `balanceOf` is a view function and no transfer consults it.

```solidity
uint256 private _scale = 1e18;                      // owner-settable

function balanceOf(address a) public view override returns (uint256) {
    return super.balanceOf(a) * _scale / 1e18;
}
```

A wallet showing a million tokens is reporting what the token chose to report. The transfer path reads the underlying mapping, so a sale sized from the displayed balance reverts for insufficient funds and a smaller sale delivers a fraction of what the interface promised. Rebasing tokens do exactly this legitimately, so the pattern is not on its own a signal.

**External state.** The rule is not in the token at all.

```solidity
interface IPolicy {
    function check(address from, address to, uint256 v) external view returns (bool);
}

address public policy;                              // owner-settable

function _update(address from, address to, uint256 value) internal override {
    require(IPolicy(policy).check(from, to, value), "blocked");
    super._update(from, to, value);
}
```

The token's verified source contains no restriction, only a call to an address the deployer controls and can repoint. Reading the token teaches nothing about whether it can be sold, and the [contract](/wiki/economics/finance/defi/smart-contract) holding the answer is frequently unverified.

## Why one simulation is not enough

A honeypot check simulates a buy followed by a sell against current chain state, using `eth_call` against a forked node or a state override, and reports whether the sell succeeded and what it returned. Against an allowlist, a zero transaction cap, or a hostile policy contract set at deploy time, this works: the simulated sell reverts. Against a 100% tax it works only if the check compares proceeds against expectation, since nothing reverts.

What a single simulation cannot see is a later block. `setSellFee`, `setMaxTxAmount`, and `setPolicy` are one owner transaction each, and the contract is benign when scanned and hostile in the block after that transaction lands. A scanner reports on state at block N; the holder sells at block N + 5,000. The same gap swallows an implementation swap behind a proxy, where every line of the audited code is replaced without the address changing.

Simulation is also gameable directly. A token can allowlist the addresses public scanners are known to simulate from, gate its restriction on `block.number` so it activates after the launch window, or condition on properties the synthetic simulation account does not share with a real holder.

## Detection

- **Check whether anyone other than the deployer has sold.** Read the pair's swap events in the token-to-base direction and confirm the sellers are neither the deployer nor addresses it funded. A token with four hundred buys and no third-party sells is a honeypot until shown otherwise, and this evidence is behavioural rather than static, so it survives every evasion above.
- **Read the transfer path.** Every mechanism here lives in `_update` or `_transfer`. Follow each branch to the end and note every value in those branches that an external function can set.
- **List the owner-settable functions and their bounds.** A fee setter with no maximum, a cap setter, and a policy or router address setter are each sufficient on their own, whatever their current values.
- **Check for a proxy.** An implementation address at the standard proxy storage slot means the source read today is not a commitment about tomorrow.
- **Treat scanners as a filter rather than a verdict.** Public honeypot simulators catch the static cases cheaply and in bulk, and they are simulating exactly the state that an owner transaction changes. They also fire on honest contracts often enough that the failure has its own literature — [token false alarms](/wiki/economics/finance/defi/token-false-alarms).

## Where the law lands

Honeypots are deployed pseudonymously and cheaply, often in batches from a [permissionless token factory](/wiki/economics/finance/defi/permissionless-token-factory), with each token's take measured in thousands of dollars. Where a deployer has been identified, United States charges have followed the same pattern as other token frauds — wire fraud on the misrepresentation, plus money laundering on the proceeds — and the Securities and Exchange Commission's unregistered-offering theory under [financial regulation](/wiki/economics/finance/regulation) applies to the sale itself. Identification is the binding constraint, and the per-token amounts are far below the threshold at which most prosecutors open a file.

## External links

- [ERC-20 in OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/5.x/erc20) — the `_update` hook every mechanism above overrides
- [EIP-20](https://eips.ethereum.org/EIPS/eip-20) — the standard, which places no constraint on what a transfer may refuse
- [How Uniswap works](https://docs.uniswap.org/contracts/v2/concepts/protocol-overview/how-uniswap-works) — why a sale is a transfer to the pair address
- [Ethereum JSON-RPC API](https://ethereum.org/en/developers/docs/apis/json-rpc/) — `eth_call`, the primitive every honeypot simulator is built on
- [honeypot.is](https://honeypot.is/) — a public simulator, useful as the filter described above
