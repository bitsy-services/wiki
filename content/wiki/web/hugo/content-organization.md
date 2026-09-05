---
title: "Content Organization"
weight: 10
aliases: ["/wiki/hugo/content-organization/"]
---

The `content/` directory is the site map. Hugo derives every URL from the file path: `content/docs/guide/alpha.md` is served at `/docs/guide/alpha/`, with the `content/` prefix and the `.md` suffix dropped and a directory containing `index.html` written for it. There is no routing table and no place to declare a URL other than the file's own location, which is what makes renaming a page a link-breaking operation rather than a configuration change.

## One character separates two kinds of page

A directory under `content/` can hold an `_index.md` or an `index.md`.

`_index.md` makes the directory a **branch bundle** — a section. The page renders through `list.html` — which file that resolves to is [template lookup](/wiki/web/hugo/template-lookup) — and its `.Pages` collection contains the pages beneath it. `content/docs/_index.md` is served at `/docs/`, and every page under `content/docs/` belongs to it.

`index.md` makes the directory a **leaf bundle** — one page that owns the files sitting beside it. `content/docs/bundle/index.md` is served at `/docs/bundle/`, and a sibling `data.txt` becomes a page resource, available to templates as `.Resources` and copied to `/docs/bundle/data.txt` on build. A leaf bundle has no children; any Markdown file inside it is a resource of the page, not a page of its own.

```text
content/
├── docs/
│   ├── _index.md          branch bundle → /docs/          (has .Pages)
│   ├── guide/
│   │   ├── alpha.md       →  /docs/guide/alpha/
│   │   └── beta.md        →  /docs/guide/beta/
│   └── bundle/
│       ├── index.md       leaf bundle   → /docs/bundle/    (has .Resources)
│       └── data.txt       →  /docs/bundle/data.txt
```

Getting the two backwards is quiet rather than loud. Name a section index `index.md` and the section stops listing its children, because Hugo now believes the sibling Markdown files are attachments.

## A directory is not automatically a section

`content/docs/guide/` in the tree above contains two pages and no `_index.md`. It is therefore not a section: no page is generated at `/docs/guide/`, and `alpha.md` reports its section as `docs`, not `guide`. Only a top-level directory under `content/` or a directory carrying an `_index.md` becomes a section.

The consequence is a 404 on a URL a reader will guess. Trimming `/docs/guide/alpha/` back to `/docs/guide/` is a normal navigation habit, and it lands on nothing until the directory gets an `_index.md`. Every subdirectory in this wiki's `content/wiki/` has one for that reason.

## Front matter

Front matter is the block at the top of the file, fenced with `---` for YAML, `+++` for TOML, or braces for JSON. Hugo reserves a set of keys and hands everything else to templates under `.Params`.

```yaml
---
title: "Content Organization"     # required in practice; templates render it
weight: 10                        # sort order within the section
date: 2026-09-03
draft: true                       # excluded unless `hugo -D`
slug: "organizing-content"        # replaces the filename in the URL
url: "/some/other/path/"          # replaces the whole path
aliases: ["/old/path/"]           # generates redirect pages at these URLs
layout: "wide"                    # forces a specific template
type: "docs"                      # overrides the type used in template lookup
---
```

`weight` sorts ascending, and pages without a weight sort *after* every page that has one — a section holding `10`, `20`, and one unweighted page lists them in that order. This is why the convention here is to number in tens: inserting a page between two others is a one-line edit rather than a renumbering pass.

`layout` and `type` are the two keys that change which template renders the page rather than what the page contains; [template lookup](/wiki/web/hugo/template-lookup#the-order) is where they take effect.

`aliases` is the repair for a rename. Hugo generates a small redirecting HTML page at each old URL, which recovers inbound links from outside the site. It does nothing for links *inside* the site, which still point at a path that now only redirects — [internal links](/wiki/web/hugo/internal-links) is where that gets checked.

## Cascade

A branch bundle can set front matter on everything beneath it:

```yaml
---
title: "Docs"
cascade:
  color: blue
  type: docs
---
```

Every descendant page — including leaf bundles several directories down — now reports `.Params.color` as `blue` unless it sets the key itself. `layout` and `type` cascade with everything else, so one block at the top of a subtree can route all of it through a different template. The cost is that a page can carry a parameter appearing nowhere in its own front matter, and the only place to look is upward.

## Keeping files out of the build

`ignoreFiles` in the site configuration takes a list of regular expressions matched against the file path, and Hugo skips anything matching.

```toml
ignoreFiles = ['CLAUDE\.md$']
```

This wiki uses it for exactly one purpose. Directory-scoped agent instructions live in a `CLAUDE.md` inside the content folder they govern, so the instructions sit beside the pages they describe — see [Claude Code](/wiki/ai/context-engineering/claude-code) for why proximity matters there. Without the ignore rule, each of those files would render as a wiki page at a URL like `/wiki/ai/llm/claude`, indexed by search engines and linked from the sidebar.

`draft: true` is the other exclusion, and it behaves differently: drafts are skipped by `hugo` but included by `hugo server -D`, so a draft is visible locally and absent in production without any file moving.

## Check yourself

`hugo list all` prints one row per page with its path, kind, section, and permalink, which answers most "why is this page at that URL" questions directly:

```bash
hugo list all
```

```text
path,slug,title,...,permalink,kind,section
content/docs/guide/alpha.md,,Alpha,...,https://example.org/docs/guide/alpha/,page,docs
content/docs/_index.md,,Docs,...,https://example.org/docs/,section,docs
```

The `kind` column distinguishes `page` from `section`, so a directory that should be a section and shows no `section` row is missing its `_index.md`.

## External references

- [Hugo: Page bundles](https://gohugo.io/content-management/page-bundles/)
- [Hugo: Front matter](https://gohugo.io/content-management/front-matter/)
- [Hugo: URL management](https://gohugo.io/content-management/urls/)
