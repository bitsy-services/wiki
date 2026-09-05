---
title: "Themes and Modules"
weight: 30
aliases: ["/wiki/hugo/themes-and-modules/"]
---

A Hugo theme is a project directory with the same shape as yours — `layouts/`, `assets/`, `static/`, `i18n/`, `data/`, `archetypes/`, and often `content/` — mounted underneath your own. Hugo merges the two trees into one filesystem before the build starts, so from a template's point of view there is a single `layouts/` and a single `assets/`. Every question about "how do I change this theme" reduces to a question about that merge.

```toml
theme = 'hugo-book'
```

The value can be a list, in which case earlier entries take priority over later ones. A project file beats a theme file at the *same* path; it does not beat a theme file at a more specific one, which is the distinction [template lookup](/wiki/web/hugo/template-lookup#the-theme-is-interleaved-not-underneath) turns on.

## Overriding means matching a path

To change a theme file, put a file of your own at the identical path. There is no patch mechanism, no partial override, and no inheritance: the project's `layouts/_partials/docs/html-head-favicon.html` replaces the theme's file of that name in full, and any part of the theme's version you still wanted has to be copied across.

This wiki overrides five files. `layouts/single.html` and `layouts/list.html` replace the theme's page templates. `layouts/_partials/docs/html-head-favicon.html` replaces a partial that emitted one `<link>` tag for a single `favicon.png` with one that emits the full set. `assets/manifest.json` replaces a theme asset whose icon entry pointed at a `favicon.svg` this site does not have — the same override rule applied to `assets/` rather than `layouts/`.

The fifth, `layouts/_partials/docs/inject/head.html`, costs nothing to write. hugo-book ships nine empty partials under `inject/`, called from the places a site is most likely to want to add something, and overriding an empty file loses nothing. A theme that provides those hooks converts an override from a fork of somebody's template into an addition; a theme that does not leaves copy-and-modify as the only route.

Matching the path exactly is a stricter requirement than it sounds, because [template lookup](/wiki/web/hugo/template-lookup) interleaves project and theme candidates by specificity. A project file at a *less* specific path than the theme's does not override it; it is simply never reached.

## Vendoring: submodule or module

Two ways to get a theme onto disk, and the choice is about how the version is pinned.

**A git submodule** puts the theme's repository inside yours at `themes/<name>`, pinned to a commit:

```bash
git submodule add https://github.com/alex-shpak/hugo-book themes/hugo-book
git submodule update --init --recursive
```

The commit is recorded in the parent repository, so a checkout gets the exact theme the last build used. The cost is that every clone and every continuous-integration job needs the `--recursive` flag or an explicit `submodule update`, and forgetting it produces an empty `themes/` directory and a build with no layouts at all. This wiki takes this route: `.gitmodules` points at `hugo-book`, pinned to the commit tagged `v13`.

**A Hugo Module** is a Go module. Hugo shells out to the Go toolchain for resolution and caching, so Go has to be installed even though nothing here is Go code you wrote.

```bash
hugo mod init github.com/you/your-site
hugo mod get github.com/alex-shpak/hugo-book
```

```toml
[module]
  [[module.imports]]
    path = 'github.com/alex-shpak/hugo-book'
```

Versions are pinned in `go.mod`, updated with `hugo mod get -u`, and can be committed into `_vendor/` with `hugo mod vendor` for builds that must not reach the network. Modules compose: a module can import other modules, and Hugo mounts the whole graph.

The submodule is fewer moving parts for one theme that changes rarely. The module is the better answer once you are importing several, or once you want a version constraint rather than a commit hash.

## Mounts

Modules also expose the merge itself as configuration. A `mounts` block maps any directory on disk — including one inside an imported module — to any of Hugo's target directories:

```toml
[module]
  [[module.mounts]]
    source = 'content'
    target = 'content'
  [[module.mounts]]
    source = 'node_modules/katex/dist'
    target = 'assets/katex'
```

Declaring any mount replaces the defaults for that target, so the identity mounts have to be restated alongside the new one. The common uses are pulling a stylesheet or font out of `node_modules/` into `assets/` without a copy step, and assembling `content/` from several directories that live apart for editorial reasons. `excludeFiles` on a mount does the same job as the site-level `ignoreFiles` for a single mounted tree.

## Pitfalls, by severity

1. **An unpinned theme changing under a build.** A submodule tracking a branch, or a module import with no version, means the site that deploys tonight is built against code nobody reviewed. Hugo's own template system changed incompatibly at v0.146, and themes moved with it. Pin to a commit or a tag.
2. **A clone without submodules.** `git clone` alone leaves `themes/hugo-book` empty, and the resulting build has no layouts. Hugo does not report a missing theme as an error — it renders pages with whatever templates it can find, which may be none. Use `git clone --recurse-submodules`, and make the build step run `git submodule update --init` where the environment is not yours to control.
3. **An override that misses the path.** The file is written, the build succeeds, and the theme's version renders. `hugo --printUnusedTemplates` names files that rendered nothing, which is the fastest way to catch it.
4. **A local edit inside `themes/`.** It works until the submodule is updated, then it is gone, and it is invisible to anyone reading the project's own `layouts/`. Copy the file out to the project path instead.

## External references

- [Hugo: Modules](https://gohugo.io/hugo-modules/)
- [Hugo: Configure modules and mounts](https://gohugo.io/configuration/module/)
- [Hugo themes directory](https://themes.gohugo.io/)
- [hugo-book](https://github.com/alex-shpak/hugo-book) — the theme this wiki uses
