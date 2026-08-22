---
title: "Security"
weight: 18
bookCollapseSection: true
---

Practical, hands-on guides to handling secrets, keys, and credentials on developer machines -- the operational side of security, as distinct from the cryptographic theory covered under [Computer Science](/wiki/cs). The concern here is mundane and constant: private keys, API tokens, and `.env` files accumulate across a machine, and in a repository full of [smart contract](/wiki/economics/finance/defi/smart-contract) deploy scripts, a leaked key is not a recoverable mistake.

The three pages describe one stack, and read best from the top down.

[`pass`](/wiki/security/pass) is the interface: a thin shell wrapper over GPG and git that keeps every secret as an individually encrypted file in a versioned store, so you get history and sync without ever committing plaintext.

[GPG](/wiki/security/gpg) is the engine underneath it -- the OpenPGP implementation doing the actual encryption and signing, and worth understanding directly because `pass` inherits its key model, its trust model, and its failure modes.

[YubiKey](/wiki/security/yubikey) is the hardening step. Its OpenPGP smartcard applet holds the GPG private key on the device, so the private material never touches disk and never leaves the hardware -- decryption happens on the key, with a physical touch, or it does not happen at all.

## Wiki Pages

{{< section >}}
