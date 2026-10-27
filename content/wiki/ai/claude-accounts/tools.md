---
title: "Tools for Multiple Accounts"
weight: 60
---

Public tools for running [Claude Code](/wiki/ai/context-engineering/claude-code) on more than one account come in four kinds. Usage trackers read Claude Code's local transcripts and report usage per account. Account switchers store several logins and change which one Claude Code uses. Subscription-pooling proxies sit between Claude Code and Anthropic, hold several subscriptions, and send each request out on whichever one has room. Routers and gateways put a different credential, or a different model provider, behind Claude Code. Anthropic's terms contain nothing that bears on the trackers, while a Usage Policy clause that takes effect on 12 November 2026 describes what the proxies do. Each project below was checked against its repository on 26 October 2026.

## At a glance

| Tool | Kind | Mechanism | Standing under the terms |
| --- | --- | --- | --- |
| `CLAUDE_CONFIG_DIR`, `claude auth`, `/usage`, status line | Built in | One configuration directory per login | Documented by Anthropic |
| ccusage | Tracker | Reads transcripts and prices their tokens at list rates | Reads local files only |
| Claude Code Usage Monitor | Tracker | Reads transcripts and the status line's official percentages | Reads local data only |
| claude-swap | Switcher | Stores each account's login, starts sessions as any of them, and can rotate between them automatically | Manual switching among one's own accounts is ordinary; automatic rotation is getting around limits "through multiple accounts", which the wrap-up allowance terms (below) name |
| CC Switch | Switcher | Rewrites Claude Code's provider settings: endpoint, key and model | Depends on the provider chosen; resold relays are prohibited |
| ccflare, better-ccflare, TeamClaude | Proxy | Hold several subscription logins and spread requests across them | Matches what the November 2026 Usage Policy clause prohibits, as written |
| Claude Code Router | Router | Local gateway to other companies' models | Uses other providers' keys; Anthropic does not support non-Claude models behind Claude Code |
| LiteLLM, Claude apps gateway | Gateway | Per-developer keys and spend caps in front of one provider account | Documented by Anthropic for organizations |

## Built into Claude Code

Anthropic's own pieces cover the basics: `CLAUDE_CONFIG_DIR` for one directory per account, `claude auth login` and `claude auth status` to sign each in and check it, `/usage` and the status line's `rate_limits` fields for the meters, and `apiKeyHelper` for keys. [One config directory per account](/wiki/ai/claude-accounts/config-directories) puts them together. Organizations get more: Team and Enterprise plans have per-member usage credits and spend caps, and managed settings, which an organization deploys to its machines and which users' own settings cannot override, can set `forceLoginOrgUUID`, after which Claude Code reports an error and exits at startup when the claude.ai login in use belongs to any other organization.

## Usage trackers

