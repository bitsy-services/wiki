---
title: "Organization Roles"
weight: 40
---

An organization role is a set of permissions that a GitHub organization grants across the whole organization, to one of its members or to a [team](/wiki/git/github/teams). The organization is the shared account that owns a group's repositories. Most of these roles let the holder manage one part of the organization, such as billing or security settings. Five of them carry a [repository role](/wiki/git/github/repository-roles) instead, and give the holder that role on every repository the organization owns, including repositories created after the assignment.

GitHub predefines a set of these roles in every organization, and organizations on GitHub Enterprise Cloud, the enterprise plan of GitHub.com, and on GitHub Enterprise Server, the edition a company runs on its own servers, can add custom ones. A person or team can hold several at once, and the roles add up with every other source of access the person has.

## The predefined roles

These are built into every organization on GitHub.com:

| Role | Grants |
| --- | --- |
| Owner | Full administrative control of the organization |
| Member | Standard access to the organization's features |
| Moderator | Moderation in the organization's public repositories: blocking and unblocking non-members, limiting interactions, hiding comments |
| Billing manager | The billing settings and subscription details |
| Security manager | Security policies, alerts and configurations across the organization and all its repositories, and Read on every repository |
| CI/CD admin | GitHub Actions, the organization's continuous integration and continuous delivery service: its policies, runners, secrets and variables |
| App Manager | Creating, editing and deleting the organization's GitHub Apps |
| All-repository read | Read on every repository |
| All-repository triage | Triage on every repository |
| All-repository write | Write on every repository |
| All-repository maintain | Maintain on every repository |
| All-repository admin | Admin on every repository |

An all-repository role grants its repository role on every repository the organization owns, those that exist when the role is assigned and those created later. GitHub's announcement of the five, in July 2024, presented them as a way to replace automation that "watches for new repository creation and adds the right users or team to every repository". An assignment cannot leave a repository out.

## Assigning a role

Organization owners assign the roles. In the organization's **Settings**, under **Access**, **Organization roles** has two pages. **Role management** lists the roles and what each permits. **Role assignments** lists who holds which role, and **New role assignment** adds one: search for the users or teams, choose a role, and click **Add new assignment**. An assignment gives one role, so a second role takes a second assignment.

The REST API exposes the same operations. `GET /orgs/{org}/organization-roles` lists the roles, each with an `id`, a `name`, a `base_role` naming the repository role it carries, if any, and a `source` that is `Predefined`, `Organization` or `Enterprise`. `PUT /orgs/{org}/organization-roles/teams/{team_slug}/{role_id}` assigns a role to a team, `PUT /orgs/{org}/organization-roles/users/{username}/{role_id}` to a person, and `DELETE` on the same paths removes it. A `DELETE` on the team or user path without a role ID removes every role the team or person holds. Personal access tokens (classic) and OAuth app tokens need the `admin:org` scope for all of these. [Team write access to all repositories](/wiki/git/github/team-write-access#with-the-github-cli) uses them with the GitHub command-line tool.

## Which plans have them

The predefined roles exist in every organization on GitHub.com, on GitHub Free, GitHub Team and GitHub Enterprise Cloud. GitHub Enterprise Server has the five all-repository roles from version 3.15, but not the whole table: GitHub's documentation lists Moderator and Billing manager for GitHub.com only, and has shown some of the other roles only on later Enterprise Server releases. Custom organization roles are limited to GitHub Enterprise Cloud and GitHub Enterprise Server.

GitHub's own documentation disagrees with itself on this point. Its page *Permissions of predefined organization roles* carries the label "Organizations on GitHub Enterprise Cloud", while its text says the predefined roles "are available by default in every organization". The label arrived in March 2026, when the list of predefined roles moved to that page from *Using organization roles*, a page labelled for GitHub Free, GitHub Pro, GitHub Team, GitHub Enterprise Cloud and GitHub Enterprise Server. The July 2024 announcement put the roles in the organization settings, "where all organization owners can view and assign them", and the documentation written for that release showed them on every GitHub.com plan and on Enterprise Server from 3.15.

## Custom organization roles

On GitHub Enterprise Cloud, an organization can create up to 20 custom organization roles, and the owners of its enterprise account can create roles for it to use. A custom role can hold permissions over organization settings, such as viewing the audit log, or a base repository role (Read, Triage, Write, Maintain or Admin) with further repository permissions on top, or both. Like the predefined all-repository roles, the repository part applies to "all current and future repositories in the organization". GitHub marks the repository part as a public preview. For access to particular repositories, it points to custom repository roles instead.

## Organization roles and the base permission

An organization's base permission is a single repository role that every member holds on every repository. An all-repository role reaches the same repositories, but only for the people and teams it is assigned to. Both add to whatever else a person holds, and since each repository role contains the ones below it, a person who holds two of them has the higher one. The highest role from any source is what applies on the repository.

## Further reading

- GitHub Docs, [Roles in an organization](https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/roles-in-an-organization)
- GitHub Docs, [Permissions of predefined organization roles](https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/permissions-of-predefined-organization-roles)
- GitHub Docs, [Using organization roles](https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles)
- GitHub Docs, [Permissions of custom organization roles](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-peoples-access-to-your-organization-with-roles/about-custom-organization-roles)
- GitHub Docs, [REST API endpoints for organization roles](https://docs.github.com/en/rest/orgs/organization-roles)
- GitHub Changelog, [Pre-defined organization roles that grant access to all repositories](https://github.blog/changelog/2024-07-10-pre-defined-organization-roles-that-grant-access-to-all-repositories/) (10 July 2024)
