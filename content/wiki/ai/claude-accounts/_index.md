---
title: "Multiple Claude Accounts"
weight: 55
bookCollapseSection: true
---

[Claude Code](/wiki/ai/context-engineering/claude-code) sends each model request with one credential, and the account behind that credential decides how the request is paid for. A claude.ai login on a Pro, Max, Team or seat-based Enterprise plan draws on a usage allowance that refills on two clocks, one of five hours and one of a week. A Claude Console API key, or a cloud provider's credential such as Amazon Bedrock's, is billed per token instead. Claude Code keeps one saved login per configuration directory: `~/.claude` by default, or whichever directory the `CLAUDE_CONFIG_DIR` environment variable names. Running several accounts therefore means keeping several directories and choosing one each time a session starts.

## Why one person runs several

The reasons concern where code goes, who pays, how far one allowance stretches, and which kind of credential a job needs.

Pro and Max are consumer plans. Anthropic trains future models on Claude Code sessions from those accounts when the account's model-improvement setting is on, and in that case keeps the data for five years; with the setting off it keeps the data for 30 days. Team, Enterprise and API accounts are covered by Anthropic's Commercial Terms, under which it does not train on code or prompts unless the customer chooses to provide them for model improvement, keeps data for 30 days, and can enable zero data retention (ZDR) for a qualifying Enterprise organization. Code that belongs to an employer or a client goes on that organization's account for this reason, and a personal subscription stays with personal projects.

Each account is also a bill. A subscription charges one card, a Team seat charges the organization that bought it, and a Console API key charges the workspace that issued it, which can carry its own spend limit. Work done with a client's key is billed to the client's Console organization directly.

One allowance has a ceiling. The largest individual plan, Max 20x at $200 a month, allows 20 times Pro's usage in each five-hour session, under a weekly limit that Anthropic does not publish as a multiple. Beyond it, Anthropic sells usage credits at API rates, and work can move to an API key.

Automation has its own credential rules. `claude -p --bare`, the scripted mode that skips hooks, plugins and instruction files, never reads a subscription login: against the Anthropic API it needs an API key or an `apiKeyHelper` script. Anthropic's terms direct products built on the Claude Agent SDK to API keys as well.

## What the terms allow, in brief

Holding more than one account is allowed. Claude Code's documentation describes a work account and a personal account signed in side by side, and Thariq Shihipar, then an engineer on Anthropic's Claude Code team, wrote in February 2026 that "it's not against terms of service to have multiple MAX accounts". Sharing a login with another person, reselling access, and signing a third-party tool in with a subscription are prohibited.

Spreading one person's work across several subscriptions to keep going past their limits is the contested case. Anthropic's terms for Claude Code's wrap-up allowance, a small, capped extension that lets a response already under way continue briefly to a stopping point when the five-hour limit arrives, list "an attempt to get around usage limits (for example, through multiple accounts or automation designed to exploit the allowance)" among the grounds for withholding it. [What the terms allow](/wiki/ai/claude-accounts/terms) quotes each document.

## Choosing a setup

| Need | Setup | Details |
| --- | --- | --- |
| Employer and personal work on one machine | One configuration directory per account, with employer code only on the employer's account | [Work and personal](/wiki/ai/claude-accounts/layouts#work-and-personal) |
| Several clients, each billed and kept apart | One directory per client, signed in to the client's organization or using its API key | [One account per client](/wiki/ai/claude-accounts/layouts#one-account-per-client) |
| Scripts and continuous integration | An API key from a Console workspace, kept apart from the interactive account | [Sessions on a subscription, scripts on a key](/wiki/ai/claude-accounts/layouts#sessions-on-a-subscription-scripts-on-a-key) |
| More capacity, or a smaller bill | A larger plan rather than a second subscription, usage credits past Max 20x, and scripts on an API key | [Using multiple accounts cost-effectively](/wiki/ai/claude-accounts/cost-model) |
| A team | Team seats, one per named person | [A team on Team seats](/wiki/ai/claude-accounts/layouts#a-team-on-team-seats) |
| Several subscriptions pooled behind a proxy | Avoid: it matches a clause the Usage Policy adds on 12 November 2026 | [Subscription-pooling proxies](/wiki/ai/claude-accounts/tools#subscription-pooling-proxies) |

## In this section

[Plans and usage limits](/wiki/ai/claude-accounts/plans-and-limits) comes first: what a plan's allowance is, what draws on it, what happens when it runs out, and the paid ways past it. [What the terms allow](/wiki/ai/claude-accounts/terms) quotes the consumer and commercial terms, the Usage Policy, and statements by Anthropic and its staff on multiple accounts. [Which credential Claude Code uses](/wiki/ai/claude-accounts/credentials) covers where each kind of login is stored and which of several credentials wins, including the exported API key that bills per token while a subscription is signed in.

[One config directory per account](/wiki/ai/claude-accounts/config-directories) is the setup itself: aliases, a shell function that picks the account by project, sharing instructions and skills between accounts, a status line that names the account, and the editor extensions. [Using multiple accounts cost-effectively](/wiki/ai/claude-accounts/cost-model) sets a larger plan against a second subscription, usage credits and an API key, says which work each kind of account is cheapest for, and works out when to move up a plan. [Tools for multiple accounts](/wiki/ai/claude-accounts/tools) reviews what others have published, from usage trackers to proxies that pool subscriptions, with each one's standing under the terms. [Account layouts](/wiki/ai/claude-accounts/layouts) closes the section with seven arrangements, each with its setup, cost and risk.

## Related

- [Claude Code](/wiki/ai/context-engineering/claude-code): the harness these accounts sign in to, worked through on one real task.
- [Loops in Claude Code](/wiki/ai/loop-engineering/claude-code): `claude -p` and the other unattended modes, which run on whatever credential their environment supplies.
- [Prompt caching & cost](/wiki/ai/prompt-caching): the per-token economics behind API-key billing.
- [Identity separation](/wiki/security/identity-separation): keeping identities unlinkable, a stronger property than keeping accounts apart.

## Further reading

- Anthropic, [Authentication](https://code.claude.com/docs/en/authentication), including the section on logging in with multiple accounts
- Anthropic, [Use Claude Code with your Pro or Max plan](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan)
- Anthropic, [Legal and compliance](https://code.claude.com/docs/en/legal-and-compliance) and [Data usage](https://code.claude.com/docs/en/data-usage)
- Thariq Shihipar, [post on X](https://x.com/trq212/status/2024230184287949207) (18 February 2026) on holding several Max accounts
