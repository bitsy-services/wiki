---
title: "How Many Claude Accounts, and What Type"
weight: 10
aliases: ["/wiki/ai/claude-accounts/plans-and-limits/", "/wiki/ai/claude-accounts/terms/", "/wiki/ai/claude-accounts/cost-model/", "/wiki/ai/claude-accounts/layouts/"]
---

Hold one account for each organization whose code you work on: one personal subscription for your own projects, your employer's account for its code, and each client's account for that client's code. Add an API key only for scripts and scheduled jobs. When your subscription keeps running out, move up a plan, or turn on usage credits for the gap, instead of buying a second subscription for the same work.

## Which account for which work

| Work | Account | Billed |
| --- | --- | --- |
| Your own projects | A personal subscription: Pro, Max or Ultra | A flat monthly price, with usage limits |
| Your employer's code | A seat on the employer's Team or Enterprise plan | To the employer |
| A client's code | A seat on the client's plan, or a login to the client's Claude Console organization | To the client |
| Scripts, CI and scheduled jobs | An API key from the Claude Console, Anthropic's developer platform | Per token, to whoever owns the key |

The type matters because of what Anthropic does with the data. Pro, Max and Ultra are consumer plans: while an account's model-improvement setting is on, Anthropic trains new models on its conversations and its [Claude Code](/wiki/ai/context-engineering/claude-code) sessions. Team, Enterprise and API accounts are commercial, and Anthropic does not train on code or prompts sent under them unless the customer opts in. The model-improvement setting is yours to change, not the code owner's, so code that belongs to someone else goes on a commercial account, under terms its owner agreed to. If a client provides none, use a commercial account of your own, such as a Claude Console account billed per token, not your personal subscription.

Open your personal account with a personal email address. Anthropic's consumer terms say that an account using an employer's address "may be linked to the organization's Anthropic enterprise account", and that the organization's administrator "may be able to monitor and control the Account".

## Which plan

The free plan does not include Claude Code. These three individual plans do:

| Plan | Price | Usage |
| --- | --- | --- |
| Pro | $20 a month, or $17 a month billed yearly | Limits that reset every five hours and every week |
| Max | $100 a month | Five times Pro's, every five hours and every week |
| Ultra | $200 a month | Ten times Pro's every week, and no five-hour limit once Anthropic has verified the account |

Start on Pro. Move to Max when you hit Pro's limits most weeks, and to Ultra when you hit Max's; Anthropic gives the same advice. Max and Ultra are billed monthly, so one month on the larger plan shows whether it is enough. For an occasional heavy week, or for more than Ultra allows, turn on usage credits in Settings > Usage on claude.ai: prepaid credit that keeps the work going at API prices once the plan's limits are spent.

A company of 2 to 150 people buys Team seats instead. A standard seat costs $25 a month, or $20 billed yearly; a premium seat, with five times a standard seat's usage, costs $125, or $100 billed yearly.

## Why not a second subscription

Billed monthly, each individual plan costs $20 a month for each multiple of Pro's usage: Max is five times Pro for $100, and Ultra ten times Pro's weekly usage for $200. At monthly prices, then, a second subscription buys no cheaper usage than moving up a plan. It only buys an amount between two plans, such as two Pro subscriptions for $40 instead of Max for $100, and usage credits cover that gap on the account you already have.

Two subscriptions for the same work also cost you in use. Each keeps its own limits and its own conversations, and when one runs out you switch accounts by hand and start a new conversation.

Anthropic's Claude Code documentation expects work and personal accounts side by side, so separate accounts for separate work are normal. A second account to carry the same work past a limit is a different matter. The terms of Anthropic's wrap-up allowance, which lets a Claude Code response that is already running finish after the five-hour limit arrives, list "an attempt to get around usage limits (for example, through multiple accounts or automation designed to exploit the allowance)" among the grounds for withholding that allowance.

## Next

[Map a Claude account to a directory or repo](/wiki/ai/claude-accounts/per-directory) gives each account its own configuration directory and points each of your project directories at one of them.

## Further reading

- Anthropic, [Plans and pricing](https://claude.com/pricing), [What is the Max plan?](https://support.claude.com/en/articles/11049741-what-is-the-max-plan) and [What is the Ultra plan?](https://support.claude.com/en/articles/17728952-what-is-the-ultra-plan)
- Anthropic, [Use Claude Code with your Pro, Max or Ultra plan](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-max-or-ultra-plan), for what to do when you reach a limit
- Anthropic, [Data usage](https://code.claude.com/docs/en/data-usage), for which plans are used for training
- Anthropic, [Consumer Terms of Service](https://www.anthropic.com/legal/consumer-terms), section 2 on business email addresses
- Anthropic, [Manage usage credits](https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans) and [Claude Code wrap-up allowance](https://support.claude.com/en/articles/17040437-claude-code-wrap-up-allowance)
