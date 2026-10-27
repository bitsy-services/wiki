---
title: "One Config Directory per Account"
weight: 40
---

A [Claude Code](/wiki/ai/context-engineering/claude-code) configuration directory holds one account's login together with everything Claude Code keeps for that account: settings, personal instructions, skills, plugins, Model Context Protocol (MCP) servers, prompt history and session transcripts. The default is `~/.claude`, with a global config file beside it at `~/.claude.json`. Setting the `CLAUDE_CONFIG_DIR` environment variable before `claude` starts points all of it, global config file included, at another directory. Two directories behave as two independent installations of the same program, each signed in to its own account, and Anthropic's documentation recommends this for staying signed in to a work account and a personal one at once.

## What a directory holds

| In the directory | Contents |
| --- | --- |
| `.credentials.json`, or on macOS a Keychain entry keyed to the directory | The login |
| `.claude.json` | Account details, user-scope MCP servers, and each project's trust and history |
| `settings.json` | Permissions, hooks, environment variables, model, status line, `apiKeyHelper` |
| `CLAUDE.md`, `rules/` | Personal instructions loaded in every project |
| `skills/`, `agents/`, `commands/` | Personal skills, subagents and commands |
| `plugins/` | Installed plugins |
| `projects/` | Session transcripts, which `--resume` reads, and auto memory |
| `history.jsonl` | Typed prompts, for up-arrow recall |
| `stats-cache.json` | The totals `/usage` shows |

The default directory differs from the others in one respect. With the variable unset, the global config file sits beside the directory, at `~/.claude.json`; with the variable set, it moves inside, to `$CLAUDE_CONFIG_DIR/.claude.json`. `CLAUDE_CONFIG_DIR=~/.claude` is therefore not the default: run that way, Claude Code 2.1.310 created and used `~/.claude/.claude.json`, a new file, in place of the existing `~/.claude.json` with its account details, MCP servers and project trust. The default account is the one started with the variable unset.

An empty value is not the default either. With `CLAUDE_CONFIG_DIR=` set to an empty string, the same version reported an empty `configDirectory` and used the current directory as its configuration directory: started in a repository, it took the `apiKeyHelper` from a `settings.json` at the repository's root as if it were a user setting, and wrote a `backups/` folder into the working tree. Removing the variable restores the default; emptying it does not.

## Add a subscription account

One alias per extra account, in `~/.bashrc` or `~/.zshrc`, is the form Anthropic's documentation gives:

```bash
alias claude-work='CLAUDE_CONFIG_DIR=~/.claude-work claude'
```

In a new terminal, the first `claude-work` runs first-launch setup for the empty directory, login included, and `claude` carries on with the default account. To sign in without starting a session, run the login on its own; `--email` fills in the address on the sign-in page:

```bash
CLAUDE_CONFIG_DIR=~/.claude-work claude auth login --email you@work.example
```

The sign-in finishes in a browser. When one claude.ai login belongs to more than one organization, such as a personal plan and an employer's Team plan, Anthropic's instructions have the user select the plan on the authorization page, and that choice decides which allowance the directory draws on.

## Add an API-key account

An account billed to a Console workspace, the group of API keys within a Claude Console organization that carries its own spend limits, gets its own directory, with the key supplied by a command in that directory's `settings.json` so that it never enters a shell profile. Here the key is stored in [pass](/wiki/security/pass#scripting-integration), a password store built on GPG:

```json
{
  "apiKeyHelper": "pass show anthropic/acme-claude-code"
}
```

saved as `~/.claude-acme/settings.json`, with an alias like the one above:

```bash
alias claude-acme='CLAUDE_CONFIG_DIR=~/.claude-acme claude'
```

Claude Code runs the `apiKeyHelper` command through `/bin/sh`, sends what it prints as the key, and caches the value for five minutes before running it again. The helper outranks any login saved in the same directory, and no other directory reads this `settings.json`.

The keyless Console sign-in is the wrong tool here. Choosing *Sign in with your Console account* at `/login` stores the result outside the directory, in an Anthropic profile, and in the documentation's words "Claude Code signs you out of any claude.ai login stored on the machine". The older *Create an API key* route stores the key with the directory's other credentials and stays per directory.

## Pick the account by project directory

