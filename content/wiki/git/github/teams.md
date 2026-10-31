---
title: "Teams"
weight: 30
---

A team on GitHub is a named group of members of one organization, the shared account that owns a set of repositories. An organization can grant access to a team instead of to each person: a [repository role](/wiki/git/github/repository-roles) on one repository, or an [organization role](/wiki/git/github/organization-roles) across all of them. Every member of the team then holds that access, a person added to the team gains it, and a person removed loses it. A team is also an address. Members can mention it in a comment to notify the people in it, request a pull request review from it, and name it as the owner of files in a `CODEOWNERS` file.

GitHub derives each team's slug, the form of the name used in its URL and in API paths, from the team's name, so a team called `Justice League` has the slug `justice-league`. Granting a team access to a repository takes Admin on that repository, which every organization owner has on every repository.

## Members and maintainers

A team has two roles of its own. A member belongs to the team and holds whatever access it has been given. A maintainer can also manage the team: rename it and change its description and visibility, add and remove members, make other members maintainers, manage how review requests to the team are assigned, and remove the team's access to repositories. Being a maintainer does not let a person give the team access to a repository; that takes Admin on the repository. Organization owners can manage every team.

Creating a team through the REST API makes the account that created it a maintainer, so an owner who scripts the creation of a team ends up on it.

## Visible and secret teams

A visible team can be seen and mentioned by every member of the organization. A secret team is visible only to its own members and to the organization's owners, although its name still shows in any comment that mentions it. People outside the organization cannot see any of its teams. The REST API calls a visible team `closed`, and creates a team without a parent as secret unless the request says otherwise.

## Nested teams

A team can have one parent team, and a parent can have several child teams. A child team inherits the repository access of its parent, so granting a parent Write on a repository gives every team below it the same. GitHub's example is the hierarchy Employees, Engineering, Application Engineering, Identity: a grant to Engineering reaches Application Engineering and Identity too. Inherited access can only be changed on the parent, and removing it there removes it from every child. Mentioning a parent team notifies the members of its child teams as well. Those people are listed on the parent's **Members** tab, but they are not direct members of the parent.

Organization roles appear to pass down the same way, although GitHub's documentation does not say so directly. Its announcement of the all-repository roles describes "indirect assignments", roles that a user or team receives through a team it belongs to, and the REST API's list of a team's members includes the members of its child teams. A team that holds a role such as [All-repository write](/wiki/git/github/team-write-access) should therefore be treated as extending it to any team nested beneath it.

Secret teams cannot be nested, as parents or as children.

## Who can join a team

Only members of the organization can be on a team. Outside collaborators, the people given access to particular repositories without joining the organization, cannot. An owner who adds someone from outside the organization to a team sends them an invitation to the organization, by username or email address, and they join the team when they accept it. The membership stays pending until then, and the invitation expires after seven days. On a plan billed per user, each invitation needs an unused license.

Organizations on GitHub Enterprise Cloud can synchronize a team with a group in an identity provider, the service that holds the company's user accounts. Membership of a synchronized team is managed in the identity provider, and the REST API refuses changes to it.

## Who can create a team

Organization owners can always create teams. Members can too unless an owner clears **Allow members to create teams** under **Settings**, **Member privileges**, **Team creation rules**; by default it is allowed.

## When access ends

Removing a person from a team removes the access they held only through it. If they are left with no access to a private repository, GitHub deletes their forks of it, though not their local clones. Deleting a team, or revoking its access to a private repository, has the same effect on each member who has no access to the repository through another team.

## Further reading

- GitHub Docs, [About organization teams](https://docs.github.com/en/organizations/organizing-members-into-teams/about-teams), including nested teams
- GitHub Docs, [Assigning the team maintainer role to a team member](https://docs.github.com/en/organizations/organizing-members-into-teams/assigning-the-team-maintainer-role-to-a-team-member)
- GitHub Docs, [Changing team visibility](https://docs.github.com/en/organizations/organizing-members-into-teams/changing-team-visibility)
- GitHub Docs, [Managing team access to an organization repository](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/managing-team-access-to-an-organization-repository), on what happens to forks
- GitHub Docs, [Setting team creation permissions in your organization](https://docs.github.com/en/organizations/managing-organization-settings/setting-team-creation-permissions-in-your-organization)
- GitHub Docs, [REST API endpoints for teams](https://docs.github.com/en/rest/teams/teams) and [team members](https://docs.github.com/en/rest/teams/members)
