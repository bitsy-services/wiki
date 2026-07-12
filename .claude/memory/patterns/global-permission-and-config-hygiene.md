---
name: global-permission-and-config-hygiene
description: How this user wants permissions and agent config managed — explicit allow-lists, in source control, changed only with their sign-off
metadata:
  type: feedback
---

Consolidates three Gen 0 observations (`allowlist-not-denylist`,
`permission-sprawl`, `prefer-source-control`) that all turned out to be the same
underlying preference, plus a fourth data point from the 2026-07-12 harness
session.

**The rule:** agent permissions and config are a reviewable artifact the user
owns. They are enumerated explicitly, kept in source control, and changed only
with the user's knowledge.

Three consequences:

1. **Allow-list, don't deny-list.** Enumerate safe operations rather than using
   a broad wildcard plus deny overrides. With a deny-list, every new command
   variant is silently permitted; the user would rather absorb an extra prompt
   than have an unintended action slip through. Watch for the flip side, though:
   granular one-off entries accumulate into sprawl (`~/.claude/settings.json`
   had 100+), and every near-miss variant re-prompts. Consolidate *within* a
   tool family (`Bash(hugo *)`, `Bash(npm *)`), not across tools, and prune dead
   entries that name one-time paths or URLs.

2. **Project-level, not user-level.** Put config in the repo's
   `.claude/settings.json`, never `~/.claude/settings.json`, so the change shows
   up in a diff and can be reverted. Enforced structurally now: the
   `guard-write.sh` PreToolUse hook denies writes under `~/.claude/`.

3. **Never widen your own permissions silently.** In the 2026-07-12 session the
   auto-mode classifier blocked an edit that added `Bash(scripts/check.sh)` to
   the allow-list and installed a `Stop` hook running a script written minutes
   earlier — correctly, because a broad "make yourself more autonomous" brief is
   not consent for a specific privilege grant. The right move is to write the
   hook, test it by piping JSON into it directly, and then **show the user the
   settings diff and let them apply it.**

**How to apply:** when a task would benefit from a new permission or hook, build
and verify the mechanism, then propose the config change as a diff. Do not treat
generic encouragement as authorization for self-modification.

Related: [[unnecessary-prompting]] — this is the exception to it. Asking before
changing the permission surface is not busywork; it is the one place a
confirmation genuinely belongs.
