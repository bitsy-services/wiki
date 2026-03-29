---
name: allowlist-not-denylist
description: User prefers explicit allow-lists over broad wildcards with deny overrides, especially for git
type: feedback
---

For permissions, use explicit allow-lists of safe operations rather than broad wildcards paired with deny rules.

**Why:** A deny-list approach means any new command variant is silently allowed. The user prefers to be prompted for anything not explicitly whitelisted — the cost of an extra prompt is lower than the risk of an unintended destructive action slipping through.

**How to apply:** When setting up permissions, enumerate the safe subcommands individually. Don't use `Bash(git *)` + deny overrides. Same principle applies to other tools with destructive subcommands.
