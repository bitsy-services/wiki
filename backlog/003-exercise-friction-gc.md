# 003 — Exercise or simplify the friction GC

- **Priority:** P3 (deferred judgement; not a code change)
- **Status:** done (2026-07-12) — GC exercised, mechanism kept

## Resolution

The mechanism was exercised as designed rather than simplified away. Three of the
four Gen 0 notes (`allowlist-not-denylist`, `permission-sprawl`,
`prefer-source-control`) turned out to be one preference viewed from three angles,
and a fourth data point arrived in the same session when the auto-mode classifier
blocked the agent from granting itself permissions. They consolidated into
`patterns/global-permission-and-config-hygiene.md` (Gen 1) and the consumed Gen 0
files were deleted. `unnecessary-prompting` stayed at Gen 0 — it is a different
theme with only one observation.

So the GC does earn its keep, and `self-improvement.md` stays as written. Worth
revisiting only if `patterns/` sits at exactly one entry for several more sessions.

One promotion candidate is now visible: the Gen 1 pattern is `global-` scoped, and
per the rule's own Scoping table a stable `global-` pattern belongs in the user's
`~/.claude/CLAUDE.md`, not this repo. That needs the user's say-so, and it collides
with `prefer-source-control` — the user does not want `~/.claude/` edited. Left
open deliberately.

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
