---
title: "Hugo"
weight: 24
bookCollapseSection: true
---

Hugo is a static site generator (SSG): it reads a directory of Markdown files and Go templates and writes a directory of finished HTML. Nothing executes when a reader arrives. The server hands out files assembled minutes or months earlier, so a traffic spike costs bandwidth rather than compute, and the only code exposed to the public is whatever serves the bytes. Hugo itself is a single statically linked Go binary with no interpreter, package manager, or database behind it.

This wiki is a Hugo site: 298 pages, rebuilt from empty in 1.9 seconds of wall time and 10 seconds of processor time on a twelve-core laptop. The gap between those two numbers is Hugo rendering pages on several cores at once. `hugo server` narrows the loop further by rebuilding only the pages a saved file affects and pushing the result into the open browser over a websocket.

Two binaries carry the name. The standard build does everything described in this section except Sass; the **extended** build adds Sass transpilation and WebP encoding, and announces itself as `+extended` in `hugo version`. The distinction bites when a theme's stylesheet is written in Sass and the standard binary reports a missing transpiler. This repository pins the extended build through the `hugo-bin` npm package, so the binary a contributor runs is the binary the deploy runs.

## The directory contract

A Hugo project is a fixed set of directories, each with one job. `hugo new site` creates the input ones empty.

```text
hugo.toml      site configuration (hugo.yaml and hugo.json also work)
content/       Markdown files; this tree becomes the URL structure
layouts/       Go templates
assets/        files for the build pipeline — transpiled, minified, fingerprinted
static/        files copied into the output byte for byte, unprocessed
data/          structured data the templates can read
i18n/          translation tables
archetypes/    front matter templates for new content files
themes/        vendored themes, each carrying its own copy of the above
public/        the build output — written, not read; safe to delete at any time
```

`assets/` and `static/` are the pair most often confused. A file in `static/favicon.png` lands at `/favicon.png` with its bytes and its name untouched. A file in `assets/` does not appear in the output at all until a template asks for it, and its published name usually carries a content hash — the difference is spelled out in [Hugo Pipes](/wiki/hugo/hugo-pipes).

Themes are not a separate mechanism. A theme is another project directory with the same layout, merged underneath yours, which is why overriding a theme file means [placing a file at the same path](/wiki/hugo/themes-and-modules) and nothing else.

## What Hugo checks, and what it does not

Hugo fails a build on a template that will not parse, a shortcode that does not exist, and front matter it cannot decode. Those are compile errors in the ordinary sense and they arrive with a file and line number.

It does not check that `/wiki/does-not-exist` resolves to a page. A Markdown link to a path is copied into the HTML verbatim, the build exits zero, and the 404 appears in production. Warnings do not fail the build either — `hugo` exits 0 having printed them — so a gate that shells out to `hugo` and tests the exit status is weaker than it looks. [Internal links](/wiki/hugo/internal-links) covers the two ways out: the `ref` shortcode, which does resolve at build time, and an external checker over the rendered page set, which is what this wiki runs.

## In this section

[Content organization](/wiki/hugo/content-organization) is where the URL structure comes from, and where one character decides a directory's shape: `_index.md` makes it a section with children, `index.md` makes it one page with attached files.

[Template lookup](/wiki/hugo/template-lookup) explains which of the files in `layouts/` renders a given page. The rule is specificity, not layering, and a project template does not automatically beat a theme's.

[Themes and modules](/wiki/hugo/themes-and-modules) covers vendoring a theme as a git submodule or a Hugo Module, and what "overriding" a theme actually means once the union filesystem is understood.

[Shortcodes](/wiki/hugo/shortcodes) are templates callable from inside Markdown, with two delimiter forms that differ in whether the output is fed back through the Markdown renderer.

[Render hooks](/wiki/hugo/render-hooks) replace Goldmark's output for a whole class of Markdown construct — every link, every image, every fenced block — without touching the content.

[Hugo Pipes](/wiki/hugo/hugo-pipes) is the asset pipeline: `resources.Get`, then transpile, bundle, minify, and fingerprint, with the published filename carrying a hash of the contents.

[Internal links](/wiki/hugo/internal-links) is the gap above, in detail.

[Building and deploying](/wiki/hugo/deploying) covers `baseURL`, build environments, and what shipping a directory of files to a static host looks like in practice.

## Wiki Pages

{{< section >}}

## External references

- [Hugo documentation](https://gohugo.io/documentation/)
- [Hugo source](https://github.com/gohugoio/hugo) — the Go implementation
- [Goldmark](https://github.com/yuin/goldmark) — the CommonMark parser Hugo renders Markdown with
