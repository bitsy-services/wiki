---
title: "Switch Between Claude Accounts"
weight: 30
aliases: ["/wiki/ai/claude-accounts/config-directories/", "/wiki/ai/claude-accounts/credentials/", "/wiki/ai/claude-accounts/tools/"]
---

Start [Claude Code](/wiki/ai/context-engineering/claude-code) with `CLAUDE_CONFIG_DIR` set to the other account's configuration directory, the folder that holds that account's login, settings and history. An alias in `~/.bashrc` or `~/.zshrc` turns that into one word:

```bash
alias claude-work='CLAUDE_CONFIG_DIR=~/.claude-work claude'
```

In a new terminal, `claude` starts your default account and `claude-work` the work account. The first `claude-work` creates the directory and walks you through signing the work account in. Each session keeps the account it started with, so two terminals can run two accounts side by side.

Both need the `claude` command on your `PATH`. The VS Code extension's own copy of Claude Code is not on it, so if `claude` is not found, install it with `curl -fsSL https://claude.ai/install.sh | bash`.

## Switching, wherever you are

| Where | How |
| --- | --- |
| A terminal | Type `claude-work` or `claude` |
| A directory mapped to an account | `cd` into it; [Map a Claude account to a directory or repo](/wiki/ai/claude-accounts/per-directory) sets this up |
| A running session | Exit, then start the other account. `/login` inside the session would instead replace this directory's login, and you would have to sign in again to get it back |
| A script or cron job | Name the account's directory on the command line, as in [scripts and cron jobs](#scripts-and-cron-jobs) |
| The VS Code panel | Change `CLAUDE_CONFIG_DIR` in the `claudeCode.environmentVariables` setting, then run **Developer: Reload Window**, or switch to the account's VS Code profile if each account [has one](/wiki/ai/claude-accounts/per-directory#in-vs-code) |
| The Claude desktop app or claude.ai | Sign out, then sign in as the other account |

## Scripts and cron jobs

Scripts and cron jobs load neither your aliases nor your `PATH`, so name the account's directory and the full path to `claude`:

```bash
CLAUDE_CONFIG_DIR="$HOME/.claude-api" "$HOME/.local/bin/claude" -p "your prompt"
```

`~/.local/bin` is where Anthropic's installer puts `claude`; `command -v claude` shows where yours is. [`claude -p`](/wiki/ai/loop-engineering/claude-code#claude--p-any-program-can-be-the-loop) runs one prompt and exits. Give scripts an account billed per token, here `~/.claude-api`, signed in with **Anthropic Console account** and then **Create an API key**, so that they never spend the usage limits your interactive sessions need.

## Which account is this?

- **Inside a session**, `/status` shows the account in use. In the VS Code panel, `/usage` shows the signed-in account.
- **From a shell**, `claude auth status` or `claude-work auth status` prints the `email` and `orgName` of the account that command would use, and its `configDirectory`.
- **On screen all the time**: give each account a status line, the bar at the bottom of a session, that prints its name. Add this to `~/.claude-work/settings.json`, and the same to each other account's `settings.json` with its own name in place of `work`:

  ```json
  {
    "statusLine": { "type": "command", "command": "echo work" }
  }
  ```

## Pitfalls

- **The browser decides which account signs in.** If it is signed in to claude.ai as your other account, the new directory gets that account. Press `c` at the sign-in screen to copy the link, open it in a private window, and paste the code it shows back into the terminal.
- **An exported `ANTHROPIC_API_KEY` beats every account.** Claude Code uses the key instead of the account's login and bills its owner per token: an interactive session asks once whether to use it, and `claude -p` uses it without asking. Remove the export from your shell profile.
- **Conversations stay with their account.** `--resume` and `--continue` find only the current account's conversations, because each configuration directory keeps its own history. Work moved to another account starts a new conversation.
- **For the default account, leave `CLAUDE_CONFIG_DIR` unset.** `CLAUDE_CONFIG_DIR=~/.claude` is not the same: it makes Claude Code look for its account file inside `~/.claude` instead of at `~/.claude.json`, so it starts without the [Model Context Protocol (MCP)](/wiki/ai/mcp) servers and trusted folders you set up.

## Related

- [How many Claude accounts, and what type](/wiki/ai/claude-accounts/how-many-accounts): which accounts to have in the first place.
- [Map a Claude account to a directory or repo](/wiki/ai/claude-accounts/per-directory): `cd` as the switch, and sharing instructions and skills between accounts.

## Further reading

- Anthropic, [Authentication](https://code.claude.com/docs/en/authentication), including logging in with multiple accounts and which credential wins when several are present
- Anthropic, [Environment variables](https://code.claude.com/docs/en/env-vars), for `CLAUDE_CONFIG_DIR`
- Anthropic, [Customize your status line](https://code.claude.com/docs/en/statusline)
