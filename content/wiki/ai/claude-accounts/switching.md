---
title: "Switching Between Claude Accounts"
weight: 5
aliases: ["/wiki/ai/claude-accounts/config-directories/"]
---

[Claude Code](/wiki/ai/context-engineering/claude-code) keeps one saved login per configuration directory, the folder that also holds its settings, personal instructions and session history. The default directory is `~/.claude`. Setting the `CLAUDE_CONFIG_DIR` environment variable when `claude` starts selects a different directory, with a login of its own. Running several accounts therefore means one directory per account, and switching accounts means starting `claude` with a different `CLAUDE_CONFIG_DIR`. With one shell alias per account, switching is the difference between typing `claude` and typing `claude-work`.

## Why run more than one account

Separate accounts keep apart three things that one account mixes:

- **The terms the code is sent under.** Pro, Max and Ultra are consumer plans, and while an account's model-improvement setting is on, Anthropic trains new models on its data, Claude Code sessions included. Team, Enterprise and API accounts are under the Commercial Terms, and Anthropic does not train on code or prompts sent under them unless the customer opts in. An employer's or a client's code belongs on that organization's account.
- **Who pays.** Each account bills its owner: a Team seat bills the employer that bought it, and a client's API key bills the client.
- **What a job needs.** Scripts and scheduled runs suit an API key. They are billed per token instead of spending the subscription's [usage allowance](/wiki/ai/claude-accounts/plans-and-limits), they can be capped in dollars, and [`claude -p --bare`](/wiki/ai/loop-engineering/claude-code#claude--p-any-program-can-be-the-loop), the stripped-down scripted mode, never reads a subscription login at all.

Using a second subscription to keep working once the first reaches its usage limit is a different case. The terms of Claude Code's wrap-up allowance, a small, capped extension that lets a response already under way continue briefly to a stopping point when the five-hour limit arrives, list "an attempt to get around usage limits (for example, through multiple accounts …)" among the grounds for withholding it. [What the terms allow](/wiki/ai/claude-accounts/terms#getting-past-usage-limits) quotes the clauses, and [using multiple accounts cost-effectively](/wiki/ai/claude-accounts/cost-model) prices the routes Anthropic sells instead: a larger plan, usage credits and API keys.

## What an account is to Claude Code

To Claude Code, an account is a configuration directory. Each directory holds one login and everything Claude Code keeps alongside it:

| In the directory | What it holds |
| --- | --- |
| `.credentials.json`, or on macOS a Keychain entry tied to the directory | The login |
| `.claude.json` | Account details, personal [MCP](/wiki/ai/mcp) (Model Context Protocol) servers, and which projects are trusted |
| `settings.json` | Settings, including the status line (a bar at the bottom of the screen) and any `apiKeyHelper` (a command that prints an API key) |
| `CLAUDE.md`, `skills/`, `agents/` | Personal instructions, skills and subagents |
| `plugins/` | Installed [plugins](/wiki/ai/plugins/claude-code) |
| `projects/`, `history.jsonl` | Session transcripts, which `--resume` lists, and the history of typed prompts |

The default directory keeps one file elsewhere: with `CLAUDE_CONFIG_DIR` unset, `.claude.json` sits beside the directory, at `~/.claude.json`.

Two things reach every account, whichever directory is in use:

