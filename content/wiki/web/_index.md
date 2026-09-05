---
title: "Web"
weight: 24
bookCollapseSection: true
---

How a document gets from a repository to a browser. The tools that build a site, the formats it travels in, and the machinery that serves it — a page that renders, a URL that resolves, a cache that expires at the right time.

The section takes the publishing side of the web rather than the application side. Its first subsection is the one this wiki is made of: [Hugo](/wiki/web/hugo), the static site generator, across nine pages covering where URLs come from, which template renders a given page, the [asset pipeline](/wiki/web/hugo/hugo-pipes), and the [internal-link checking Hugo does not do](/wiki/web/hugo/internal-links).

## Where the boundaries fall

Three neighbouring sections hold material a reader might expect to find here, and the split is deliberate in each case.

The durable ideas underneath the wire live in [Computer Science](/wiki/cs): [content addressing](/wiki/cs/ipfs) rather than the servers that implement it, [canonicalization](/wiki/cs/canonicalization-attack) rather than the parsers that get it wrong, [entity addressing](/wiki/cs/entity-addressing) rather than the URL scheme it argues about. A concept that would still be true if the web were replaced tomorrow belongs there.

Keys, certificates, and credentials on the machine doing the publishing are in [Security](/wiki/security), which is about handling secrets rather than about what they authorise.

[Git](/wiki/git) is the step before this one: it gets content into the repository that a build then turns into a site.

## Wiki Pages

{{< section >}}
