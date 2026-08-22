---
title: "zkLogin"
weight: 60
---

zkLogin is Sui's native primitive for controlling an on-chain address with an existing Web2 login. A user signs in with Google, Apple, Facebook, Twitch, or any other OpenID Connect provider, and from that login alone derives and operates a fully self-custodial Sui address — no seed phrase, no browser extension, no private key for the user to back up. It is the mechanism behind the onboarding pitch in the [Sui overview](/wiki/economics/finance/defi/sui/): log in with Google, start transacting.

The trick is that the credential proving who you are never touches the chain, and the chain never learns which Google account is behind an address. Both properties fall out of a [zero-knowledge proof](/wiki/cs/zero-knowledge-proofs) over the login token. To follow the rest of this page it helps to know two acronyms: **OAuth 2.0** is the protocol that lets one site delegate "sign in with X" to a provider; **OpenID Connect (OIDC)** is the identity layer on top of OAuth that has the provider return a signed **JWT** (JSON Web Token) asserting who the user is.

## How a Login Becomes an Address

The flow chains together a throwaway key, a standard OAuth login, a secret salt, and a proof.

1. **Ephemeral key pair.** The wallet or [dApp](/wiki/economics/finance/defi/dapp) generates a fresh key pair in the browser. It is deliberately short-lived: the user picks a `max_epoch` (a Sui epoch is ~24 hours), after which the key is dead and the user must log in again. Nothing about this key persists.

2. **OAuth/OIDC login with a committed nonce.** The app runs the ordinary "sign in with X" redirect, but sets the OIDC `nonce` to a commitment over the ephemeral *public* key, the `max_epoch`, and some randomness (`jwt_randomness`). The provider authenticates the user normally and returns a JWT — a payload it has signed with its RSA key — that echoes back that nonce. Because the provider signed a token containing a commitment to the ephemeral key, that key is now cryptographically bound to this login session without the provider ever knowing it is a blockchain key.

3. **Address derivation from the JWT plus a salt.** The JWT carries the standard OIDC claims: `sub` (the provider's stable identifier for the user), `iss` (which provider issued it), and `aud` (which application it was issued to). A separate **user salt** — a secret value the OAuth provider does *not* hold — is folded in, and the Sui address is derived as a hash of `sub`, `iss`, `aud`, and the salt. The salt is what unlinks the address from the OAuth identity: the same Google account with two different salts yields two unrelated addresses, and nobody can reverse an address back to a Google account without the salt.

4. **Zero-knowledge proof.** A proving service takes the JWT and produces a [zero-knowledge proof](/wiki/cs/zero-knowledge-proofs) attesting that the holder possesses a valid, provider-signed OIDC credential whose claims derive the claimed address — *without revealing the credential*. The sensitive `sub` is a private input and never leaves the proof; `iss`, `aud`, and `kid` (the key ID identifying which provider signing key was used) are public, so any Sui validator can fetch the provider's published key and verify the RSA signature itself. Transactions are then signed by the ephemeral key and submitted with the proof attached. Validators check the proof and the signature, and the transaction settles like any other.

The chain therefore verifies "this person holds a current login from Google for this app, and that login maps to this address" while learning neither the person's identity nor their salt.

## The Two-Factor Security Model

zkLogin is a two-factor scheme, and this is the single most important thing to internalize. To move funds you need **both** a fresh OAuth login **and** the salt. Compromising the Google account alone is useless to an attacker — without the salt they cannot reconstruct the address or its proof. This is a genuine security upgrade over a single seed phrase.

The flip side is symmetric: lose access to **both** the salt and the OAuth account and the address is gone forever, exactly like a lost seed phrase. So **salt management is the central design decision** of any zkLogin integration, and it is fundamentally a custody tradeoff:

- **User-managed salt** — the user stores their own salt (a password, an exported file). Maximally trustless, but reintroduces a secret the user can lose, which partly undercuts the seedless UX.
- **App backend** — the dApp stores per-user salts server-side, keyed by the OAuth identity. Smooth UX, but the backend operator can now derive the user's address, so it is a custodial-flavored compromise and a breach target.
- **Salt service** — a dedicated service (e.g. behind a hardware-backed enclave) returns the salt only on presentation of a valid JWT. Better isolation than co-locating salts with app data, but it is still infrastructure that must stay available and honest.

There is no universally correct choice; pick based on how much custody risk and how much liveness dependency the application can tolerate.

## Privacy

Because the credential is consumed inside the zero-knowledge proof, no third party — and not even the OAuth provider — can link an on-chain zkLogin address back to the underlying Google or Apple identity. The provider sees an ordinary login with an opaque nonce; observers see an address and a proof. The salt is what severs the last link between `sub`/`iss`/`aud` and the address, so even someone who later learns the JWT cannot find the address without it.

## Why It Matters

Seed phrases are the largest onboarding barrier in crypto: they are intimidating, easy to lose, and a magnet for phishing. zkLogin removes them while keeping the address self-custodial — the user, not a company, authorizes every transaction with their ephemeral key. Contrast this with custodial "social login" wallets, where signing in with Google really means a service holds the keys on your behalf and you are trusting them not to freeze or seize the account. zkLogin gives the same one-tap experience without surrendering custody.

## Gotchas and Limitations

Ordered by severity:

- **Salt loss is fund loss.** Losing both the salt and the OAuth account permanently locks the address. Whatever salt-management approach you choose, its durability and recoverability *is* the wallet's recoverability. Treat it with the seriousness of seed-phrase backup.
- **Dependence on the OAuth provider.** If the provider is down, suspends the account, or deletes it, the user cannot log in and therefore cannot transact. Providers also rotate their OIDC signing keys; the chain must track the current `kid` set, and a rotation that outpaces this tracking can temporarily break verification for affected tokens.
- **Proving-service trust and liveness.** Most integrations call a hosted proving service to generate the proof. The proof is verified on-chain so a malicious prover cannot forge transactions, but a slow or offline prover blocks the user from transacting, and a service that sees JWTs is a privacy consideration. Self-hosting the prover removes the dependency at the cost of running the infrastructure.

## External Links

- [What is zkLogin? — Sui Documentation](https://docs.sui.io/concepts/cryptography/zklogin)
- [zkLogin Demystified — Sui Blog deep dive](https://blog.sui.io/zklogin-deep-dive/)
- [zkLogin: Privacy-Preserving Blockchain Authentication with Existing Credentials (paper)](https://arxiv.org/abs/2401.11735)
