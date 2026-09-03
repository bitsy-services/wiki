---
title: "Building and Deploying"
weight: 80
---

`hugo` writes the finished site into `public/` and stops. There is no deploy step in Hugo, and no server component to install: the artefact is a directory of files, and every host that can serve a directory of files can serve it. Deployment is therefore a copy, and the hosting bill is bandwidth.

```bash
hugo                          # build into public/
hugo --minify                 # minify HTML, XML, CSS, JS on the way out
hugo --gc                     # prune unreferenced cache entries afterwards
hugo --cleanDestinationDir    # delete output files no longer generated
hugo -d dist                  # write somewhere other than public/
```

`--cleanDestinationDir` matters after a rename. Hugo writes what the content produces and leaves everything else alone, so a page moved from `/wiki/old/` to `/wiki/new/` leaves the old directory sitting in `public/` and, on a host that syncs rather than replaces, sitting in production. `public/` is safe to delete before any build for the same reason.

## `baseURL` is not cosmetic

Most links in a Hugo site are relative and work regardless of configuration. The ones that cannot be relative all read `baseURL`: the sitemap, the RSS feed, `<link rel="canonical">`, Open Graph and Twitter card image URLs, and anything a template builds with `.Permalink` rather than `.RelPermalink`.

```toml
baseURL = 'https://wiki.bitsy.services/'
```

Get it wrong and the site looks correct in a browser while the sitemap advertises `https://example.org/`, the feed's entries point at a domain you do not own, and social cards fetch an image from nowhere. Nothing in the build objects, because every one of those values is exactly what was configured. `hugo -b https://staging.example.net/` overrides it for a one-off build.

## Environments

Hugo has a build environment, defaulting to `production` for `hugo` and `development` for `hugo server`. Configuration can be split by environment in a `config/` directory:

```text
config/
├── _default/
│   └── hugo.toml     applies to every environment
├── development/
│   └── hugo.toml     merged over _default for `hugo server`
└── production/
    └── hugo.toml     merged over _default for `hugo`
```

Templates read the same value through `hugo.Environment` and `hugo.IsProduction`, which is the hook for suppressing analytics and third-party embeds locally, or for emitting `<meta name="robots" content="noindex">` on a staging build. `hugo -e staging` selects an arbitrary environment name, and `config/staging/` supplies its overrides.

## Pinning the binary

Hugo is a single binary with no lockfile, so nothing in a checkout says which version it was written against. The template system was reorganized in v0.146 and the `gist` and `twitter` [shortcodes](/wiki/hugo/shortcodes) were removed in v0.156, so a version gap shows up as a build that fails on the deploy machine and not on the author's.

The `hugo-bin` npm package downloads a Hugo into `node_modules`, and `npx hugo` runs that one rather than whatever is on the path:

```json
{
  "devDependencies": { "hugo-bin": "^0.149.2" },
  "hugo-bin": { "buildTags": "extended" }
}
```

`buildTags: extended` is required wherever the theme's stylesheets are Sass. Continuous integration is usually pinned separately — this repository's workflow names `hugo-version: '0.159.0'` with `extended: true`.

Having two pins is not the same as having them agree. In this repository `npx hugo` reports 0.152.2 and the workflow builds with 0.159.0, and `hugo-bin` 0.149.2 is the package version that installs the first of those, so the number written in `package.json` is not a Hugo version at all. A caret range moves on the package's schedule, a workflow pin does not reach a contributor's editor, and the version that decides whether the site builds is the one on the machine that deploys. An exact `hugo-bin` version, matched by the version named in the workflow, is what makes the three agree.

## Deploying

The upload is host-specific and the build is not. This wiki targets Cloudflare Workers static assets, configured in `wrangler.jsonc`:

```json
{
  "name": "wiki",
  "build": { "command": "npx hugo" },
  "assets": { "directory": "public" }
}
```

```json
{
  "scripts": {
    "build": "hugo",
    "deploy": "npx hugo && wrangler deploy",
    "preview": "npx hugo && wrangler dev"
  }
}
```

Three details generalize to any static host.

**The 404 page.** Hugo generates `public/404.html` from `layouts/404.html`, and a host that answers misses with its own generic page never shows it. On Cloudflare's static assets the key is `not_found_handling: "404-page"`; other hosts have an equivalent, and some read `404.html` by convention. The snippet above does not set it, which is what an unnoticed default looks like: the file is built on every deploy and served to nobody.

**Cache headers, split two ways.** [Fingerprinted assets](/wiki/hugo/hugo-pipes#fingerprinting-and-cache-policy) take a long `max-age`; the HTML that names them must not. One policy for both is either a stale site or a slow one.

**Build on the host or build locally.** A host that runs `hugo` itself needs the theme's git submodule (`--recurse-submodules`, or an explicit `git submodule update --init`) and a pinned Hugo version, and gives you deploys triggered by a push. Building locally and uploading `public/` needs neither, and makes the deploy exactly as reproducible as the machine that ran it. Either way, run the site's gate first: `scripts/check.sh` here, which builds the site and then checks every [internal link](/wiki/hugo/internal-links), because a push that deploys is a push that publishes the 404s with it.

## External references

- [Hugo: Hosting and deployment](https://gohugo.io/host-and-deploy/)
- [Hugo: Configure Hugo](https://gohugo.io/configuration/)
- [Cloudflare: Static assets on Workers](https://developers.cloudflare.com/workers/static-assets/)
- [hugo-bin](https://www.npmjs.com/package/hugo-bin) — the npm wrapper that pins the binary
