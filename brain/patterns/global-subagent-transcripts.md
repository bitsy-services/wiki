---
name: global-subagent-transcripts
description: A running subagent's transcript is noise, so wait for its notification; a dead one's transcript and the scratchpad are a salvage source, so read them before re-running
metadata:
  type: feedback
---

Consolidates two Gen 0 observations (`global-taskoutput-transcript-flood`,
`global-workflow-transcripts-survive-a-session-limit`) on 2026-10-18. Both
concern the raw JSONL transcript a subagent leaves behind, and they point in
opposite directions depending on whether the agent is still alive.

**A running agent: do not read it.** Calling `TaskOutput` on a running
`local_agent` task, or reading its `.output` file, returns the raw JSONL
conversation (thinking blocks, signatures, per-message token accounting)
truncated to whatever fits. Two such polls in one session cost roughly 35k
tokens and surfaced no conclusion, because the findings exist only once the
agent finishes. This does not apply to background Bash tasks or workflows,
where `TaskOutput` is the intended way to collect results.

**A dead agent: salvage it.** On 2026-09-08 an eight-agent research workflow
(`wf_08f493ea-0ee`) ran for ten minutes, made 746 tool calls and spent 1.2M
tokens, then every agent failed with "You've hit your session limit". The
result was null and `journal.jsonl` held only `started`/`failed` lines, but
each agent's transcript in
`~/.claude/projects/<project>/<session>/subagents/workflows/<run>/agent-*.jsonl`
(700–960 KB each) still held every fetch, search and Bash output. A 40-line
script pairing each `tool_use` with its `tool_result` recovered about 340
sources, and the agents had `curl`ed many primary texts into the session
scratchpad, which outlives them. A session limit kills the reporting step, not
the reading that preceded it.

**Why:** polling a live agent spends context on noise; re-running a dead one
repeats work that is already on disk.

**How to apply:**

- Launch an agent, do unrelated work, and let the completion notification
  deliver the report. If several run at once, one blocking poll cannot observe
  the others anyway.
- On a session-limit failure, read `journal.jsonl` first, then list the
  transcript directory and the scratchpad before deciding anything.
- Extract with a script, not `Read`: each transcript is about 90k tokens and
  `Read` caps at 25k. Drop failed and binary results, keep fetch bodies and
  Bash output, then read the condensed digests in slices of about 400 lines.
- Prefer the scratchpad texts over the digests for quotations, and bank
  verified quotes in notes files as you go, so a later context summary cannot
  lose them.
- Agents that `curl` PDFs should extract text with `pypdf` (installed; `fitz`
  and `pdftotext` are not); `WebFetch` returns corrupted binary for most
  academic PDFs.
- A single background agent that dies on the limit can simply be resumed:
  after the reset, `SendMessage` to its agent ID continues it from its own
  transcript (2026-10-18, a review round on `git/squashing` finished this
  way in three tool calls). Prefer that to a fresh agent or a salvage script
  when the agent's work is still needed.

Related: [[global-numbers-beyond-their-sources]].