A shell function named `claude` can choose the directory from the current path, so that every session started under `~/work` uses the work account without a separate command:

```bash
claude() {
  if [ -z "${CLAUDE_CONFIG_DIR:-}" ]; then
    case "$PWD/" in
      "$HOME/work/"*)
        CLAUDE_CONFIG_DIR="$HOME/.claude-work" command claude "$@"
        return ;;
      "$HOME/clients/acme/"*)
        CLAUDE_CONFIG_DIR="$HOME/.claude-acme" command claude "$@"
        return ;;
    esac
    env -u CLAUDE_CONFIG_DIR claude "$@"
    return
  fi
  command claude "$@"
}
```

A non-empty `CLAUDE_CONFIG_DIR` already set, by an alias or by hand, wins, so `claude-work` still works anywhere. An empty one counts as unset, and outside the listed paths `env -u` removes the variable before the real program starts, which keeps the default account on its own `~/.claude.json` and away from the empty-value behaviour above. The slash appended to `$PWD` stops `~/workshop` from matching `~/work`. `command claude` and `env` both run the real program, not the function, and the function returns that program's exit status. It was tested in Bash 5.3 and in dash, under `set -u` and with a space in `$HOME`, against a stand-in `claude` that printed its environment.

The function only acts on `claude` typed in a shell that has loaded it. The editor extensions, the desktop app, scripts, cron jobs and a work repository cloned outside `~/work` all start on the default account; [Work and personal](/wiki/ai/claude-accounts/layouts#work-and-personal) covers the settings that reach sessions started those ways.

## Share instructions and skills between accounts

Each directory starts empty, while much of a person's configuration belongs in every account. Personal instructions can be shared by importing one `CLAUDE.md` from the others. A user-scope `CLAUDE.md` loads its imports without asking, so `~/.claude-work/CLAUDE.md` can begin with the default account's file and add what is specific to the account:

```text
@~/.claude/CLAUDE.md

Open pull requests against the team's main branch only.
```

Skills can be shared by linking each skill's folder, since Claude Code follows a symlinked skill folder and loads it once even when several locations point at it:

```bash
mkdir -p ~/.claude-work/skills
for skill in ~/.claude/skills/*/; do
  [ -d "$skill" ] || continue
  name=$(basename "$skill")
  [ -e ~/.claude-work/skills/"$name" ] || ln -s "${skill%/}" ~/.claude-work/skills/"$name"
done
```

The `[ -d ]` test skips the unexpanded pattern when there are no skills yet, and the `[ -e ]` test skips skills already linked, so running the loop again links only the skills added since. It was tested in Bash and dash, including a skill whose name contains a space.

Settings are better kept separate. Most of what differs between accounts lives in `settings.json`: the status line label below, an `apiKeyHelper`, and `env` entries. User-scope MCP servers live in each directory's `.claude.json`, so a server added with `claude mcp add -s user` in one account is missing from the others until it is added there too, and plugins are installed per directory in the same way.

## Label each session with its account

A status line is a command Claude Code runs when a session starts and again as new messages arrive, passing it a JSON description of the session on standard input and showing what it prints in a bar at the bottom of the screen. For Pro and Max subscribers the JSON includes `rate_limits`, the percentage used of the five-hour and weekly limits, from the session's first response onward. This script prints the account's name, the model and both percentages:

```python
#!/usr/bin/env python3
# Status line for one Claude Code account: its label, the model, and plan usage.
import json
import sys
import time

data = json.load(sys.stdin)
parts = [sys.argv[1] if len(sys.argv) > 1 else "default",
         data.get("model", {}).get("display_name", "?")]

limits = data.get("rate_limits") or {}
five = limits.get("five_hour") or {}
if five.get("used_percentage") is not None:
    text = f"5h {five['used_percentage']:.0f}%"
    if five.get("resets_at"):
        text += time.strftime(" until %H:%M", time.localtime(five["resets_at"]))
    parts.append(text)
week = limits.get("seven_day") or {}
if week.get("used_percentage") is not None:
    parts.append(f"week {week['used_percentage']:.0f}%")

print(" | ".join(parts))
```

Saved as `~/.local/bin/claude-statusline` and made executable, it is named in each account's `settings.json` with that account's label, here `~/.claude/settings.json` for the personal default:

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.local/bin/claude-statusline personal"
  }
}
```

and `~/.claude-work/settings.json` with `work` in its place. A personal session on a Max plan then shows `personal | Opus 5.5 | 5h 24% until 16:00 | week 41%`. Team and Enterprise seats and API-key accounts get no `rate_limits`, so their sessions show only the label and the model. The script was tested against sample session JSON with full, partial and missing `rate_limits`.

## Editors, the desktop app and background sessions

The VS Code extension takes the directory from its `claudeCode.environmentVariables` setting, which needs an absolute path because the extension does not expand `~`:

```json
{
  "claudeCode.environmentVariables": [
    { "name": "CLAUDE_CONFIG_DIR", "value": "/home/you/.claude-work" }
  ]
}
```

The extension declares that setting with machine scope, which VS Code allows only in user settings or in a remote's settings, never in a workspace's. One set of user settings therefore runs one account, and a remote window, such as a WSL distribution or an SSH host, has settings of its own and can run another; aliases still work in the integrated terminal. VS Code profiles each keep their own user settings and can be tied to a folder, which should allow one profile per account, but that was not tested here. The editor integrations write their connection lock files under `ide/` inside the configuration directory, and a terminal session reads them from its own, so `/ide` from a session on a different account from the editor's looks in the wrong place.

The Claude desktop app reads `CLAUDE_CONFIG_DIR` from the places it reads other environment variables for development servers, and needs to be quit and reopened after a change. Background sessions in agent view run under a supervisor per configuration directory, each with its own list of sessions.

## What a directory does not separate

Anything in the repository loads for every account: the project's `.claude/settings.json`, `.claude/settings.local.json`, `.mcp.json` and `CLAUDE.md`. Credentials in the environment, such as `ANTHROPIC_API_KEY`, `CLAUDE_CODE_OAUTH_TOKEN` and the cloud-provider switches, apply in whichever directory is in use and outrank its saved login; [Which credential Claude Code uses](/wiki/ai/claude-accounts/credentials) gives the order. A Console sign-in made without an API key is stored outside the directory, in an Anthropic profile, a credential file under `~/.config/anthropic`, and making one signs out every claude.ai login on the machine.

Conversations stay with the account that held them. Transcripts are kept under `projects/` in the directory where they were recorded, so `claude --resume` lists only that account's sessions, and work that moves to another account starts a new conversation there. `/login` within one directory replaces the login and keeps the history, because the directory has not changed.

## Check

For each directory, confirm which credential it holds and that the right account is behind it:

```bash
# the default account: the real program, past the function, with the variable unset
env -u CLAUDE_CONFIG_DIR claude auth status --text

