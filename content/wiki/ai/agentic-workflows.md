---
title: "Agentic Workflows"
weight: 40
---

An agentic workflow is a language model running in a loop with tools — planning, acting, observing the result, and deciding the next step — rather than answering in a single call. The loop is what makes it powerful and what makes it expensive: every iteration re-reads the accumulated history, every tool result enters the window, and every wrong turn compounds into the next. Getting value from an agent is mostly the discipline of *not* reaching for one until the problem needs it, then constraining it tightly when it does.

## Workflow versus agent

These two words are often used interchangeably; the distinction is the most useful one in this area.

- A **workflow** orchestrates models and tools through *predefined code paths*. The control flow is fixed by the engineer; the model fills in steps. A pipeline that drafts text, then translates it, then checks tone is a workflow — the sequence never changes.
- An **agent** lets the model *direct its own process* — it decides which tool to call, in what order, and when it is done. The control flow is emergent.

Workflows are predictable, debuggable, and cheap. Agents are flexible and handle problems whose shape you cannot know in advance, at the cost of higher spend, more error surface, and harder debugging. Most production systems labelled "agents" are workflows with one or two agentic steps, and that is usually the right design.

## When an agent earns its overhead

Start with the simplest thing that works and add autonomy only when a simpler structure provably fails. The progression, in increasing cost and capability:

1. **A single structured call** — one well-engineered prompt with retrieval and examples. Most tasks stop here. (Wording it well is [prompt engineering](/wiki/ai/prompt-engineering).)
2. **A fixed workflow** — chain, route, or parallelize calls when the task has separable subtasks whose order you know.
3. **An agent** — only when it is genuinely impossible to predict the number of steps or hardcode the path: open-ended research, multi-file code changes, debugging where the next move depends on what the last one revealed.

The economics make the threshold concrete. Agents use roughly **4× the tokens of a single chat-style call, and multi-agent systems roughly 15×**. On agentic web-research evaluations, token volume alone explains about 80% of the performance variance — capability and cost rise together. An agent is justified only when the value of getting the task right is high enough to pay that multiple, and a single call cannot get it right. Using an agent for a task a workflow could do is the most common and most wasteful mistake in this area.

## Workflow patterns

Before reaching for a fully autonomous loop, know the structured patterns that solve most problems with far less risk:

- **Prompt chaining** — decompose into fixed sequential steps, each consuming the last one's output. Trades latency for accuracy on cleanly separable subtasks (draft → critique → revise).
- **Routing** — classify the input and dispatch to a specialized handler or a right-sized model. Keeps each path's prompt focused and routes cheap queries to cheap models.
- **Parallelization** — run independent subtasks at once (*sectioning*) or run the same task several times and aggregate (*voting*). Good for guardrails, multi-perspective review, and reducing variance.
- **Orchestrator–workers** — a coordinating model decomposes a task it cannot pre-plan and delegates pieces to workers. The dynamic analogue of parallelization, used when the subtasks are not known until runtime.
- **Evaluator–optimizer** — one model produces, another scores against a rubric, and the loop iterates until the bar is met. Works only when "good" is articulable as criteria the evaluator can apply.

The autonomous agent is the limit of orchestrator–workers with the planning loop fully internalized — reserve it for when even the orchestrator cannot enumerate the steps.

## The agent loop

A bare agent loop is simple: receive a goal, plan, call a tool, observe the result, decide whether the goal is met, and repeat or stop. Its power comes from one property — **the environment supplies ground truth at every step**. A compiler error, a failing test, a search miss is feedback the model did not generate and cannot wish away, which is what lets an agent recover from its own mistakes. A loop without that grounding (one that only reasons about its own output) does not self-correct; it compounds.

Two properties must be engineered, not assumed:

- **A stopping condition.** The loop ends on success *or* on a guard: an iteration cap, a budget cap, or a no-progress detector. Without one, an agent that cannot find a nonexistent answer will search forever, and a confused one will burn the budget restating itself.
- **Human checkpoints before irreversible actions.** The loop should pause for confirmation before anything it cannot undo — deleting data, sending a transaction, publishing externally — rather than trusting its own unverified reasoning at the moment of highest consequence.

## Planning and decomposition

The reliable agentic pattern separates *planning* from *execution* rather than interleaving them turn by turn. A plan produced up front — and revised explicitly when the environment contradicts it — is debuggable and gives the model a stable spine to work against; planning rediscovered on every turn drifts and re-litigates settled decisions.

Decompose the goal into sub-goals with **scoped context** — each sub-task carries only what it needs, and replanning is confined to the active sub-task instead of rerunning the whole plan. Make each sub-goal *verifiable*: a step whose completion you cannot check is a step the agent cannot know it finished. Turning checks into first-class parts of the plan ("write the function" → "write the function; the test passes") is what makes a long plan self-correcting instead of merely long.

## Tool design — the agent-computer interface

An agent is only as good as the tools it can call, and tool design deserves the same care as the prompt. The model interacts with your system entirely through these contracts; ambiguity in them shows up as wrong actions.

