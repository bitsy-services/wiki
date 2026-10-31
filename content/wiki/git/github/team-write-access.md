---
title: "Team Write Access to All Repositories"
weight: 10
---

A GitHub organization, the shared account that owns a group's repositories, can give one team the Write role on every one of its repositories with a single assignment: the organization role **All-repository write**, assigned to the team. An [organization role](/wiki/git/github/organization-roles) is a set of permissions granted across the whole organization instead of on one repository. This one carries Write, the [repository role](/wiki/git/github/repository-roles) that lets a person push commits and merge pull requests. Once the team holds it, each member can write to every repository the organization owns, including repositories created later, and a person added to the team afterwards gets the same access on joining.

An organization owner sets it up in three steps on github.com: create the [team](/wiki/git/github/teams), add the people, and assign the role to the team. All-repository write is built into [every organization on GitHub.com](/wiki/git/github/organization-roles#which-plans-have-them), on the free plan as on the paid ones, and into GitHub Enterprise Server, the edition of GitHub that a company runs on its own servers, from version 3.15. The same steps can be run from a terminal with the GitHub command-line tool, `gh`.

## Before you start

- You need to be an owner of the organization, its top administrative role. Only owners can assign organization roles.
- The repositories have to belong to an organization. A repository under a personal account has no teams, only collaborators.
- Only members of the organization can be on a team. An owner who adds someone from outside sends them an invitation to the organization, and they join the team when they accept it. On a plan billed per user, each invitation needs an unused license.
- Write includes read access to GitHub Actions secrets. Actions is GitHub's service for running automated workflows in a repository, and GitHub's guidance for it says that "any user with write access to your repository has read access to all secrets configured in your repository", so the team can read the Actions secrets of every repository in the organization.

## On github.com

### 1. Create the team

1. Open the organization's page and click the **Teams** tab.
2. Click **New team**.
3. Type a name for the team, such as `Developers`, and optionally a description.
4. Leave **Parent team** empty.
5. Under **Team visibility**, choose **Visible**, so that every member of the organization can see the team and mention it.
6. Click **Create team**.

If the organization already has a team with that name, choose another name rather than reusing it: everyone already on that team would receive the role.

### 2. Add the members

1. On the team's page, click the **Members** tab, then **Add a member**.
2. Type the person's GitHub username and press Enter. Someone outside the organization can be entered by username or email address; GitHub emails them an invitation.
3. Check that the name shown is the person you mean, and click the **Add** button, which names the person and the team.

Repeat for each person.

### 3. Give the team All-repository write

1. On the organization's page, click **Settings**.
2. In the sidebar, under **Access**, click **Organization roles**, then **Role assignments**.
3. Click **New role assignment**.
4. Search for the team and select it, then select the role **All-repository write**.
5. Click **Add new assignment**.

If the list has no **All-repository write**, as on GitHub Enterprise Server before 3.15, [grant Write repository by repository](#without-all-repository-write) instead.

### 4. Check the result

Under **Settings**, **Organization roles**, **Role assignments**, the **Teams** tab lists the team with a count of its roles; clicking the count shows **All-repository write**. The team's own page and each repository's access settings mention the organization-wide grant instead of listing every repository.

## With the GitHub CLI

These commands repeat the steps from a terminal, using `gh` signed in as an organization owner. The organization-role requests need the `admin:org` scope, the permission on `gh`'s token for managing an organization, which `gh` does not request when it signs in. This command adds it, after a confirmation in the browser:

```bash
gh auth refresh -h github.com -s admin:org
```

Set the organization's name, the part after `github.com/` in its address, and create the team:

```bash
ORG=your-org
TEAM=$(gh api --method POST "orgs/$ORG/teams" -f name='Developers' -f privacy=closed --jq .slug) || TEAM=
echo "$TEAM"
```

`echo` prints the team's slug, the form of its name used in URLs and API paths, such as `developers`. An error followed by an empty line means no team was created, most often because one with that name exists already. Choose another name rather than reusing that team: everyone already on it would receive the role. `privacy=closed` is what the web page calls **Visible**; without it the API creates a secret team. The API also makes whoever creates a team one of its [maintainers](/wiki/git/github/teams#members-and-maintainers), the members who can manage it, so the owner running the command is now on the team, and can leave it on the team's **Members** tab.

In a later terminal session, or for the team made in the web steps above, set `TEAM` by hand to the team's slug, the last part of the address of its page. For `github.com/orgs/your-org/teams/developers`, that is `TEAM=developers`.

Add the members, listing their usernames after `in`, separated by spaces:

```bash
for user in alice bob carol; do
  if gh api "orgs/$ORG/members/$user" --silent; then
    gh api --method PUT "orgs/$ORG/teams/${TEAM:?}/memberships/$user" --jq .state
  else
    echo "$user is not a member of $ORG: skipped"
  fi
done
```

Each person added prints `active`. The loop adds only people who are already members of the organization: for anyone else `gh` reports `Not Found (HTTP 404)` and the loop skips them, so a mistyped username cannot send an invitation to a stranger's account. Someone from outside is invited from the organization's **People** tab instead, where the invitation can name the team, and joins it on accepting. `${TEAM:?}` stops a command when `TEAM` is empty, instead of sending it with a gap in the address.

Find the role:

```bash
ROLE=$(gh api "orgs/$ORG/organization-roles" \
  --jq '.roles[] | select(.source == "Predefined" and .base_role == "write") | .id') || ROLE=
gh api "orgs/$ORG/organization-roles/${ROLE:?}" --jq .name
```

The first command picks All-repository write out of the organization's roles: the role GitHub predefines whose repository role is Write. The second prints that role's name as the API spells it, which should be something like `all_repo_write`. If the first command prints an error, the usual cause is a missing `admin:org` scope. If it prints nothing and the second stops with `ROLE: parameter null or not set`, the organization has no such role, and the [per-repository method](#without-all-repository-write) applies. Otherwise, assign the role to the team; the command prints nothing when it succeeds:

```bash
gh api --method PUT "orgs/$ORG/organization-roles/teams/${TEAM:?}/${ROLE:?}"
```

Check who now holds the access, and test one of them:

```bash
gh api --paginate "orgs/$ORG/teams/${TEAM:?}/members" --jq '.[].login'
gh api --paginate "orgs/$ORG/teams/${TEAM:?}/invitations" --jq '.[] | .login // .email'
gh api "repos/$ORG/website/collaborators/alice/permission" --jq .role_name
```

The first command lists everyone on the team, including the members of any child teams (teams nested inside it), and each of them now has Write. The second lists anyone invited to the team who has not yet accepted; each will hold Write on accepting, with nothing more from the owner. The third checks one person on one repository, with a real repository in place of `website` and a team member in place of `alice`. The expected answer is `write`. GitHub reports the highest role a person holds on the repository from any source, so an organization owner shows `admin`.

`gh` keeps the `admin:org` scope until it is removed. This removes it, again after a confirmation in the browser:

```bash
gh auth refresh -h github.com -r admin:org
```

## What the team can and cannot do

Write lets each member push to any branch that no protection rule or ruleset restricts, merge pull requests, approve a pull request so that the approval counts towards a required review, create releases, and edit and run GitHub Actions workflows. It does not let them push to protected branches, change branch protection rules or rulesets (GitHub's newer form of branch rules), manage who has access, change the repository's settings, or delete, archive or transfer the repository. Those belong to the Maintain and Admin roles, and [Repository roles](/wiki/git/github/repository-roles) lists what each of the five roles adds.

The role covers every repository the organization owns, and an assignment cannot leave one out. A team that must not write to some repositories needs [per-repository grants](#without-all-repository-write). An archived repository stays read-only for everyone, whatever their role.

The access follows the team's membership, and that membership includes nested teams. A team later nested under this one should be expected to receive the role as well: GitHub's announcement of the roles describes roles that a user or team receives through a team it belongs to, and the team's member list includes the members of its child teams.

## Without All-repository write

The older method grants Write repository by repository. It is the one to use when the organization has no All-repository write role, or when the team should write to all repositories but a few. In the web interface it is done in each repository: **Settings**, **Collaborators & teams**, **Add teams**, then choose the team and the role **Write**. From the terminal, with `ORG` and `TEAM` set as in the CLI steps, first list the repositories:

```bash
gh api --paginate "orgs/$ORG/repos?per_page=100" \
  --jq '.[] | select(.archived | not) | .name' > repos.txt
```

`repos.txt` now holds the name of every repository in the organization that is not archived. Archived ones are left out because GitHub does not let anyone add a team to an archived repository. Delete the line of any repository the team should not write to, then grant Write on the rest:

```bash
while read -r repo; do
  gh api --method PUT "orgs/$ORG/teams/${TEAM:?}/repos/$ORG/$repo" -f permission=push && echo "$repo"
done < repos.txt
```

`push` is the API's name for Write, and each repository's name is printed once its grant succeeds. The grants are per repository, so a repository created later has none until it is granted on its own, with its name in place of `new-repo`:

```bash
gh api --method PUT "orgs/$ORG/teams/${TEAM:?}/repos/$ORG/new-repo" -f permission=push
```

Running both commands above again instead would rebuild `repos.txt` with every repository, including the ones deleted from it, and would set the team back to Write wherever its role has been raised or lowered since.

## When the team would be everyone

If every member of the organization should write to every repository, no team is needed. The organization's base permission is a repository role that every member holds on every repository, and it can be set to Write: **Settings**, then **Member privileges** under **Access**, then **Write** under **Base permissions**, and confirm the change. It applies to current and future members alike, and never to outside collaborators, the people given access to particular repositories without joining the organization. A team limits the access to the people in it; the base permission reaches every member, with no exceptions.

## Taking the access away

To remove the role and keep the team, open **Settings**, **Organization roles**, **Role assignments**, click the team's role count, click **Remove** beside **All-repository write**, and confirm with **Remove**. From the terminal, with `ORG` and `TEAM` set as in the CLI steps, these commands add the `admin:org` scope back, find the role again, remove it from the team, and drop the scope:

```bash
gh auth refresh -h github.com -s admin:org
ROLE=$(gh api "orgs/$ORG/organization-roles" \
  --jq '.roles[] | select(.source == "Predefined" and .base_role == "write") | .id') || ROLE=
gh api --method DELETE "orgs/$ORG/organization-roles/teams/${TEAM:?}/${ROLE:?}"
gh auth refresh -h github.com -r admin:org
```

The `:?` guards matter most here. With an empty `ROLE` and no guard, the request would go to `…/teams/developers/`, a trailing slash away from the endpoint that removes every organization role the team holds.

Grants made repository by repository go when the team is deleted: on the **Teams** tab, select the team, then choose **Delete** from the menu above the list. To keep the team, remove each repository it has been granted, as GitHub lists them:

```bash
gh api --paginate "orgs/$ORG/teams/${TEAM:?}/repos" --jq '.[].name' |
while read -r repo; do
  gh api --method DELETE "orgs/$ORG/teams/${TEAM:?}/repos/$ORG/$repo" && echo "$repo"
done
```

The list comes from GitHub rather than from `repos.txt`, so it includes repositories granted on their own later. An archived repository keeps its grant, since GitHub refuses to change the teams of an archived repository; `gh` reports an error for it.

Removing a person from the team takes away the Write they held through it. A person left with no access to a private repository loses their forks of it as well: GitHub deletes the forks, though not the clones on the person's own machine.

## Further reading

- GitHub Docs, [Creating a team](https://docs.github.com/en/organizations/organizing-members-into-teams/creating-a-team) and [Adding organization members to a team](https://docs.github.com/en/organizations/organizing-members-into-teams/adding-organization-members-to-a-team)
- GitHub Docs, [Using organization roles](https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles) and [Permissions of predefined organization roles](https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/permissions-of-predefined-organization-roles)
- GitHub Changelog, [Pre-defined organization roles that grant access to all repositories](https://github.blog/changelog/2024-07-10-pre-defined-organization-roles-that-grant-access-to-all-repositories/) (10 July 2024)
- GitHub Docs, [REST API endpoints for organization roles](https://docs.github.com/en/rest/orgs/organization-roles), [for teams](https://docs.github.com/en/rest/teams/teams) and [for organization members](https://docs.github.com/en/rest/orgs/members)
- GitHub Docs, [Setting base permissions for an organization](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/setting-base-permissions-for-an-organization)
- GitHub Docs, [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) for GitHub Actions, on what write access exposes
