---
title: "Using a Claude Code Plugin"
weight: 10
---

A Claude Code plugin is a directory that the harness can install, namespace, version, and reload as a unit. It is the packaged form of the same building blocks the harness already loads from `.claude/`: slash commands, [skills](/wiki/ai/context-engineering#just-in-time-retrieval), [subagents](/wiki/ai/agentic-workflows#sub-agent-delegation), [hooks](/wiki/ai/context-engineering/claude-code#pick-the-cheapest-mechanism-that-works), [MCP](/wiki/ai/mcp) servers, and a handful of less-common pieces (LSP servers, background monitors, on-`PATH` binaries, default settings). The difference is one of *distribution and lifecycle* rather than capability — anything a plugin does you could also do by hand in a project's `.claude/`. The reason to use a plugin is that you don't want to.

This page is about consuming plugins others have packaged. [Authoring a plugin](/wiki/ai/plugins/authoring) covers the production side.

## Anatomy

A plugin is a directory containing a `.claude-plugin/plugin.json` manifest and any of the component directories below it:

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # name, description, version, author
├── skills/
│   └── <skill-name>/
│       └── SKILL.md         # YAML frontmatter + instructions
├── agents/                  # subagent definitions
├── hooks/
│   └── hooks.json           # event handlers (same shape as settings.json hooks)
├── .mcp.json                # MCP server configurations
├── .lsp.json                # LSP server configurations
├── monitors/
│   └── monitors.json        # background commands that stream into the session
├── bin/                     # executables added to PATH while enabled
└── settings.json            # plugin-managed default settings
```

Two specifics worth pinning down because they trip people up:

- **`commands/` is the older flat form; `skills/` is the new one.** Both work. New plugins should use `skills/` because it supports a `SKILL.md` body, [progressive disclosure](/wiki/ai/context-engineering#just-in-time-retrieval), and tool restrictions.
- **Only `plugin.json` lives inside `.claude-plugin/`.** Putting `skills/` or `hooks/` inside that directory is the single most common authoring mistake; the harness will silently not find them.

The manifest itself is small — name, description, version, optional author. The `name` is the namespace: a skill called `review` inside a plugin called `quality-tools` is invoked as `/quality-tools:review`. Namespacing is unconditional; it is what lets two plugins ship the same skill name without colliding.

## Installing

Two installation routes, both via the `/plugin` command:

- **From a marketplace.** `/plugin marketplace add <source>` registers the catalog (a git repo containing a `.claude-plugin/marketplace.json`); `/plugin install <plugin-name>@<marketplace-name>` installs one. Updates pull with `/plugin marketplace update`.
- **From a local directory or URL.** `claude --plugin-dir ./my-plugin` loads a plugin for one session without installing it. `--plugin-url` does the same with a hosted `.zip`. These are the development paths; for ongoing use a real install is cheaper to manage.

Two marketplaces are present out of the box:

- **`claude-plugins-official`** — Anthropic's curated set, available automatically. Inclusion is at Anthropic's discretion; the bar is real.
- **`claude-community`** — third-party submissions that pass an automated safety and review pipeline. Added with `/plugin marketplace add anthropics/claude-plugins-community`; installs are scoped with `@claude-community`.

Beyond those, any git repository with a `.claude-plugin/marketplace.json` at its root is a valid marketplace; private repositories work the same way for team-internal distribution.

## Enabled, installed, and the reload cycle

A plugin can be installed and not enabled; the manifest is on disk but the harness is not loading its surface. Enabling makes the skills, hooks, MCP servers, monitors, and `bin/` entries active for the session. The split matters because [context cost](#context-cost-in-practice) is paid by the enabled set, not the installed set — installing aggressively and enabling sparingly is a real strategy.

`/reload-plugins` re-reads plugin files without restarting Claude Code. It is essential during plugin authoring; for consumers it is mostly useful after a marketplace update.

## Context cost in practice

The [parent page's ranking](/wiki/ai/plugins/#context-cost-is-the-central-tradeoff) of plugins as medium-to-high context cost is the right baseline; Claude Code's specifics shift the picture in both directions:

- **Skills are cheap until invoked.** A `SKILL.md` body does not enter the window; only its frontmatter `description` does, so the harness can route to it. A plugin that ships ten skills costs roughly ten short descriptions, not ten full bodies.
- **Tool schemas can be heavy.** A bundled MCP server with twenty tools puts twenty tool schemas in the prompt every turn — the kind of thing that quietly inflates the [stable prefix](/wiki/ai/prompt-caching) until the [cache benefit](/wiki/ai/prompt-caching) is undone by sheer volume.
- **Hooks, monitors, and `bin/` are zero context cost at idle.** They are deterministic plumbing the model never reads; they only enter the session when they fire or output. A plugin made entirely of these is essentially free from the context perspective — its cost is on your machine, not in your prompt.
- **Some surfaces are deferred.** The harness can list tool *names* up front and load full schemas only on demand; when this is in effect, a plugin's per-turn footprint is just the names. Treat this as a nice-to-have rather than a guarantee — design your enabled set as if every schema is always present.

The composite rule: prefer plugins whose surface is skills and hooks over plugins whose surface is dozens of MCP tools, and prune the enabled set on long-running sessions. Long sessions re-read everything every turn; an extra plugin is paid for many times.

## Security: a plugin runs code on your machine

The trust model is the only thing about plugins worth being unhappy about by default. A plugin can:

- Run shell commands on every matched tool call (hooks).
- Start a long-running local process that sees your tool inputs and outputs (MCP servers).
- Stream output into your conversation from arbitrary commands (monitors).
- Add executables to the `PATH` the Bash tool resolves against (`bin/`).
- Force-enable or force-disable settings, including which agent runs as the main thread.

This is closer to `brew install` than to a browser extension. The defensible practice mirrors what you would do for any third-party code:

- **Audit before enabling.** Open `plugin.json`, `hooks/hooks.json`, `.mcp.json`, and `bin/`. A trustworthy plugin is short and obvious in these files; a sprawling one deserves scrutiny.
- **Pin a specific version.** Set the explicit `version` field in the marketplace entry or install at a known commit. Drift is the failure mode you can least observe.
- **Prefer first-party for anything privileged.** Curated marketplaces have an actual review pipeline; community marketplaces have a low bar by design. For plugins that touch credentials, prod systems, or money, default to the curated set.
- **Run untrusted plugins in a sandbox.** The same logic [agentic-engineering applies to tool execution](/wiki/ai/agentic-engineering#guardrails-and-the-irreversible-action-problem) applies one layer up: if you cannot read the plugin's code, run the harness in an isolated environment until you can.

## Managing the plugin set day to day

A few habits keep the surface from sprawling:

- **Disable what you are not using this week.** Installation is cheap; enablement is what costs context. The set you actually need across a project is usually small.
- **Treat marketplace updates like dependency updates.** `/plugin marketplace update` can pull behavior changes you did not write. Look at the diff before enabling the new version on a session where it matters.
- **Keep project-specific knowledge in `.claude/`, not plugins.** A plugin installs everywhere it is enabled; convention that belongs to one repo belongs in [that repo's rules and `CLAUDE.md`](/wiki/ai/context-engineering/claude-code#durable-instructions-claudemd-and-rules), not in a portable package.

## Pitfalls, by severity

Ordered worst-first — the early items can compromise your environment; the later ones only waste capacity.

1. **Enabling a plugin you have not read.** Hooks, MCP servers, `bin/` entries, and forced settings all run with your privileges the moment the plugin is enabled. The blast radius is whatever the harness can reach. Mitigation: read the manifest and the hook/MCP definitions before enabling; pin to a known version; prefer curated marketplaces for anything privileged.
2. **MCP tool flood.** A plugin (or several) bundles dozens of MCP tools whose schemas land in the window every turn. The cache hits, but the prompt is fat; the model spends attention on tools it never uses and the cost line creeps up. Mitigation: prefer skill-based plugins, disable heavy MCP-bundling plugins between sessions, watch the per-task cost trend not the unit price.
3. **Overlapping skill surfaces.** Two plugins both offer a "review" skill; the model picks one that *almost* fits the situation. Namespacing prevents the literal name clash but not the semantic overlap, which is the harder failure. Mitigation: keep the enabled set small and skill descriptions specific; use namespaces in your prompt when ambiguity matters.
4. **Forgetting `/reload-plugins` during development.** You change a plugin, the harness keeps using the cached version, and you debug behavior the file no longer has. The least severe — only your time is wasted — but the most common during authoring. Mitigation: reload after every change; or use `--plugin-dir` which reloads naturally between sessions.

## Practical checklist

- Install via marketplace for ongoing use; use `--plugin-dir` for development and trial.
- Prefer the curated marketplace for plugins that touch credentials or production.
- Read `plugin.json`, `hooks/hooks.json`, and `.mcp.json` before enabling anything from a community source.
- Pin to an explicit `version` rather than tracking a moving `main`.
- Enable the small set you actually need; disable the rest to keep the prompt slim.
- Prefer skill-based plugins over MCP-tool-heavy ones for long sessions.
- Keep project-specific conventions in `.claude/`; reserve plugins for capabilities that travel.
- Run `/reload-plugins` after marketplace updates; check the diff on plugins that act privileged.

## Related

- [AI plugins](/wiki/ai/plugins) — the section parent: bundling, landscape, trust.
- [Authoring a plugin](/wiki/ai/plugins/authoring) — the production side, including why packaging pays off for solo use.
- [Context engineering › Claude Code](/wiki/ai/context-engineering/claude-code) — the harness that loads what a plugin ships.
- [MCP](/wiki/ai/mcp) — the tool-server protocol many plugins wrap.
- [Prompt caching & cost](/wiki/ai/prompt-caching) — why every enabled plugin is paid for on every turn.

## Further reading

- Anthropic, [Discover and install plugins](https://code.claude.com/docs/en/discover-plugins)
- Anthropic, [Plugins overview](https://code.claude.com/docs/en/plugins)
- Anthropic, [Plugins reference](https://code.claude.com/docs/en/plugins-reference)
- Anthropic, [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
