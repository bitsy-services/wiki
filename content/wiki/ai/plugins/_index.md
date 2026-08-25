---
title: "AI Plugins"
weight: 60
bookCollapseSection: true
---

An AI plugin is a bundled extension to an [agentic harness](/wiki/ai/context-engineering/claude-code) — slash commands, [skills](/wiki/ai/context-engineering#just-in-time-retrieval), [subagents](/wiki/ai/agentic-workflows#sub-agent-delegation), hooks, [MCP](/wiki/ai/mcp) servers, sometimes a default-agent activation — shipped as a directory with a manifest, versioned, and installable from a marketplace. The unit of distribution is the plugin; the unit of execution is the harness that loads it. Without the harness, the plugin is inert files; without plugins, the harness only sees what you wrote into its always-on configuration.

Plugins occupy a specific slot in the [stratified extension hierarchy](/wiki/ai/context-engineering/claude-code#pick-the-cheapest-mechanism-that-works): cheaper than baking a capability into every project, more expensive than a hook or rule because the plugin's tool surface generally has to be present each turn.

## Why bundle, instead of a raw MCP server or hand-rolled config

[MCP](/wiki/ai/mcp) standardizes how a model talks to an external tool server; a plugin standardizes how a *package* of extensions (one or more tool servers, plus the prompts, subagents, hooks, and skills that go around them) is named, versioned, installed, and reloaded. The difference shows up in three places:

- **Lifecycle.** A plugin can be installed, enabled, disabled, updated, and uninstalled as one thing. A loose collection of MCP servers, rule files, and shell scripts has to be re-assembled by hand in every checkout.
- **Distribution.** Plugins live in marketplaces — JSON catalogs in a git repository — and update by `git pull`. There is no equivalent for "the dozen tweaks in my `.claude/` directory."
- **Namespacing and conflict.** Two plugins can both define a `review` skill because the harness namespaces them by plugin (`/plugin-a:review`, `/plugin-b:review`). Hand-rolled configuration in a single project has no such isolation.

The relationship is the one a system package has to a loose script in `~/bin`. Both run; only one can be upgraded, pinned, and removed as a unit.

## The landscape

The term "AI plugin" is used loosely. The plugins this section is about are extensions to *agentic coding harnesses* — the long-running, tool-calling loops covered in [agentic workflows](/wiki/ai/agentic-workflows). The neighbouring uses:

- **Claude Code plugins.** Anthropic's harness, the case [the next page](/wiki/ai/plugins/claude-code) covers end to end. A first-party plugin system with an official curated marketplace and a community marketplace.
- **MCP servers.** The substrate, not a plugin format. A plugin in any harness frequently bundles one or more MCP servers; outside a plugin, an MCP server is configured directly.
- **Other harnesses' extensions.** Cursor and Continue have their own extension models; Cline reads project-level rule files. The vocabulary is similar but the manifest formats are not portable — a Claude Code plugin does not drop into Cursor.
- **ChatGPT Plugins (historical) and Apps.** OpenAI's earlier "ChatGPT Plugins" were retired in favor of GPTs and Apps. These are end-user-facing extensions to a chat product, not extensions to a coding agent, and a different problem from the one this section addresses.

The rest of this section focuses on the Claude Code lineage because it is the most fully specified case and the one running in this repository, but the patterns — bundling, namespacing, marketplace distribution, trust boundaries — generalize across harnesses.

## What a plugin costs per turn

A plugin's tools, skill descriptions, and agent definitions can land in the window every turn whether the model uses them or not. The [Claude Code page](/wiki/ai/context-engineering/claude-code#pick-the-cheapest-mechanism-that-works) ranks plugins and MCP as the *most* expensive extension mechanism by exactly this measure. Two refinements modern harnesses apply:

- **Progressive disclosure for skills.** A skill's body loads only when the model decides to invoke it; only the short description sits in the window all the time. A plugin made entirely of skills is far cheaper than one made of tools.
- **Deferred tool schemas.** A harness can list a plugin's tool *names* but defer the full JSON schema until the model asks to load it. When this is available, the per-turn cost collapses to a name list. When it is not, every plugin's full schema is in every prompt.

The practical rule: prefer plugins whose surface is skills and subagents over plugins whose surface is dozens of small tools, and install fewer plugins on long-running sessions than on short ones. A long session re-reads everything every turn (see [prompt caching](/wiki/ai/prompt-caching) for the economics), so the marginal cost of an extra plugin is paid many times.

## Trust and the supply-chain surface

A plugin can ship hooks (arbitrary shell commands run by the harness), MCP servers (long-running local processes that read tool output and call back), monitors (background commands that stream into your session), and `bin/` entries (executables added to your `PATH`). Installing one is closer to installing a Homebrew package than to installing a VS Code extension — the trust boundary is the same as for arbitrary code from the author.

The defensible model:

- **Pin the source.** Install from a specific commit or version, not a moving `main`, when the harness allows it. Drift in a plugin you trusted last week is drift in code that runs on your machine.
- **Read the manifest before enabling.** What hooks fire? What MCP servers start? What does `bin/` add to your `PATH`? These are short answers a manifest can give you; the alternative is finding out by surprise.
- **Prefer first-party or curated marketplaces for anything that touches secrets or production.** Community marketplaces are useful for low-risk capabilities; an unaudited plugin from one is the wrong place to source the thing that gets your AWS keys.

The mechanisms are dual-use: running real commands, hosting real servers, and modifying the agent's behavior are what a plugin is for and what an unsafe one exploits, and nothing in the manifest distinguishes the two. [Agentic engineering](/wiki/ai/agentic-engineering#guardrails-and-the-irreversible-action-problem) names the same trust model for tools generally; a plugin install applies it one layer earlier.

## Pitfalls, by severity

Ordered worst-first — the early items expose your system or money; the later ones only waste tokens.

1. **Installing a plugin you have not audited.** The plugin's hooks, MCP servers, and `bin/` entries run with your user's privileges. A malicious or compromised plugin is a foothold into whatever the harness can reach — credentials, source, deploy keys. The most dangerous failure because the harm is outside the agent's reasoning loop entirely. Mitigation: read the manifest before enabling, prefer curated marketplaces for sensitive workflows, pin to a known version.
2. **Plugin overload bleeding into wrong-tool selection.** Twenty enabled plugins each offering a `review`-ish or `deploy`-ish surface and the model picks one that *almost* fits. The same [tool-design failure](/wiki/ai/agentic-workflows#tool-design--the-agent-computer-interface) the agentic-workflows page warns about, made worse because the overlap is across plugins you forgot you installed. Mitigation: keep the enabled set small; disable plugins you are not actively using; rely on namespacing only as defence in depth.
3. **Context bloat from always-on tool schemas.** Every enabled plugin's tool schema lands in every turn, the stable prefix grows, and the [prompt cache hit rate](/wiki/ai/prompt-caching) is fine — but the prompt itself is now large enough to crowd out working room. Cheap per-token, expensive per-task. Mitigation: prefer skill-based plugins, disable heavy ones between sessions, watch the cost trend rather than the unit price.
4. **Reaching for a plugin when a project rule would do.** A constraint that applies to one project gets packaged as a reusable plugin and installs everywhere — including the projects where it is wrong. The least severe — the agent still works — but it noisily widens the agent's surface for no benefit. Mitigation: project rules in [`.claude/`](/wiki/ai/context-engineering/claude-code#durable-instructions-claudemd-and-rules) for project-scoped knowledge; plugins for capabilities that travel.

## In this section

- [Using a Claude Code plugin](/wiki/ai/plugins/claude-code) — anatomy, install, namespacing, context cost, and security applied to Anthropic's harness.
- [Authoring a plugin](/wiki/ai/plugins/authoring) — when packaging pays off even if you are the only user, and the minimum scaffold to get started.

## Related

- [Context engineering › Claude Code](/wiki/ai/context-engineering/claude-code) — the harness that loads the plugins; the extension hierarchy this page builds on.
- [MCP](/wiki/ai/mcp) — the tool-server protocol many plugins wrap or include.
- [Agentic workflows](/wiki/ai/agentic-workflows) — the loop a plugin's tools and subagents drop into.
- [Prompt caching & cost](/wiki/ai/prompt-caching) — why every enabled plugin is paid for on every turn.
- [Agentic engineering](/wiki/ai/agentic-engineering#guardrails-and-the-irreversible-action-problem) — the trust model the install step inherits.

## Further reading

- Anthropic, [Plugins overview](https://code.claude.com/docs/en/plugins)
- Anthropic, [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- Anthropic, [Discover and install plugins](https://code.claude.com/docs/en/discover-plugins)
- Model Context Protocol, [Specification](https://modelcontextprotocol.io/)
