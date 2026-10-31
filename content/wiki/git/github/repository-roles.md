---
title: "Repository Roles"
weight: 20
---

A repository role is the level of access a person or a team has to one repository owned by a GitHub organization. GitHub defines five, and each includes everything the one below it allows: **Read**, **Triage**, **Write**, **Maintain** and **Admin**. A person can hold roles on the same repository from several sources at once, such as a [team](/wiki/git/github/teams), the organization's base permission and an [organization role](/wiki/git/github/organization-roles), and the highest of them is the one in effect.

## The five roles

From least access to most, with GitHub's own description of whom each role is for:

| Role | Recommended for | What it adds to the role above |
| --- | --- | --- |
| Read | "non-code contributors who want to view or discuss your project" | Clone, pull and fork; open issues; comment; review pull requests |
| Triage | "contributors who need to proactively manage issues, discussions, and pull requests without write access" | Apply labels and milestones; close, reopen and assign any issue or pull request; request reviews; mark duplicates |
| Write | "contributors who actively push to your project" | Push to branches that no protection rule or ruleset restricts; merge pull requests; approvals that count towards required reviews; create and edit releases; create labels and milestones; edit and run GitHub Actions workflows and manage their secrets and variables; publish packages; act as a code owner |
| Maintain | "project managers who need to manage the repository without access to sensitive or destructive actions" | Push to branches protected by branch protection rules; edit the description and topics; configure how pull requests merge; choose the GitHub Pages publishing source; turn on Discussions; limit interactions |
| Admin | "people who need full access to the project, including sensitive and destructive actions like managing security or deleting a repository" | Change the settings and visibility; manage who has access; edit branch protection rules and rulesets; manage webhooks and deploy keys; change the default branch; delete, archive or transfer the repository |

The table is a selection from GitHub's full reference, linked below, in which no action is allowed to one role and refused to a role above it.

Write includes GitHub Actions, GitHub's service for running automated workflows in a repository. A person with Write can push a workflow and run it, and GitHub's guidance for Actions states that "any user with write access to your repository has read access to all secrets configured in your repository".

Maintain's right to push to protected branches applies to branch protection rules only. Rulesets, the newer form of branch rules, keep their own list of who may bypass them, and the role does not put anyone on it.

## Where a role comes from

In an organization, a person's role on a repository can come from any of these sources:

- Ownership. Organization owners have Admin on every repository the organization owns.
- The base permission, one role that every member of the organization holds on every repository: none, Read, Write or Admin, with Read as the default. It does not apply to outside collaborators, the people given access to particular repositories without joining the organization.
- [Teams](/wiki/git/github/teams). A team given a role on a repository passes it to each of its members, and a child team inherits the repository access of its parent.
- [Organization roles](/wiki/git/github/organization-roles). The five all-repository roles give the holder the matching repository role on every repository, including repositories created later.
- Direct access. A person can be given a role on one repository by name. This is how an outside collaborator gets in.

GitHub's documentation calls roles "additive": a person given access through several sources "has the sum of all access grants". Since each of the five roles contains the ones below it, the sum of two of them is the higher one. One consequence is that no grant can lower another: a team's Read on a repository leaves a member at Write if the base permission is Write. Where a person holds different roles from different sources, the repository's **Collaborators & teams** settings page marks them with a **Mixed roles** warning, and hovering over it shows where each role comes from.

## Role names in the API

The REST API names the roles `pull`, `triage`, `push`, `maintain` and `admin` when a role is granted, as in the `permission` field of a request that adds a repository to a team. When it reports a person's access, the permission check returns two fields. `role_name` holds the role's actual name. The older `permission` field knows only `admin`, `write`, `read` and `none`, so it reports Maintain as `write` and Triage as `read`. Both are computed from every source of access, and the response does not say which source a role came from.

## Custom repository roles

Organizations on GitHub Enterprise Cloud, the enterprise plan of GitHub.com, and on GitHub Enterprise Server, the edition a company runs on its own servers, can define custom repository roles, up to 20 of them, or five on Enterprise Server releases before 3.19. Each starts from Read, Triage, Write or Maintain and adds chosen permissions, and anyone with Admin on a repository can then grant it there like one of the five. Organizations on GitHub Free and GitHub Team have only the five.

## Repositories under a personal account

A repository owned by a personal account has no roles, only two levels of access: its owner, who has full control, and collaborators, whom the owner invites. GitHub's own advice for anyone who needs finer control is to transfer the repository to an organization.

## Further reading

- GitHub Docs, [Repository roles for an organization](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization), with the full table of actions
- GitHub Docs, [Setting base permissions for an organization](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/setting-base-permissions-for-an-organization)
- GitHub Docs, [Managing teams and people with access to your repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/managing-teams-and-people-with-access-to-your-repository)
- GitHub Docs, [Get repository permissions for a user](https://docs.github.com/en/rest/collaborators/collaborators#get-repository-permissions-for-a-user), the REST permission check
- GitHub Docs, [About custom repository roles](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/about-custom-repository-roles)
- GitHub Docs, [Permission levels for a personal account repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/repository-access-and-collaboration/permission-levels-for-a-personal-account-repository)
