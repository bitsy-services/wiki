---
title: "Canonicalization Attacks on Signed XML"
weight: 11
---

XML digital signatures bind a cryptographic signature to a canonicalized representation of an XML document (or a portion of it). This creates a gap that attackers can exploit: the signature covers what the canonicalization algorithm *sees*, but the application processes what the XML parser *produces*. When those two views diverge, an attacker can modify the document's effective meaning without invalidating its signature.

This page focuses on XML-specific attacks. For the general concept, see [Canonicalization Attack](/wiki/cs/canonicalization-attack).

## How XML signatures work

The [XML Signature](https://www.w3.org/TR/xmldsig-core/) specification (W3C) defines a process:

1. **Reference resolution** -- identify the signed content via URI references.
2. **Canonicalization** -- transform the referenced XML into a canonical byte stream using an algorithm like [Canonical XML (C14N)](https://www.w3.org/TR/xml-c14n/) or [Exclusive Canonical XML (Exc-C14N)](https://www.w3.org/TR/xml-exc-c14n/).
3. **Digest** -- hash the canonical form.
4. **Signature** -- sign the digest (along with the `SignedInfo` element, which is itself canonicalized).

The attack surface lies in step 1 and 2: if the attacker can manipulate the document so that the canonicalized, signed content remains unchanged while the *application-visible* content differs, the signature verifies but the application acts on attacker-controlled data.

## XML Signature Wrapping (XSW)

XSW is the most well-known class of attack against XML signatures. The core idea: move the signed element to a location the application ignores, and place a forged element where the application expects to find it.

### Mechanism

An XML signature typically references a signed element by its `Id` attribute. The attacker:

1. Copies the original signed element (with its `Id`) to a different location in the document tree -- for example, inside a wrapper element that the application skips.
2. Creates a new element with the same structure but attacker-controlled content, and places it where the application looks for it.
3. The signature verification resolves the `Id` reference, finds the original (relocated) element, canonicalizes it, and confirms the signature is valid.
4. The application, using a different lookup strategy (e.g., XPath position rather than `Id`), processes the forged element.

### Variants

Researchers have catalogued numerous XSW variants depending on where the original element is relocated (sibling, child, ancestor of the `Signature` element) and how the forged element is positioned. The taxonomy from Somorovsky et al. (2012) identifies at least eight distinct attack patterns against SAML (Security Assertion Markup Language) single sign-on systems.

## C14N pitfalls

Even without XSW, the canonicalization algorithm itself can introduce issues:

- **Inclusive vs. exclusive canonicalization.** Inclusive C14N (the default) inherits namespace declarations from ancestor elements into the canonical form. If the document is restructured, those inherited namespaces change, which can either break legitimate signatures or -- in some implementations -- be exploited to create ambiguity. Exclusive C14N ([Exc-C14N](https://www.w3.org/TR/xml-exc-c14n/)) was designed to address this by only including namespaces that are visibly used.
- **Comment handling.** The `WithComments` variants of C14N preserve XML comments; the default variants strip them. If a signature uses the non-comment variant but the application processes comments, an attacker can inject content via comments.
- **Whitespace normalization.** C14N normalizes attribute values and line endings but preserves most element content whitespace. Subtle differences in whitespace handling between the canonicalizer and the application can create divergent interpretations.

## Namespace manipulation

XML namespaces add another layer of complexity:

- An attacker can redefine a namespace prefix to point to a different URI, changing the semantic meaning of elements without altering their local names.
- Namespace declarations on ancestor elements can shadow or override those on descendant elements, and different C14N algorithms handle this differently.
- When combined with XSW, namespace manipulation can make forged elements appear to belong to the expected namespace while the signed originals are pushed into an inert one.

## Mitigations

1. **Use Exclusive Canonicalization (Exc-C14N).** It limits the scope of inherited namespace context and reduces the attack surface for restructuring attacks.
2. **Enforce strict schema validation.** Validate the XML document against a rigid schema *after* signature verification. Reject documents with unexpected elements, duplicated `Id` attributes, or structural anomalies.
3. **Bind reference resolution to application processing.** Ensure the same element the signature verified is the same element the application acts on. Use the signature's reference URI to locate the element for both purposes.
4. **Limit XML features.** Disable DTD processing, external entity resolution, and XInclude. These expand the attack surface beyond canonicalization.
5. **Consider alternatives to XML Signature.** For new systems, JSON Web Signatures (JWS) or simpler signing schemes avoid much of the XML complexity. For SAML, use libraries that are hardened against known XSW variants.

## References

- [XML Signature Syntax and Processing (W3C)](https://www.w3.org/TR/xmldsig-core/)
- [Exclusive XML Canonicalization (W3C)](https://www.w3.org/TR/xml-exc-c14n/)
- [Canonical XML Version 1.0 (W3C)](https://www.w3.org/TR/xml-c14n/)
- Somorovsky, J. et al. "On Breaking SAML: Be Whoever You Want to Be" (USENIX Security 2012)
