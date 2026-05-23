---
title: "YubiKey"
weight: 30
---

A **YubiKey** is a small USB (and NFC) hardware authenticator made by Yubico. Among several applets it implements an **OpenPGP smartcard**, which can hold [GPG](/wiki/security/gpg) private keys on the device itself. Once a key is moved onto the card, the private material never exists on disk and never leaves the hardware -- cryptographic operations happen *on* the YubiKey, and the host only sends in ciphertext and gets back plaintext.

This makes it the natural hardening step for a [`pass`](/wiki/security/pass) store: the GPG key that can decrypt every secret stops being a file an attacker can copy and becomes a physical object you hold. With a touch policy enabled, each decryption also requires a deliberate tap, so malware cannot silently drain the store even while the key is plugged in.

## External references

- [Yubico](https://www.yubico.com/) and the [YubiKey OpenPGP documentation](https://developers.yubico.com/PGP/)
- [drduh/YubiKey-Guide](https://github.com/drduh/YubiKey-Guide) -- the widely-followed walkthrough for generating and moving GPG keys to a YubiKey
- [ykman (YubiKey Manager) CLI](https://docs.yubico.com/software/yubikey/tools/ykman/) -- for setting touch policies and managing applets
- [usbipd-win](https://github.com/dorssel/usbipd-win) -- forwarding a USB YubiKey into WSL2, which has no native USB support
