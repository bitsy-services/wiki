---
title: "Plans and Usage Limits"
weight: 10
---

A Pro, Max, Team or seat-based Enterprise subscription buys an allowance of usage that refills on two clocks: a session limit that resets every five hours, and a weekly limit that resets at a fixed time each week. Anthropic meters the allowance itself and publishes no token figure for it. Everything a subscriber does in Claude on the web, in the desktop and mobile apps, and in [Claude Code](/wiki/ai/context-engineering/claude-code) draws on the same allowance. A Claude Console API key has no allowance: each request is billed per token, requests are throttled at the organization's rate limits, and they stop when a prepaid balance runs out or a spend limit set by the owner is reached.

## The plans

Anthropic publishes each plan's allowance as a multiple of Pro's allowance per five-hour session.

| Plan | US price per month | Allowance per five-hour session | Terms |
| --- | --- | --- | --- |
| Pro | $20, less when billed annually | 1 × Pro, the unit | Consumer |
| Max 5x | $100 | 5 × Pro | Consumer |
| Max 20x | $200 | 20 × Pro | Consumer |
| Team, Standard seat | $25, or $20 billed annually; two seats minimum | 1.25 × Pro | Commercial |
| Team, Premium seat | $125, or $100 billed annually | 6.25 × Pro | Commercial |
| Enterprise, usage-based | By contract | No per-seat limit; billed at API rates | Commercial |
| Console API key | Per token | None; throttled by rate limits, stopped by an empty prepaid balance or a spend limit | Commercial |

Max is sold monthly only. A Team plan holds up to 150 seats, and each seat's limits belong to its member: one member reaching a limit does not stop the others, and the support article on Team plans states that "each seat is for one named individual." Legacy seat-based Enterprise plans have per-seat allowances like Team's; the usage-based Enterprise plan has none.

The weekly limit is the one Anthropic does not quantify. Each plan's weekly limit "applies across all models", resets at a day and time assigned to the account, and shows in Settings > Usage on claude.ai, but no support article gives it as a multiple of Pro's. A plan with twenty times Pro's session allowance is therefore not documented to have twenty times Pro's week. Anthropic also reserves the right to "limit your usage in other ways, such as weekly and monthly caps or model and feature usage, at our discretion." On 14 September 2026 it set Claude Code's weekly limits 25% above their level before a summer promotion, on Pro, Max, Team and seat-based Enterprise plans.