# every other account
for dir in ~/.claude-work ~/.claude-acme; do
  CLAUDE_CONFIG_DIR="$dir" claude auth status
done
```

The JSON form names the `configDirectory` in use and the `authMethod`, which is `claude.ai` for a subscription login and `api_key_helper` for a directory with a helper. Inside a session, `/status` shows the email and organization the login belongs to.

## Related

- [Which credential Claude Code uses](/wiki/ai/claude-accounts/credentials): the precedence order that environment credentials follow into every directory.
- [Account layouts](/wiki/ai/claude-accounts/layouts): which directories to create for which arrangement of accounts.
- [Identity separation](/wiki/security/identity-separation): the same per-directory pattern applied to git identities and SSH keys.
- [Claude Code](/wiki/ai/context-engineering/claude-code): what `CLAUDE.md`, skills and hooks do once loaded.

## Further reading

- Anthropic, [Authentication: log in with multiple accounts](https://code.claude.com/docs/en/authentication#log-in-with-multiple-accounts)
- Anthropic, [Explore the .claude directory](https://code.claude.com/docs/en/claude-directory) and [Environment variables](https://code.claude.com/docs/en/env-vars)
- Anthropic, [Manage Claude's memory: import additional files](https://code.claude.com/docs/en/memory#import-additional-files) and [Skills](https://code.claude.com/docs/en/skills)
- Anthropic, [Customize your status line](https://code.claude.com/docs/en/statusline) and [Use Claude Code in VS Code](https://code.claude.com/docs/en/vs-code)
- Visual Studio Code, [Contribution points: configuration scopes](https://code.visualstudio.com/api/references/contribution-points#contributes.configuration)
