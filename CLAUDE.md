# CLAUDE.md

## Project Overview

This is the Bitsy Services Wiki, a Hugo static site using the Hugo Book theme. It is deployed to Cloudflare Pages at wiki.bitsy.services.

## Structure

- `content/wiki/` — wiki pages (Markdown with YAML frontmatter)
- `hugo.toml` — site configuration
- `themes/hugo-book` — theme (git submodule, do not edit)
- `static/` — static assets (images, files)
- `layouts/` — template overrides; a file here shadows the theme's file of the same name
- `scripts/` — the checks
- `backlog/` — harness improvement items, consumed one per session

## Verifying your work

**`scripts/check.sh` is the definition of done.** It builds the site and checks
every internal link, every `#anchor`, every code fence, and every frontmatter
block. Run it before you claim a content change is finished; a `Stop` hook runs
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
