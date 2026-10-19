---
title: "Squashing Commits"
weight: 5
---

Squashing replaces a run of commits with a single commit. A Git commit stores a snapshot of every file, an author, a message, and a link to the commit it was made on top of, called its parent; a merge commit has two parents. The replacement takes the snapshot of the run's last commit and the parent of its first, so the files end up exactly as they were, while the intermediate snapshots, their messages and their separate authors leave the history.

Squashing happens in two places. On a branch nobody else has fetched, an interactive rebase rewrites the branch so that several commits become one, usually to fold corrections into the commit they correct. When a branch lands, a squash merge writes the branch's combined change onto the target branch as one new commit, and leaves the branch's own commits where they were.

Either way the result is a new commit with a new ID. Git treats a branch as merged when its tip can be reached by following parent links back from the target, and the new commit has no link to the commits it replaced. After a squash merge, Git therefore still reports the branch as unmerged, further work on the branch can conflict with its own earlier changes, and a branch built on top of it replays commits whose changes the target already has.

## How to squash

### On a branch

`git rebase -i main` opens an editor on a list of the branch's commits since it left `main`, oldest first. Each line is a command, initially `pick`, followed by a commit's ID and subject. When the editor closes, Git carries out the list from top to bottom, building each commit afresh on top of `main`.

Three commands squash. `squash` melds a commit into the previous one in the list and opens an editor holding both messages. `fixup` melds it and keeps only the previous commit's message, and `fixup -C`, added in Git 2.32, keeps only the melded commit's message. In all three cases the result keeps the author of the commit melded into.

Corrections can be marked as such when they are committed, which leaves the list nothing to edit. `git commit --fixup=<commit>` records a correction whose subject is `fixup!` followed by the target's subject, and `git rebase -i --autosquash main` moves each such commit under its target and marks it `fixup`. For four commits, two of them corrections, autosquash writes this list, and the rebase leaves two commits:

```text
pick 55ce1d4 Parse the config file
fixup d8ed96e fixup! Parse the config file
pick 3a730b0 Validate config keys
fixup 8b51b40 fixup! Validate config keys
```

From Git 2.50, each subject in the list is prefixed with `#`. Setting `rebase.autoSquash` to `true` makes `--autosquash` the default for interactive rebases.

Collapsing a whole branch into one commit needs no list:

```bash
git reset --soft $(git merge-base HEAD main)
git commit
```

`git merge-base HEAD main` prints the most recent commit the branch and `main` share. `reset --soft` moves the branch back to that commit and leaves every file, and the staged changes, as they were, so the next commit records the branch's whole change, along with anything that was already staged.

### When a branch lands

`git merge --squash feature` works out the result a merge of `feature` would have, stages it, and stops without committing. The `git commit` that follows makes an ordinary commit with one parent, the target's previous tip. Its author is whoever runs the commit, and the editor opens on a message that lists every squashed commit with its author.

Code-hosting services, called forges, run the same operation on the server. On GitHub a branch usually lands through a [pull request](/wiki/git/contributing-to-open-source), the page that proposes the merge and holds its review, and *Squash and merge* makes the person who opened it the author, crediting every commit author in it as a co-author. GitLab calls the same page a merge request, and its squash option records the merge request's creator as the author. It also adds a merge commit on top of the squash, unless the project uses fast-forward merges, which move the target branch up to the new commit instead of adding one. [Squash Merge](/wiki/git/squash-merge) covers the commands, the forge settings and the message.

## What the graph records

Git's history is a [directed acyclic graph](/wiki/cs/dag), a graph whose links all point one way and never form a loop: every commit links to its parents, and following those links from a branch's tip reaches everything the branch contains. A commit reachable that way is an *ancestor* of the tip, and Git counts a branch as merged into `main` when the branch's tip is an ancestor of `main`.

```text
before          A---B           main
                     \
                      C---D---E   feature

merge commit    A---B-----------M   main
                     \         /
                      C---D---E     feature

squash merge    A---B---S       main
                     \
                      C---D---E   feature
```

M and S hold the same snapshot. M has two parents, B and E, so C, D and E are ancestors of `main`. S has one parent, B, so they are not, and Git's commands report exactly that:

