---
title: "Which Credential Claude Code Uses"
weight: 30
---

[Claude Code](/wiki/ai/context-engineering/claude-code) can hold several credentials at once: the claude.ai login that `/login` saves, a Claude Console API key, a long-lived subscription token, a script that prints a key, and a cloud provider's credentials. Each request carries one of them, chosen by a fixed order of precedence. Environment variables rank above the saved login, so an API key exported in a shell profile can decide which account pays while a subscription is signed in: an interactive session uses it once the user approves it, and `claude -p`, the non-interactive mode that runs one prompt and exits, uses it without asking.

## Where each credential is kept

| Credential | Created by | Kept in |
| --- | --- | --- |
| claude.ai login, for Pro, Max, Team and Enterprise | `/login` in a session, or `claude auth login` | `.credentials.json` in the configuration directory on Linux and Windows; on macOS, a Keychain entry keyed to the configuration directory |
| Console API key | `/login`, choosing the Console account and *Create an API key* | The configuration directory, with the login credentials |
| Console sign-in without a key | `/login`, choosing *Sign in with your Console account* | An Anthropic profile in `~/.config/anthropic` (`%APPDATA%\Anthropic` on Windows) |
| Long-lived subscription token | `claude setup-token`, which prints the token once and saves it nowhere | Wherever it is pasted; Claude Code reads it from `CLAUDE_CODE_OAUTH_TOKEN` |
| API key from the environment | Copied from the Console | `ANTHROPIC_API_KEY` |
| Gateway token | An organization's gateway | `ANTHROPIC_AUTH_TOKEN`, sent as a bearer token |
| Key-printing script | The `apiKeyHelper` setting | The script's own source, such as a password store |
| Cloud provider | The provider's tools | `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX` or `CLAUDE_CODE_USE_FOUNDRY`, plus the provider's own credentials |

On macOS, Claude Code writes the login to `.credentials.json` instead when the Keychain refuses the write, as it does when locked during an SSH session.

Only the first two rows live inside the configuration directory, the folder that `CLAUDE_CONFIG_DIR` selects, and those are the logins that [one directory per account](/wiki/ai/claude-accounts/config-directories) keeps apart. A Console sign-in without a key is written to a profile outside it, the one `ANTHROPIC_PROFILE` names or else the active or `default` profile, so two such sign-ins made from two directories with no `ANTHROPIC_PROFILE` set land in the same profile. That sign-in has a wider side effect as well: in the documentation's words, "Claude Code signs you out of any claude.ai login stored on the machine." The rest come from environment variables and settings files: a variable reaches every directory used from the shell that exported it, and a setting reaches every directory that reads the file it is in.

## The order of precedence

When more than one credential is present, Claude Code uses the first of these that is set:

1. Cloud provider credentials, when `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX` or `CLAUDE_CODE_USE_FOUNDRY` is set.
2. `ANTHROPIC_AUTH_TOKEN`.
3. `ANTHROPIC_API_KEY`.
4. The output of the `apiKeyHelper` script.
5. `CLAUDE_CODE_OAUTH_TOKEN`.
6. An Anthropic profile named by `ANTHROPIC_PROFILE`, or Workload Identity Federation credentials, which let a cloud workload exchange its own identity token for Anthropic access.
7. The subscription login saved by `/login`.

A session signed in to a Claude apps gateway, which is Anthropic's gateway software that an organization runs itself and that signs developers in through the organization's identity provider, overrides the whole list. The login that Pro, Max, Team and Enterprise users rely on comes last, so each credential above it in the list takes priority over it once present, and an exported API key once approved in an interactive session.

## An exported API key

`ANTHROPIC_API_KEY` outranks every saved login. In an interactive session, Claude Code asks once whether to use the key and records the answer in the configuration directory, so a second directory asks again. The *Use custom API key* toggle in `/config`, shown only while the variable is set, changes the answer later. A `claude -p` run uses the key whenever it is present, without asking.

From then on the key's account is billed per token, which Anthropic's support article on the variable says happens "even if you're logged into Claude Code with a claude.ai subscription or a different Console account." A key exported in `~/.bashrc` for some other program reaches every terminal: each directory's interactive sessions are offered it, and every `claude -p` run started from such a shell is billed to it without a prompt.

