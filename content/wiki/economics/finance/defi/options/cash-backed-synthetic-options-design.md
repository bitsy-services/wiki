---
title: Cash-Backed Synthetic Options Design
weight: 81
---

The [Cash-Backed Synthetic Option (CBSO)](/wiki/economics/finance/defi/options/cash-backed-synthetic-option) system is four contracts -- Option, Option Factory, Option Settler, and [Fee Box](/wiki/economics/finance/defi/fee-box) -- plus an external Asset Price Oracle that the first three all read from.

## Option Contract

The Option contract is the core unit. Each instance represents a single CBSO with specific parameters:

| Property | Description |
|----------|-------------|
| Asset Price Oracle | The [oracle](/wiki/economics/finance/defi/oracle-node) providing price data for the underlying asset |
| [Option Type](/wiki/economics/finance/defi/options/option-type) | Put or call |
| Stake | The collateral amount backing the option |
| [Strike Price](/wiki/economics/finance/defi/options/strike-price) | The price at which the option settles |
| Expiry | The expiration timestamp |
| [Fee Box](/wiki/economics/finance/defi/fee-box) | The contract that receives [collateralization fees](/wiki/economics/finance/defi/collateralization-fee) after settlement |

Each Option is an [ERC-20](/wiki/economics/finance/defi/ethereum/erc-20) token, making it transferable and tradeable on any [DEX](/wiki/economics/finance/defi/dex).

### Key Functions

- **`exercise()`** -- Allows the holder to exercise the option if it is in the money at expiry.
- **`burn()`** -- Destroys the token, called during settlement or when a minter buys back their position.
- **`isExpired()`** -- Returns whether the option has passed its expiration timestamp.
- **`getIntrinsicValue()`** -- Calculates the current intrinsic value based on the oracle's latest price data.

## Asset Price Oracle

The Asset Price Oracle aggregates price reports from decentralized [oracle nodes](/wiki/economics/finance/defi/oracle-node) to determine the fair market value of the underlying asset. It supports any asset with a reliable price feed -- cryptocurrencies, equities, commodities, or custom indices.

### Key Functions

- **`updatePrice()`** -- Accepts new price data from authorized oracle nodes.
- **`getPrice()`** -- Returns the latest aggregated price.
- **`finalizePrice()`** -- Locks the price at expiry, making it immutable for settlement. Once finalized, the oracle becomes a [finalized smart contract](/wiki/economics/finance/defi/finalized-smart-contract) for that expiry -- its state can no longer change.

Finalization is what makes every option sharing an expiry settle against the same number, which closes both the race between settlement calls and the front-running that a still-moving price would invite.

## Option Factory

The Option Factory is the entry point for minters. It handles option creation and ensures each new option is registered with the correct settler.

### Key Functions

- **`mint(optionType, stake, strike, expiry)`** -- Creates a new Option with the specified parameters. The minter deposits collateral equal to the stake plus the [collateralization fee](/wiki/economics/finance/defi/collateralization-fee). The factory registers the option with the appropriate Option Settler (creating one if needed) and transfers the minted tokens to the minter.
- **`getOption(address)`** -- Returns the details of a previously minted option.
- **`createSettler(expiry)`** -- Creates a new Option Settler for a given expiry if one does not already exist.

## Option Settler

The Option Settler manages all options for a given asset and expiry. After the oracle finalizes the price, the settler calculates payouts and distributes collateral.

### Key Functions

- **`addOption(address)`** -- Registers an option with this settler.
- **`settleAll()`** -- Iterates through all registered options, calculates each payout based on the finalized oracle price, distributes collateral to holders and minters, and forwards accumulated [collateralization fees](/wiki/economics/finance/defi/collateralization-fee) to the [Fee Box](/wiki/economics/finance/defi/fee-box).
- **`settleSingle(address)`** -- Settles one option independently.
- **`removeOption(address)`** -- Removes a fully settled and burned option from the registry.

## Fee Box

The [Fee Box](/wiki/economics/finance/defi/fee-box) is the terminal destination for [collateralization fees](/wiki/economics/finance/defi/collateralization-fee). It collects fees after settlement and manages their distribution to protocol stakeholders. See the dedicated [Fee Box](/wiki/economics/finance/defi/fee-box) page for details on its interface and security model.

## Option Lifecycle

The full lifecycle of a CBSO flows through these contracts in sequence:

1. **Minting.** The minter calls `Option Factory.mint()`, depositing collateral and paying the collateralization fee. The factory creates the Option contract and registers it with the appropriate Option Settler.

2. **Trading.** The minted ERC-20 tokens circulate freely. Holders can trade them on [DEXs](/wiki/economics/finance/defi/dex), transfer them between wallets, or hold until expiry.

3. **Buy-back (optional).** A minter can purchase tokens on the open market and call `burn()` to reclaim a prorated share of collateral and fees.

4. **Price finalization.** [Oracle nodes](/wiki/economics/finance/defi/oracle-node) push price updates throughout the option's life via `updatePrice()`. At expiry, `finalizePrice()` locks the settlement price.

5. **Settlement.** A [decentralized keeper](/wiki/economics/finance/defi/decentralized-keeper) or any external caller triggers `settleAll()` on the Option Settler. The settler distributes payouts to holders based on the finalized price, returns remaining collateral to minters, and forwards collected fees to the Fee Box.

## Security Considerations

**Oracle integrity.** The system's correctness depends entirely on the oracle delivering an accurate finalized price. Using a decentralized oracle network (such as a [staked consensus oracle](/wiki/economics/finance/defi/staked-consensus-oracle)) mitigates single-point-of-failure risk, but oracle manipulation remains the highest-severity threat to the system.

**Collateral custody.** All collateral is held in [smart contracts](/wiki/economics/finance/defi/smart-contract) on [Ethereum](/wiki/economics/finance/defi/ethereum/), not in any custodial account. The contracts are the sole authority over fund movement.

**Settlement atomicity.** The `settleAll()` function must handle gas limits carefully when processing large numbers of options. The `settleSingle()` escape hatch allows individual settlement if a batch operation would exceed block gas limits.