- **The repository's own configuration.** A project's `.claude/settings.json`, `.mcp.json` and `CLAUDE.md` load for every account that opens it.
- **Credentials in the environment.** An exported `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN` or `CLAUDE_CODE_OAUTH_TOKEN` outranks the login saved in any directory; [Pitfalls](#pitfalls) has the fix.

## Configure each account

The snippets are for Bash and Zsh, on macOS, Linux and WSL. Aliases go in `~/.bashrc` or `~/.zshrc` and take effect in new terminals.

### A second subscription

Here a work login joins a personal one, and the personal one stays the default, in `~/.claude`.

1. Add an alias that starts Claude Code with the work directory:

   ```bash
   alias claude-work='CLAUDE_CONFIG_DIR=~/.claude-work claude'
   ```

2. Open a new terminal and sign the new directory in:

   ```bash
   claude-work auth login
   ```

   The command opens a browser and also prints the login URL. If the browser is signed in to claude.ai as the personal account, open the URL in a private window, or in the browser profile used for work, instead. If the browser shows a code rather than returning to the terminal, paste it at the `Paste code here if prompted` prompt.

3. If the work login belongs to more than one organization, such as a personal Max plan and an employer's Team plan, the authorization page asks which one to authorize. Choose the employer's: that choice decides which plan the directory draws on.

4. Check where the login landed:

   ```bash
   claude-work auth status --text
   ```

   The output names the login method, the organization and the email. If the organization is not the employer's, run `claude-work auth login` again and choose the other one.

From then on `claude-work` starts a work session and `claude` a personal one.

### An API key

An API key comes from the Claude Console, Anthropic's developer platform, and bills the organization that issued it: a client's key bills the client, and a key of one's own suits scripts. The key goes in the directory's settings as a command that prints it, so it never sits in a shell profile, where every other account would pick it up.

1. Store the key, here in [pass](/wiki/security/pass), a password store built on [GPG](/wiki/security/gpg):

   ```bash
   pass insert anthropic/acme
   ```

2. Create the directory, and save the setting below as `~/.claude-acme/settings.json`:

   ```bash
   mkdir -p ~/.claude-acme
   ```

   ```json
   {
     "apiKeyHelper": "pass show anthropic/acme"
   }
   ```

   Claude Code runs the `apiKeyHelper` command through `/bin/sh`, sends what it prints as the key, and caches it for five minutes. Any command that prints the key will do.

3. Add an alias:

   ```bash
   alias claude-acme='CLAUDE_CONFIG_DIR=~/.claude-acme claude'
   ```

Do not use `/login` with *Sign in with your Console account* for this. That sign-in creates no key and is stored outside the configuration directory, so every directory shares it, and making it signs out every claude.ai login on the machine.

### Share instructions and skills

A new directory starts without the default account's personal `CLAUDE.md` and skills. These commands share them with the work account; repeat them for each directory:

```bash
echo '@~/.claude/CLAUDE.md' >> ~/.claude-work/CLAUDE.md
mkdir -p ~/.claude/skills
ln -s ~/.claude/skills ~/.claude-work/
```

The first makes the work account's `CLAUDE.md` import the default one, and lines added below the import apply to the work account alone. The other two link the default account's skills folder, creating it first if it does not exist yet, so a skill added in either account appears in both; `ln` refuses if the work account already has a `skills` folder of its own.

Settings stay separate, since the status line label and any `apiKeyHelper` differ between accounts. MCP servers and plugins are installed per directory, so add each one to every account that needs it, through that account's alias: `claude-work mcp add --scope user` followed by the server's usual arguments.

## Switch between accounts

### In a terminal

Run the alias for the account: `claude` for the default, `claude-work` or `claude-acme` for the others. Terminals are independent, so two can run different accounts side by side. The alias carries every subcommand and flag with it, as in `claude-work --resume` or `claude-work auth status`.

### By project folder

A shell function named `claude` can choose the account from the current folder, so that `claude` typed anywhere under `~/work` starts the work account. It goes in the same file as the aliases:

```bash
claude() {
  if [ -n "${CLAUDE_CONFIG_DIR:-}" ]; then
    CLAUDE_CONFIG_DIR="$CLAUDE_CONFIG_DIR" command claude "$@"
    return
  fi
  case "$PWD/" in
    "$HOME/work/"*)
      CLAUDE_CONFIG_DIR="$HOME/.claude-work" command claude "$@" ;;
    "$HOME/clients/acme/"*)
      CLAUDE_CONFIG_DIR="$HOME/.claude-acme" command claude "$@" ;;
    *)
      env -u CLAUDE_CONFIG_DIR claude "$@" ;;
  esac
}
```

An account already chosen, by an alias or by setting `CLAUDE_CONFIG_DIR`, wins. Otherwise each folder gets one `case` entry, and anywhere else the default account runs. `command claude` and `env … claude` run the real program rather than the function. The last branch removes the variable instead of leaving it empty, because an [empty `CLAUDE_CONFIG_DIR`](#pitfalls) is not the default, and the slash added to `$PWD` stops `~/workshop` from matching `~/work`. The function and the aliases were tested together in Bash 5.3, dash and Zsh 5.9, under `set -u` and with a space in the home folder's path.

The function switches accounts only for `claude` typed in a shell that loaded it, in a folder it lists. Everything else starts on the default account: VS Code without its own setting, scripts and cron jobs that do not set `CLAUDE_CONFIG_DIR`, wrappers such as `timeout`, and a work repository cloned outside `~/work`. The desktop app has a sign-in of its own. The sections below cover the editor, the desktop app and scripts.

### Inside a session

`/login` signs the current directory in to a different account and replaces the login it held. The settings and history stay, since the directory is the same. Going back means signing in again, so `/login` suits a one-off change, and a directory per account suits switching every day.

### In VS Code

The extension takes the directory from its `claudeCode.environmentVariables` setting. The value must be an absolute path, because the extension does not expand `~`:

```json
{
  "claudeCode.environmentVariables": [
    { "name": "CLAUDE_CONFIG_DIR", "value": "/home/you/.claude-work" }
  ]
}
```

Where the entry goes depends on the window:

- **A local window**: user settings, opened with **Preferences: Open User Settings (JSON)**. A VS Code profile created with its own settings, rather than borrowing the default profile's, keeps its own value, and a profile can be tied to a folder, so one profile per account switches accounts with the folder. That follows from VS Code's source and was not tried in a running editor.
- **A WSL, SSH or dev container window**: that remote's settings, opened with **Preferences: Open Remote Settings**. VS Code ignores this setting in user settings there.

A workspace's `.vscode/settings.json` cannot hold it. To switch, change or remove the entry, then run **Developer: Reload Window**. The integrated terminal takes the aliases as usual.

### In the desktop app

Claude Desktop signs in from its app menu and reads neither `apiKeyHelper` nor `ANTHROPIC_API_KEY`. To switch accounts there, sign out from the app menu and sign in again as the other account.

### In scripts and cron jobs

Scripts do not load the aliases in `~/.bashrc`, so a script names the directory itself. Pointing an unattended run at an API-key directory keeps it off the subscription:

```bash
CLAUDE_CONFIG_DIR="$HOME/.claude-acme" claude -p "Summarize the failures in last night's test run" --max-budget-usd 2
```

`--max-budget-usd` stops the run once Claude Code's own estimate of its spend reaches the cap. The estimate can differ from the bill and spend can pass the cap, so leave headroom. If the key helper fails, as `pass` can under cron when nothing is there to unlock the key, the run exits with an error: the directory holds no other credential to fall back on.

With `--bare`, which Anthropic plans to make the default for `-p`, Claude Code ignores an `apiKeyHelper` in the directory's `settings.json`, so the helper has to come with the command:

```bash
claude -p --bare --settings '{"apiKeyHelper": "pass show anthropic/acme"}' "Summarize the failures in last night's test run" --max-budget-usd 2
```

## Check which account is in use

From the folder a session would start in, run `auth status` through the same command the session would use:

```bash
claude auth status --text
claude-work auth status --text
```

For a subscription login the output names the login method, such as `Claude Team account`, the organization and the email; for a key helper it reads `Auth token: apiKeyHelper`. The command exits with status 1 when the directory holds no credential. Without `--text` it prints JSON with the `configDirectory` in use, the `authMethod` (`claude.ai` or `api_key_helper`), and for a subscription the `email`, `orgName` and `subscriptionType`. Inside a session, `/status` shows the same account details.

### Label each session with its account

A status line is a bar at the bottom of Claude Code that shows whatever a command prints, and it can keep the account's name on screen. Add a `statusLine` entry to each directory's `settings.json`, with that account's name:

```json
{
  "statusLine": { "type": "command", "command": "echo work" }
}
```

Claude Code passes the command a JSON description of the session on standard input. For Pro, Max and Ultra logins the description includes the plan's usage from the session's first response on: the five-hour and weekly windows, or whichever of them the plan has. This script prints them beside the label:

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

Save it as `~/.local/bin/claude-statusline`, make it executable with `chmod +x`, and use `~/.local/bin/claude-statusline work` as the command in place of `echo work`. A personal session on a Max plan then shows `personal | Opus 5.5 | 5h 24% until 16:00 | week 41%`. Team and Enterprise seats and API keys get no usage figures, so their sessions show the label and the model.

## Pitfalls

- **Anything the aliases and the function do not reach runs on the default account.** That covers VS Code without its own setting, scripts and cron jobs that do not set `CLAUDE_CONFIG_DIR`, and a work repository cloned outside the folders the function lists. If the default is a personal Pro, Max or Ultra login, employer code started any of those ways goes out under the consumer terms. On a machine used mostly for work, make the work account the default, in `~/.claude`, and give the personal one its own directory and alias; [Work and personal](/wiki/ai/claude-accounts/layouts#work-and-personal) weighs the two arrangements. The desktop app is separate: it runs on whichever account is signed in to it.
- **An empty `CLAUDE_CONFIG_DIR` makes the current folder the configuration directory.** Started in a repository, Claude Code 2.1.314 then reads a `settings.json` at the repository's root as its own settings, runs an `apiKeyHelper` command found there, and writes its own folders, such as `projects/` and `backups/`, into the repository. Use `unset CLAUDE_CONFIG_DIR`, not `CLAUDE_CONFIG_DIR=`.
- **An exported API key overrides every account.** `ANTHROPIC_API_KEY` set in a shell profile outranks the login in every directory. An interactive session asks once per directory whether to use it, `claude -p` uses it without asking, and either way the key's account is billed per token. Remove the export, run `unset ANTHROPIC_API_KEY` in open terminals, and give the key to one account through an `apiKeyHelper` instead.
- **`CLAUDE_CONFIG_DIR=~/.claude` is not the default account.** With the variable set, `.claude.json` is read from inside the directory, so Claude Code 2.1.314 starts a new `~/.claude/.claude.json` and does not see the MCP servers and project trust kept in `~/.claude.json`. For the default account, leave the variable unset.
- **Conversations stay with their account.** Transcripts live in the directory that recorded them, so `--resume` lists only the current account's sessions, and work moved to another account starts a new conversation.

## Related

- [Which credential Claude Code uses](/wiki/ai/claude-accounts/credentials): the full order of precedence, and the limits of each kind of credential.
- [Account layouts](/wiki/ai/claude-accounts/layouts): which accounts to keep for work and personal use, for clients, for scripts and for a team.
- [Plans and usage limits](/wiki/ai/claude-accounts/plans-and-limits): what each account's allowance is and what happens when it runs out.
- [Tools for multiple accounts](/wiki/ai/claude-accounts/tools): third-party switchers and usage trackers, and where each stands under the terms.

## Further reading

- Anthropic, [Authentication: log in with multiple accounts](https://code.claude.com/docs/en/authentication#log-in-with-multiple-accounts)
- Anthropic, [Explore the .claude directory](https://code.claude.com/docs/en/claude-directory) and [Environment variables](https://code.claude.com/docs/en/env-vars)
- Anthropic, [Settings reference: apiKeyHelper](https://code.claude.com/docs/en/settings-reference#apikeyhelper) and [Customize your status line](https://code.claude.com/docs/en/statusline)
- Anthropic, [Use Claude Code in VS Code](https://code.claude.com/docs/en/vs-code) and [Use Claude Code with your Team or Enterprise plan](https://support.claude.com/en/articles/11845131-use-claude-code-with-your-team-or-enterprise-plan)
- Anthropic, [Run Claude Code programmatically](https://code.claude.com/docs/en/headless) and [Data usage](https://code.claude.com/docs/en/data-usage)
- Visual Studio Code, [Profiles](https://code.visualstudio.com/docs/configure/profiles) and [configuration scopes](https://code.visualstudio.com/api/references/contribution-points#contributes.configuration)