`unset ANTHROPIC_API_KEY` returns the current shell to the subscription. A key that one account needs can live in that account's settings as an `apiKeyHelper` command, where the other directories never see it; [One config directory per account](/wiki/ai/claude-accounts/config-directories#add-an-api-key-account) shows the setup.

Other credentials also survive a `/login`:

- `CLAUDE_CODE_OAUTH_TOKEN`: `/login` switches the running session to the new login, but each new session reads the variable again until it is removed from the shell profile or settings.
- `apiKeyHelper`: a helper named in a settings file outranks `/login` for as long as the setting is present.
- A cloud-provider switch: a stale `CLAUDE_CODE_USE_VERTEX`, exported by a profile that cannot be edited, is cancelled by setting it to an empty string in a settings file's `env` block, which Claude Code treats as unset when choosing a provider.

## What each credential can do

| Credential | Limits |
| --- | --- |
| Long-lived subscription token | Needs a Pro, Max, Team or Enterprise plan; valid for one year; makes model requests only, so Remote Control (driving a local session from a phone or browser) and claude.ai connectors (integrations attached to a claude.ai account) do not work; not read in `--bare` mode, the scripted mode that skips hooks, plugins and instruction files |
| API key, `apiKeyHelper` or gateway token | Billed per token with no allowance and no wrap-up allowance; not used by the Claude desktop app or by cloud sessions (Claude Code sessions that run on Anthropic's infrastructure), which authenticate with the claude.ai login |
| Anthropic profile | claude.ai connectors and `/schedule` routines unavailable while it is selected |
| Any credential, in `--bare` mode | No OAuth credential or keychain is read: the Anthropic API needs `ANTHROPIC_API_KEY` or an `apiKeyHelper` passed in `--settings`, and cloud providers read their own credentials as usual |
| claude.ai login | Expires: Claude Code warns three days ahead with `Your login expires in 3 days · run /login to renew`, and an expired login stops unattended sessions until someone signs in again |

Cloud sessions always use the subscription, even when `ANTHROPIC_API_KEY` is set in their environment.

## Check

Run these in the shell a session would start from, with the same `CLAUDE_CONFIG_DIR`:

```bash
# JSON: authMethod, configDirectory, and apiKeySource when a key is involved;
# exits 0 when a credential is available, 1 when none is
claude auth status

# which variable supplies each credential, and which one is not in use
claude auth status --text
```

`authMethod` is one of `none`, `claude.ai`, `oauth_token`, `api_key`, `api_key_helper` and `third_party`. With an exported key and a credential that ranks below it, the answer depends on how the command is run. Tested with Claude Code 2.1.310 and a key exported beside `CLAUDE_CODE_OAUTH_TOKEN`: run in a terminal, it answered for an interactive session, reporting `oauth_token` until the key was approved in that directory and `api_key` afterwards; captured by a script with no terminal, it reported `api_key` whether or not the key had been approved, which is the credential a `claude -p` run uses. The JSON does not separate the two token variables: `authMethod` reads `oauth_token` for a gateway token in `ANTHROPIC_AUTH_TOKEN` and for a long-lived token in `CLAUDE_CODE_OAUTH_TOKEN` alike. The `--text` form names the variable, and with both set, version 2.1.310 printed `Auth token: ANTHROPIC_AUTH_TOKEN`, as the order of precedence predicts. Inside a session, `/status` shows the account, organization and email in use, and when a login and an API key are both configured it marks the one that is not in use.

## Related

- [One config directory per account](/wiki/ai/claude-accounts/config-directories): keeping logins apart, and giving one account an API key without exposing it to the others.
- [Plans and usage limits](/wiki/ai/claude-accounts/plans-and-limits): what each kind of credential is billed against.
- [Loops in Claude Code](/wiki/ai/loop-engineering/claude-code#claude--p-any-program-can-be-the-loop): `claude -p` and `--bare`, where an exported key is used without asking.
- [Secret management with pass](/wiki/security/pass): a store for the keys an `apiKeyHelper` prints.

## Further reading

- Anthropic, [Authentication](https://code.claude.com/docs/en/authentication): credential storage, precedence and long-lived tokens
- Anthropic, [Manage API key environment variables in Claude Code](https://support.claude.com/en/articles/12304248-manage-api-key-environment-variables-in-claude-code)
- Anthropic, [CLI reference](https://code.claude.com/docs/en/cli-reference) for `claude auth` and `claude setup-token`
- Anthropic, [Environment variables](https://code.claude.com/docs/en/env-vars)
