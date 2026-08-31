---
title: "YubiKey"
weight: 30
---

A **YubiKey** is a small USB (and NFC) hardware authenticator made by Yubico. Among several applets it implements an **OpenPGP smartcard**, which can hold [GPG](/wiki/security/gpg) private keys on the device itself. Once a key is moved onto the card, the private material never exists on disk and never leaves the hardware -- cryptographic operations happen *on* the YubiKey, and the host only sends in ciphertext and gets back plaintext.

This makes it the natural hardening step for a [`pass`](/wiki/security/pass) store: the GPG key that can decrypt every secret stops being a file an attacker can copy and becomes a physical object you hold. With a touch policy enabled, each decryption also requires a deliberate tap, so malware cannot silently drain the store even while the key is plugged in.

## WebAuthn and FIDO2

The same device implements a second, unrelated applet: FIDO2/WebAuthn, the standard behind "security key" logins. A credential here is an origin-bound keypair — the key is created for `example.com` and the browser will not offer it to `examp1e.com`, because the origin is part of what gets signed rather than something the user is asked to eyeball. That binding is what makes it phishing-resistant in a way no shared secret is: a one-time code from an authenticator app is equally valid on the real site and on a proxy of it, and a code sent over SMS is valid for whoever currently controls the number, which is the whole premise of a [SIM swap](/wiki/economics/finance/fraud/sim-swap).

Two limits are worth holding onto. The key authenticates a login; it does not review what happens after one, so it does nothing about a session the attacker already holds. And enrolling a single key makes loss of the device a lockout, so accounts that support it should carry two enrolled keys rather than a key plus an SMS fallback — a fallback is a second, weaker door into the same account.

## External references

- [Yubico](https://www.yubico.com/) and the [YubiKey OpenPGP documentation](https://developers.yubico.com/PGP/)
- [drduh/YubiKey-Guide](https://github.com/drduh/YubiKey-Guide) -- the widely-followed walkthrough for generating and moving GPG keys to a YubiKey
- [ykman (YubiKey Manager) CLI](https://docs.yubico.com/software/yubikey/tools/ykman/) -- for setting touch policies and managing applets
- [W3C Web Authentication](https://www.w3.org/TR/webauthn-2/) -- the specification, including the origin-binding rules
- [usbipd-win](https://github.com/dorssel/usbipd-win) -- forwarding a USB YubiKey into WSL2, which has no native USB support
