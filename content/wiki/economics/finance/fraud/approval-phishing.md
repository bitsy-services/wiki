---
title: "Approval Phishing"
weight: 75
---

Approval phishing takes a victim's assets with the victim's own permission, granted in advance. The signature moves nothing; it grants a standing right to move things later, and the transfer that follows is submitted by the attacker, from the attacker's account, paying the attacker's gas, usually after the victim has closed the tab.

Everything below is signature semantics: what each prompt authorises, what it costs, and what evidence it leaves. How the victim reached the page that asks, and who built the script doing the asking, is on [wallet drainers](/wiki/economics/finance/fraud/wallet-drainer). [Address poisoning](/wiki/economics/finance/fraud/address-poisoning) takes funds with no signature at all.

## The allowance model

A [smart contract](/wiki/economics/finance/defi/smart-contract) cannot reach into an account and take tokens. The [ERC-20](/wiki/economics/finance/defi/ethereum/erc-20) standard has no mechanism for it: `transfer` moves the caller's own balance, and `transferFrom` moves someone else's only up to an allowance that owner set with `approve(spender, amount)`. Every deposit, swap, and stake is two steps — the owner approves, the contract pulls.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract Vault {
    // The user first sends their own transaction:
    //     token.approve(address(vault), amount)
    // Only after that can this contract move their tokens.
    function deposit(IERC20 token, uint256 amount) external {
        token.transferFrom(msg.sender, address(this), amount);
    }
}
```

Illustrative rather than production code: a real deposit needs return-value handling and accounting.

Two transactions per trade is one gas fee more than users tolerate, so interfaces began requesting `type(uint256).max`, an allowance so large it never needs raising again. That is a permanent right to the token's entire balance, including tokens acquired years later, until it is explicitly revoked. Allowances sit per owner, per spender, per token, per chain, and nothing expires them.

## setApprovalForAll

[ERC-721](/wiki/economics/finance/defi/ethereum/erc-721) and [ERC-1155](/wiki/economics/finance/defi/ethereum/erc-1155) have no amount to cap. One call to `setApprovalForAll(operator, true)` lets an operator move every token the owner holds in that collection, present and future. Marketplaces required it because a listing must stay fillable without another signature the moment a buyer appears, and because listing ten items should not cost ten approvals.

It is worse than an unlimited ERC-20 approval in one respect: that approval covers one fungible balance, this one covers items that are individually unique and individually priced, and revocation is all or nothing per collection.

## Off-chain signatures

Ethereum Improvement Proposal (EIP) 2612 added `permit` to the token contract itself: rather than sending an `approve` transaction, the owner signs a structured message that anyone holding it can submit to set the allowance. The signature costs no gas, broadcasts nothing, and creates no on-chain record. A victim who signs one and then checks their transaction history sees an empty afternoon.

The structure is EIP-712 typed data, which wallets can decode and display:

```text
domain   name, version, chainId, verifyingContract   which token, which chain
message  owner                                       who is granting
         spender                                     who may take
         value                                       how much
         nonce                                       replay counter
         deadline                                    valid until
```

A phishing page renders its own summary above the prompt; the wallet's decoding of those fields — which token, who may take, how much, until when — is the only account of what is being signed.

Permit2, Uniswap's shared approval contract, extends this to tokens that never implemented `permit`: the owner approves Permit2 once per token and thereafter signs off-chain permissions naming a spender, an amount, and an expiry. One signature can carry a batch of several tokens, each with its own amount and expiry, to a single spender — raising the blast radius from one token to a portfolio.

"It is only a signature, not a transaction" is the costliest misconception in this area: a signature granting an allowance is worth exactly what the tokens it names are worth, differs from a transaction only in who pays gas and when, and leaves nothing in the history for the victim to notice.

## Blind signing

`eth_sign` presents a 32-byte hash with no structure to decode, so signing one authorises whatever that hash preimages — a transfer, an approval, an order fill — and nothing in the prompt can say which. Wallets now warn hard on it or refuse it, and hardware wallets ship with blind signing disabled, because a device that cannot render the payload can only ask the user to confirm a hash they cannot read.

## Delegation

EIP-7702, live on Ethereum since the Pectra upgrade in May 2025, lets an externally owned account (EOA) sign an authorization pointing its address at contract code, so later calls to the account execute that code. Signed by the account's own key, it is what brings batching and sponsored gas to ordinary accounts.

The phishing surface is the batch: one call into delegated code can run an arbitrary sequence — approve three tokens, transfer a fourth — behind a single confirmation, so a wallet has to decode the sequence rather than the outer call. Analysts including Wintermute observed shortly after Pectra that a large share of early delegations pointed at one copy-pasted sweeper contract, used to empty accounts whose keys were already compromised — that use needs the key, not a signature.

## What each prompt authorises

```text
approve(spender, n)
  authorises   spender moves up to n of one token on one chain, until revoked
  costs        a transaction; the victim pays gas
  leaves       an approval entry in the victim's transaction history