- **One tool, one job.** If a human engineer cannot say with certainty which of two tools applies in a situation, the model will not do better. Overlapping tools create decision points that silently degrade the whole loop.
- **Make misuse hard (*poka-yoke*).** Shape arguments so the wrong call is structurally difficult — require absolute paths instead of relative, enums instead of free strings — rather than documenting the constraint and hoping.
- **Return high-signal output.** Tool results are the fastest-growing consumer of the window; a tool that dumps an entire table when the agent needed one row poisons every subsequent turn. Scope and paginate at the tool boundary. This is the [context-engineering](/wiki/ai/context-engineering) discipline applied at the source.
- **Document like a junior engineer's brief.** Clear descriptions, examples, edge cases, and explicit boundaries between similar tools. A tool description *is* a prompt; the same craft applies as in [prompt engineering](/wiki/ai/prompt-engineering).

## Sub-agent delegation

Delegating a sub-task to a sub-agent with its own fresh context window is the strongest single lever for keeping a long-running agent coherent: the sub-agent reads hundreds of files or runs a wide search and returns *one synthesized answer*, so the fan-out never enters the parent's window — the parent keeps the conclusion, not the dump. This is covered in depth under [context engineering](/wiki/ai/context-engineering#sub-agent-context-isolation); the agentic-design points are:

- **Delegate breadth, not depth.** Multi-agent architectures shine on breadth-first work that splits into independent parallel directions and exceeds one context window — on Anthropic's internal research evaluation the orchestrator-subagent design beat single-agent Opus by ~90%. They *hurt* when every agent needs the same shared context or the subtasks have many cross-dependencies. Most coding work is the latter, which is why it rarely benefits from multi-agent decomposition.
- **A subagent needs a contract, not a topic.** Vague instructions ("research the X shortage") cause subagents to duplicate work and leave gaps. Each delegation needs an objective, an output format, guidance on which tools and sources to use, and explicit boundaries.
- **Scale the swarm to the question.** Simple fact-finding wants one subagent and a handful of tool calls; only genuinely complex work justifies ten or more. Spawning fifty subagents for a trivial query is a real and expensive failure mode, not a hypothetical.

## Verification loops

The defining advantage of an agent is that it can check its own work against the environment — but only if verification is built into the loop rather than hoped for.

- **Prefer environmental verification to self-evaluation.** A passing test, a clean compile, a returned HTTP 200 is ground truth. A model asked "did you do this correctly?" without running anything will frequently say yes regardless. Wire the check to the world, not to the model's opinion.
- **Use a separate evaluator with a rubric for fuzzy criteria.** Where there is no test (research quality, writing, completeness), an evaluator model scoring against an explicit rubric — factual accuracy, completeness, source quality — applied by a *different* call than the one that produced the work catches errors the producer is blind to.
- **Evaluate the system early and small.** A rubric over ~20 representative cases, plus human review for the edge cases automation misses, surfaces systemic bias far sooner than waiting to build a large eval set. Human testers reliably find failure classes that LLM-as-judge does not.

## Pitfalls, by severity

Ordered worst-first — the early items cause wrong or irreversible actions; the later ones only cause waste.

1. **Acting irreversibly on unverified output.** The agent deletes data, sends a transaction, or publishes based on its own un-checked reasoning, at the one moment that cannot be undone. The most dangerous failure. Mitigation: a mandatory human checkpoint before any irreversible or outward-facing action, and verification *before* the action, never after.
2. **No stopping condition.** The loop runs without progress — searching for a nonexistent answer, restating itself, or recursively spawning subagents — compounding cost and error with every iteration. Mitigation: iteration and budget caps, a no-progress detector, and delegation depth proportional to task complexity.
3. **Delegation without a contract.** Subagents launched with a topic instead of an objective, output format, and boundaries duplicate each other's work and leave the goal half-covered while spending the full multi-agent token premium. Mitigation: every delegation carries an explicit brief.
4. **Agentic when a workflow would do.** An autonomous loop used for a task with a predictable path multiplies token cost 4–15× and widens the error surface for zero added capability. The least severe failure — the output can still be correct — but the most pervasive, and the one the simplicity-first progression prevents outright.

## Practical checklist

- Start with a single call; escalate to a workflow, then an agent, only when the simpler form provably fails.
- Justify the 4–15× token premium against the value of the task before choosing an agent.
- Give every loop an explicit stopping condition and a human checkpoint before irreversible actions.
- Plan first, execute second; revise the plan explicitly when the environment contradicts it.
- Make every sub-goal verifiable, and wire verification to the environment, not the model's self-assessment.
- One tool one job; shape arguments so misuse is structurally hard; scope tool output at the source.
- Delegate breadth-first fan-out to subagents with a full contract; keep cross-dependent work in one agent.
- Evaluate early on ~20 cases with a rubric plus human review, not a large eval built too late.

## Related

- [Context engineering](/wiki/ai/context-engineering) — the discipline that sub-agent delegation, tool-result hygiene, and the loop's growing window all depend on.
- [Claude Code](/wiki/ai/context-engineering/claude-code) — the explore–plan–implement–verify loop and sub-agent delegation worked end-to-end on a real task (the section's running example).
- [Prompt engineering](/wiki/ai/prompt-engineering) — wording tool descriptions and the per-step instructions the loop executes.
- [Prompt caching & cost](/wiki/ai/prompt-caching) — why the loop's re-read-everything-each-turn cost makes a stable prefix essential.

## Further reading

- Anthropic, [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Anthropic, [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- Anthropic, [Claude Agent SDK overview](https://docs.claude.com/en/api/agent-sdk/overview)
