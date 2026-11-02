---
title: "Multiple Claude Accounts"
weight: 55
bookCollapseSection: true
---

[Claude Code](/wiki/ai/context-engineering/claude-code) keeps each account's login, settings and history in a configuration directory, `~/.claude` by default. To use another account, start Claude Code with the `CLAUDE_CONFIG_DIR` environment variable set to that account's directory. The first run walks you through signing the account in:

```bash
CLAUDE_CONFIG_DIR=~/.claude-work claude
```

Three pages turn that into a setup, one for each decision, in the order the decisions come up:

- [How many Claude accounts, and what type](/wiki/ai/claude-accounts/how-many-accounts): one account for each organization whose code you work on, and which plan to buy. Decided once, and revisited when a job, a client or your usage changes.
- [Map a Claude account to a directory or repo](/wiki/ai/claude-accounts/per-directory): set up once per account, after which changing into a directory picks its account.
- [Switch between Claude accounts](/wiki/ai/claude-accounts/switching): what to type day to day, in a terminal, in a running session, in scripts and in VS Code.

## Further reading

- Anthropic, [Log in with multiple accounts](https://code.claude.com/docs/en/authentication#log-in-with-multiple-accounts)
