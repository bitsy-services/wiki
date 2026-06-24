---
title: "Squash Merge"
weight: 10
---

A **squash merge** collapses every commit on a feature branch into a single new commit on the target branch. Instead of replaying the branch's history one commit at a time, Git combines all of the branch's changes into one diff and lands that as a lone commit. The original per-commit history of the branch is discarded from the target branch's record.

It is the workflow of choice when the branch's intermediate commits are noise -- "wip", "fix typo", "address review" -- and only the net change is worth keeping in the permanent history.

## Why squash

A short-lived feature branch usually accumulates commits that matter while you are working but not afterward. Squashing trades that granular, messy history for one clean, atomic commit:

- **Linear, readable `main` history.** Each merged feature is exactly one commit. `git log` on the target branch reads as a list of features, not a transcript of every keystroke.
- **Easy revert.** Backing out a feature is a single `git revert` of one commit, rather than unwinding a chain.
- **Bisect-friendly.** [`git bisect`](https://git-scm.com/docs/git-bisect) steps over whole features instead of half-finished intermediate states that may not even build.

The cost is that the branch's internal history is gone from `main`. If those intermediate commits carry real value -- a carefully staged refactor where each step is meaningful and independently reviewable -- prefer a regular merge or a rebase that preserves them.

## On the command line

Git's `--squash` flag stages the combined changes without creating the merge commit, leaving you to write a single fresh commit message:

```bash
git switch main
git pull                      # make sure main is current
git merge --squash feature/login
git commit                    # author one commit; the editor opens prefilled
```

`git merge --squash` differs from a normal merge in two ways: it records **no** second parent (the result is an ordinary commit, not a merge commit), and it does **not** advance the branch pointer automatically -- you commit yourself. Because there is no merge-parent link, Git will not consider `feature/login` "merged," so delete it explicitly once you are satisfied:

```bash
git branch -D feature/login
```

If you would rather keep the branch's commits but still flatten them, an interactive rebase (`git rebase -i`) lets you `squash` or `fixup` commits selectively before merging -- a finer-grained tool when only *some* of the history is noise.

## On GitHub

For pull requests, GitHub performs the squash for you. On the merge button, choose **"Squash and merge"** (rather than "Create a merge commit" or "Rebase and merge"). GitHub concatenates the PR's commit messages into the proposed message; edit it down to one clear description before confirming.

To make this the default and avoid accidental merge commits, a repository admin can restrict the allowed merge methods in **Settings -> General -> Pull Requests**, leaving only "Allow squash merging" enabled.

## Writing the squashed commit message

Because the squash discards the individual messages, the one message you write is the *only* record of the change. Make it carry its weight:

- A concise summary line (~50 characters) in the imperative mood: "Add OAuth login flow".
- A blank line, then a body explaining the *why* and any non-obvious decisions.
- A reference to the PR or issue it closes (`Closes #123`).

## Pitfalls

- **Lost authorship on collaborative branches.** A squash credits the whole change to whoever runs the squash (or to the PR author on GitHub). If multiple people contributed distinct commits, that attribution is flattened. Use a regular merge when preserving co-authorship matters, or add [`Co-authored-by:`](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors) trailers.
- **Re-merging a squashed branch causes conflicts.** After a squash, the source branch shares no merge link with the target. If you keep working on the old branch and merge again, Git re-presents already-merged changes as new and may conflict. The clean habit: delete the branch after squashing and cut a fresh one for follow-up work.
- **Squashing a shared/published branch rewrites nobody's history but confuses everyone's.** Squash short-lived branches that only you have pushed. Avoid squash-merging long-running branches that others have branched from.

## External references

- [Git docs: `git merge --squash`](https://git-scm.com/docs/git-merge#Documentation/git-merge.txt---squash)
- [GitHub docs: About merge methods -- squashing](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges#squash-and-merge-your-commits)
- [Pro Git: Rewriting History](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History) -- interactive rebase, the finer-grained alternative
