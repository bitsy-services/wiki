# 003 — Exercise or simplify the friction GC

- **Priority:** P3 (deferred judgement; not a code change)
- **Status:** open

## Problem

`.claude/rules/self-improvement.md` defines a generational garbage collector
for friction memory (Gen 0 `friction/` → Gen 1 `patterns/` → Gen 2 promoted
rules). In practice `patterns/` is empty and all four friction memories are
`global-` scoped — none `project-` or `topic-`. The mechanism is more elaborate
than its usage. Unused process machinery is itself a cost (it must be read and
maintained), and over-formalization is the failure mode the audit explicitly
cautioned against.

## Proposed fix

This is a watch-and-decide item, deliberately deferred — not work to schedule.

At the next start-of-conversation friction scan (per self-improvement.md):

- Evaluate whether the friction notes (now including the .claude/-write-prompt
  friction from the 2026-05-18 session) cluster into a Gen 1 pattern. If so,
  consolidate and delete the consumed Gen 0 files — exercise the mechanism as
  designed.
- If the GC remains unused across several more sessions, propose to the user
  *simplifying* `self-improvement.md` (e.g. collapse Gen 1 into Gen 0→Gen 2)
  rather than maintaining machinery that never runs.

Resolve by either exercising the GC once or proposing the simplification; then
set `Status: done`.

## Files

- `.claude/memory/friction/*`, `.claude/memory/patterns/` (if consolidating)
- `.claude/rules/self-improvement.md` (if simplifying — confirm with user; it's
  a checked-in rule)

## Verification

Judgement item — no automated check. Resolution is a recorded decision (a Gen 1
pattern file created, or a user-approved simplification of the rule).
