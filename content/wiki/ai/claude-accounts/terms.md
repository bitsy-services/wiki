---
title: "What the Terms Allow"
weight: 20
---

Three documents govern a Claude account. The Consumer Terms of Service cover the Free, Pro and Max plans; the Commercial Terms of Service cover Team, Enterprise and API accounts; and the Usage Policy applies to everyone under either. The legal and compliance page for [Claude Code](/wiki/ai/context-engineering/claude-code) adds conditions on how its logins may be used. Read together, they let one person hold several accounts, forbid sharing a consumer account, restrict subscription logins to Anthropic's own apps, and in one place name multiple accounts as a way of getting around [usage limits](/wiki/ai/claude-accounts/plans-and-limits). The quotations below are from the versions published on 26 October 2026.

## Holding several accounts

Neither set of terms limits how many accounts one person holds, and the Usage Policy's rule on creating multiple accounts, quoted [below](#getting-past-usage-limits), concerns the purposes they are created for. Claude Code's documentation assumes that some people hold more than one: its authentication page explains how to stay "signed in to multiple accounts at once, such as work and personal accounts". In February 2026 a developer posted that Anthropic was "now going after people with multiple paid Max accounts". Thariq Shihipar, then an engineer on Anthropic's Claude Code team, replied the same day:

> a bit confused by the post, were they banned? I'll reach out on Reddit but we haven't changed anything here
>
> it's not against terms of service to have multiple MAX accounts, though sometimes people are using multiple MAX accounts to do things like resell tokens which of course is against terms of service

An account opened with an employer's email address can come under the employer's control. The Consumer Terms say that such an account "may be linked to the organization's Anthropic enterprise account, and the organization's administrator may be able to monitor and control the Account, including having access to Materials." A personal account needs a personal address.

## Sharing and reselling

The Consumer Terms forbid sharing outright: "You may not share your Account login information, Anthropic API key, or Account credentials with anyone else. You also may not make your Account available to anyone else." They also forbid using the services to "resell the Services", and the Commercial Terms forbid resale "except as expressly approved by Anthropic". Neither the Commercial Terms nor the Service Specific Terms they incorporate contain a rule against sharing: the Commercial Terms let a customer use the Services to serve its own "customers and end users", and the legal page allows an API key configured "for use by the customer's own authorized users", provided the usage "is billed to the key owner" and "is not resold or intermediated". Seats are the exception: Anthropic's support article on Team plans states that "each seat is for one named individual."

Anthropic connected sharing to its usage limits when it announced weekly limits in July 2025:

> In other cases, a small number of users are violating our usage policies by sharing and reselling accounts. This impacts capacity for all Claude users, and we're taking appropriate action to stop it.

A household or a team splitting one Max subscription is therefore the case the terms rule out, however the cost is divided. A company that runs Claude Code inside its own product may not pay for its users' usage either: the legal page requires each end user to sign in with their own API key, subscription or cloud-provider credential.

## Subscription logins outside Anthropic's apps

A subscription's login is an OAuth token, and the legal page limits where it may be used:

> OAuth authentication is intended exclusively for purchasers of Claude Free, Pro, Max, Team, and Enterprise subscription plans and is designed to support ordinary use of Claude Code and other native Anthropic applications.

It goes on to say that "developers may not collect, store, or intermediate Claude.ai credentials or session tokens," and that sign-in "must complete through Anthropic's own flow." In January 2026, as The Register reported, Shihipar said in a thread on X that Anthropic had taken steps to prevent third-party tools from "spoofing the Claude Code harness", and wrote that "third-party harnesses using Claude subscriptions create problems for users and are prohibited by our Terms of Service."

Scripted use of Claude Code on one's own subscription is anticipated by the documents. The Consumer Terms forbid access "through automated or non-human means, whether through a bot, script, or otherwise," except through an API key "or where we otherwise explicitly permit it," and the legal page states that "advertised usage limits for Pro and Max plans assume ordinary, individual usage of Claude Code and the Agent SDK." After a documentation change in February 2026 suggested otherwise, Shihipar wrote: "Nothing is changing about how you can use the Agent SDK and MAX subscriptions!" Anthropic's article on Max's API credits describes the same case from the billing side: for a user "signed in with your Claude plan", `claude -p` (Claude Code's non-interactive mode) "and Agent SDK usage still draw from your plan's usage limits". The condition that remains is the legal page's ordinary, individual usage. Products built for other people are a separate case: the legal page directs their developers to API keys or a cloud provider, and allows a platform to host an unmodified Claude Code that each end user signs in to with their own subscription.

## Getting past usage limits

No document says in so many words that a person may not open a second subscription when the first reaches its limit. The legal page ties the advertised limits to "ordinary, individual usage," quoted above.

