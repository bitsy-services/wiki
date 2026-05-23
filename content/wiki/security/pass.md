---
title: "Secret Management with pass"
weight: 10
---

`pass` ([passwordstore.org](https://www.passwordstore.org/)) is a thin shell wrapper over [GPG](/wiki/security/gpg) and git. It is built for exactly the problem of secrets scattered across `.env` files, exported private keys, and API tokens pasted into notes: it pulls them into one encrypted, versioned, greppable tree on disk.

This guide covers one-time setup (including the WSL Ubuntu wrinkles), the daily workflow, migrating your existing secrets in, scripting against the store, and the [YubiKey](/wiki/security/yubikey) hardening path. It assumes you are comfortable on the command line.

## The mental model

There is very little to `pass`. Once you internalize the storage model, every command is obvious:

- Each secret is a **single GPG-encrypted file** under `~/.password-store`, named after its path in the tree — `api/openai.gpg`, `keys/eth/deployer.gpg`.
- The **directory tree is your namespace**. Folders are organizational, nothing more.
- By convention the **first line of a secret is the password/token itself**; any lines after it are freeform metadata (`username:`, `url:`, notes). Commands that copy "the secret" copy the first line.
- The whole store is a **git repository**. Every change is auto-committed, so you get history and can sync to a remote.

The one thing that is *not* encrypted is the tree itself — filenames and folder names are plaintext. Keep that in mind when naming things (see [Security notes](#security-notes-ordered-by-blast-radius)).

## One-time setup

### Install

```bash
sudo apt update
sudo apt install pass
```

This pulls in `gnupg` and `tree` as dependencies and installs shell completions for bash and zsh.

### Create a GPG key

`pass` encrypts to a GPG key, so you need one. If you don't already have a key (check with `gpg --list-secret-keys`), generate one:

```bash
gpg --full-generate-key
```

Choose **ECC (Curve 25519)** for a modern, fast key, or **RSA 4096** if you need broad compatibility. Set a **strong passphrase** — this passphrase is the last line of defense for every secret you are about to store. Pick a realistic expiry (you can always extend it later).

Then find the key's fingerprint:

```bash
gpg --list-secret-keys --keyid-format=long
```

The 40-character fingerprint on the `sec` line is what you'll hand to `pass`. (A fingerprint is more precise than an email address when you have multiple keys.)

### WSL: let GPG prompt you for the passphrase

WSL Ubuntu has no GUI by default, so GPG's default graphical passphrase prompt (`pinentry-gnome3`) fails with an `Inappropriate ioctl for device` error. Switch to the terminal pinentry:

```bash
sudo apt install pinentry-curses
```

Tell the GPG agent to use it — add to `~/.gnupg/gpg-agent.conf`:

```ini
pinentry-program /usr/bin/pinentry-curses
```

The curses/tty pinentry needs to know which terminal you're on, so add this to your shell profile (`~/.bashrc` or `~/.zshrc`):

```bash
export GPG_TTY=$(tty)
```

Then reload the agent:

```bash
gpg-connect-agent reloadagent /bye
```

From now on GPG will prompt for your passphrase inline in the terminal.

### Initialize the store

Point `pass` at your key:

```bash
pass init <YOUR-FINGERPRINT>
```

This creates `~/.password-store/` with a `.gpg-id` file recording which key the store encrypts to. (To store somewhere else, set `PASSWORD_STORE_DIR`.)

### Turn on git

```bash
pass git init
pass git remote add origin git@github.com:you/secret-store.git
```

`pass` auto-commits on every insert, edit, and removal, so your history is maintained for free. Push it with `pass git push`. The files are GPG-encrypted, so the remote only ever sees ciphertext — but a private repository is still the right call.

## Daily workflow

### Add a secret

A single-line secret (prompted, hidden, confirmed):

```bash
pass insert api/openai
```

A multiline secret — use this when a credential travels with metadata, like an AWS key with its key ID, region, and account:

```bash
pass insert -m aws/prod
```

Type the **token on the first line**, then metadata on the following lines, and finish with `Ctrl-D`. A typical multiline entry:

```text
AKIA...SECRETACCESSKEYVALUE
key_id: AKIAIOSFODNN7EXAMPLE
region: us-east-1
account: 1234-5678-9012
```

### Generate a strong secret

When you're creating a fresh credential rather than importing one:

```bash
pass generate github/token 40      # 40 characters
pass generate -n db/app-password 32 # -n = no symbols (for finicky inputs)
```

The default length is 25 (`PASSWORD_STORE_GENERATED_LENGTH`).

### Read a secret

```bash
pass api/openai     # print the whole entry to stdout
pass -c api/openai  # copy first line to the clipboard, auto-cleared after 45s
pass -c2 aws/prod   # copy line 2 instead (a metadata field)
```

`pass name` is shorthand for `pass show name`. The clip timeout is `PASSWORD_STORE_CLIP_TIME` (default 45 seconds).

### WSL: make the clipboard work

`pass -c` needs a clipboard backend. On **Windows 11 with WSLg** (the built-in GUI/Wayland layer), install the Wayland clipboard tools and it just works, syncing straight to the Windows clipboard:

```bash
sudo apt install wl-clipboard
```

Without WSLg, there's no clipboard for `pass -c` to reach; pipe to the Windows clipboard manually instead (note: no automatic clearing):

```bash
pass show api/openai | clip.exe
```

### Edit, organize, search

```bash
pass edit aws/prod      # decrypt to a tmpfs file, open $EDITOR, re-encrypt
pass                    # print the whole store as a tree
pass find aws           # list entry names matching "aws"
pass grep AKIA          # decrypt everything and grep the contents
pass mv api/openai api/openai-personal
pass cp api/openai api/openai-backup
pass rm -r aws/staging  # -r for a whole subtree
```

`pass edit` never writes plaintext to your normal filesystem — it uses a temporary file in RAM-backed storage and re-encrypts on save.

## Migrating your scattered secrets in

The point of all this is to consolidate. Here is how each common source maps in.

### `.env` files

For a single service, store the whole file as one multiline secret by piping it in:

```bash
pass insert -m env/myapp < .env
shred -u .env            # securely delete the plaintext original
```

If you'd rather have one secret per variable (handy for selective injection later), loop over the file:

```bash
while IFS='=' read -r key value; do
  [ -z "$key" ] && continue
  printf '%s\n' "$value" | pass insert -m "env/myapp/$key"
done < .env
shred -u .env
```

### Exported private keys

```bash
pass insert -m keys/eth/deployer < deployer.key
shred -u deployer.key
```

Once a fund-controlling key lives in `pass`, your GPG key indirectly guards those funds — this is the strongest argument for the [YubiKey path](#yubikey-the-hardening-path) below.

### Loose API tokens

The one-liners that were living in your shell history or a sticky note:

```bash
pass insert api/stripe
pass insert api/cloudflare
```

## Scripting integration

This is where consolidation pays off: secrets stop being files you copy around and become values you pull on demand.

### Inject into a single command

```bash
OPENAI_API_KEY=$(pass api/openai) ./run.sh
```

Command substitution strips the trailing newline, so for a single-line secret `$(pass name)` *is* exactly the value.

### Export several at once

A wrapper function keeps the secrets in the process environment and out of files:

```bash
with-secrets() {
  export OPENAI_API_KEY=$(pass api/openai)
  export STRIPE_KEY=$(pass api/stripe)
  exec "$@"
}

# usage: with-secrets ./deploy.sh
```

### Replace `.env` files with direnv

[direnv](https://direnv.net/) loads environment variables when you `cd` into a project and unloads them when you leave. Put the lookups in `.envrc` (commit it — it contains no secrets, only `pass` paths):

```bash
export OPENAI_API_KEY=$(pass api/openai)
export DATABASE_URL=$(pass env/myapp/DATABASE_URL)
```

Now the project's secrets are present in the shell exactly when you're working on it, and there is no plaintext `.env` on disk to leak or accidentally commit.

### When a tool insists on an actual file

Some tools only read an env file from a path. Prefer **process substitution** so the plaintext lives in a transient FIFO, never on disk:

```bash
some-tool --env-file <(pass show env/myapp)
```

Only fall back to writing a real file (`pass show env/myapp > .env`) when a tool can't accept a path like that — and `shred -u .env` the moment it's done.

### Don't leak what you just protected

- **Never pass a secret as a command-line argument.** Argv is visible to every process via `ps` and lands in your shell history. Use environment injection or stdin.
- Prefix a one-off command with a space (with `HISTCONTROL=ignorespace` set) to keep it out of history entirely.

## Security notes (ordered by blast radius)

1. **Your GPG private key is the key to everything.** If it leaks, *every* secret in the store — including any exported private keys or seed phrases — is exposed at once. Guard it with a strong passphrase and move it to hardware (next section). This is the single point of catastrophic failure.
2. **Plaintext on disk defeats the whole system.** Avoid materializing `.env` files; use environment injection or process substitution. When you must write one, `shred -u` it immediately.
3. **Filenames and the tree are not encrypted.** `keys/eth/deployer` is readable by anyone who can see the store directory or its git remote. Never encode a secret into a path or filename.
4. **Clipboard residue.** `pass -c` clears after `PASSWORD_STORE_CLIP_TIME`, but clipboard-history managers may retain a copy regardless.

## YubiKey: the hardening path

Once your secrets live in `pass`, the GPG key is the crown jewel — and right now it's a file on your laptop. Moving it onto a [YubiKey](/wiki/security/yubikey) means the private key never sits on disk and decryption requires the physical device:

- **Move the encryption subkey onto the card** with `gpg --edit-key` → `keytocard` (or generate keys on-card from the start). Afterwards `~/.gnupg` holds only a stub that points at the card.
- **Require a touch per decryption:** `ykman openpgp keys set-touch enc on`. Now every `pass show` triggers a deliberate tap, so malware can't silently read the store even while the key is plugged in.

**WSL caveat:** WSL2 has no native USB support, so a YubiKey isn't visible to GPG inside the distro out of the box. Either forward the device with [usbipd-win](https://github.com/dorssel/usbipd-win), or run `gpg`/`scdaemon` on the Windows side (Gpg4win) and bridge the agent into WSL. This is the roughest edge of `pass` on WSL; if it fights you, running the smartcard side on Windows is the common workaround.

## Backup and recovery

The store is just files plus git, so backup is `pass git push` to a private remote. But the encrypted files are useless without the GPG key, so **back up the key separately** — a printed paper copy in a safe, or simply the fact that it now lives on a YubiKey. Losing the GPG key means losing every secret in the store, permanently.
