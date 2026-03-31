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

## Content Conventions

- Pages go under `content/wiki/`
- Use `weight` in frontmatter to control sidebar ordering
- Use `bookCollapseSection: true` for section pages (`_index.md`)
- Code blocks should specify a language for syntax highlighting

## Self-Improvement

See `.claude/rules/self-improvement.md` for the full framework. When working in this repo, update this file if you discover new project-level conventions (build nuances, theme customizations, shortcodes, gotchas).
