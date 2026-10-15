---
title: "The Ralph Loop"
weight: 10
---

## What the Ralph loop is

The Ralph loop is a shell loop that feeds one prompt file to a coding agent, waits for the agent to exit, and feeds it the same file again, indefinitely. Geoffrey Huntley published it on 14 July 2025, named it after Ralph Wiggum of *The Simpsons*, and gave its purest form as one line of Bash:

```bash
while :; do cat PROMPT.md | claude-code ; done
```

Each pass starts a new agent process with an empty [context window](/wiki/ai/context-engineering). Nothing from the previous pass survives except what it left on disk: the code, the git history, and a handful of files that the prompt tells every pass to read. It is the smallest complete [outer loop](/wiki/ai/loop-engineering). The previous run ending is the trigger, the prompt is the same text every time, and all of the state lives in the repository.

`claude-code` in Huntley's line stands for whichever agent is in use. He wrote that Ralph "can be done with any tool that does not cap tool calls and usage", and the builds in his post ran on Amp. With Claude Code the agent is `claude -p`, its non-interactive mode, which runs one prompt and exits. A version with bounds looks like this:

```bash
for i in $(seq 1 50); do
  cat PROMPT.md | claude -p \
    --allowedTools "Read,Edit,Write,Bash(cargo test *),Bash(git add *),Bash(git commit *)" \
    --max-budget-usd 5
done
```

The `seq` caps the number of passes and `--max-budget-usd` caps the spend of each one; neither caps the other. `--allowedTools` lists what a pass may do without asking, and in a `-p` run any other call is denied, since there is nobody to ask. Without `--bare`, each pass also runs the project's hooks, so a [Stop-hook gate](/wiki/ai/loop-engineering/claude-code#the-stop-hook-the-loop-that-starts-when-claude-stops) applies to every pass.

## What each pass reads

The prompt names a fixed set of files that every pass loads before it does anything else. In Huntley's builds there are three: a `specs/` directory with one specification per component, a plan file (`fix_plan.md`) listing the remaining work in priority order, and `AGENT.md`, which records how to build and run the project. He calls this allocating "the stack the same way every loop." The specifications are re-read on every pass and the reading is never reused, which he concedes is wasteful. In exchange, every pass starts from the same known state, and none starts from whatever an earlier conversation happened to leave in its window.

The passes communicate only through those files. The prompt tells each pass to update the plan when it finishes an item or notices a bug, to add to `AGENT.md` when it learns the right way to run a command, and to commit. Huntley also has each pass write down why every test it adds exists, "because future loops will not have the reasoning in their context window."

## One item per pass

The rule Huntley repeats most is "one item per loop." His figure for the usable window was about 170,000 tokens, and his observation was that "the more you use the context window, the worse the outcomes you'll get." A pass that takes on one item finishes well inside a fresh window. He relaxes the rule himself, and his published prompt for CURSED, the compiler for a new programming language that he built this way, asks for "the most important 10 things." The rule is what to return to when the loop "starts going off the rails."

