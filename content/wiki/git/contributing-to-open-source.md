---
title: "Submitting a PR to a Third-Party Repo"
weight: 20
---

Opening a pull request against someone else's open source project is as much a social act as a technical one. You are asking a maintainer -- usually an unpaid volunteer with a backlog -- to read your change, trust it, and take on the burden of maintaining it forever. The best contributions minimize that burden: they are small, they follow the project's existing conventions, and they arrive with enough context that the maintainer can say yes without a second round of questions. This page is an opinionated checklist for getting a change merged into a repository you don't control.

## Before you write any code

The most common reason a good patch gets rejected is that it was unwelcome before it was even written. Spend the cheap effort up front.

- **Read the contributing guide.** Look for `CONTRIBUTING.md`, a `.github/` directory, the `README`, and any `CODE_OF_CONDUCT.md`. These tell you the expected workflow, coding style, test commands, and how the maintainers want to be approached. Ignoring them signals you didn't look.
- **Search existing issues and PRs.** Someone may have already proposed your change and had it rejected for reasons you should know. If an open issue describes the problem, comment there before starting.
- **Open an issue first for anything non-trivial.** For a one-line typo fix, just send the PR. For a new feature, a refactor, or a behavioral change, ask first: "I'd like to fix X by doing Y -- would you accept a PR?" A few sentences can save you a weekend of work on a change the maintainer will never merge. Large unsolicited PRs are the ones that rot in the queue.
- **Confirm the license is compatible** with whatever you intend to do, and check whether the project requires a [Contributor License Agreement](https://en.wikipedia.org/wiki/Contributor_License_Agreement) (CLA) or a [Developer Certificate of Origin](https://developercertificate.org/) (DCO) sign-off. A CLA bot will block your PR until you sign; DCO requires every commit be made with `git commit -s`.

## Set up the fork

You don't have push access, so the standard mechanism is the **fork-and-pull** model: you fork the repository into your own account, push a branch there, and open a PR from your fork back to the original ("upstream").

```bash
# Fork on GitHub first (the "Fork" button, or `gh repo fork`), then:
git clone git@github.com:your-username/project.git
cd project
git remote add upstream git@github.com:original-owner/project.git
git fetch upstream
```

Keeping two remotes -- `origin` (your fork) and `upstream` (the source) -- lets you pull in their changes while pushing your work to your own copy. The [GitHub CLI](https://cli.github.com/) collapses the fork-and-clone step:

```bash
gh repo fork original-owner/project --clone
```

Never work on `main` in your fork. Branch for each change so you can keep your fork's `main` a clean mirror of upstream:

```bash
git switch -c fix/parser-off-by-one upstream/main
```

## Keep the change small and focused

A reviewer's willingness to merge is inversely proportional to the size of the diff. One PR should do one thing.

- **Separate concerns into separate PRs.** Don't reformat the whole file in the same change that fixes the bug -- the maintainer can't tell the substantive change from the whitespace churn. If you must reformat, do it in its own PR.
- **Match the surrounding code.** Use the project's naming, indentation, and idioms even if you'd personally do it differently. A PR that imports your stylistic preferences is a PR that starts an argument.
- **Don't bundle unrelated drive-by fixes.** Note them in an issue instead. A focused diff is reviewable in one sitting; a sprawling one gets deferred.
- **Include tests.** A change with a test that demonstrates the fix is dramatically more likely to be merged, because the maintainer doesn't have to take your word that it works -- and a regression test protects your fix from being undone later.

## Keep your branch current

Long-lived branches drift from upstream and accumulate conflicts. Sync frequently, and prefer [rebasing](https://git-scm.com/book/en/v2/Git-Branching-Rebasing) onto upstream over merging it in, so your branch stays a clean series of commits on top of the latest `main` rather than a tangle of merge commits:

```bash
git fetch upstream
git rebase upstream/main
```

Because rebasing rewrites your branch's commits, you'll need to force-push -- but use the safe variant, which refuses to clobber work you haven't seen:

```bash
git push --force-with-lease
```

Only ever force-push to *your own* PR branch. Force-pushing a branch others have based work on rewrites shared history and breaks their clones.

## Write commits and a PR description the maintainer can read

The commit history and the PR description are how you make the maintainer's job easy. Treat them as the deliverable, not an afterthought.

- **Write meaningful commit messages**: a concise imperative summary line, a blank line, then a body explaining *why* the change is needed. See the [squash merge](squash-merge.md) page for how messages get combined when a PR is squashed.
- **Reference the issue** the PR addresses with a [closing keyword](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) (`Closes #123`) so it auto-closes on merge.
- **Explain the change in the PR body**: what problem it solves, the approach you took, any alternatives you rejected, and how you tested it. If the project ships a PR template, fill it out completely.
- **Show, don't assert.** For a UI change, include before/after screenshots. For a behavioral change, paste the command output or a failing-then-passing test.

## After you open the PR

Submitting is the start of a conversation, not the end of the work.

- **Make CI pass.** Most projects run linting and tests on every PR. A red check is the first thing a maintainer sees; fix it before asking for review. Run the project's test and lint commands locally first so CI isn't your debugger.
- **Respond to review graciously.** Maintainers are doing you a favor by reviewing. Address feedback, push follow-up commits (don't force-push mid-review unless asked -- it makes the reviewer re-read everything), and resolve threads as you go. If you disagree, explain your reasoning calmly; the maintainer has the final say in their own project.
- **Be patient and persistent without nagging.** A polite check-in after a week or two is fine. Daily pings are not. Maintainers are busy, and many PRs simply wait.
- **Accept that it might not be merged.** Maintainers decline changes for reasons that have nothing to do with quality -- scope, maintenance cost, project direction. A rejection isn't a verdict on your work. You can always keep the change in your own fork.

## Etiquette in one paragraph

Be the contributor maintainers want more of: ask before building anything large, keep diffs small and conventional, write the description you'd want to receive, make CI green, and treat review as collaboration rather than combat. The technical mechanics of forking and rebasing are easy to learn; the social mechanics of being a low-friction contributor are what actually get your code merged.

## External references

- [GitHub: Contributing to a project](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project) -- the canonical fork-and-pull walkthrough
- [GitHub: About forks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks)
- [Open Source Guides: How to Contribute](https://opensource.guide/how-to-contribute/) -- maintained by GitHub, covering the social side in depth
- [How to write the perfect pull request](https://github.blog/2015-01-21-how-to-write-the-perfect-pull-request/) -- the GitHub team's own guidance
- [Pro Git: Contributing to a Project](https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project)
