---
title: "ERC-20"
weight: 10
---

ERC-20 — the twentieth [Ethereum Request for Comment](/wiki/economics/finance/defi/ethereum/eip) — is the standard interface for fungible tokens on [Ethereum](/wiki/economics/finance/defi/ethereum/). Proposed by Fabian Vogelsteller in 2015 ([EIP](/wiki/economics/finance/defi/ethereum/eip)-20), it defines six functions and two events that every compliant token must implement. Wallets, [DEXs](/wiki/economics/finance/defi/dex), lending protocols, and aggregators all speak ERC-20, so a token that implements the interface is tradeable and usable as collateral on the day it deploys, without asking any of them to add support for it.

## The interface

```solidity
interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
```

The two-step `approve` + `transferFrom` pattern is the standard way for a [smart contract](/wiki/economics/finance/defi/smart-contract) to spend tokens on behalf of a user. The user first approves a spending allowance, then the contract calls `transferFrom` to pull the tokens.

## Non-standard tokens and gotchas

The ERC-20 spec says `transfer` and `transferFrom` must return `bool`, but several widely-used tokens deviate:

### USDT (no return value)

Tether's `transfer` and `approve` functions return nothing. A [Solidity](/wiki/economics/finance/defi/solidity/) contract that checks the return value with `require(token.transfer(...))` will revert when interacting with USDT, because the [EVM](/wiki/economics/finance/defi/ethereum#the-ethereum-virtual-machine-evm) interprets the missing return data as a failed `bool` decode.

### Fee-on-transfer tokens

Some tokens deduct a fee on every transfer. If your contract assumes that the amount received equals the amount sent, accounting will silently break. The safe pattern is to measure the balance before and after the transfer:

```solidity
uint256 before = token.balanceOf(address(this));
token.safeTransferFrom(msg.sender, address(this), amount);
uint256 received = token.balanceOf(address(this)) - before;
```

### Rebasing tokens

Tokens like stETH change every holder's balance automatically. Contracts that cache a balance and assume it stays constant will miscalculate. Most DeFi protocols use the wrapped, non-rebasing variant (wstETH) instead.

### Approval race condition

If a user calls `approve` to change an existing non-zero allowance, a malicious spender can front-run and spend both the old and new allowances. The standard mitigation is to set the allowance to zero first, then set the new value — or use `increaseAllowance` / `decreaseAllowance` (not part of the ERC-20 spec but widely available in OpenZeppelin's implementation).

## SafeERC20

OpenZeppelin's `SafeERC20` library wraps all ERC-20 calls to handle non-standard tokens. It:

- Uses low-level `call` and checks the return data length, accepting both `true` and empty return values.
- Provides `safeTransfer`, `safeTransferFrom`, `safeApprove`, `safeIncreaseAllowance`, and `safeDecreaseAllowance`.

Always use `SafeERC20` when writing contracts that interact with arbitrary tokens:

```solidity
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract Vault {
    using SafeERC20 for IERC20;

    function deposit(IERC20 token, uint256 amount) external {
        token.safeTransferFrom(msg.sender, address(this), amount);
    }
}
```

## Permit (EIP-2612)

EIP-2612 extends ERC-20 with a `permit` function that allows approvals via off-chain signatures instead of a separate on-chain `approve` transaction. The user signs a typed message; the contract calls `permit` to set the allowance and `transferFrom` in a single transaction. It removes one on-chain transaction from every approve-then-spend flow, and with it the standing allowance that would otherwise sit between the two.

## Related standards

| Standard | Purpose |
|----------|---------|
| ERC-721 | Non-fungible tokens (NFTs) — each token has a unique ID. |
| ERC-1155 | Multi-token standard — supports both fungible and non-fungible tokens in one contract. |
| ERC-777 | Backwards-compatible extension with hooks for send/receive. Never gained wide adoption due to reentrancy concerns. |
| ERC-4626 | Tokenised vault standard — extends ERC-20 with deposit/withdraw/redeem for yield-bearing vaults. |

## What the standard leaves out

The interface carries `name`, `symbol` and `decimals` and nothing else about the token's identity. There is no icon, no website, no description, and no issuer field, so every logo a wallet or explorer displays comes from an off-chain database that somebody had to submit the token to. [Token registration](/wiki/economics/finance/defi/token-registration) covers where those databases are and what each one asks for. [ERC-1046](/wiki/economics/finance/defi/token-registration/on-chain-metadata) adds an optional `tokenURI` that puts the metadata document back on the contract, at the cost of near-zero adoption among the things that would read it.

## External links

- [EIP-20 specification](https://eips.ethereum.org/EIPS/eip-20) — the canonical standard
- [OpenZeppelin ERC20 implementation](https://docs.openzeppelin.com/contracts/5.x/erc20) — the reference implementation most deployed tokens inherit from
- [OpenZeppelin SafeERC20](https://docs.openzeppelin.com/contracts/5.x/api/token/erc20#SafeERC20) — library documentation
- [EIP-2612: Permit](https://eips.ethereum.org/EIPS/eip-2612) — gasless approval extension