ccusage, run with `npx ccusage@latest`, reads the transcripts under `projects/` in a configuration directory and reports tokens and API-equivalent cost by day, week, month or session. With `CLAUDE_CONFIG_DIR` set to one directory it reports one account, and with a comma-separated list it reports several together. `ccusage blocks` groups usage into five-hour blocks counted from the first message, the tool's own reconstruction of the session window, and `ccusage statusline` prints a compact line for Claude Code's status bar. The live dashboard of earlier versions, `blocks --live`, was removed in version 18. The tool reads local files, and with `--offline` it also skips fetching current model prices. [Using multiple accounts cost-effectively](/wiki/ai/claude-accounts/cost-model#measure-usage-in-api-equivalent-dollars) shows how to read its figures.

Claude Code Usage Monitor, installed with `uv tool install claude-monitor` and run as `claude-monitor`, is a terminal dashboard of the current five-hour window with a forecast of when it will run out. Its fourth major version can also serve as an account's status-line command (`claude-monitor --statusline`), capturing the official `rate_limits` percentages and labelling each figure as official or as a local estimate. Its plan presets carry the project's own token estimates, such as 88,000 tokens for Max 5x and 220,000 for Max 20x. Anthropic publishes no token figures for any plan, so the official percentages are the ones to trust.

## Account switchers

claude-swap, installed with `uv tool install claude-swap` and run as `cswap`, keeps a copy of each account's login: sign in with Claude Code, run `cswap add`, and repeat for the next account. `cswap run 2` starts Claude Code as account 2 in that terminal only, sharing the default `~/.claude` setup but keeping a separate chat history, and `cswap map` binds a directory to an account so that `cswap run` there picks it. `cswap switch` changes the default login itself, holding Claude Code's credential locks while it writes. The README warns against running `/logout` before adding the next account, because Claude Code may revoke the stored token of the account being left.

`cswap auto` goes further. It polls each account's usage and moves the default login to another account before the current one reaches its limit, with strategies such as spending first the account whose week resets soonest. Claude Code's wrap-up allowance, a small, capped extension that lets a response already in progress continue briefly to a stopping point at the five-hour limit, has terms that give "an attempt to get around usage limits (for example, through multiple accounts or automation designed to exploit the allowance)" as grounds for withholding it, and rotation across accounts is the first of those examples. Switching to carry on past a limit is the case [What the terms allow](/wiki/ai/claude-accounts/terms#getting-past-usage-limits) marks as contested. Without `auto`, claude-swap offers what one configuration directory per account offers, with more convenience, in exchange for a third-party program holding every account's tokens.

CC Switch is a desktop app that switches the API provider behind Claude Code and several other coding agents by rewriting their configuration: the endpoint, the key and the model, leaving plugins, hooks and Model Context Protocol (MCP) server settings in place. It ships more than ninety provider presets, among them other companies' models behind Anthropic-compatible endpoints and what its README calls community relays. Sponsor notices in the same README advertise Claude Code access at a fraction of the official price, which is the resold access covered below.

## Subscription-pooling proxies

ccflare, its fork better-ccflare, and TeamClaude run as local proxies. Claude Code is pointed at the proxy instead of at Anthropic, the proxy holds the login tokens of several Claude subscriptions, and each request goes out on one of them. When an account nears its limit or answers with a rate-limit error, the next request goes out on another. TeamClaude rotates at 98% of a five-hour or weekly limit by default, preferring the account whose weekly limit resets soonest; ccflare retries a rate-limited request on another account.

Claude Code's legal page says developers "may not collect, store, or intermediate Claude.ai credentials or session tokens", and the Usage Policy that takes effect on 12 November 2026 forbids providing access to Claude "through unauthorized means, including services that route requests through consumer subscriptions". TeamClaude's compliance notes argue that a proxy one person runs for their own subscriptions is consistent with the terms; the documents contain no exception for that case, and the wrap-up allowance terms list getting around usage limits "through multiple accounts" among the grounds for withholding that allowance. better-ccflare's README states that Anthropic bans subscription logins used outside Claude Code, and the proxy keeps those accounts away from its traffic for other agents.

## Routers and gateways

Claude Code Router is a local gateway that gives Claude Code one endpoint and forwards each request to a provider chosen by rule, among them Anthropic, OpenRouter, DeepSeek and Gemini, with fallbacks, key rotation and pools of credentials. Its savings come from other companies' models, and it adds no Claude capacity. Anthropic's gateway documentation says it "doesn't support routing Claude Code to non-Claude models through any gateway", so Claude Code's behaviour on another model is undocumented. A credential pool filled with Claude subscription logins would make the router a pooling proxy, with the same standing.

For an organization that pays per token, a gateway is the documented way to run many people on one bill. Claude Code reaches one through `ANTHROPIC_BASE_URL` and a gateway credential, or through `/login` for Anthropic's own gateway; either way requests are billed to the account behind the gateway, and no subscription is used. LiteLLM, an open-source gateway, issues virtual keys and tracks spend per key; Anthropic's cost documentation reports that several large enterprises use it, while noting it is unaffiliated with Anthropic and unaudited. Anthropic's Claude apps gateway serves organizations on Amazon Bedrock, Google Cloud, Microsoft Foundry and Claude Platform on AWS, signs developers in through the organization's single sign-on (SSO), and caps each developer's spend by day, week or month.

## Resold access

Some services sell Claude Code access below Anthropic's prices, in the form of an endpoint and a key for Claude Code's `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN` variables. Claude Code sends each request's full context to that endpoint, so the operator receives every prompt, every file Claude reads and every command output in the session, which for client or employer code is a disclosure to an unknown party. A relay configured with `ANTHROPIC_BASE_URL` alone is worse: with no gateway credential set, the saved claude.ai login stays the active credential, so requests go to the relay under the subscriber's own login. The Consumer Terms prohibit reselling access, Claude Code's legal page already forbids third-party developers to "route requests through Free, Pro, or Max plan credentials on behalf of their users", and the Usage Policy adds its clause on services that route requests through consumer subscriptions on 12 November 2026. Anthropic's own routes to Claude are its subscriptions, usage credits, API keys and the cloud providers.

## Related

- [One config directory per account](/wiki/ai/claude-accounts/config-directories): the built-in mechanism the switchers automate.
- [What the terms allow](/wiki/ai/claude-accounts/terms): the clauses quoted on this page, in full.
- [Using multiple accounts cost-effectively](/wiki/ai/claude-accounts/cost-model): what the trackers' figures mean for choosing a plan.
- [MCP](/wiki/ai/mcp): the Model Context Protocol, whose servers these tools copy between accounts or leave behind.

## Further reading

- [ccusage](https://github.com/ccusage/ccusage) and [Claude Code Usage Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor)
- [claude-swap](https://github.com/realiti4/claude-swap) and [CC Switch](https://github.com/farion1231/cc-switch)
- [ccflare](https://github.com/snipeship/ccflare), [better-ccflare](https://github.com/tombii/better-ccflare) and [TeamClaude](https://github.com/KarpelesLab/teamclaude), with TeamClaude's [compliance notes](https://github.com/KarpelesLab/teamclaude/blob/master/docs/compliance.md)
- [Claude Code Router](https://github.com/musistudio/claude-code-router) and [LiteLLM](https://github.com/BerriAI/litellm)
- Anthropic, [Run Claude Code through a gateway](https://code.claude.com/docs/en/gateways) and [Claude apps gateway spend limits](https://code.claude.com/docs/en/claude-apps-gateway-spend-limits)
