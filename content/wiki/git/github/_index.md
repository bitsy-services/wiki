---
title: "GitHub"
weight: 30
bookCollapseSection: true
---

GitHub is a hosting service for [Git](/wiki/git) repositories. Git records history and copies it between repositories, and has no notion of accounts or of who may push. GitHub adds both. Every repository on it belongs either to a personal account or to an organization, a shared account with many members, and an organization decides through roles and teams what each member may do to each of its repositories.

This section covers that access model. [Team write access to all repositories](/wiki/git/github/team-write-access) is a recipe for one team holding Write on every repository the organization has or will have, set up by an owner in three steps. It comes first because it assumes nothing beyond Git itself: the terms it uses are explained where they first appear. The pages after it take those terms in depth. [Repository roles](/wiki/git/github/repository-roles) is the ladder of five access levels on a single repository, from Read to Admin, and the rule that combines roles from several sources into the one in effect. [Teams](/wiki/git/github/teams) covers the groups that hold those roles: who can be in one, how visibility and nesting work, and what happens to access when someone leaves. [Organization roles](/wiki/git/github/organization-roles) covers roles granted across the whole organization, including the five that carry a repository role to every repository, and which plans have them.

## Where the boundaries fall

The Git workflow itself, from squashing commits to landing a branch, is in the parent [Git](/wiki/git) section, which also has [the script that signs a new machine in to GitHub](/wiki/git/wsl-setup). Keys and credentials on a developer's own machine belong to [Security](/wiki/security). This section starts where they stop: with what an account may do once GitHub knows whose it is.

## Wiki Pages

{{< section >}}
