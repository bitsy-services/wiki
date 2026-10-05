---
title: "Identity Separation"
weight: 40
---

Identity separation is the practice of keeping two or more sets of accounts — a work identity and a pseudonym, say — so that nobody outside can show they belong to the same person. The property being kept is *unlinkability*: an observer who sees both identities cannot tell whether they are related.

That is a stronger property than having separate accounts. Separate logins limit the damage when one credential leaks. Unlinkability ends when a single identifier — an email address, a public key, a handle — appears on both sides, and nothing fails or warns when it does.

## How identities get linked

The examples use two invented identities on one laptop: `Ines Varga <ines@acme.example>` for work, and the pseudonym `brinewick` for a hobby project.

**Commit email.** [Git](/wiki/git) copies `user.name` and `user.email` from its configuration into every commit. Most machines have one global setting, so a commit in the hobby repository is authored by `Ines Varga <ines@acme.example>`, and anyone who clones the repository can read that with `git log`. GitHub also matches the address to an account and shows that account as the author. The separation is an identity per directory: one `includeIf "gitdir:~/hobby/"` section per identity in `~/.gitconfig`, each loading a file that holds that identity's name and address for every repository under its directory. Leaving the global identity unset and adding `user.useConfigOnly = true` makes git refuse to commit anywhere else, where it would otherwise guess an address from the login name and hostname.

**Default SSH key.** When `ssh` connects, it offers the server each public key held by its agent and each default key file (`~/.ssh/id_ed25519` and its siblings) until one is accepted. A server sees every key offered before the one it accepts, and a server that accepts none sees them all, the pseudonym's included. GitHub publishes each account's keys at `https://github.com/<username>.keys`, so a server that records what it was offered can match the keys against a crawl of those lists; `ssh whoami.filippo.io` is a public demonstration that tells visitors their GitHub username. The separation is one key per identity, stored under a filename `ssh` does not try by default, and a `~/.ssh/config` that names the key for each host:

```text
Host github-work
    HostName github.com
    IdentityFile ~/.ssh/work_ed25519

Host github-hobby
    HostName github.com
    IdentityFile ~/.ssh/hobby_ed25519

Host *
    IdentitiesOnly yes
```

`IdentitiesOnly yes` restricts the offer to the configured file, and under `Host *` it also covers servers with no entry of their own, which then receive no key. The two aliases exist because both accounts are on `github.com`; the hobby repository's remote becomes `git@github-hobby:brinewick/project.git`. A [GPG](/wiki/security/gpg) signing key shared between identities links them more directly, because its user ID carries a name and an email address.

**Reused handle.** A handle that appears on two sites is the first link an observer tests, because testing is free: Sherlock, an open-source tool, checks one username against more than 400 sites. If Ines once used `brinewick` on a forum profile that shows her name, the hobby account is linked on the day it is created. A derived handle (`brinewick-dev`) or a reused avatar image fails the same way. The separation is a handle and an image made for the pseudonym and used nowhere else.

**Metadata.** Most of it is values nobody typed. Each commit records the author's UTC offset beside its timestamp, such as `-0500`, which narrows the location and, across a history, shows the hours the author keeps. A pasted stack trace or log prints the home directory, `/home/ines/`. Photos and PDF files can carry the author's name, the device and the location in fields that viewers do not display. Prose is the hardest case: given enough text under both names, [stylometry](/wiki/cs/stylometry) can attribute both to one author from the rates of common words such as *upon* and *while*, which a writer does not consciously choose.

None of this needs the service's cooperation: it is visible to anyone who clones the repository, runs a server Ines connects to, or searches for the handle. The service itself sees more — the IP address of each login, the recovery email and phone number, a payment card — and no setting above changes that, which matters when the service is breached or served a legal demand.

## The case for

- **Audiences differ.** An employer, a client and a hobby forum each see what was published to them and nothing else.
- **Exposure stops at the pseudonym.** A pseudonym that cannot be traced to a legal name cannot be traced to an employer or a home address, so harassment of the account cannot follow its owner to either.

## The case against

- **Reputation does not transfer.** Commits, answers and writing under one name vouch for each other. A pseudonym starts with none of that, and what it earns cannot be claimed without ending the separation.
- **The cost recurs.** Every commit, upload and login is another chance to use the wrong identity, for as long as the separation matters.
- **Some services forbid it.** GitHub's terms say "One person or legal entity may maintain no more than one free Account", so a second free account for a pseudonym breaks them.

## One identity, deliberately

Using one name everywhere, on purpose, is the other coherent position. It gives up the ability to wall off a context and gets a record that accumulates in one place, with nothing to configure and no wrong key to offer. Its one requirement is that everything published under the name is something its owner is willing for every audience to read.

The costly position is the one in between that nobody chose: identities believed separate and already linked by one commit. Their owner writes under the pseudonym what they would not sign, while the link sits in a public repository.

## Cheap early, nearly impossible late

Before the first commit, separation costs a second email address, a second key and a few lines of configuration. After a link has been published, removing it means changing every copy, and most copies belong to someone else.

A commit's author line is part of the data its ID is computed from, so correcting the line gives that commit and [every commit descended from it](/wiki/cs/dag#where-dags-show-up) a new ID. Each clone and fork has to adopt the rewritten history, and the old history survives in every copy that does not, including in archives such as Software Heritage that copy public repositories without being asked. A link also has to be seen only once: deleting the evidence does not delete what an observer already learned.

The workable repair is to abandon the linked pseudonym and start another, kept separate from its first commit onward. The choice between separating and not has the same asymmetry: separate identities can be merged on any day by saying so, and a merged identity cannot be split.

## Check

Run these in a repository that is meant to belong to one identity, with the host from its remote in place of `github-hobby`.

```bash
# every author and committer identity in the history
git log --all --format='%an <%ae>%n%cn <%ce>' | sort -u

# what ssh will offer that host, read from the configuration without connecting
ssh -G github-hobby | grep -i '^identit'

# the account the host maps that key to
ssh -T git@github-hobby
```

The first should print one identity, plus `GitHub <noreply@github.com>` if anything was merged in the web interface. The second should print `identitiesonly yes` and a single `identityfile`, and the third should name the pseudonym's account.

## Further reading

- [RFC 6973 — Privacy Considerations for Internet Protocols](https://www.rfc-editor.org/rfc/rfc6973), whose terminology section defines unlinkability and pseudonymity
- [git-config: conditional includes](https://git-scm.com/docs/git-config#_conditional_includes) and [ssh_config(5)](https://man.openbsd.org/ssh_config#IdentitiesOnly), for the settings named above
- [GitHub Docs: Setting your commit email address](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address)
- Filippo Valsorda, [ssh whoami.filippo.io](https://words.filippo.io/whoami-updated/) (2023) — how the demonstration server matches offered keys to GitHub accounts
- [Sherlock](https://github.com/sherlock-project/sherlock) — the username search tool
- [GitHub Terms of Service](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service), section B.3, for the one-free-account rule
