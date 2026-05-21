---
title: "Authoring a Plugin"
weight: 20
---

The first plugin most people author is for themselves: a few slash commands they keep re-creating in every new project, a hook they want everywhere, a [subagent](/wiki/ai/agentic-workflows#sub-agent-delegation) that has earned a permanent slot. The instinct is to keep that in `.claude/` because there is only one user. That instinct is usually right for *project-scoped* knowledge and usually wrong for *capabilities that travel* — and the reason has nothing to do with sharing.

This page is about producing plugins, with particular attention to the solo case. [Using a plugin](/wiki/ai/plugins/claude-code) covers the consumption side and the anatomy in detail.

## Why package even when the only user is you

Bundling buys things that survive your decision not to publish:

- **Cross-project portability without copy-paste.** A `.claude/` directory works in one repository. The same files as an installed plugin work in every repository you open. Without packaging, the third project you open is the project where you forgot to copy your skills over.
- **A real version number.** When the plugin changes behavior, you can decide whether each project picks it up. Pinning a version is how you avoid "the agent started doing something different yesterday and I don't know why." A folder of files in `.claude/` has no such handle.
- **Reloadable without restart.** `/reload-plugins` re-reads the surface in place. During iteration that turns a feedback loop measured in seconds into one measured in milliseconds — which is the difference between iterating and not bothering.
- **A clean interface forces the right factoring.** Writing a `plugin.json` and a manifested `skills/` directory makes you decide *what* the plugin is, the same way turning a script into a library makes you decide what the library exports. The pressure to name and bound things is a feature, not overhead.
- **Separation between project rules and reusable capability.** [Project rules](/wiki/ai/context-engineering/claude-code#durable-instructions-claudemd-and-rules) describe *this codebase* — its conventions, its build, its gotchas. A plugin describes *a capability* — a review workflow, a deploy helper, a research agent. Mixing them works at small scale and rots at large scale; the boundary is worth drawing early.

None of this requires another user. It is the same argument for turning a useful Bash function into a stand-alone script: lifecycle, portability, and the discipline of naming the thing.

## When *not* to author one

Packaging has its own carrying cost — a manifest to maintain, a version to think about, a place to keep it. Skip the plugin when:

- **The knowledge is project-specific.** Conventions about *this* codebase belong in *this* codebase's `CLAUDE.md` and `.claude/rules/`. A plugin that hard-codes one project's structure is wrong everywhere else it loads.
- **You are still experimenting.** Start in `.claude/`; the friction is lower. Promote to a plugin when the shape is stable. The docs even support this with a documented `.claude/` → plugin migration path.
- **It is a one-off.** A skill you will use twice for one task does not need a manifest. Write it as a quick prompt or a project-local skill and delete it after.

The decision is roughly the [generational consolidation](/wiki/ai/context-engineering/claude-code#memory-is-structured-note-taking-with-a-garbage-collector) logic this repository's rules describe: raw observation, then pattern, then promoted rule. A plugin is the same — Gen 0 is a prompt in chat; Gen 1 is a file in `.claude/`; Gen 2 is a packaged plugin. Promote on evidence of repeated use, not on aspiration.

## The minimum scaffold

The smallest useful plugin is a directory, a manifest, and one skill. Everything else is optional.

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── hello/
        └── SKILL.md
```

```json
// .claude-plugin/plugin.json
{
  "name": "my-plugin",
  "description": "One-line description shown in the plugin manager",
  "version": "0.1.0",
  "author": { "name": "Your Name" }
}
```

```markdown
<!-- skills/hello/SKILL.md -->
---
description: Greet the user warmly. Use when the user opens a new session.
---

Greet the user by name if known. Ask what they want to work on today.
```

Load and try it without installing:

```bash
claude --plugin-dir ./my-plugin
```

Invoke with the namespaced form, `/my-plugin:hello`. Edit `SKILL.md`, run `/reload-plugins`, try again. That is the entire development loop.

The components most commonly added on top, in roughly the order people reach for them:

- **Hooks** (`hooks/hooks.json`) — deterministic shell commands the harness fires on tool events. Lint-on-save, pre-commit checks, formatters. The schema is the same as the `hooks` block in `settings.json`, so an existing hook lifts in directly.
- **Subagents** (`agents/`) — named agents the model can delegate to with their own system prompt, tool set, and model choice. The cleanest packaging unit for a specialist behavior like a code reviewer or a research forager.
- **MCP servers** (`.mcp.json`) — external tool servers the plugin brings along. Useful for capabilities that are not just prompts — a real API, a database, a search backend.

The full surface (LSP, monitors, `bin/`, default `settings.json`) is documented in the [components inventory](/wiki/ai/plugins/claude-code#anatomy) on the consumer page; the principle is to add a component only when the cheaper form does not do the job.

## Distributing the plugin to yourself

A plugin installed via `--plugin-dir` works for one session; for ongoing use, give it the same lifecycle a published plugin gets, even if the audience is one.

A *personal marketplace* is the lightweight form: a single git repository containing one or more of your plugins plus a `.claude-plugin/marketplace.json` catalog at the root. Push it to a private GitHub repo. Add it on each machine you use:

```bash
/plugin marketplace add github:you/your-claude-plugins
/plugin install your-plugin@your-plugins
```

That gives you, the only user, the same `update`/`pin`/`enable`/`disable` controls a public marketplace gives a community. The marketplace file is small — `name`, `owner`, and a `plugins` array pointing at each plugin's directory — and adding a second plugin later is a one-line change.

## Versioning: explicit or per-commit

The `version` field in `plugin.json` is optional, and the choice has real consequences:

- **Set an explicit `version`** (e.g. `0.1.0`) and the harness only treats a release as new when the field changes. This is the right default once anything depends on the plugin's behavior — including your own muscle memory. Bumping the field is your decision to ship a change.
- **Omit `version`** and a git-hosted plugin treats every commit as a new version. Useful for fast solo iteration where you want every push picked up automatically; dangerous on anything where surprise behavior changes are bad.

A working pattern for solo use: omit `version` on a personal scratch plugin while you are still finding its shape, set it as soon as you would mind it changing under you.

## Migration from `.claude/`

The documented path from a project-local configuration to a plugin is mechanical: create `my-plugin/.claude-plugin/plugin.json`, copy `.claude/skills/` → `my-plugin/skills/`, copy `.claude/agents/` → `my-plugin/agents/`, lift any hooks from `.claude/settings.json` into `my-plugin/hooks/hooks.json` (the format is identical), and test with `--plugin-dir`. The plugin version takes precedence when loaded, so the original `.claude/` copies can be removed.

This is the path that makes the "start in `.claude/`, promote when it stabilizes" advice cheap. The migration is rote because nothing about the components changes — only their packaging does.

## Pitfalls, by severity

Ordered worst-first — the early items ship broken behavior; the later ones only slow you down.

1. **A plugin that assumes your project's layout.** Hard-coded paths, project-specific commands in hooks, or a skill that names files that exist only in one repo. It works where you wrote it and breaks silently elsewhere — exactly the failure plugins were meant to solve, inverted. Mitigation: if it depends on the project, it belongs in the project. A plugin's prompts should ask the environment, not assume it.
2. **Component directories inside `.claude-plugin/`.** Putting `skills/` or `hooks/` inside `.claude-plugin/` (which is meant to hold *only* the manifest) makes the harness silently fail to find them. The docs call this the single most common authoring mistake. Mitigation: `.claude-plugin/plugin.json` lives alone; every other directory sits at the plugin root.
3. **Forgetting to bump `version`.** A plugin with an explicit `version` only ships changes when the field changes. Push behavior changes without bumping it and downstream installs — including your other machines — silently stay on the old version. Mitigation: treat the version field like a release toggle; bump it whenever a consumer should pick the change up.
4. **Bundling an MCP server when a skill would do.** A skill is small, lazy-loaded, and costs almost nothing at idle. An MCP server is a process, has tool schemas in the prompt every turn, and adds a real install dependency. Reaching for the heavier form when the lighter one suffices makes the plugin worse for everyone who installs it, you included. Mitigation: try the skill first; promote to MCP only when there is a real external dependency or stateful interaction to manage.

## Practical checklist

- Author when the capability travels across projects, the lifecycle (version, reload, enable/disable) is worth having, or the boundary forces useful factoring — even with one user.
- Stay in `.claude/` for project-specific conventions, experiments, and one-offs.
- Smallest viable plugin: directory + `.claude-plugin/plugin.json` + one skill. Iterate with `--plugin-dir` and `/reload-plugins`.
- Keep only `plugin.json` inside `.claude-plugin/`; every other directory sits at the plugin root.
- Distribute to yourself via a personal git marketplace; install with `github:you/repo`.
- Set an explicit `version` as soon as anything depends on the plugin; bump it on every consumer-visible change.
- Promote to a plugin from `.claude/` once the shape is stable; the migration path is mechanical.
- Prefer skills and hooks; reach for MCP servers only when an external dependency genuinely justifies one.

## Related

- [AI plugins](/wiki/ai/plugins) — the section parent: bundling, landscape, trust, and the context-cost lens.
- [Using a Claude Code plugin](/wiki/ai/plugins/claude-code) — the consumer side and the full component inventory.
- [Context engineering › Claude Code](/wiki/ai/context-engineering/claude-code) — the harness whose extension hierarchy the plugin slots into.
- [Agentic workflows › Tool design](/wiki/ai/agentic-workflows#tool-design--the-agent-computer-interface) — the discipline a plugin's tool and skill surface should obey.
- [Prompt engineering](/wiki/ai/prompt-engineering) — wording the skill bodies, hook descriptions, and subagent system prompts the plugin ships.

## Further reading

- Anthropic, [Create plugins](https://code.claude.com/docs/en/plugins)
- Anthropic, [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- Anthropic, [Plugins reference](https://code.claude.com/docs/en/plugins-reference)
- Anthropic, [Skills](https://code.claude.com/docs/en/skills)
- Anthropic, [Subagents](https://code.claude.com/docs/en/sub-agents)
- Anthropic, [Hooks](https://code.claude.com/docs/en/hooks)
