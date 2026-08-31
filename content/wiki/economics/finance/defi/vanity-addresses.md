---
title: "Vanity Addresses and Salt Mining"
weight: 35
---

A *vanity address* is an Ethereum address whose hex encoding contains a desired pattern — a leading run of zeros, a recognisable prefix like `0xC0FFEE…`, or a trailing brand suffix. Because addresses are derived from a hash, a specific address cannot be requested; one has to be *mined*, by trying inputs until the output matches the filter.

Two distinct flavours of mining show up in practice. The math is the same in both — Keccak-256 has no exploitable structure, so each candidate is an independent uniform draw — while the input that varies, the cost of a hit, and the security implications are not.

| Variant | What you brute-force | What it produces |
|---|---|---|
| **EOA (externally owned account) vanity** | A 32-byte private key | A user/account address with a chosen pattern |
| **CREATE2 salt mining** | The 32-byte `salt` argument | A contract address with a chosen pattern |

## The Search Space

An [Ethereum](ethereum) address is the lower 20 bytes of the Keccak-256 hash of either a public key (for an EOA) or the deployer / salt / init-code triple (for a [CREATE2](https://eips.ethereum.org/EIPS/eip-1014) contract). 20 bytes is 40 hex characters, drawn from `[0-9a-f]`.

Because Keccak-256 is indistinguishable from a random oracle for this purpose, matching an `N`-hex-character prefix is a Bernoulli trial with success probability `16⁻ᴺ`. The expected number of attempts to find one match is `16ᴺ`:

| Pattern length | Expected attempts | Wall time at 1 GH/s |
|---|---|---|
| 4 hex chars | 6.5 × 10⁴ | < 1 ms |
| 6 hex chars | 1.7 × 10⁷ | ~17 ms |
| 8 hex chars | 4.3 × 10⁹ | ~4 seconds |
| 10 hex chars | 1.1 × 10¹² | ~18 minutes |
| 12 hex chars | 2.8 × 10¹⁴ | ~3 days |
| 16 hex chars | 1.8 × 10¹⁹ | ~580 years |

Each additional hex character costs 16×. Each additional zero *byte* (two hex chars at the same fixed value) costs 256×. The "wall time" column above assumes a modest single-GPU rig hashing at one billion guesses per second; high-end miners and clusters scale roughly linearly from there.

The distribution is geometric: the median is `0.69 × 16ᴺ` and the 99th percentile is around `4.6 × 16ᴺ`. Plan for variance: stopping at the mean leaves a ~37% chance of having found nothing.

## EOA Vanity Mining

For an externally-owned account, the address is:

```text
addr = keccak256(uncompressedPubKey)[12:]    // last 20 bytes
```

where `uncompressedPubKey` is the 64-byte secp256k1 public key (X and Y coordinates concatenated). Mining works like this:

1. Pick a random 32-byte private key `k`.
2. Compute the public key `K = k·G` on secp256k1.
3. Hash with Keccak-256 and take the last 20 bytes.
4. Check the pattern. If no match, increment `k` (or hash it) and retry.

Step 2 is the bottleneck. A scalar multiplication on secp256k1 is much more expensive than a Keccak round. Mature tools amortise this with the *trick*: do one full point multiplication to get a base point, then iterate by repeated point *additions* of `G`, which are far cheaper. GPU implementations process millions of candidates per kernel launch this way.

### Use Cases

- **Branding** — a recognisable prefix is more memorable than a random hash. Many [DAO](/wiki/economics/finance/defi/dao) treasuries, bridges, and OG project addresses are mined.
- **Phishing resistance** — users learn to recognise the prefix of a legitimate address. (Weak; attackers can mine confusable addresses too, which is exactly what [address poisoning](/wiki/economics/finance/fraud/address-poisoning) does with the truncated form every interface displays.)
- **Burn / sink addresses** — `0x000…dead`, `0x000…0000`, etc. These don't need mining since no one holds the key.

EOA vanity addresses **do not save gas**. The address only appears on chain when the EOA sends a transaction; the cost there is dominated by signature verification, not by the address bytes.

### The Profanity Vulnerability

[`profanity`](https://github.com/johguse/profanity) was the dominant open-source GPU EOA miner from roughly 2017 to 2022. In September 2022, [1inch disclosed](https://blog.1inch.io/a-vulnerability-disclosed-in-profanity-an-ethereum-vanity-address-tool-68ed7455fc8c/) that every key it produced was recoverable.

The flaw was in the seed:

- profanity used `xoshiro256**` to generate candidate keys.
- It seeded the pseudo-random number generator (PRNG) from a **32-bit value** (a `time(NULL)` cast or similar). 2³² states is exhaustively searchable on commodity hardware in hours.
- Given any single address-key pair from a profanity batch, an attacker could recover the seed by trying all 2³² values, and thereby recover *every other key the same run produced* — including the lucky one the user kept.

Multiple high-value wallets, including a vanity address holding Wintermute treasury funds, were drained. Total losses are estimated in the high tens of millions of USD.

{{< hint danger >}}
**Treat any EOA vanity address generated before late 2022 as compromised** unless you are certain the tool used a cryptographically strong seed (e.g. `/dev/urandom`, `getrandom(2)`). When in doubt, sweep funds to a freshly generated wallet and abandon the vanity key. PRNG seeding is the weakest link in any key-generation pipeline: a 32-bit seed is exhaustible on commodity hardware no matter how strong everything downstream of it is.
{{< /hint >}}

Modern forks (e.g. `profanity-2`, `vanity-eth`) seed from the OS entropy pool. Verify before running any tool that you found on GitHub — the original `profanity` repository is archived but the binaries are still floating around.

## CREATE2 Salt Mining

[`CREATE2`](https://eips.ethereum.org/EIPS/eip-1014) ([EIP](/wiki/economics/finance/defi/ethereum/eip)-1014) deploys a contract to a deterministic address derived from the deployer, a chosen 32-byte `salt`, and the hash of the init code:

```text
addr = keccak256(0xff ++ deployer ++ salt ++ keccak256(initCode))[12:]
```

The `salt` can be varied until the resulting `addr` carries the pattern. Unlike EOA mining there is no elliptic-curve step — each candidate is one Keccak-256 (the inner `keccak256(initCode)` is computed once and cached). GPU throughput on consumer cards is in the multi-GH/s range.

### Why Mine a Contract Address — Gas Savings

Leading zero bytes in a contract address translate directly into ongoing gas savings every time the address is used:

- **Calldata** — under [EIP-2028](https://eips.ethereum.org/EIPS/eip-2028), each zero byte in transaction calldata costs **4 gas** versus **16 gas** for a non-zero byte. An address embedded in calldata (e.g. as a `to` field, an argument encoded in the contract's application binary interface (ABI) format, a Multicall target) saves **12 gas per leading zero byte per call**.
- **Bytecode `PUSH`** — pushing the address as an immediate inside another contract uses `PUSHN` where `N` equals the number of significant bytes. An address with `k` leading zero bytes can be pushed with `PUSH(20-k)` instead of `PUSH20`, shrinking deployed bytecode by `k` bytes (200·`k` gas saved at deployment, plus a smaller code object forever after).

For a contract that is the target of millions of transactions — Seaport, Uniswap routers, the Gnosis Safe singleton — those 12-gas-per-byte savings dominate the one-time cost of mining. [OpenSea's Seaport 1.1](https://opensea.io/blog/articles/introducing-seaport-protocol) is the canonical example: its address `0x00000000006c3852cbEf3e08E8dF289169EdE581` has six leading zero bytes, saving 72 gas of calldata cost per call site that references it.

### The Math, Concretely

Each leading zero hex character is one factor of 16. Each leading zero *byte* is two zero hex chars at fixed positions, so 256× per byte:

| Leading zeros | Expected hashes | Calldata gas saved per call |
|---|---|---|
| 4 zero bytes (8 hex) | 4.3 × 10⁹ | 48 |
| 5 zero bytes (10 hex) | 1.1 × 10¹² | 60 |
| 6 zero bytes (12 hex) | 2.8 × 10¹⁴ | 72 |
| 7 zero bytes (14 hex) | 7.2 × 10¹⁶ | 84 |
| 8 zero bytes (16 hex) | 1.8 × 10¹⁹ | 96 |

Six zero bytes is the current practical sweet spot — feasible on a small GPU cluster in days, with savings substantial enough for protocol-tier contracts. Seven is rare; eight is the realm of dedicated mining campaigns and has been done only a handful of times.

### Tooling

- **[`create2crunch`](https://github.com/0age/create2crunch)** — by [0age](https://github.com/0age), Rust + OpenCL. Optimises specifically for *leading zero bytes*, scoring candidates by zero count rather than matching a literal prefix. The de-facto standard for gas-saving deploys.
- **[`ERADICATE2`](https://github.com/johguse/ERADICATE2)** — the CREATE2 sibling of `profanity`, by the same author. CUDA. Searches for leading/trailing patterns. Not affected by the profanity PRNG bug because the salt is not a secret — there is nothing to recover.
- **[`cast create2`](https://book.getfoundry.sh/reference/cast/cast-create2)** — Foundry's built-in CPU miner. Convenient for short prefixes (4–6 hex chars) where you don't need GPU throughput.

For shared-deployer scenarios, the standard pattern is to deploy via the [deterministic deployer at `0x4e59b44847b379578588920cA78FbF26c0B4956C`](https://github.com/Arachnid/deterministic-deployment-proxy) — a stateless `CREATE2` factory that exists at the same address on every [EVM](/wiki/economics/finance/defi/ethereum#the-ethereum-virtual-machine-evm) chain. Mining a salt against this deployer yields the same contract address everywhere, which matters for cross-chain protocols.

### Salt Mining Has No Cryptographic Risk

A salt is not a secret. It can be public, reused, and hard-coded; the safety of the deployed contract depends on the init code, not the salt. So unlike EOA mining there is no PRNG-quality concern — `rand()` is fine for salt search.

The one operational hazard is **front-running the deployment**: anyone watching the mempool can see your salt, race ahead with their own `CREATE2(yourSalt, theirInitCode)`, and brick your address. The standard mitigation is to deploy via a factory that hashes `msg.sender` into the salt or restricts who can call it — this is what the [Arachnid deterministic deployer](https://github.com/Arachnid/deterministic-deployment-proxy) does, and it's why Foundry's CREATE2 deployments are safe by default. See [`foundry-broadcast`](solidity/foundry-broadcast) for a concrete walkthrough of the failure mode.

## CPU vs. GPU

| Workload | CPU throughput | GPU throughput | Notes |
|---|---|---|---|
| EOA (secp256k1 + Keccak) | ~10⁵–10⁶ keys/s | ~10⁸–10⁹ keys/s | Limited by point arithmetic. |
| CREATE2 salt (Keccak only) | ~10⁶–10⁷ hashes/s | ~10⁹–10¹⁰ hashes/s | Pure Keccak; trivially parallel. |

A modern desktop GPU is roughly 1000× faster than a single CPU core for either job. For anything past ~8 hex characters of pattern, GPU is mandatory — CPU mining will be running long after the pattern stops being economically interesting.

Cloud GPU rentals (RunPod, vast.ai, Lambda Labs) are usually cheaper than buying hardware unless you mine continuously. Budget the rental against the gas savings you expect over the contract's lifetime: at six leading zero bytes, the breakeven is on the order of a million calls.

## Pitfalls

{{< hint danger >}}
**Don't import an EOA vanity key from an unverified tool.** The profanity incident is the canonical case, but the underlying risk — weak entropy, leaked seeds, compromised binaries — applies to every wallet generator. If branding matters, mine on an air-gapped machine with verified source and a strong RNG, and treat the resulting key with the same paranoia as a hardware-wallet seed phrase.
{{< /hint >}}

{{< hint warning >}}
**Salt mining for a fixed address requires a fixed init code.** Any change to constructor arguments, compiler version, or imported libraries changes `keccak256(initCode)` and invalidates the mined salt. Lock the build (compiler version, optimiser settings, library addresses) before mining, and re-mine if any of them change.
{{< /hint >}}

{{< hint warning >}}
**Don't conflate "leading zeros" with "small address."** `0x0000…ABCD` and `0xABCD…0000` are very different — only leading zeros translate into `PUSHN` and calldata gas savings, because the recursive length prefix (RLP) and ABI encodings are big-endian. Trailing-zero vanity addresses look pretty but save no gas.
{{< /hint >}}

{{< hint info >}}
**EIP-3541 reserved-prefix.** Contracts deployed to addresses starting with `0xef` are still legal, but contract *bytecode* starting with `0xef` is forbidden (reserved for EOF). This affects what your init code can return, not what addresses you can mine.
{{< /hint >}}

## External Links

- [EIP-1014: CREATE2](https://eips.ethereum.org/EIPS/eip-1014) — the deterministic-address opcode.
- [EIP-2028: Calldata gas cost reduction](https://eips.ethereum.org/EIPS/eip-2028) — the source of the zero-byte savings.
- [1inch disclosure of the profanity vulnerability](https://blog.1inch.io/a-vulnerability-disclosed-in-profanity-an-ethereum-vanity-address-tool-68ed7455fc8c/) — the post-mortem in the original author's words.
- [`create2crunch`](https://github.com/0age/create2crunch) — leading-zero-optimised salt miner (Rust + OpenCL).
- [`ERADICATE2`](https://github.com/johguse/ERADICATE2) — pattern-matching CREATE2 miner (CUDA).
- [Arachnid deterministic deployer](https://github.com/Arachnid/deterministic-deployment-proxy) — the canonical cross-chain CREATE2 factory at `0x4e59b44847b379578588920cA78FbF26c0B4956C`.