- `git branch -d feature` refuses with `error: the branch 'feature' is not fully merged`, so deleting it takes `-D`, which skips the check. A branch pushed with `git push -u` is checked instead against its *upstream*, the clone's copy of the remote branch, `origin/feature`. If every commit was pushed, `-d` then deletes the branch with the warning `not yet merged to HEAD`. That copy outlives the branch on the server until `git fetch --prune` removes it, and after that `-d` refuses again.
- `git log main..feature`, which lists the commits reachable from `feature` but not from `main`, still lists C, D and E.
- `git cherry` recognises a commit by a hash of its diff, called its *patch ID*, which ignores line numbers and whitespace but covers the unchanged lines shown around each change. It can match a squashed branch only if the branch was a single commit, because the diff of S is the combined change of every commit on the branch.
- The *merge base* of `main` and `feature`, the most recent commit both contain, is still B.

Nothing in the graph records that S came from `feature`. Only the message of S can say so, and the pull request page if a forge made the merge.

## Continuing on a squashed branch

A merge compares each side with the merge base. Where only one side changed a region, the merge takes that side's version; where both changed it the same way, it takes the change once; where they changed it differently, it stops with a conflict.

After a squash merge the merge base is still B, so the next merge of `feature` compares a `main` holding the changes from C, D and E inside S with a `feature` holding them as C, D and E. Lines nobody has touched since merge cleanly, and C, D and E join the history of `main` beside S, so the same change is recorded twice. A line that C, D or E changed and a new commit on `feature` changes again is a conflict: `main` has the first version, `feature` the second, and B the original. A second squash merge uses the same merge base and stops on the same lines.

The same lines conflict in the other direction. If someone edits one of them on `main` and `feature` then merges `main` in, `feature` has the version from C, D or E, `main` has the newer one, and B has the original.

A long-lived branch can meet these conflicts on every round: a `develop` branch merged into `main` at each release, a release branch merged back, a fork pulling from the project it forked. Such a branch should land with a merge commit, which makes the branch's tip an ancestor of the target, moves the merge base forward, and leaves the next round only what is new. GitHub's documentation says squash merging "works best for short-lived branches", and GitLab's says "You should not squash and merge long-running branches."

Where a long-lived branch is squash-merged anyway, GitLab's documentation gives two ways to keep it in step: after each merge, rebase the branch onto the target, or merge the target back into it. Either makes the squash commit an ancestor of the branch, so the next merge compares only what came after it. The merge rewrites nothing, which matters on a branch other people work on. A plain `git rebase main` replays the squashed commits and stops at each one that changed a line which a later squashed commit changed again, because `main` holds only the last version; the `--onto` form below replays only the commits made after the squash.

Follow-up work on a squash-merged branch belongs on a new branch from the updated `main`. Commits already made on the old branch move across with `--onto`, given the commit the branch pointed to when it was squash-merged. That is the newest commit the pull request contained or, if the default message of a local `git merge --squash` was kept, the first commit it names, since it lists them newest first. List what will move before rebasing, because naming a later commit silently drops every follow-up commit up to and including it:

```bash
git log --oneline <last-squashed-commit>..feature
git rebase --onto main <last-squashed-commit> feature
```

The rebase replays the commits on `feature` that come after `<last-squashed-commit>` onto `main`, and nothing before it.

## Stacked branches

A branch made from another branch that has not landed yet, so that it carries that branch's commits as well as its own, is *stacked* on it. Stacking lets a second change go into review while the first is still open.

When the lower branch is squash-merged, `git rebase main` on the upper branch replays every commit that `main` cannot reach, and those include the lower branch's originals. A plain rebase drops a replayed commit whose change `main` already has (an interactive one stops at each and asks), and a lower branch of a single commit can be skipped before it is replayed at all, when its patch ID matches the squash commit's. The commits that stop the rebase are intermediate states: a commit that changed a line which a later commit on the lower branch changed again. `main` has the later version, the replayed commit the earlier one, and the rebase reports a conflict over a change that has already landed.

Replaying only the upper branch's own commits avoids all of it:

```bash
git rebase --onto main feature-a feature-b
```