The wrap-up allowance is a small, capped extension that lets a Claude Code response already in progress continue briefly to a stopping point when the five-hour limit arrives, described under [plans and usage limits](/wiki/ai/claude-accounts/plans-and-limits#when-an-allowance-runs-out). Its terms, published on 22 September 2026 as a supplement to both sets of terms, say:

> We may withhold the Wrap-Up Allowance from any account or organization if we determine there has been fraud, abuse, an attempt to get around usage limits (for example, through multiple accounts or automation designed to exploit the allowance), or a violation of these terms or our Usage Policy.

The Consumer Terms say users "must not abuse, harm, interfere with, or disrupt our Services, including, for example, introducing viruses or malware, spamming or DDoSing Services, or bypassing any of our systems or protective measures", a clause whose examples are attacks on the service.

The Usage Policy that takes effect on 12 November 2026 changes two clauses that bear on the question and adds a third. The first concerns multiple accounts. The version in force since 15 September 2025 forbids users to "coordinate malicious activity across multiple accounts to avoid detection or circumvent product guardrails or generating identical or similar inputs that otherwise violate our Usage Policy"; the November version adds the creation of accounts:

> Coordinate malicious activity across multiple accounts, or create multiple accounts, to avoid detection, circumvent product guardrails, or generate identical or similar inputs that otherwise violate our Usage Policy

Its purposes are evading detection, getting around guardrails, and repeating inputs that break the policy. The second clause concerns bypassing. The September version forbids users to "intentionally bypass capabilities, restrictions, or guardrails established within our products for the purposes of instructing the model to produce harmful outputs". The November version drops the purpose:

> Intentionally bypass or interfere with capabilities, restrictions, or guardrails established within our products, including by circumvention of the account sign-up or log-in process or by instructing the model to produce harmful outputs (e.g., jailbreaking or prompt injection), without prior authorization from Anthropic

This clause lists restrictions and guardrails as different things, and this page reads a usage limit as a restriction, governed by this clause. Read as a guardrail instead, a usage limit would bring a second account opened to get past it directly under the multiple-accounts clause, which forbids creating accounts to "circumvent product guardrails". The third clause is new in the November version:

> Resell, proxy, or otherwise provide access to Claude through unauthorized means, including services that route requests through consumer subscriptions or misrepresent the product or client being used

Read literally, then, the November text covers a deliberate attempt to get past a usage limit by any means Anthropic has not authorized, and the wrap-up terms name multiple accounts as one such means. Upgrading, usage credits and API keys are means Anthropic sells. A proxy that holds several subscriptions and spreads one person's requests across them routes requests through consumer subscriptions, which is the pattern the new resale-and-proxy clause describes.

TeamClaude, an open-source proxy that pools one person's subscriptions and rotates to the next account at 98% of a limit, argues the other side in its compliance notes. Its premise is that "Claude Code's own `/extra-usage` flow already offers signing into a *different* account when you hit a limit", from which it concludes that "the idea that using more than one of your own subscriptions is inherently off-limits is hard to square with the first-party client offering to do the same thing by hand." The current documentation describes a different flow. Claude Code's limit messages now point to `/usage-credits`, which turns on usage credits or requests them from an admin, and Anthropic's support article for Pro and Max subscribers who reach a limit lists upgrading, usage credits, waiting for the reset, and switching to "a Claude Console account" to "purchase API usage credits". Waiting is free and the other three are paid routes to more usage; none of them is a second subscription's allowance. The argument holds for owning several subscriptions, each signed in for its own work.

## Where common practices stand

| Practice | Standing |
| --- | --- |
| A work account and a personal account, each for its own work | Documented by Anthropic |
| Several subscriptions held by one person, each for its own projects | Not against the terms, per a Claude Code team member in February 2026; the November 2026 Usage Policy forbids creating multiple accounts only for the purposes it lists |
| One Pro or Max subscription, or one Team seat, shared by several people | Prohibited by the Consumer Terms, and by Anthropic's rule that each Team seat is for one named individual |
| A subscription login used by a third-party coding tool | Prohibited by the legal page |
| Signing in to a second subscription to continue work the first has run out of | Contested: the wrap-up terms give getting around limits through multiple accounts as grounds for withholding that allowance, and the November 2026 Usage Policy covers deliberate bypassing of product restrictions without Anthropic's authorization |
| Software that rotates one person's work across subscriptions as each nears its limit | Getting around limits through multiple accounts, which the wrap-up terms name; matches what the November 2026 bypass clause prohibits, as written |
| A proxy that pools subscriptions | Matches what the November 2026 resale-and-proxy clause prohibits, as written |

## Enforcement

Under the Consumer Terms, Anthropic "may suspend or terminate your access to the Services (including any Subscriptions) at any time without notice to you if we believe that you have breached these Terms," and a subscriber terminated for a violation is "not entitled to any refund." The legal page reserves the right to enforce its credential rules "without prior notice." The Consumer Terms point to Anthropic's trust and safety support center for appeals.

This page quotes the documents and is not legal advice. The documents change, and the next version of the Usage Policy takes effect on 12 November 2026.

## Related

- [Multiple Claude accounts](/wiki/ai/claude-accounts): the reasons for running several accounts, and the section map.
- [The cost of more capacity](/wiki/ai/claude-accounts/cost-model): the sanctioned routes to more usage, priced.
- [Tools for multiple accounts](/wiki/ai/claude-accounts/tools): the switchers and proxies these clauses apply to.

## Further reading

- Anthropic, [Consumer Terms of Service](https://www.anthropic.com/legal/consumer-terms) (effective 8 October 2025) and [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) (effective 17 June 2025)
- Anthropic, [Usage Policy](https://www.anthropic.com/legal/aup) (the version effective 12 November 2026; earlier versions under its version history)
- Anthropic, [Legal and compliance](https://code.claude.com/docs/en/legal-and-compliance) (Claude Code docs)
- Anthropic, [Claude Code Wrap-Up Allowance](https://support.claude.com/en/articles/17040437-claude-code-wrap-up-allowance) (22 September 2026)
- Anthropic, [post on X](https://x.com/AnthropicAI/status/1949898513019466140) (28 July 2025) on sharing and reselling accounts
- Thariq Shihipar, posts on X on [multiple Max accounts](https://x.com/trq212/status/2024230184287949207) and [the Agent SDK](https://x.com/trq212/status/2024212378402095389) (18 February 2026)
- Thomas Claburn, [Anthropic: No, absolutely not, you may not use third-party harnesses with Claude subs](https://www.theregister.com/2026/02/20/anthropic_clarifies_ban_third_party_claude_access/), The Register (20 February 2026)
- TeamClaude, [Compliance and terms of service](https://github.com/KarpelesLab/teamclaude/blob/master/docs/compliance.md)
