---
title: "Canonicalization Attack"
weight: 10
---

A canonicalization attack exploits inconsistencies in how systems normalize data into a standard ("canonical") form. When two components in a pipeline disagree on what a given input *means* -- because they canonicalize it differently, or one canonicalizes and the other doesn't -- an attacker can craft input that passes validation in one form but behaves maliciously in another.

## What is canonicalization?

Canonicalization (sometimes abbreviated C14N) is the process of converting data that has more than one valid representation into a single, standard form:

- **File paths**: `/var/www/../www/index.html` and `/var/www/index.html` refer to the same file.
- **URLs**: `https://example.com/%2e%2e/admin` and `https://example.com/../admin` encode the same traversal.
- **Unicode**: the character "é" can be a single code point (U+00E9) or a base letter plus a combining accent (U+0065 U+0301).
- **XML**: attribute ordering, whitespace handling, and namespace declarations can all vary without changing the document's logical content.

Canonicalization is necessary for correctness -- digital signatures, caching, deduplication, and access control all depend on it. The vulnerability arises when canonicalization is *inconsistent* across components, or when validation happens before canonicalization rather than after.

## Attack patterns

### Path traversal

A web server blocks requests to `/etc/passwd`, but an attacker submits `/var/www/../../etc/passwd`. If the access-control check runs before path canonicalization, the blocklist never matches, and the canonicalized path reaches the filesystem.

### Double encoding

URL-encoding `../` produces `%2e%2e%2f`. If a filter decodes once and checks the result, but the downstream component decodes a second time, the attacker can double-encode: `%252e%252e%252f`. The filter sees the literal string `%2e%2e%2f` (harmless), while the backend decodes it to `../`.

### Unicode normalization

Some systems normalize Unicode to one of its standard normalization forms (NFC, NFKC) before comparison. An attacker might register a username using a visually identical but canonically different character sequence -- for example, using a Cyrillic "а" (U+0430) where Latin "a" (U+0061) is expected. If the authentication system normalizes but the registration system does not (or vice versa), the attacker can impersonate another user.

### XML structure manipulation

[XML digital signatures](/wiki/cs/canonicalization-attacks-on-signed-xml) are particularly susceptible. The signature covers a canonicalized view of the document, but the application may process a different logical view -- allowing an attacker to inject or relocate elements without invalidating the signature.

## The validate-before-canonicalize problem

The most common root cause is performing security checks on raw input and then canonicalizing afterward. MITRE catalogues this as [CWE-180](https://cwe.mitre.org/data/definitions/180.html) ("Incorrect Behavior Order: Validate Before Canonicalize"). The related [CWE-179](https://cwe.mitre.org/data/definitions/179.html) covers the broader category of premature validation.

The fix is to **canonicalize first, then validate the canonical form**, which in practice requires knowing every canonicalization step in the pipeline and ensuring no later component re-interprets the data.

## Mitigations

1. **Canonicalize before validation.** Apply all normalization steps (URL decoding, Unicode normalization, path resolution) before running security checks.
2. **Reject ambiguous input.** Rather than trying to normalize everything, refuse input that contains encoding tricks -- double-encoded characters, overlong UTF-8 sequences, or path traversal sequences.
3. **Use allowlists over blocklists.** A blocklist that tries to enumerate dangerous patterns will always miss edge cases. An allowlist that specifies exactly what valid input looks like is more robust.
4. **Ensure pipeline consistency.** Every component that touches the data should agree on its canonical form. Audit the full path from input to processing.
5. **Leverage established libraries.** For example, the Open Worldwide Application Security Project's ESAPI (Enterprise Security API) library provides canonicalization utilities designed to handle multi-layer encoding ([CWE-88](https://cwe.mitre.org/data/definitions/88.html) discusses this in the context of argument delimiters).

## Further reading

- [CWE-180: Incorrect Behavior Order: Validate Before Canonicalize](https://cwe.mitre.org/data/definitions/180.html)
- [CWE-179: Incorrect Behavior Order: Early Validation](https://cwe.mitre.org/data/definitions/179.html)
- [Canonicalization Attacks on Signed XML Documents](/wiki/cs/canonicalization-attacks-on-signed-xml) -- a companion page covering XML Signature Wrapping and related attacks
