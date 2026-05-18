---
title: "Claude Code"
weight: 10
---

[Context engineering](/wiki/ai/context-engineering) is a discipline; Claude Code is a harness that implements it. Reading the harness back-to-front is the fastest way to make the discipline concrete, so this page works one real task end to end: **asking Claude Code to write a page for this wiki**. Every principle from the parent page is shown operating on artifacts you can open in this repository, and this same task is the running example reused across the rest of the [AI section](/wiki/ai) — when another page needs "a concrete agentic workload," it means this one.

## The model is the small part

A source-level analysis of Claude Code (≈512K lines, ~1,900 files) found that only **1.6% of the codebase is AI decision logic; the other 98.4% is deterministic infrastructure** — permission gates, the context-management pipeline, tool routing, session persistence, and recovery. The agent loop itself is a plain reason–act–observe `while` loop. Almost everything that determines whether the wiki page comes out well is *plumbing around the model*, and most of that plumbing is the context engineering this section is about. The practical reading: you do not improve results by prompting harder, you improve them by configuring the harness so the right tokens are present and the wrong ones never enter.

## The task, step by step

Type *"write a wiki page on X"* as the first message and a specific chain fires, each step a context-engineering decision:

1. **Intent is resolved from durable instructions, not guessed.** A project rule (`.claude/rules/wiki-workflow.md`) says to treat a first message as a page-creation request. That rule is in the window before the request is, so the agent acts on a convention instead of re-deriving it — durable context doing its job.
2. **Explore before drafting.** The agent reads two or three sibling pages and the rules files to learn the house format. This is [just-in-time retrieval](/wiki/ai/context-engineering#just-in-time-retrieval): the repository is external memory, and only the pages relevant to *this* page are pulled in, not a dump of `content/`.
3. **Plan, then write.** A short plan (sections, path, frontmatter) precedes the draft. Separating exploration from execution keeps the draft from solving the wrong problem and gives compaction something concrete to preserve.
4. **Write to disk early.** The draft becomes a file as soon as it exists, not a long message held in conversation — because the conversation is the volatile part (see compaction below).
5. **Verify against the environment.** `hugo` builds the site. A bad shortcode or malformed frontmatter fails the build; that failure is ground truth, the way a failing test is in [agentic workflows](/wiki/ai/agentic-workflows#verification-loops).

The rest of this page is what makes each step reliable.

## Durable instructions: CLAUDE.md and rules

The highest-leverage context is the [right-altitude instruction](/wiki/ai/context-engineering#right-altitude-instructions) — small, and applied on every turn. Claude Code loads it from a four-level cascade, managed → user → project (`CLAUDE.md`) → local, and delivers it as *user* context rather than a hard system prompt: compliance is probabilistic, which is why emphatic phrasing ("IMPORTANT", "YOU MUST") measurably raises adherence instead of being redundant.

This repository is a live specimen. `CLAUDE.md` carries build commands and structure; `.claude/rules/wiki-content.md` says *"Do not add an `# H1` — Hugo renders the frontmatter title as h1."* That rule is at the right altitude: specific enough to change the output (this page starts at `##` because of it), general enough to apply to every page. The discipline is the pruning test from Anthropic's guide — for each line ask *"would removing this cause a mistake?"* — because a bloated `CLAUDE.md` does not fail loudly; it dilutes attention until the agent quietly ignores the rule you cared about. An over-stuffed instruction file is worse than a short one.

## Pick the cheapest mechanism that works

`CLAUDE.md` is loaded *every* session; that is its power and its cost. Knowledge needed only sometimes — how to write a Solidity example, say — belongs in a [skill](/wiki/ai/context-engineering#just-in-time-retrieval) that loads on demand, not in the always-on file. The extension mechanisms stratify by exactly this context cost:

- **Hooks** — zero context cost; deterministic scripts the harness runs, not text the model reads. Use them for anything that must happen every time without exception (a lint-on-save, a block on writing outside `content/`).
- **Skills** — low cost; a folder of instructions loaded only when relevant. A "draft a wiki page" skill lives here.
- **Plugins / MCP** — medium-to-high cost; whole tool schemas present every turn whether called or not.

The rule that follows: encode a constraint as a hook before a rule, and a rule before a tool, because that order is also cheapest-context-first.

## Subagents keep the drafting window clean

The single strongest lever is [sub-agent isolation](/wiki/ai/context-engineering#sub-agent-context-isolation). "Read every existing AI page and all the rules files and extract the house style" is a wide read that would pour a dozen file bodies into the window the draft has to be written in. Delegated to a subagent, that fan-out happens in a separate context and only a synthesized summary returns — Anthropic reports such returns landing around **1,000–2,000 tokens** versus the tens of thousands the raw reads would cost. The parent keeps the conclusion, not the dump, and starts drafting with a clean budget. The [agentic-workflows](/wiki/ai/agentic-workflows#sub-agent-delegation) rule applies: delegate breadth (a style sweep), keep depth (the actual drafting, which needs the accumulated decisions) in the main agent.

## Memory is structured note-taking with a garbage collector

Anthropic's context-engineering guidance names *structured note-taking* — an external memory file the agent maintains across sessions — as a core long-horizon technique. This repo implements it and goes further: `.claude/memory/` holds a `MEMORY.md` index plus individual fact files, and `.claude/rules/self-improvement.md` runs them through a generational collector — raw friction observations (Gen 0) consolidate into patterns (Gen 1) and, once stable, are promoted to checked-in rules (Gen 2). The context-engineering point is the parent page's rule made operational: *facts that must survive go to a durable artifact, not a conversational aside* that [compaction](/wiki/ai/context-engineering#compaction-and-summarization) will silently discard. A decision about wiki conventions written into memory outlives the session; the same decision mentioned only in chat does not.

## Compaction will eat your draft

Claude Code does not wait for the context limit and then truncate. It runs a graduated pipeline — budget reduction, snipping, microcompaction, context collapse, and finally auto-compaction — degrading lazily as the window fills. Every stage is lossy by design. The consequence for the wiki task is direct and is why step 4 above exists: a half-finished page that lives only as conversation can be summarized into "drafted a page about X" and its actual prose is gone. Mitigations, all instances of the parent page's rules:

- **Externalize the artifact.** Write the page to a file early; the file is outside the window and survives every compaction stage.
- **Front-load conclusions.** State "the page uses sections A/B/C because the sibling pages do" explicitly, so the summarizer keeps a decision rather than reconstructing it.
- **`/clear` between unrelated pages.** Drafting a DeFi page and an AI page in one session is the kitchen-sink failure: each pollutes the other's window for no benefit. One page, one clean context.

## Verify the build, not your memory of it

Claude Code's own guidance calls a verification mechanism *the single highest-leverage thing you can configure*. For this wiki the mechanism is free: `hugo` either builds or it does not. Wire the check to the world. Two habits from [tool-result hygiene](/wiki/ai/context-engineering#tool-result-hygiene) sharpen this:

- **Don't re-read the file you just wrote to "check it."** The write either succeeded or errored; re-reading only duplicates the page in the window and teaches you nothing the build will not.
- **Run the build instead.** It is the environmental ground truth; the agent's recollection of what it wrote is not.

## Pitfalls, by severity

Ordered worst-first — the early items publish wrong content; the later ones only waste budget.

1. **Context poisoning.** The agent invents a Hugo frontmatter key or a shortcode that does not exist, writes it into the page, and — attending to its own prior output as fact — builds the rest of the page around it. Worse on a wiki: a fabricated "further reading" URL or a misattributed research claim looks authoritative and ships. The most dangerous failure because the output is confidently wrong. Mitigation: verify external facts and references against the source before they enter the page, and let the `hugo` build catch invented syntax.
2. **Stale context.** A rule or sibling page is read, then changed (by you, or by the agent earlier in the session), and a later step drafts against the version that no longer exists — a page written to a convention that was just revised. Mitigation: re-read after external changes; trust the harness's file-state tracking over a remembered snapshot.
3. **Over-stuffed durable context.** A `CLAUDE.md` or rules set grown long enough that the wiki-formatting rule is diluted and the agent reintroduces an `# H1`. Pervasive because instruction files only accrete. Mitigation: apply the pruning test on every edit; move sometimes-knowledge to skills.
4. **Unscoped exploration.** "Investigate the wiki before writing" with no scope reads hundreds of pages, fills the window, and starves the draft. The least severe — the page can still be correct — but the most common. Mitigation: scope the read to siblings, or delegate the sweep to a subagent so only the conclusion returns.

## Practical checklist

- Let durable rules resolve intent; don't restate conventions the rules already encode.
- Explore siblings just-in-time; never preload `content/` to "have context."
- Delegate the style sweep to a subagent; keep drafting in the main window.
- Write the draft to disk early — the file survives compaction; the conversation does not.
- Encode constraints cheapest-context-first: hook, then rule, then tool.
- Keep `CLAUDE.md` and rules at the right altitude; run the pruning test on every line.
- Put decisions that must outlive the session in `.claude/memory/`, not in chat.
- Verify with `hugo`; don't re-read the file you just wrote.
- One page per session context; `/clear` before the next.

## Related

- [Context engineering](/wiki/ai/context-engineering) — the discipline this page makes concrete; the budget, curation, compaction, and pitfalls in the abstract.
- [Agentic workflows](/wiki/ai/agentic-workflows) — the explore–plan–implement–verify loop and sub-agent delegation that the wiki task instantiates.
- [Prompt engineering](/wiki/ai/prompt-engineering) — wording the rules and the page request that this harness then routes.
- [Prompt caching & cost](/wiki/ai/prompt-caching) — why keeping `CLAUDE.md` and tool schemas stable at the front of the window is also what makes the session cheap.

## Further reading

- Anthropic, [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices)
- Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Liu, Zhao, Shang & Shen, [Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems](https://arxiv.org/abs/2604.14228) (arXiv:2604.14228)
- Anthropic, [Claude Code memory (CLAUDE.md)](https://code.claude.com/docs/en/memory) and [Subagents](https://code.claude.com/docs/en/sub-agents)
