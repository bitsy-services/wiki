# Bitsy Services Wiki

Internal wiki built with [Hugo](https://gohugo.io/) and the [Hugo Book](https://github.com/alex-shpak/hugo-book) theme.

## Local Development

```sh
hugo server -D
```

## Adding Content

Create Markdown files under `content/docs/`. Use `weight` in frontmatter to control sidebar order:

```markdown
---
title: "Page Title"
weight: 10
---

Your content here.
```

## Deployment

Deployed to Cloudflare Pages:

- **Build command:** `hugo`
- **Build output directory:** `public`
