# CLAUDE.md

## Project Overview

This is the Bitsy Services Wiki, a Hugo static site using the Hugo Book theme. It is deployed to Cloudflare Pages at wiki.bitsy.services.

## Structure

- `content/wiki/` — wiki pages (Markdown with YAML frontmatter)
- `hugo.toml` — site configuration
- `themes/hugo-book` — theme (git submodule, do not edit)
- `static/` — static assets (images, files)
- `layouts/` — template overrides

## Commands

- `hugo server -D` — local dev server with drafts
- `hugo` — production build to `public/`

## Default Intent

Treat the first message of a conversation as a request to create a new wiki page unless the intent is clearly something else (e.g. a question, bug report, or explicit edit request). Draft the page, choose a sensible path under `content/wiki/`, and set appropriate frontmatter.

## Content Conventions

- Pages go under `content/wiki/`
- Use `weight` in frontmatter to control sidebar ordering
- Use `bookCollapseSection: true` for section pages (`_index.md`)
- Code blocks should specify a language for syntax highlighting

## Self-Improvement

When working in this repo, update this file if you discover:

- New conventions or patterns that are established in the content
- Build or deployment nuances (e.g. Cloudflare-specific config)
- Theme customizations added in `layouts/`
- Shortcodes or partials in use
- Any gotchas or non-obvious behavior