This replays the commits on `feature-b` that are not on `feature-a` onto `main`. It needs `feature-a` to still point at the lower branch's last commit; if the branch has been deleted, the ID of that commit, the newest one its pull request contained, works in its place.

On GitHub, deleting the lower branch after its merge retargets the upper pull request to `main`. The retargeted pull request still lists the lower branch's commits, because a pull request shows everything after the merge base, and the merge base has not moved. GitHub's native stacked pull requests, generally available on github.com since October 2026, rebase the next pull request onto the base automatically after each merge.

## Squash, merge commit or rebase

There are three ways to land a branch, and forges offer all three as buttons. A merge commit keeps the branch's commits as they are and adds a commit with two parents. A rebase replays the branch's commits onto the target's tip as copies with new IDs, so the target stays a single line. A squash merge writes one new commit. The difference shows in the commands that read history afterwards.

| | Merge commit | Rebase | Squash merge |
|---|---|---|---|
| `git log` on `main` | every commit, plus a merge per branch | every commit, in one line | one commit per branch |
| `git blame` on a line | the commit that wrote it, with its message | the commit that wrote it, with its message | the branch's one commit and message |
| `git bisect` finds | the commit that introduced the bug, if every commit builds; with `--first-parent`, the merge | the commit that introduced the bug, if every commit builds | the branch's one commit |
| Backing a branch out | `git revert -m 1` on the merge | a revert of each commit | `git revert` on the commit |
| Authors | each commit keeps its own | each commit keeps its own | one per branch; GitHub adds co-authors |

The first parent of a merge commit is the previous tip of the branch that was checked out when the merge was made, so on `main` the chain of first parents steps from one landed branch to the next. On a history of merge commits, `git log --first-parent` lists one merge per landed branch, the same view a squashed history gives, and `git bisect --first-parent`, from Git 2.29, tests only those merges; the branch's own commits stay underneath for a finer search. The view depends on each branch being merged into `main`, as a forge's merge button does, rather than `main` being fast-forwarded onto a branch: the `git log` manual says first-parent history "makes sense only when following a strict policy of merging all topic branches when staying on a single integration branch".

GitHub's documentation offers squash merging as a way "to create a more streamlined Git history". That holds for the plain `git log` most tools display; on a history of merge commits, `--first-parent` gives the same view without discarding anything.

Reverting a merge commit, with `-m 1` naming the first parent as the side to return to, undoes the branch's changes, but the branch's commits are still ancestors of `main`. The `git revert` manual puts it as "Reverting a merge commit declares that you will never want the tree changes brought in by the merge." Merging the fixed branch later brings in only the commits made since. It conflicts where a fix edits a line the revert restored, and the rest of the branch stays reverted with nothing to flag it. Git's how-to on reverting a faulty merge gives two ways back: revert the revert before merging the fixed branch, or rebuild the branch with new commits, which `git rebase --no-ff` does, and merge the rebuilt branch as it is. A reverted squash commit leaves no such link behind, and squash-merging the fixed branch lands all of it.

A rebase leaves the branch merged only when the branch itself is moved onto the copies and `main` fast-forwarded to it, as a local rebase followed by `git merge --ff-only` does. GitHub's *Rebase and merge* puts new commits on `main` and leaves the branch where it was, so Git reports it unmerged. A copy keeps the original's patch ID only if `main` had not changed the lines around it, so `git cherry` can list a commit that has landed as missing; `git rebase` drops such a commit anyway, because replaying it changes nothing.

## When to squash

History on `main` is read long after it is written: `git blame` to find out why a line exists, `git bisect` to find which change broke something, `git revert` to back one out. All three work in whole commits. Blame on a line from a commit called `wip` explains nothing, bisect cannot test a commit that does not build, and reverting one commit of a series can leave the rest broken. The unit that serves all three is the logical change: one purpose, a snapshot that builds and passes its tests, and a message that says why. Whether to squash comes down to whether a branch's commits already are such changes.

Projects that review every commit make this a rule. Git's own contribution guidelines say "Make separate commits for logically separate changes". The Linux kernel's guidelines ask contributors to "Separate each logical change into a separate patch" and to make sure the kernel "builds and runs properly after each patch in the series", because a `git bisect` can stop at any of them. GitHub's documentation draws the line in the same place for pull requests: squash "when a pull request represents one logical change", and use a merge commit "when the individual commits in a pull request are meaningful on their own".

