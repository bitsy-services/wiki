# CLAUDE.md

## Project Overview

This is the wiki published at wiki.bitsy.services, a Hugo static site using the Hugo Book theme, deployed to Cloudflare Pages. The site's name lives in exactly one place — `title` in `hugo.toml` — and every rendered copy derives from it; see Site Name below.

It is a public, general-purpose technical wiki rather than an internal one. Any technical subject is in scope; which subjects get written follows the work at bitsy.services. `.claude/rules/wiki-scope.md` is the authority on what belongs, `.claude/rules/wiki-taxonomy.md` on where it goes, and the consequence for writing is that every page is read cold by someone arriving from a search engine.

## Structure

- `content/wiki/` — wiki pages (Markdown with YAML frontmatter)
- `hugo.toml` — site configuration
- `themes/hugo-book` — theme (git submodule, do not edit)
- `static/` — static assets (images, files); the icon set is generated, see below. `static/ads.txt` carries the Google AdSense publisher ID and must keep serving from the site root
- `layouts/` — template overrides; a file here shadows the theme's file of the same name
- `scripts/` — the checks; `scripts/acronyms.txt` is the acronym registry they enforce
- `backlog/` — harness improvement items, consumed one per session

## Site Name

`title` in `hugo.toml` is the only place the site is named. The h1 on the home
page, the sidebar brand, the `<title>` tag, the Open Graph and Twitter tags and
`assets/manifest.json` all read `.Site.Title`. `content/_index.md` sets no
`title` of its own — Hugo leaves a titleless home page's `.Title` empty rather
than falling back to the site title, so `layouts/home.html` renders
`.Site.Title` as the h1 instead. `scripts/check-content.py` inverts its
frontmatter rule for that one file: every other page must have a `title`, and
the home page must not.

## Site Icons

`static/favicon.png` is the **source of truth** for the site mark — a supplied
1600x1600 image, not generated art. `favicon.ico` and `apple-touch-icon.png`
beside it are pure resamplings of it produced by `scripts/gen-icons.py`, which
only resizes and never draws. To change the mark, replace `favicon.png` and
re-run `python3 scripts/gen-icons.py`. `static/og-image.png` is a byte-for-byte
copy of the same file, kept separate so the social card can be changed without
touching the favicon.

The `<link>` tags live in `layouts/_partials/docs/html-head-favicon.html`, which
overrides the theme's single-`favicon.png` partial. `assets/manifest.json`
overrides the theme's, whose icon entry pointed at a `favicon.svg` this site
does not have. The default Open Graph and Twitter card image is
`params.images` in `hugo.toml`; Hugo's embedded `opengraph.html` and
`schema.html` read it automatically, and
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

- Pages go under `content/wiki/`. The `new-wiki-page` skill has the full procedure, and `.claude/rules/wiki-taxonomy.md` decides the path — including when a subject warrants a new section, which is a decision to raise before drafting rather than land in a diff.
- Use `weight` in frontmatter to control sidebar ordering
- Use `bookCollapseSection: true` for section pages (`_index.md`)
- Start the body at `##`. `layouts/single.html` renders the frontmatter `title` as the page h1 (`layouts/list.html` for sections, `layouts/home.html` for the home page); the theme itself renders no title heading at all.
- Code blocks must specify a language (`text` for formulas and ASCII diagrams)
- Directory-scoped agent instructions can live in a `CLAUDE.md` inside a `content/wiki/<section>/` folder; `ignoreFiles = ['CLAUDE\.md$']` in `hugo.toml` keeps Hugo from rendering them as pages

## Self-Improvement

See `.claude/rules/self-improvement.md` for the full framework. When working in this repo, update this file if you discover new project-level conventions (build nuances, theme customizations, shortcodes, gotchas).