Fable, the model tier above Opus, has rules of its own. On Max plans and Team Premium seats, Fable 5 and Fable 5.1 may use up to half of the weekly allowance; past that, a session can carry on with Fable on [usage credits](#usage-credits), if they are turned on, or switch to another model and stay within the plan. On Pro and Team Standard seats, Fable bills to usage credits from the first request. An interactive session asks once before Fable requests start billing usage credits and not again after the first yes, while a `claude -p` run, Claude Code's non-interactive mode, bills them without asking.

## What draws on the allowance

The allowance is spent by the work each message causes, so messages differ widely in cost. Anthropic's support articles list message and conversation length, attachments, tool use, the model and the effort level among the factors, and say that usage on claude.ai, Claude Code and the desktop app "counts towards the same usage limit."

A Claude Code turn is large by chat standards. Each request resends the conversation so far, the instruction files, and every file Claude has read in the session, so a long session costs more per message as it goes on. [Prompt caching](/wiki/ai/prompt-caching) makes the repeated prefix cheaper without removing it. Anthropic's guide to usage in Claude Code calls starting a fresh conversation with `/clear` when the task changes "the single most effective lever for both quality and cost."

The model is the other large factor. The same guide calls Sonnet "the right choice for the large majority of coding work" and says that Opus "uses meaningfully more of your quota, so consider switching to Sonnet for routine work." On the API, Opus 5.5 costs $4 per million input tokens and $20 per million output tokens, twice Sonnet 5.5's $2 and $10; Fable 5.1 costs $10 and $50. The `opusplan` model setting runs Opus while Claude Code is in plan mode and Sonnet for the edits that follow, which puts the expensive model on the planning step only.

## When an allowance runs out

Claude Code warns first, with a line such as `You've used 85% of your session limit · resets 3:45pm`. At the limit it stops sending requests and prints one of four messages:

```text
You've hit your session limit · resets 3:45pm
You've hit your weekly limit · resets Mon 12:00am
You've hit your Opus limit · resets 3:45pm
You've hit your Sonnet limit · resets 3:45pm
```

The session and weekly limits count every model together, so switching models with `/model` does not restore access. The Opus and Sonnet limits count one model family, and a switch to a model outside that family keeps the session going.

What happens next depends on the plan and on what the subscriber has turned on:

| Mechanism | Effect | Conditions |
| --- | --- | --- |
| Wrap-up allowance | A response already in progress at the five-hour limit continues briefly to a stopping point, shown as `Usage limit reached · wrapping up` | Once per weekly period on Pro, at every five-hour limit on Max and Team Premium seats; counts against the weekly limit; Claude Code 2.1.277 or later; not on API keys or cloud providers; still rolling out |
| Waiting | Claude Code waits in the open session and continues the interrupted task after the reset | Interactive sessions signed in with a subscription; the `/config` setting *Continue automatically at usage limit* turns it off |
| Limit reset | Refills the five-hour or the weekly limit at once | Granted occasionally to eligible plans; spent from Settings > Usage in a browser or the desktop app, not from a terminal |
| Usage credits | Requests continue, billed at API rates | Turned on in Settings > Usage or with `/usage-credits`, before the limit or when it arrives; Team and Enterprise members without billing access request them from an admin |
| Upgrade | The larger plan's limits apply from the moment of the upgrade | Pro to Max, or Max 5x to Max 20x |

## Usage credits

Usage credits switch requests to pay-as-you-go billing at standard API rates once one of the plan's limits is spent, and the usage notification changes to "Now using credits." They are enabled in Settings > Usage on claude.ai, or with `/usage-credits` from Claude Code. They are prepaid, optionally refilled by auto-reload, and stopped by a monthly spend limit the subscriber sets. The limits themselves reset on their usual schedule.

Credits bought in bundles cost less. On Pro, Max and Team plans, $45 buys $50 of credit, $200 buys $250, and $700 buys $1,000, a discount of 10%, 20% and 30%. Pro and Max subscribers can buy up to $2,000 of discounted bundles a month, and Team owners up to $3,000; usage past that is billed at the standard rate. In most places credits do not expire; in some jurisdictions, Japan among them, they expire six months after purchase, a rule in force since 10 September 2026.

## API credits on Max and Team

Max and Team plans also include a monthly credit for the Claude API, separate from the subscription allowance and claimed into one Claude Console organization the subscriber links:

| Plan | Monthly API credit |
| --- | --- |
| Max 5x | $100 |
| Max 20x | $200 |
| Team, Standard seat | $20 per seat |
| Team, Premium seat | $100 per seat |

A Team's credits are pooled into one balance capped at $500 a month. The credit becomes claimable after seven days on the plan and lapses at the end of each billing cycle. It covers the Claude API, Claude Managed Agents, the Claude Agent SDK, and `claude -p` runs that authenticate with an API key from the linked organization. It does not cover interactive Claude Code in the terminal, an editor, the desktop app or the web, which stays on the plan's allowance, and it cannot pay for usage credits.

## Reading the meters

| Where | What it shows |
| --- | --- |
| `/usage` in Claude Code (aliases `/cost`, `/stats`) | The plan's usage bars and reset times; for an API key, the session's cost at list price |
| Settings > Usage on claude.ai | The session and weekly bars, the Fable bar where it applies, the weekly reset time, and usage-credit spend |
| A custom status line | `rate_limits.five_hour` and `rate_limits.seven_day`, each with `used_percentage` and `resets_at`, after a session's first response, for Pro and Max subscribers |
| `claude auth status` | Which credential and directory a session would use; no usage figures |

In a terminal, the status line is the only meter that stays on screen while Claude works. [One config directory per account](/wiki/ai/claude-accounts/config-directories#label-each-session-with-its-account) has a script that prints the account's name beside the two percentages.

## Related

- [Multiple Claude accounts](/wiki/ai/claude-accounts): why one person runs several accounts, and the map of this section.
- [Using multiple accounts cost-effectively](/wiki/ai/claude-accounts/cost-model): the prices on this page compared in one unit.
- [Prompt caching & cost](/wiki/ai/prompt-caching): why a long session's repeated prefix costs less than its first turn.

## Further reading

- Anthropic, [What is the Pro plan?](https://support.claude.com/en/articles/8325606-what-is-the-pro-plan), [What is the Max plan?](https://support.claude.com/en/articles/11049741-what-is-the-max-plan) and [What is the Team plan?](https://support.claude.com/en/articles/9266767-what-is-the-team-plan)
- Anthropic, [Models, usage, and limits in Claude Code](https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code)
- Anthropic, [Manage usage credits for paid Claude plans](https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans) and [Buy usage bundles](https://support.claude.com/en/articles/14246112-buy-usage-bundles)
- Anthropic, [Monthly API credits for Max and Team plans](https://support.claude.com/en/articles/17154008-monthly-api-credits-for-max-and-team-plans)
- Anthropic, [Claude Fable models on your plan](https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan) and [Claude Code Wrap-Up Allowance](https://support.claude.com/en/articles/17040437-claude-code-wrap-up-allowance)
- Anthropic, [Errors: You've hit your session limit](https://code.claude.com/docs/en/errors#youve-hit-your-session-limit) and [Status line: rate limit usage](https://code.claude.com/docs/en/statusline#rate-limit-usage)
- Anthropic, [Pricing](https://platform.claude.com/docs/en/about-claude/pricing) (API, per million tokens)
