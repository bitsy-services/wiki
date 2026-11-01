---
name: global-status-lines-during-long-research
description: Research and test phases ran dozens of tool calls with no text, and the harness had to prompt three times for an update; post a one-line status every few calls
metadata:
  type: feedback
---

2026-10-30, `ai/claude-accounts/switching.md`. Between the first plan line and
the draft, the turn fetched docs, read them and ran shell and binary tests
across roughly fifty tool calls. The harness interrupted three times with "The
user hasn't heard from you in a while", and each time the update was written
only because it asked.

Hypothesis: verification work feels like a single step from the inside
("checking the claims") while the user sees nothing at all, and the longer it
runs the less the user can tell a stall from progress.

**Why:** an unexplained silence costs the user's attention and trust even when
the work inside it is sound.

**How to apply:** during research or testing, write one line every five or so
tool calls: what was just confirmed or refuted, and what is being checked
next. Findings that change the plan (a pitfall reconfirmed, a doc that
contradicts the wiki) go in that line as they land, not only in the report.

Related: `.claude/rules/kit/collaboration.md`.
