---
title: "Git on WSL Ubuntu 26.04"
weight: 2
---

A new Ubuntu 26.04 under the [Windows Subsystem for Linux](/wiki/microsoft/wsl) (WSL), Microsoft's way of running Linux distributions on Windows, comes with Git 2.53 installed and nothing else Git needs to work with GitHub: no name or email for commits, no key, and no GitHub command-line tool. Two PowerShell commands install the distribution, and one bash script fills in the rest. Afterwards there is a Linux user named `claude` and one SSH key, which GitHub accepts both for pushes and for verifying commit signatures. Git's global configuration commits as the GitHub account and signs every commit with that key.

The script stops for the `sudo` password, a passphrase for the new key (typed twice), the same passphrase once more to load the key, and a press of Enter before the GitHub sign-in, which finishes in a browser on Windows. Every step is safe to repeat, so after a failure the script can be run again without duplicating anything.

The examples use the Linux user name `claude`. The script itself does not depend on it: it reads the user from `$USER` and `$HOME`.

## Before you start

- Windows 11, or Windows 10 version 2004 (build 19041) or later, which `wsl --install` requires.
- A GitHub account, signed in to a browser on Windows.
- WSL itself. In PowerShell, `wsl --version` prints the version numbers of WSL, its kernel and Windows when it is installed. If it does not, open PowerShell with *Run as administrator*, install the WSL components alone, and restart Windows:

```powershell
wsl --install --no-distribution
```

## Install Ubuntu 26.04

In PowerShell:

```powershell
wsl --update
wsl --install -d Ubuntu-26.04
```

`Ubuntu-26.04` is the name `wsl --list --online` gives the image. The plain `Ubuntu` entry in that list carries no version number, so naming the release pins it.

The first launch runs Ubuntu's provisioning script, `/usr/lib/wsl/wsl-setup`, which asks three questions:

1. `Create a default Unix user account:` arrives with the Windows user name filled in, lower-cased. Erase it and type `claude`. The script accepts lowercase letters, digits, `_` and `-`, starting with a letter or `_`.
2. A password, twice, from `adduser`. It becomes the password `sudo` asks for, and nothing on this page stores it.
3. `Would you like to opt-in to platform metrics collection (Y/n)?` is Ubuntu Insights, which sends Canonical anonymous reports about the system. The answer is prefilled with `y`, and `n` declines. The answer is saved in the Windows registry, and later Ubuntu installs read it from there instead of asking.

The provisioning script adds `claude` to the `sudo` group and writes `default=claude` under `[user]` in `/etc/wsl.conf`, which is what makes every later session log in as `claude`. The prompt then reads `claude@<computer-name>:~$`: WSL gives the distribution the Windows computer name as its hostname. `wsl -d Ubuntu-26.04` opens it again later, and `wsl --set-default Ubuntu-26.04` makes it the one a bare `wsl` opens.

## Run the script

Inside Ubuntu, create the file, paste the script below into it, and run it with `bash`:

```bash
nano ~/setup-github.sh     # paste, then Ctrl+O, Enter, Ctrl+X
bash ~/setup-github.sh
```

Run it as a file instead of pasting the lines into the prompt. The script sets `set -e`, which ends the shell at the first failed command, and pasted into the prompt, that shell is the terminal. It also refuses to start under `sudo` or without a terminal. Under `sudo` it would set up root's home instead of `claude`'s, and with no terminal to ask in, `ssh-keygen` quietly creates a key without a passphrase.

