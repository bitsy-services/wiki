---
title: "Map a Claude Account to a Directory or Repo"
weight: 20
---

Put a one-line `.envrc` file in the directory that holds an account's repos. The line names the account's configuration directory, the folder where [Claude Code](/wiki/ai/context-engineering/claude-code) keeps the account's login, settings and history. direnv, a shell extension, loads a directory's `.envrc` when you `cd` into it and unloads it when you leave. Every `claude` started inside the directory then runs on that account; anywhere else, `claude` runs on your default account in `~/.claude`.

```bash
# ~/work/.envrc
export CLAUDE_CONFIG_DIR="$HOME/.claude-work"
```

The steps are for Bash or Zsh on macOS, Linux or WSL. They use `~/work` for the directory of work repos and `~/.claude-work` for the work account's configuration directory; substitute your own names.

## 1. Install direnv

```bash
sudo apt install direnv     # Debian, Ubuntu, WSL
brew install direnv         # macOS
```

Add its hook to the end of your shell's startup file, then open a new terminal:

```bash
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc    # Bash
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc      # Zsh
```

## 2. Point the directory at the account

```bash
echo 'export CLAUDE_CONFIG_DIR="$HOME/.claude-work"' >> ~/work/.envrc
direnv allow ~/work
```

direnv refuses to load an `.envrc` until you run `direnv allow`, and refuses again each time the file changes, until you rerun it. Meanwhile, `claude` in that directory starts your default account.

To map a single repo instead, put the file in the repo and keep it out of Git:

```bash
cd ~/src/acme-app
echo 'export CLAUDE_CONFIG_DIR="$HOME/.claude-acme"' >> .envrc
echo .envrc >> .git/info/exclude
direnv allow
```

## 3. Sign the account in

```bash
cd ~/work
claude
```

direnv prints `direnv: export +CLAUDE_CONFIG_DIR` as you enter. Claude Code creates the account's directory and walks you through setup: a theme, then a login method.

- For a Pro, Max, Ultra, Team or Enterprise account, choose **Claude account with subscription**.
- For an API key account, choose **Anthropic Console account**, then **Create an API key**. Avoid the option marked recommended, **Sign in with your Console account**: Claude Code stores it outside the account's directory, so every account shares it, and it signs out every claude.ai login on the machine.

A browser opens for the sign-in. If that browser is signed in to claude.ai as your other account, press `c` to copy the sign-in link, open it in a private window, and paste the code it shows back into the terminal.

## 4. Check it

From any repo in the directory:

```bash
claude auth status
```

`configDirectory` should end in `.claude-work`, and `loggedIn` should be `true`. Run it outside the directory and `configDirectory` ends in `.claude`.

## In VS Code

**The integrated terminal** follows `.envrc` like any terminal. The extension's own copy of Claude Code is not on your `PATH`, so install the `claude` command first:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**The Claude panel** does not read `.envrc`. It takes the configuration directory from the `claudeCode.environmentVariables` setting, which needs the full path, because the extension does not expand `~`:

```json
{
  "claudeCode.environmentVariables": [
    { "name": "CLAUDE_CONFIG_DIR", "value": "/home/you/.claude-work" }
  ]
}
```

VS Code accepts this setting in user settings and in Remote Settings, but not in a workspace's own settings, so the panel cannot map a single repo the way `.envrc` does:

- **Local folders.** Create a VS Code profile for each account, with its own settings. In each profile, add the setting with **Preferences: Open User Settings (JSON)**, then open that account's folders in the profile. VS Code reopens each folder in the profile it was last opened in.
- **WSL, SSH and container windows.** Add the setting with **Preferences: Open Remote Settings (JSON)**. Remote Settings apply to every folder on that machine, so the panel runs one account there. For the other accounts, run `claude` in the integrated terminal.

## Share your instructions and skills

A new account starts without your personal `CLAUDE.md`, skills, settings, plugins and [Model Context Protocol (MCP)](/wiki/ai/mcp) servers. These commands give the work account the default account's `CLAUDE.md` and skills:

```bash
mkdir -p ~/.claude-work ~/.claude/skills
echo '@~/.claude/CLAUDE.md' >> ~/.claude-work/CLAUDE.md
ln -s ~/.claude/skills ~/.claude-work/
```

The work account's `CLAUDE.md` now imports the default one, and anything you add below that line applies to work only. Both accounts read one skills folder, so a skill added in either shows up in both. If the work account already has a `skills` folder, `ln` refuses: move its contents into `~/.claude/skills`, delete it, and run `ln` again. Settings, plugins and MCP servers stay separate: install them in each account that needs them.

## Pitfalls

- **Anything not started from your shell uses the default account.** That covers scripts, cron jobs, the VS Code panel and the Claude desktop app, unless they set `CLAUDE_CONFIG_DIR` themselves. On a machine used mostly for work, sign `~/.claude` in to the work account and give the personal account its own directory, so whatever misses the mapping lands on work.
- **An exported `ANTHROPIC_API_KEY` beats every account.** Claude Code uses the key instead of the account's login and bills its owner per token: an interactive session asks once whether to use it, and `claude -p` uses it without asking. Remove the export from your shell profile.
- **A repo with its own `.envrc` replaces the directory's.** Inside it, `claude` runs on the default account. Make `source_up` the first line of the repo's `.envrc`, so that it loads the parent's file as well.

## Related

- [How many Claude accounts, and what type](/wiki/ai/claude-accounts/how-many-accounts): which accounts to set up.
- [Switch between Claude accounts](/wiki/ai/claude-accounts/switching): switching in a terminal, in a running session, in scripts and in VS Code.

## Further reading

- Anthropic, [Log in with multiple accounts](https://code.claude.com/docs/en/authentication#log-in-with-multiple-accounts), [Sign in without an API key](https://code.claude.com/docs/en/authentication#sign-in-without-an-api-key) and [Set up Claude Code](https://code.claude.com/docs/en/setup)
- Anthropic, [Use Claude Code in VS Code](https://code.claude.com/docs/en/vs-code), for the extension's settings
- [direnv](https://direnv.net/), including its [hook setup](https://direnv.net/docs/hook.html) and the `source_up` function in the [standard library](https://direnv.net/man/direnv-stdlib.1.html)
- Visual Studio Code, [Profiles](https://code.visualstudio.com/docs/configure/profiles)
