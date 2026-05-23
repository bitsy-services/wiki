---
title: "GPG (GnuPG)"
weight: 20
---

**GnuPG** (GPG) is the free, complete implementation of the OpenPGP standard. It provides public-key encryption and digital signatures from the command line, and it is the encryption engine underneath [`pass`](/wiki/security/pass): every secret in a password store is an individual file encrypted to your GPG public key, decryptable only with the matching private key.

The model is asymmetric. A **key pair** has a public half (used to encrypt *to* you, safe to share) and a private half (used to decrypt, guarded by a passphrase and never shared). A modern GPG identity is usually a primary key plus subkeys for signing, encryption, and authentication -- which is what lets the private key be moved onto hardware like a [YubiKey](/wiki/security/yubikey) one subkey at a time.

## External references

- [GnuPG official site](https://gnupg.org/) and [the GnuPG manual](https://gnupg.org/documentation/manuals/gnupg/)
- [RFC 9580 -- OpenPGP](https://www.rfc-editor.org/rfc/rfc9580) (the current standard)
- [Arch Wiki: GnuPG](https://wiki.archlinux.org/title/GnuPG) -- thorough, distro-agnostic setup notes
- [riseup.net OpenPGP best practices](https://riseup.net/en/security/message-security/openpgp/best-practices)