```bash
#!/usr/bin/env bash
# Git and GitHub on a fresh WSL Ubuntu 26.04. Safe to run again.
set -euo pipefail

KEY="$HOME/.ssh/id_ed25519"
TITLE="$USER@$(hostname) WSL Ubuntu 26.04"
# SHA-256 of GitHub's apt signing keyring, from cli/cli docs/install_linux.md
GH_KEYRING_SHA256=6084d5d7bd8e288441e0e94fc6275570895da18e6751f70f057485dc2d1a811b
SCOPES=admin:public_key,admin:ssh_signing_key

step() { printf '\n==> %s\n' "$*"; }
die() { printf '%s\n' "$*" >&2; exit 1; }

[ "$(id -u)" -ne 0 ] || die "Run this as your own user, without sudo."
[ -t 0 ] || die "Run this in a terminal: bash ~/setup-github.sh"
[ -n "${XDG_RUNTIME_DIR:-}" ] || die "XDG_RUNTIME_DIR is not set; run this from a normal WSL terminal."

step "Updating Ubuntu"
sudo apt-get update
sudo apt-get full-upgrade -y

step "Installing git, the SSH client and the GitHub CLI"
if [ ! -f /etc/apt/sources.list.d/github-cli.list ]; then
  keyring=$(mktemp)
  curl -fsSL -o "$keyring" https://cli.github.com/packages/githubcli-archive-keyring.gpg
  echo "$GH_KEYRING_SHA256  $keyring" | sha256sum --check --quiet
  sudo install -D -m 644 "$keyring" /etc/apt/keyrings/githubcli-archive-keyring.gpg
  rm -f "$keyring"
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" |
    sudo tee /etc/apt/sources.list.d/github-cli.list >/dev/null
  sudo apt-get update
fi
sudo apt-get install -y git openssh-client gh

step "Creating an SSH key"
if [ ! -f "$KEY" ]; then
  ssh-keygen -t ed25519 -C "$TITLE" -f "$KEY"
fi

step "Pointing every shell at Ubuntu's ssh-agent"
agent_block='
# >>> ssh-agent >>>
# Ubuntu runs an agent per user, started by systemd on first use, but WSL
# shells are not told where it listens. The first terminal after the
# distribution starts loads the key, asking for its passphrase if it has one.
export SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/openssh_agent"
[ -t 0 ] && { ssh-add -T ~/.ssh/id_ed25519.pub 2>/dev/null || ssh-add ~/.ssh/id_ed25519; }
# <<< ssh-agent <<<'
grep -qF '# >>> ssh-agent >>>' ~/.bashrc || printf '%s\n' "$agent_block" >>~/.bashrc
eval "$agent_block" || die "The key was not loaded into the agent. Run the script again and type its passphrase."

step "Signing in to GitHub"
if ! gh auth status --hostname github.com >/dev/null 2>&1; then
  gh auth login --hostname github.com --git-protocol ssh --web --skip-ssh-key --scopes "$SCOPES"
else
  # An earlier plain `gh auth login` lacks the two scopes the key uploads need.
  granted=$(gh api --include / 2>/dev/null | grep -i '^x-oauth-scopes:' || true)
  if [[ $granted != *admin:public_key* || $granted != *admin:ssh_signing_key* ]]; then
    gh auth refresh --hostname github.com --scopes "$SCOPES"
  fi
fi

step "Trusting github.com's SSH host keys"
ssh-keygen -R github.com >/dev/null 2>&1 || true
gh api meta --jq '.ssh_keys[] | "github.com " + .' >>~/.ssh/known_hosts

step "Adding the key to GitHub, for sign-in and for signing commits"
gh ssh-key add "$KEY.pub" --type authentication --title "$TITLE"
gh ssh-key add "$KEY.pub" --type signing --title "$TITLE"

step "Configuring git"
id=$(gh api user --jq .id)
login=$(gh api user --jq .login)
name=$(gh api user --jq '.name // ""')
[ -n "$name" ] || name=$login
email="$id+$login@users.noreply.github.com"
git config --global user.name "$name"
git config --global user.email "$email"
git config --global init.defaultBranch main
git config --global pull.rebase true
git config --global push.autoSetupRemote true
git config --global gpg.format ssh
git config --global user.signingkey "$KEY.pub"
git config --global commit.gpgsign true
signer="$email namespaces=\"git\" $(cut -d' ' -f1-2 "$KEY.pub")"
grep -qxF "$signer" ~/.ssh/allowed_signers 2>/dev/null || printf '%s\n' "$signer" >>~/.ssh/allowed_signers
git config --global gpg.ssh.allowedSignersFile ~/.ssh/allowed_signers

step "Checking"
scratch=$(mktemp -d)
git -C "$scratch" init -q
git -C "$scratch" commit -q --allow-empty -m "signing test"
signature=$(git -C "$scratch" log -1 --format='%G? %GS')
rm -rf "$scratch"
echo "test commit signature: $signature"
[ "${signature%% *}" = G ] || die "The test commit's signature did not verify."
reply=$(ssh -o ConnectTimeout=15 -T git@github.com 2>&1) || true
echo "$reply"
grep -qF "successfully authenticated" <<<"$reply" || die "SSH sign-in to GitHub failed."

step "Done: git commits as $name <$email>, signed, and pushes over SSH"
echo "Open a new terminal (or run: source ~/.bashrc) so it can reach the ssh-agent."
```

