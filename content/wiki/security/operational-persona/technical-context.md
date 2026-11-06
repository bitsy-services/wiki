---
title: "Persona Technical Context"
weight: 30
---

The technical context of an [operational persona](/wiki/security/operational-persona), a set of accounts, credentials, recovery methods and environment run as one identity, is the environment it acts from: the directory holding its repositories, the Git and SSH settings that apply there, the browser profile with its sessions, the tool logins on disk, the operating-system user and the network route. Context is bound to a persona when the environment picks the identity, so that acting as the persona takes no decision and acting as nobody fails.

[Identity separation](/wiki/security/identity-separation#how-identities-get-linked) sets up the first layer of this for `brinewick`, the pseudonym of a developer called Ines: an identity per directory and a key per host. Each layer above it is more work to run and separates more.

## Layers of separation

An agent in this table is the background process that holds unlocked SSH or GPG keys.

| Layer | Separates | Still shared |
| --- | --- | --- |
| Directory settings: `includeIf`, `~/.ssh/config`, [direnv](/wiki/security/pass#replace-env-files-with-direnv) | Commit identity, the SSH key offered, tool logins chosen by environment variable | Files, agents, the system credential store, browser, network route |
| Browser container, as in Firefox | Cookies, local storage, cache | History, bookmarks, saved passwords, [fingerprint](/wiki/security/operational-persona/isolation-failures/browser-and-device#fingerprints), [address](/wiki/security/operational-persona/isolation-failures/network-address) |
| Browser profile | Cookies, site data, history, bookmarks, saved passwords | Most of the fingerprint, address |
| Operating-system user | Home directory, agents, credential store, file permissions, the path in stack traces | Kernel, hardware, address |
| Virtual machine, as in Qubes OS | Operating system, applications, and the network route if it is given its own | Hardware, the host |
| Separate device | All of the above | The operator's location and habits |

The first three layers stop mistakes: a wrong commit address, a wrong key offered, a session open in the wrong window. They do little against a compromised process, which runs as the same user and can read every persona's key files and cookies. Microsoft's guidance for administrators states the general case: "An attacker who compromises a PC or device can impersonate or steal credentials/tokens for all accounts that use it, undermining many or all other security assurances." A persona that needs containment against malware on the machine, meaning a compromise elsewhere on it gives no control over this persona, starts at the operating-system user. One holding a key that moves funds or signs releases usually belongs in a virtual machine or on its own device.

For a pseudonym on a shared laptop, directory settings and a browser profile of its own are the default. A leaked password or key then stops at its persona, and the laptop itself is written down as an accepted exception in the inventory. Move up a layer when the stakes change.

Pointing `HOME` at another directory is not a layer. Git follows `HOME`, while `ssh` takes the home directory from the password database, so a shell with `HOME=~/hobby` still reads the real `~/.ssh/config`. A second operating-system user changes both.

## Fail closed

A context fails closed when acting outside any persona produces an error, and fails open when it produces a default identity. Git fails closed with no global identity and `user.useConfigOnly = true`: outside a persona's directory, `git commit` stops with `fatal: no email was given and auto-detection is disabled`. SSH fails closed with `IdentitiesOnly yes` under `Host *` and no key in a default-named file.

Most other tools fail open. `gh`, the [GitHub](/wiki/git/github) command line, [`gpg`](/wiki/security/gpg) and [`pass`](/wiki/security/pass) each take a directory from an environment variable, and each treats an empty value as if it were unset and falls back to a default location. `pass` says so in its source, `PREFIX="${PASSWORD_STORE_DIR:-$HOME/.password-store}"`, and `gh` and `gpg` behave the same way when run with `GH_CONFIG_DIR=` and `GNUPGHOME=`. A lookup that fails in a script, or a shell that never loaded the variable, acts as whoever is at the default.

Keep the defaults empty: no global Git identity, no `~/.ssh/id_ed25519`, nothing in `~/.config/gh`, `~/.gnupg` or `~/.password-store`. A fall-through then finds no identity to act as.

`gh` needs one more step. `gh auth login` stores its token in the system credential store when one exists, and that store is shared by every configuration directory. A directory with no configuration of its own can then read the last login's token: `gh auth status` reports no login while `gh auth token` prints the token. `gh auth login --insecure-storage` writes the token to `hosts.yml` in the persona's configuration directory instead, as plain text at mode 600, and that directory stays out of any repository.

## Selecting by directory

A persona's tool settings can move into its directory with one file, which direnv loads on entering the directory and unloads on leaving it:

```bash
# ~/hobby/.envrc
export GH_CONFIG_DIR="$HOME/hobby/.config/gh"
export GNUPGHOME="$HOME/hobby/.gnupg"
export PASSWORD_STORE_DIR="$HOME/hobby/.password-store"
export CLAUDE_CONFIG_DIR="$HOME/hobby/.claude"
export TZ=UTC
```

`CLAUDE_CONFIG_DIR` is the [configuration directory of Claude Code](/wiki/ai/claude-accounts/per-directory), a coding assistant. `TZ=UTC` makes Git record a `+0000` offset on each commit, for the reason under [what the context publishes](#what-the-context-publishes). Other tools have their own variable: `NPM_CONFIG_USERCONFIG` for npm, `AWS_SHARED_CREDENTIALS_FILE` for the AWS command line and `DOCKER_CONFIG` for Docker.

Create the GnuPG directory first with `mkdir -m 700 ~/hobby/.gnupg`. `gpg` stops with `directory does not exist` if it is missing, and warns if others can read it.

The file has gaps, and with the defaults empty most of them end in a refusal:

- direnv refuses a new or edited file until `direnv allow ~/hobby` runs again, and until then none of the variables are set.
- [In Bash the file loads at the next prompt](/wiki/ai/claude-accounts/per-directory#pitfalls), so `cd ~/hobby/project && git commit` runs before it and records the system's time zone.
- A repository with its own `.envrc` replaces this one unless its first line is `source_up`.
- Programs not started from that shell miss it: cron jobs, desktop applications, editor panels.
- An exported `GH_TOKEN` or `GITHUB_TOKEN` takes precedence over `GH_CONFIG_DIR`, so neither belongs in a shell profile.

One `ssh-agent` holding every persona's key is also a shared object. `IdentitiesOnly` limits what servers are offered, and any process that can reach the agent's socket can still ask for a signature from any key in it. `IdentityAgent` in a `Host` block points that host at the persona's own agent.

## What the context publishes

Some context leaves as data in what the persona produces. Git records the UTC offset of each commit from the time zone: `TZ=America/New_York` writes `-0500` in winter and `TZ=UTC` writes `+0000`. The hours themselves remain visible, and [they correlate](/wiki/security/operational-persona/isolation-failures/behavioural-correlation#hours). A stack trace prints the home directory, so a persona on its own operating-system user can publish `/home/brinewick` in place of `/home/ines`.

## Check

```bash
# from a directory outside every persona: each should refuse or find nothing
git var GIT_AUTHOR_IDENT                         # fatal: no email was given and auto-detection is disabled
gh auth token                                    # no oauth token found for github.com
ls ~/.ssh/id_* 2>/dev/null                       # no output
ssh -G example.com | grep -i '^identitiesonly'   # identitiesonly yes

# from a repository under the persona's directory: each should name the persona
git var GIT_AUTHOR_IDENT                         # brinewick <brinewick@brinewick.example> ...
gpg --version | grep -i '^home'                  # Home: /home/ines/hobby/.gnupg
gh auth status                                   # Logged in to github.com account brinewick
```

## Further reading

- [git-config: conditional includes](https://git-scm.com/docs/git-config#_conditional_includes) and [ssh_config(5)](https://man.openbsd.org/ssh_config), including `IdentityAgent`
- [GitHub CLI environment variables](https://cli.github.com/manual/gh_help_environment) and [`gh auth login`](https://cli.github.com/manual/gh_auth_login), for token storage
- Mozilla, [Firefox profiles](https://support.mozilla.org/en-US/kb/profile-manager-create-remove-switch-firefox-profiles) and [what containers do and do not separate](https://wiki.mozilla.org/Security/Contextual_Identity_Project/Containers)
- Google, [Manage Chrome with multiple profiles](https://support.google.com/chrome/answer/2364824)
- [Qubes OS introduction](https://doc.qubes-os.org/en/latest/introduction/intro.html)
- Microsoft, [Why are privileged access devices important](https://learn.microsoft.com/en-us/security/privileged-access-workstations/privileged-access-devices)
