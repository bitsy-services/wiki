---
title: "Sui Move"
weight: 20
---

Move is a resource-oriented programming language created at Meta for the Diem (Libra) project. When that project wound down, the language survived its sponsor: it now underpins several chains, of which Sui is the most prominent. **Sui Move** is Mysten Labs' dialect, adapted to fit Sui's [object model](/wiki/economics/finance/defi/sui/object-model) rather than the account storage of the original ("core") Move and its other major descendant, Aptos Move. [IOTA](/wiki/economics/finance/defi/iota/) runs the same Mysten dialect, so the material here applies there too.

The language's central idea is that on-chain assets should be ordinary typed values that the type system refuses to copy, drop, or otherwise mishandle. This is the opposite of [Solidity](/wiki/economics/finance/defi/solidity/), where a token balance is just a number in a mapping and nothing in the language stops you from forgetting to update it. If you write [smart contracts](/wiki/economics/finance/defi/smart-contract) on [Ethereum](/wiki/economics/finance/defi/ethereum/), Move will feel both familiar and strange: the tooling rhymes, but the safety guarantees are enforced by the compiler instead of by convention.

## Resources and Linear Types

A `struct` in Move is a value with *linear* (or "affine") semantics. By default the type system will not implicitly copy it and will not let it silently go out of scope. Once you hold one, you must do something deliberate with it — return it, store it, or pass it on. You cannot duplicate a coin by assigning it to two variables, and you cannot lose one by dropping it on the floor; both are compile errors. Whole bug classes — accidental token loss, double-spends from a stray copy — are simply not expressible.

This is what "resource-oriented" means in practice. An asset is not a number you remember to decrement; it is a value the compiler tracks from creation to destruction.

## Abilities

Move controls what can be done with a type through four **abilities**, declared with `has`:

- `copy` — the value may be duplicated.
- `drop` — the value may be discarded without being used.
- `store` — the value may be stored inside another struct and persisted, and (as an owned object) transferred between addresses.
- `key` — the struct is a top-level Sui object. A `key` struct **must** have a `UID` as its first field, named `id`.

A real asset deliberately *omits* `copy` and `drop` — that omission is what makes it scarce and conserved. A typical Sui object carries `key` and `store`:

```move
module my_pkg::sword {
    use sui::object::UID;

    public struct Sword has key, store {
        id: UID,
        strength: u64,
    }
}
```

`key` lets `Sword` exist as a standalone object the protocol can own and address; `store` lets it be embedded in another object (say, a chest) or transferred via the generic transfer functions below.

## No Global Storage

This is the single biggest difference between Sui Move and core/Aptos Move. In core Move, contracts read and write a per-account global store with `move_to`, `borrow_global`, and `move_from`. Sui Move has none of that. State lives entirely in [objects](/wiki/economics/finance/defi/sui/object-model), and a function can only touch the objects explicitly passed into it.

Functions marked `public` or `entry` therefore take objects as parameters. There is no ambient "the caller's storage" to reach into — if a function needs an object, that object must appear in its signature, which is exactly what lets Sui schedule non-overlapping transactions in parallel. To get an object back out to a user, you call one of:

- `transfer::transfer` — give an object to an address (the object's module must define this for its own type).
- `transfer::public_transfer` — the same, for any type with `store`, callable from outside the defining module.
- `transfer::share_object` — make an object *shared*, so anyone may reference it (this is how AMM pools and order books are built).

```move
module my_pkg::sword {
    use sui::object::{Self, UID};
    use sui::tx_context::TxContext;
    use sui::transfer;

    public struct Sword has key, store {
        id: UID,
        strength: u64,
    }

    /// Mint a new Sword and hand it to `recipient`.
    public entry fun mint(strength: u64, recipient: address, ctx: &mut TxContext) {
        let sword = Sword { id: object::new(ctx), strength };
        transfer::transfer(sword, recipient);
    }
}
```

`object::new(ctx)` draws a fresh `UID` from the transaction context; `transfer` consumes the `sword` value, satisfying the linear-type rule that it must be disposed of deliberately.

## Modules and Packages

Code is organized into **modules** (`module pkg::name { ... }`), and modules are grouped into **packages** that you publish as a unit. A published package is itself an immutable on-chain object — its bytecode cannot be mutated in place. Upgrades work through a versioned upgrade policy: you publish a new version of the package and migrate, rather than patching the deployed code. This makes "the code at this address can change under you" a non-default, opt-in property, unlike a Solidity proxy.

## The Move 2024 Edition

Sui Move's syntax was substantially revised in the **Move 2024** edition, which is now the default for new packages. Highlights:

- **Method syntax** — call `x.foo(y)` instead of `module::foo(x, y)` when `foo` takes the receiver as its first argument.
- **Enums** — sum types with named or positional variants, enabling exhaustive `match`.
- **Macro functions** — `macro fun` bodies inline at the call site and accept lambdas, giving higher-order patterns (`vector::for_each!`) without runtime closures.
- **Positional fields** — tuple-style structs like `public struct Wrapper(Coin<SUI>)`.
- **`public(package)`** — replaces the old `friend` mechanism for intra-package visibility; the compiler infers the rest.

Note that `public struct` (rather than bare `struct`) and ability annotations are required in this edition.

## Contrast with Solidity

| | Sui Move | Solidity |
|---|---|---|
| Assets | linear typed values, conserved by the compiler | numbers in mappings, conserved by hand |
| Reentrancy | impossible for owned objects (no shared mutable global state to re-enter) | a perennial vuln class requiring guards |
| Ownership | explicit and protocol-tracked | implicit in storage layout |
| Verification | designed for formal verification (Move Prover) | bolted on after the fact |

The tradeoff is real. Move has a steeper learning curve — linear types and the no-global-storage model force a different mental model — and a smaller, younger tooling and library ecosystem than the EVM's. You are trading a large, battle-tested-but-footgun-laden world for a smaller, safer-by-construction one.

## External Links

- [The Move Book](https://move-book.com/) — the canonical Sui Move language reference
- [Sui Move Concepts](https://docs.sui.io/concepts/sui-move-concepts) — official docs on packages, modules, and abilities
- [Move Adds Enums and Macros in 2024 Edition](https://blog.sui.io/move-edition-2024-update/) — the Move 2024 feature announcement
