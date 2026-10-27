---
title: "Using Multiple Accounts Cost-Effectively"
weight: 50
---

Among the individual plans that include [Claude Code](/wiki/ai/context-engineering/claude-code), Max 20x buys the most usage per dollar. At $200 a month it allows twenty times the usage of the $20 Pro plan in each five-hour session, twice the rate of Pro and Max 5x at their monthly prices. On Anthropic's published figures, no combination of smaller subscriptions matches it: two Max 5x subscriptions cost the same $200 and allow half as much, split across two accounts. Past Max 20x, Anthropic sells two routes to more usage: [usage credits](/wiki/ai/claude-accounts/plans-and-limits#usage-credits), billed at API rates once a plan's limit is spent and up to 30% cheaper in bundles, and API keys at list price. A second subscription opened to keep working past the first one's limits is the [contested case](/wiki/ai/claude-accounts/terms#getting-past-usage-limits) under Anthropic's terms.

Several accounts lower a bill in other ways. Work for an employer or a client goes on that organization's account and is billed to it, through a [Team seat](/wiki/ai/claude-accounts/layouts#a-team-on-team-seats) it pays for or an API key it issues. A script that runs Claude Code on an API key is billed per token and leaves the subscription's allowance to interactive work. Max 5x includes $100 and Max 20x $200 a month of [API credit](#scripts-on-the-included-api-credit), which Anthropic's FAQ says can pay for such runs. Each account's plan is then chosen for the work that account alone carries, by the arithmetic below. An extra credential can raise a bill as well: an [API key exported in a shell profile](/wiki/ai/claude-accounts/credentials#an-exported-api-key) is billed per token for every non-interactive `claude -p` run, ahead of a signed-in subscription and without a prompt.

Choosing among a larger plan, usage credits and an API key takes arithmetic, because each is priced in its own unit: plans as multiples of Pro's allowance per five-hour session, credits and keys in dollars per million tokens. The sections below compare them in one unit, the API-equivalent cost: what a piece of work would have cost on an API key at list price, computed from the token counts Claude Code records for every session.

## Prices in one table

| Route | Price per month | What it buys | Per-session allowance per $100 a month |
| --- | --- | --- | --- |
| Pro | $20 | Pro's allowance | 5 × Pro |
| Max 5x | $100 | 5 × Pro | 5 × Pro |
| Max 20x | $200 | 20 × Pro | 10 × Pro |
| Team, Standard seat | $25, or $20 billed annually | 1.25 × Pro | 5 × Pro, or 6.25 × annually |
| Team, Premium seat | $125, or $100 billed annually | 6.25 × Pro | 5 × Pro, or 6.25 × annually |
| Usage credits | List API price | Tokens | |
| Usage credits from a $1,000 bundle | $700 | $1,000 of tokens at list price | |
| API key | List API price | Tokens | |

Per dollar, every plan but one buys the same five-hour allowance, five times Pro's for each $100 a month, or 6.25 times on annual Team billing. Max 20x buys ten times, twice the rate of every other plan billed monthly. A Team plan needs at least two members, with seats of either type mixed freely. That is as far as the published figures go: Anthropic gives no multiple for the weekly limits, so the comparison covers the five-hour windows only. Team seats are also the only subscriptions in the table under the Commercial Terms, which matters more than the price for client and employer code; [plans and usage limits](/wiki/ai/claude-accounts/plans-and-limits) covers the difference.

The list prices for the current models, per million tokens:

| Model | Input | Output | Cache read |
| --- | --- | --- | --- |
| Fable 5.1 | $10 | $50 | $0.25 |
| Opus 5.5 | $4 | $20 | $0.20 |
| Sonnet 5.5 | $2 | $10 | $0.10 |
| Haiku 5.5, prompts up to 100,000 tokens | $0.10 | $0.50 | $0.01 |
| Haiku 5.5, prompts over 100,000 tokens | $0.50 | $2.50 | $0.05 |

A cache read is input that matches the start of a recently sent request. On a normal Claude Code turn the whole previous request is that prefix and only the latest exchange is new, so most of each request's input is billed at the cache-read rate. Haiku's price tier is set by the request's whole prompt, cached input included, so a long session moves to the second Haiku row. [Prompt caching & cost](/wiki/ai/prompt-caching) explains the mechanism.

## Measure usage in API-equivalent dollars

Claude Code records each session's token counts in its transcripts, so the API-equivalent cost of past work can be computed afterwards. ccusage, an open-source command-line tool, reads the transcripts and prices them at list rates, for one configuration directory or several:

```bash
# the default account
npx ccusage@latest claude monthly

# one other account
CLAUDE_CONFIG_DIR="$HOME/.claude-work" npx ccusage@latest claude monthly

# both accounts in one report
CLAUDE_CONFIG_DIR="$HOME/.claude,$HOME/.claude-work" npx ccusage@latest claude monthly
```

For a subscriber the figure is a counterfactual, money not spent that would have been on an API key. Claude Code deletes transcripts after 30 days unless `cleanupPeriodDays` is raised, so ccusage sees about a month of history by default. For a sense of scale, Anthropic's cost documentation reports that "across enterprise deployments, the average cost is around $13 per developer per active day and $150-250 per developer per month, with costs remaining below $30 per active day for 90% of users."

## Subscription or API key

When a month's API-equivalent cost is below a plan's price, an API key costs less than the plan; above it, the plan costs less, provided the work fits within the allowance. Anthropic's enterprise average of $150 to $250 a month starts above the Max 5x price and runs past Max 20x's. Whether a heavier month fits is something only the meters can show, because Anthropic publishes no allowance in tokens or dollars, and the API-equivalent cost of a full week on Max cannot be read off any page.

## Climbing the plan ladder

Usage credits turn an overflow into a number. A subscriber who enables them with a monthly cap sees, at the end of the month, what the work beyond the allowance cost at list price, and that figure can be set against the price of the next plan up:

| Step | Extra cost per month | Per-session allowance |
| --- | --- | --- |
| Pro to Max 5x | $80 | 1 × to 5 × Pro |
| Max 5x to Max 20x | $100 | 5 × to 20 × Pro |

If a month's usage-credit spend exceeds the step, the larger plan is the cheaper way to buy that usage, provided its allowance absorbs the overflow, and since Max is billed monthly, one month on the larger plan tests that. Bundles move the threshold: credits bought at 20% or 30% off make the same overflow cost 0.8 or 0.7 times as much.

As a worked example, a Max 5x subscriber ends a month with $160 of usage credits spent at list price. The step to Max 20x costs $100. Bought from the $250 bundle that sells for $200, the same $160 of credit would have cost $128, which is still more than $100, so a month on Max 20x is the cheaper experiment. A subscriber with $60 of overflow would keep Max 5x and buy credits.

## Two subscriptions or a bigger one

Two Max 5x subscriptions cost the same $200 as one Max 20x. They give ten times Pro's per-session allowance in two separate pools, where Max 20x gives twenty times in one. On the figures Anthropic publishes, one Max 20x buys twice as much for the same money, needs no second login, and raises no question under the terms. A claim that two smaller plans' weekly limits add up to more than one larger plan's cannot be checked against Anthropic's documents, which give no weekly figure for either.

A second subscription makes sense where it would exist anyway, as a boundary: a personal plan beside an employer's seat, or a business's plan beside its owner's personal one. Past Max 20x, the routes Anthropic sells are usage credits, up to 30% below list price in bundles, and API keys at list price. A second Max 20x for the same person's work is the contested route that [What the terms allow](/wiki/ai/claude-accounts/terms#getting-past-usage-limits) describes.

## Scripts on the included API credit

Max 5x includes $100 and Max 20x $200 a month of credit for the Claude API, claimed into one linked Console organization, the Claude Console account that holds API keys and their billing. The FAQ in Anthropic's article on the credit says it covers `claude -p` runs, Claude Code's non-interactive mode, "when you run them yourself with an API key from your linked Claude Console organization", and not interactive sessions. Anthropic's article on Claude Code with Pro and Max says more broadly that the credits "can't be used in Claude Code or the Claude apps", so the Console's billing page after a first run is where to confirm which balance it drew on. Moving scheduled and scripted runs onto such a key takes them off the subscription's allowance, which is then left to interactive work. At Sonnet 5.5's list price, $100 pays for 50 million input tokens or 10 million output tokens.

Each run reports its cost when started with `--output-format json`, in a `total_cost_usd` field, and `--max-budget-usd` stops a run once Claude Code's own estimate of its spend reaches the cap. The estimate can differ from the bill and a run can pass the cap, so the cap needs headroom. [Sessions on a subscription, scripts on a key](/wiki/ai/claude-accounts/layouts#sessions-on-a-subscription-scripts-on-a-key) has the setup.

## Spending less per task

Every route above prices capacity; the other lever is using less of it per task. The model sets the per-token rate: Sonnet 5.5 costs half as much as Opus 5.5, and Haiku 5.5, on prompts up to 100,000 tokens, a twentieth of Sonnet's input and output prices and a tenth of its cache-read price. Claude Code's `opusplan` setting runs Opus in plan mode and Sonnet for the edits that follow. Lowering the effort level reduces the tokens a model spends thinking, and `/clear` between unrelated tasks stops a session from resending the old conversation on every turn. [Claude Code](/wiki/ai/context-engineering/claude-code) and [context engineering](/wiki/ai/context-engineering) cover the habits that keep a session's context small.

## Related

- [Plans and usage limits](/wiki/ai/claude-accounts/plans-and-limits): the allowances, credits and bundles priced here.
- [Account layouts](/wiki/ai/claude-accounts/layouts): which of these routes each arrangement of accounts uses.
- [Agentic engineering](/wiki/ai/agentic-engineering#cost-engineering-at-scale): cost as an engineering metric for systems built on the API.

## Further reading

- Anthropic, [Pricing](https://platform.claude.com/docs/en/about-claude/pricing) and [claude.com/pricing](https://claude.com/pricing)
- Anthropic, [Manage costs effectively](https://code.claude.com/docs/en/costs) (Claude Code docs)
- Anthropic, [Buy usage bundles](https://support.claude.com/en/articles/14246112-buy-usage-bundles) and [Monthly API credits for Max and Team plans](https://support.claude.com/en/articles/17154008-monthly-api-credits-for-max-and-team-plans)
- [ccusage](https://github.com/ccusage/ccusage): documentation for its Claude Code reports and the `CLAUDE_CONFIG_DIR` list
