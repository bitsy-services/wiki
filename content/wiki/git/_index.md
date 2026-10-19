---
title: "Git"
weight: 22
bookCollapseSection: true
---

Working notes and how-to guides for [Git](https://git-scm.com/) -- the distributed version control system behind nearly everything in this repository. These pages favor a particular, opinionated workflow over an exhaustive command reference: small, complete commits and clean, linear history.

The official [Pro Git book](https://git-scm.com/book/en/v2) remains the best free reference for anything not covered here.

Three pages so far, on the places that workflow gets contentious. [Squashing commits](/wiki/git/squashing) comes first: what replacing several commits with one does to the commit graph, why further work on a squash-merged branch, and any branch built on it, can then conflict with changes that have already landed, and how to tell a branch worth squashing from one that is not. [Squash merge](/wiki/git/squash-merge) is the landing method in detail -- the commands, the forge button, and the commit message that has to carry the whole branch. [Contributing to open source](/wiki/git/contributing-to-open-source) is the other side of the same coin: a pull request against someone else's project is a social act before it is a technical one, and the conventions exist to make a volunteer maintainer's job smaller rather than larger.

## Wiki Pages

{{< section >}}