### What it asks for

1. **The `sudo` password**, the one set at the username prompt.
2. **A passphrase for the new key**, twice. Pressing Enter both times creates a key without one; [the passphrase and the agent](#the-passphrase-and-the-agent) covers what each choice costs.
3. **The passphrase again**, when `ssh-add` loads the key into the agent. A key without a passphrase loads without asking. Pressing Enter here stops the script with a message saying the key was not loaded, Ctrl+C stops it outright, and a rerun asks again.
4. **Enter**, for the GitHub sign-in. `gh` 2.103.2 printed this on 26.04:

```text
! Did you know that expiring tokens can be requested with --expiring? Read more at https://gh.io/gh-expiring-tokens

! One-time code (XXXX-XXXX) copied to clipboard
Press Enter to open https://github.com/login/device in your browser...
! Failed opening a web browser at https://github.com/login/device
  exec: "xdg-open,x-www-browser,www-browser,wslview": executable file not found in $PATH
  Please try entering the URL in your browser manually
```

The failure is expected. `gh` opens a browser through the first of `xdg-open`, `x-www-browser`, `www-browser` and `wslview` it finds, a fresh Ubuntu 26.04 has none of them, and the `wslu` package that used to supply `wslview` is not in the 26.04 archive. The code does reach Windows: `gh` copies it by default, and its clipboard library falls back to `clip.exe`, the Windows clipboard tool, which WSL makes runnable from Linux. Open <https://github.com/login/device> in a browser on Windows, paste the code, and authorize *GitHub CLI*. From there `gh` polls GitHub until the authorization arrives, and the script carries on by itself, ending with these lines:

```text
==> Done: git commits as Your Name <12345678+your-login@users.noreply.github.com>, signed, and pushes over SSH
Open a new terminal (or run: source ~/.bashrc) so it can reach the ssh-agent.
```

The second line is there because terminals that were open when the script ran, including the one it ran in, do not know where the agent is, so with a passphrase-protected key every commit and push in them asks for it again.

## What the script does

The script was run on 23 October 2026 in a throwaway Ubuntu 26.04 distribution: from a clean install, again on top of its own result, and through its guards and recovery paths. Those were no terminal, `sudo`, Enter at the passphrase prompt, a sign-in without the key scopes, and an `ssh -T` that GitHub refused. The calls that need a real GitHub account were stubbed: the sign-in, the key uploads, the profile lookup and the final `ssh -T`. What `gh` and GitHub do at those steps comes from `gh`'s source and GitHub's documentation.

### SSH rather than Git Credential Manager

Microsoft's own guide to Git on WSL takes a different route: Git Credential Manager, installed with Git for Windows, which keeps an HTTPS token in the Windows Credential Manager and shares it with Git on the Windows side. That holds for HTTPS remotes only: the guide itself says Git Credential Manager "only works with HTTP(S) remotes". It also notes that, by default, the Windows copy reads Git for Windows' configuration rather than the distribution's. Without Git for Windows, Git Credential Manager can be installed inside WSL instead, but it then runs as a Linux program and cannot use Windows' credential storage. SSH needs nothing installed on Windows beyond WSL, and the same key signs the commits.

### The GitHub CLI comes from GitHub's repository

Ubuntu 26.04's own archive carries `gh` 2.46.0, released in March 2024. GitHub's repository installed 2.103.2 when this script was tested in October 2026. The script follows GitHub's instructions for Debian and Ubuntu with one addition: before apt trusts the downloaded signing keyring, `sha256sum --check` compares it with the checksum GitHub publishes alongside those instructions, so a substituted file stops the script. A key rotation stops it too, and the fix is the new checksum from the same page, `docs/install_linux.md` in the `cli/cli` repository.

### One SSH key, registered twice

The key is Ed25519, at `~/.ssh/id_ed25519`. That is one of the file names `ssh` tries without being told, so no `~/.ssh/config` is needed.

GitHub keeps two lists of keys for each account. A key on the authentication list lets `git push` and `git fetch` over SSH act as the account. A key on the signing list makes GitHub mark commits signed with it as *Verified*, when the commit's email address is a verified address on the account or the account's no-reply address, which GitHub's signing instructions suggest for keeping the real one private. The same key can sit on both lists: GitHub's documentation says "you can even upload your existing authentication key" as a signing key. `gh ssh-key add --type` picks the list. It checks the list first and reports `Public key already exists on your account` instead of failing, which is what makes the step safe to repeat.

On the Git side, `gpg.format ssh` switches signing from [GPG](/wiki/security/gpg) to `ssh-keygen -Y sign`. GPG is the older way to sign commits, and it has expiry and revocation, which SSH keys do not. `user.signingkey` names the public key, and `commit.gpgsign` signs every commit without `-S`. Tags are left alone. `tag.gpgsign` would turn every `git tag NAME` into a signed annotated tag that opens an editor for its message, so a signed tag is made on purpose, with `git tag -s`. `~/.ssh/allowed_signers` maps the email address to the key, and `gpg.ssh.allowedSignersFile` tells Git where it is. Git 2.53 needs both to check a signature locally. With the setting but no file, `git log --show-signature` reports a good signature without saying whose, beside `Unable to open allowed keys file`. With no setting at all, Git refuses to check, printing `gpg.ssh.allowedSignersFile needs to be configured and exist for ssh signature verification` and `No signature`. The script's final check reads the same status, so it fails in either case.

### The passphrase and the agent

`ssh-keygen` asks for a passphrase and accepts an empty one. The difference is what the key file is worth on its own. Without a passphrase, the file is the credential: any process running as `claude` can copy it and push as the GitHub account from another machine. With one, a copy of the file is useless without the passphrase. That protects the key and not the account: the same process can read the `gh` token the script leaves in plain text, which can push over HTTPS and, until its key scopes are dropped, register a key of its own ([signing in, and the token it leaves](#signing-in-and-the-token-it-leaves)). In return for the passphrase, something has to hold the unlocked key, or every commit and push asks for it again. On 26.04, a key without a passphrase signs commits with no agent running. A key with one, with no agent and no terminal to ask in, fails with `incorrect passphrase supplied to decrypt private key`.

Ubuntu 26.04 already runs that something. Its `openssh-client` package installs `ssh-agent.socket`, a systemd user socket at `$XDG_RUNTIME_DIR/openssh_agent` (`/run/user/1000/openssh_agent` for the first user), which starts `ssh-agent` on the first connection. The socket unit announces that address only to systemd's own environment, through `systemctl --user set-environment`. A WSL shell never learns it, and `ssh-add` there reports `Could not open a connection to your authentication agent`. The block the script appends to `~/.bashrc` supplies the address and, in a shell with a terminal, loads the key unless the agent already holds it:

```bash
export SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/openssh_agent"
[ -t 0 ] && { ssh-add -T ~/.ssh/id_ed25519.pub 2>/dev/null || ssh-add ~/.ssh/id_ed25519; }
```

`ssh-add -T` asks the agent to sign with this particular key, where `ssh-add -l` would be satisfied by any key at all. The `[ -t 0 ]` test keeps a shell without a terminal, such as `bash -i` reading commands from a pipe, from having its input consumed as passphrase attempts. In a new terminal, Enter at the prompt skips loading the key. Ctrl+C skips it too, but also skips the rest of `~/.bashrc` for that terminal.

The first terminal after the distribution starts asks for the passphrase, and later terminals find the key loaded and ask nothing. The key stays loaded until the distribution stops, at `wsl --shutdown` or `wsl --terminate`, or when WSL shuts down a distribution with nothing open in it. In testing, a terminal opened a few seconds after the last one closed found the key loaded. One opened less than half a minute later found the distribution restarted, and asked again.

Ubuntu's `~/.bashrc` returns early in a shell that is not interactive. A program started some other way, such as a `wsl.exe -e` command or a systemd service, has no `SSH_AUTH_SOCK`, and with a passphrase-protected key, its commits fail to sign. A tool like that needs `SSH_AUTH_SOCK` set to the same path, or a key without a passphrase.

### GitHub's host keys come from GitHub's API

The first `ssh` to a host it has not seen before stops to show the host key's fingerprint and asks whether to trust it. The script skips that question. It writes GitHub's keys into `~/.ssh/known_hosts` from `https://api.github.com/meta`, the endpoint GitHub's fingerprints page points to. The list arrives over HTTPS, so the trust rests on GitHub's TLS certificate rather than on the first connection. Every run first removes any existing `github.com` entries with `ssh-keygen -R`, so an outdated entry in a `~/.ssh` copied from another machine cannot outlive a key GitHub has replaced.

### Signing in, and the token it leaves

`gh auth login --web` uses GitHub's device flow: `gh` shows a code, the browser enters it, and GitHub hands `gh` an OAuth token. `--git-protocol ssh` makes `gh` use SSH addresses for the repositories it clones. `--skip-ssh-key` stops `gh` offering to make and upload a key of its own, since the script does that itself. `--scopes` adds `admin:public_key` and `admin:ssh_signing_key` to the default scopes (`repo`, `read:org` and `gist`), because adding keys to the two lists needs them. When `gh` is already signed in, the script reads the scopes the token carries from the `X-OAuth-Scopes` header of an API response, and runs `gh auth refresh` if either key scope is missing. Without that check, a token from an earlier plain `gh auth login` fails at the key upload.

`gh` stores the token in the system credential store when there is one. A fresh WSL install has none: nothing on the session bus answers to `org.freedesktop.secrets`. So `gh` prints `Authentication credentials saved in plain text` and writes the token to `~/.config/gh/hosts.yml`. Anything that reads that file can do what the scopes allow: full access to every repository the account can reach, and adding SSH keys to the account. Once the keys are on GitHub, the two key scopes can be dropped, at the cost of one more visit to the browser:

```bash
gh auth refresh --hostname github.com --remove-scopes admin:public_key,admin:ssh_signing_key
```

A later run of the script finds them missing and asks for them again, through the same browser step.

### The Git configuration

`user.name` is the name on the GitHub profile, or the login when the profile has none. `user.email` is the account's ID-based no-reply address, `<ID>+<login>@users.noreply.github.com`, built from the account ID and login that `gh api user` returns. Commits made with it are attributed to the account, the real address stays out of every clone's history, and, unlike the older `<login>@users.noreply.github.com` form, the attribution survives a change of username. Accounts that turned on email privacy before 18 July 2017 were given the older form, and GitHub's email reference says that turning *Keep my email address private* off and on again issues the ID-based one. On an account that old, do that before relying on the address the script writes: the script's own check verifies the signature locally and cannot tell whether GitHub recognizes the address. A rerun of the script sets the name and address again from the profile, replacing any edit made since. This sets up exactly one identity. Keeping two apart on one machine, with an identity per directory and a key per host, is covered in [identity separation](/wiki/security/identity-separation).

Three more settings change Git's behaviour where an unconfigured 2.53 stops or guesses:

- `init.defaultBranch main`. Unconfigured, `git init` names the first branch `master` and prints a hint that the default becomes `main` in Git 3.0. GitHub names a new repository's default branch `main`.
- `pull.rebase true`. Unconfigured, `git pull` on a branch that has diverged from its upstream stops with `fatal: Need to specify how to reconcile divergent branches.` With it, the pull replays the local commits on top of the fetched ones, which is the preference [contributing to open source](/wiki/git/contributing-to-open-source#keep-your-branch-current) states for keeping a branch current.
- `push.autoSetupRemote true`. Unconfigured, the first `git push` of a new branch fails with `The current branch topic has no upstream branch`. With it, that push creates the branch on GitHub and tracks it.

## Check

```bash
gh auth status
ssh -T git@github.com
git config --global --list
```

`ssh -T` prints `Hi <login>! You've successfully authenticated, but GitHub does not provide shell access.` and exits with status 1 even then, because GitHub opens no shell. On a network that blocks port 22, it times out or is refused instead (the script gives up after 15 seconds). GitHub also accepts SSH on port 443 at `ssh.github.com`, which its documentation covers under *Using SSH over the HTTPS port*. That is a different host name, checked against a separate `[ssh.github.com]:443` entry that the script does not write, so the first connection there asks about the host key; GitHub's fingerprints page lists the values to compare. In any repository, `git log --show-signature -1` on a new commit shows `Good "git" signature for <ID>+<login>@users.noreply.github.com with ED25519 key SHA256:...`. After a push, GitHub shows the same commit as *Verified*. `ssh-keygen -lf ~/.ssh/id_ed25519.pub` prints the fingerprint to compare against both lists at <https://github.com/settings/keys>.

## Where repositories go

Keep repositories under `/home/claude`, not under `/mnt/c`. Microsoft's guidance is to store files in the Linux file system when working from a Linux command line, because access across the two file systems is slower. Windows reaches the same files at `\\wsl.localhost\Ubuntu-26.04\home\claude`, and `explorer.exe .` opens the current directory in File Explorer. Windows and Linux use different line endings by default, so a repository checked out by Git for Windows and then used from WSL can show every file as modified. Keeping each repository on one side avoids that.

## Starting over

Remove the key from both lists at <https://github.com/settings/keys>. The `gh` token stays valid on GitHub even after its file is gone, and `gh auth logout` does not change that, since it only deletes the local copy. Revoking means opening *GitHub CLI* at <https://github.com/settings/applications> and choosing *Revoke Access*, which revokes every token `gh` has been issued, on every machine. Then, from PowerShell:

```powershell
wsl --unregister Ubuntu-26.04
```

Unregistering deletes the distribution's whole file system, the private key included, and cannot be undone.

## Further reading

WSL itself has [a short page under Microsoft](/wiki/microsoft/wsl). This one sits under Git because what it configures is Git's identity and its access to GitHub, and WSL is where that runs.

- Microsoft, [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install) and [basic commands](https://learn.microsoft.com/en-us/windows/wsl/basic-commands)
- Microsoft, [Get started using Git on WSL](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-git), the Git Credential Manager route
- GitHub CLI, [Installing gh on Linux](https://github.com/cli/cli/blob/trunk/docs/install_linux.md), with the keyring checksums
- GitHub Docs, [About commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification) and [GitHub's SSH key fingerprints](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints)
- GitHub Docs, [Using SSH over the HTTPS port](https://docs.github.com/en/authentication/troubleshooting-ssh/using-ssh-over-the-https-port)
- GitHub Docs, [email addresses reference](https://docs.github.com/en/account-and-profile/reference/email-addresses-reference), on the no-reply address
- Git, [`gpg.ssh.allowedSignersFile`](https://git-scm.com/docs/git-config#Documentation/git-config.txt-gpgsshallowedSignersFile) in `git-config`
