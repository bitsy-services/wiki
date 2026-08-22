# Bitsy Services Wiki

Internal wiki built with [Hugo](https://gohugo.io/) and the
[Hugo Book](https://github.com/alex-shpak/hugo-book) theme, deployed to
Cloudflare Pages at [wiki.bitsy.services](https://wiki.bitsy.services/).

## Local development

```sh
git submodule update --init --recursive   # the theme is a submodule
hugo server -D
```

## Adding content

Pages live under `content/wiki/<section>/`, and the URL mirrors the path:
`content/wiki/economics/finance/defi/amm.md` serves at
`/wiki/economics/finance/defi/amm`.

```markdown
---
title: "Automated Market Maker"
weight: 20
---

## What it is

...
```

`weight` orders the sidebar within a directory. Don't put an `# H1` in the body —
`layouts/single.html` renders the frontmatter `title` as the page's h1.

The conventions are written down in [`.claude/rules/`](.claude/rules/) — audience,
linking, page structure, and Solidity examples. They apply to humans and agents
alike.

## Checks

```sh
scripts/check.sh
```

Builds the site and verifies that every internal link resolves to a real page,
every `#anchor` matches a real heading, every code fence declares a language, and
every page has valid frontmatter. **Hugo does not check internal links** — it
renders a dead `/wiki/...` link without complaint — so this script is what keeps
a rename from silently 404ing in production.

It runs three ways, and they are the same check:

- by hand, as above;
- in CI on every push and pull request ([`.github/workflows/check.yml`](.github/workflows/check.yml));
- at the end of every Claude Code turn, via a `Stop` hook, so an agent cannot
  leave the wiki broken.

## Deployment

Cloudflare Pages:

- **Build command:** `hugo`
- **Build output directory:** `public`

## Layout overrides

`themes/hugo-book/` is a git submodule — do not edit it. To change rendering, add
a file under `layouts/` with the same name and it shadows the theme's version.
That is how `layouts/single.html` and `layouts/list.html` render the page title
as an `<h1>`, which the theme itself does not do.
