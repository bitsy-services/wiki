---
title: "Template Lookup"
weight: 20
---

Every page Hugo renders is matched against an ordered list of candidate template paths, and the first one that exists wins. The list is generated from the page itself — its kind, its type, its section, its output format, its language, and any `layout` in its front matter — so nothing declares which template a page uses. The page's attributes and the set of files on disk decide it between them.

## The files

Templates live in `layouts/`, in the project and in every theme. Hugo v0.146 reorganized the directory, and material written before March 2025 describes a tree that no longer matches what a current theme ships:

| Old location | Current location |
| --- | --- |
| `layouts/_default/single.html` | `layouts/single.html` |
| `layouts/_default/baseof.html` | `layouts/baseof.html` |
| `layouts/index.html` | `layouts/home.html` |
| `layouts/partials/` | `layouts/_partials/` |
| `layouts/shortcodes/` | `layouts/_shortcodes/` |
| `layouts/_default/_markup/` | `layouts/_markup/` |

The old paths still resolve, which is why a mixed tree builds without complaint and why the two conventions coexist in tutorials. The underscore prefix now marks the directories Hugo treats specially rather than as page types, and `_default` is gone because the root of `layouts/` is the default.

## The order

Hugo walks from most specific to least. For a regular page in the `docs` section, rendering as HTML, the candidates run roughly:

```text
layouts/docs/page.html          section, page kind
layouts/docs/single.html        section
layouts/page.html               page kind
layouts/single.html             default
```

[Front matter](/wiki/hugo/content-organization#front-matter) widens the list at the top. `layout: wide` inserts `layouts/docs/wide.html` and `layouts/wide.html` ahead of everything above; `type: manual` substitutes `manual` for `docs`, and both cascade, so one block on a section index can redirect every page under it to a different template. Output formats and languages add their own candidates, which is how one page renders to HTML and JSON from two different files.

## The theme is interleaved, not underneath

The mental model that breaks builds is layering: project templates on top, theme templates beneath, project always wins. Hugo does not work that way. It builds one candidate list and checks the project and every theme at each position, so **a theme's more specific template beats the project's less specific one**.

Give a theme `layouts/docs/single.html` and a project `layouts/single.html`, and pages in the `docs` section render through the theme's file. Adding `layouts/docs/single.html` to the project — matching the theme's path exactly — takes it back. The rule for [overriding a theme template](/wiki/hugo/themes-and-modules#overriding-means-matching-a-path) is therefore mechanical: find the theme file, and put your file at the identical path under your own `layouts/`. This wiki overrides `layouts/_partials/docs/html-head-favicon.html` by copying that path verbatim out of the theme.

The corollary is that a theme can quietly capture pages you thought you controlled. A theme shipping `layouts/posts/single.html` owns everything in a `posts` section no matter what sits at your project root.

## Base templates and blocks

`baseof.html` is the outer shell: the `<html>` element, the head, the chrome, and a set of `{{ block }}` placeholders that the page template fills.

```go-html-template
{{/* layouts/baseof.html */}}
<html>
  <head>{{ partial "head.html" . }}</head>
  <body>{{ block "main" . }}{{ end }}</body>
</html>
```

```go-html-template
{{/* layouts/single.html */}}
{{ define "main" }}
  <h1>{{ .Title }}</h1>
  {{ .Content }}
{{ end }}
```

The base template is applied only when the page template contains `{{ define }}` blocks. A `single.html` consisting of a bare `{{ .Content }}` renders on its own — no `<html>` element, no head, no chrome — and the failure looks like a broken base template rather than a template that was never consulted. `baseof.html` follows the same lookup rules as everything else, so a section can have its own.

## Partials

A partial is a template called for its output, from a path under `layouts/_partials/`:

```go-html-template
{{ partial "docs/footer.html" . }}
{{ partialCached "docs/menu.html" . .Section }}
```

The second argument is the context the partial receives. Inside a `range`, the dot is the item being ranged over rather than the page, so `{{ partial "x.html" . }}` in that position hands the partial a list element where it expected a page, and the partial's `.Title` resolves to nothing.

`partialCached` caches the rendered result. The trailing arguments form the cache key, so `partialCached "docs/menu.html" . .Section` renders the menu once per section rather than once per page. Omitting the key caches one result for the whole site, which is correct for a genuinely invariant partial and wrong the moment the partial reads anything off the page.

## Check yourself

Two flags answer the questions that lookup order raises:

```bash
hugo --printUnusedTemplates    # templates on disk that never rendered anything
hugo --templateMetrics --templateMetricsHints
```

`--printUnusedTemplates` catches the override that did not take: a file written to shadow a theme template, sitting one path segment off, rendering nothing. `--templateMetrics` reports execution counts and cumulative duration per template, which is how a partial that should have been a `partialCached` shows up.

## External references

- [Hugo: Template lookup order](https://gohugo.io/templates/lookup-order/)
- [Hugo v0.146.0 template system overview](https://gohugo.io/templates/new-templatesystem-overview/)
- [Hugo: Base templates and blocks](https://gohugo.io/templates/base/)
- [Go `html/template`](https://pkg.go.dev/html/template) — the engine underneath, including its contextual escaping
