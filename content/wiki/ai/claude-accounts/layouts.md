---
title: "Account Layouts"
weight: 70
---

An account layout is the set of accounts one person or one team runs [Claude Code](/wiki/ai/context-engineering/claude-code) on, together with the rule that decides which account a session uses. Each layout below meets one of the needs listed in the [section index](/wiki/ai/claude-accounts#why-one-person-runs-several): a boundary around code, a boundary around billing, a different kind of credential, or more capacity. The first, a single account, is the baseline the others add to, and each layout gives its setup, its cost and its risk.

| Situation | Layout |
| --- | --- |
| One person, personal projects, within one plan's limits | [One account](#one-account) |
| Code that belongs to an employer | [Work and personal](#work-and-personal) |
| Several clients | [One account per client](#one-account-per-client) |
| Scheduled, scripted or CI runs | [Sessions on a subscription, scripts on a key](#sessions-on-a-subscription-scripts-on-a-key) |
| Limits reached regularly on the plan that suits the work | [Overflow to credits or an API key](#overflow-to-credits-or-an-api-key) |
| Several people | [A team on Team seats](#a-team-on-team-seats) |
| Two personal subscriptions | [Two subscriptions for one person](#two-subscriptions-for-one-person) |

The setups use the aliases, the per-directory function and the status line script from [One config directory per account](/wiki/ai/claude-accounts/config-directories).

## One account

A single subscription is sized with [the cost model](/wiki/ai/claude-accounts/cost-model), and usage credits are turned on with a monthly cap as the margin for a heavy week. Nothing needs configuring beyond `/login`, and no `ANTHROPIC_API_KEY` belongs in the shell profile.

The settings that stretch one allowance are model choice, context and visibility. Anthropic's guide to usage in Claude Code calls Sonnet "the right choice for the large majority of coding work"; `/model opusplan` keeps Opus for planning. `/clear` between unrelated tasks stops each turn from resending the last task's conversation. A status line showing the five-hour and weekly percentages turns a limit from an interruption into a number on screen.

The risk is using it for code it should not carry. A Pro or Max plan is under the Consumer Terms, and with the model-improvement setting on, its sessions can be used for training and kept for five years.

## Work and personal

The employer's code runs on the employer's Team or Enterprise seat and everything else on a personal Pro or Max plan, each in its own configuration directory. The employer's code stays under the employer's Commercial Terms, retention settings and bill, and personal projects stay off the employer's account.

```bash
# ~/.bashrc or ~/.zshrc: the personal account is the default; work has its own directory
alias claude-work='CLAUDE_CONFIG_DIR=~/.claude-work claude'
```

Sign the work directory in with the work address, choosing the employer's plan when the authorization page offers a choice:

```bash
CLAUDE_CONFIG_DIR=~/.claude-work claude auth login --email you@company.example
```

The per-directory function, with the employer's repositories kept under one path such as `~/work`, makes `claude` typed in a shell there use the work account. It does not reach the editor extensions, the desktop app, scripts, cron jobs or a work repository cloned elsewhere, which all start on the default account. On a machine used mostly for the employer, the reverse arrangement errs toward the employer's terms: with the work account as the default and the personal account behind the alias, a session started any other way lands on the employer's account, at the cost of personal work started from the editor, the desktop app or a script landing there too. The editor's own `CLAUDE_CONFIG_DIR` setting covers the sessions the editor starts, and on a machine the employer manages, `forceLoginOrgUUID`, described below, refuses another organization's login however a session starts. The personal account needs a personal email address: the Consumer Terms allow an account opened with an employer's address to be linked to the employer's organization, whose administrators may then "monitor and control the Account, including having access to Materials".

Each side pays for its own account. On a laptop the employer manages, managed settings, which the employer deploys and the user's own settings cannot override, may set `forceLoginOrgUUID`, after which Claude Code exits at startup when the login belongs to any other organization; the personal account then belongs on a personal machine. The other failure is an employer API key exported in the shell profile, which outranks both logins, as [Which credential Claude Code uses](/wiki/ai/claude-accounts/credentials#an-exported-api-key) explains.

## One account per client

A consultant or agency gives each client its own configuration directory, signed in to the client's organization: a seat on the client's Team or Enterprise plan, or an API key from a Console workspace the client owns, a workspace being the group of API keys within a Claude Console organization that carries its own spend limits. The client's code then goes to Anthropic under the client's agreement, and the client is billed directly.

```bash
alias claude-acme='CLAUDE_CONFIG_DIR=~/.claude-acme claude'
alias claude-globex='CLAUDE_CONFIG_DIR=~/.claude-globex claude'
```

For a client who issues an API key, the directory's `settings.json` names a helper that prints it, so the key never sits in a shell profile:

```json
{
  "apiKeyHelper": "pass show clients/acme/anthropic-key",
  "cleanupPeriodDays": 7
}
```

`cleanupPeriodDays` sets how long that directory keeps transcripts on the laptop, 30 days by default, without affecting the other clients. It is a partial control. The deletion runs as a sweep after a session starts in that directory, and `--bare` runs skip it, so a directory nobody opens keeps its transcripts indefinitely; the sweep also leaves `history.jsonl`, the record of typed prompts with their project paths, and each project's auto memory in place. At the end of an engagement, `CLAUDE_CONFIG_DIR=~/.claude-acme claude purge --all` deletes that account's transcripts, auto memory and prompt history after asking for confirmation; `claude auth logout` run with the same variable then signs the account out, and the directory can be deleted. With one case per client in the per-directory function, a session started from a shell in a client's checkout picks the client's account.

A client who provides no account leaves the consultant's own commercial account, a Team plan with its two-seat minimum or a Console key, as the fallback for that client's code; a personal Pro or Max plan would put the code under the Consumer Terms.

## Sessions on a subscription, scripts on a key

Interactive sessions run on the subscription, and anything a script, a cron job or a pipeline starts runs on a Console API key. Unattended runs then cannot spend the allowance an interactive session needs later in the week, each run can be capped in dollars, and `--bare`, which never reads a subscription login, works unchanged. On Max, the plan's monthly API credit pays for the scripts: $100 on Max 5x and $200 on Max 20x, after linking a Console organization in the billing settings on claude.ai.

Create a key in the linked organization, set a spend limit on its workspace in the Console, and store the key with `pass insert anthropic/scripts`. The script then reads the key, refuses to run without one, and hands it to Claude Code alone:

```bash
#!/usr/bin/env bash
set -euo pipefail

key="$(pass show anthropic/scripts)"
[ -n "$key" ] || { echo "no API key from pass" >&2; exit 1; }

ANTHROPIC_API_KEY="$key" CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1 \
  claude -p --bare "Summarize the failures in last night's test run" \
  --output-format json --max-budget-usd 2
```

The guard matters because Claude Code skips an empty `ANTHROPIC_API_KEY` and falls through to the next credential. `pass show` can fail under cron, where no terminal is available to ask for the GPG passphrase, and without the guard the run would then go out on the subscription login, the allowance this layout protects. `--bare` closes the same gap from the other side, since bare mode reads no OAuth credential: tested with an empty key, a `--bare` run stopped at `Not logged in · Please run /login`. It also skips the project's hooks, plugins and `CLAUDE.md`; a script that needs them can drop `--bare` and rely on the guard alone. `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` keeps the key out of the shell commands, hooks and tool servers the run starts. The JSON output reports the run's cost in `total_cost_usd`.

Of Claude Code usage, the included credit covers `claude -p` and Agent SDK runs that authenticate with a key from the linked organization, according to the FAQ in Anthropic's article on the credit. Runs started by the Claude Code GitHub Action, an editor extension or the desktop app count as Claude Code usage, which the credit does not cover even with `-p`, so they are billed to the key's organization from its purchased credit. Anthropic's article on Claude Code with Pro and Max puts it more broadly, saying the credits "can't be used in Claude Code or the Claude apps", so the Console's billing page after the first run shows which balance the script drew on.

## Overflow to credits or an API key

One subscription carries the work it can hold, and the rest is bought explicitly. Usage credits on the same account are the simpler form: nothing changes in Claude Code, requests continue past the limit at list price, a monthly spend limit bounds the bill, and the conversation carries on. Credits bought as bundles cost 10% to 30% less, and the [cost model](/wiki/ai/claude-accounts/cost-model#climbing-the-plan-ladder) says when a month's overflow has grown past the price of the next plan.

The alternative is a separate API-key directory, set up as in [One config directory per account](/wiki/ai/claude-accounts/config-directories#add-an-api-key-account) and started with its own alias, such as `claude-api`, when the subscription runs out. It suits an organization that already buys API credit, or a person who wants overflow on a different invoice. Its cost is the same list price without the bundle discount, and a session moved to it starts a new conversation, because transcripts stay in the directory where they were recorded. Both forms are routes Anthropic sells, and the terms raise no question about either.

## A team on Team seats

Each person on the team gets a Team seat: Standard seats at 1.25 times Pro's per-session allowance for light users, Premium seats at 6.25 times for heavy ones, mixed freely, with two seats at least. Usage credits can be enabled for members with per-member spend limits. A seat replaces both the shared login, which Anthropic's Team plan article rules out ("each seat is for one named individual"), and personal Max subscriptions expensed to the company, which put company code under the Consumer Terms.

| Seat | Monthly | Annual, per month | Per-session allowance | Monthly API credit |
| --- | --- | --- | --- | --- |
| Standard | $25 | $20 | 1.25 × Pro | $20 |
| Premium | $125 | $100 | 6.25 × Pro | $100 |

The team's API credits are pooled, up to $500 a month. Members sign in with `/login` and choose the team's plan. On company machines, managed settings with `forceLoginMethod` set to `"claudeai"` and `forceLoginOrgUUID` set to the team's organization ID make Claude Code refuse, at startup, a claude.ai login from any other organization and an API key supplied by the environment. A Premium seat costs $25 a month more than Max 5x for 6.25 against 5 times Pro's session allowance; Max 20x gives more per session than a Premium seat, under consumer terms and on one person's card.

## Two subscriptions for one person

One person holds two personal subscriptions. Thariq Shihipar, then an engineer on Anthropic's Claude Code team, wrote in February 2026 that "it's not against terms of service to have multiple MAX accounts"; what the documents address is what the accounts are used for.

Kept to separate purposes, such as a personal plan and a plan the person's own business pays for, each in its own directory, the arrangement is the work-and-personal layout with two personal accounts.

Claude Code's wrap-up allowance is a small, capped extension that lets a response already in progress continue briefly to a stopping point at the five-hour limit. Its terms give "an attempt to get around usage limits (for example, through multiple accounts …)" as grounds for withholding it, and carrying one stream of work past the first subscription's limits is that case. Automating the rotation, with a switcher's automatic mode or a pooling proxy, matches what the November 2026 Usage Policy clauses prohibit, as written. The Consumer Terms let Anthropic suspend or terminate an account without notice, and a subscriber terminated for a violation gets no refund.

On price, two Max 5x subscriptions give half the per-session allowance of one Max 20x for the same $200. Past Max 20x, $200 a month buys $250 of list-price usage as a bundle of usage credits. Whether a second Max 20x would hold more than that cannot be read from Anthropic's documents, which publish no allowance in dollars, while the credits are the route the terms do not question. [What the terms allow](/wiki/ai/claude-accounts/terms#getting-past-usage-limits) quotes each passage.

## Check

For each account in the layout, confirm the directory holds the intended credential and organization:

```bash
env -u CLAUDE_CONFIG_DIR claude auth status --text
for dir in ~/.claude-work ~/.claude-acme; do
  echo "== $dir"
  CLAUDE_CONFIG_DIR="$dir" claude auth status --text
done
```

Then open a session in a repository of each kind and run `/status`: the email and organization should match the account the layout assigns to that repository.

## Related

- [One config directory per account](/wiki/ai/claude-accounts/config-directories): the aliases, function, helper and status line these layouts use.
- [The cost of more capacity](/wiki/ai/claude-accounts/cost-model): choosing a plan size before choosing a layout.
- [What the terms allow](/wiki/ai/claude-accounts/terms): the passages behind each layout's risk.
- [Loops in Claude Code](/wiki/ai/loop-engineering/claude-code): the scheduled and scripted runs that the key-for-scripts layout moves off the subscription.

## Further reading

- Anthropic, [Use Claude Code with your Team or Enterprise plan](https://support.claude.com/en/articles/11845131-use-claude-code-with-your-team-or-enterprise-plan) and [What is the Team plan?](https://support.claude.com/en/articles/9266767-what-is-the-team-plan)
- Anthropic, [Authentication: restrict login to your organization](https://code.claude.com/docs/en/authentication#restrict-login-to-your-organization)
- Anthropic, [Monthly API credits for Max and Team plans](https://support.claude.com/en/articles/17154008-monthly-api-credits-for-max-and-team-plans)
- Anthropic, [Run Claude Code programmatically](https://code.claude.com/docs/en/headless) for `claude -p`, `--bare` and JSON output, and [Environment variables](https://code.claude.com/docs/en/env-vars) for `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`
- Anthropic, [Explore the .claude directory: clear local data](https://code.claude.com/docs/en/claude-directory#clear-local-data) for `claude purge`
- Thariq Shihipar, [post on X](https://x.com/trq212/status/2024230184287949207) (18 February 2026) on holding several Max accounts
