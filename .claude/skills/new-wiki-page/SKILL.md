---
name: new-wiki-page
description: Create a new page (or section) in this Hugo wiki — choose the path, write the frontmatter, link it into the existing pages, and verify it builds. Use whenever the task is to add or substantially expand wiki content.
argument-hint: [topic]
---

# Creating a wiki page

A procedure, not a set of facts. The always-on rules in `.claude/rules/` tell you
*what good content looks like*; this tells you *how to land it*.

## 1. Place it

**`.claude/rules/wiki-taxonomy.md` is the authority.** Read it before choosing a
path: it carries the section map, the rules for what may sit at the top level,
and the procedure for the case where nothing fits. Do not infer placement from
the existing tree — `git/` and `microsoft/` sit at a grain the rules no longer
allow, and reading them as precedent is what put the Hugo section at
`/wiki/hugo` instead of `/wiki/web/hugo`.

State the path and the reason before drafting. A wrong placement is a sentence
to correct now and a `git mv` plus a link rewrite plus an alias on every file
later.

- A single page is `content/wiki/<section>/<slug>.md`.
- A topic that needs several pages is a folder with an `_index.md` carrying
  `bookCollapseSection: true`, plus one file per child page. Three pages is the
  threshold for making that folder; one page does not get one.
- The URL is the path minus `content/` and minus the `.md`, so
  `content/wiki/economics/finance/defi/amm.md` serves at
  `/wiki/economics/finance/defi/amm`. Choose the slug with the URL in mind —
  other pages will link to it, and moving it later breaks every inbound link.

Check first whether a stub already exists for the topic; expanding a stub beats
creating a rival page.

## 2. Frontmatter

```yaml
---
title: "Automated Market Maker"
weight: 20
---
```

`weight` orders the sidebar within its directory; leave a gap (10, 20, 30) so a
later page can be slotted in without renumbering. Section `_index.md` files also
take `bookCollapseSection: true`.

Do not start the body with an `# H1` — `layouts/single.html` already renders the
title as the page's h1. Start at `##`.

## 3. Link it in — both directions

A new page that nothing links to is unreachable except from the sidebar. Before
you finish:

- Link *out* to related pages on first mention of each domain term.
- Link *in*: grep for the topic across `content/` and add links from the pages
  that already discuss it.

```bash
grep -rln "automated market maker\|AMM" content/
```

If you reference a page that doesn't exist yet, create it as a stub — a real
page with frontmatter and a short body of external links on the topic. The
checker fails on links to nonexistent pages, so this is not optional.

## 4. Verify

```bash
scripts/check.sh
```

This builds the site and checks every internal link and anchor, the code-fence
languages, and the frontmatter. It must be green. It is also wired to a Stop
hook, so a red check will block the turn from ending anyway.

Writing a page with Solidity examples? `.claude/rules/solidity-examples.md`
loads automatically for `content/wiki/economics/finance/defi/**`, and its rules are not optional —
the code in this wiki gets copy-pasted.
