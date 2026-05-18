# 002 — Right-mechanism refactor (skills / agents)

- **Priority:** P2
- **Status:** open

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
