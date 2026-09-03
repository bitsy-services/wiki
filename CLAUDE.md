# CLAUDE.md

## Project Overview

This is the Bitsy Services Wiki, a Hugo static site using the Hugo Book theme. It is deployed to Cloudflare Pages at wiki.bitsy.services.

## Structure

- `content/wiki/` — wiki pages (Markdown with YAML frontmatter)
- `hugo.toml` — site configuration
- `themes/hugo-book` — theme (git submodule, do not edit)
- `static/` — static assets (images, files); the icon set is generated, see below
- `layouts/` — template overrides; a file here shadows the theme's file of the same name
- `scripts/` — the checks; `scripts/acronyms.txt` is the acronym registry they enforce
- `backlog/` — harness improvement items, consumed one per session

## Site Icons

`favicon.svg`, `favicon.ico`, `apple-touch-icon.png` and `og-image.png` in
`static/` are **generated** — do not hand-edit them. They all come from one
parametric description of the hexagonal web mark in `scripts/gen-icons.py`
(`GEOM` holds the stroke width and the three radii). Change the mark there and
re-run `python3 scripts/gen-icons.py`, so the vector and raster copies cannot
drift apart.

The `<link>` tags live in `layouts/_partials/docs/html-head-favicon.html`, which
overrides the theme's single-`favicon.png` partial. The default Open Graph and
Twitter card image is `params.images` in `hugo.toml`; Hugo's embedded
`opengraph.html` and `schema.html` read it automatically, and
`layouts/_partials/docs/inject/head.html` adds `twitter_cards.html`, which the
theme does not call on its own. A page can override it with `images` in its own
frontmatter.

## Verifying your work

**`scripts/check.sh` is the definition of done.** It builds the site and checks
every internal link, every `#anchor`, every code fence, every frontmatter
block, and every acronym. Run it before you claim a content change is finished; a `Stop` hook runs
it anyway, and a red check blocks the turn from ending.

The link check is the load-bearing part: **Hugo does not validate internal
links.** It renders `/wiki/does-not-exist` without complaint, so a page rename
silently 404s in production unless this script catches it. It already caught six
such links.

If a page is new or substantially rewritten, follow it with the `wiki-reviewer`
subagent — it re-reads the result in a fresh context, without the reasoning that
produced it.

## Commands

- `scripts/check.sh` — build + content checks (the gate)
- `hugo server -D` — local dev server with drafts
- `hugo` — production build to `public/`

## Content Conventions

- Pages go under `content/wiki/`. The `new-wiki-page` skill has the full procedure.
- Use `weight` in frontmatter to control sidebar ordering
- Use `bookCollapseSection: true` for section pages (`_index.md`)
- Start the body at `##`. `layouts/single.html` renders the frontmatter `title` as the page h1; the theme itself renders no title heading at all.
- Code blocks must specify a language (`text` for formulas and ASCII diagrams)
- Directory-scoped agent instructions can live in a `CLAUDE.md` inside a `content/wiki/<section>/` folder; `ignoreFiles = ['CLAUDE\.md$']` in `hugo.toml` keeps Hugo from rendering them as pages

## Self-Improvement

See `.claude/rules/self-improvement.md` for the full framework. When working in this repo, update this file if you discover new project-level conventions (build nuances, theme customizations, shortcodes, gotchas).
