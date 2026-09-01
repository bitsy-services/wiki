---
name: taskoutput-transcript-flood
description: Polling TaskOutput on a local_agent task floods context with raw JSONL transcript instead of the agent's report
type: feedback
---

Do not call `TaskOutput` to poll a running `local_agent` (subagent) task. Wait for
its completion notification, which delivers the agent's final report cleanly.

**Why:** For a `local_agent`, `TaskOutput` returns the raw JSONL conversation
transcript — thinking blocks, signatures, per-message token accounting — truncated
to whatever fits. Two such polls in this session cost roughly 35k tokens and
surfaced no conclusion, because the agent's actual findings only exist once it
finishes. The tool's own description warns against `Read`-ing the `.output` file
for this reason; calling `TaskOutput` on the same task has the same effect. This
does *not* apply to background **Bash** tasks or workflows, where `TaskOutput` is
the intended way to collect results.

**How to apply:** Launch the agent, do unrelated work, and let the notification
arrive. If a wait is genuinely needed, use a background `sleep` rather than a
poll. When several agents run at once, remember that one blocking poll cannot
observe the others anyway — the notifications can.
