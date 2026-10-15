---
title: "Loop Engineering"
weight: 45
bookCollapseSection: true
---

## What loop engineering is

Loop engineering is writing the program that prompts a coding agent, in place of a person typing each prompt. The program is an **outer loop**: a shell `while` loop, a cron schedule, or a handler for an event such as a pull request being opened. Each time round, it starts the agent with a message, waits for the run to end, and then goes round again or stops. Inside each run the agent executes the same [agent loop](/wiki/ai/agentic-workflows#the-agent-loop) it would for a person, calling a tool, reading the result and choosing the next call, and that inner loop does not change. What changes is the author of the first message. Three jobs a person used to do between messages move into the program with it: choosing the next task, judging whether the last one was done, and stopping.

## Two loops

| | Agent loop (inner) | Outer loop |
| --- | --- | --- |
| One iteration is | one tool call and its result | one agent run, start to finish |
| The next step is chosen by | the model | the program |
| The loop ends when | the model stops calling tools, or hits a cap | a check passes, the work runs out, or a cap is hit |
| It runs for | minutes | days, or until switched off |
| State is kept in | the context window | files, commits, an issue tracker |

The word *loop* is used for both, and a good deal of writing on agents means the inner one. Simon Willison's *Designing agentic loops* (September 2025) is about choosing the tools, the goal and the sandbox for a single agent run; loop engineering in the sense of this page is about what starts that run, and the next one.

The outer loop is old machinery. A cron job is one, and so is a continuous integration (CI) pipeline. The new part is the thing being run: it takes an instruction in English and can do open-ended work, so the main output of the loop's code is a prompt.

## What starts a run

A loop is classified most usefully by what starts its next iteration. The documentation for [Claude Code](/wiki/ai/context-engineering/claude-code), Anthropic's coding agent, sorts its own mechanisms the same way: "Pick based on what should start the next turn."

A clock is the simplest trigger. A fixed interval (check the deploy every five minutes) suits polling, and a cron schedule (triage new issues at 09:00 on weekdays) suits recurring chores. An event starts a run when something happens elsewhere: a pull request is opened, a CI job fails, an alert fires and calls an endpoint. A third kind of loop restarts the agent as soon as the previous run exits and keeps doing so until some condition holds. The [Ralph loop](/wiki/ai/loop-engineering/ralph-loop) is this shape written as one line of shell. The last kind lets the agent set the delay before its own next run, short while a build is finishing and long when nothing is pending.

## The prompt becomes a source file

A prompt typed into a session is read once, by a model that can ask what was meant. A prompt in a loop is read on every iteration, against a repository that has changed since the previous one, with nobody there to answer a question.

The prompt therefore describes how to find the work instead of naming it. *Fix the broken link on the attention page* is a one-off. *Run `scripts/check.sh`, fix the first failure it reports, and commit* is a loop body: it is the same text every time, and the varying part of the task, which failure, comes from the state of the repository.

It is also maintained like code. It lives in a file, it is versioned and reviewed, and it is edited when an iteration goes wrong, since the same mistake otherwise recurs on every run. Claude Code reads a project's default loop prompt from `.claude/loop.md` and picks up edits on the next iteration. Its documentation tells the author of a cloud routine, a saved prompt that Anthropic's servers run on a schedule or a trigger, that the prompt "must be self-contained and explicit about what to do and what success looks like."

## What carries over between runs

There are two designs, and the choice between them shapes everything else about a loop.

In the first, each run is a new process with an empty [context window](/wiki/ai/context-engineering) and the same prompt. Nothing accumulates from one run to the next, so the window never fills and [compaction](/wiki/ai/context-engineering#compaction-and-summarization) never discards anything. Each run has to find out afresh where things stand, and anything the next run needs has to be written down where it will look: commits, a progress file, a checklist, the issue tracker. `claude -p` (Claude Code's non-interactive mode, which runs one prompt and exits) in a shell loop, a cloud routine and a CI job all work this way.

In the second, the loop sends each new message into a session that stays open, so every iteration sees the ones before it. Continuity costs nothing, but the window grows with every iteration until compaction summarizes the early ones away. Claude Code's `/loop` and `/goal` work this way.

Either way the durable record is the repository. The context-engineering rule that a decision belongs in a file and not in chat applies across runs as well as across turns. A fresh-context loop enforces it, since a fact left only in the conversation is gone when the run ends.

## What checks the work

A person prompting an agent reads each answer before writing the next prompt, and that reading is the check. An outer loop removes the reader, so the check has to be something that runs: a test suite, a build, a linter, a script that exits non-zero. This wiki's repository runs its checks from a [Stop hook](/wiki/ai/loop-engineering/claude-code#the-stop-hook-the-loop-that-starts-when-claude-stops), a script Claude Code runs each time the agent tries to end its turn, which can refuse and send the agent back to work. Its header comment says why:

> Without it, "looks done" is the only completion signal and the human becomes the verification loop.

A check that runs sets the ceiling on what a loop can be trusted to do. The loop keeps iterating until the check passes, so it converges on whatever passes the check. Work whose correctness a script can decide suits a loop: a build, a failing test, a dead link. Work that only a reader can judge does not. This wiki's gate checks internal links, anchors, code fences, frontmatter and acronyms. It cannot tell whether a sentence parses, and a loop gated on it alone would produce pages whose links all resolve and whose sentences nobody has read.

A model can be the check where no script can. In Claude Code's `/goal`, a small model reads the conversation after each turn and rules whether a stated condition holds. It reads only what the conversation contains, so it is as reliable as the evidence the condition forces into the transcript. A condition that names a command and its exit status gets the command run. A condition that names only an outcome leaves the evaluator to weigh what the agent wrote about it.

## When it stops

Each run needs the stopping condition every [agent loop](/wiki/ai/agentic-workflows#the-agent-loop) needs. The outer loop needs its own as well, of a different kind: the queue of work is empty, the check passes, a cap on iterations or spend is reached, or a person switches it off. A loop that never ends by design, such as a nightly triage job, still needs an expiry, and Claude Code puts one on in-session loops: recurring tasks expire after seven days, which its documentation says bounds "how long a forgotten loop can run."

A loop triggered by the agent's own attempt to stop can run forever. A Stop hook that blocks whenever the check is red will block indefinitely on a failure the agent cannot fix. Claude Code guards against this twice: it tells the hook when the agent is already continuing because of an earlier block, and it overrides any hook that blocks eight times in a row without the agent calling a tool in between. [Loops in Claude Code](/wiki/ai/loop-engineering/claude-code#the-stop-hook-the-loop-that-starts-when-claude-stops) has the details.

## What the person does instead

Boris Cherny, who created Claude Code at Anthropic, described the shift in June 2026 as the second of two steps. In the first, the engineer stopped writing source code and talked to an agent that wrote it. In the second:

> I don't talk to an agent anymore. I talk to loop or I talk to a routine and it prompts Claude for me.

He was answering a question about Claude Code's `/loop` command, and the two nouns in his answer name its in-session loop and its cloud routine, both covered under [Loops in Claude Code](/wiki/ai/loop-engineering/claude-code). A week earlier, on stage at a WorkOS event, he had put it as a job description: "My job is to write loops." The loops he listed in a post that March were skills run on timers, among them `/loop 5m /babysit`, "to auto-address code review, auto-rebase, and shepherd my PRs to production," and `/loop 1h /pr-pruner`, "to close out stale and no longer necessary PRs."

The name followed within days. Peter Steinberger posted on 7 June 2026 that "you shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents," and Addy Osmani's post the same day defined the practice: "Loop engineering is replacing yourself as the person who prompts the agent. You design the system that does it instead." An August 2026 study by Lulla, Treude, Baltes and others credits Osmani's post with the name, summarizes the practice as "instead of prompting an agent interactively, developers design systems that prompt agents for them," and cautions that the practitioner sources it draws on "are not independent."

The person's work becomes three things: writing loop bodies, writing checks, and reading what the loops produce. The third is the one that does not scale. A loop on a five-minute timer can open pull requests faster than one person can read them, so the checks decide how much of the output a person has to read, and the rate at which a person can review sets how many loops are worth running.

## Pitfalls, by severity

Ordered worst-first. The early items let an unattended loop do damage; the later ones let it waste money, or stop working without anyone noticing.

1. **An irreversible action with nobody there to stop it.** The [agentic-workflows page](/wiki/ai/agentic-workflows#pitfalls-by-severity) puts a human checkpoint before anything an agent cannot undo. An outer loop removes the human by construction, so the checkpoint has to move into the harness. Mitigation: deny the dangerous commands at the tool boundary, run without production credentials, and have the loop open a pull request for a person to merge instead of pushing or deploying.
2. **Someone else's text inside the prompt.** A loop that reads issue bodies, pull-request comments or web pages takes in instructions from whoever wrote them, which is prompt injection with no one reading along. Mitigation: give a loop that reads outside text no tool whose misuse cannot be undone, as under [agentic engineering](/wiki/ai/agentic-engineering#guardrails-and-the-irreversible-action-problem).
3. **A loop that can edit its own check.** When the gate is a file in the repository the loop writes to, deleting the failing test is one way to turn the check green. Anthropic's long-running harness tells its agent "it is unacceptable to remove or edit tests" and keeps its feature list in JSON, which the model was less likely to overwrite than Markdown. Mitigation: make the check's files unwritable to the agent, with a hook that denies the write, or run the check from a copy the agent cannot reach.
4. **Cost without a ceiling.** Each iteration is a full agent run that re-reads its context from scratch, and a loop with no cap keeps paying for that. Nicholas Carlini's [C compiler](/wiki/ai/loop-engineering/ralph-loop#the-same-shape-at-larger-scale), built by sixteen looping agents over two weeks and written up by Anthropic, cost just under $20,000. Mitigation: a cap on iterations and spend per run and per day, as under [cost engineering](/wiki/ai/agentic-engineering#cost-engineering-at-scale).
5. **A loop that stops, or runs and does nothing.** A session closes, a schedule expires, a credential lapses, and the work stops without an error anywhere a person looks. A run that exits cleanly having achieved nothing looks the same as one that worked. Mitigation: have every run leave a record a person reads, and treat a gap in the records as a failure.

## In this section

[The Ralph loop](/wiki/ai/loop-engineering/ralph-loop) comes first because it is the smallest complete outer loop: one prompt file, one line of shell, and a new context for each run. It also covers Anthropic's long-running-agent harness, which is the same shape with a feature list and a progress file added. [Loops in Claude Code](/wiki/ai/loop-engineering/claude-code) then goes through the seven mechanisms one harness provides, from a timer inside an open session to a routine running in the cloud, and works through the Stop hook this wiki uses as its own gate.

## Related

- [Agentic workflows](/wiki/ai/agentic-workflows): the inner loop that every outer-loop iteration runs.
- [Agentic engineering](/wiki/ai/agentic-engineering): the lifecycle around many loops, from evaluation to observability and cost.
- [Context engineering](/wiki/ai/context-engineering): what each run sees, and why a long-running session degrades.
- [Claude Code](/wiki/ai/context-engineering/claude-code): the section's running example, a harness writing a page for this wiki.

## Further reading

- Claude, [Reflecting on a year of Claude Code](https://www.youtube.com/watch?v=Hth_tLaC2j8) (video, 8 June 2026): Boris Cherny and Cat Wu; the loop passage is at 10:24
- WorkOS, [Boris Cherny: Claude Code & the Future of Engineering](https://www.youtube.com/watch?v=RkQQ7WEor7w) (video, 2 June 2026): "My job is to write loops" at 11:36
- Addy Osmani, [Loop Engineering](https://addyosmani.com/blog/loop-engineering/) (7 June 2026)
- Lulla, Nersesyan, Mohsenimofidi, Treude & Baltes, [Loop Engineering: Building Blocks, Adoption, and Impact](https://arxiv.org/abs/2608.21884) (arXiv:2608.21884, August 2026)
- Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (November 2025)
- Simon Willison, [Designing agentic loops](https://simonwillison.net/2025/Sep/30/designing-agentic-loops/) (September 2025): the inner loop, for contrast
