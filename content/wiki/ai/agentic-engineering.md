---
title: "Agentic Engineering"
weight: 50
---

Agentic engineering is the engineering discipline around systems where a model takes action: building, evaluating, deploying, and operating them. The other pages in this section name what happens inside a single turn or a single loop — [prompt engineering](/wiki/ai/prompt-engineering) wording instructions, [context engineering](/wiki/ai/context-engineering) curating what the model sees, [agentic workflows](/wiki/ai/agentic-workflows) shaping the loop. Agentic engineering is the lifecycle around them: the evals you write before launch, the traces you read after, the guardrails that keep the loop from cashing real money against a bad reasoning chain, the cost work that turns a working prototype into something a team can run on a budget.

The shift in skill set is the headline. Building a non-agentic LLM feature is mostly prompt iteration against a notebook. Building an agentic one is mostly *systems work* — distributed traces, error budgets, replay, evaluation harnesses, permission models — applied to a non-deterministic component with no native debugger. The model is the small part (1.6% of Claude Code's codebase per [the source-level analysis cited under the running example](/wiki/ai/context-engineering/claude-code#the-model-is-the-small-part)); the engineering around it is the rest.

## Where it sits relative to the rest

A decomposition of the discipline, smallest to largest unit of work:

- **Prompt engineering** — one instruction to one model.
- **Context engineering** — what one turn sees and in what order.
- **Agentic workflow design** — what one loop does over multiple turns.
- **Agentic engineering** — what one system does across many loops, users, and weeks.

The pages on the first three are about getting one execution right. This page is about getting a hundred thousand of them right, and noticing within a day when they stop.

## The lifecycle: build, evaluate, deploy, operate

Software has had this lifecycle for decades. The agentic version differs in three places:

- **Build is mostly tools and context, not code.** The model is fixed; you ship by changing what it sees and what it can do. Most of "building an agent" is writing tool contracts, retrieval, system prompts, and rules — work that *looks like* configuration but determines behavior more than the surrounding code does.
- **Evaluate is empirical, not unit-testable.** There is no oracle for "the agent did the right thing." Quality is measured against rubrics, golden tasks, and human review on a sample. Eval design is part of the agent, not an afterthought.
- **Operate is where most failures live.** The agent that passed pre-launch evals will encounter inputs they did not cover, tools whose responses shifted, and prompts users phrase in ways no one anticipated. Observability and a fast rollback path matter more than they do for deterministic code.

Skipping evaluation or observability does not break the prototype — that is the trap. The system runs, it returns plausible answers, and the failures are silent until a user notices. The discipline is to wire both in from the start, even thinly, because retrofitting them after a regression is far more expensive than building them in.

## Evaluation as a first-class artifact

Treat the eval set the way you treat the tests: it ships with the system, it is reviewed, it grows with every interesting bug, and a change is judged against it before merge. Two practical points the [agentic-workflows page](/wiki/ai/agentic-workflows#verification-loops) only touches on:

- **Start with ~20 cases and human review of the edge.** A small set caught early is more valuable than a large one delayed. The first cases come from real or representative tasks, not invented ones, and human review catches the systemic biases that automated scoring misses.
- **LLM-as-judge has known failure modes.** Models are reliable graders on narrow, well-specified rubrics (factual match, format conformance) and unreliable on diffuse ones (writing quality, "helpfulness"). Use them where their judgement is calibrated against humans, not as a generic stand-in for human review.

The eval set is also the safest place to encode regressions. When the agent does the wrong thing in production, the fix is not just a code change; it is a new eval case that pins the corrected behavior down so a later change cannot un-fix it.

## Observability is not optional

A traditional service is debugged by reading logs of deterministic state transitions. An agent's behavior is emergent across a long chain of tool calls, retrieved context, and model decisions, none of which a single log line captures. The minimum useful observability stack:

- **Full traces of every loop** — the prompt, every tool call and result, the model's text at each step, timing. Without this, post-hoc analysis of a failure is guesswork.
- **Replay** — the ability to re-run a specific session with a different prompt, tool, or model and compare. This is what makes an agent debuggable; without replay, every fix is a hope.
- **Aggregate views** — per-tool error rates, per-task token spend, distribution of loop lengths. The tail of long loops is where cost and confusion accumulate, and aggregates surface it before users do.

Pick a tracing layer early; the cost of not having one is paid in incidents you cannot reconstruct. The shape is the same across the open-source options (LangSmith, Langfuse, Phoenix, OpenTelemetry's GenAI conventions): trace tree, span attributes, replay.

## Guardrails and the irreversible-action problem

The [agentic-workflows page](/wiki/ai/agentic-workflows#pitfalls-by-severity) names acting irreversibly on unverified output as the worst failure of an agent. The engineering response is a layered control:

- **Authorize at the tool boundary, not in the prompt.** A tool that can spend money or send a message authenticates and is rate-limited at the harness layer, not gated only by "the system prompt says to ask first." Prompts are advisory; tool boundaries are enforceable.
- **Two-party for the highest-stakes actions.** Some calls — a production deploy, a transaction, a destructive change — require a human approval step the agent cannot bypass. The harness, not the model, owns that gate.
- **Sandboxes for execution.** Code the agent runs goes to an isolated environment with no credentials and a tight egress policy by default. The cost is small; the alternative is a prompt-injection foothold straight into your infrastructure.

Guardrails are the place where security engineering meets agentic engineering. Treat the agent's tool surface like an API exposed to the public internet, because functionally it is one — an attacker who can influence the model's input can influence the agent's actions.

## Cost engineering at scale

A working prototype hides the economics; production exposes them. The levers, roughly in order of yield:

- **[Prompt caching](/wiki/ai/prompt-caching).** A stable prefix — system prompt, tool definitions, durable rules — at the front of the window is the single largest source of savings on a busy system. Worth the architectural discipline.
- **Right-sized models per step.** Route classification and small structured calls to a cheaper model; reserve the flagship for the steps that need it. Most pipelines have at least one step that is over-modeled.
- **Bounded loops.** Iteration caps and budget caps are cost controls as much as safety controls. A loop with no ceiling is a billing incident waiting for the wrong input.
- **Workflows over agents when possible.** The 4–15× token multiple noted under [agentic workflows](/wiki/ai/agentic-workflows#when-an-agent-earns-its-overhead) is the single biggest cost decision, and the one most often made wrong.

The discipline is to measure cost the way you measure latency — per request, per task, per tenant — and to track it as a first-class signal, not a monthly surprise on the invoice.

## The team shape

Agentic systems sit between three skill sets that rarely live in one person: applied AI for evaluation and model behavior, software engineering for the harness, and domain expertise for what "correct" looks like. A team that ships agents well usually has all three represented, with shared ownership of the eval set as the artifact that forces them to agree. A team missing one of the three predictably under-invests in the corresponding work — pure software teams ship with thin evals; pure ML teams ship with weak harnesses; pure domain teams ship with both.

## Pitfalls, by severity

Ordered worst-first — the early items ship wrong behavior into production; the later ones only waste effort.

1. **No evaluation, only vibes.** The agent is judged by ad-hoc demos and the team's recent interactions, not a stable set of cases. Regressions ship undetected and the only signal is user complaints. The most dangerous failure because it has no detection mechanism. Mitigation: a small eval set from day one, grown with every fixed bug.
2. **Guardrails in the prompt instead of the harness.** Authorization for high-stakes actions encoded in "ask before doing X" rather than at the tool boundary. A prompt-injected input or a confused loop bypasses it. Mitigation: enforce at the tool layer; treat prompt-level rules as defense in depth, not the primary control.
3. **No observability.** Production failures are unreplayable; the team debugs from screenshots and recollection. The fix rate collapses because root-causing takes days. Mitigation: trace every loop end to end from the first deploy, even with a thin stack.
4. **Cost discovered in production.** No per-request cost metric, no iteration cap, no caching strategy. The bill arrives as the first signal. Mitigation: cost as a first-class metric, with caps and caching from day one.

## Practical checklist

- Treat the eval set as a shipped artifact; start small, grow it with every fix.
- Trace every loop end-to-end and make replay a first-class capability.
- Enforce high-stakes guardrails at the tool boundary, not in the prompt.
- Cache the stable prefix, right-size models per step, cap iterations and budgets.
- Pick the workflow over the agent unless the path is genuinely unpredictable.
- Wire all of this in from the start, thinly — the cost of retrofit is far higher than the cost of building it small early.

## Related

- [Context engineering](/wiki/ai/context-engineering) — managing what each turn sees; a sub-discipline of this one.
- [Prompt engineering](/wiki/ai/prompt-engineering) — wording the instructions the loop executes.
- [Agentic workflows](/wiki/ai/agentic-workflows) — the patterns this discipline composes into a running system.
- [Prompt caching & cost](/wiki/ai/prompt-caching) — the economics that make cost engineering a tractable problem.
- [Claude Code](/wiki/ai/context-engineering/claude-code) — a real harness exhibiting the build, observe, guard, and verify properties this page argues for.

## Further reading

- Anthropic, [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- Anthropic, [Claude Agent SDK overview](https://docs.claude.com/en/api/agent-sdk/overview)
- Anthropic, [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- OpenTelemetry, [GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