setApprovalForAll(operator, true)
  authorises   operator moves any item in that collection, now and in future
  costs        a transaction; the victim pays gas
  leaves       an approval entry in history

permit (EIP-2612)
  authorises   the same standing right as approve, granted by signature
  costs        nothing
  leaves       nothing until someone submits it, then a transfer out

Permit2 batch
  authorises   several tokens, each with its own amount, to one spender
  costs        nothing
  leaves       nothing at signing time

eth_sign(hash)
  authorises   whatever the hash encodes, which the wallet cannot decode
  costs        nothing
  leaves       nothing

EIP-7702 authorization
  authorises   contract code to run as the account until it is replaced
  costs        nothing to sign; someone must submit it
  leaves       a delegation visible on the account once submitted
```

## Cases

**OpenSea, February 2022.** Seventeen users lost 254 items worth roughly $1.7 million. They held valid `setApprovalForAll` grants to the marketplace's Wyvern contract and had signed partial orders, which an attacker collected and completed during a contract migration. OpenSea's post-mortem found the signatures were harvested off its own site and remained fillable.

**A single address, September 2023.** Scam Sniffer and PeckShield reported about $24 million in staked-ether derivatives taken from one address after it signed `increaseAllowance` transactions on a phishing site. Those are on-chain and did appear in the victim's history, which is what separates this case from the `permit` variant above: the approvals were visible and still went unnoticed, and the transfers came later in the attacker's own transactions.

## Pitfalls and defence

**Revoke live approvals.** [revoke.cash](https://revoke.cash) and Etherscan's token-approval tool list what an address has granted on the chain being viewed. Each revocation is its own gas-paying transaction, per token and per chain. Zeroing an allowance does not invalidate an unsubmitted EIP-2612 `permit` signature, which dies only when its deadline passes or its nonce is consumed — and you can consume it yourself by submitting any `permit` of your own at the current nonce. Permit2 inverts this: because it pulls funds through its own allowance on the token, revoking the token's approval to Permit2 kills every outstanding Permit2 signature for that token at once, and `invalidateNonces` and `lockdown` do the same without touching the allowance.

**Approve exact amounts.** Some wallets now default to the amount the transaction needs and flag unlimited as a warning state, at the cost of an approval per trade.

**Read simulations for what they cannot see.** Simulation runs the pending transaction and shows the balance changes, which catches a straightforward drain. A signature has nothing to replay, so it falls outside simulation entirely; wallets that decode typed data can still show what a `permit` would grant, which is decoding rather than simulation. Neither knows what the spender will do a week later, and a site can hand one payload to the simulator and another to the wallet.

**An approval outlives its context.** It survives the front end that requested it, the domain going dark, and an upgrade of the token, since allowances live in the token's storage and a proxy upgrade preserves storage.

## Where the law lands

The theft is charged as wire fraud and money laundering; no statute makes an approval revocable after the fact. Recovery depends on the asset: a centralized issuer can freeze its own token and an exchange can freeze a deposit under [anti-money laundering](/wiki/economics/finance/regulation/anti-money-laundering) obligations at the [cash-out](/wiki/economics/finance/fraud/cashing-out) stage, while ether has neither. A token whose owner can freeze balances at will has [hidden admin controls](/wiki/economics/finance/fraud/hidden-admin-controls), the same power pointed the other way.

## External links

- [EIP-2612](https://eips.ethereum.org/EIPS/eip-2612) — the `permit` specification, typed-data struct and nonce handling
- [EIP-712](https://eips.ethereum.org/EIPS/eip-712) — typed structured data, what makes a signature prompt readable
- [EIP-7702](https://eips.ethereum.org/EIPS/eip-7702) — set-code authorizations for externally owned accounts
- [Uniswap Permit2](https://github.com/Uniswap/permit2) — the contract, its batched permission types and expiries
- [revoke.cash](https://revoke.cash) — allowance viewer and revocation across chains
