---
name: prefer-source-control
description: User prefers changes to be under source control; avoid modifying semi-persistent files like ~/.claude/settings.json
type: feedback
---

Do not make semi-persistent changes to files outside of source control (e.g. `~/.claude/settings.json`). Prefer project-level config files (`.claude/settings.json`) that are checked into the repo.

**Why:** Changes outside source control are hard to track, review, and revert. The user wants to see diffs and have history.

**How to apply:** When modifying config, always target the project-level file. If user-level changes are truly needed, confirm first and explain why project-level won't work.
