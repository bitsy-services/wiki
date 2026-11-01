---
name: global-scratchpad-lives-in-tmp
description: The session scratchpad is under /tmp, which a WSL restart wipes; after a crash, check uptime and the scratchpad before resuming agents that were pointed at it
metadata:
  type: feedback
---

On 2026-10-26 the WSL instance restarted in the middle of a review round
(`uptime` showed 15 minutes when work resumed). The session's scratchpad,
`/tmp/claude-<uid>/<project>/<session>/scratchpad/`, survived as a path but
lost everything in it: about 60 fetched source documents, the notes file of
verified quotes, the test scripts, the Hugo binary and the theme clone. The
two reviewers resumed with `SendMessage` found their sources gone, re-fetched
some of them, and one reported that it could not re-run the gate.

**Why:** Claude Code puts the scratchpad under the system temp directory, and
a WSL distribution clears `/tmp` when it restarts. The conversation itself
survived, so the facts were still in context; the files that let a reviewer
check them were not.

**How to apply:** after "continue after a crash", run `uptime` and list the
scratchpad before resuming any agent. Rebuild what the agents were told to
use (sources, notes, gate tooling) first, then tell them where it now is.
Keep the notes file short and keyed to `file:line`, so it is cheap to
rebuild. Related: [[global-subagent-transcripts]],
[[project-gate-needs-hugo-and-theme]].