Inside a pass, the main context is meant to "operate as a scheduler": wide searches and file writing go to [subagents](/wiki/ai/context-engineering#sub-agent-context-isolation), so their output never fills the window that is doing the planning. Only one subagent may run the build and tests.

## Backpressure

Huntley's name for the check is backpressure: anything that rejects bad output before the next pass builds on it. A compiler, a type checker, a test suite, a static analyser and a security scanner all count. The requirement on all of them is speed ("the wheel has got to turn fast"), since every pass waits on them. He wanted "extreme correctness" for CURSED, chose Rust to get it, and paid for it in compile time. For a dynamically typed language, he wrote, a loop without a static analyser or type checker will "run into a bonfire of outcomes."

The single-subagent rule for builds and tests is part of the same idea. Fan the test run out to hundreds of subagents and the result is what he calls "bad form back pressure": many partial reports where the loop needed one verdict.

## When it stops

`while :` has no exit condition. The loop ends when a person stops it. Huntley describes that person's work as watching the output for repeated mistakes and adding a line to the prompt for each one, which he compares to putting up a sign beside a slide (`SLIDE DOWN, DON'T JUMP, LOOK AROUND`) and to tuning a guitar. "There is no such thing as a perfect prompt"; his own had "evolved through continual tuning based on observation of [LLM](/wiki/ai/llm) behaviour." When the plan file runs out, or the loop wanders off course, he deletes the plan, runs a planning pass with a different prompt to write a new one, and switches back to building.

The Claude Code [plugin](/wiki/ai/plugins/claude-code) that Anthropic publishes under the same name works differently. It runs inside one session: a [Stop hook](/wiki/ai/loop-engineering/claude-code#the-stop-hook-the-loop-that-starts-when-claude-stops) feeds the same prompt back each time Claude tries to stop, so the passes share one context window instead of each getting a fresh one. It ends when Claude prints an agreed phrase such as `<promise>COMPLETE</promise>`, or at an iteration cap. A phrase the agent prints is a report from the agent that it has finished, and the plugin's own README advises treating the cap as the primary safety mechanism. Huntley's post links a video arguing that the plugin "isn't it."

## Pitfalls, by severity

Ordered worst-first. The first two come from running any loop unattended, and the rest from Huntley's post.

1. **Permission checks switched off outside a sandbox.** A pass cannot stop to ask, and both the Ralph Playbook's loop and Anthropic's C-compiler loop pass `--dangerously-skip-permissions` so that it never has to. That flag removes every check on whatever machine the loop runs on, and the C-compiler post adds "Run this in a container, not your actual machine." Mitigation: list the tools a pass needs with `--allowedTools` and let everything else be denied, and run the loop in a container that holds no credentials it does not need. The [loop-engineering pitfalls](/wiki/ai/loop-engineering#pitfalls-by-severity) cover the general case.
2. **Spend with no ceiling.** `while :` never exits, and a per-run budget does not bound the loop. Mitigation: a counter on the passes, as in the bounded version above, and a spending limit on the account the loop bills.
3. **A wrong specification.** The loop builds faithfully to whatever the specifications say. One of CURSED's lexer specifications defined the same keyword twice for opposite cases, and he noticed only a month in, after the loop had spent that month building on it. Mitigation: read the specifications before starting the loop, and when the loop builds the wrong thing, suspect the specification before the model.
4. **Placeholder implementations.** A pass can satisfy the build with a stub. Huntley's explanation is that "the reward function is compiling code." Mitigation: a line in the prompt forbidding placeholders, and periodic passes whose only job is to find stubs and add them to the plan.
5. **Duplicate implementations.** A pass searches the code, wrongly concludes that a feature is missing, and writes it again. He calls this nondeterminism "the Achilles' heel of Ralph." Mitigation: a sign in the prompt, "don't assume not implemented", and a search before every change.
6. **A broken build in the morning.** "You'll wake up to a broken codebase" that the loop cannot repair. Mitigation: commit after every passing item so that `git reset --hard` is always a short step back, or write a different prompt to rescue it.

His scope note sits above the last four: "There's no way in heck would I use Ralph in an existing code base." He recommends it for new projects, "with the expectation you'll get 90% done with it," and adds that engineers are still needed to steer it.

## The same shape at larger scale

Anthropic's engineering post *Effective harnesses for long-running agents* (November 2025) describes a structured Ralph loop. Two prompts run on an otherwise identical harness. The first pass, the initializer, expands the request into a JSON list of features (over 200 for a clone of claude.ai), all marked failing, and writes a progress log, an `init.sh` script and a first commit. Every later pass starts with an empty window, reads the progress log and the git history, picks the highest-priority failing feature, works on that one alone, and leaves the code in a state fit to merge.

The feature list is the loop's check, and the harness protects it. Passes may change only each feature's `passes` field, under the instruction "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality." The list is JSON because the model was "less likely to inappropriately change or overwrite JSON files compared to Markdown files." The two failures the design answers are the ones a bare loop shows: a pass that tries to build everything at once and runs out of context halfway, and a later pass that sees progress, concludes the work is finished, and stops.

Nicholas Carlini's C compiler, written up by Anthropic in February 2026, ran sixteen agents in parallel, each in a `while true` loop ("if you've seen Ralph-loop, this should look familiar"). Over nearly 2,000 sessions and just under $20,000 of API use they produced a 100,000-line compiler that builds Linux 6.9.

## In this wiki

This wiki's repository keeps a harness backlog in the same shape, with a person as the trigger. Its README says: pick the highest-priority open item, start a fresh session, read only that item's file, run its verification, mark it done, and take one item per session. Each item file is written so that "a fresh session can execute it cold." Every step except starting the session is written for an agent, and the step left to the person is the one a `claude -p` loop would replace.

## Related

- [Loop engineering](/wiki/ai/loop-engineering): the outer loop in general, of which this is the smallest case.
- [Loops in Claude Code](/wiki/ai/loop-engineering/claude-code): `claude -p`, the Stop hook the plugin is built on, and the other mechanisms one harness offers.
- [Context engineering](/wiki/ai/context-engineering): why a fuller window gives worse results, which is the case for one item per pass.
- [Agentic workflows](/wiki/ai/agentic-workflows#verification-loops): environmental verification, the general form of backpressure.

## Further reading

- Geoffrey Huntley, [Ralph Wiggum as a "software engineer"](https://ghuntley.com/ralph/) (14 July 2025) and [everything is a ralph loop](https://ghuntley.com/loop/) (17 January 2026)
- Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (26 November 2025), with [reference code](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)
- Anthropic, [Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) (5 February 2026)
- Anthropic, [the `ralph-wiggum` plugin](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) for Claude Code
- Clayton Farr, [The Ralph Playbook](https://github.com/ClaytonFarr/ralph-playbook): a `claude -p` version with separate planning and building prompts
