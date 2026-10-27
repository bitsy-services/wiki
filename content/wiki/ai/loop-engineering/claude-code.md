---
title: "Loops in Claude Code"
weight: 20
---

[Claude Code](/wiki/ai/context-engineering/claude-code) has seven ways to send Claude its next message without a person typing it. Each is an [outer loop](/wiki/ai/loop-engineering): something outside the agent that starts a turn, and the seven differ on three questions. What starts the next turn? Where does the run happen? What has to be open while it runs?

| Mechanism | Next turn starts when | Runs on | Needs an open session | Permission prompts |
| --- | --- | --- | --- | --- |
| `/loop` | an interval elapses, or a delay Claude picked | your machine | yes | as the session |
| `/goal` | a turn ends and an evaluator rules the condition unmet | your machine | yes, or one non-interactive run | as the session |
| Stop hook | Claude ends a turn and a script blocks it | wherever the session runs | yes | as the session |
| Desktop scheduled task | a schedule fires | your machine | no, but the app must be open | set per task |
| Routine | a schedule, an HTTP call, or a GitHub event | Anthropic's cloud | no | never asks; runs everything it can reach |
| `claude -p` (one prompt, one run, then exit) | the calling program runs it | wherever it is called | no | set by flags |
| GitHub Action | a workflow event or schedule | GitHub's runners | no | set by `--allowedTools` |

