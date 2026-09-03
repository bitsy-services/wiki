---
title: "Internal Links"
weight: 70
---

Hugo does not validate internal links. A Markdown link to a page that does not exist is copied into the HTML exactly as written, the build succeeds, and the exit status is zero:

```text
[dead](/docs/guide/nope)
```

```html
<a href="/docs/guide/nope">dead</a>
```

No warning is logged. Forcing on the [embedded link render hook](/wiki/hugo/render-hooks) does not change the outcome — it resolves destinations it recognizes and passes the rest through untouched, so `[q](nope.md)` also ships as `href="nope.md"`. Resolution and validation are different jobs, and Hugo only does the first.

The practical consequence is that renaming a page is the most dangerous edit in a Hugo site. Every inbound link becomes a 404 that no build will mention, and the first report comes from a reader or from a crawler weeks later.

## What `ref` does differently

The `ref` and `relref` shortcodes, and the `ref` and `relref` template functions, resolve a page reference against the site's page collection and fail when it does not resolve:

```text
[beta]({{</* ref "/docs/guide/beta" */>}})
```

```text
ERROR [en] REF_NOT_FOUND: Ref "/docs/guide/nope":
  "content/docs/guide/alpha.md:4:7": page not found
```

The build exits 1. `refLinksErrorLevel` controls the severity and defaults to `ERROR`, so this is the behaviour without any configuration. Two knobs soften it:

```toml
refLinksErrorLevel = 'WARNING'      # log and continue; exit status stays 0
refLinksNotFoundURL = '/404.html'   # what to emit in place of the dead target
```

With both set, the example above logs a warning and renders `<a href="/404.html">`. That is the right setting for a site importing content it does not control, and the wrong one for a site that wants a gate, since a warning does not fail a build.

The cost of `ref` is paid in the content files. A page full of `{{</* ref */>}}` calls is no longer portable Markdown — it does not render correctly in an editor preview, on a code-hosting site, or through any other renderer — and the shortcode noise sits in the middle of every sentence that carries a link.

## The other route: check the output

The alternative is to write ordinary Markdown links and validate them separately, after the page set is known. That is what this wiki does. `scripts/check-content.py` builds the map of every URL Hugo will serve, walks every internal link written in every content file, and reports any target that is not in the map. It has caught six dead links so far, all of them from renames.

The same pass checks fragments, which is the half that is easy to forget. A link to `/wiki/ai/agentic-workflows#tool-design` is a 404 in the only sense that matters — the reader lands somewhere and the page does not move — while being a perfectly valid URL that no link checker looking at HTTP status codes will flag.

Checking fragments means reproducing Hugo's anchor generation. `markup.goldmark.parser.autoHeadingID` generates heading IDs and `autoIDType` selects the algorithm, defaulting to `github`:

| Heading | `id` |
| --- | --- |
| `## Tool design — the ACI` | `tool-design--the-aci` |
| `## A/B testing & more` | `ab-testing--more` |

Punctuation is dropped, letters are lowercased, and each remaining whitespace character becomes its own dash. Runs are not collapsed, so a heading with an em dash surrounded by spaces produces two consecutive dashes where the dash used to be. Duplicate headings on one page get `-1`, `-2` suffixes.

## Why the build's exit status is not enough

`hugo` exits 0 having printed its warnings. A gate that runs `hugo` and tests the exit status therefore passes on a build that logged a deprecated template call, a missing translation, and a `refLinksErrorLevel = 'WARNING'` reference to a page that is gone.

Two ways to close that:

```bash
hugo --panicOnWarning     # first WARNING becomes a fatal error
hugo --printPathWarnings  # warn when two pages want the same output path
```

`--panicOnWarning` is blunt: it fails on a theme's deprecation notices as readily as on a broken reference, which on a vendored theme means it fails until the theme is updated. A separate checker over the content, wired into the same gate, distinguishes the two.

## Check yourself

```bash
scripts/check.sh
```

In this repository that is one command: `hugo` builds the site, then `scripts/check-content.py` resolves every internal link and every fragment against the rendered page set, and a `Stop` hook runs it whether or not anyone remembers to. A red result blocks the change rather than annotating it.

The design worth copying is not the specific script. It is that the check runs on the *page set produced by the build*, not on the content tree as written — a link is correct when Hugo will serve its target, and only the build knows what Hugo will serve.

## External references

- [Hugo: Links and cross references](https://gohugo.io/content-management/cross-references/)
- [Hugo: Configure Hugo — refLinksErrorLevel](https://gohugo.io/configuration/all/)
- [Hugo: `ref` and `relref` functions](https://gohugo.io/functions/urls/ref/)
