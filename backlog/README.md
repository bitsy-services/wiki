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
| [001](001-deterministic-enforcement.md) | **P1** | Deterministic enforcement layer (hooks) | done (2026-07-12) |
| [002](002-right-mechanism-refactor.md)  | P2 | Right-mechanism refactor (skills/agents) | done (2026-07-12) |
| [003](003-exercise-friction-gc.md)      | P3 | Exercise or simplify the friction GC | done (2026-07-12) |

All three were closed in the 2026-07-12 harness session. The repo now has a
deterministic gate (`scripts/check.sh`, run by a `Stop` hook and by CI), a
write-guard, a load-on-demand skill and reviewer subagent, and a Gen 1 pattern in
memory.

The backlog is empty. Next time friction shows up, add an item here rather than
carrying it in a session.

Lives at the repo root (not under `.claude/`, not in `CLAUDE.md`): the backlog
is sometimes-relevant, so per the cheapest-context-first principle it stays out
of always-on context. Discover it by this known path.