The first three keep one session going, so every iteration shares a [context window](/wiki/ai/context-engineering) with the ones before it. The other four start a new session for each run, so a run sees only what an earlier one wrote down. That split is the [fresh-context question](/wiki/ai/loop-engineering#what-carries-over-between-runs) on the parent page. A same-session loop left running for days accumulates history until [compaction](/wiki/ai/context-engineering#compaction-and-summarization) summarizes its early iterations away; a fresh-session loop forgets everything it did not write to disk.

## `/loop`: a timer inside the session

`/loop 5m check the deploy` re-sends *check the deploy* every five minutes. Claude Code turns the interval into a cron expression with one-minute granularity, so `30s` becomes a minute and an interval like `7m` is rounded to the nearest clean cron step.

Leave the interval out (`/loop check whether CI passed`) and the model sets the delay itself. After each iteration it schedules the next one somewhere between one minute and one hour, through a tool called `ScheduleWakeup`, and prints the delay and the reason. It can end the loop by calling the same tool with `stop: true`. An iteration that neither reschedules nor stops gets one fallback wakeup about twenty minutes later, and the loop ends if that one does not reschedule either.

A bare `/loop` runs a built-in maintenance prompt: carry on with unfinished work, tend the current branch's pull request, then run cleanup passes. A file at `.claude/loop.md` replaces that prompt for the project. Edits to the file take effect on the next iteration, so the loop body is a file in the repository, versioned with everything else and editable while the loop runs.

The limits all follow from the loop living inside a session:

- It fires only while Claude Code is running and idle, between turns. Closing the terminal stops it.
- A fire missed while Claude was busy runs once when it becomes idle; missed intervals are not replayed.
- Recurring tasks expire seven days after creation. The documentation gives the reason as bounding "how long a forgotten loop can run."
- A session holds at most fifty scheduled tasks, and a self-paced `/loop` is not restored when the session is resumed.

## `/goal`: run until a condition holds

`/goal all tests in test/auth pass and the lint step is clean` starts a turn with the condition as its instruction. When the turn ends, Claude Code sends the condition and the conversation to a small, fast model, which returns one of three verdicts: *not yet met*, *met*, or *impossible*. On *not yet met* Claude starts another turn, with the evaluator's reason as guidance. The other two clear the goal.

The evaluator does not call tools. In the documentation's words it "doesn't run commands or read files independently", so it judges only what the conversation contains. A condition is therefore only as good as the evidence it forces into the transcript. A condition that names only an outcome, *the tests pass*, leaves the evaluator to weigh whatever Claude wrote about the tests. *`npm test` exits 0* makes Claude run the command and leaves the output where the evaluator reads it. The documentation also recommends naming what must not change on the way, such as "no other test file is modified", which closes the cheapest route to a passing test.

A clause like `or stop after 20 turns` bounds the run, and Claude Code ends the loop on its own if several turns in a row make no tool calls. `claude -p "/goal …"` runs the whole loop in one non-interactive invocation.

## The Stop hook: the loop that starts when Claude stops

A [hook](/wiki/ai/context-engineering/claude-code#pick-the-cheapest-mechanism-that-works) is a script the harness runs at a fixed point. The `Stop` hook runs each time Claude finishes responding. If it prints `{"decision": "block", "reason": "…"}`, or exits with code 2, the turn does not end: Claude receives the reason as a message and keeps working. The reason string is a prompt, and a script wrote it. `/goal` is built on this mechanism: the documentation describes it as "a wrapper around a session-scoped prompt-based Stop hook", the kind of hook that asks a model instead of running a script.

This wiki's repository runs one. Its `Stop` hook runs the site's gate, `scripts/check.sh`, which builds the site and checks every internal link, anchor, code fence, frontmatter block and acronym. If the gate fails, the hook blocks and hands Claude the failure output. The hook is registered in the project's `.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/verify.sh",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

and `.claude/hooks/verify.sh` is the whole of it. Claude Code passes the hook a JSON object on standard input, which the script reads first:

```bash
#!/usr/bin/env bash
set -uo pipefail

input=$(cat)

# Claude is already continuing because of this hook — let it stop, or we spin.
if [ "$(printf '%s' "$input" | jq -r '.stop_hook_active // false')" = "true" ]; then
  exit 0
fi

root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"

if out=$("$root/scripts/check.sh" 2>&1); then
  exit 0
fi

jq -nc --arg out "$out" '{
  decision: "block",
  reason: ("scripts/check.sh is failing, so this work is not done. Fix every problem below and re-run it — do not stop while it is red.\n\n" + $out)
}'
exit 0
```

Unlike `/goal`, this check runs the gate itself, so its verdict does not depend on what Claude printed. Anthropic's `ralph-wiggum` plugin is a Stop hook of the other kind: it feeds the same prompt back on every stop until Claude prints an agreed phrase, and [the Ralph loop](/wiki/ai/loop-engineering/ralph-loop#when-it-stops) compares it with the shell loop it is named after.

A hook that blocks every time would block forever on a failure Claude cannot fix, so there are two guards. The input carries `stop_hook_active`, which is true when Claude is already continuing because a Stop hook blocked. The documented pattern, used above, is to exit early when it is set; with it, the hook sends Claude back once per stop, and the second attempt to stop goes through whether or not the check has turned green. The harness has its own cap as well: after a Stop hook blocks eight times in a row with no tool call from Claude in between, Claude Code overrides it and ends the turn. The count resets whenever Claude calls a tool, so a hook that relies on the cap alone keeps sending Claude back for as long as each retry does some work. `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` raises it.

## Desktop scheduled tasks: a schedule on your own machine

The Claude Desktop app can run a saved prompt on a schedule with no session open. Each run is a new session on the local machine, with access to local files and tools, working in a chosen folder or, if the task is set to, in a git worktree of its own. By default it works on the folder as it stands, uncommitted changes included. The app has to be open and the machine awake. A run that falls due while the computer sleeps is skipped, and on waking the app starts one catch-up run for the most recent missed time in the last seven days and discards the rest.

Each task has its own permission mode. In Manual mode, a run that needs a tool nobody has approved stalls until someone answers, so the documentation suggests running a new task once by hand and choosing *always allow* at each prompt. The prompt is stored as a `SKILL.md` file under `~/.claude/scheduled-tasks/`, and edits to it take effect on the next run.

## Routines: the loop moves off the laptop

A routine is, in the documentation's definition, "a saved Claude Code configuration: a prompt, one or more repositories, and a set of connectors, packaged once and run automatically." A connector is an integration with an outside service, such as Slack, Linear or Google Drive, attached to the owner's claude.ai account and exposed to Claude as [MCP](/wiki/ai/mcp) tools. A routine runs on Anthropic's infrastructure, so it keeps running with the laptop closed. Routines are a research preview. `/schedule daily PR review at 9am` creates one from the command line.

A routine starts on any combination of three triggers. A schedule fires hourly at most, or once at a set time. An authenticated HTTP POST to the routine's `/fire` endpoint fires it on demand. A GitHub pull-request or release event can fire it, with filters on branch, label, author and the like.

Each run is a new cloud session that clones the selected repositories fresh, from the default branch, or from the pull request's head commit when a pull request triggered it. Nothing from an earlier run is present unless that run committed it or wrote it somewhere the next can read. Claude pushes to branches prefixed `claude/`, and GitHub branch protection decides what it may push beyond that.

A routine runs with no permission prompts. The documentation says there is "no permission-mode picker", and the session runs shell commands and calls every included connector, writes included, without stopping for approval. All connected connectors are included by default, and anything the routine does through them, commits and pull requests included, appears under the owner's accounts. What a routine can reach is set by its repositories, its environment's network allowlist and its connectors, so those three are where the permission decision is made.

The run list's green status means the session started and exited without an infrastructure error. The documentation is explicit that it "does not mean the task in your prompt succeeded."

## `claude -p`: any program can be the loop

`claude -p` runs one prompt non-interactively and exits, with a non-zero status on failure:

```bash
claude -p "Run scripts/check.sh and fix the first failure it reports" \
  --allowedTools "Read,Edit,Bash(scripts/check.sh)" \
  --output-format json
```

Each invocation is a new session unless `--continue` or `--resume` attaches it to an earlier one. That makes `claude -p` the building block for loops written in something else: a shell `while` loop (the [Ralph loop](/wiki/ai/loop-engineering/ralph-loop) is one line of it), a cron entry, a CI job. Two flags bound a run that nobody is watching. `--max-budget-usd` stops it at a spending cap, and `--permission-prompts none` denies any call that would otherwise wait for a person to approve it.

Without `--bare`, a `-p` run loads the project's hooks, plugins, MCP servers and `CLAUDE.md` the way an interactive session does, Stop hook included. `--bare` skips them (a skill still runs when the prompt names it as `/skill-name`), and the documentation recommends it for scripted calls so that a run gives the same result on every machine. It also authenticates only with an [API key](/wiki/ai/claude-accounts/credentials), never a subscription login. In a repository whose gate is a Stop hook, like this wiki's, the two pull against each other: a `--bare` loop never runs the gate, so the loop body has to run the check itself. The Claude Agent SDK exposes the same loop to Python and TypeScript programs.

The GitHub Action, `anthropics/claude-code-action`, runs the same thing on GitHub's runners. Given a `prompt` input it runs on whatever event the workflow names, including a `schedule`. Scheduled workflows run from the default branch only, and GitHub disables them in a public repository after sixty days without activity.

## Pitfalls, by severity

Ordered worst-first. The early items let an unattended run do damage, the next one spends money to no purpose, and the last lets the loop stop without anyone noticing.

1. **A routine writes with every connector.** It runs without approval prompts, includes every connected connector by default, and acts under its owner's accounts. A prompt that goes wrong posts, files and commits as that person. Mitigation: remove every connector the routine does not need, keep the network allowlist narrow, and protect the branches it should not push to.
2. **Text from outside becomes part of the prompt.** A routine fired by a pull request, or a loop that reads issue bodies or web pages, takes in text written by someone else. The `/fire` endpoint wraps its payload in a block labelled as untrusted data, but content the session fetches during the run "keeps its normal handling." Mitigation: grant such a loop no tool whose misuse cannot be undone.
3. **A `/goal` condition that the transcript can satisfy without a check.** The evaluator reads the conversation and runs nothing, so a claim of success counts as evidence. Mitigation: name the command and the exit status in the condition, and name what must not change.
4. **A Stop hook with no guard.** It sends Claude back on every stop, spending a turn's worth of tokens each time. The harness cap of eight consecutive blocks stops only retries that call no tools, so a hook whose failure Claude keeps trying and failing to fix keeps it going indefinitely. Mitigation: check `stop_hook_active`, or have the hook count its own blocks and give up after a fixed number.
5. **The loop stops, or runs and does nothing, and nobody is looking.** A `/loop` dies with its session and expires after seven days. A Desktop task skips the runs its machine slept through. A routine's green status means only that it ran. A scheduled GitHub workflow in a quiet public repository is switched off after sixty days. Mitigation: have each run leave a record somewhere a person looks, and notice when the records stop.

## Related

- [Loop engineering](/wiki/ai/loop-engineering): the outer loop in general, independent of any harness.
- [The Ralph loop](/wiki/ai/loop-engineering/ralph-loop): the smallest outer loop, built on `claude -p`.
- [Claude Code](/wiki/ai/context-engineering/claude-code): the same harness from the side of context: what each turn sees, and the hooks, skills and plugins that shape it.
- [Agentic engineering](/wiki/ai/agentic-engineering#guardrails-and-the-irreversible-action-problem): authorizing at the tool boundary, which unattended runs depend on.

## Further reading

- Anthropic, [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks) (`/loop` and the cron tools)
- Anthropic, [Keep Claude working toward a goal](https://code.claude.com/docs/en/goal) (`/goal`)
- Anthropic, [Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide) and the [hooks reference](https://code.claude.com/docs/en/hooks)
- Anthropic, [Automate work with routines](https://code.claude.com/docs/en/routines)
- Anthropic, [Run Claude Code programmatically](https://code.claude.com/docs/en/headless) and [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)
