---
paths:
  - "**"
---

# Self-Improvement

## Friction Detection

Proactively notice when interactions are clumsy, inefficient, or misaligned. Symptoms include:

- User has to repeat or rephrase a request
- User corrects an assumption or approach
- User expresses frustration or impatience
- A task takes multiple back-and-forth rounds when it should have been straightforward
- User overrides a tool call or rejects a permission prompt
- Output is too verbose or too terse for the situation
- Wrong level of abstraction chosen (too high-level, too detailed)

When you detect friction: hypothesize the root cause and save it as a **feedback** memory in `.claude/memory/friction/`. Include the hypothesis and enough context to evaluate it later. Tag the filename with the scope (see Scoping below).

## Generational Memory Consolidation

Friction memories follow a generational garbage-collector model:

### Gen 0 — Raw observations (friction/)
Individual friction events as they happen. These are cheap to write and ephemeral. Each is a single memory file in `.claude/memory/friction/`.

### Gen 1 — Patterns (patterns/)
When 2-3 related Gen 0 observations accumulate around a theme, consolidate them into a pattern file in `.claude/memory/patterns/`. Delete the consumed Gen 0 files. A pattern should name the recurring issue and the emerging rule.

### Gen 2 — Rules (promoted to .claude/rules/)
When a Gen 1 pattern has proven stable and general across multiple conversations, propose promoting it to a rules file in `.claude/rules/`. Confirm with the user before creating or modifying rules files, since these are checked into the repo and affect all future sessions.

### Consolidation triggers
- At the **start** of a conversation: scan Gen 0 memories. If any cluster is ready for Gen 1 promotion, do it.
- At the **end** of a substantial conversation: review what friction occurred and whether new Gen 0 entries are warranted.
- When the user explicitly asks to review friction/patterns.

## Scoping

Partition learnings by how broadly they apply. Use filename prefixes:

| Prefix | Scope | Example |
|--------|-------|---------|
| `global-` | Useful across all projects | `global-verbosity.md` |
| `project-` | Specific to this repo/project | `project-hugo-gotchas.md` |
| `topic-` | Narrow subject matter | `topic-solidity-examples.md` |

When promoting Gen 1 patterns to Gen 2 rules:
- `global-` patterns should go into the user's `~/.claude/CLAUDE.md` or equivalent cross-project config (confirm with user).
- `project-` patterns go into `.claude/rules/` in this repo.
- `topic-` patterns go into topic-scoped rules files (like the existing `solidity-examples.md`).

## What not to record

- One-off misunderstandings that were immediately clarified and unlikely to recur.
- Friction caused by external factors (slow network, tool bugs) rather than interaction patterns.
- Anything already captured in an existing rules file.
