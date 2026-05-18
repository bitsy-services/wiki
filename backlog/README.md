# Harness Backlog

Prioritized, contract-shaped design-improvement items for this repo's Claude Code
harness (`.claude/` config, not wiki content). Each item is self-contained: a
fresh session can execute it cold without the context that produced it.

Source: the harness audit in the 2026-05-18 "Claude Code" page session, which
checked this repo against Anthropic's Claude Code best practices, Anthropic's
"Effective context engineering for AI agents," and arXiv:2604.14228.

## How to consume this backlog

1. Pick the highest-priority item with `Status: open`.
2. Start a **fresh** session (`/clear`) — do not inherit unrelated context.
3. Read only that item file; execute its **Proposed fix**.
4. Run its **Verification**; if it passes, set `Status: done` and note the commit.
5. One item per session context. Don't batch unrelated items.

## Items

| # | Priority | Item | Status |
|---|----------|------|--------|
| [001](001-deterministic-enforcement.md) | **P1** | Deterministic enforcement layer (hooks) | open |
| [002](002-right-mechanism-refactor.md)  | P2 | Right-mechanism refactor (skills/agents) | open |
| [003](003-exercise-friction-gc.md)      | P3 | Exercise or simplify the friction GC | open |

P1 is the highest-leverage, smallest change, and closes the trust-then-verify
gap; do it first. P3 is a deferred judgement call, not a code change.

Lives at the repo root (not under `.claude/`, not in `CLAUDE.md`): the backlog
is sometimes-relevant, so per the cheapest-context-first principle it stays out
of always-on context. Discover it by this known path.