**Squash:**

- **A commit that corrects another commit on the same branch.** A typo, a failing test, an addressed review comment: fold it into the commit it corrects with `fixup`, which keeps that commit's message and author.
- **A pull request that is one change, with commits that record how it was written.** `wip`, `try again` and `address review` describe the process rather than the result. A squash merge lands the result as one commit with one message, which a GitHub repository can set to default to the pull request's title and description.
- **Where the project asks for it.** Some projects squash every pull request, and some ask contributors to squash before review. [Contributing to someone else's project](/wiki/git/contributing-to-open-source) means following its convention.

**Don't squash:**

- **Commits that are separate changes.** A refactor that changes no behaviour, followed by the change that relies on it, is two commits a reviewer can check one at a time and a bisect can tell apart. Squashed, a one-line behaviour change sits in a diff of every file the refactor touched, and reverting it reverts the refactor too.
- **A branch that lives on after it lands.** `develop`, release branches and upstream syncs take merge commits, for the reasons under [continuing on a squashed branch](#continuing-on-a-squashed-branch).
- **Commits someone else has built on.** Squashing rewrites them, so each person with a copy holds two versions of the same work, and the `git rebase` manual says that rewriting a branch others have based work on "is a bad idea: anyone downstream of it is forced to manually fix their history." A `git pull` that merges brings the originals back beside the squashed commit. A `git pull --rebase` replays only that person's own commits, provided their clone had fetched the branch before it was rewritten; the rebase uses the clone's record of where the remote branch used to point.
- **A branch several people wrote, where the record of who wrote what matters.** A squash merge records one author for the whole branch. GitHub credits the others as co-authors, but `git blame` attributes every line to the one commit. Folding fixups into their targets keeps each commit, and each commit's author.

Between the two lists sits the habit that projects reviewing commit by commit ask for: fold the corrections into the commits they correct, then land the series with a merge commit or a rebase, so each commit survives.

A repository that allows only squash merges gives up landing a branch as several commits, and in return each pull request lands as one commit. Nobody has to tidy their commits, and the pull request page keeps the discussion. That suits small, single-purpose pull requests; a change that should land as a series has to become a series of pull requests instead, often [stacked](#stacked-branches). The setting governs only how pull requests are merged. For every commit on `main` to be one reviewed pull request, branch protection also has to require an approved pull request for every change and apply to admins as well, which a classic branch protection rule does not do by default.

## Squashing during review

Squashing rewrites commits, so a branch squashed while under review has to be force-pushed, and the new commits replace the ones reviewers have read. Committing each correction with `--fixup`, aimed at the commit it corrects, keeps it visible as a commit of its own, and the folding waits until the branch is approved:

```bash
# during review: each correction names the commit it corrects
git commit --fixup=3a730b0
git push

# after approval: fold the corrections in, then replace the remote branch
git rebase -i --autosquash main
git push --force-with-lease --force-if-includes
```

`--force-with-lease` overwrites the remote branch only if it still points where this clone last saw it, so commits someone else pushed in the meantime are not silently discarded. A fetch that runs in the background, from a scheduled job for example, updates that record and defeats the check. `--force-if-includes`, added in Git 2.30, closes the gap by also requiring that the local branch has at some point contained the remote branch's current tip. On a repository that squash-merges, the second step is unnecessary, because the merge folds the corrections in with everything else.

## Undoing a squash

A squash creates new commits, and the old ones stay in the repository until garbage collection removes them. The reflog, Git's local record of where each branch has pointed, keeps them reachable for 30 days by default, and the branch's own reflog is the dependable way back.

`git reflog feature` lists the branch's past positions, newest first, each named `feature@{n}`. A rebase squash writes an entry `rebase (finish)`, and the tip before the squash is the entry just below it. The `reset --soft` recipe under [On a branch](#on-a-branch) writes `reset: moving to`, which points at the merge base, and then a `commit` directly above that; the tip before the squash is the entry just below `reset: moving to`.

Which command returns the branch to that entry depends on what has happened since. If no commits have been made on the branch since the squash, and nothing was staged when the recipe ran, a reset with `feature` checked out does it:

```bash
git reflog feature
git reset --keep <tip-before-squash>
```

`--keep` leaves uncommitted changes in place, and refuses to run if a file it would have to change has some, which can happen when the rebase also moved the branch onto a newer `main`. A refusal moves nothing, and running `git stash` before the reset and `git stash pop` after it gets past one; a pop that conflicts keeps the stash until it is dropped by hand. From another branch, `git branch -f feature <tip-before-squash>` moves the branch without touching any files.

With commits made since the squash, either command would drop them from the branch and from the files. Replay them onto the old tip instead, with `<squash-commit>` the `rebase (finish)` entry or the recipe's `commit` directly above `reset: moving to`. Before running the rebase, check that the `git log` line lists exactly the commits made since the squash:

```bash
git log --oneline <squash-commit>..feature
git rebase --onto <tip-before-squash> <squash-commit> feature
```

Anything that was staged when the recipe ran went into its commit and exists nowhere else, so the reset and the replay both leave it behind. `git reset --soft <tip-before-squash>` in place of `--keep` keeps it staged, and `git diff <tip-before-squash> <squash-commit>` shows what it was.

If the squash was already pushed, the remote branch still holds it after the undo. A plain `git push` is rejected, and replacing the remote branch takes the same `git push --force-with-lease --force-if-includes` as any rewrite. A `git pull` brings the squash back instead: a merging pull records the change twice, beside a merge commit, and a rebasing pull drops the restored commits again without an error.

`ORIG_HEAD` is a shortcut while the squash is still the last command Git ran: a rebase or a reset leaves it naming the branch's tip from before, so `git reset --keep ORIG_HEAD` then does the same as the reset above. There is one `ORIG_HEAD`, not one per branch, though, and every merge, pull, rebase, reset and stash rewrites it, on whichever branch it runs. After any of those, the same reset sends the branch somewhere else, or nowhere, without an error.

A squash merge leaves the branch alone, so its commits remain on it until it is deleted. GitHub also keeps a reference to each pull request's commits, which `git fetch origin pull/<number>/head:<branch>` retrieves into a local branch. Undoing the merge on a `main` that others have pulled is a `git revert` of the squash commit, not a reset. On a `main` nobody else has, `git reset --keep ORIG_HEAD` straight after the commit removes it, since `git merge --squash` sets `ORIG_HEAD` too.

## Check

Run these with the branch in question in place of `feature`. After a forge has made the merge, run `git fetch` first and put `origin/main` in place of `main`, since the local `main` lacks the squash commit until it is updated.

```bash
# commits on the branch that main cannot reach; a squash-merged
# branch still lists every one of them
git log --oneline main..feature

# the snapshot a merge of feature into main would produce, and main's own
git merge-tree --write-tree main feature
git rev-parse 'main^{tree}'
```

When the last two print the same ID, merging `feature` would change nothing, so `main` already has all of its changes and `git branch -D feature` loses no work. Different IDs mean the branch has changes `main` lacks, or that `main` has since edited some of the same lines, in which case `merge-tree` also reports a conflict and exits with status 1. `git merge-tree --write-tree` needs Git 2.38 or later.

## Further reading

- [git-rebase](https://git-scm.com/docs/git-rebase): the interactive commands, `--autosquash` and `--onto`, and a section on recovering from a rebase of a branch someone else had already fetched
- [git-merge](https://git-scm.com/docs/git-merge): `--squash`
- [git-commit](https://git-scm.com/docs/git-commit): `--fixup` and `--squash`
- [How to revert a faulty merge](https://github.com/git/git/blob/master/Documentation/howto/revert-a-faulty-merge.adoc): why a reverted merge stays reverted when the branch is merged again
- [Linux kernel: Submitting patches](https://docs.kernel.org/process/submitting-patches.html#separate-your-changes), section *Separate your changes*
- [GitHub Docs: Pull request merges](https://docs.github.com/en/pull-requests/reference/pull-request-merges): the three merge methods, the default squash message, and long-running branches
- [GitLab Docs: Squash and merge](https://docs.gitlab.com/user/project/merge_requests/squash_and_merge/): the extra merge commit, and the squash commit's author and committer
- [Pro Git: Rewriting History](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History)
