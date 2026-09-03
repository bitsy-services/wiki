---
title: "Hugo Pipes"
weight: 60
---

Hugo Pipes is the asset pipeline: files under `assets/` are fetched as resource objects, passed through transformations, and published under a name the pipeline chooses. Nothing here is a separate build step or a watch process. It is a chain of template functions evaluated while the page that references the asset is rendered.

```go-html-template
{{ $css := resources.Get "css/main.scss" | css.Sass | minify | fingerprint }}
<link rel="stylesheet" href="{{ $css.RelPermalink }}" integrity="{{ $css.Data.Integrity }}">
```

That produces:

```html
<link rel="stylesheet"
      href="/css/main.min.ce323643df844223c686fbca413cedc8c01bb90845c8224e83a37497388d84ac.css"
      integrity="sha256-zjI2Q9+EQiPGhvvKQTztyMAbuQhFyCJOg6N0lziNhKw=">
```

The Sass was transpiled, the result minified, and the published filename given a SHA-256 digest of the contents. `fingerprint` also fills `.Data.Integrity` with the same digest in the format the `integrity` attribute wants — subresource integrity (SRI), which makes the browser refuse a stylesheet that does not hash to the expected value.

## Fingerprinting and cache policy

A filename containing a hash of the contents cannot go stale. Change one declaration in the Sass and the published name changes, so the browser requests a URL it has never seen and the old cached copy is irrelevant rather than wrong. That in turn makes an aggressive cache policy safe: a fingerprinted asset can be served with a year-long `max-age`, because a new version arrives under a new name rather than by expiry.

The HTML that references it must not be cached that way. It is the only file whose URL is stable, so it is the only file that has to be re-fetched for a [deploy](/wiki/hugo/deploying) to take effect.

## `assets/` and `static/`

Both of [the two directories](/wiki/hugo#the-directory-contract) end up serving files, and they are not interchangeable.

| | `static/` | `assets/` |
| --- | --- | --- |
| Reaches the output | always, on every build | only if a template publishes it |
| Filename | unchanged | whatever the pipeline produces |
| Transformations | none | the full pipeline |
| Referenced as | a literal path | `.RelPermalink` on a resource |

The asymmetry in the first row catches people. A resource that is fetched and transformed but whose `.RelPermalink` or `.Permalink` is never evaluated is not written to `public/` at all — Hugo publishes on reference, so an asset assigned to a variable and then unused simply does not exist in the build.

`static/` is the right home for files whose exact path is part of a contract with something outside the site. This wiki keeps `ads.txt` and its favicons there: `ads.txt` has to answer at the site root under that name, and a fingerprinted `favicon.a1b2c3.png` would not be found by anything looking for `/favicon.ico`.

## The transformations

**Stylesheets.** `css.Sass` transpiles Sass and SCSS. The default transpiler is the LibSass implementation compiled into the extended Hugo binary; `css.Sass (dict "transpiler" "dartsass")` switches to Dart Sass, which has to be installed separately as a `sass` executable on the path. `css.PostCSS` runs the project's PostCSS configuration, and `css.TailwindCSS` runs the Tailwind compiler; both shell out to tools installed through npm.

**Scripts.** `js.Build` bundles with esbuild — imports resolved, tree shaking, a target syntax level, optional source maps — in-process, with no separate bundler configuration file.

**Everything.** `minify` picks a minifier from the media type. `fingerprint` hashes and renames. `resources.Concat` joins several resources into one, which is how a set of partial stylesheets becomes a single request. `resources.FromString` synthesises a resource from generated content, so a template can build a file and put it through the same pipeline.

**Images.** `.Resize`, `.Fit`, `.Fill`, `.Crop`, and `.Filter` operate on image resources — a page bundle's own images included — with the results cached in `resources/_gen/`. Committing that directory trades repository size for build time: the output is deterministic, and a build machine without it re-encodes every image on the first build.

**Remote files.** `resources.GetRemote` fetches a URL and returns a resource, cached between builds. It puts a network dependency in the middle of a build, which is a reasonable trade for a font or an icon set and a bad one for anything that might rate-limit.

## Errors and caching

A transformation failure is a build failure with the offending file named — a Sass syntax error stops the build rather than shipping an empty stylesheet.

`resources.GetRemote` splits its failures across two channels, and only one of them is loud. A transport failure — refused connection, bad certificate, name that does not resolve — throws from inside the function and stops the build. An HTTP error status does not: a 404 returns a nil resource, leaves `.Err` unset, and logs nothing. The commonly copied guard handles neither case well, because `with` on a nil resource simply skips the block and the page ships with no stylesheet link and no complaint. The `else` branch is the part that matters:

```go-html-template
{{ $url := "https://example.org/fonts.css" }}
{{ with resources.GetRemote $url }}
  {{ with .Err }}
    {{ errorf "%s" . }}
  {{ else }}
    <link rel="stylesheet" href="{{ .RelPermalink }}">
  {{ end }}
{{ else }}
  {{ errorf "unable to fetch %s" $url }}
{{ end }}
```

Transformation results are cached in `resources/_gen/` and in the Hugo cache directory, keyed by the inputs, so an unchanged stylesheet is not re-transpiled on every build. `hugo --gc` prunes cache entries no longer referenced, and `hugo --ignoreCache` forces the work to be redone when a cached result is suspected of being stale.

## External references

- [Hugo: Resources](https://gohugo.io/functions/resources/)
- [Hugo: Images](https://gohugo.io/content-management/image-processing/)
- [esbuild](https://esbuild.github.io/) — the bundler behind `js.Build`
- [MDN: Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)
