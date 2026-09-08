---
name: global-workflow-transcripts-survive-a-session-limit
description: When a Workflow's agents all die on "You've hit your session limit", their transcripts still hold every fetched source — salvage those instead of re-running after the reset
metadata:
  type: feedback
---

On 2026-09-08 an eight-agent research workflow (`wf_08f493ea-0ee`) ran for ten
minutes, made 746 tool calls and spent 1.2M tokens, then every agent failed
with "You've hit your session limit · resets 8:50pm". The workflow result was
`{"brief": null, ...}` and `journal.jsonl` recorded only `started`/`failed`
lines, so at the tool-result level nothing had been produced.

The work was not lost. Each agent's full transcript sat in
`~/.claude/projects/<project>/<session>/subagents/workflows/<run>/agent-*.jsonl`
(700–960 KB each), holding every `WebFetch` extraction, `WebSearch` result and
`Bash` output the agent had seen. A 40-line Python script that walked the JSONL,
paired each `tool_use` with its `tool_result`, dropped thinking blocks and
failed fetches, and wrote one condensed Markdown digest per agent recovered
~340 fetched sources. Better still, the agents had `curl`ed many primary texts
into the session scratchpad (`/tmp/claude-1000/<project>/<session>/scratchpad/`),
which survives the agents — Kaiser 1911, two editions of Ranganathan's
Prolegomena, the Bliss BC2 introduction, Z39.19, ISO 25964, Alexander 1965, the
FHS pages — so the page could be written from primary quotes with `grep` and
`sed`, which is more reliable than the agents' summaries anyway.

**Why:** a session limit kills the *reporting* step, not the *reading* that
preceded it. Re-running after the reset would have repeated 1.2M tokens of
fetching to reproduce material already on disk, and the memory rule against
polling `TaskOutput` is about a *running* agent — a dead agent's `.jsonl` is
just a file.

**How to apply:**

- On a session-limit failure, read `journal.jsonl` first; if it shows only
  `failed` lines, list the transcript directory and the scratchpad before
  deciding anything.
- Extract with a script, not `Read`: the raw transcripts are ~90k tokens each
  and the Read tool caps at 25k. Condense (drop 403/404/binary results, trim
  search summaries, keep `WebFetch` bodies and `Bash` output), then Read the
  condensed digests in ~400-line slices.
- Prefer the scratchpad texts over the digests for quotations, and bank
  verified quotes into notes files as you go, so a later context summarisation
  cannot lose them.
- Agents that `curl` PDFs should extract text with `pypdf` (installed; `fitz`
  and `pdftotext` are not) — `WebFetch` returns "corrupted PDF binary" for
  most academic PDFs and the agent has to fall back anyway.

Related: [[global-taskoutput-transcript-flood]], [[global-numbers-beyond-their-sources]].
