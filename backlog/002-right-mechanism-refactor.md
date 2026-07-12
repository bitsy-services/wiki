# 002 — Right-mechanism refactor (skills / agents)

- **Priority:** P2
- **Status:** done (2026-07-12)

## Resolution

The premise turned out to be worse than described. `solidity-examples.md` was not
merely *loading always by omission* — it, and four other `wiki-*` rules, carried a
`globs:` frontmatter key. Claude Code's field is **`paths:`**. An unrecognized key
fails open, so every rule the author believed was scoped to `content/wiki/**` was
loading unconditionally into every session.

- `solidity-examples.md` now uses `paths: ["content/wiki/defi/**/*.md"]` — all 15
  pages with Solidity blocks are under `defi/`, so it now loads exactly when
  relevant and costs nothing otherwise.
- The other `wiki-*` rules had their dead `globs:` key removed and stay always-on
  *honestly*. They are ~40 lines combined and every session in this repo writes
  wiki content, so path-scoping them would save nothing and risks loading them too
  late to inform planning. Total always-on instruction budget is 175 lines, inside
  the 200-line guidance.
- `.claude/skills/new-wiki-page/SKILL.md` — the page-creation *procedure* (a
  procedure, not a fact, so a skill and not a rule). Loads on demand.
- `.claude/agents/wiki-reviewer.md` — fresh-context review pass, tools limited to
  Read/Grep/Glob/Bash.

## Problem

`.claude/rules/solidity-examples.md` is loaded into context **every session**
but is only relevant when writing DeFi-section pages with Solidity. That is
sometimes-knowledge living in always-on context — the same anti-pattern the
harness audit flagged, in miniature. The cost ladder says sometimes-knowledge
belongs in a skill (load-on-demand), not a rule (load-always). Separately, the
Claude Code wiki page calls subagent delegation "the single strongest lever,"
yet no `.claude/skills/` or `.claude/agents/` is checked into the repo, so the
Writer/Reviewer pattern is only ever ad hoc.

## Proposed fix

1. Move `.claude/rules/solidity-examples.md` content into
   `.claude/skills/solidity-examples/SKILL.md` with appropriate frontmatter
   (`name`, `description`). Delete the rule file (or slim to nothing — do not
   leave a pointer that re-adds always-on cost).
2. Audit the other `.claude/rules/*` for the same property. `wiki-content`,
   `wiki-linking`, `wiki-audience`, `always`, `self-improvement` are genuinely
   always-relevant and should stay rules; `solidity-examples` is the clear
   outlier. Document the keep/move decision for each in the commit message.
3. Optional, lower value: add `.claude/agents/wiki-style-reviewer.md`
   (tools: Read, Grep, Glob) for a clean-context review pass on new pages.

## Files

- `.claude/rules/solidity-examples.md` — delete
- `.claude/skills/solidity-examples/SKILL.md` — new
- `.claude/agents/wiki-style-reviewer.md` — new (optional)

## Verification

- After the change, `solidity-examples` no longer appears in the always-on
  project-instruction block at session start.
- A DeFi/Solidity page task pulls the skill on demand; an AI-section page task
  does not load Solidity guidance into context at all.
